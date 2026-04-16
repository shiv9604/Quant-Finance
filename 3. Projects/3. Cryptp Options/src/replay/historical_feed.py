"""
Historical data feed for replay testing.
Replicates the backtester's data loading logic and exposes the same
interface as MarketData so the live strategy/risk code runs unchanged.
"""

import os
import glob
import datetime
from typing import Optional

import pandas as pd

from src.data.market_data import MarketData, MarketSnapshot, OptionTick
from src.logs.logger import logger

SPOT_DIR = "data/BTCUSD/spot"
OPTIONS_DIR = "data/BTCUSD/options"
EXCEL_CACHE = os.path.join(SPOT_DIR, "BTCUSDT_1m_combined.xlsx")

BINANCE_COLS = [
    "open_time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "close_time",
    "quote_vol",
    "trades",
    "taker_base",
    "taker_quote",
    "ignore",
]


def _load_spot_df() -> pd.DataFrame:
    """Load combined 1-min spot data (same as backtester)."""
    if os.path.exists(EXCEL_CACHE):
        raw = pd.read_excel(EXCEL_CACHE)
        raw["DateTime"] = pd.to_datetime(raw["DateTime"], utc=True)
    else:
        files = sorted(glob.glob(os.path.join(SPOT_DIR, "BTCUSDT-1m-*.csv")))
        if not files:
            raise FileNotFoundError(f"No 1-minute CSV files in {SPOT_DIR}")
        chunks = []
        for f in files:
            tmp = pd.read_csv(f, header=None, names=BINANCE_COLS)
            sample = tmp["open_time"].dropna().iloc[0]
            unit = "us" if sample > 1e14 else "ms"
            tmp["DateTime"] = pd.to_datetime(
                tmp["open_time"], unit=unit, utc=True, errors="coerce"
            )
            chunks.append(tmp)
        raw = pd.concat(chunks, ignore_index=True)
        raw.dropna(subset=["DateTime"], inplace=True)
        raw.sort_values("DateTime", inplace=True)
        raw.drop_duplicates(subset="DateTime", inplace=True)

    df = raw[["DateTime", "Open", "High", "Low", "Close", "Volume"]].copy()
    df["DateTime"] = pd.to_datetime(df["DateTime"], utc=True)
    df.set_index("DateTime", inplace=True)
    df.index = df.index.tz_convert("Asia/Kolkata")
    df = df.apply(pd.to_numeric, errors="coerce")
    df["Date"] = df.index.date
    df["Time"] = df.index.time
    return df


def _load_options_for_date(date: pd.Timestamp, spot: float) -> pd.DataFrame:
    """Load + resample options ticks to 1-min close (same as backtester)."""
    ym = date.strftime("%Y-%m")
    filepath = os.path.join(OPTIONS_DIR, f"BTC_{ym}.csv")
    if not os.path.exists(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
    df["timestamp"] = (
        df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
    )
    df = df[df["timestamp"].dt.date == date.date()].copy()
    if df.empty:
        return pd.DataFrame()

    def _parse(sym):
        parts = sym.split("-")
        return {
            "opt_type": "call" if parts[0] == "C" else "put",
            "strike": float(parts[2]),
            "expiry_str": f"20{parts[3][4:6]}-{parts[3][2:4]}-{parts[3][:2]}",
        }

    parsed = df["product_symbol"].apply(_parse)
    df["option_type"] = parsed.apply(lambda x: x["opt_type"])
    df["strike"] = parsed.apply(lambda x: x["strike"])
    df["expiry_str"] = parsed.apply(lambda x: x["expiry_str"])
    df = df[df["strike"].between(spot - 5000, spot + 5000)]

    df["time"] = df["timestamp"].dt.floor("1min").dt.time
    df_1m = (
        df.groupby(["expiry_str", "strike", "option_type", "time"])["price"]
        .last()
        .reset_index()
        .rename(columns={"price": "close"})
    )
    return df_1m


class HistoricalFeed:
    """
    Replays historical data day by day, minute by minute.
    Exposes get_snapshot() matching the MarketData interface.
    """

    def __init__(self):
        print("Loading spot data...")
        self._spot_df = _load_spot_df()
        self._opt_cache: dict = {}  # date string → options DataFrame
        self._current_date: Optional[pd.Timestamp] = None
        self._current_time: Optional[datetime.time] = None
        self._current_spot: float = 0.0

    def set_cursor(self, date: pd.Timestamp, time: datetime.time, spot: float):
        """Set the replay cursor to a specific date/time before calling get_snapshot."""
        self._current_date = date
        self._current_time = time
        self._current_spot = spot

        date_str = str(date.date())
        if date_str not in self._opt_cache:
            self._opt_cache[date_str] = _load_options_for_date(date, spot)

    def get_snapshot(self, asset: str = "BTC") -> MarketSnapshot:
        """Build a MarketSnapshot from historical data at the current cursor."""
        date = self._current_date
        time = self._current_time
        spot = self._current_spot
        opt_df = self._opt_cache.get(str(date.date()), pd.DataFrame())

        # Build option chain at current time
        chain = []
        if not opt_df.empty:

            expiries = pd.to_datetime(opt_df["expiry_str"].unique())
            future = sorted([e for e in expiries if e.date() >= date.date()])
            if future:
                nearest_expiry = str(future[0].date())
                opt_df_exp = opt_df[opt_df["expiry_str"] == nearest_expiry]
            else:
                opt_df_exp = pd.DataFrame()
            at_time = (
                opt_df_exp[opt_df_exp["time"] <= time]
                if not opt_df_exp.empty
                else pd.DataFrame()
            )
            for _, row in at_time.drop_duplicates(
                subset=["strike", "option_type"], keep="last"
            ).iterrows():
                expiry_ddmmyy = row["expiry_str"].replace("-", "")[
                    2:
                ]  # YYYYMMDD → DDMMYY
                expiry_ddmmyy = (
                    row["expiry_str"][8:10]
                    + row["expiry_str"][5:7]
                    + row["expiry_str"][2:4]
                )
                sym = (
                    f"{'C' if row['option_type'] == 'call' else 'P'}"
                    f"-BTC-{int(row['strike'])}-{expiry_ddmmyy}"
                )
                chain.append(
                    OptionTick(
                        symbol=sym,
                        strike=row["strike"],
                        option_type=row["option_type"],
                        expiry=expiry_ddmmyy,
                        mark_price=float(row["close"]),
                        ltp=float(row["close"]),
                        bid=float(row["close"]) * 0.99,
                        ask=float(row["close"]) * 1.01,
                        iv=0.0,
                        delta=0.0,
                    )
                )

        vol_signal = self._detect_vol_signal(date, time)
        ts = f"{date.date()} {time} IST"
        return MarketSnapshot(
            spot=spot, chain=chain, snapshot_ts=ts, vol_signal=vol_signal
        )

    def get_combined_premium(
        self, ce_symbol: str, pe_symbol: str
    ) -> tuple[float, float]:
        """Return current historical mark prices for both legs."""
        date = self._current_date
        time = self._current_time
        opt_df = self._opt_cache.get(str(date.date()), pd.DataFrame())
        if opt_df.empty:
            return 0.0, 0.0

        def _get_price(symbol: str) -> float:
            parts = symbol.split("-")
            opt_type = "call" if parts[0] == "C" else "put"
            strike = float(parts[2])
            ddmmyy = parts[3]  # e.g. "011224"
            expiry_str = f"20{ddmmyy[4:6]}-{ddmmyy[2:4]}-{ddmmyy[:2]}"  # → "2024-12-01"
            rows = opt_df[
                (opt_df["option_type"] == opt_type)
                & (opt_df["strike"] == strike)
                & (opt_df["expiry_str"] == expiry_str)
                & (opt_df["time"] <= time)
            ]
            if rows.empty:
                return 0.0
            return float(rows.iloc[-1]["close"])

        return _get_price(ce_symbol), _get_price(pe_symbol)

    def get_spot_at(self, date: pd.Timestamp, time: datetime.time) -> float:
        """Return spot close price at a specific date/time."""
        day = self._spot_df[self._spot_df["Date"] == date.date()]
        at_time = day[day["Time"] <= time]
        if at_time.empty:
            return 0.0
        return float(at_time.iloc[-1]["Close"])

    def get_trading_days(self, start: str, end: str) -> list:
        """Return sorted list of dates with spot data in the range."""
        mask = (self._spot_df["Date"] >= pd.Timestamp(start).date()) & (
            self._spot_df["Date"] <= pd.Timestamp(end).date()
        )
        return sorted(self._spot_df[mask]["Date"].unique())

    def get_minutes_for_day(
        self,
        date,
        from_time: datetime.time,
        to_time: datetime.time,
    ) -> list[datetime.time]:
        """Return all 1-min timestamps for a date within the scan window."""
        day = self._spot_df[self._spot_df["Date"] == date]
        window = day[(day["Time"] >= from_time) & (day["Time"] <= to_time)]
        return list(window["Time"].values)

    # ── Vol signal (matches _detect_vol_signal in market_data.py) ────────────

    def _detect_vol_signal(
        self, date: pd.Timestamp, current_time: datetime.time
    ) -> dict:
        scan_from = datetime.time(13, 15)
        day = self._spot_df[self._spot_df["Date"] == date.date()]
        window = day[(day["Time"] >= scan_from) & (day["Time"] <= current_time)]

        if len(window) < 3:
            return {"found": False}

        # Resample to 5-min candles
        window_idx = window.copy()
        window_idx.index = pd.to_datetime(
            window_idx.index if hasattr(window_idx.index, "tz") else window_idx.index
        )
        candles_5m = (
            window.reset_index()
            .set_index("DateTime")
            .resample("5min")
            .agg(
                open=("Open", "first"),
                high=("High", "max"),
                low=("Low", "min"),
                close=("Close", "last"),
            )
            .dropna()
            .reset_index()
        )

        if len(candles_5m) < 3:
            return {"found": False}

        min_range_pts = 200.0
        atr_threshold = 100.0
        body_threshold = 75.0
        min_candles = 3

        for i in range(len(candles_5m) - min_candles + 1):
            w = candles_5m.iloc[i : i + min_candles]
            zone_range = w["high"].max() - w["low"].min()

            trs = []
            for j in range(len(w)):
                row = w.iloc[j]
                prev_close = w.iloc[j - 1]["close"] if j > 0 else row["open"]
                trs.append(
                    max(
                        row["high"] - row["low"],
                        abs(row["high"] - prev_close),
                        abs(row["low"] - prev_close),
                    )
                )
            avg_atr = sum(trs) / len(trs)
            max_body = (w["close"] - w["open"]).abs().max()

            if (
                zone_range >= min_range_pts
                and avg_atr >= atr_threshold
                and max_body >= body_threshold
            ):
                spot_price = float(w.iloc[-1]["close"])
                return {"found": True, "spot_price": spot_price}

        return {"found": False}
