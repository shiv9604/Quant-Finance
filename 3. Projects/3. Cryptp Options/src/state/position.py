"""
Active trade state — single source of truth for the current position.

Persisted to JSON after every mutation so a process restart
resumes cleanly without re-entering an already-live position.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


STATE_FILE = os.path.join("logs", "state.json")


@dataclass
class Position:
    # Is a trade currently open?
    active: bool = False

    # Entry details
    entry_time: str = ""  # ISO string, IST
    ce_symbol: str = ""
    pe_symbol: str = ""
    ce_entry_price: float = 0.0
    pe_entry_price: float = 0.0
    entry_premium: float = 0.0  # combined CE + PE at entry
    size: float = 0.0  # lot size

    # Live tracking (updated each loop)
    current_premium: float = 0.0  # combined CE + PE mark price now
    prev_premium: float = 0.0  # previous cycle's combined premium
    consec_rises: int = 0  # consecutive minutes premium has risen
    peak_pnl_pct: float = 0.0  # best PnL % reached so far

    # Exit details (filled after close)
    exit_time: str = ""
    exit_reason: str = ""
    exit_pnl_usd: float = 0.0
    exit_pnl_pct: float = 0.0

    # Daily tracking
    daily_pnl_usd: float = 0.0  # cumulative P&L for today


class PositionStore:
    """
    Loads and saves Position to disk.
    Always call save() after mutating state so restarts are safe.
    """

    def __init__(self, path: str = STATE_FILE):
        self._path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def load(self) -> Position:
        """Load position from disk. Returns blank Position if file missing."""
        if not os.path.exists(self._path):
            return Position()
        try:
            with open(self._path, "r") as f:
                data = json.load(f)
            return Position(
                **{k: v for k, v in data.items() if k in Position.__dataclass_fields__}
            )
        except Exception:
            return Position()

    def save(self, pos: Position) -> None:
        """Persist current state to disk."""
        with open(self._path, "w") as f:
            json.dump(asdict(pos), f, indent=2)

    def reset(self) -> Position:
        """Clear state — call after confirmed exit."""
        blank = Position()
        self.save(blank)
        return blank

    def open(
        self,
        ce_symbol: str,
        pe_symbol: str,
        ce_price: float,
        pe_price: float,
        size: float,
        entry_time: str,
        daily_pnl_so_far: float = 0.0,
    ) -> Position:
        """Build and persist an entry state."""
        combined = ce_price + pe_price
        pos = Position(
            active=True,
            entry_time=entry_time,
            ce_symbol=ce_symbol,
            pe_symbol=pe_symbol,
            ce_entry_price=ce_price,
            pe_entry_price=pe_price,
            entry_premium=combined,
            size=size,
            current_premium=combined,
            prev_premium=combined,
            consec_rises=0,
            peak_pnl_pct=0.0,
            daily_pnl_usd=daily_pnl_so_far,
        )
        self.save(pos)
        return pos

    def update_mark(self, pos: Position, ce_mark: float, pe_mark: float) -> Position:
        """Update live premium tracking and consecutive-rise counter."""
        combined = ce_mark + pe_mark

        if combined > pos.prev_premium:
            pos.consec_rises += 1
        else:
            pos.consec_rises = 0

        pnl_pct = (
            (pos.entry_premium - combined) / pos.entry_premium * 100
            if pos.entry_premium > 0
            else 0.0
        )
        if pnl_pct > pos.peak_pnl_pct:
            pos.peak_pnl_pct = pnl_pct

        pos.prev_premium = pos.current_premium
        pos.current_premium = combined
        self.save(pos)
        return pos

    def close(
        self,
        pos: Position,
        exit_reason: str,
        exit_time: str,
        pnl_usd: float,
        pnl_pct: float,
    ) -> Position:
        """Record exit details and deactivate position."""
        pos.active = False
        pos.exit_time = exit_time
        pos.exit_reason = exit_reason
        pos.exit_pnl_usd = pnl_usd
        pos.exit_pnl_pct = pnl_pct
        pos.daily_pnl_usd += pnl_usd
        self.save(pos)
        return pos
