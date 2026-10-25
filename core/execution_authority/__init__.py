"""Core execution authority (Work 28, contract V1.2, Gate 2).

Implements the approved Core-side execution authority: enrolled service
identities (port-agnostic, DR-1), Work-scoped short-lived grants with
server-side validation (DR-2), a durable append-only record store with
restart recovery and full run/evidence linkage (DR-3), mounted separately
from the LOCKED v0.1 meeting API but inside the Core authority boundary
(DR-4). Nothing here wires the MCP gateway or v54 catalog.
"""
from core.execution_authority.authority import ExecutionAuthority, ExecutionAuthorityConfigError, load_enrolled_identities
from core.execution_authority.store import AppendOnlyRecordStore

__all__ = ["ExecutionAuthority", "ExecutionAuthorityConfigError", "load_enrolled_identities", "AppendOnlyRecordStore"]
