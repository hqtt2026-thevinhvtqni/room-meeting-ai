"""Validate external strategy signals WITHOUT placing orders.

Work 200 bridge boundary: inputs are untrusted; output is review-only.
No broker/network/exchange imports and no execution capability.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import re
from typing import Any, Mapping


class SignalRejected(ValueError):
    """Untrusted signal failed the safety or schema gate."""


@dataclass(frozen=True)
class IntakePolicy:
    allowed_symbols: frozenset[str] = frozenset({"BTCUSDT"})
    allowed_exchanges: frozenset[str] = frozenset({"OKX"})
    allowed_markets: frozenset[str] = frozenset({"SPOT"})
    allowed_timeframes: frozenset[str] = frozenset({"15m"})
    max_age_seconds: int = 120
    future_tolerance_seconds: int = 5

    def __post_init__(self) -> None:
        if self.max_age_seconds < 1 or self.future_tolerance_seconds < 0:
            raise ValueError("invalid freshness policy")
        if not all((self.allowed_symbols, self.allowed_exchanges, self.allowed_markets, self.allowed_timeframes)):
            raise ValueError("allow-lists must not be empty")


@dataclass(frozen=True)
class Signal:
    event_id: str
    strategy: str
    version: str
    symbol: str
    exchange: str
    market: str
    timeframe: str
    side: str
    event_time: datetime
    candle_closed_at: datetime
    entry: Decimal
    stop_loss: Decimal
    take_profit_1: Decimal
    take_profit_2: Decimal | None
    take_profit_3: Decimal | None


@dataclass(frozen=True)
class IntakeDecision:
    status: str  # REVIEW_ONLY; never ORDER_ACCEPTED or ORDER_FILLED
    signal: Signal


def _timestamp(value: Any, name: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise SignalRejected(f"{name}: expected ISO-8601 timestamp")
    try:
        d = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SignalRejected(f"{name}: invalid timestamp") from exc
    if d.tzinfo is None or d.utcoffset() is None:
        raise SignalRejected(f"{name}: timezone required")
    return d.astimezone(timezone.utc)


def _price(value: Any, name: str, *, required: bool = True) -> Decimal | None:
    if not required and value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, str, Decimal)):
        raise SignalRejected(f"{name}: numeric string required")
    try:
        n = Decimal(str(value))
    except InvalidOperation as exc:
        raise SignalRejected(f"{name}: invalid decimal") from exc
    if not n.is_finite() or n <= 0:
        raise SignalRejected(f"{name}: must be positive and finite")
    return n


def parse_signal(payload: Mapping[str, Any], policy: IntakePolicy, *, now: datetime) -> Signal:
    if not isinstance(payload, Mapping):
        raise SignalRejected("payload must be an object; legacy BX421 pipe alerts are not accepted")
    # Be explicit: merely claiming these fields does not authenticate the sender.
    required = {"event_id", "strategy", "version", "symbol", "exchange", "market",
                "timeframe", "side", "event_time", "candle_closed_at", "closed_bar",
                "execution_mode", "entry", "stop_loss", "take_profit_1"}
    missing = required - payload.keys()
    if missing:
        raise SignalRejected("missing fields: " + ", ".join(sorted(missing)))
    if payload.get("execution_mode") != "SIGNAL_ONLY":
        raise SignalRejected("only SIGNAL_ONLY permitted")
    if payload.get("closed_bar") is not True:
        raise SignalRejected("unconfirmed candle forbidden")
    if payload.get("live_execution") is not False:
        raise SignalRejected("live_execution must explicitly be false")
    if payload.get("paper_only") is not True:
        raise SignalRejected("paper_only must explicitly be true")
    for k in ("event_id", "strategy", "version", "symbol", "exchange", "market", "timeframe", "side"):
        if not isinstance(payload[k], str) or not payload[k].strip():
            raise SignalRejected(f"{k}: invalid string")
    eid = payload["event_id"]
    if not re.fullmatch(r"[A-Za-z0-9_.:-]{8,128}", eid):
        raise SignalRejected("event_id: invalid format")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", payload["strategy"]):
        raise SignalRejected("strategy: invalid format")
    if payload["symbol"] not in policy.allowed_symbols:
        raise SignalRejected("symbol not allowed")
    if payload["exchange"] not in policy.allowed_exchanges:
        raise SignalRejected("exchange not allowed")
    if payload["market"] not in policy.allowed_markets:
        raise SignalRejected("market not allowed")
    if payload["timeframe"] not in policy.allowed_timeframes:
        raise SignalRejected("timeframe not allowed")
    side = payload["side"]
    if side not in ("BUY", "SELL"):
        raise SignalRejected("unsupported action; only BUY or SELL plan for review")
    t = _timestamp(payload["event_time"], "event_time")
    close_at = _timestamp(payload["candle_closed_at"], "candle_closed_at")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("now must be timezone-aware")
    utcnow = now.astimezone(timezone.utc)
    if t > utcnow + timedelta(seconds=policy.future_tolerance_seconds):
        raise SignalRejected("event time in the future")
    if utcnow - t > timedelta(seconds=policy.max_age_seconds):
        raise SignalRejected("stale event")
    if close_at > t:
        raise SignalRejected("candle not closed at event time")
    if utcnow - close_at > timedelta(seconds=policy.max_age_seconds):
        raise SignalRejected("stale candle close")
    e = _price(payload["entry"], "entry")
    sl = _price(payload["stop_loss"], "stop_loss")
    t1 = _price(payload["take_profit_1"], "take_profit_1")
    t2 = _price(payload.get("take_profit_2"), "take_profit_2", required=False)
    t3 = _price(payload.get("take_profit_3"), "take_profit_3", required=False)
    if t3 is not None and t2 is None:
        raise SignalRejected("TP3 requires TP2")
    if side == "BUY" and not (sl < e < t1 and (t2 is None or t1 < t2) and (t3 is None or t2 < t3)):
        raise SignalRejected("invalid BUY SL/TP ordering")
    if side == "SELL" and not (sl > e > t1 and (t2 is None or t1 > t2) and (t3 is None or t2 > t3)):
        raise SignalRejected("invalid SELL SL/TP ordering")
    return Signal(eid, payload["strategy"], payload["version"], payload["symbol"],
                  payload["exchange"], payload["market"], payload["timeframe"], side,
                  t, close_at, e, sl, t1, t2, t3)


class SignalIntake:
    """In-memory deduplication; reset on restart => NOT production replay protection."""

    def __init__(self, policy: IntakePolicy | None = None):
        self.policy = policy or IntakePolicy()
        self._seen: set[str] = set()

    def accept_for_review(self, payload: Mapping[str, Any], *, now: datetime) -> IntakeDecision:
        signal = parse_signal(payload, self.policy, now=now)
        if signal.event_id in self._seen:
            raise SignalRejected("duplicate event_id")
        self._seen.add(signal.event_id)
        return IntakeDecision("REVIEW_ONLY", signal)
