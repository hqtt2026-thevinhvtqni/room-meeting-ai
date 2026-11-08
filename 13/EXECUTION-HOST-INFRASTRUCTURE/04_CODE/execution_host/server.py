from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from .identity import RuntimeIdentity
from .models import WorkContext, ExecutionRequest, new_execution_id
from .source_snapshot import SourceSnapshotError, workspace_source_sha256
from .w12_adapter import W12ExecutionAdapter


class CoreAuthorityError(RuntimeError):
    def __init__(self, status_code: int, reason: str):
        super().__init__(reason)
        self.status_code = status_code
        self.reason = reason


class CoreAuthorityClient:
    """Online Core grant validation; no local authorization fallback."""

    def __init__(self, base_url: str, timeout: float = 5.0):
        parsed = urlparse(base_url)
        if parsed.scheme != "https" and parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise CoreAuthorityError(503, "core_authority_transport_must_be_private_tls")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise CoreAuthorityError(503, "core_authority_url_invalid")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, token: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
        req = Request(
            self.base_url + path,
            data=data,
            headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            with urlopen(req, timeout=self.timeout) as response:
                raw = response.read(1024 * 1024 + 1)
                if len(raw) > 1024 * 1024:
                    raise CoreAuthorityError(502, "core_authority_response_too_large")
                result = json.loads(raw.decode("utf-8"))
                if not isinstance(result, dict):
                    raise CoreAuthorityError(502, "core_authority_response_invalid")
                return result
        except HTTPError as exc:
            status = exc.code if exc.code in {401, 403, 404, 409, 503} else 502
            raise CoreAuthorityError(status, "core_execution_grant_denied") from None
        except (URLError, TimeoutError, OSError, UnicodeError, json.JSONDecodeError):
            raise CoreAuthorityError(503, "core_authority_unreachable_or_invalid") from None

    def validate_grant(self, work_id: str, grant_id: str, token: str) -> dict:
        return self._request(
            "GET",
            f"/works/{quote(work_id, safe='')}/execution-grants/{quote(grant_id, safe='')}/validate",
            token,
        )

    def record_run(self, work_id: str, grant_id: str, token: str, payload: dict) -> dict:
        return self._request(
            "POST",
            f"/works/{quote(work_id, safe='')}/execution-grants/{quote(grant_id, safe='')}/runs",
            token,
            payload,
        )


def _is_pytest_command(command: list[str]) -> bool:
    if not command:
        return False
    executable = Path(command[0]).stem.lower()
    if executable == "pytest":
        return True
    return executable in {"python", "python3"} and len(command) >= 3 and command[1:3] == ["-m", "pytest"]


def _mark_evidence_blocked(result: dict, reason: str) -> None:
    evidence_ref = result.get("evidence_ref")
    if not isinstance(evidence_ref, str) or not evidence_ref:
        return
    try:
        path = Path(evidence_ref)
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["status"] = "BLOCKED"
        payload["blocker"] = reason
        payload["core_run_recorded"] = False
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, TypeError):
        pass


class Handler(BaseHTTPRequestHandler):
    host: W12ExecutionAdapter | None = None
    runtime_identity: RuntimeIdentity | None = None
    core: CoreAuthorityClient | None = None

    def _send(self, code: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/health":
            if self.host is None:
                self._send(503, {"status": "BLOCKED", "reason": "runtime_not_initialized"})
                return
            self._send(200, {
                "status": "PASS",
                "service": "execution-host",
                "provider": self.host.provider_type,
                "runtime_provider": "REAL",
                "runtime_enabled": True,
                "runtime_allow_processes": self.host.allow_processes,
                "authority_mode": "CORE_ONLINE_GRANT_REQUIRED",
                "core_authority_configured": self.core is not None,
                "runtime_identity": self.runtime_identity.as_dict(),
            })
            return
        self._send(404, {"status": "NOT_FOUND"})

    def do_POST(self) -> None:
        if self.path != "/execute":
            self._send(404, {"status": "NOT_FOUND"})
            return
        if self.host is None:
            self._send(503, {"status": "BLOCKED", "reason": "runtime_not_initialized"})
            return
        if self.core is None:
            self._send(503, {"status": "BLOCKED", "reason": "core_authority_not_configured"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1024 * 1024:
                self._send(413, {"status": "BLOCKED", "reason": "request_body_size_invalid"})
                return
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(body, dict) or set(body) != {"work_id", "grant_id", "purpose", "execution_request"}:
                self._send(400, {"status": "BLOCKED", "reason": "request_contract_invalid"})
                return
            work_id, grant_id, purpose = body["work_id"], body["grant_id"], body["purpose"]
            if not all(isinstance(x, str) and x.strip() for x in (work_id, grant_id, purpose)):
                self._send(400, {"status": "BLOCKED", "reason": "grant_request_fields_invalid"})
                return
            authorization = self.headers.get("Authorization", "")
            if not authorization.startswith("Bearer ") or not authorization[7:].strip():
                self._send(401, {"status": "BLOCKED", "reason": "execution_grant_required"})
                return
            token = authorization[7:].strip()

            # Core supplies the canonical Work paths and source binding.
            grant = self.core.validate_grant(work_id, grant_id, token)
            if grant.get("status") != "active" or grant.get("work_id") != work_id:
                self._send(403, {"status": "BLOCKED", "reason": "execution_grant_not_active_or_work_mismatch"})
                return
            if grant.get("purpose") != purpose or purpose != "pytest_run":
                self._send(403, {"status": "BLOCKED", "reason": "execution_grant_purpose_not_supported"})
                return

            request_data = body["execution_request"]
            if not isinstance(request_data, dict):
                self._send(400, {"status": "BLOCKED", "reason": "execution_request_invalid"})
                return
            execution_request = ExecutionRequest(**request_data)
            if execution_request.timeout_seconds != 30.0 or execution_request.run_test or execution_request.collect_artifacts:
                self._send(403, {"status": "BLOCKED", "reason": "w12_runtime_only_supports_30s_single_pytest_call"})
                return
            if not isinstance(grant.get("max_timeout_seconds"), int) or execution_request.timeout_seconds > grant["max_timeout_seconds"]:
                self._send(403, {"status": "BLOCKED", "reason": "execution_timeout_exceeds_grant"})
                return
            if not _is_pytest_command(list(execution_request.command or ())):
                self._send(403, {"status": "BLOCKED", "reason": "pytest_grant_requires_pytest_command"})
                return

            workspace = grant.get("execution_workspace")
            expected_source = grant.get("source_sha256")
            if not isinstance(workspace, str) or not isinstance(expected_source, str):
                self._send(503, {"status": "BLOCKED", "reason": "core_work_snapshot_binding_missing"})
                return
            actual_source = workspace_source_sha256(workspace)
            if actual_source != expected_source:
                self._send(409, {"status": "BLOCKED", "reason": "work_source_snapshot_mismatch"})
                return

            ctx = WorkContext(
                work_id=grant["work_id"],
                work_name=grant["work_name"],
                workspace_root=grant["workspace_root"],
                execution_workspace=grant["execution_workspace"],
                evidence_root=grant["evidence_root"],
                authorized=True,
                execution_id=new_execution_id(),
                runtime={"source_sha256": actual_source},
            )
            result = self.host.execute_work(ctx, execution_request).as_dict()
            run_record = {
                "source_sha256": actual_source,
                "exit_status": result.get("status", "BLOCKED"),
                "output_refs": [x for x in (result.get("stdout"), result.get("stderr")) if x],
                "evidence_refs": [result["evidence_ref"]] if result.get("evidence_ref") else [],
                "handoff_ids": [],
            }
            try:
                self.core.record_run(work_id, grant_id, token, run_record)
            except CoreAuthorityError:
                result["status"] = "BLOCKED"
                result["blocker"] = "core_run_record_failed"
                _mark_evidence_blocked(result, "core_run_record_failed")
            self._send(200, result)
        except CoreAuthorityError as exc:
            self._send(exc.status_code, {"status": "BLOCKED", "reason": exc.reason})
        except SourceSnapshotError as exc:
            self._send(409, {"status": "BLOCKED", "reason": str(exc)})
        except (KeyError, TypeError, ValueError, UnicodeError, json.JSONDecodeError):
            self._send(400, {"status": "BLOCKED", "reason": "request_or_work_context_invalid"})

    def log_message(self, *args) -> None:
        # Never log Authorization headers, credentials, or request bodies.
        pass


def serve(host: str | None = None, port: int | None = None) -> None:
    bind_host = host or os.getenv("ROOM_HOP_EXECUTION_HOST_BIND", "127.0.0.1")
    bind_port = port or int(os.getenv("ROOM_HOP_EXECUTION_HOST_PORT", "8031"))
    identity = RuntimeIdentity(bind_address=f"{bind_host}:{bind_port}")
    Handler.runtime_identity = identity
    Handler.host = W12ExecutionAdapter(allow_processes=True, runtime_identity=identity)
    core_url = os.getenv("ROOM_HOP_CORE_AUTHORITY_URL", "")
    try:
        Handler.core = CoreAuthorityClient(core_url) if core_url else None
    except CoreAuthorityError:
        Handler.core = None
    ThreadingHTTPServer((bind_host, bind_port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
