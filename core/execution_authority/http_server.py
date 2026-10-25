"""Separate HTTP mount for the Core execution authority (DR-4).

Runs as its own process/port so fail-closed startup or shutdown of the
execution authority can never regress the LOCKED v0.1 meeting API, while
code ownership stays inside the Core package. Surface per contract V1.2:

* POST /works/{work_id}/execution-grants     issue a Work-scoped grant
* GET  /works/{work_id}/execution-grants/{grant_id}   grant status
* POST /works/{work_id}/execution-runs      record a run outcome

Service identity travels in the X-Room-Hop-Service-Identity header;
credential values are never printed or returned in any response.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from core.execution_authority.authority import (
    ExecutionAuthority,
    ExecutionAuthorityConfigError,
    load_enrolled_identities,
    load_works_registry,
)
from core.execution_authority.store import AppendOnlyRecordStore

SERVICE_IDENTITY_HEADER = "X-Room-Hop-Service-Identity"


class ExecutionAuthorityHandler(BaseHTTPRequestHandler):
    authority: ExecutionAuthority = None  # type: ignore[assignment]

    def _send(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code: int, error: str) -> None:
        self._send(code, {"status": "BLOCKED", "error": error})

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeError):
            raise ValueError("invalid_request_body")
        if not isinstance(data, dict):
            raise ValueError("invalid_request_body")
        return data

    def log_message(self, format: str, *args: Any) -> None:
        # Never log headers: the service identity credential is secret.
        return

    def do_GET(self) -> None:
        parts = [p for p in self.path.split("/") if p]
        if len(parts) != 4 or parts[0] != "works" or parts[2] != "execution-grants":
            self._error(404, "unknown_route")
            return
        work_id, grant_id = parts[1], parts[3]
        try:
            caller = self.authority.authenticate(self.headers.get(SERVICE_IDENTITY_HEADER))
            status = self.authority.grant_status(grant_id)
        except PermissionError as exc:
            self._error(401, str(exc))
            return
        except LookupError:
            self._error(404, "unknown_grant")
            return
        # Grant metadata is scoped to the service identity that owns it.
        if status.get("work_id") != work_id or status.get("service_identity") != caller:
            self._error(404, "unknown_grant")
            return
        self._send(200, {"status": "ok", "grant": status})

    def do_POST(self) -> None:
        parts = [p for p in self.path.split("/") if p]
        try:
            if len(parts) == 3 and parts[0] == "works" and parts[2] == "execution-grants":
                self._handle_grant(parts[1])
                return
            if len(parts) == 3 and parts[0] == "works" and parts[2] == "execution-runs":
                self._handle_run(parts[1])
                return
            self._error(404, "unknown_route")
        except ValueError as exc:
            self._error(400, str(exc))

    def _handle_grant(self, work_id: str) -> None:
        try:
            name = self.authority.authenticate(self.headers.get(SERVICE_IDENTITY_HEADER))
        except PermissionError as exc:
            self._error(401, str(exc))
            return
        work = self.authority._works.get(work_id)
        if work is None:
            self._error(404, "unknown_work")
            return
        if name not in work["allowed_identities"]:
            self._error(403, "caller_not_authorized_for_work")
            return
        try:
            body = self._read_json()
        except ValueError as exc:
            self._error(400, str(exc))
            return
        purpose = body.get("purpose")
        if not isinstance(purpose, str) or not purpose.strip():
            self._error(400, "purpose_required")
            return
        try:
            grant = self.authority.issue_grant(name, work_id, purpose)
        except FileExistsError:
            self._error(409, "grant_already_active")
            return
        self._send(200, {"status": "ok", "grant": grant})

    def _handle_run(self, work_id: str) -> None:
        try:
            caller = self.authority.authenticate(self.headers.get(SERVICE_IDENTITY_HEADER))
        except PermissionError as exc:
            self._error(401, str(exc))
            return
        try:
            body = self._read_json()
        except ValueError as exc:
            self._error(400, str(exc))
            return
        grant_id = body.get("grant_id")
        token = body.get("grant_token")
        if not isinstance(grant_id, str) or not grant_id.strip():
            self._error(400, "grant_id_required")
            return
        try:
            grant = self.authority.validate_grant_token(grant_id, token if isinstance(token, str) else "")
        except LookupError:
            self._error(404, "unknown_grant")
            return
        except PermissionError as exc:
            self._error(403, str(exc))
            return
        if grant.get("work_id") != work_id:
            self._error(404, "unknown_grant")
            return
        if grant.get("service_identity") != caller:
            self._error(403, "caller_not_authorized_for_grant")
            return
        try:
            run = self.authority.record_run(
                grant_id,
                source_sha256=body.get("source_sha256"),
                exit_status=body.get("exit_status"),
                output_refs=body.get("output_refs") or [],
                evidence_refs=body.get("evidence_refs") or [],
                handoff_ids=body.get("handoff_ids") or [],
            )
        except (PermissionError, ValueError) as exc:
            self._error(403, str(exc))
            return
        self._send(200, {"status": "ok", "run": run})


def serve(host: str, port: int, authority: ExecutionAuthority) -> ThreadingHTTPServer:
    handler = type("BoundExecutionAuthorityHandler", (ExecutionAuthorityHandler,), {"authority": authority})
    server = ThreadingHTTPServer((host, port), handler)
    server.serve_forever()
    return server


def load_authority_from_env() -> ExecutionAuthority:
    identities = load_enrolled_identities(os.environ.get("EXECUTION_AUTHORITY_ENROLLED_IDENTITIES"))
    works = load_works_registry(os.environ.get("EXECUTION_AUTHORITY_WORKS_FILE"))
    data_dir = os.environ.get("EXECUTION_AUTHORITY_DATA_DIR")
    if not isinstance(data_dir, str) or not data_dir.strip():
        raise ExecutionAuthorityConfigError("EXECUTION_AUTHORITY_DATA_DIR must be set")
    store = AppendOnlyRecordStore(data_dir)
    return ExecutionAuthority(store=store, enrolled_identities=identities, works=works)


def main() -> None:
    host = os.environ.get("EXECUTION_AUTHORITY_HOST", "127.0.0.1")
    port_raw = os.environ.get("EXECUTION_AUTHORITY_PORT", "8001")
    try:
        port = int(port_raw)
    except ValueError as exc:
        raise ExecutionAuthorityConfigError("EXECUTION_AUTHORITY_PORT must be an integer") from exc
    authority = load_authority_from_env()
    names = ",".join(sorted(authority._identities))
    works = ",".join(sorted(authority._works))
    print("execution-authority: armed; enrolled identities: " + names + "; works: " + works, flush=True)
    serve(host, port, authority)


if __name__ == "__main__":
    main()
