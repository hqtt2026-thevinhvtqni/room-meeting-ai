"""WP15 — Execution grant binding for Work 28 snapshot runs (offline).

A grant is issued only by a trusted authority (Core / deployment). Public
requests never create grants. Binding is fail-closed: any mismatch between
grant and request refuses execution before snapshot or process spawn.

This module does not perform HTTP I/O and does not open the MCP execution gate.
"""
from __future__ import annotations

import hmac
import time
from dataclasses import dataclass
from typing import Any

from .work28_contract import Work28RunRequest, validate_request


@dataclass(frozen=True)
class ExecutionGrant:
    """Server-side grant. grant_id is opaque; work_id is authoritative."""

    grant_id: str
    work_id: str
    entry_path: str
    operation: str
    expected_source_sha256: str
    expires_at_unix: float | None = None


class GrantError(ValueError):
    """Grant missing, expired, or mismatched."""


def issue_grant_for_tests(
    *,
    grant_id: str,
    work_id: str,
    entry_path: str,
    operation: str,
    expected_source_sha256: str,
    ttl_seconds: float | None = 300.0,
) -> ExecutionGrant:
    """Test/helper only — production grants come from Core, not this helper."""
    exp = None if ttl_seconds is None else time.time() + float(ttl_seconds)
    return ExecutionGrant(
        grant_id=grant_id,
        work_id=work_id,
        entry_path=entry_path,
        operation=operation,
        expected_source_sha256=expected_source_sha256,
        expires_at_unix=exp,
    )


def assert_grant_active(grant: ExecutionGrant, *, now: float | None = None) -> None:
    if not isinstance(grant, ExecutionGrant):
        raise GrantError("grant_invalid_type")
    if not grant.grant_id or not isinstance(grant.grant_id, str):
        raise GrantError("grant_id_missing")
    if grant.expires_at_unix is not None:
        ts = time.time() if now is None else now
        if ts > grant.expires_at_unix:
            raise GrantError("grant_expired")


def bind_grant_to_request(
    grant: ExecutionGrant,
    payload: dict[str, Any],
    *,
    now: float | None = None,
) -> Work28RunRequest:
    """Validate public payload and require exact match to server-side grant."""
    assert_grant_active(grant, now=now)
    request = validate_request(payload)

    if request.work_id != grant.work_id:
        raise GrantError("grant_work_mismatch")
    if request.entry_path != grant.entry_path:
        raise GrantError("grant_entry_mismatch")
    if request.operation != grant.operation:
        raise GrantError("grant_operation_mismatch")
    if not hmac.compare_digest(
        request.expected_source_sha256, grant.expected_source_sha256
    ):
        raise GrantError("grant_hash_mismatch")

    return request


__all__ = [
    "ExecutionGrant",
    "GrantError",
    "assert_grant_active",
    "bind_grant_to_request",
    "issue_grant_for_tests",
]
