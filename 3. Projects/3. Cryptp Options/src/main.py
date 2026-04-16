"""
Main orchestrator — the trading loop.

Wires all components together and runs the core loop:

    while True:
        market  = market_data.update()
        state   = position.get()
        log_diag(market + state)

        if not state.active:
            if strategy.evaluate_entry(market, state):
                execution.enter()
        else:
            log_pnl(state)
            if risk.should_exit(market, state):
                execution.exit()

        sleep(loop_interval)

To start:
    DRY_RUN=true python -m src.main          ← paper mode
    python -m src.main                        ← live (uses .env credentials)
"""

import os
import sys
import time
import signal
from datetime import datetime, timezone, timedelta

# Load .env before importing config
try:
    from dotenv import load_dotenv

    load_dotenv()  # loads .env (credentials)
    env_name = os.getenv("APP_ENV", "testnet")  # default to testnet
    load_dotenv(f".env.{env_name}", override=True)  # overrides with env settings
except ImportError:
    pass

from src.config import config
from src.logs.logger import logger
from src.data.market_data import MarketData
from src.state.position import Position, PositionStore
from src.core.short_vol import ShortVolStrategy
from src.risk.risk_engine import RiskEngine
from src.execution.broker import DeltaBroker, BrokerError
from src.execution.order_manager import OrderManager


IST = timezone(timedelta(hours=5, minutes=30))


# ── Wiring ────────────────────────────────────────────────────────────────────


def build_components():
    broker = DeltaBroker(
        config.api_key, config.api_secret, config.base_url, config.dry_run
    )
    market_data = MarketData(broker)
    order_mgr = OrderManager(broker, config.fill_timeout_s)
    strategy = ShortVolStrategy()
    risk = RiskEngine()
    store = PositionStore()
    return broker, market_data, order_mgr, strategy, risk, store


# ── Helpers ───────────────────────────────────────────────────────────────────


def ist_now_str() -> str:
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S IST")


def pnl_usd(position: Position) -> float:
    """Current unrealised P&L in USD for the open position."""
    return (position.entry_premium - position.current_premium) * position.size


def pnl_pct(position: Position) -> float:
    if position.entry_premium == 0:
        return 0.0
    return (
        (position.entry_premium - position.current_premium)
        / position.entry_premium
        * 100
    )


# ── Main loop ─────────────────────────────────────────────────────────────────


def run():
    logger.trade(
        "SYSTEM_START",
        {
            "env": config.base_url,
            "dry_run": config.dry_run,
            "asset": config.asset,
            "lot": config.lot_size,
        },
    )

    broker, market_data, order_mgr, strategy, risk, store = build_components()
    position = store.load()  # resume from disk in case of restart

    if position.active:
        logger.trade(
            "RESUME",
            {
                "ce": position.ce_symbol,
                "pe": position.pe_symbol,
                "entry_premium": position.entry_premium,
            },
        )

    # Graceful shutdown on Ctrl-C / SIGTERM
    _running = [True]

    def _handle_signal(sig, frame):
        logger.trade("SHUTDOWN_SIGNAL", {"signal": sig})
        _running[0] = False

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    while _running[0]:
        try:
            _cycle(market_data, order_mgr, strategy, risk, store, position)
        except Exception as e:
            logger.error("Unhandled error in main cycle", exc=e)

        # Reload position from disk (handles external modifications)
        position = store.load()
        now_ist = datetime.now(IST).time()                                                                  
        in_window = config.scan_from <= now_ist <= config.scan_to
                                                                
        if position.active or in_window:
            interval = config.loop_interval_s   # 1s — full precision
        else:                                                        
            interval = 30                        # outside window — conserve resources                      
        
        for _ in range(interval):                                                                           
            if not _running[0]:
                break                                                                                       
            time.sleep(1)

    logger.trade("SYSTEM_STOP", {"final_daily_pnl": position.daily_pnl_usd})


def _cycle(market_data, order_mgr, strategy, risk, store, position: Position):
    now_str = ist_now_str()

    # ── Fetch market snapshot ──────────────────────────────────────────────
    try:
        market = market_data.get_snapshot(config.asset)
    except Exception as e:
        logger.error("Failed to fetch market snapshot", exc=e)
        return

    # ── Diagnostic log every cycle ────────────────────────────────────────
    logger.diag(
        {
            "time": now_str,
            "spot": market.spot,
            "active": position.active,
            "daily_pnl": round(position.daily_pnl_usd, 2),
            "chain_ticks": len(market.chain),
            **(
                {
                    "ce": position.ce_symbol,
                    "pe": position.pe_symbol,
                    "current_prem": round(position.current_premium, 4),
                    "entry_prem": round(position.entry_premium, 4),
                    "pnl_pct": round(pnl_pct(position), 2),
                    "consec_rises": position.consec_rises,
                }
                if position.active
                else {}
            ),
        }
    )

    # ── No position: evaluate entry ────────────────────────────────────────
    if not position.active:
        entry_allowed, reason = risk.can_enter(position)
        if not entry_allowed:
            return  # diag log already captured why

        signal = strategy.evaluate_entry(market, position)
        if not signal.should_enter:
            return

        # ── Enter ──────────────────────────────────────────────────────
        logger.trade(
            "ENTRY_SIGNAL",
            {
                "ce": signal.ce_symbol,
                "ce_ref": signal.ce_ref_price,
                "pe": signal.pe_symbol,
                "pe_ref": signal.pe_ref_price,
                "spot": market.spot,
                "reason": signal.reason,
            },
        )

        try:
            ce_fill, pe_fill = order_mgr.enter_strangle(
                signal.ce_symbol,
                signal.pe_symbol,
                config.lot_size,
                signal.ce_ref_price,
                signal.pe_ref_price,
            )
        except Exception as e:
            logger.error("Entry aborted", exc=e)
            return

        position = store.open(
            ce_symbol=signal.ce_symbol,
            pe_symbol=signal.pe_symbol,
            ce_price=ce_fill,
            pe_price=pe_fill,
            size=config.lot_size,
            entry_time=now_str,
            daily_pnl_so_far=position.daily_pnl_usd,
        )

        logger.trade(
            "ENTRY",
            {
                "ce": signal.ce_symbol,
                "ce_fill": ce_fill,
                "pe": signal.pe_symbol,
                "pe_fill": pe_fill,
                "combined_prem": position.entry_premium,
                "capital": round(position.entry_premium * config.lot_size, 2),
            },
        )

    # ── Position active: update marks, check exits ─────────────────────────
    else:
        try:
            ce_mark, pe_mark = market_data.get_combined_premium(
                position.ce_symbol, position.pe_symbol
            )
        except Exception as e:
            logger.error("Failed to fetch combined premium", exc=e)
            return

        position = store.update_mark(position, ce_mark, pe_mark)

        # PnL snapshot log
        logger.pnl(
            {
                "time": now_str,
                "ce_mark": ce_mark,
                "pe_mark": pe_mark,
                "combined": round(position.current_premium, 4),
                "entry_prem": round(position.entry_premium, 4),
                "pnl_pct": round(pnl_pct(position), 2),
                "pnl_usd": round(pnl_usd(position), 2),
                "consec_rises": position.consec_rises,
                "peak_pnl_pct": round(position.peak_pnl_pct, 2),
            }
        )

        # Strategy exit check
        strat_signal = strategy.evaluate_exit(market, position)

        # Risk engine final decision
        should_exit, exit_reason = risk.should_exit(position, strat_signal)

        if not should_exit:
            return

        # ── Exit ───────────────────────────────────────────────────────
        logger.trade("EXIT_SIGNAL", {"reason": exit_reason})

        try:
            ce_exit, pe_exit = order_mgr.exit_strangle(
                position.ce_symbol,
                position.pe_symbol,
                position.size,
                exit_reason,
            )
        except Exception as e:
            logger.error("Exit order failed", exc=e)
            return

        realised_exit_prem = ce_exit + pe_exit
        final_pnl_usd = (position.entry_premium - realised_exit_prem) * position.size
        final_pnl_pct = (
            (position.entry_premium - realised_exit_prem) / position.entry_premium * 100
            if position.entry_premium > 0
            else 0.0
        )

        position = store.close(
            position,
            exit_reason=exit_reason,
            exit_time=now_str,
            pnl_usd=final_pnl_usd,
            pnl_pct=final_pnl_pct,
        )

        logger.trade(
            "EXIT",
            {
                "reason": exit_reason,
                "ce_exit": ce_exit,
                "pe_exit": pe_exit,
                "pnl_usd": round(final_pnl_usd, 2),
                "pnl_pct": round(final_pnl_pct, 2),
                "peak_pnl": round(position.peak_pnl_pct, 2),
                "daily_pnl": round(position.daily_pnl_usd, 2),
            },
        )


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not config.api_key or not config.api_secret:
        print("ERROR: DELTA_API_KEY and DELTA_API_SECRET must be set.")
        sys.exit(1)

    run()
