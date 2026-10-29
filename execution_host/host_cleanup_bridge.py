"""Shared cleanup attestation for ExecutionHost results.

Used so host.py can stay thin while cleanup is never a bare {process_reaped: bool}.
"""
from __future__ import annotations

from typing import Any

from .process_job import CleanupResult, ManagedProcess


def attested_cleanup(process) -> dict[str, Any]:
    if process is None:
        return CleanupResult(process_reaped=True, notes=("no_process",)).as_dict()
    return ManagedProcess(process).cleanup(terminate_first=False).as_dict()


ISOLATION_STATUS = "NOT_VERIFIED"  # process reaping != OS sandbox
