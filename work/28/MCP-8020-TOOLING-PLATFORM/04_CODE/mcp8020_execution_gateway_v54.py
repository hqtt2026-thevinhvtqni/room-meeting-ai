"""Work 28 v54 execution gateway: protocol-complete but deliberately UNWIRED.

Implements the seven sandbox execution/evidence tool handlers against an
injected CoreExecutionClient. No concrete client ships in this build because
the authenticated Core route, the canonical W12-W13 runtime, and the OS
isolation gate are not yet evidenced (PROPOSED_EXECUTION_TOOL_CONTRACT_V1
section 5: NO-GO). Wiring a concrete, evidenced client is what flips these
tools from NOT_IMPLEMENTED to IMPLEMENTED in the v54 catalog. Until then the
service answers them with a stable NOT_IMPLEMENTED error. Nothing here fakes
a PASS: every status comes from the client, and BLOCKED is the default.
"""
from __future__ import annotations
from typing import Any, Protocol
from mcp8020_catalog_v54 import ToolCallError

class CoreExecutionClient(Protocol):
    """Contract the canonical Core :8000 -> W12/W13 route must satisfy."""

    def submit(self, request: dict[str, Any]) -> dict[str, Any]:
        """Start a bounded run. Returns run_id and initial status."""
        ...

    def get_status(self, run_id: str) -> dict[str, Any]:
        """Return the authoritative run status: PASS, FAIL, TIMEOUT, BLOCKED, DENIED, CANCELLED, QUEUED, RUNNING."""
        ...

    def get_result(self, run_id: str) -> dict[str, Any]:
        """Return exit code and bounded output references for a finished run."""
        ...

    def cancel(self, run_id: str) -> dict[str, Any]:
        """Cancel the process tree; CANCELLED only when cleanup is verified."""
        ...

    def collect_artifact(self, run_id: str, artifact_path: str) -> dict[str, Any]:
        """Return artifact metadata and hash for a run."""
        ...

    def generate_evidence(self, run_id: str, evidence_type: str, refs: list[str]) -> dict[str, Any]:
        """Bind request/run/exit/output/source references into an evidence record."""
        ...

    def create_handoff(self, work_id: str, status: str, evidence_refs: list[str], next_action: str) -> dict[str, Any]:
        """Create a handoff record referencing verified evidence."""
        ...

class BlockedExecutionClient:
    """Fail-closed client used when no verified Core route exists."""

    def _blocked(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise ToolCallError("BLOCKED", "no verified Core :8000 execution route is wired in this build")

    submit = _blocked
    get_status = _blocked
    get_result = _blocked
    cancel = _blocked
    collect_artifact = _blocked
    generate_evidence = _blocked
    create_handoff = _blocked

_REQUIRED_METHODS = ("submit", "get_status", "get_result", "cancel", "collect_artifact", "generate_evidence", "create_handoff")

class ExecutionGateway:
    """Binds the seven v54 execution/evidence tools to a CoreExecutionClient."""

    def __init__(self, client: CoreExecutionClient) -> None:
        for method in _REQUIRED_METHODS:
            if not callable(getattr(client, method, None)):
                raise ToolCallError("INVALID_INPUT", "client does not satisfy CoreExecutionClient: missing " + method)
        self._client = client

    def sandbox_run_python(self, work_id: str, script: str, args: list[str] | None = None, timeout_seconds: int = 30) -> dict[str, Any]:
        request = {"operation": "RUN_SCRIPT", "language": "python", "work_id": work_id, "entry": script, "args": list(args or []), "timeout_seconds": timeout_seconds}
        return self._client.submit(request)

    def sandbox_run_command(self, work_id: str, command: str, args: list[str] | None = None, timeout_seconds: int = 30) -> dict[str, Any]:
        # The client remains the authority on the allowlist; the gateway never
        # constructs a shell string, passes through a label + argv only.
        request = {"operation": "RUN_COMMAND", "work_id": work_id, "entry": command, "args": list(args or []), "timeout_seconds": timeout_seconds}
        return self._client.submit(request)

    def sandbox_get_execution_status(self, run_id: str) -> dict[str, Any]:
        return self._client.get_status(run_id)

    def sandbox_get_execution_result(self, run_id: str) -> dict[str, Any]:
        return self._client.get_result(run_id)

    def sandbox_collect_artifact(self, run_id: str, artifact_path: str) -> dict[str, Any]:
        return self._client.collect_artifact(run_id, artifact_path)

    def sandbox_generate_evidence(self, run_id: str, evidence_type: str, refs: list[str] | None = None) -> dict[str, Any]:
        return self._client.generate_evidence(run_id, evidence_type, list(refs or []))

    def sandbox_create_handoff(self, work_id: str, status: str, evidence_refs: list[str] | None = None, next_action: str = "") -> dict[str, Any]:
        if status not in ("PASS", "FAIL", "BLOCKED", "TIMEOUT"):
            raise ToolCallError("INVALID_INPUT", "handoff status must be PASS, FAIL, BLOCKED, or TIMEOUT")
        return self._client.create_handoff(work_id, status, list(evidence_refs or []), next_action)
