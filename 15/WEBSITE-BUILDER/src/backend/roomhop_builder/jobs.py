"""Job lifecycle state machine (issue #34, part B).

States: QUEUED -> RUNNING -> SUCCEEDED | FAILED | BLOCKED.

Hard rules encoded here (not just documented):

* ``SUCCEEDED`` is unreachable unless the job's evidence bundle is
  complete (diff, log, preview, e2e report, runtime status) — verified by
  ``EvidenceStore.is_complete()`` at transition time. No fake PASS.
* Terminal states (SUCCEEDED / FAILED / BLOCKED) are immutable; a new
  attempt must be a new job. Mirrors the ROOM-HOP Core rule that
  ``closed`` is immutable and "reopen" means creating a new meeting.
* Every transition is appended to an in-record history so the backend can
  prove *when* and *why* a job moved, independently of agent narration.
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Optional

from .errors import (
    EvidenceMissingError,
    InvalidTransitionError,
    UnknownJobError,
    ValidationError,
)

TERMINAL_STATES = frozenset({"SUCCEEDED", "FAILED", "BLOCKED"})


class JobState(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


#: Allowed transitions. Anything not listed is rejected.
TRANSITIONS: dict[JobState, frozenset[JobState]] = {
    JobState.QUEUED: frozenset({JobState.RUNNING, JobState.BLOCKED, JobState.FAILED}),
    JobState.RUNNING: frozenset(
        {JobState.SUCCEEDED, JobState.FAILED, JobState.BLOCKED}
    ),
    JobState.SUCCEEDED: frozenset(),
    JobState.FAILED: frozenset(),
    JobState.BLOCKED: frozenset(),
}

#: Maximum length of the free-text request accepted from the API.
MAX_INTENT_LENGTH = 4000
MAX_SITE_NAME_LENGTH = 120


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _new_job_id() -> str:
    return f"W15-{uuid.uuid4().hex[:12]}"


@dataclass
class TransitionRecord:
    from_state: Optional[str]
    to_state: str
    at: str
    reason: str


@dataclass
class WebsiteJob:
    """One website-build request and its lifecycle record."""

    intent: str
    site_name: str
    created_by: str
    id: str = field(default_factory=_new_job_id)
    created_at: str = field(default_factory=_utcnow)
    state: JobState = JobState.QUEUED
    error: Optional[str] = None
    history: list[TransitionRecord] = field(default_factory=list)
    update_count: int = 0
    last_update_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.history:
            self.history.append(
                TransitionRecord(from_state=None, to_state=JobState.QUEUED.value,
                                 at=self.created_at, reason="created")
            )

    @property
    def is_terminal(self) -> bool:
        return self.state.value in TERMINAL_STATES

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "intent": self.intent,
            "site_name": self.site_name,
            "created_by": self.created_by,
            "state": self.state.value,
            "terminal": self.is_terminal,
            "error": self.error,
            "created_at": self.created_at,
            "update_count": self.update_count,
            "last_update_id": self.last_update_id,
            "history": [
                {"from": h.from_state, "to": h.to_state, "at": h.at, "reason": h.reason}
                for h in self.history
            ],
        }


def validate_create_payload(payload: Any) -> dict:
    """Validate a create request against the contract.

    Returns cleaned fields or raises ``ValidationError`` with a list of
    field-level problems. Deliberately strict: unknown keys are rejected so
    typos cannot silently become no-ops.
    """
    if not isinstance(payload, dict):
        raise ValidationError("payload must be a JSON object")

    allowed = {"intent", "site_name", "created_by"}
    unknown = sorted(set(payload) - allowed)
    problems: list[dict] = []
    if unknown:
        problems.append({"field": ",".join(unknown), "problem": "unknown field(s)"})

    cleaned: dict[str, str] = {}
    for key in ("intent", "site_name", "created_by"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            problems.append({"field": key, "problem": "required non-empty string"})
            continue
        value = value.strip()
        limit = MAX_INTENT_LENGTH if key == "intent" else MAX_SITE_NAME_LENGTH
        if len(value) > limit:
            problems.append({"field": key, "problem": f"longer than {limit} characters"})
            continue
        cleaned[key] = value

    if problems:
        raise ValidationError("invalid create payload", details={"problems": problems})
    return cleaned


class JobStore:
    """In-memory job registry with a validated state machine.

    Thread-safe for the small local server use case. Persistence is out of
    scope for this phase (documented as a known limitation).
    """

    def __init__(self, *, evidence_checker: Optional[Callable[[str], bool]] = None) -> None:
        self._jobs: dict[str, WebsiteJob] = {}
        self._lock = threading.RLock()
        # Injected so the SUCCESS gate checks real evidence, not a flag set
        # by the caller. Defaults to "no evidence => cannot succeed".
        self._evidence_checker = evidence_checker or (lambda job_id: False)

    # -- read ---------------------------------------------------------------

    def get(self, job_id: str) -> WebsiteJob:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise UnknownJobError(f"no job {job_id}")
            return job

    def list(self, state: Optional[str] = None) -> list[WebsiteJob]:
        with self._lock:
            jobs = list(self._jobs.values())
        if state:
            try:
                wanted = JobState(state.upper())
            except ValueError as exc:
                raise ValidationError(
                    f"invalid state filter {state!r}",
                    details={"allowed": [s.value for s in JobState]},
                ) from exc
            jobs = [j for j in jobs if j.state is wanted]
        return jobs

    # -- write --------------------------------------------------------------

    def create(self, payload: Any) -> WebsiteJob:
        fields = validate_create_payload(payload)
        job = WebsiteJob(**fields)
        with self._lock:
            self._jobs[job.id] = job
        return job

    def transition(
        self,
        job_id: str,
        to: JobState | str,
        *,
        reason: str,
        error: Optional[str] = None,
    ) -> WebsiteJob:
        if not isinstance(reason, str) or not reason.strip():
            raise ValidationError("transition requires a non-empty reason")
        try:
            target = JobState(to) if not isinstance(to, JobState) else to
        except ValueError as exc:
            raise ValidationError(
                f"unknown target state {to!r}",
                details={"allowed": [s.value for s in JobState]},
            ) from exc

        with self._lock:
            job = self.get(job_id)
            current = job.state

            if target not in TRANSITIONS[current]:
                raise InvalidTransitionError(
                    f"cannot move job {job_id} from {current.value} to {target.value}",
                    details={
                        "job_id": job_id,
                        "from": current.value,
                        "to": target.value,
                        "allowed": sorted(s.value for s in TRANSITIONS[current]),
                    },
                )

            if target is JobState.SUCCEEDED and not self._evidence_checker(job_id):
                raise EvidenceMissingError(
                    f"refusing to mark job {job_id} SUCCEEDED without complete evidence",
                    details={
                        "job_id": job_id,
                        "required_evidence": ["diff", "log", "preview", "e2e", "runtime_status"],
                    },
                )

            job.history.append(
                TransitionRecord(
                    from_state=current.value,
                    to_state=target.value,
                    at=_utcnow(),
                    reason=reason.strip(),
                )
            )
            job.state = target
            if error is not None:
                job.error = error
            elif target is not JobState.SUCCEEDED:
                job.error = None
            return job
