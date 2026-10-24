from datetime import datetime, timezone, timedelta
from decimal import Decimal as D
import pytest

from crypto_bot.models import Candle, OrderRequest, Side
from crypto_bot.risk import RiskLimits, RiskManager
from crypto_bot.paper_broker import PaperBroker
from crypto_bot.data_validation import validate_candles


def candle(minute, close="100"):
    price = D(close)
    return Candle("BTCUSDT", datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=minute),
                  price, price, price, price, D("1"))


def test_rejects_naive_timestamp():
    with pytest.raises(ValueError, match="timezone-aware"):
        Candle("BTCUSDT", datetime(2026, 1, 1), D("10"), D("10"), D("10"), D("10"), D("1"))


def test_rejects_duplicate_or_out_of_order_timestamps():
    with pytest.raises(ValueError, match="strictly increasing"):
        validate_candles([candle(1), candle(1)])


def test_paper_broker_applies_fee_and_slippage():
    risk = RiskManager(RiskLimits(D("1000"), D("2000"), D("100")))
    broker = PaperBroker(risk, fee_rate=D("0.01"), slippage_rate=D("0.01"))
    fill = broker.submit(OrderRequest("BTCUSDT", Side.BUY, D("1")), D("100"))
    assert fill.simulated is True
    assert fill.price == D("101.00")
    assert fill.fee == D("1.0100")


def test_risk_limit_rejects_large_order():
    risk = RiskManager(RiskLimits(D("50"), D("100"), D("20")))
    broker = PaperBroker(risk)
    with pytest.raises(PermissionError, match="risk controls"):
        broker.submit(OrderRequest("BTCUSDT", Side.BUY, D("1")), D("100"))


def test_kill_switch_blocks_orders():
    risk = RiskManager(RiskLimits(D("1000"), D("2000"), D("100")))
    risk.activate_kill_switch()
    broker = PaperBroker(risk)
    with pytest.raises(PermissionError):
        broker.submit(OrderRequest("BTCUSDT", Side.BUY, D("1")), D("100"))


def test_daily_loss_limit_triggers_kill_switch():
    risk = RiskManager(RiskLimits(D("1000"), D("2000"), D("50")))
    assert not risk.approve(OrderRequest("BTCUSDT", Side.BUY, D("1")), D("100"), daily_pnl=D("-50"))
    assert risk.halted
