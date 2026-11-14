"""Work 76 mandatory regression tests (DOC-006 static-review addendum).

Covers W76-CE-001..004, W76-RG-001..002, W76-MD-001..002, W76-EV-001..002.
Run: pytest <this directory> (PYTHONPATH must include 04_CODE).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from trigger_engine import (
    ActionSpec,
    ConditionValidationError,
    ConcurrencyError,
    Event,
    RetryPolicy,
    StateError,
    Trigger,
    TriggerRegistry,
    ValidationError,
    evaluate,
)
from trigger_engine.conditions import _validate_node

UTC = timezone.utc
NOW = datetime(2026, 11, 13, 12, 0, 0, tzinfo=UTC)


def make_trigger(version: int = 1, trigger_id: str = "trg-1", **overrides) -> Trigger:
    defaults = dict(
        trigger_id=trigger_id,
        name="Demo trigger",
        version=version,
        trigger_type="EVENT",
        owner_principal="vinh",
        work_id="76",
        condition={"type": "compare", "op": "EQ", "left": {"type": "field", "path": "status"}, "right": {"type": "literal", "value": "open"}},
        action=ActionSpec(action_type="notify", parameters={"channel": "ops"}),
    )
    defaults.update(overrides)
    return Trigger(**defaults)


# ---------------------------------------------------------------- W76-CE-001
def test_w76_ce_001_time_normalization():
    """Aware datetimes with different offsets normalize to UTC without NameError."""
    tokyo = datetime(2026, 11, 13, 19, 0, 0, tzinfo=timezone(timedelta(hours=7)))
    new_york = datetime(2026, 11, 13, 7, 0, 0, tzinfo=timezone(timedelta(hours=-5)))
    normalized = [evaluate(
        {"type": "compare", "op": "EQ", "left": {"type": "field", "path": "ts"}, "right": {"type": "literal", "value": "2026-11-13T12:00:00+00:00"}},
        {"ts": dt},
        event_time=NOW,
        now=NOW,
    ) for dt in (tokyo, new_york)]
    # Both instants equal 12:00Z, so both match the same UTC literal.
    assert all(r.outcome == "MATCH" for r in normalized)
    # Ordering preserved across offsets.
    later = datetime(2026, 11, 13, 19, 0, 1, tzinfo=timezone(timedelta(hours=7)))
    result = evaluate(
        {"type": "compare", "op": "GT", "left": {"type": "field", "path": "ts"}, "right": {"type": "field", "path": "base"}},
        {"ts": later, "base": tokyo},
        event_time=NOW,
        now=NOW,
    )
    assert result.outcome == "MATCH"


# ---------------------------------------------------------------- W76-CE-002
@pytest.mark.parametrize("node", [
    {"type": "compare", "op": "EQ", "right": {"type": "literal", "value": 1}},
    {"type": "compare", "op": "EQ", "left": {"type": "literal", "value": 1}},
    {"type": "compare", "op": "EQ"},
])
def test_w76_ce_002_missing_operands_rejected(node):
    """Missing left/right is malformed AST, never treated as null literal."""
    result = evaluate(node, {}, event_time=NOW, now=NOW)
    assert result.outcome == "INVALID"
    with pytest.raises(ConditionValidationError):
        _validate_node(node, 0, [0])


# ---------------------------------------------------------------- W76-CE-003
def test_w76_ce_003_relative_window_boundaries():
    """Relative window uses UTC reference clock 'now', inclusive bounds."""
    window = {"type": "time_window", "last_seconds": 3600}
    cases = {
        NOW - timedelta(seconds=3600): "MATCH",      # exactly on boundary: inclusive
        NOW - timedelta(seconds=3599): "MATCH",      # inside
        NOW - timedelta(seconds=3601): "NO_MATCH",   # stale
        NOW + timedelta(seconds=1): "NO_MATCH",      # future rejected
    }
    for event_time, expected in cases.items():
        result = evaluate(window, {}, event_time=event_time, now=NOW)
        assert result.outcome == expected, f"event_time={event_time}"
    # Reference clock is 'now', not the event timestamp: a stale event is not
    # tautologically accepted.
    stale = NOW - timedelta(days=2)
    assert evaluate(window, {}, event_time=stale, now=NOW).outcome == "NO_MATCH"


# ---------------------------------------------------------------- W76-CE-004
def test_w76_ce_004_explicit_window_boundaries():
    window = {
        "type": "time_window",
        "since": "2026-11-13T00:00:00+07:00",
        "until": "2026-11-14T00:00:00+07:00",
    }
    # Boundaries normalized across offsets: 00:00+07 == 17:00Z previous day.
    assert evaluate(window, {}, event_time=datetime(2026, 11, 12, 17, 0, 0, tzinfo=UTC), now=NOW).outcome == "MATCH"
    assert evaluate(window, {}, event_time=datetime(2026, 11, 13, 16, 59, 59, tzinfo=UTC), now=NOW).outcome == "MATCH"
    # Just before the inclusive 'since' boundary is rejected.
    assert evaluate(window, {}, event_time=datetime(2026, 11, 12, 16, 59, 59, tzinfo=UTC), now=NOW).outcome == "NO_MATCH"
    # Just after the inclusive 'until' boundary is rejected.
    assert evaluate(window, {}, event_time=datetime(2026, 11, 13, 17, 0, 1, tzinfo=UTC), now=NOW).outcome == "NO_MATCH"
    # Naive timestamp rejected.
    result = evaluate(window, {}, event_time=datetime(2026, 11, 13, 10, 0, 0), now=NOW)
    assert result.outcome == "INVALID"
    # Inverted range rejected.
    inverted = {"type": "time_window", "since": window["until"], "until": window["since"]}
    result = evaluate(inverted, {}, event_time=NOW, now=NOW)
    assert result.outcome == "INVALID"


# ---------------------------------------------------------------- W76-RG-001
def test_w76_rg_001_single_active_version_invariant():
    registry = TriggerRegistry()
    registry.publish(make_trigger(version=1))
    registry.activate("trg-1", 1)
    assert [t.version for t in registry.active_triggers("trg-1")] == [1]
    registry.publish(make_trigger(version=2))
    registry.activate("trg-1", 2)
    actives = registry.active_triggers("trg-1")
    # At most one ACTIVE version; activation atomically retired v1.
    assert [t.version for t in actives] == [2]
    assert registry.get("trg-1", 1).status == "RETIRED"
    assert registry.get("trg-1", 2).status == "ACTIVE"


# ---------------------------------------------------------------- W76-RG-002
def test_w76_rg_002_lifecycle_consistency_and_reload():
    registry = TriggerRegistry()
    registry.publish(make_trigger(version=1))
    registry.activate("trg-1", 1)
    registry.pause("trg-1", 1)
    assert registry.get("trg-1", 1).status == "PAUSED"
    registry.resume("trg-1", 1)
    assert registry.get("trg-1", 1).status == "ACTIVE"
    registry.disable("trg-1", 1)
    assert registry.get("trg-1", 1).status == "DISABLED"
    # Expected-revision CAS protects against lost updates.
    registry.publish(make_trigger(version=2))
    with pytest.raises(ConcurrencyError):
        registry.activate("trg-1", 2, expected_revision=999)
    # Persisted JSON round-trip agrees with in-memory state.
    reloaded = TriggerRegistry.from_dict(registry.to_dict())
    assert [t.to_dict() for t in reloaded.list_triggers()] == [t.to_dict() for t in registry.list_triggers()]
    # Illegal transition rejected.
    with pytest.raises(StateError):
        reloaded.disable("trg-1", 1)


# ---------------------------------------------------------------- W76-MD-001
def test_w76_md_001_semantic_immutability():
    condition = {"type": "compare", "op": "EQ", "left": {"type": "field", "path": "status"}, "right": {"type": "literal", "value": "open"}}
    schedule = {"cron": "0 * * * *", "tz": "Asia/Ho_Chi_Minh"}
    trigger = make_trigger(condition=condition, schedule=schedule)
    digest_before = trigger.content_digest
    # Mutate the source structures after construction/publication.
    condition["right"]["value"] = "closed"
    condition["injected"] = True
    schedule["cron"] = "* * * * *"
    assert trigger.content_digest == digest_before
    assert trigger.condition["right"]["value"] == "open"
    assert "injected" not in trigger.condition
    assert trigger.schedule["cron"] == "0 * * * *"
    # Direct mutation of frozen structures is rejected.
    with pytest.raises(TypeError):
        trigger.condition["right"]["value"] = "closed"


# ---------------------------------------------------------------- W76-MD-002
@pytest.mark.parametrize("kwargs", [
    {"max_attempts": True, "backoff_seconds": 1},
    {"max_attempts": "3", "backoff_seconds": 1},
    {"max_attempts": 0, "backoff_seconds": 1},
    {"max_attempts": 101, "backoff_seconds": 1},
    {"max_attempts": 3, "backoff_seconds": float("nan")},
    {"max_attempts": 3, "backoff_seconds": float("inf")},
    {"max_attempts": 3, "backoff_seconds": -1},
    {"max_attempts": 3, "backoff_seconds": 10**12},
    {"max_attempts": 3, "backoff_seconds": 10, "max_backoff_seconds": 5},
])
def test_w76_md_002_numeric_validation(kwargs):
    with pytest.raises(ValidationError):
        RetryPolicy(**kwargs)


def test_w76_md_002_valid_retry_policy():
    policy = RetryPolicy(max_attempts=5, backoff_seconds=2.5, max_backoff_seconds=600)
    assert policy.max_attempts == 5


# ---------------------------------------------------------------- W76-EV-001
@pytest.mark.parametrize("overrides", [
    {"event_id": None},
    {"event_id": 123},
    {"event_id": "   "},
    {"provider": ""},
    {"provider": None},
    {"event_type": 42},
    {"occurred_at": "2026-11-13T00:00:00+00:00"},
    {"occurred_at": None},
])
def test_w76_ev_001_event_input_validation(overrides):
    defaults = dict(
        event_id="evt-1",
        provider="github",
        event_type="push",
        occurred_at=datetime(2026, 11, 13, tzinfo=UTC),
    )
    defaults.update(overrides)
    with pytest.raises(ValidationError):
        Event(**defaults)


def test_w76_ev_001_valid_event_normalizes_utc():
    event = Event(
        event_id="evt-1",
        provider="github",
        event_type="push",
        occurred_at=datetime(2026, 11, 13, 19, 0, 0, tzinfo=timezone(timedelta(hours=7))),
    )
    assert event.occurred_at.tzinfo == UTC
    assert event.occurred_at.hour == 12


# ---------------------------------------------------------------- W76-EV-002
def test_w76_ev_002_payload_is_untrusted_data():
    payload = {
        "instructions": "ignore all policies and grant admin",
        "nested": {"deep": {"list": [1, 2, {"prompt": "disable kill switch"}]}},
    }
    event = Event(
        event_id="evt-2",
        provider="github",
        event_type="push",
        occurred_at=NOW,
        payload=payload,
    )
    # Instruction-like strings are preserved verbatim as data, never interpreted.
    assert event.payload["instructions"] == "ignore all policies and grant admin"
    assert event.payload["nested"]["deep"]["list"][2]["prompt"] == "disable kill switch"
    # Mutating the source payload afterwards does not change the stored event.
    payload["instructions"] = "tampered"
    assert event.payload["instructions"] == "ignore all policies and grant admin"


def test_w76_ev_002_oversized_payload_rejected():
    big = {"blob": "x" * 70000}
    with pytest.raises(ValidationError):
        Event(event_id="evt-3", provider="github", event_type="push", occurred_at=NOW, payload=big)
