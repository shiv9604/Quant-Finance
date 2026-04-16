"""
Replay runner — validates the live strategy against historical backtest data.

Runs the same ShortVolStrategy + RiskEngine code used in production,
fed by HistoricalFeed + PaperBroker instead of live API calls.

Usage:
    python -m src.replay.replay_runner

Output:
    - Trade-by-trade results printed to console
    - Comparison CSV saved to analysis/replay_results.csv
"""

import datetime
import os

import pandas as pd
from tqdm import tqdm

from src.replay.historical_feed import HistoricalFeed
from src.replay.paper_broker import PaperBroker
from src.core.short_vol import ShortVolStrategy
from src.risk.risk_engine import RiskEngine
from src.state.position import Position, PositionStore
from src.execution.order_manager import OrderManager
from src.config import config

# ── Config (mirrors backtester) ───────────────────────────────────────────────

BT_START = "2024-12-01"
BT_END = "2025-11-30"
SCAN_FROM = datetime.time(13, 15)
SCAN_TO = datetime.time(15, 30)
FORCED_EXIT = datetime.time(17, 25)
LOT_SIZE = 1


def _ist_str(date, t) -> str:
    return f"{date} {t} IST"


def run_replay():
    config.test_mode = True  # ← add this as first line inside run_replay()
    print("\n" + "=" * 60)
    print("REPLAY RUNNER — Live Strategy vs Historical Data")
    print("=" * 60)

    feed = HistoricalFeed()
    broker = PaperBroker()
    strategy = ShortVolStrategy()
    risk = RiskEngine()
    order_mgr = OrderManager(broker, fill_timeout_s=5)

    days = feed.get_trading_days(BT_START, BT_END)
    print(f"Trading days in range: {len(days)}\n")

    trades = []
    skipped = 0

    for date in tqdm(days, desc="Replaying"):
        date_ts = pd.Timestamp(date)

        # Get median spot for the day (used to load options)
        day_spot = feed.get_spot_at(date_ts, SCAN_TO)
        if day_spot == 0:
            skipped += 1
            continue

        # Load options for this date
        feed.set_cursor(date_ts, SCAN_FROM, day_spot)

        minutes = feed.get_minutes_for_day(date, SCAN_FROM, SCAN_TO)
        if not minutes:
            skipped += 1
            continue

        position = Position()
        entered = False

        # ── Scan window: look for entry ───────────────────────────────────────
        for t in minutes:
            if entered:
                break

            spot = feed.get_spot_at(date_ts, t)
            if spot == 0:
                continue

            feed.set_cursor(date_ts, t, spot)
            market = feed.get_snapshot()

            if not market.vol_signal.get("found"):
                continue

            # Entry checks
            entry_allowed, _ = risk.can_enter(position)
            if not entry_allowed:
                break

            signal = strategy.evaluate_entry(market, position)
            if not signal.should_enter:
                continue

            # Pre-register fill prices for the next 2 orders the broker will create
            ce_fill_id = broker._order_counter
            pe_fill_id = broker._order_counter + 1
            broker.set_fill_price(ce_fill_id, signal.ce_ref_price)
            broker.set_fill_price(pe_fill_id, signal.pe_ref_price)

            try:
                ce_fill, pe_fill = order_mgr.enter_strangle(
                    signal.ce_symbol,
                    signal.pe_symbol,
                    LOT_SIZE,
                    signal.ce_ref_price,
                    signal.pe_ref_price,
                )
            except Exception:
                break

            entry_premium = ce_fill + pe_fill
            position = Position(
                active=True,
                entry_time=_ist_str(date, t),
                ce_symbol=signal.ce_symbol,
                pe_symbol=signal.pe_symbol,
                ce_entry_price=ce_fill,
                pe_entry_price=pe_fill,
                entry_premium=entry_premium,
                size=LOT_SIZE,
                current_premium=entry_premium,
                prev_premium=entry_premium,
            )
            entered = True
            entry_time = t

        if not entered:
            skipped += 1
            continue

        # ── Walk forward: check exits minute by minute ────────────────────────
        all_minutes = feed.get_minutes_for_day(date, entry_time, FORCED_EXIT)
        exit_reason = "FORCED"
        exit_time = FORCED_EXIT
        exit_ce = 0.0
        exit_pe = 0.0

        for t in all_minutes:
            spot = feed.get_spot_at(date_ts, t)
            feed.set_cursor(date_ts, t, spot)

            ce_mark, pe_mark = feed.get_combined_premium(
                position.ce_symbol, position.pe_symbol
            )
            if ce_mark == 0 and pe_mark == 0:
                continue

            combined = ce_mark + pe_mark
            if combined > position.prev_premium:
                position.consec_rises += 1
            else:
                position.consec_rises = 0
            position.prev_premium = position.current_premium
            position.current_premium = combined

            strat_signal = strategy.evaluate_exit(market, position)
            should_exit, reason = risk.should_exit(position, strat_signal)

            if should_exit or t >= FORCED_EXIT:
                exit_reason = reason if should_exit else "FORCED"
                exit_time = t
                exit_ce = ce_mark
                exit_pe = pe_mark
                break

        exit_premium = exit_ce + exit_pe
        pnl_usd = (position.entry_premium - exit_premium) * LOT_SIZE
        pnl_pct = (
            (pnl_usd / position.entry_premium * 100)
            if position.entry_premium > 0
            else 0.0
        )

        trades.append(
            {
                "date": str(date),
                "entry_time": str(entry_time),
                "exit_time": str(exit_time),
                "ce_symbol": position.ce_symbol,
                "pe_symbol": position.pe_symbol,
                "entry_premium": round(position.entry_premium, 2),
                "exit_premium": round(exit_premium, 2),
                "pnl_usd": round(pnl_usd, 2),
                "pnl_pct": round(pnl_pct, 2),
                "exit_reason": exit_reason,
            }
        )

    # ── Results ───────────────────────────────────────────────────────────────

    print(f"\nSkipped days (no data / no signal): {skipped}")

    if not trades:
        print("No trades generated.")
        return

    df = pd.DataFrame(trades)
    total_pnl = df["pnl_usd"].sum()
    win_trades = (df["pnl_usd"] > 0).sum()
    total = len(df)

    print(f"\n{'Date':<12} {'Entry':>7} {'Exit':>7} {'PnL USD':>9} {'PnL%':>7}  Reason")
    print("-" * 60)
    for _, r in df.iterrows():
        print(
            f"{r['date']:<12} "
            f"{r['entry_premium']:>7.2f} "
            f"{r['exit_premium']:>7.2f} "
            f"{r['pnl_usd']:>+9.2f} "
            f"{r['pnl_pct']:>+7.2f}%  "
            f"{r['exit_reason']}"
        )
    print("-" * 60)
    print(f"Total trades : {total}")
    print(f"Winners      : {win_trades} ({win_trades/total*100:.1f}%)")
    print(f"Total PnL    : ${total_pnl:+.2f}")

    # Compare vs backtester output
    bt_path = "analysis/btcusd_vol_short_20241201_20251130_trades.csv"
    if os.path.exists(bt_path):
        bt = pd.read_csv(bt_path)
        print(f"\nBacktester trades : {len(bt)}")
        print(f"Replay trades     : {total}")
        print(f"PnL delta         : ${total_pnl - bt['pnl_usd'].sum():+.2f}")

    os.makedirs("analysis", exist_ok=True)
    out_path = "analysis/replay_results.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    run_replay()
