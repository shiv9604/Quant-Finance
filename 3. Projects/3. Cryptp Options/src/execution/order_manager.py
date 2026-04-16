"""
Order lifecycle manager.
Single responsibility: place and close strangle positions, confirm fills.

Does NOT contain strategy or risk logic.
Calls broker.py for all exchange communication.
"""

import time
from typing import Optional, Tuple

from src.execution.broker import DeltaBroker, BrokerError
from src.logs.logger import logger


class OrderManager:

    def __init__(self, broker: DeltaBroker, fill_timeout_s: int = 60):
        self._broker = broker
        self._timeout = fill_timeout_s

    # ── Entry ─────────────────────────────────────────────────────────────────

    def enter_strangle(
        self,
        ce_symbol: str,
        pe_symbol: str,
        size: float,
        ce_ref_price: Optional[float] = None,
        pe_ref_price: Optional[float] = None,
    ) -> Tuple[float, float]:
        """
        Sell CE and PE legs.
        Uses limit orders at mark price if ref prices supplied (maker = lower fees).
        Falls back to market order if not filled within fill_timeout_s.

        Returns (ce_fill_price, pe_fill_price).
        Raises RuntimeError if either leg fails to fill.
        """
        ce_order = self._place_leg("sell", ce_symbol, size, ce_ref_price)
        pe_order = self._place_leg("sell", pe_symbol, size, pe_ref_price)

        # In dry_run mode, fills are simulated — no polling needed
        if self._broker._dry_run:
            return ce_ref_price or 0.0, pe_ref_price or 0.0

        ce_fill = self._await_fill(ce_order["id"], ce_symbol, ce_ref_price)
        pe_fill = self._await_fill(pe_order["id"], pe_symbol, pe_ref_price)

        # If one leg filled but the other timed out → close the filled leg immediately
        if ce_fill is None or pe_fill is None:
            logger.trade(
                "PARTIAL_FILL_ABORT",
                {
                    "ce_fill": ce_fill,
                    "pe_fill": pe_fill,
                    "ce_symbol": ce_symbol,
                    "pe_symbol": pe_symbol,
                },
            )
            if ce_fill is not None:
                self._force_close(ce_symbol, size)
            if pe_fill is not None:
                self._force_close(pe_symbol, size)
            raise RuntimeError("Partial fill — position aborted and unwound.")

        logger.trade(
            "FILL_CONFIRMED",
            {
                "ce_symbol": ce_symbol,
                "ce_fill": ce_fill,
                "pe_symbol": pe_symbol,
                "pe_fill": pe_fill,
            },
        )
        return ce_fill, pe_fill

    # ── Exit ──────────────────────────────────────────────────────────────────

    def exit_strangle(
        self,
        ce_symbol: str,
        pe_symbol: str,
        size: float,
        reason: str,
    ) -> Tuple[float, float]:
        """
        Buy back CE and PE legs to close the short strangle.
        Always uses market orders for exits — speed > price.

        Returns (ce_exit_price, pe_exit_price).
        """
        # Cancel any stale open orders first
        self._broker.cancel_all(ce_symbol)
        self._broker.cancel_all(pe_symbol)

        ce_order = self._broker.place_order(ce_symbol, "buy", size, "market_order")
        pe_order = self._broker.place_order(pe_symbol, "buy", size, "market_order")

        # In dry_run mode, fills are simulated
        if self._broker._dry_run:
            return 0.0, 0.0

        ce_exit = self._await_fill(ce_order["id"], ce_symbol)
        pe_exit = self._await_fill(pe_order["id"], pe_symbol)

        # Market orders should always fill; log warning if they don't
        if ce_exit is None:
            logger.error(f"CE exit fill not confirmed for {ce_symbol}")
            ce_exit = 0.0
        if pe_exit is None:
            logger.error(f"PE exit fill not confirmed for {pe_symbol}")
            pe_exit = 0.0

        logger.trade(
            "EXIT_FILLS",
            {
                "reason": reason,
                "ce_symbol": ce_symbol,
                "ce_exit": ce_exit,
                "pe_symbol": pe_symbol,
                "pe_exit": pe_exit,
            },
        )
        return ce_exit, pe_exit

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _place_leg(self, side, symbol, size, ref_price):
        order = self._broker.place_order(symbol, side, size, "market_order")
        logger.trade(
            "ORDER_PLACED",
            {
                "side": side,
                "symbol": symbol,
                "size": size,
                "ref_price": ref_price,
                "order_id": order.get("id"),
            },
        )
        return order

    def _await_fill(
        self, order_id: str, symbol: str, fallback_price: float = 0.0
    ) -> Optional[float]:
        """
        Poll order status until filled or timeout.
        Returns the average fill price, or None on timeout.
        """
        deadline = time.time() + self._timeout
        while time.time() < deadline:
            try:
                order = self._broker.get_order(order_id)
                state = order.get("state", "")

                if state == "closed":
                    unfilled = int(order.get("unfilled_size", 1))
                    if unfilled == 0:
                        fill_price = float(order.get("avg_fill_price", 0) or 0)
                        if fill_price == 0.0:
                            fill_price = (
                                fallback_price  # ← use mark price at order time
                            )
                        logger.diag(
                            {"fill_confirmed": order_id, "fill_price": fill_price}
                        )
                        return fill_price
                if state in ("cancelled", "rejected"):
                    logger.error(f"Order {order_id} {state}")
                    return None

                time.sleep(2)
            except Exception as e:
                logger.error(f"Poll error for {order_id}", exc=e)
                time.sleep(2)

        logger.error(f"Fill timeout for {order_id} ({symbol})")
        self._broker.cancel_all(symbol)
        return None

    def _force_close(self, symbol: str, size: float) -> None:
        """Emergency market buy to close an accidentally open short."""
        try:
            self._broker.place_order(symbol, "buy", size, "market_order")
            logger.trade("EMERGENCY_CLOSE", {"symbol": symbol, "size": size})
        except Exception as e:
            logger.error(f"Emergency close failed for {symbol}", exc=e)
