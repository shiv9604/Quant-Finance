"""
Base strategy interface.
Every strategy must implement evaluate_entry and evaluate_exit.

Adding a new strategy = create a new file in src/core/ and subclass Strategy.
The rest of the system (risk, execution, main loop) never changes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

from src.data.market_data import MarketSnapshot
from src.state.position import Position


@dataclass
class EntrySignal:
    should_enter: bool
    ce_symbol: str = ""
    pe_symbol: str = ""
    ce_ref_price: float = 0.0  # suggested limit price for CE leg
    pe_ref_price: float = 0.0  # suggested limit price for PE leg
    reason: str = ""  # why entry was triggered (for diag log)


@dataclass
class ExitSignal:
    should_exit: bool
    reason: str = "none"  # "sl_hit" | "prem_rebuild" | "forced_time" | "none"


class Strategy(ABC):
    """
    Pluggable strategy interface.

    Strategy SUGGESTS entry and exit.
    Risk engine has final veto on exits.
    Execution layer acts on confirmed decisions.
    """

    @abstractmethod
    def evaluate_entry(
        self,
        market: MarketSnapshot,
        position: Position,
    ) -> EntrySignal:
        """
        Called every loop cycle when no position is active.
        Returns EntrySignal with should_enter=True and selected strikes
        if conditions are met.
        """
        ...

    @abstractmethod
    def evaluate_exit(
        self,
        market: MarketSnapshot,
        position: Position,
    ) -> ExitSignal:
        """
        Called every loop cycle when a position is active.
        Strategy can suggest an exit (e.g. premium rebuild detected).
        Risk engine will also run its own checks independently.
        """
        ...
