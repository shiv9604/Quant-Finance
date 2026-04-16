"""
All configuration in one place.
Change values here or override via environment variables.
"""

import os
from dataclasses import dataclass, field
from datetime import time


@dataclass
class Config:
    # ── Broker ────────────────────────────────────────────────
    api_key: str = field(default_factory=lambda: os.getenv("DELTA_API_KEY", ""))
    api_secret: str = field(default_factory=lambda: os.getenv("DELTA_API_SECRET", ""))
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "DELTA_BASE_URL", "https://cdn-ind.testnet.deltaex.org"  # testnet default
        )
    )

    # ── Asset ─────────────────────────────────────────────────
    asset: str = "BTC"
    spot_symbol: str = "BTCUSD"  # ← add this line
    lot_size: int = 1

    # ── Entry window (IST) ────────────────────────────────────
    scan_from: time = time(13, 15)
    scan_to: time = time(15, 30)
    forced_exit: time = time(17, 25)

    # ── Strategy ─────────────────────────────────────────────
    strike_offset: int = 0  # min distance OTM from spot (USD)

    # ── Risk ─────────────────────────────────────────────────
    sl_pct: float = 0.80  # exit if loss >= 80% of entry premium
    prem_rebuild_n: int = 6  # consecutive premium rises = exit signal
    max_daily_loss: float = 150.0  # hard stop on the day (USD)

    # ── Execution ─────────────────────────────────────────────
    fill_timeout_s: int = 60  # seconds to wait for fill before cancelling
    order_retry: int = 3  # retries on order placement failure

    # ── Loop ──────────────────────────────────────────────────
    loop_interval_s: int = field(
        default_factory=lambda: int(os.getenv("LOOP_INTERVAL_S", "10"))
    )

    # ── Logging ───────────────────────────────────────────────
    log_dir: str = "logs"
    dry_run: bool = field(
        default_factory=lambda: os.getenv("DRY_RUN", "false").lower() == "true"
    )
    test_mode: bool = field(
        default_factory=lambda: os.getenv("TEST_MODE", "false").lower() == "true"
    )


# Singleton — import this everywhere
config = Config()
