"""
Paper broker for replay testing.
Simulates order fills at historical prices — no API calls.
Implements the same interface as DeltaBroker.
"""

import time as _time


class PaperBroker:
    """
    Drop-in replacement for DeltaBroker during replay.
    Fills are injected by the replay runner via set_fill_price().
    """

    def __init__(self):
        self._dry_run = False  # tells OrderManager to poll (we override fills)
        self._fill_prices: dict = {}  # order_id → fill price
        self._order_counter = 1000

    def set_fill_price(self, order_id, price: float):
        """Called by replay runner to register what price an order fills at."""
        self._fill_prices[order_id] = price

    # ── Order management ─────────────────────────────────────────────────────

    def place_order(
        self,
        symbol: str,
        side: str,
        size: float,
        order_type: str = "market_order",
        limit_price=None,
        post_only: bool = False,
    ) -> dict:
        order_id = self._order_counter
        self._order_counter += 1
        # Fill immediately at the price registered by replay runner
        fill_price = self._fill_prices.get(order_id, 0.0)
        return {
            "id": order_id,
            "state": "open",
            "product_symbol": symbol,
            "size": size,
            "side": side,
        }

    def get_order(self, order_id) -> dict:
        """Return closed order with registered fill price."""
        fill_price = self._fill_prices.get(order_id, 0.0)
        return {
            "id": order_id,
            "state": "closed",
            "unfilled_size": 0,
            "avg_fill_price": str(fill_price),
        }

    def cancel_order(self, order_id, product_id=None) -> bool:
        return True

    def cancel_all(self, product_symbol: str) -> bool:
        return True

    # ── Market data (not used in replay — feed handles this) ─────────────────

    def get_ticker(self, symbol: str) -> dict:
        return {}

    def get_spot_ticker(self, symbol: str = "BTCUSD") -> dict:
        return {}

    def get_option_chain(self, asset: str, expiry: str) -> list:
        return []

    def get_positions(self, asset: str = "BTC") -> list:
        return []

    def get_balance(self) -> list:
        return []

    def get_candles(self, symbol: str, resolution: str, start: int, end: int) -> list:
        return []
