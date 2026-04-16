"""
Long Volatility Strategy — stub for future implementation.

Buying straddles / strangles when IV is low and a breakout is expected.
Entry: low IV environment, buy ATM CE + PE
Exit: when combined premium expands significantly (target 50–100% gain)
"""

from src.core.strategy import Strategy, EntrySignal, ExitSignal
from src.data.market_data import MarketSnapshot
from src.state.position import Position


class LongVolStrategy(Strategy):

    def evaluate_entry(self, market: MarketSnapshot, position: Position) -> EntrySignal:
        # TODO: implement long vol entry logic
        raise NotImplementedError("LongVolStrategy not yet implemented")

    def evaluate_exit(self, market: MarketSnapshot, position: Position) -> ExitSignal:
        # TODO: implement long vol exit logic
        raise NotImplementedError("LongVolStrategy not yet implemented")
