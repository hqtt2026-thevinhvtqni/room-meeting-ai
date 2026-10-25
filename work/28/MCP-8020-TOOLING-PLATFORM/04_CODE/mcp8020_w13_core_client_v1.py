"""Staged CoreExecutionClient seam over the hardened W13 execution host.

This module implements the seven-method CoreExecutionClient protocol expected
by ExecutionGateway (mcp8020_execution_gateway_v54) on top of the WEE
ExecutionHostBridge, which now carries the deployment execution token.

It is deliberately STAGED and NOT WIRED: no MCP registration or v54 service
import references it. Flipping the v54 execution tools from NOT_IMPLEMENTED to
IMPLEMENTED requires deployment evidence (armed startup, live 401/403 probe,
E2E Core :8000 -> W13 run with bound evidence), per the Work 28 gate rules.

Trust model:
* work_context_provider(work_id) must be supplied by trusted server-side
  composition; it derives the authoritative WorkContext (including the
  authorized flag) from Core, never from the public request.
* request_builder(request) maps a validated gateway request into the W13
  ExecutionRequest payload. It must reject arbitrary shell input upstream.
* The bridge enforces token authentication and surfaces exact HTTP statuses.
* This client adds an in-memory run registry keyed by execution_id; any run_id
  unknown to the registry answers BLOCKED. Cancel is refused: the synchronous
  bridge boundary has no verified process-tree cancellation path yet.
"""
from __future__ import annotations

from typing import Any

from mcp8020_catalog_v54 import ToolCallError

_ALLOWED_STATUSES = ("PASS", "FAIL", "TIMEOUT", "BLOCKED", "DENIED", "CANCELLED")
_HANDOFF_STATUSES = ("PASS", "FAIL", "BLOCKED", "TIMEOUT")


class W13CoreExecutionClientV1:
    """Fail-closed CoreExecutionClient adapter over ExecutionHostBridge."""

    def __init__(self, *, bridge: Any, work_context_provider: Any, request_builder: Any) -> None:
        if not callable(getattr(bridge, "invoke", None)):
            raise ToolCallError("INVALID_INPUT", "bridge must provide invoke(work_context, execution_request)")
        if not callable(work_context_provider):
            raise ToolCallError("INVALID_INPUT", "work_context_provider must be callable(work_id)")
        if not callable(request_builder):
            raise ToolCallError("INVALID_INPUT", "request_builder must be callable(request)")
        self._bridge = bridge
        self._work_context_provider = work_context_provider
        self._request_builder = request_builder
        self._runs: dict[str, dict[str, Any]] = {}

    @staticmethod
    def _as_dict(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return dict(value)
        if hasattr(value, "as_dict"):
            return dict(value.as_dict())
        raise ToolCallError("BLOCKED", "execution_host_returned_non_object")

    @staticmethod
    def _record(result: Any) -> dict[str, Any]:
        entry = W13CoreExecutionClientV1._as_dict(result)
        status = entry.get("status")
        if status not in _ALLOWED_STATUSES:
            entry["status"] = "BLOCKED"
            entry.setdefault("blocker", "unknown_execution_host_status")
        return entry

    def submit(self, request: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(request, dict):
            raise ToolCallError("INVALID_INPUT", "request must be a mapping")
        work_id = request.get("work_id")
        if not isinstance(work_id, str) or not work_id.strip():
            raise ToolCallError("INVALID_INPUT", "request must carry a non-empty work_id")
        context = self._work_context_provider(work_id)
        run = self._request_builder(request)
        result = self._bridge.invoke(context, run)
        entry = self._record(result)
        run_id = entry.get("execution_id")
        if not isinstance(run_id, str) or not run_id.strip():
            blocker = entry.get("blocker") or "execution_host_returned_no_execution_id"
            raise ToolCallError("BLOCKED", "execution did not start: " + blocker)
        entry["submitted_work_id"] = work_id
        self._runs[run_id] = entry
        return {"run_id": run_id, "status": entry["status"], "work_id": entry.get("work_id") or work_id}

    def _lookup(self, run_id: str) -> dict[str, Any]:
        entry = self._runs.get(run_id)
        if entry is None:
            raise ToolCallError("BLOCKED", "unknown_execution_run_id")
        return entry

    def get_status(self, run_id: str) -> dict[str, Any]:
        entry = self._lookup(run_id)
        return {"run_id": run_id, "status": entry["status"], "work_id": entry.get("work_id")}

    def get_result(self, run_id: str) -> dict[str, Any]:
        entry = self._lookup(run_id)
        return {
            "run_id": run_id,
            "status": entry["status"],
            "exit_code": entry.get("exit_code"),
            "stdout_ref": entry.get("stdout_ref"),
            "stderr_ref": entry.get("stderr_ref"),
            "evidence_ref": entry.get("evidence_ref"),
        }

    def cancel(self, run_id: str) -> dict[str, Any]:
        raise ToolCallError("BLOCKED", "cancel_not_supported_synchronous_boundary")

    def collect_artifact(self, run_id: str, artifact_path: str) -> dict[str, Any]:
        entry = self._lookup(run_id)
        artifacts = entry.get("artifacts") or []
        if artifact_path not in artifacts:
            raise ToolCallError("BLOCKED", "artifact_not_in_run_manifest")
        return {"run_id": run_id, "artifact_path": artifact_path, "artifacts": list(artifacts)}

    def generate_evidence(self, run_id: str, evidence_type: str, refs: list[str]) -> dict[str, Any]:
        entry = self._lookup(run_id)
        evidence_ref = entry.get("evidence_ref")
        if not isinstance(evidence_ref, str) or not evidence_ref.strip():
            raise ToolCallError("BLOCKED", "run_has_no_bound_evidence_reference")
        return {
            "run_id": run_id,
            "evidence_type": evidence_type,
            "evidence_ref": evidence_ref,
            "refs": list(refs),
            "status": entry["status"],
        }

    def create_handoff(self, work_id: str, status: str, evidence_refs: list[str], next_action: str) -> dict[str, Any]:
        if status not in _HANDOFF_STATUSES:
            raise ToolCallError("INVALID_INPUT", "handoff status must be PASS, FAIL, BLOCKED, or TIMEOUT")
        if not isinstance(evidence_refs, list) or not evidence_refs:
            raise ToolCallError("INVALID_INPUT", "handoff requires at least one evidence reference")
        for ref in evidence_refs:
            if not isinstance(ref, str) or not ref.strip():
                raise ToolCallError("INVALID_INPUT", "evidence references must be non-empty strings")
        return {
            "work_id": work_id,
            "status": status,
            "evidence_refs": list(evidence_refs),
            "next_action": next_action,
        }


__all__ = ["W13CoreExecutionClientV1"]
