"""Fail-closed compatibility gate for Work 28 -> canonical Work 13 /execute.

This module checks schema and Work binding only. It is not an authorization
boundary: a plain dict, including authorized=True, cannot prove provenance.
"""
from __future__ import annotations

from typing import Any

from mcp8020_execution_contract_v1 import (
    ExecutionContractError,
    validate_python_run_request,
)


class W13CompatibilityError(ValueError):
    """Raised when a Work 28 request cannot safely map to canonical W13."""


W13_WORK_CONTEXT_REQUIRED = frozenset({
    "work_id", "work_name", "workspace_root", "execution_workspace",
    "evidence_root", "authorized",
})
W13_EXECUTION_REQUEST_ALLOWED = frozenset({
    "command", "timeout_seconds", "collect_artifacts", "run_test",
})
W28_HASH_BOUND_REQUEST_REQUIRED = frozenset({
    "work_id", "entry_path", "operation", "expected_source_sha256",
})


def audit_w13_contract_compatibility(
    *, work_context: Any, run_request: Any
) -> dict[str, Any]:
    """Return a schema diagnostic; never treat caller data as trusted authority.

    Deliberately does not map entry_path to command, derive authorization from
    a request body, or claim that a caller-provided hash was verified.
    """
    if not isinstance(work_context, dict):
        raise W13CompatibilityError("W13_WORK_CONTEXT_MUST_BE_CORE_DERIVED_OBJECT")
    missing_context = sorted(W13_WORK_CONTEXT_REQUIRED - set(work_context))
    if missing_context:
        raise W13CompatibilityError(
            "W13_WORK_CONTEXT_REQUIRED_FIELDS_MISSING:" + ",".join(missing_context)
        )
    context_work_id = work_context.get("work_id")
    if not isinstance(context_work_id, str) or not context_work_id.strip():
        raise W13CompatibilityError("W13_WORK_CONTEXT_INVALID_WORK_ID")

    if not isinstance(run_request, dict):
        raise W13CompatibilityError("W28_RUN_REQUEST_MUST_BE_OBJECT")
    try:
        normalized = validate_python_run_request(run_request)
    except ExecutionContractError as exc:
        raise W13CompatibilityError("W28_CONTRACT_INVALID:" + str(exc)) from exc

    if context_work_id != normalized["work_id"]:
        raise W13CompatibilityError("W13_WORK_CONTEXT_WORK_ID_MISMATCH")

    unsupported = sorted(set(normalized) - W13_EXECUTION_REQUEST_ALLOWED)
    missing_w13 = sorted({"command"} - set(normalized))
    if unsupported or missing_w13:
        parts = []
        if unsupported:
            parts.append("W28_FIELDS_UNSUPPORTED_BY_W13:" + ",".join(unsupported))
        if missing_w13:
            parts.append("W13_EXECUTION_REQUEST_FIELDS_MISSING:" + ",".join(missing_w13))
        parts.append("UNSAFE_MAPPING_REFUSED_NO_ENTRY_PATH_TO_COMMAND_TRANSLATION")
        raise W13CompatibilityError(";".join(parts))

    # This branch is diagnostic only; callers must still use trusted Core,
    # authenticated caller identity, a snapshot provider, and pinned runtime.
    return {
        "compatible": True,
        "work_id": normalized["work_id"],
        "request_contract": "W28_HASH_BOUND_V1",
        "w13_request_contract": "W13_EXECUTION_REQUEST_SNAPSHOT",
        "note": "Schema compatibility only; authentication and runtime gates remain external.",
    }


__all__ = [
    "W13CompatibilityError",
    "audit_w13_contract_compatibility",
    "W13_WORK_CONTEXT_REQUIRED",
    "W13_EXECUTION_REQUEST_ALLOWED",
]
