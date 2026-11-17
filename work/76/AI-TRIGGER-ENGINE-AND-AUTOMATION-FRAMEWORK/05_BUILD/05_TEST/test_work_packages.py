from datetime import datetime, timezone, timedelta
import json
import pytest

from trigger_engine.gateway import EventGateway, GatewayRejected, SourceRegistration
from trigger_engine.scheduler import TimeScheduler, OneShotSchedule, SchedulerBlocked
from trigger_engine.policy import PolicyAdapter, PolicyOutcome, PolicyRequest, PolicyResult
from trigger_engine.orchestrator import ExecutionStateMachine, ExecutionState, StateTransitionError
from trigger_engine.audit import AuditWriter, AuditUnavailable

class Verifier:
    def verify(self, source_id, headers, body): return headers.get("x-valid") == "yes"
class Replay:
    def __init__(self): self.seen=set()
    def reserve(self, source_id, event_id, expires_at):
        key=(source_id,event_id)
        if key in self.seen: return False
        self.seen.add(key); return True
class Schema:
    def validate(self, payload):
        if "value" not in payload: raise ValueError("value required")
class Due:
    def __init__(self): self.seen=set()
    def claim_once(self, schedule_id, key):
        if key in self.seen: return False
        self.seen.add(key); return True
class Provider:
    def __init__(self, result): self.result=result
    def evaluate_current(self, request): return self.result
class Approval:
    def verify_current(self, approval_ref, request): return approval_ref=="approved"
class Sink:
    def __init__(self): self.rows=[]
    def append(self, row): self.rows.append(row)
    def append_transition(self, row): self.rows.append(row)

def test_gateway_auth_schema_scope_and_replay():
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    replay=Replay()
    gateway=EventGateway({"source-a":SourceRegistration("source-a","76",frozenset({"order.created"}),Schema())},Verifier(),replay)
    body=json.dumps({"event_id":"e-1","event_type":"order.created","occurred_at":now.isoformat(),"work_id":"999","payload":{"value":1}}).encode()
    result=gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)
    assert result.work_id=="76"
    assert result.event.payload["value"]==1
    with pytest.raises(GatewayRejected):
        gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)

def test_gateway_fails_closed_without_auth_or_replay_port():
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    gateway=EventGateway({},None,None)
    with pytest.raises(GatewayRejected):
        gateway.ingest("missing",{},b"{}",received_at=now)

def test_scheduler_claims_due_occurrence_once():
    due=Due(); scheduler=TimeScheduler(due)
    schedule=OneShotSchedule("s-1","76",datetime(2026,11,18,12,tzinfo=timezone.utc))
    now=datetime(2026,11,18,12,1,tzinfo=timezone.utc)
    assert scheduler.due(schedule,now) is not None
    assert scheduler.due(schedule,now) is None

def test_scheduler_requires_durable_store_and_explicit_timezone():
    with pytest.raises(SchedulerBlocked):
        TimeScheduler(None).due(OneShotSchedule("s","76",datetime.now(timezone.utc)),datetime.now(timezone.utc))
    with pytest.raises(ValueError):
        OneShotSchedule("s","76",datetime(2026,11,18,12))

def test_policy_missing_provider_is_indeterminate():
    request=PolicyRequest("principal","76","WP-76-05","notify","p1","a1","c1")
    result=PolicyAdapter(None).authorize(request)
    assert result.outcome==PolicyOutcome.INDETERMINATE

def test_policy_requires_current_approval():
    request=PolicyRequest("principal","76","WP-76-05","notify","p1","a1","c1")
    need=PolicyResult(PolicyOutcome.REQUIRE_APPROVAL,"d1","r1","approval required")
    adapter=PolicyAdapter(Provider(need),Approval())
    assert adapter.authorize(request).outcome==PolicyOutcome.DENY
    assert adapter.authorize(request,"approved").outcome==PolicyOutcome.ALLOW

def test_policy_provider_exception_fails_closed():
    class Broken:
        def evaluate_current(self, request): raise RuntimeError("offline")
    request=PolicyRequest("p","76","WP-76-05","a","r","as","c")
    assert PolicyAdapter(Broken()).authorize(request).outcome==PolicyOutcome.INDETERMINATE

def test_state_machine_requires_audit_sink_and_legal_transitions():
    machine=ExecutionStateMachine(None)
    with pytest.raises(StateTransitionError):
        machine.start("x","c")
    sink=Sink(); machine=ExecutionStateMachine(sink); machine.start("y","c")
    assert machine.transition("y",ExecutionState.SOURCE_AUTHENTICATED,"source authenticated","c")==ExecutionState.SOURCE_AUTHENTICATED
    assert machine.transition("y",ExecutionState.VALIDATED,"schema valid","c")==ExecutionState.VALIDATED
    with pytest.raises(StateTransitionError):
        machine.transition("y",ExecutionState.SUCCEEDED,"skip","c")

def test_state_machine_commits_only_after_sink_append():
    class FailAfterStart:
        def __init__(self): self.calls=0
        def append_transition(self, row):
            self.calls+=1
            if self.calls>1: raise OSError("disk")
    sink=FailAfterStart()
    machine=ExecutionStateMachine(sink); machine.start("z","c")
    with pytest.raises(StateTransitionError, match="append failed") as exc:
        machine.transition("z",ExecutionState.SOURCE_AUTHENTICATED,"authenticated","c")
    assert isinstance(exc.value.__cause__, OSError)
    assert machine.state("z")==ExecutionState.RECEIVED

def test_audit_writer_hash_chain_and_fail_closed():
    sink=Sink(); writer=AuditWriter(sink)
    first=writer.write(record_id="r1",work_id="76",actor_ref="svc:test",action="ingest",outcome="accepted",correlation_id="c1",payload={"x":1})
    second=writer.write(record_id="r2",work_id="76",actor_ref="svc:test",action="evaluate",outcome="denied",correlation_id="c1",payload={"x":2})
    assert first.previous_hash==""
    assert second.previous_hash==first.record_hash
    with pytest.raises(AuditUnavailable):
        AuditWriter(None).write(record_id="r",work_id="76",actor_ref="a",action="x",outcome="y",correlation_id="c",payload={})

def test_audit_sink_failure_does_not_advance_hash_head():
    class Broken:
        def append(self, row): raise OSError("offline")
    writer=AuditWriter(Broken())
    with pytest.raises(AuditUnavailable):
        writer.write(record_id="r",work_id="76",actor_ref="a",action="x",outcome="y",correlation_id="c",payload={})

from trigger_engine.retry import IdempotencyGuard, DuplicateExecution, RetryPlanner
from trigger_engine.models import RetryPolicy

def test_retry_planner_is_bounded_and_stops_at_budget():
    planner=RetryPlanner(RetryPolicy(max_attempts=3,backoff_seconds=5,max_backoff_seconds=8))
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    first=planner.plan(completed_attempts=1,now=now,retryable=True)
    second=planner.plan(completed_attempts=2,now=now,retryable=True)
    final=planner.plan(completed_attempts=3,now=now,retryable=True)
    assert first.due_at==now+timedelta(seconds=5)
    assert second.due_at==now+timedelta(seconds=8)
    assert final.retry is False

def test_retry_planner_never_retries_non_retryable_failure():
    planner=RetryPlanner(RetryPolicy(max_attempts=4,backoff_seconds=1))
    result=planner.plan(completed_attempts=1,now=datetime.now(timezone.utc),retryable=False)
    assert result.retry is False and result.due_at is None

def test_idempotency_guard_requires_durable_atomic_store():
    with pytest.raises(RuntimeError):
        IdempotencyGuard(None).claim("76","k",now=datetime.now(timezone.utc),ttl_seconds=60)
    class Store:
        def __init__(self): self.keys=set()
        def claim(self,scope,key,expires_at):
            if (scope,key) in self.keys: return False
            self.keys.add((scope,key)); return True
    guard=IdempotencyGuard(Store()); now=datetime.now(timezone.utc)
    guard.claim("76","k",now=now,ttl_seconds=60)
    with pytest.raises(DuplicateExecution):
        guard.claim("76","k",now=now,ttl_seconds=60)


# W76-AU-001 — audit payloads use strict canonical JSON
def test_audit_payload_digest_is_canonical_across_mapping_order():
    sink=Sink()
    writer=AuditWriter(sink)
    first=writer.write(record_id="canonical-1",work_id="76",actor_ref="svc:test",action="ingest",outcome="accepted",correlation_id="c1",payload={"b":2,"a":1})
    second=writer.write(record_id="canonical-2",work_id="76",actor_ref="svc:test",action="ingest",outcome="accepted",correlation_id="c1",payload={"a":1,"b":2})
    assert first.payload_digest==second.payload_digest

@pytest.mark.parametrize("payload", [
    {"amount": float("nan")},
    {"amount": float("inf")},
    {"nested": [1, float("-inf")]},
])
def test_audit_rejects_non_finite_payload_without_appending(payload):
    sink=Sink()
    writer=AuditWriter(sink)
    with pytest.raises(ValueError):
        writer.write(record_id="invalid",work_id="76",actor_ref="svc:test",action="ingest",outcome="accepted",correlation_id="c1",payload=payload)
    assert sink.rows==[]


# W76-EG-001 — malformed gateway inputs fail closed before replay reservation
def test_gateway_rejects_unhashable_event_type_as_gateway_error():
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    replay=Replay()
    gateway=EventGateway({"source-a":SourceRegistration("source-a","76",frozenset({"order.created"}),Schema())},Verifier(),replay)
    body=b'{"event_id":"e-bad","event_type":[],"occurred_at":"2026-11-18T12:00:00+00:00","payload":{"value":1}}'
    with pytest.raises(GatewayRejected):
        gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)
    assert replay.seen==set()

def test_gateway_rejects_non_finite_payload_before_replay_reservation():
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    replay=Replay()
    gateway=EventGateway({"source-a":SourceRegistration("source-a","76",frozenset({"order.created"}),Schema())},Verifier(),replay)
    body=b'{"event_id":"e-nan","event_type":"order.created","occurred_at":"2026-11-18T12:00:00+00:00","payload":{"value":NaN}}'
    with pytest.raises(GatewayRejected):
        gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)
    assert replay.seen==set()

def test_gateway_replay_store_exception_is_declared_fail_closed_error():
    class BrokenReplay:
        def reserve(self,source_id,event_id,expires_at): raise OSError("store offline")
    now=datetime(2026,11,18,12,tzinfo=timezone.utc)
    gateway=EventGateway({"source-a":SourceRegistration("source-a","76",frozenset({"order.created"}),Schema())},Verifier(),BrokenReplay())
    body=json.dumps({"event_id":"e-2","event_type":"order.created","occurred_at":now.isoformat(),"payload":{"value":1}}).encode()
    with pytest.raises(GatewayRejected,match="replay protection unavailable"):
        gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)

def test_gateway_rejects_naive_received_at():
    now=datetime(2026,11,18,12)
    replay=Replay()
    gateway=EventGateway({"source-a":SourceRegistration("source-a","76",frozenset({"order.created"}),Schema())},Verifier(),replay)
    body=json.dumps({"event_id":"e-3","event_type":"order.created","occurred_at":"2026-11-18T12:00:00+00:00","payload":{"value":1}}).encode()
    with pytest.raises(GatewayRejected,match="received_at"):
        gateway.ingest("source-a",{"x-valid":"yes"},body,received_at=now)
    assert replay.seen==set()


# W76-ID-001 — idempotency storage failures are distinct from duplicates
def test_idempotency_store_failure_is_unavailable_not_duplicate():
    from trigger_engine.retry import IdempotencyUnavailable
    class Broken:
        def claim(self,scope,key,expires_at): raise OSError("database offline")
    with pytest.raises(IdempotencyUnavailable,match="claim failed"):
        IdempotencyGuard(Broken()).claim("76","k",now=datetime.now(timezone.utc),ttl_seconds=60)

def test_idempotency_indeterminate_store_result_fails_closed():
    from trigger_engine.retry import IdempotencyUnavailable
    class Indeterminate:
        def claim(self,scope,key,expires_at): return None
    with pytest.raises(IdempotencyUnavailable,match="indeterminate"):
        IdempotencyGuard(Indeterminate()).claim("76","k",now=datetime.now(timezone.utc),ttl_seconds=60)

@pytest.mark.parametrize("kwargs", [
    {"work_id":None,"idempotency_key":"k","ttl_seconds":60},
    {"work_id":"76","idempotency_key":" ","ttl_seconds":60},
    {"work_id":"76","idempotency_key":"k","ttl_seconds":True},
    {"work_id":"76","idempotency_key":"k","ttl_seconds":0},
])
def test_idempotency_guard_rejects_malformed_scope_key_or_ttl(kwargs):
    class Store:
        def claim(self,scope,key,expires_at): return True
    with pytest.raises(ValueError):
        IdempotencyGuard(Store()).claim(kwargs["work_id"],kwargs["idempotency_key"],now=datetime.now(timezone.utc),ttl_seconds=kwargs["ttl_seconds"])

def test_retry_planner_rejects_non_boolean_retryable_and_invalid_clock():
    planner=RetryPlanner(RetryPolicy(max_attempts=3,backoff_seconds=1))
    with pytest.raises(ValueError):
        planner.plan(completed_attempts=1,now=datetime.now(timezone.utc),retryable=1)
    with pytest.raises(ValueError):
        planner.plan(completed_attempts=1,now="not-a-datetime",retryable=True)


# W76-SC-001 — scheduler store failures are distinct from already-claimed occurrences
def test_scheduler_store_exception_fails_closed_with_declared_error():
    class BrokenDue:
        def claim_once(self,schedule_id,key): raise OSError("store offline")
    schedule=OneShotSchedule("s","76",datetime(2026,11,18,12,tzinfo=timezone.utc))
    with pytest.raises(SchedulerBlocked,match="claim failed"):
        TimeScheduler(BrokenDue()).due(schedule,datetime(2026,11,18,12,tzinfo=timezone.utc))

def test_scheduler_indeterminate_store_result_is_blocked_not_duplicate():
    class UnknownDue:
        def claim_once(self,schedule_id,key): return None
    schedule=OneShotSchedule("s","76",datetime(2026,11,18,12,tzinfo=timezone.utc))
    with pytest.raises(SchedulerBlocked,match="indeterminate"):
        TimeScheduler(UnknownDue()).due(schedule,datetime(2026,11,18,12,tzinfo=timezone.utc))

@pytest.mark.parametrize("schedule_id,work_id,run_at", [
    (None,"76",datetime(2026,11,18,12,tzinfo=timezone.utc)),
    ("s"," ",datetime(2026,11,18,12,tzinfo=timezone.utc)),
    ("s","76","2026-11-18T12:00:00Z"),
])
def test_scheduler_rejects_malformed_schedule_fields(schedule_id,work_id,run_at):
    with pytest.raises(ValueError):
        OneShotSchedule(schedule_id,work_id,run_at)

def test_scheduler_rejects_invalid_clock_before_store_claim():
    class DueSpy:
        def __init__(self): self.called=False
        def claim_once(self,schedule_id,key): self.called=True; return True
    store=DueSpy()
    schedule=OneShotSchedule("s","76",datetime(2026,11,18,12,tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        TimeScheduler(store).due(schedule,"not-a-datetime")
    assert store.called is False


# W76-GW-004 — registered payload schema is enforced before replay reservation
def test_gateway_schema_rejection_does_not_consume_replay_identity():
    now = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    replay = Replay()
    schema = Schema()
    gateway = EventGateway(
        {"source-a": SourceRegistration("source-a", "76", frozenset({"order.created"}), schema)},
        Verifier(),
        replay,
    )

    def body(payload):
        return json.dumps({
            "event_id": "same-event-id",
            "event_type": "order.created",
            "occurred_at": now.isoformat(),
            "payload": payload,
        }).encode()

    # Missing required schema field must be rejected and must not reserve the
    # event ID; the corrected retry with the same ID must still be accepted.
    with pytest.raises(GatewayRejected, match="schema validation failed"):
        gateway.ingest("source-a", {"x-valid": "yes"}, body({"other": 1}), received_at=now)
    assert replay.seen == set()

    accepted = gateway.ingest(
        "source-a", {"x-valid": "yes"}, body({"value": 1}), received_at=now
    )
    assert accepted.event.event_id == "same-event-id"
    assert replay.seen == {("source-a", "same-event-id")}


def test_gateway_schema_exception_fails_closed_without_replay_reservation():
    now = datetime(2026, 11, 18, 12, tzinfo=timezone.utc)
    replay = Replay()

    class BrokenSchema:
        def validate(self, payload):
            raise RuntimeError("schema service unavailable")

    gateway = EventGateway(
        {"source-a": SourceRegistration("source-a", "76", frozenset({"order.created"}), BrokenSchema())},
        Verifier(),
        replay,
    )
    body = json.dumps({
        "event_id": "schema-outage",
        "event_type": "order.created",
        "occurred_at": now.isoformat(),
        "payload": {"value": 1},
    }).encode()
    with pytest.raises(GatewayRejected, match="schema validation failed"):
        gateway.ingest("source-a", {"x-valid": "yes"}, body, received_at=now)
    assert replay.seen == set()

 
# W76-PL-003 — policy requests/results must carry typed authoritative identity
def test_policy_rejects_incomplete_request_before_provider_call():
    class ProviderSpy:
        def __init__(self):
            self.called = False
        def evaluate_current(self, request):
            self.called = True
            return PolicyResult(PolicyOutcome.ALLOW, "decision-1", "rev-1", "allowed")

    with pytest.raises(ValueError, match="principal_ref"):
        PolicyRequest("", "76", "WP-76-05", "notify", "policy-1", "assignment-1", "corr-1")

    provider = ProviderSpy()
    result = PolicyAdapter(provider).authorize(None)
    assert result.outcome == PolicyOutcome.INDETERMINATE
    assert provider.called is False


@pytest.mark.parametrize("provider_result", [
    PolicyResult("ALLOW", "decision-1", "rev-1", "allowed"),
    PolicyResult(PolicyOutcome.ALLOW, "", "rev-1", "allowed"),
    PolicyResult(PolicyOutcome.ALLOW, "decision-1", "", "allowed"),
    PolicyResult(PolicyOutcome.ALLOW, "decision-1", "rev-1", ""),
])
def test_policy_malformed_authoritative_response_fails_indeterminate(provider_result):
    request = PolicyRequest("principal", "76", "WP-76-05", "notify", "policy-1", "assignment-1", "corr-1")
    result = PolicyAdapter(Provider(provider_result)).authorize(request)
    assert result.outcome == PolicyOutcome.INDETERMINATE


def test_policy_approval_ref_must_be_non_empty_string():
    request = PolicyRequest("principal", "76", "WP-76-05", "notify", "policy-1", "assignment-1", "corr-1")
    need = PolicyResult(PolicyOutcome.REQUIRE_APPROVAL, "decision-1", "rev-1", "approval required")
    result = PolicyAdapter(Provider(need), Approval()).authorize(request, object())
    assert result.outcome == PolicyOutcome.DENY


# W76-GW-005 — registration lookup key must match its trusted source identity
def test_gateway_rejects_registration_key_source_identity_mismatch():
    registration = SourceRegistration("source-b", "76", frozenset({"order.created"}), Schema())
    with pytest.raises(ValueError, match="keys must exactly match"):
        EventGateway({"source-a": registration}, Verifier(), Replay())


def test_gateway_rejects_non_registration_values():
    with pytest.raises(ValueError, match="keys must exactly match"):
        EventGateway({"source-a": object()}, Verifier(), Replay())


# W76-AU-002 — serialize concurrent in-process audit appends into one hash chain
def test_audit_writer_concurrent_appends_do_not_fork_hash_chain():
    from concurrent.futures import ThreadPoolExecutor

    sink = Sink()
    writer = AuditWriter(sink)

    def write_one(i):
        return writer.write(
            record_id=f"concurrent-{i}", work_id="76", actor_ref="svc:test",
            action="execute", outcome="accepted", correlation_id="parallel",
            payload={"index": i},
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(write_one, range(40)))

    assert len(records) == 40
    assert len(sink.rows) == 40
    assert sink.rows[0].previous_hash == ""
    for previous, current in zip(sink.rows, sink.rows[1:]):
        assert current.previous_hash == previous.record_hash


# W76-OR-002 — serialize concurrent state transitions and reject malformed metadata
def test_state_machine_concurrent_same_state_transition_only_commits_once():
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    sink = Sink()
    machine = ExecutionStateMachine(sink)
    machine.start("exec-concurrent", "corr-concurrent")
    barrier = Barrier(2)

    def advance():
        barrier.wait()
        try:
            return machine.transition(
                "exec-concurrent", ExecutionState.SOURCE_AUTHENTICATED,
                "source verified", "corr-concurrent",
            )
        except StateTransitionError:
            return "REJECTED"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: advance(), range(2)))

    assert results.count(ExecutionState.SOURCE_AUTHENTICATED) == 1
    assert results.count("REJECTED") == 1
    assert machine.state("exec-concurrent") == ExecutionState.SOURCE_AUTHENTICATED
    assert len(sink.rows) == 2


@pytest.mark.parametrize("execution_id,correlation_id", [
    ("", "corr"), (None, "corr"), ("exec", ""), ("exec", None),
])
def test_state_machine_start_rejects_malformed_identity(execution_id, correlation_id):
    machine = ExecutionStateMachine(Sink())
    with pytest.raises(StateTransitionError):
        machine.start(execution_id, correlation_id)


def test_state_machine_rejects_untyped_target_and_missing_transition_metadata():
    machine = ExecutionStateMachine(Sink())
    machine.start("exec-valid", "corr-valid")
    with pytest.raises(StateTransitionError, match="target must"):
        machine.transition("exec-valid", "FAILED", "reason", "corr-valid")
    with pytest.raises(StateTransitionError, match="reason"):
        machine.transition("exec-valid", ExecutionState.FAILED, "", "corr-valid")
