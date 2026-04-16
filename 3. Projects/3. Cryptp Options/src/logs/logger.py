"""
Unified logging layer.
Three separate log streams: diagnostic, trade events, in-trade PnL.

Usage (from any layer):
    from src.logs.logger import logger
    logger.diag({"cycle": 1, "spot": 104200, "active": False})
    logger.trade("ENTRY", {"ce": "C-BTC-105000-150125", "premium": 83.0})
    logger.pnl({"pnl_pct": 12.4, "combined": 73.0})
"""

import json
import logging
import os
from datetime import datetime, timezone


def _ist_now() -> str:
    """Return current time as IST ISO string."""
    from datetime import timedelta

    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")


def _build_file_logger(name: str, filepath: str) -> logging.Logger:
    """Create a logger that writes JSON lines to a rotating file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)
    log.propagate = False

    if not log.handlers:
        fh = logging.FileHandler(filepath, encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(message)s"))
        log.addHandler(fh)

        # Also mirror to stdout for live monitoring
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(message)s"))
        log.addHandler(ch)

    return log


class TradingLogger:
    """
    Three log files, each with a dedicated write method.
    All entries are JSON lines — easy to parse, grep, and load into pandas.
    """

    def __init__(self, log_dir: str = "logs"):
        self._diag = _build_file_logger("diag", os.path.join(log_dir, "diag.log"))
        self._trade = _build_file_logger("trades", os.path.join(log_dir, "trades.log"))
        self._pnl = _build_file_logger("pnl", os.path.join(log_dir, "pnl.log"))

    def _emit(self, log: logging.Logger, payload: dict) -> None:
        payload["_ts"] = _ist_now()
        log.info(json.dumps(payload))

    def diag(self, data: dict) -> None:
        """Every loop cycle: decision inputs (spot, IV, active state, etc.)."""
        self._emit(self._diag, {"stream": "DIAG", **data})

    def trade(self, event: str, data: dict) -> None:
        """Trade lifecycle events: ENTRY, EXIT, CANCEL, ERROR."""
        self._emit(self._trade, {"stream": "TRADE", "event": event, **data})

    def pnl(self, data: dict) -> None:
        """Minute-by-minute in-trade PnL snapshots."""
        self._emit(self._pnl, {"stream": "PNL", **data})

    def error(self, msg: str, exc: Exception | None = None) -> None:
        """Errors go to diag.log with an ERROR tag."""
        payload: dict = {"stream": "DIAG", "level": "ERROR", "msg": msg}
        if exc:
            payload["exc"] = str(exc)
        self._emit(self._diag, payload)


# Module-level singleton — import from anywhere
logger = TradingLogger()
