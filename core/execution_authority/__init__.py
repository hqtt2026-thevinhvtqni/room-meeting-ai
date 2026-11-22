"""Core execution authority implementation candidate (Work 28, contract V1.2).

This package contains source code for enrolled service identities (DR-1),
Work-scoped short-lived grants and server-side validation (DR-2), an
append-only record store with restart recovery and run/evidence linkage
(DR-3), and a separate HTTP process within the Core package boundary (DR-4).

The companion V1.2 contract remains PROPOSED / NOT APPROVED. Source presence
and CI tests do not constitute owner approval, deployment, or MCP wiring.
Nothing here wires the MCP gateway or v54 catalog.
"""
from core.execution_authority.authority import ExecutionAuthority, ExecutionAuthorityConfigError, load_enrolled_identities
from core.execution_authority.store import AppendOnlyRecordStore

__all__ = ["ExecutionAuthority", "ExecutionAuthorityConfigError", "load_enrolled_identities", "AppendOnlyRecordStore"]
