"""Fail-closed Work 28 → canonical Work 13 /execute envelope adapter.

The canonical W13 dataclasses currently do not accept the Work 28 hash-bound
entrypoint contract. Do not manufacture an incompatible envelope and do not map
entry_path into command. This adapter refuses until Core/W13 publish a reviewed,
versioned contract and a safe server-side implementation.
"""
from __future__ import annotations

from typing import Any

from mcp8020_execution_contract_v1 import (
    ExecutionContractError,
    validate_python_run_request,
)
from mcp8020_w13_contract_compatibility_v1 import (
    W13CompatibilityError,
    audit_w13_contract_compatibility,
)


class EnvelopeError(ValueError):
    """Raised when the W13 envelope cannot be built safely."""


def build_w13_execute_envelope(
    *,
    work_context: dict[str, Any],
    run_request: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(work_context, dict):
        raise EnvelopeError("work_context must be a dict derived by Core")
    if not isinstance(run_request, dict):
        raise EnvelopeError("run_request must be a dict")

    try:
        normalized = validate_python_run_request(run_request)
        audit_w13_contract_compatibility(
            work_context=work_context,
            run_request=normalized,
        )
    except (ExecutionContractError, W13CompatibilityError) as exc:
        raise EnvelopeError(
            "W13_CANONICAL_CONTRACT_NOT_COMPATIBLE:" + str(exc)
        ) from exc

    # No safe adapter exists yet even if the schemas are later changed to
    # appear compatible: the hash-bound entrypoint must be resolved and
    # verified by a trusted server-side snapshot provider, not this mapper.
    raise EnvelopeError(
        "W13_SAFE_SERVER_SIDE_ENTRYPOINT_ADAPTER_NOT_IMPLEMENTED"
    )


def assert_not_legacy_v54_shape(payload: dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise EnvelopeError("payload must be a dict")
    if "script" in payload or (
        "entry" in payload and "entry_path" not in payload
    ):
        raise EnvelopeError(
            "legacy v54 script/entry shape is not accepted; "
            "use entry_path + expected_source_sha256"
        )
    if payload.get("operation") == "RUN_COMMAND":
        raise EnvelopeError("RUN_COMMAND has no W13 migration path")


__all__ = [
    "EnvelopeError",
    "build_w13_execute_envelope",
    "assert_not_legacy_v54_shape",
]
