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
    assert machine.transition("y",ExecutionState.VALIDATED,"schema valid","c")==ExecutionState.VALIDATED
    with pytest.raises(StateTransitionError):
        machine.transition("y",ExecutionState.SUCCEEDED,"skip","c")

def test_state_machine_commits_only_after_sink_append():
    class BrokenSink:
        def append_transition(self, row): raise OSError("disk")
    machine=ExecutionStateMachine(BrokenSink()); machine.start("z","c")
    with pytest.raises(OSError):
        machine.transition("z",ExecutionState.VALIDATED,"valid","c")
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
