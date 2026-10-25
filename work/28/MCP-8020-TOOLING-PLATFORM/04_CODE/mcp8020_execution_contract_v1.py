"""Fail-closed validator for the proposed Work 28 Python execution contract.

This module validates request/result shape only. It does not authorize a caller,
open files, launch processes, or prove a live Core/runtime route. Those remain
mandatory server-side gates before any execution tool may be enabled.
"""
from __future__ import annotations

import re
from typing import Any

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_WORK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_ALLOWED_OPERATIONS = {"RUN_SCRIPT", "RUN_TESTS"}
_ALLOWED_RESULT_STATUSES = {
    "QUEUED", "RUNNING", "PASS", "FAIL", "TIMEOUT",
    "BLOCKED", "DENIED", "CANCELLED",
}
_ALLOWED_REQUEST_KEYS = {
    "work_id", "entry_path", "operation",
    "expected_source_sha256", "timeout_seconds",
}


class ExecutionContractError(ValueError):
    """Raised when an execution request or result violates the contract."""


def validate_python_run_request(payload: Any) -> dict[str, Any]:
    """Validate a public run request and return a normalized copy.

    Principal, cwd, interpreter, argv, environment and shell are deliberately
    absent. Core must derive identity/Work authorization from authenticated
    transport and perform canonical path containment + immutable snapshot/hash
    checks itself. This function is not an authorization boundary.
    """
    if not isinstance(payload, dict):
        raise ExecutionContractError("request must be an object")
    extra = set(payload) - _ALLOWED_REQUEST_KEYS
    missing = {"work_id", "entry_path", "operation", "expected_source_sha256"} - set(payload)
    if extra:
        raise ExecutionContractError("unsupported request fields: " + ", ".join(sorted(extra)))
    if missing:
        raise ExecutionContractError("missing required fields: " + ", ".join(sorted(missing)))

    work_id = payload["work_id"]
    if not isinstance(work_id, str) or not _WORK_ID_RE.fullmatch(work_id):
        raise ExecutionContractError("invalid work_id")

    entry_path = payload["entry_path"]
    if not isinstance(entry_path, str) or not entry_path or "\x00" in entry_path:
        raise ExecutionContractError("invalid entry_path")
    # Use a platform-independent lexical check. The authoritative server must
    # still reject symlinks/reparse points and prove resolved containment.
    normalized = entry_path.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("//") or ":" in normalized:
        raise ExecutionContractError("entry_path must be Work-relative")
    parts = normalized.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ExecutionContractError("entry_path contains unsafe path components")
    if any(part.endswith((" ", ".")) for part in parts):
        raise ExecutionContractError("entry_path contains Windows-ambiguous names")

    operation = payload["operation"]
    if not isinstance(operation, str) or operation not in _ALLOWED_OPERATIONS:
        raise ExecutionContractError("unsupported operation")

    expected_hash = payload["expected_source_sha256"]
    if not isinstance(expected_hash, str) or not _SHA256_RE.fullmatch(expected_hash):
        raise ExecutionContractError("expected_source_sha256 must be lowercase SHA-256 hex")

    timeout = payload.get("timeout_seconds", 30)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 300:
        raise ExecutionContractError("timeout_seconds must be an integer in 1..300")

    return {
        "work_id": work_id,
        "entry_path": "/".join(parts),
        "operation": operation,
        "expected_source_sha256": expected_hash,
        "timeout_seconds": timeout,
    }


def result_is_verified_pass(result: Any, expected_source_sha256: str,
                            operation: str, expected_work_id: str | None = None) -> bool:
    """Return True only for a complete, evidence-backed successful result.

    This is a result-shape guard, not proof that the evidence itself is trusted.
    Evidence integrity, runtime identity and authorization must be verified by
    the trusted Core/runtime before this function is used for acceptance.
    """
    if not isinstance(result, dict):
        return False
    if not isinstance(operation, str) or operation not in _ALLOWED_OPERATIONS:
        return False
    if not isinstance(expected_source_sha256, str) or not _SHA256_RE.fullmatch(expected_source_sha256):
        return False
    if expected_work_id is not None and (not isinstance(expected_work_id, str) or not _WORK_ID_RE.fullmatch(expected_work_id)):
        return False
    if result.get("status") != "PASS":
        return False
    exit_code = result.get("exit_code")
    if isinstance(exit_code, bool) or not isinstance(exit_code, int) or exit_code != 0:
        return False
    if result.get("source_sha256") != expected_source_sha256:
        return False
    if expected_work_id is not None and result.get("work_id") != expected_work_id:
        return False
    for key in ("request_id", "run_id", "work_id", "runtime_identity", "evidence_ref"):
        value = result.get(key)
        if not isinstance(value, str) or not value.strip():
            return False
    if operation == "RUN_TESTS":
        summary = result.get("test_summary")
        if not isinstance(summary, dict):
            return False
        total = summary.get("total")
        if isinstance(total, bool) or not isinstance(total, int) or total < 1:
            return False
        if "failed" not in summary or "errors" not in summary:
            return False
        failed = summary["failed"]
        errors = summary["errors"]
        if any(isinstance(n, bool) or not isinstance(n, int) or n < 0
               for n in (failed, errors)):
            return False
        if failed != 0 or errors != 0:
            return False
    return True
