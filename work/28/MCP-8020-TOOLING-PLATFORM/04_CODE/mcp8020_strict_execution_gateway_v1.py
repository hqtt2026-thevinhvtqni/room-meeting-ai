"""Strict hash-bound execution gateway adapter (not wired into v54 service).

This adapter is a staging seam for Work 28 contract reconciliation. It accepts
only the v1 request envelope and forwards the normalized envelope to an
injected trusted Core client. It does not authorize callers, read files, hash
source, launch processes, or prove runtime identity. Keep catalog tools
NOT_IMPLEMENTED until those server-side gates and live evidence exist.
"""
from __future__ import annotations

from typing import Any, Protocol

from mcp8020_execution_contract_v1 import (
    ExecutionContractError,
    result_is_verified_pass,
    validate_python_run_request,
)


class StrictCoreExecutionClient(Protocol):
    def submit(self, request: dict[str, Any]) -> dict[str, Any]:
        """Submit to the authenticated canonical Core execution route."""
        ...


class StrictExecutionGatewayV1:
    """Narrow gateway that forwards only a validated hash-bound request."""

    def __init__(self, client: StrictCoreExecutionClient) -> None:
        if not callable(getattr(client, "submit", None)):
            raise TypeError("client must provide callable submit(request)")
        self._client = client

    def run(self, request: Any) -> dict[str, Any]:
        """Validate request shape before any client call."""
        normalized = validate_python_run_request(request)
        result = self._client.submit(normalized)
        if not isinstance(result, dict):
            raise RuntimeError("Core execution client returned a non-object result")
        return result

    @staticmethod
    def verified_pass(
        result: Any,
        expected_source_sha256: str,
        operation: str,
        expected_work_id: str | None = None,
    ) -> bool:
        """Shape-only acceptance guard; Core evidence authenticity remains external."""
        return result_is_verified_pass(
            result, expected_source_sha256, operation, expected_work_id
        )


__all__ = [
    "ExecutionContractError",
    "StrictExecutionGatewayV1",
]
