"""Cleanup attestation helpers for ExecutionHost.

Prefer spawn_managed() for new work. wrap_existing_popen() is labeled and must
never be used to claim Windows Job Object containment or isolation PASS.
"""
from __future__ import annotations

from typing import Any

from .process_job import (
    ISOLATION_STATUS,
    CleanupResult,
    ManagedProcess,
    spawn_managed,
    wrap_existing_popen,
)

__all__ = [
    "ISOLATION_STATUS",
    "attested_cleanup",
    "spawn_managed",
    "wrap_existing_popen",
    "ManagedProcess",
    "CleanupResult",
]


def attested_cleanup(managed: ManagedProcess | None) -> dict[str, Any]:
    """Serialize cleanup from a ManagedProcess (spawned or explicitly wrapped)."""
    if managed is None:
        return CleanupResult(
            process_reaped=True,
            job_object="NOT_ATTACHED",
            notes=("no_process",),
        ).as_dict()
    return managed.cleanup(terminate_first=False).as_dict()
