from __future__ import annotations

import json
import os
from urllib import error, request
from urllib.parse import quote, urlsplit
from typing import Any

from execution_host.source_snapshot import workspace_source_sha256


class CoreGrantExecutionError(RuntimeError):
    pass


def _safe_endpoint(value: str, *, label: str) -> str:
    value = value.rstrip("/")
    parsed = urlsplit(value)
    loopback_http = parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise CoreGrantExecutionError(label + "_invalid_url")
    if parsed.scheme == "https" or loopback_http:
        return value
    raise CoreGrantExecutionError(label + "_must_use_https_or_loopback_http")


class CoreGrantExecutionHost:
    """WEE LifecycleController adapter: issue via Core, execute via Host."""

    def __init__(
        self,
        *,
        core_url: str | None = None,
        host_url: str | None = None,
        agent_id: str | None = None,
        agent_credential: str | None = None,
        timeout: float = 10.0,
        execution_timeout: float = 3630.0,
        transport=None,
    ):
        self.core_url = _safe_endpoint(
            core_url or os.getenv("ROOM_HOP_CORE_AUTHORITY_URL", ""),
            label="core_authority_url",
        )
        self.host_url = _safe_endpoint(
            host_url or os.getenv("EXECUTION_HOST_URL", "http://127.0.0.1:8031"),
            label="execution_host_url",
        )
        self.agent_id = agent_id or os.getenv("ROOM_HOP_EXECUTION_AGENT_ID", "")
        self.agent_credential = (
            agent_credential or os.getenv("ROOM_HOP_EXECUTION_AGENT_CREDENTIAL", "")
        )
        self.timeout = timeout
        self.execution_timeout = execution_timeout
        self.transport = transport or self._http_transport
        if not self.agent_id or not self.agent_credential:
            raise CoreGrantExecutionError("execution_agent_identity_not_configured")

    @staticmethod
    def _http_transport(url: str, method: str, body: bytes | None, headers: dict, timeout: float):
        req = request.Request(url, data=body, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=timeout) as response:
                return response.status, response.read()
        except error.HTTPError as exc:
            return exc.code, exc.read()
        except (error.URLError, TimeoutError, OSError):
            raise CoreGrantExecutionError("execution_authority_or_host_unreachable") from None

    def _request(
        self,
        base_url: str,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        service_id: str | None = None,
        credential: str | None = None,
        request_timeout: float | None = None,
    ) -> dict[str, Any]:
        headers = {"Accept": "application/json"}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        if service_id is not None:
            headers["X-ROOM-HOP-SERVICE-ID"] = service_id
            headers["X-ROOM-HOP-SERVICE-CREDENTIAL"] = credential or ""
        body = (
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
            if payload is not None else None
        )
        status, raw = self.transport(
            base_url + path, method, body, headers, request_timeout or self.timeout
        )
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeError, json.JSONDecodeError):
            raise CoreGrantExecutionError("invalid_authority_or_host_response") from None
        if not isinstance(data, dict):
            raise CoreGrantExecutionError("invalid_authority_or_host_response")
        if status < 200 or status >= 300:
            detail = data.get("detail") or data.get("reason") or "execution_request_failed"
            raise CoreGrantExecutionError(str(detail))
        return data

    def discover(self, context) -> dict[str, Any]:
        report = self._request(self.host_url, "GET", "/health")
        if report.get("status") != "PASS":
            raise CoreGrantExecutionError("execution_host_not_ready")
        return {
            "status": "PASS",
            "provider_type": report.get("provider_type"),
            "authority": report.get("authority"),
            "grant_cache": report.get("grant_cache"),
            "work_id": context.work_id,
            "execution_id": context.execution_id,
        }

    def execute_authorized(self, context) -> dict[str, Any]:
        required = (
            "assignment_id", "task_id", "environment_id",
            "host_identity_id", "test_entrypoint",
        )
        missing = [
            key for key in required
            if not getattr(context, key, None)
        ]
        if missing:
            raise CoreGrantExecutionError(
                "canonical_work_context_missing:" + ",".join(missing)
            )
        source_sha = workspace_source_sha256(context.execution_workspace)
        issue_payload = {
            "purpose": "pytest_run",
            "repository": context.repository,
            "branch": context.branch,
            "expected_head": context.expected_head,
            "assignment_id": context.assignment_id,
            "task_id": context.task_id,
            "host_identity_id": context.host_identity_id,
            "source_sha256": source_sha,
            "environment_id": context.environment_id,
            "test_entrypoint": list(context.test_entrypoint),
        }
        requested_timeout = getattr(context, "requested_timeout_seconds", None)
        if requested_timeout is not None:
            issue_payload["requested_timeout_seconds"] = requested_timeout

        work_path = quote(str(context.work_id), safe="")
        grant = self._request(
            self.core_url,
            "POST",
            f"/works/{work_path}/execution-grants",
            payload=issue_payload,
            service_id=self.agent_id,
            credential=self.agent_credential,
        )
        grant_id = grant.get("grant_id")
        grant_token = grant.get("grant_token")
        if not grant_id or not grant_token:
            raise CoreGrantExecutionError("core_grant_response_incomplete")

        result: dict[str, Any] | None = None
        execution_error: Exception | None = None
        revocation_error: str | None = None
        try:
            result = self._request(
                self.host_url,
                "POST",
                "/execute-granted",
                payload={
                    "work_id": str(context.work_id),
                    "grant_id": grant_id,
                    "grant_token": grant_token,
                },
                request_timeout=max(
                    self.execution_timeout,
                    int(getattr(context, "requested_timeout_seconds", None) or 0) + 30,
                ),
            )
            if result.get("work_id") != str(context.work_id):
                raise CoreGrantExecutionError("execution_host_work_binding_mismatch")
            if result.get("run_record_persisted") is not True:
                raise CoreGrantExecutionError("execution_run_record_not_persisted")
        except Exception as exc:
            execution_error = exc
        finally:
            try:
                revoked = self._request(
                    self.core_url,
                    "POST",
                    f"/works/{work_path}/execution-grants/{quote(str(grant_id), safe='')}/revoke",
                    service_id=self.agent_id,
                    credential=self.agent_credential,
                )
                if revoked.get("status") != "revoked":
                    raise CoreGrantExecutionError("grant_revocation_not_confirmed")
            except Exception as revoke_exc:
                revocation_error = str(revoke_exc) or type(revoke_exc).__name__

        if execution_error is not None or revocation_error is not None:
            blockers = []
            if execution_error is not None:
                blockers.append(str(execution_error))
            if revocation_error is not None:
                blockers.append("grant_revocation_failed:" + revocation_error)
            return {
                "status": "BLOCKED",
                "work_id": str(context.work_id),
                "execution_id": context.execution_id,
                "grant_id": grant_id,
                "run_record_persisted": bool(
                    result and result.get("run_record_persisted")
                ),
                "grant_revocation_confirmed": revocation_error is None,
                "blocker": ";".join(blockers),
            }
        return {
            **(result or {}),
            "grant_id": grant_id,
            "grant_revocation_confirmed": True,
            "grant_revoked_after_run": True,
        }
