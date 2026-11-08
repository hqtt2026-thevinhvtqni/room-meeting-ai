from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Callable
from urllib import error, request

_WORK_ID = re.compile(r"^W[0-9]+$")


@dataclass(frozen=True)
class BridgeResult:
    execution_id: str | None
    work_id: str | None
    status: str
    evidence_ref: str | None = None
    exit_code: int | None = None
    stdout_ref: str | None = None
    stderr_ref: str | None = None
    artifacts: list[str] | None = None
    blocker: str | None = None
    cleanup: dict[str, Any] | None = None
    provider_type: str = "HTTP_EXECUTION_HOST"
    runtime_instance_id: str | None = None
    runtime_build_hash: str | None = None
    runtime_started_at: str | None = None
    runtime_pid: int | None = None
    runtime_platform: str | None = None
    runtime_bind_address: str | None = None
    raw: dict[str, Any] | None = None

    def as_dict(self):
        return asdict(self)


class ExecutionHostBridge:
    """WEE boundary: obtain a Core grant, then call the Host with that grant."""

    def __init__(
        self,
        endpoint: str | None = None,
        timeout: float = 35.0,
        transport: Callable[[str, bytes, float, dict[str, str]], tuple[int, bytes]] | None = None,
        core_endpoint: str | None = None,
        service_credential: str | None = None,
        core_transport: Callable[[str, bytes, float, dict[str, str]], tuple[int, bytes]] | None = None,
    ):
        self.endpoint = (endpoint or os.getenv("EXECUTION_HOST_URL", "http://127.0.0.1:8031")).rstrip("/")
        self.core_endpoint = (core_endpoint or os.getenv("ROOM_HOP_CORE_AUTHORITY_URL", "")).rstrip("/")
        self.service_credential = service_credential or os.getenv("ROOM_HOP_EXECUTION_SERVICE_CREDENTIAL", "")
        self.timeout = timeout
        self.transport = transport or self._http_transport
        self.core_transport = core_transport or self._http_transport

    @staticmethod
    def _http_transport(url: str, body: bytes, timeout: float, headers: dict[str, str]) -> tuple[int, bytes]:
        req = request.Request(url, data=body, headers=headers, method="POST")
        with request.urlopen(req, timeout=timeout) as response:
            return response.status, response.read(1024 * 1024 + 1)

    @staticmethod
    def _to_dict(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return dict(value)
        if hasattr(value, "as_dict"):
            return value.as_dict()
        if is_dataclass(value):
            return asdict(value)
        raise TypeError("request_must_be_mapping_or_dataclass")

    @staticmethod
    def _blocked(work_id: str | None, blocker: str, execution_id: str | None = None) -> BridgeResult:
        return BridgeResult(execution_id, work_id, "BLOCKED", blocker=blocker, cleanup={"process_reaped": False})

    def invoke(self, work_context: Any, execution_request: Any) -> BridgeResult:
        try:
            context = self._to_dict(work_context)
            run = self._to_dict(execution_request)
        except TypeError as exc:
            return self._blocked(None, str(exc))

        work_id = context.get("work_id")
        if not isinstance(work_id, str) or not _WORK_ID.fullmatch(work_id):
            return self._blocked(work_id if isinstance(work_id, str) else None, "canonical_work_id_required")
        if not self.core_endpoint or not self.service_credential:
            return self._blocked(work_id, "core_service_identity_not_configured")

        command = run.get("command")
        timeout_seconds = run.get("timeout_seconds", 30.0)
        if not isinstance(command, (list, tuple)) or not command:
            return self._blocked(work_id, "pytest_command_required")
        if timeout_seconds != 30 and timeout_seconds != 30.0:
            return self._blocked(work_id, "w12_runtime_only_supports_30s_single_pytest_call")
        if run.get("run_test", False) or run.get("collect_artifacts", ()):
            return self._blocked(work_id, "w12_runtime_only_supports_single_pytest_call")
        executable = str(command[0]).replace("\\\\", "/").rsplit("/", 1)[-1].lower()
        is_pytest = executable == "pytest" or (
            executable in {"python", "python3", "python.exe", "python3.exe"}
            and len(command) >= 3 and list(command[1:3]) == ["-m", "pytest"]
        )
        if not is_pytest:
            return self._blocked(work_id, "pytest_grant_requires_pytest_command")

        grant_body = json.dumps(
            {"purpose": "pytest_run", "max_timeout_seconds": 30},
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            grant_code, grant_raw = self.core_transport(
                f"{self.core_endpoint}/works/{work_id}/execution-grants",
                grant_body,
                self.timeout,
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "X-ROOM-HOP-SERVICE-CREDENTIAL": self.service_credential,
                },
            )
            grant = json.loads(grant_raw.decode("utf-8"))
            if grant_code < 200 or grant_code >= 300 or not isinstance(grant, dict):
                return self._blocked(work_id, "core_execution_grant_denied")
        except (TimeoutError, error.URLError, OSError):
            return self._blocked(work_id, "core_authority_unreachable")
        except (ValueError, UnicodeError):
            return self._blocked(work_id, "invalid_core_grant_response")

        grant_id = grant.get("grant_id")
        grant_token = grant.get("grant_token")
        if (
            not isinstance(grant_id, str) or not grant_id
            or not isinstance(grant_token, str) or not grant_token
            or grant.get("work_id") != work_id
            or grant.get("purpose") != "pytest_run"
        ):
            return self._blocked(work_id, "core_grant_binding_invalid")

        host_body = json.dumps(
            {
                "work_id": work_id,
                "grant_id": grant_id,
                "purpose": "pytest_run",
                "execution_request": {
                    "command": list(command),
                    "timeout_seconds": 30.0,
                    "collect_artifacts": [],
                    "run_test": False,
                },
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        try:
            code, payload = self.transport(
                self.endpoint + "/execute",
                host_body,
                self.timeout,
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "Bearer " + grant_token,
                },
            )
            data = json.loads(payload.decode("utf-8"))
            if not isinstance(data, dict):
                return self._blocked(work_id, "invalid_execution_host_response")
            result = data.get("result") if isinstance(data.get("result"), dict) else data
            status = result.get("status", "BLOCKED")
            if code < 200 or code >= 300:
                status = "BLOCKED"
            return BridgeResult(
                result.get("execution_id"),
                result.get("work_id", work_id),
                status,
                result.get("evidence_ref"),
                result.get("exit_code"),
                result.get("stdout") or result.get("stdout_ref"),
                result.get("stderr") or result.get("stderr_ref"),
                result.get("artifacts") or [],
                result.get("blocker") or (None if 200 <= code < 300 else "execution_host_http_" + str(code)),
                result.get("cleanup") or {},
                result.get("provider_type", "HTTP_EXECUTION_HOST"),
                result.get("runtime_instance_id"),
                result.get("runtime_build_hash"),
                result.get("runtime_started_at"),
                result.get("runtime_pid"),
                result.get("runtime_platform"),
                result.get("runtime_bind_address"),
                data,
            )
        except (TimeoutError, error.URLError, OSError):
            return self._blocked(work_id, "execution_host_unreachable")
        except (ValueError, UnicodeError):
            return self._blocked(work_id, "invalid_execution_host_json")


def execute_work(
    work_context: Any,
    execution_request: Any,
    *,
    endpoint: str | None = None,
    timeout: float = 35.0,
    transport=None,
    core_endpoint: str | None = None,
    service_credential: str | None = None,
    core_transport=None,
) -> BridgeResult:
    return ExecutionHostBridge(
        endpoint=endpoint,
        timeout=timeout,
        transport=transport,
        core_endpoint=core_endpoint,
        service_credential=service_credential,
        core_transport=core_transport,
    ).invoke(work_context, execution_request)
