"""Domain errors for the Work 15 backend foundation.

Every error carries a machine-readable ``code`` so the HTTP layer can map
it to a stable response contract instead of leaking Python exception text.
"""

from __future__ import annotations


class BuilderError(Exception):
    """Base class for all domain errors."""

    code = "BUILDER_ERROR"
    http_status = 400

    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message, "details": self.details}


class ValidationError(BuilderError):
    """Input failed schema/contract validation before any state was touched."""

    code = "VALIDATION_ERROR"
    http_status = 422


class UnknownJobError(BuilderError):
    """No job exists with the requested id."""

    code = "UNKNOWN_JOB"
    http_status = 404


class InvalidTransitionError(BuilderError):
    """A lifecycle transition is not allowed by the state machine."""

    code = "INVALID_TRANSITION"
    http_status = 409


class JobNotTerminalError(BuilderError):
    """An operation requires the job to be in a terminal state."""

    code = "JOB_NOT_TERMINAL"
    http_status = 409


class EvidenceMissingError(BuilderError):
    """Attempted to mark a job SUCCEEDED without complete evidence.

    This is the anti-fake-PASS gate: WORK.md forbids reporting success
    without DIFF / LOG / PREVIEW / E2E / runtime-status proof.
    """

    code = "EVIDENCE_MISSING"
    http_status = 409


class RuntimeBlockedError(BuilderError):
    """The execution host refused to grant a sandboxed runtime."""

    code = "RUNTIME_BLOCKED"
    http_status = 409


class RuntimeFailedError(BuilderError):
    """The provisioned runtime failed to start or serve the preview."""

    code = "RUNTIME_FAILED"
    http_status = 502
