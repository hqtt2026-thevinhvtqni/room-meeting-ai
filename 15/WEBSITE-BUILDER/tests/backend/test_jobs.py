"""Foundation tests for the job lifecycle state machine (issue #34, part E).

Covers: valid paths, rejected paths, terminal immutability, and the rule
that SUCCEEDED is impossible without complete evidence.
"""

from __future__ import annotations

import pytest

from roomhop_builder.errors import (
    EvidenceMissingError,
    InvalidTransitionError,
    UnknownJobError,
    ValidationError,
)
from roomhop_builder.jobs import JobState, JobStore, TRANSITIONS, validate_create_payload

VALID_PAYLOAD = {
    "intent": "Trang landing page cho quán cà phê, có menu và form đặt bàn",
    "site_name": "cafe-demo",
    "created_by": "vinh",
}


def make_store(**kwargs) -> JobStore:
    return JobStore(**kwargs)


# -- validation -------------------------------------------------------------


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"intent": "", "site_name": "x", "created_by": "y"},
        {"intent": "   ", "site_name": "x", "created_by": "y"},
        {"intent": "a" * 5000, "site_name": "x", "created_by": "y"},
        {"intent": "ok", "site_name": "s" * 200, "created_by": "y"},
        {"intent": "ok", "site_name": "s"},  # missing created_by
        {"intent": 123, "site_name": "s", "created_by": "y"},  # wrong type
        ["not-a-dict"],
        {"intent": "ok", "site_name": "s", "created_by": "y", "shell": "rm -rf /"},
    ],
)
def test_invalid_create_payloads_are_rejected(payload):
    with pytest.raises(ValidationError) as exc:
        validate_create_payload(payload)
    assert exc.value.code == "VALIDATION_ERROR"


def test_unknown_field_is_listed_in_details():
    with pytest.raises(ValidationError) as exc:
        validate_create_payload({**VALID_PAYLOAD, "runtime": "docker"})
    fields = [p["field"] for p in exc.value.details["problems"]]
    assert "runtime" in fields


def test_valid_payload_is_trimmed_and_accepted():
    cleaned = validate_create_payload({**VALID_PAYLOAD, "intent": "  hello  "})
    assert cleaned["intent"] == "hello"


# -- creation / lookup ------------------------------------------------------


def test_created_job_starts_queued_with_history():
    store = make_store()
    job = store.create(VALID_PAYLOAD)
    assert job.state is JobState.QUEUED
    assert job.id.startswith("W15-")
    assert job.history[0].to_state == "QUEUED"
    assert job.is_terminal is False


def test_get_unknown_job_raises_404_style_error():
    with pytest.raises(UnknownJobError):
        make_store().get("W15-does-not-exist")


def test_list_filters_by_state_and_rejects_bad_filter():
    store = make_store()
    a = store.create(VALID_PAYLOAD)
    b = store.create(VALID_PAYLOAD)
    store.transition(a.id, JobState.RUNNING, reason="test")
    assert [j.id for j in store.list("RUNNING")] == [a.id]
    assert len(store.list()) == 2
    with pytest.raises(ValidationError):
        store.list("NOT_A_STATE")


# -- transitions ------------------------------------------------------------


def test_happy_path_queued_running_succeeded_when_evidence_complete():
    store = JobStore(evidence_checker=lambda job_id: True)
    job = store.create(VALID_PAYLOAD)
    store.transition(job.id, JobState.RUNNING, reason="worker start")
    done = store.transition(job.id, JobState.SUCCEEDED, reason="evidence verified")
    assert done.state is JobState.SUCCEEDED
    assert [h.to_state for h in done.history] == ["QUEUED", "RUNNING", "SUCCEEDED"]


def test_success_without_evidence_is_refused():
    store = JobStore(evidence_checker=lambda job_id: False)
    job = store.create(VALID_PAYLOAD)
    store.transition(job.id, JobState.RUNNING, reason="worker start")
    with pytest.raises(EvidenceMissingError) as exc:
        store.transition(job.id, JobState.SUCCEEDED, reason="agent claims it works")
    assert exc.value.code == "EVIDENCE_MISSING"
    assert job.state is JobState.RUNNING  # refusal must not mutate state


def test_queued_cannot_jump_to_succeeded():
    store = JobStore(evidence_checker=lambda job_id: True)
    job = store.create(VALID_PAYLOAD)
    with pytest.raises(InvalidTransitionError):
        store.transition(job.id, JobState.SUCCEEDED, reason="skip the work")


@pytest.mark.parametrize("target", ["RUNNING", "SUCCEEDED", "FAILED", "BLOCKED"])
def test_failed_is_immutable(target):
    store = JobStore(evidence_checker=lambda job_id: True)
    job = store.create(VALID_PAYLOAD)
    store.transition(job.id, JobState.RUNNING, reason="start")
    store.transition(job.id, JobState.FAILED, reason="boom", error="runtime died")
    with pytest.raises(InvalidTransitionError):
        store.transition(job.id, target, reason="try to resurrect")


def test_blocked_is_immutable_and_records_error_reason():
    store = make_store()
    job = store.create(VALID_PAYLOAD)
    blocked = store.transition(job.id, JobState.BLOCKED, reason="no runtime grant",
                               error="RUNTIME_NOT_WIRED")
    assert blocked.error == "RUNTIME_NOT_WIRED"
    assert blocked.is_terminal
    with pytest.raises(InvalidTransitionError):
        store.transition(blocked.id, JobState.RUNNING, reason="please work")


def test_transition_table_has_no_back_edges_from_terminal_states():
    for state in TRANSITIONS:
        if state.value in ("SUCCEEDED", "FAILED", "BLOCKED"):
            assert TRANSITIONS[state] == frozenset()


def test_transition_requires_non_empty_reason_and_known_target():
    store = make_store()
    job = store.create(VALID_PAYLOAD)
    with pytest.raises(ValidationError):
        store.transition(job.id, JobState.RUNNING, reason="   ")
    with pytest.raises(ValidationError):
        store.transition(job.id, "PAUSED", reason="invented state")


def test_runtime_failure_path_records_error():
    store = make_store()
    job = store.create(VALID_PAYLOAD)
    store.transition(job.id, JobState.RUNNING, reason="start")
    failed = store.transition(job.id, JobState.FAILED, reason="preview 502",
                              error="runtime returned HTTP 502")
    assert failed.error == "runtime returned HTTP 502"
    assert failed.state is JobState.FAILED
