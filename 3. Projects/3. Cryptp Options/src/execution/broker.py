"""
Delta Exchange API wrapper.
Single responsibility: HTTP communication with the exchange.

Handles:
  - HMAC-SHA256 request signing
  - GET / POST / DELETE with retries
  - Rate-limit awareness (logs 429s, backs off)
  - Dry-run mode (logs orders without sending)
"""

import hashlib
import hmac
import json
import time
from typing import Any, Optional
from urllib.parse import urlencode

import requests

from src.logs.logger import logger


class BrokerError(Exception):
    """Raised when the exchange returns a non-2xx response."""

    def __init__(self, status: int, body: str):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {body}")


class DeltaBroker:
    """
    Thin HTTP adapter for the Delta Exchange REST API.
    Does not contain any strategy or risk logic.
    """

    def __init__(
        self, api_key: str, api_secret: str, base_url: str, dry_run: bool = False
    ):
        self._key = api_key
        self._secret = api_secret
        self._base = base_url.rstrip("/")
        self._dry_run = dry_run
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    # ── Signing ───────────────────────────────────────────────────────────────

    def _sign(self, method: str, path: str, query: str, body: str) -> dict:
        """
        Delta signature = HMAC-SHA256(method + timestamp + path + query + body).
        Timestamp must be within 5 seconds of server time.
        """
        ts = str(int(time.time()))
        msg = method.upper() + ts + path + query + body
        sig = hmac.new(
            self._secret.encode(),
            msg.encode(),
            hashlib.sha256,
        ).hexdigest()
        return {
            "api-key": self._key,
            "signature": sig,
            "timestamp": ts,
        }

    # ── Core request ─────────────────────────────────────────────────────────

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        payload: Optional[dict] = None,
        retries: int = 3,
    ) -> Any:
        query = ("?" + urlencode(params)) if params else ""
        body_str = json.dumps(payload) if payload else ""
        url = self._base + path + (("?" + urlencode(params)) if params else "")
        headers = self._sign(
            method, path, ("?" + urlencode(params)) if params else "", body_str
        )

        for attempt in range(retries):
            try:
                resp = self._session.request(
                    method,
                    url,
                    headers=headers,
                    data=body_str or None,
                    timeout=10,
                )

                if resp.status_code == 429:
                    reset_ms = int(resp.headers.get("X-RATE-LIMIT-RESET", 5000))
                    wait = reset_ms / 1000 + 0.5
                    logger.error(f"Rate limited. Sleeping {wait:.1f}s")
                    time.sleep(wait)
                    continue

                if not resp.ok:
                    raise BrokerError(resp.status_code, resp.text)

                return resp.json()

            except requests.Timeout:
                logger.error(f"Timeout on {method} {path} (attempt {attempt + 1})")
                time.sleep(2**attempt)
            except BrokerError:
                raise
            except Exception as e:
                logger.error(f"Request error on {method} {path}", exc=e)
                time.sleep(2**attempt)

        raise BrokerError(0, f"All {retries} attempts failed for {method} {path}")

    # ── Market data ───────────────────────────────────────────────────────────

    def get_ticker(self, symbol: str) -> dict:
        """Fetch ticker for a single product. Returns mark_price, ltp, bid, ask."""
        data = self._request("GET", f"/v2/tickers/{symbol}")
        return data.get("result") or {}

    def get_option_chain(self, asset: str, expiry_ddmmyyyy: str) -> list[dict]:
        """
        Fetch all call and put options for asset on a given expiry.
        expiry_ddmmyyyy: e.g. '15-01-2025'
        """
        params = {
            "contract_types": "call_options,put_options",
            "underlying_asset_symbols": asset,
            "expiry_date": expiry_ddmmyyyy,
        }
        data = self._request("GET", "/v2/tickers", params=params)
        result = data.get("result") or []
        if not result:
            logger.error(
                f"Empty option chain for {asset} {expiry_ddmmyyyy}. Raw response: {data}"
            )
        return result

    def get_spot_ticker(self, symbol: str = "BTCUSDT") -> dict:
        """Fetch spot/perpetual ticker to read current BTC price."""
        data = self._request("GET", f"/v2/tickers/{symbol}")
        result = data.get("result") or {}
        if not result:
            logger.error(f"Empty spot ticker for '{symbol}'. Raw response: {data}")
        return result

    def list_products(self, asset: str = "BTC") -> list[dict]:
        """
        List all products for an underlying asset.
        Use this to discover the correct spot/perp symbol on a new environment.
        """
        data = self._request(
            "GET", "/v2/products", params={"underlying_asset_symbol": asset}
        )
        return data.get("result") or []

    def get_balance(self) -> list[dict]:
        """Fetch wallet balances."""
        return self._request("GET", "/v2/wallet/balances").get("result") or []

    def get_positions(self, asset: str = "BTC") -> list[dict]:
        """Fetch all open positions for an underlying asset."""
        return (
            self._request(
                "GET",
                "/v2/positions/margined",
                params={"underlying_asset_symbol": asset},
            ).get("result")
            or []
        )

    # ── Order management ─────────────────────────────────────────────────────

    def place_order(
        self,
        symbol: str,
        side: str,  # "buy" | "sell"
        size: float,
        order_type: str = "market_order",  # "market_order" | "limit_order"
        limit_price: Optional[float] = None,
        post_only: bool = False,
    ) -> dict:
        """
        Place a single order. Returns full order response dict.
        In dry_run mode: logs and returns a fake order dict.
        """
        payload: dict = {
            "product_symbol": symbol,
            "size": int(size),
            "side": side,
            "order_type": order_type,
        }
        if order_type == "limit_order" and limit_price is not None:
            payload["limit_price"] = str(limit_price)
        if post_only:
            payload["post_only"] = True

        if self._dry_run:
            fake_id = f"DRY_{symbol}_{side}_{int(time.time())}"
            logger.trade("DRY_ORDER", {**payload, "order_id": fake_id})
            return {"id": fake_id, "state": "open", "product_symbol": symbol, **payload}

        result = self._request("POST", "/v2/orders", payload=payload)
        return result.get("result", {})

    def cancel_order(self, order_id: str, product_id: int) -> bool:
        """Cancel a specific order by ID."""
        if self._dry_run:
            logger.trade("DRY_CANCEL", {"order_id": order_id})
            return True
        try:
            self._request(
                "DELETE",
                "/v2/orders",
                payload={
                    "id": order_id,
                    "product_id": product_id,
                },
            )
            return True
        except BrokerError:
            return False

    def cancel_all(self, product_symbol: str) -> bool:
        """Cancel all open orders for a product (safety net before exit)."""
        if self._dry_run:
            logger.trade("DRY_CANCEL_ALL", {"product_symbol": product_symbol})
            return True
        try:
            self._request(
                "DELETE", "/v2/orders/all", payload={"product_symbol": product_symbol}
            )
            return True
        except BrokerError:
            return False

    def get_order(self, order_id: str) -> dict:
        data = self._request("GET", f"/v2/orders/{order_id}")
        result = data.get("result")
        if isinstance(result, list):
            return result[0] if result else {}
        return result or {}

    def get_candles(
        self, symbol: str, resolution: str, start: int, end: int
    ) -> list[dict]:
        """Fetch OHLCV candles. resolution in minutes, start/end are unix epochs."""
        data = self._request(
            "GET",
            "/v2/history/candles",
            params={
                "symbol": symbol,
                "resolution": resolution,
                "start": start,
                "end": end,
            },
        )
        return data.get("result") or []
