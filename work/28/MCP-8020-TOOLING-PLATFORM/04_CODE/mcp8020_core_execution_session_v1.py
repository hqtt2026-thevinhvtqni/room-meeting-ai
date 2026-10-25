"""Core grant execution session: closes the grant lifecycle around runs.

Integration slice step 2 (approved 2026-10-25): issue a Work-scoped grant
from the Core authority, hold the grant token ONLY in memory for the
lifetime of the session, re-validate it server-side BEFORE every run
recording, and refuse recording when the grant is revoked, expired, or the
token does not match. Denials happen before any side effect: nothing is
appended to the append-only store when validation fails.

STAGED and NOT WIRED into MCP registration or the v54 catalog. The runtime
remains an injected interface: this session binds authorization and
bookkeeping, not execution itself.
"""
from __future__ import annotations

from typing import Any

from mcp8020_core_authority_authorizer_v1 import require_core_canonical_work_id


class CoreExecutionSessionError(RuntimeError):
    """Raised when the session is misused against its own state."""


class CoreGrantExecutionSession:
    """One Work-scoped grant lifecycle bound to the Core authority."""

    def __init__(self, *, authority: Any, work_id: Any, credential: Any,
                 purpose: Any, grant_seconds: int | None = None) -> None:
        for method in ("issue_grant", "validate_grant_token", "record_run", "revoke_grant"):
            if not callable(getattr(authority, method, None)):
                raise TypeError("authority must provide " + method)
        work_id = require_core_canonical_work_id(work_id)
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("purpose must be a non-empty string")
        identity = authority.authenticate(credential)
        if not authority.is_identity_allowed_for_work(identity, work_id):
            raise PermissionError("caller_not_authorized_for_work")
        if grant_seconds is None:
            grant = authority.issue_grant(identity, work_id, purpose)
        else:
            grant = authority.issue_grant(identity, work_id, purpose, grant_seconds)
        if not grant.get("grant_token") or not grant.get("grant_id"):
            raise CoreExecutionSessionError("authority returned an incomplete grant")
        self._authority = authority
        self._identity = identity
        self._work_id = work_id
        self._grant_id = grant["grant_id"]
        self._grant_token = grant["grant_token"]

    @property
    def work_id(self) -> str:
        return self._work_id

    @property
    def grant_id(self) -> str:
        return self._grant_id

    def validate_for_run(self) -> dict[str, Any]:
        """Server-side DR-2 check before any side effect."""
        return self._authority.validate_grant_token(self._grant_id, self._grant_token)

    def record_run(self, *, source_sha256: str, exit_status: str,
                   output_refs: list[str], evidence_refs: list[str],
                   handoff_ids: list[str]) -> dict[str, Any]:
        """Re-validate the grant, then record the run against it."""
        self.validate_for_run()
        return self._authority.record_run(
            self._grant_id,
            source_sha256=source_sha256,
            exit_status=exit_status,
            output_refs=list(output_refs or []),
            evidence_refs=list(evidence_refs),
            handoff_ids=list(handoff_ids or []),
        )

    def revoke(self) -> dict[str, Any]:
        outcome = self._authority.revoke_grant(self._grant_id)
        self._grant_token = None
        return outcome


__all__ = ["CoreExecutionSessionError", "CoreGrantExecutionSession"]
