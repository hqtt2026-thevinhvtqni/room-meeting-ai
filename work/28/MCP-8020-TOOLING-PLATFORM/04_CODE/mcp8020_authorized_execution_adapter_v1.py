"""Fail-closed policy seam for Work 28 -> canonical W13 execution host.

This module is intentionally NOT wired into MCP registration or v54 service.
Security-sensitive capabilities are injected from trusted server-side components:
caller identity must come from authenticated middleware, authorization from Core,
snapshot metadata from a canonical Work resolver, and runtime identity from an
approved deployment configuration. This adapter does not itself authenticate,
read files, hash source bytes, launch processes, or attest evidence.
"""
from __future__ import annotations

from typing import Any, Protocol

from mcp8020_execution_contract_v1 import (
    ExecutionContractError,
    validate_python_run_request,
)


class CoreAuthorizer(Protocol):
    def authorize(self, trusted_caller: Any, work_id: str) -> bool: ...


class SourceSnapshotProvider(Protocol):
    def create_immutable_snapshot(self, work_id: str, entry_path: str) -> dict[str, Any]: ...


class PinnedExecutionRuntime(Protocol):
    def execute_snapshot(
        self, snapshot: dict[str, Any], operation: str, timeout_seconds: int,
    ) -> dict[str, Any]: ...


class AuthorizedExecutionAdapterV1:
    """Enforce the required security gates around injected trusted components."""

    def __init__(
        self,
        *,
        authorizer: CoreAuthorizer,
        snapshots: SourceSnapshotProvider,
        runtime: PinnedExecutionRuntime,
        approved_runtime_identity: str,
    ) -> None:
        if not callable(getattr(authorizer, "authorize", None)):
            raise TypeError("authorizer must provide authorize(trusted_caller, work_id)")
        if not callable(getattr(snapshots, "create_immutable_snapshot", None)):
            raise TypeError("snapshots must provide create_immutable_snapshot(work_id, entry_path)")
        if not callable(getattr(runtime, "execute_snapshot", None)):
            raise TypeError("runtime must provide execute_snapshot(snapshot, operation, timeout_seconds)")
        if not isinstance(approved_runtime_identity, str) or not approved_runtime_identity.strip():
            raise ValueError("an independently approved runtime identity is required")
        self._authorizer = authorizer
        self._snapshots = snapshots
        self._runtime = runtime
        self._approved_runtime_identity = approved_runtime_identity

    def run(self, request: Any, *, trusted_caller: Any) -> dict[str, Any]:
        """Run only when trusted authorization and all attestation gates pass.

        trusted_caller is supplied by the server integration, never read from the
        public request object. Every failure before runtime dispatch fails closed.
        """
        normalized = validate_python_run_request(request)
        if trusted_caller is None:
            raise PermissionError("authenticated caller context is required")
        if self._authorizer.authorize(trusted_caller, normalized["work_id"]) is not True:
            raise PermissionError("Core denied caller access to this Work")

        snapshot = self._snapshots.create_immutable_snapshot(
            normalized["work_id"], normalized["entry_path"]
        )
        if not isinstance(snapshot, dict):
            raise RuntimeError("snapshot provider returned a non-object")
        if snapshot.get("work_id") != normalized["work_id"]:
            raise RuntimeError("snapshot Work binding mismatch")
        if snapshot.get("entry_path") != normalized["entry_path"]:
            raise RuntimeError("snapshot entry path mismatch")
        if snapshot.get("immutable") is not True:
            raise RuntimeError("source snapshot is not attested immutable")
        if snapshot.get("source_sha256") != normalized["expected_source_sha256"]:
            raise RuntimeError("source hash mismatch; execution refused")
        snapshot_ref = snapshot.get("snapshot_ref")
        if not isinstance(snapshot_ref, str) or not snapshot_ref.strip():
            raise RuntimeError("immutable snapshot reference is required")

        result = self._runtime.execute_snapshot(
            snapshot, normalized["operation"], normalized["timeout_seconds"]
        )
        if not isinstance(result, dict):
            raise RuntimeError("runtime returned a non-object result")
        if result.get("runtime_identity") != self._approved_runtime_identity:
            raise RuntimeError("runtime identity mismatch")
        if result.get("work_id") != normalized["work_id"]:
            raise RuntimeError("runtime result Work binding mismatch")
        if result.get("source_sha256") != normalized["expected_source_sha256"]:
            raise RuntimeError("runtime result source hash mismatch")
        if result.get("snapshot_ref") != snapshot_ref:
            raise RuntimeError("runtime did not attest the exact immutable snapshot")
        for key in ("request_id", "run_id", "evidence_ref"):
            value = result.get(key)
            if not isinstance(value, str) or not value.strip():
                raise RuntimeError(f"runtime result missing trusted {key}")
        exit_code = result.get("exit_code")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            raise RuntimeError("runtime result must include an integer exit_code")
        if result.get("process_tree_cleanup_verified") is not True:
            raise RuntimeError("process-tree cleanup is not verified")
        if normalized["operation"] == "RUN_TESTS":
            summary = result.get("test_summary")
            if not isinstance(summary, dict):
                raise RuntimeError("test summary is required")
            total, failed, errors = summary.get("total"), summary.get("failed"), summary.get("errors")
            if (isinstance(total, bool) or not isinstance(total, int) or total < 1
                    or isinstance(failed, bool) or not isinstance(failed, int) or failed != 0
                    or isinstance(errors, bool) or not isinstance(errors, int) or errors != 0):
                raise RuntimeError("test run did not provide a non-empty clean test summary")
        return dict(result)


__all__ = ["AuthorizedExecutionAdapterV1"]
