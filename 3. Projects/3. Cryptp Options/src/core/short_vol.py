"""
Short Volatility Strategy.
Implements the backtested short strangle system:
  - Enter during 13:15–15:30 IST when intraday volatility stalls
  - Select OTM CE and PE on today's expiry
  - Exit on premium rebuild signal (risk engine handles SL + forced exit)

All backtester parameters are inherited from config.
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Optional

from src.config import config
from src.core.strategy import Strategy, EntrySignal, ExitSignal
from src.data.market_data import MarketSnapshot, OptionTick
from src.state.position import Position


IST = timezone(timedelta(hours=5, minutes=30))


class ShortVolStrategy(Strategy):

    def evaluate_entry(self, market: MarketSnapshot, position: Position) -> EntrySignal:
        """
        Entry criteria (all must be true):
        1. Current IST time is within scan window
        2. No active position today
        3. Volatility signal: chain IV is above threshold
        4. Liquid OTM CE and PE exist with non-zero mark price
        """
        now_ist = datetime.now(IST).time()

        # Guard 1: time window
        if not config.test_mode and not (config.scan_from <= now_ist <= config.scan_to):
            return EntrySignal(False, reason="outside_scan_window")

        # Guard 2: already in a trade
        if position.active:
            return EntrySignal(False, reason="position_already_active")

        # Guard 3: volatility signal — at least some OTM options with reasonable IV
        vol_ok, avg_iv = self._has_vol_signal(market)
        if not vol_ok:
            return EntrySignal(
                False,
                reason=f"no_vol_signal spot={avg_iv:.0f}",
            )

        # Guard 4: find valid strikes
        ce, pe = self._select_strikes(market.spot, market.chain)
        if ce is None or pe is None:
            return EntrySignal(False, reason="no_liquid_strikes")

        return EntrySignal(
            should_enter=True,
            ce_symbol=ce.symbol,
            pe_symbol=pe.symbol,
            ce_ref_price=ce.mark_price,
            pe_ref_price=pe.mark_price,
            reason=f"vol_signal spot={market.spot:.0f} ce={ce.strike:.0f} pe={pe.strike:.0f}",
        )

    def evaluate_exit(self, market: MarketSnapshot, position: Position) -> ExitSignal:
        """
        Strategy-side exit: premium rebuild.
        If combined premium has risen N consecutive cycles → new move starting, exit.
        (SL and forced-time exit are handled by risk engine, not here.)
        """
        if not position.active:
            return ExitSignal(False)

        if position.consec_rises >= config.prem_rebuild_n:
            return ExitSignal(True, reason="prem_rebuild")

        return ExitSignal(False)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _has_vol_signal(self, market: MarketSnapshot) -> tuple[bool, float]:
        vol = market.vol_signal
        return vol.get("found", False), vol.get("spot_price", 0.0)

    def _select_strikes(
        self,
        spot: float,
        chain: list[OptionTick],
    ) -> tuple[Optional[OptionTick], Optional[OptionTick]]:
        """
        Select the nearest OTM CE and PE that are:
        - At least config.strike_offset points away from spot
        - Have a positive mark price (liquid)

        Mirrors backtester zone_range selection logic.
        """
        min_offset = config.strike_offset

        # OTM calls: strike >= spot + offset, sorted nearest first
        otm_calls = sorted(
            [
                t
                for t in chain
                if t.option_type == "call"
                and t.strike >= spot + min_offset
                and t.mark_price > 0
            ],
            key=lambda t: t.strike,
        )

        # OTM puts: strike <= spot - offset, sorted nearest first (highest strike first)
        otm_puts = sorted(
            [
                t
                for t in chain
                if t.option_type == "put"
                and t.strike <= spot - min_offset
                and t.mark_price > 0
            ],
            key=lambda t: t.strike,
            reverse=True,
        )

        ce = otm_calls[0] if otm_calls else None
        pe = otm_puts[0] if otm_puts else None
        return ce, pe
