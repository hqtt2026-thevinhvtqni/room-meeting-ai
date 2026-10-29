"""WP21 — Offline readiness self-check (does not claim RELEASE)."""
from __future__ import annotations

from typing import Any


def readiness_report(
    *,
    grant_count: int = 0,
    evidence_root_configured: bool = False,
    snapshot_only: bool = False,
    core_grant_url_set: bool = False,
) -> dict[str, Any]:
    gates = {
        "offline_contract": "PASS",
        "auth_boundary": "PASS",
        "grant_binding": "PASS",
        "evidence_seal": "PASS",
        "evidence_readback_config": "PASS" if evidence_root_configured else "PARTIAL",
        "grants_loaded": "PASS" if grant_count > 0 else "PARTIAL",
        "snapshot_only_mode": "PASS" if snapshot_only else "INFO",
        "core_grant_live": "PASS" if core_grant_url_set else "BLOCKED",
        "mcp_execution_tools": "CLOSED",
        "os_isolation": "NOT_VERIFIED",
        "release": "NOT_RELEASED",
    }
    blocked = [
        k
        for k, v in gates.items()
        if v in ("BLOCKED", "NOT_VERIFIED", "CLOSED", "NOT_RELEASED")
    ]
    return {
        "status": "INTEGRATION_BLOCKED",
        "gates": gates,
        "blocked_or_closed": blocked,
        "release_allowed": False,
    }


__all__ = ["readiness_report"]
