"""Application service for Work 15 backend (issue #34).

Wires the state machine, evidence store and Builder/Runtime ports into one
orchestration entry point. The HTTP layer will call only this class — no
business logic lives in routes (same rule as ``room_hop_mcp/adapter/http_server.py``:
validate shape, call service, map response).

Orchestration contract for ``run_job``:

1. QUEUED -> RUNNING            (else nothing happens)
2. BuilderPort.build(job)       -> record diff/log evidence
3. RuntimePort.start(...)       -> record preview + runtime_status evidence
4. e2e evidence supplied by caller (never invented here)
5. SUCCEEDED only if evidence complete; otherwise FAILED / BLOCKED with reason

A blocked or failed step always leaves a written reason in history, so Xu/Qw
can audit *why* without trusting any agent's prose.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Any, Optional

from .evidence import EvidenceStore
from .errors import BuilderError, RuntimeBlockedError
from .jobs import JobState, JobStore, WebsiteJob
from .ports import BuildResult, NullBuilderPort, RefusedRuntimePort, RuntimePort, BuilderPort


@dataclass
class RunOutcome:
    job: WebsiteJob
    build: Optional[BuildResult]
    runtime: dict[str, Any]
    note: str


class BuilderService:
    def __init__(
        self,
        *,
        jobs: Optional[JobStore] = None,
        evidence: Optional[EvidenceStore] = None,
        builder: Optional[BuilderPort] = None,
        runtime: Optional[RuntimePort] = None,
        code_version: str = "unversioned",
    ) -> None:
        self.evidence = evidence or EvidenceStore()
        # The SUCCESS gate reads the evidence store, never a caller-supplied flag.
        self.jobs = jobs or JobStore(evidence_checker=self.evidence.is_complete)
        self.builder = builder or NullBuilderPort()
        self.runtime = runtime or RefusedRuntimePort()
        self.code_version = code_version
        self._handles: dict[str, Any] = {}
        self._lock = threading.RLock()

    # -- queries ------------------------------------------------------------

    def get_job(self, job_id: str) -> WebsiteJob:
        return self.jobs.get(job_id)

    def list_jobs(self, state: Optional[str] = None) -> list[WebsiteJob]:
        return self.jobs.list(state)

    def evidence_manifest(self, job_id: str) -> dict[str, Any]:
        self.jobs.get(job_id)  # 404 for unknown job
        return self.evidence.manifest(job_id)

    def runtime_status(self, job_id: str) -> dict[str, Any]:
        """Live probe of the runtime — result is observed, not remembered."""
        job = self.jobs.get(job_id)
        with self._lock:
            handle = self._handles.get(job.id)
        status = self.runtime.status(handle) if handle else None
        payload = status.to_dict() if status else {"running": False, "reason": "NO_HANDLE"}
        if handle is not None:
            self.evidence.add(
                job.id,
                "runtime_status",
                summary=f"probe: running={payload.get('running')}",
                code_version=self.code_version,
                payload=payload,
            )
        return payload

    # -- commands -----------------------------------------------------------

    def create_job(self, payload: Any) -> WebsiteJob:
        return self.jobs.create(payload)

    def add_evidence(
        self, job_id: str, kind: str, *, summary: str, payload: Optional[dict] = None
    ) -> dict[str, Any]:
        self.jobs.get(job_id)
        record = self.evidence.add(
            job_id, kind, summary=summary, code_version=self.code_version, payload=payload
        )
        return record.to_dict()

    def mark_succeeded(self, job_id: str, *, reason: str) -> WebsiteJob:
        """Explicit success attempt. Raises EVIDENCE_MISSING if proof is absent."""
        return self.jobs.transition(job_id, JobState.SUCCEEDED, reason=reason)

    def run_job(self, job_id: str, *, e2e_summary: Optional[str] = None) -> RunOutcome:
        job = self.jobs.get(job_id)
        self.jobs.transition(job_id, JobState.RUNNING, reason="worker picked up job")

        try:
            build = self.builder.build(job)
        except BuilderError as exc:
            self.jobs.transition(job_id, JobState.BLOCKED, reason=f"builder error: {exc.message}")
            return RunOutcome(job=self.jobs.get(job_id), build=None, runtime={}, note=exc.code)

        self.evidence.add(
            job.id, "diff",
            summary=build.diff_summary or "builder returned no diff summary",
            code_version=self.code_version, payload=build.to_dict(),
        )
        self.evidence.add(
            job.id, "log",
            summary=build.log or "builder returned empty log",
            code_version=self.code_version, payload={"ok": build.ok},
        )

        if not build.ok:
            reason = build.detail.get("reason", "unknown")
            # A builder that was never wired is an un-integrated boundary,
            # not a work failure -> BLOCKED (issue #34 part C wording).
            state = JobState.BLOCKED if reason == "BUILDER_NOT_WIRED" else JobState.FAILED
            self.jobs.transition(
                job_id, state,
                reason=f"builder reported failure: {reason}",
                error=str(build.detail),
            )
            return RunOutcome(job=self.jobs.get(job_id), build=build, runtime={},
                              note="BUILD_FAILED" if state is JobState.FAILED
                              else "BUILDER_NOT_WIRED")

        try:
            status = self.runtime.start(job, build.files)
        except RuntimeBlockedError as exc:
            self.jobs.transition(job_id, JobState.BLOCKED, reason=f"runtime refused: {exc.message}")
            return RunOutcome(job=self.jobs.get(job_id), build=build, runtime={}, note=exc.code)

        with self._lock:
            self._handles[job.id] = status.detail.get("handle")

        self.evidence.add(
            job.id, "preview",
            summary=f"preview at {status.preview_url}" if status.preview_url else "no preview url",
            code_version=self.code_version, payload=status.to_dict(),
        )
        self.evidence.add(
            job.id, "runtime_status",
            summary=f"runtime running={status.running} http={status.http_status}",
            code_version=self.code_version, payload=status.to_dict(),
        )

        if e2e_summary:
            self.evidence.add(
                job.id, "e2e", summary=e2e_summary, code_version=self.code_version,
                payload={"source": "external verifier"},
            )

        if not self.evidence.is_complete(job.id):
            self.jobs.transition(
                job_id, JobState.FAILED,
                reason=f"missing evidence: {','.join(self.evidence.missing_kinds(job.id))}",
                error=",".join(self.evidence.missing_kinds(job.id)),
            )
            return RunOutcome(job=self.jobs.get(job_id), build=build,
                              runtime=status.to_dict(), note="EVIDENCE_INCOMPLETE")

        final = self.jobs.transition(job_id, JobState.SUCCEEDED,
                                     reason="all required evidence recorded")
        return RunOutcome(job=final, build=build, runtime=status.to_dict(), note="OK")

    def cancel(self, job_id: str, *, reason: str) -> WebsiteJob:
        """QUEUED jobs can be dropped; RUNNING jobs must reach a real terminal state."""
        job = self.jobs.get(job_id)
        if job.state is JobState.QUEUED:
            return self.jobs.transition(job_id, JobState.BLOCKED,
                                        reason=f"cancelled before start: {reason}")
        raise RuntimeError(f"job {job_id} already {job.state.value}; cannot cancel")
