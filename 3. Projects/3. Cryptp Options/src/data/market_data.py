"""
Market data layer.
Single responsibility: fetch and normalise live market prices.

Exposes a clean, strategy-friendly interface.
All Delta Exchange response parsing stays here — the rest of the system
never touches raw API dicts.
"""

from datetime import date, timedelta, timezone, datetime
from typing import Optional

from src.config import config
from src.execution.broker import DeltaBroker
from src.logs.logger import logger
from dataclasses import dataclass, field


@dataclass
class OptionTick:
    symbol: str
    strike: float
    option_type: str  # "call" | "put"
    expiry: str  # DDMMYY string as used in Delta symbols
    mark_price: float
    ltp: float  # last traded price
    bid: float
    ask: float
    iv: float  # implied volatility (decimal, e.g. 0.65)
    delta: float


@dataclass
class MarketSnapshot:
    spot: float
    chain: list[OptionTick]
    snapshot_ts: str  # IST timestamp string
    vol_signal: dict = field(default_factory=dict)


class MarketData:

    def __init__(self, broker: DeltaBroker):
        self._broker = broker

    # ── Public interface ──────────────────────────────────────────────────────

    def get_spot(self, perp_symbol: str | None = None) -> float:
        symbol = perp_symbol or config.spot_symbol
        ticker = self._broker.get_spot_ticker(symbol)
        price = float(
            ticker.get("mark_price")
            or ticker.get("close")
            or ticker.get("last_price")
            or 0
        )
        if price == 0:
            raise ValueError(
                f"Could not read spot price for '{symbol}'. "
                f"Ticker returned: {ticker}. "
                f"Run src/discover.py to find the correct symbol."
            )
        return price

    def get_option_price(self, symbol: str) -> float:
        """
        Return current mark price for a single option symbol.
        e.g. symbol = 'C-BTC-105000-150125'
        """
        ticker = self._broker.get_ticker(symbol)
        mark = float(ticker.get("mark_price") or 0)
        return mark

    def get_combined_premium(
        self, ce_symbol: str, pe_symbol: str
    ) -> tuple[float, float]:
        """
        Fetch mark prices for both legs.
        Returns (ce_mark, pe_mark).
        """
        ce_mark = self.get_option_price(ce_symbol)
        pe_mark = self.get_option_price(pe_symbol)
        return ce_mark, pe_mark

    def get_snapshot(self, asset: str = "BTC") -> MarketSnapshot:
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)

        # After 17:30 IST today's options have expired — request next day's expiry
        expiry_cutoff = now_ist.replace(hour=17, minute=30, second=0, microsecond=0)
        if now_ist >= expiry_cutoff:
            expiry_date = (now_ist + timedelta(days=1)).date()
        else:
            expiry_date = now_ist.date()

        expiry_str = expiry_date.strftime("%d-%m-%Y")

        spot = self.get_spot()
        raw = self._broker.get_option_chain(asset, expiry_str)
        chain = [self._parse_tick(t) for t in raw if self._parse_tick(t) is not None]

        ts = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
        vol_signal = self._detect_vol_signal()
        return MarketSnapshot(
            spot=spot, chain=chain, snapshot_ts=ts, vol_signal=vol_signal
        )

    def _detect_vol_signal(self) -> dict:
        """Replicates backtester detect_peak_volatility_btc using live 5-min candles."""
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)
        scan_from = now_ist.replace(hour=13, minute=15, second=0, microsecond=0)

        candles = self._broker.get_candles(
            config.spot_symbol,
            "5m",
            int(scan_from.timestamp()),
            int(now_ist.timestamp()),
        )
        if len(candles) < 3:
            return {"found": False}

        min_range_pts = 200.0
        atr_threshold = 100.0
        body_threshold = 75.0
        min_candles = 3

        for i in range(len(candles) - min_candles + 1):
            w = candles[i : i + min_candles]
            highs = [c["high"] for c in w]
            lows = [c["low"] for c in w]
            opens = [c["open"] for c in w]
            closes = [c["close"] for c in w]

            trs = []
            for j, c in enumerate(w):
                prev_close = w[j - 1]["close"] if j > 0 else c["open"]
                trs.append(
                    max(
                        c["high"] - c["low"],
                        abs(c["high"] - prev_close),
                        abs(c["low"] - prev_close),
                    )
                )

            zone_range = max(highs) - min(lows)
            avg_atr = sum(trs) / len(trs)
            max_body = max(abs(c["close"] - c["open"]) for c in w)

            if (
                zone_range >= min_range_pts
                and avg_atr >= atr_threshold
                and max_body >= body_threshold
            ):
                spot_price = w[-1]["close"]
                return {"found": True, "spot_price": spot_price}

        return {"found": False}

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_tick(raw: dict) -> Optional[OptionTick]:
        """
        Convert a raw Delta ticker dict into a clean OptionTick.
        Returns None if essential fields are missing.
        """
        try:
            symbol = raw.get("symbol", "")
            # Symbol format: C-BTC-105000-150125  or  P-BTC-104600-150125
            parts = symbol.split("-")
            if len(parts) < 4:
                return None

            opt_type = "call" if parts[0] == "C" else "put"
            strike = float(parts[2])
            expiry = parts[3]  # DDMMYY

            # greeks nested under 'greeks' key in some responses
            greeks = raw.get("greeks") or {}
            iv_raw = (
                raw.get("implied_volatility") or raw.get("iv") or greeks.get("vega", 0)
            )
            delta_v = float(greeks.get("delta") or 0)

            return OptionTick(
                symbol=symbol,
                strike=strike,
                option_type=opt_type,
                expiry=expiry,
                mark_price=float(raw.get("mark_price") or 0),
                ltp=float(raw.get("close") or raw.get("ltp") or 0),
                bid=float(
                    (raw.get("quotes") or {}).get("best_bid")
                    or raw.get("best_bid")
                    or 0
                ),
                ask=float(
                    (raw.get("quotes") or {}).get("best_ask")
                    or raw.get("best_ask")
                    or 0
                ),
                iv=float(iv_raw) if iv_raw else 0.0,
                delta=delta_v,
            )
        except Exception as e:
            logger.error(f"Failed to parse option tick: {raw.get('symbol')}", exc=e)
            return None

    @staticmethod
    def today_expiry_label() -> str:
        ist = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist)
        cutoff = now_ist.replace(hour=17, minute=30, second=0, microsecond=0)
        if now_ist >= cutoff:
            return (now_ist + timedelta(days=1)).strftime("%d%m%y")
        return now_ist.strftime("%d%m%y")
