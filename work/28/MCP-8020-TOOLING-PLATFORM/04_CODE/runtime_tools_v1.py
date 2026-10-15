"""Work 28 runtime tools v1. Adapter-only: authorization and WorkContext resolution belong to Core.
This module intentionally does not spawn processes or execute caller commands."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping

class ToolBlocked(RuntimeError):
    """A required trusted capability is unavailable or incomplete."""
class InvalidToolRequest(ValueError):
    """The tool request violates its bounded contract."""

ALLOWED_OPERATIONS = frozenset({"RUN_TESTS", "RUN_SCRIPT"})
MAX_JSON_BYTES = 16_384

def _bounded_text(value: Any, field: str, limit: int = 512) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise InvalidToolRequest(f"{field} must be non-empty text <= {limit} chars")
    return value

@dataclass(frozen=True)
class RuntimeRequest:
    work_id: str
    operation: str
    source_sha256: str
    profile_id: str
    request_id: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RuntimeRequest":
        if not isinstance(data, Mapping):
            raise InvalidToolRequest("request must be an object")
        operation = _bounded_text(data.get("operation"), "operation", 32).upper()
        if operation not in ALLOWED_OPERATIONS:
            raise InvalidToolRequest("operation is not in the approved operation set")
        sha = _bounded_text(data.get("source_sha256"), "source_sha256", 64).lower()
        if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
            raise InvalidToolRequest("source_sha256 must be a 64-character SHA-256 hex digest")
        return cls(
            work_id=_bounded_text(data.get("work_id"), "work_id", 64),
            operation=operation,
            source_sha256=sha,
            profile_id=_bounded_text(data.get("profile_id"), "profile_id", 128),
            request_id=_bounded_text(data.get("request_id"), "request_id", 128),
        )

class RuntimeToolsV1:
    """Calls only an injected authenticated Core transport; never calls a runtime directly."""
    def __init__(self, core_call: Callable[[str, Mapping[str, Any]], Mapping[str, Any]] | None):
        self._core_call = core_call

    def _call(self, action: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        if self._core_call is None:
            raise ToolBlocked("Core authenticated runtime route is not configured")
        result = self._core_call(action, payload)
        if not isinstance(result, Mapping):
            raise ToolBlocked("Core returned a malformed response")
        output = dict(result)
        if output.get("status") not in {
            "QUEUED", "RUNNING", "PASS", "FAIL", "BLOCKED", "DENIED",
            "TIMEOUT", "NOT_FOUND", "INVALID_REQUEST"
        }:
            raise ToolBlocked("Core response has an unknown status")
        return output

    def execution_submit(self, request: Mapping[str, Any]) -> dict[str, Any]:
        req = RuntimeRequest.from_mapping(request)
        # Caller-supplied identity/authorization/workspace/command fields are never forwarded.
        return self._call("execution_submit", {
            "work_id": req.work_id, "operation": req.operation,
            "source_sha256": req.source_sha256, "profile_id": req.profile_id,
            "request_id": req.request_id,
        })

    def execution_status(self, run_id: str) -> dict[str, Any]:
        return self._call("execution_status", {"run_id": _bounded_text(run_id, "run_id", 128)})

    def execution_output_read(self, run_id: str, stream: str = "combined",
                              max_bytes: int = 16_384) -> dict[str, Any]:
        run_id = _bounded_text(run_id, "run_id", 128)
        if stream not in {"stdout", "stderr", "combined"}:
            raise InvalidToolRequest("stream must be stdout, stderr, or combined")
        if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or not 1 <= max_bytes <= MAX_JSON_BYTES:
            raise InvalidToolRequest("max_bytes must be an integer between 1 and 16384")
        return self._call("execution_output_read", {
            "run_id": run_id, "stream": stream, "max_bytes": max_bytes
        })
