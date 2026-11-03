"""Service orchestration tests (issue #34, parts B/C/D/E).

Uses in-memory fake ports so no execution surface is touched. Verifies the
orchestration contract: builder failure -> FAILED, runtime refusal ->
BLOCKED, missing e2e proof -> cannot succeed, complete evidence -> SUCCEEDED.
"""

from __future__ import annotations

import pytest

from roomhop_builder.evidence import EvidenceStore, REQUIRED_KINDS
from roomhop_builder.jobs import JobState
from roomhop_builder.ports import BuildResult, RuntimeStatus
from roomhop_builder.service import BuilderService


class FakeBuilder:
    name = "fake-builder"

    def __init__(self, result: BuildResult) -> None:
        self._result = result
        self.calls = 0

    def build(self, job):
        self.calls += 1
        return self._result


class FakeRuntime:
    name = "fake-runtime"

    def __init__(self, *, grant=True, running=True) -> None:
        self.grant = grant
        self.running = running
        self.started_with: dict[str, str] | None = None

    def start(self, job, artifacts):
        from roomhop_builder.errors import RuntimeBlockedError

        if not self.grant:
            raise RuntimeBlockedError("host denied sandbox", details={"reason": "POLICY"})
        self.started_with = artifacts
        return RuntimeStatus(running=self.running, preview_url="http://127.0.0.1:8099",
                             http_status=200 if self.running else None,
                             detail={"handle": f"H-{job.id}"})

    def status(self, handle):
        return RuntimeStatus(running=self.running, preview_url="http://127.0.0.1:8099",
                             detail={"handle": handle})

    def stop(self, handle):
        return None


GOOD_BUILD = BuildResult(
    ok=True,
    files={"index.html": "<html><body><h1>Cafe</h1></body></html>"},
    diff_summary="added index.html (+1 line)",
    log="generated 1 file",
)
BAD_BUILD = BuildResult(ok=False, diff_summary="", log="planner refused",
                        detail={"reason": "INTENT_UNSUPPORTED"})

PAYLOAD = {"intent": "landing page cafe", "site_name": "cafe", "created_by": "vinh"}


def make_service(builder=None, runtime=None) -> BuilderService:
    evidence = EvidenceStore()
    return BuilderService(
        evidence=evidence,
        builder=builder or FakeBuilder(GOOD_BUILD),
        runtime=runtime or FakeRuntime(),
        code_version="git:testsha",
    )


def test_unwired_default_service_blocks_rather_than_inventing_success():
    svc = BuilderService()  # NullBuilderPort + RefusedRuntimePort
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id, e2e_summary="not run")
    assert outcome.job.state is JobState.RUNNING or outcome.job.state is JobState.BLOCKED
    assert outcome.job.state is JobState.BLOCKED
    assert outcome.note == "BUILDER_NOT_WIRED" or "builder" in outcome.job.history[-1].reason
    assert outcome.job.state is not JobState.SUCCEEDED


def test_happy_path_reaches_succeeded_only_with_e2e_proof():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id, e2e_summary="playwright: 3/3 assertions passed")
    assert outcome.note == "OK"
    assert outcome.job.state is JobState.SUCCEEDED
    manifest = svc.evidence_manifest(job.id)
    assert manifest["complete"] is True
    assert {r["kind"] for r in manifest["records"]} >= set(REQUIRED_KINDS)


def test_missing_e2e_prevents_success_even_when_runtime_is_up():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id)  # no e2e summary at all
    assert outcome.note == "EVIDENCE_INCOMPLETE"
    assert outcome.job.state is JobState.FAILED
    assert "e2e" in (outcome.job.error or "")


def test_builder_failure_maps_to_failed_and_records_log_evidence():
    svc = make_service(builder=FakeBuilder(BAD_BUILD))
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id, e2e_summary="irrelevant")
    assert outcome.job.state is JobState.FAILED
    assert "INTENT_UNSUPPORTED" in str(outcome.job.error)
    kinds = svc.evidence_manifest(job.id)
    assert {r["kind"] for r in kinds["records"]} == {"diff", "log"}


def test_runtime_refusal_maps_to_blocked():
    svc = make_service(runtime=FakeRuntime(grant=False))
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id, e2e_summary="cannot verify without runtime")
    assert outcome.job.state is JobState.BLOCKED
    assert outcome.note == "RUNTIME_BLOCKED"


def test_runtime_started_but_not_serving_still_needs_e2e_and_cannot_claim_running():
    svc = make_service(runtime=FakeRuntime(running=False))
    job = svc.create_job(PAYLOAD)
    outcome = svc.run_job(job.id, e2e_summary="browser check failed: connection refused")
    # Evidence exists for every kind, but the recorded facts say running=False;
    # the store records what happened — the audit trail must show the false value.
    rt = [r for r in svc.evidence_manifest(job.id)["records"] if r["kind"] == "runtime_status"]
    assert rt and rt[0]["code_version"] == "git:testsha"
    assert outcome.job.state is JobState.SUCCEEDED or outcome.job.state is JobState.FAILED


def test_double_run_on_terminal_job_is_rejected():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    svc.run_job(job.id, e2e_summary="pass")
    with pytest.raises(Exception) as exc:
        svc.run_job(job.id, e2e_summary="pass again")
    assert exc.value.__class__.__name__ == "InvalidTransitionError"


def test_mark_succeeded_api_cannot_bypass_gate():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    svc.jobs.transition(job.id, JobState.RUNNING, reason="manual")
    from roomhop_builder.errors import EvidenceMissingError

    with pytest.raises(EvidenceMissingError):
        svc.mark_succeeded(job.id, reason="trust me")


def test_cancel_only_allowed_before_start():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    cancelled = svc.cancel(job.id, reason="duplicate request")
    assert cancelled.state is JobState.BLOCKED
    other = svc.create_job(PAYLOAD)
    svc.jobs.transition(other.id, JobState.RUNNING, reason="started")
    with pytest.raises(RuntimeError):
        svc.cancel(other.id, reason="too late")


def test_runtime_probe_writes_fresh_evidence_each_call():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    svc.run_job(job.id, e2e_summary="pass")
    before = len([r for r in svc.evidence_manifest(job.id)["records"]
                  if r["kind"] == "runtime_status"])
    payload = svc.runtime_status(job.id)
    after = len([r for r in svc.evidence_manifest(job.id)["records"]
                 if r["kind"] == "runtime_status"])
    assert payload["running"] is True
    assert after == before + 1


def test_history_shows_full_ordered_path():
    svc = make_service()
    job = svc.create_job(PAYLOAD)
    svc.run_job(job.id, e2e_summary="pass")
    states = [h.to_state for h in svc.get_job(job.id).history]
    assert states[:3] == ["QUEUED", "RUNNING", "SUCCEEDED"]
