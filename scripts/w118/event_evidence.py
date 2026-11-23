"""Build immutable, non-authoritative event evidence records for Work 118."""
from __future__ import annotations

import re
from typing import Any


def build_event_evidence(
    *,
    event_type: str,
    event_id: str,
    source_commit: str,
    run_id: int,
    run_attempt: int,
    actor: str,
    decision: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    required = {
        "event_type": event_type,
        "event_id": event_id,
        "source_commit": source_commit,
        "actor": actor,
        "decision": decision,
    }
    for key, value in required.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a non-empty string")
    if type(run_id) is not int or run_id < 1:
        raise ValueError("run_id must be a positive integer")
    if type(run_attempt) is not int or run_attempt < 1:
        raise ValueError("run_attempt must be a positive integer")
    if re.fullmatch(r"[0-9a-fA-F]{40}", source_commit) is None:
        raise ValueError("source_commit must be a full 40-character hexadecimal SHA")
    if details is not None and not isinstance(details, dict):
        raise ValueError("details must be an object")

    return {
        "schema_version": "1.0",
        "work_id": "118",
        "evidence_type": "OPERATION",
        "producer": "W118 Auto E2E Validation",
        "event_type": event_type,
        "event_id": event_id,
        "source_commit": source_commit,
        "run_id": run_id,
        "run_attempt": run_attempt,
        "actor": actor,
        "decision": decision,
        "details": details or {},
        "state": "RECORDED",
        "limitations": [
            "This event artifact is not a Work 70 Evidence Register row.",
            "RECORDED does not mean VERIFIED, ACCEPTED or RELEASED."
        ],
    }
