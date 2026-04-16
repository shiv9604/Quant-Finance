from src.risk.risk_engine import RiskEngine
from src.state.position import Position
from src.core.strategy import ExitSignal

engine = RiskEngine()


def _pos(entry=100.0, current=100.0):
    return Position(active=True, entry_premium=entry, current_premium=current)


def test_sl_not_triggered_below_80pct():
    hit, _ = engine.check_stop_loss(_pos(entry=100, current=179))
    assert not hit


def test_sl_triggered_at_80pct():
    hit, reason = engine.check_stop_loss(_pos(entry=100, current=180))
    assert hit
    assert "sl_hit" in reason


def test_no_exit_when_healthy():
    ok, _ = engine.should_exit(_pos(entry=100, current=90), ExitSignal(False))
    assert not ok


def test_prem_rebuild_signal_respected():
    ok, reason = engine.should_exit(_pos(), ExitSignal(True, reason="prem_rebuild"))
    assert ok
    assert reason == "prem_rebuild"


def test_daily_loss_limit():
    pos = _pos(entry=100, current=90)
    pos.daily_pnl_usd = -200.0  # already hit daily limit
    ok, reason = engine.should_exit(pos, ExitSignal(False))
    assert ok
    assert "daily_limit" in reason
