"""No external network or brokerage dependencies; deterministic tests."""
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pytest
from crypto_bot.signal_intake import IntakePolicy, SignalIntake, SignalRejected, parse_signal

NOW = datetime(2026, 10, 24, 1, 0, tzinfo=timezone.utc)


def signal(**overrides):
    obj = dict(event_id="BX428-20261024-0001", strategy="BX42MR", version="4.2.8",
               symbol="BTCUSDT", exchange="OKX", market="SPOT", timeframe="15m",
               side="BUY", event_time=NOW.isoformat(), candle_closed_at=NOW.isoformat(),
               closed_bar=True, execution_mode="SIGNAL_ONLY", live_execution=False,
               paper_only=True, entry="100", stop_loss="98", take_profit_1="102",
               take_profit_2="104", take_profit_3="106")
    obj.update(overrides)
    return obj


def test_review_only_never_submits_order():
    r=SignalIntake().accept_for_review(signal(), now=NOW)
    assert r.status == "REVIEW_ONLY"
    assert r.signal.entry == Decimal("100")
    assert not hasattr(r, "submit")


def test_duplicate_event_blocked():
    i=SignalIntake()
    i.accept_for_review(signal(), now=NOW)
    with pytest.raises(SignalRejected, match="duplicate"):
        i.accept_for_review(signal(), now=NOW)


@pytest.mark.parametrize("bad", [
    dict(live_execution=True), dict(live_execution=None), dict(paper_only=False),
    dict(execution_mode="Auto Backtest + Alerts"), dict(closed_bar=False),
    dict(symbol="XAUUSD"),dict(exchange="BINANCE"),dict(market="PERPETUAL"),
    dict(timeframe="1m"),dict(side="EXIT"),dict(entry="NaN"),
    dict(entry="Infinity"),dict(entry="-1"),dict(stop_loss="101"),
    dict(take_profit_1="99"),dict(take_profit_2="101"),dict(take_profit_3="103"),
    dict(event_time=(NOW+timedelta(minutes=1)).isoformat()),
    dict(event_time=(NOW-timedelta(minutes=5)).isoformat()),
    dict(candle_closed_at=(NOW+timedelta(seconds=1)).isoformat()),
    dict(candle_closed_at=(NOW-timedelta(minutes=5)).isoformat()),
    dict(event_time="2026-10-24T01:00:00"),
])
def test_fail_closed(bad):
    with pytest.raises(SignalRejected):
        parse_signal(signal(**bad), IntakePolicy(), now=NOW)


def test_sell_valid():
    s=signal(side="SELL", stop_loss="102", take_profit_1="98", take_profit_2="96", take_profit_3="94")
    assert parse_signal(s, IntakePolicy(), now=NOW).side=="SELL"


def test_unknown_payload_and_missing_gate_rejected():
    with pytest.raises(SignalRejected):
        parse_signal("BX421|BUY|...", IntakePolicy(), now=NOW)
    s=signal();s.pop("live_execution")
    with pytest.raises(SignalRejected):
        parse_signal(s,IntakePolicy(), now=NOW)


def test_config_validation():
    with pytest.raises(ValueError):
        IntakePolicy(max_age_seconds=0)
    with pytest.raises(ValueError):
        IntakePolicy(allowed_symbols=frozenset())
