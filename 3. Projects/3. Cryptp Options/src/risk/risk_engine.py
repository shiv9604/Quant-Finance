"""
Risk Engine — non-negotiable exit layer.

Strategy SUGGESTS exits. Risk Engine has final authority.
Every active position passes through here on every cycle.

Checks (in order of priority):
  1. Hard SL: combined premium >= entry * (1 + sl_pct)
  2. Strategy exit signal (premium rebuild, etc.)
  3. Forced time exit (17:25 IST)
  Commented as of now : 4. Global daily loss limit

Adding a new risk rule = add a method here and call it in should_exit().
"""

from datetime import datetime, timezone, timedelta
from typing import Tuple

from src.config import config
from src.core.strategy import ExitSignal
from src.state.position import Position


IST = timezone(timedelta(hours=5, minutes=30))


class RiskEngine:

    def should_exit(
        self,
        position: Position,
        strategy_signal: ExitSignal,
    ) -> Tuple[bool, str]:
        """
        Returns (should_exit: bool, reason: str).

        Called every loop cycle while a position is active.
        Checks are ordered: fastest/most critical first.
        """
        # 1. Hard stop-loss (highest priority — non-negotiable)
        sl_hit, sl_reason = self.check_stop_loss(position)
        if sl_hit:
            return True, sl_reason

        # 2. Strategy-suggested exit (e.g. premium rebuild)
        if strategy_signal.should_exit:
            return True, strategy_signal.reason

        # 3. Forced time exit
        forced, forced_reason = self.check_forced_exit()
        if forced:
            return True, forced_reason

        # 4. Global daily loss limit
        # limit_hit, limit_reason = self.check_global_risk(position)
        # if limit_hit:
        #     return True, limit_reason

        return False, "none"

    # ── Individual checks ─────────────────────────────────────────────────────

    def check_stop_loss(self, position: Position) -> Tuple[bool, str]:
        """
        SL triggers when combined mark premium has risen >= sl_pct above entry.
        e.g. entry_premium = $100, sl_pct = 0.80 → exit if current_premium >= $180.

        The position tracks mark prices — this fires before actual P&L loss is realised.
        """
        if position.entry_premium <= 0:
            return False, "none"

        loss_pct = (
            position.current_premium - position.entry_premium
        ) / position.entry_premium
        if loss_pct >= config.sl_pct:
            return True, f"sl_hit:{loss_pct*100:.1f}%"

        return False, "none"

    def check_forced_exit(self) -> Tuple[bool, str]:
        if config.test_mode:
            return False, "none"
        now_ist = datetime.now(IST).time()
        if now_ist >= config.forced_exit:
            return True, "forced_time"
        return False, "none"

    def check_global_risk(self, position: Position) -> Tuple[bool, str]:
        """
        Stop trading for the day if cumulative daily losses exceed max_daily_loss.
        Uses position.daily_pnl_usd which accumulates across trades.
        """
        # Include unrealised loss on current position
        unrealised = (position.entry_premium - position.current_premium) * position.size
        total_day_pnl = position.daily_pnl_usd + unrealised

        if total_day_pnl <= -config.max_daily_loss:
            return True, f"daily_limit:{total_day_pnl:.2f}usd"

        return False, "none"

    # ── Entry risk gate ───────────────────────────────────────────────────────

    def can_enter(self, position: Position) -> Tuple[bool, str]:
        """
        Pre-entry checks called before placing a new strangle.
        Returns (allowed: bool, reason: str).
        """
        # Already in a trade
        if position.active:
            return False, "position_active"

        ist = datetime.now(IST)
        today_str = ist.strftime("%Y-%m-%d")
        if position.exit_time and today_str in position.exit_time:
            return False, "already_traded_today"

        # Daily loss already hit (from prior trades today)
        # if position.daily_pnl_usd <= -config.max_daily_loss:
        #     return False, f"daily_limit_reached:{position.daily_pnl_usd:.2f}usd"

        # Entry window check (belt-and-suspenders)
        now_ist = datetime.now(IST).time()
        if not config.test_mode and not (config.scan_from <= now_ist <= config.scan_to):
            return False, "outside_entry_window"

        return True, "ok"
