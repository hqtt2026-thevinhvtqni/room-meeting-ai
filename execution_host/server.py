from __future__ import annotations

import hmac
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .host import ExecutionHost
from .identity import RuntimeIdentity
from .models import new_execution_id
from .work28_dispatch import DispatchError, dispatch_execute
from .work28_grant import ExecutionGrant, GrantError
from .work28_core_grant_client import (
    CORE_AUTHORITY_URL_ENV,
    GRANT_TOKEN_HEADER,
    CoreGrantSource,
    build_grant_source,
)
from .work28_readback import ReadbackError, load_sealed_result
from .work28_evidence import EvidenceError
from .work28_readiness import readiness_report
from .work28_bounds import MAX_SNAPSHOT_BYTES, MAX_OUTPUT_CHARS, MAX_GLOBAL_CONCURRENT

AUTH_HEADER = "X-Room-Hop-Execution-Auth"
AUTH_TOKEN_ENV = "ROOM_HOP_EXECUTION_AUTH_TOKEN"
# Retained as a deprecated constant for callers; it is never used as authority.
AUTHORIZED_WORKS_ENV = "ROOM_HOP_AUTHORIZED_WORKS"
WORK_ID_PATTERN = re.compile(r"W\d+")
MAX_REQUEST_BODY_BYTES = 262_144
EXECUTE_BODY_KEYS = frozenset({"work_id", "grant_id", "work28_request"})


def normalize_work_id(value):
    if not isinstance(value, str):
        raise ValueError("work_id must be a string")
    normalized = value.strip().upper()
    if not normalized or not WORK_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Work id must match the canonical W<number> format, e.g. W28;"
            " got: %r" % (value,)
        )
    return normalized


def authenticate_caller(provided, auth_token):
    if not isinstance(auth_token, str) or not auth_token:
        return False
    if not isinstance(provided, str) or not provided:
        return False
    return hmac.compare_digest(provided, auth_token)


def authorize_work(work_id, authorized_works):
    """Deprecated local allowlist helper; not used by the HTTP execution path."""
    if not isinstance(authorized_works, (set, frozenset)) or not authorized_works:
        return False
    try:
        normalized = normalize_work_id(work_id)
    except (TypeError, ValueError):
        return False
    return normalized in authorized_works


def load_execution_auth_config(environ=None):
    env = os.environ if environ is None else environ
    token = env.get(AUTH_TOKEN_ENV)
    if not isinstance(token, str) or not token.strip():
        raise RuntimeError(
            AUTH_TOKEN_ENV + " must be set to a non-empty execution transport token"
        )
    # Work authorization is derived from the live Core grant, never from a
    # deployment-local ROOM_HOP_AUTHORIZED_WORKS allowlist.
    return {"auth_token": token.strip()}


class Handler(BaseHTTPRequestHandler):
    host: ExecutionHost | None = None
    auth_token: str | None = None
    core_grant_source: CoreGrantSource | None = None
    evidence_root: str | None = None
    snapshot_only: bool = True
    # Deprecated test-compatibility attributes; never consulted for authority.
    authorized_works: frozenset | None = None
    grant_registry: dict | None = None

    def _send(self, code, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            if self.host is None:
                self._send(503, {"status": "BLOCKED", "reason": "runtime_not_initialized"})
                return
            ready = readiness_report(
                grant_count=0,
                evidence_root_configured=bool(Handler.evidence_root),
                snapshot_only=True,
                core_grant_url_set=bool(os.environ.get(CORE_AUTHORITY_URL_ENV)),
            )
            self._send(200, {
                "status": "PASS",
                "service": "execution-host",
                "provider": self.host.provider_type,
                **self.host.identity(),
                "snapshot_only": True,
                "grants_loaded": 0,
                "grant_authority": "CORE_ONLINE_PER_REQUEST",
                "evidence_root_configured": bool(Handler.evidence_root),
                "bounds": {
                    "max_snapshot_bytes": MAX_SNAPSHOT_BYTES,
                    "max_output_chars": MAX_OUTPUT_CHARS,
                    "max_global_concurrent": MAX_GLOBAL_CONCURRENT,
                },
                "readiness": ready,
            })
            return
        if self.path.startswith("/evidence/"):
            if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
                self._send(401, {"status": "BLOCKED", "reason": "caller_authentication_failed"})
                return
            if not Handler.evidence_root:
                self._send(503, {"status": "BLOCKED", "reason": "evidence_root_not_configured"})
                return
            exec_id = self.path[len("/evidence/"):].strip("/")
            try:
                payload = load_sealed_result(
                    evidence_root=Handler.evidence_root,
                    execution_id=exec_id,
                )
                self._send(200, payload)
            except ReadbackError as exc:
                code = 404 if "not_found" in str(exc) else 400
                self._send(code, {"status": "BLOCKED", "reason": type(exc).__name__ + ":" + str(exc)})
            except EvidenceError as exc:
                self._send(409, {"status": "BLOCKED", "reason": type(exc).__name__ + ":" + str(exc)})
            return
        self._send(404, {"status": "NOT_FOUND"})

    def do_POST(self):
        if self.path != "/execute":
            self._send(404, {"status": "NOT_FOUND"})
            return
        if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
            self._send(401, {"status": "BLOCKED", "reason": "caller_authentication_failed"})
            return
        try:
            if self.host is None:
                self._send(503, {"status": "BLOCKED", "reason": "runtime_not_initialized"})
                return
            source = Handler.core_grant_source
            if source is None:
                self._send(503, {"status": "BLOCKED", "reason": "core_grant_source_not_configured"})
                return
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if ctype != "application/json":
                self._send(415, {"status": "BLOCKED", "reason": "content_type_must_be_application_json"})
                return
            raw_len = int(self.headers.get("Content-Length", "0") or "0")
            if raw_len < 0 or raw_len > MAX_REQUEST_BODY_BYTES:
                self._send(413, {"status": "BLOCKED", "reason": "request_body_too_large"})
                return
            body = json.loads(self.rfile.read(raw_len))
            if not isinstance(body, dict):
                self._send(400, {"status": "BLOCKED", "reason": "body_must_be_object"})
                return
            unknown = set(body) - EXECUTE_BODY_KEYS
            if unknown:
                self._send(400, {"status": "BLOCKED", "reason": "unknown_body_keys:" + ",".join(sorted(unknown))})
                return
            if set(body) != EXECUTE_BODY_KEYS:
                self._send(400, {"status": "BLOCKED", "reason": "required_fields_missing"})
                return
            work_id = normalize_work_id(body.get("work_id"))
            grant_id = body.get("grant_id")
            grant_token = self.headers.get(GRANT_TOKEN_HEADER)
            work_request = body.get("work28_request")
            if not isinstance(grant_id, str) or not grant_id:
                self._send(400, {"status": "BLOCKED", "reason": "grant_id_required"})
                return
            if not isinstance(grant_token, str) or not grant_token:
                self._send(403, {"status": "BLOCKED", "reason": "core_grant_token_required"})
                return
            if not isinstance(work_request, dict):
                self._send(400, {"status": "BLOCKED", "reason": "work28_request_required"})
                return

            # Core validates service identity + grant token and returns the
            # authoritative Work roots and immutable execution capability.
            grant = source.fetch_grant(work_id, grant_id, grant_token)
            if not isinstance(grant, ExecutionGrant) or grant.work_id != work_id:
                raise GrantError("core_grant_binding_mismatch")
            if not all((grant.work_name, grant.workspace_root, grant.execution_workspace, grant.evidence_root)):
                raise GrantError("core_grant_context_missing")

            work_context = {
                "work_id": grant.work_id,
                "work_name": grant.work_name,
                "workspace_root": grant.workspace_root,
                "execution_workspace": grant.execution_workspace,
                "evidence_root": grant.evidence_root,
                "authorized": True,
                "execution_id": new_execution_id(),
            }
            dispatch_body = {
                "mode": "work28_snapshot",
                "execution_grant_id": grant.grant_id,
                "work28_request": work_request,
            }
            result = dispatch_execute(
                self.host,
                work_context=work_context,
                body=dispatch_body,
                grant_registry={grant.grant_id: grant},
                snapshot_only=True,
            )
            evidence_ref = result.get("evidence_ref")
            source_hash = result.get("source_sha256")
            if not isinstance(evidence_ref, str) or not evidence_ref or not isinstance(source_hash, str):
                self._send(503, {
                    "status": "BLOCKED",
                    "reason": "execution_result_missing_sealed_evidence",
                    "local_result": result,
                })
                return
            try:
                run_record = source.record_run(
                    work_id=work_id,
                    grant_id=grant_id,
                    grant_token=grant_token,
                    source_sha256=source_hash,
                    exit_status=result.get("status", "BLOCKED"),
                    output_refs=list(result.get("artifacts") or []),
                    evidence_refs=[evidence_ref],
                    handoff_ids=[],
                )
            except GrantError as exc:
                self._send(503, {
                    "status": "BLOCKED",
                    "reason": "core_run_record_failed:" + str(exc),
                    "evidence_ref": evidence_ref,
                })
                return
            result["core_run_record_id"] = run_record.get("record_id")
            result["core_authority_recorded"] = True
            self._send(200, result)
        except (DispatchError, GrantError) as exc:
            reason = str(exc)
            if reason.startswith(("core_authority_unreachable", "core_authority_unavailable")):
                code = 503
            elif reason.startswith(("core_authority_denied", "core_grant_not_found", "core_grant_binding_mismatch", "core_grant_token")):
                code = 403
            else:
                code = 400
            self._send(code, {"status": "BLOCKED", "reason": type(exc).__name__ + ":" + reason})
        except (TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
            self._send(400, {"status": "BLOCKED", "reason": type(exc).__name__ + ":" + str(exc)})
        except Exception as exc:
            self._send(503, {"status": "BLOCKED", "reason": type(exc).__name__ + ":" + str(exc)})

    def do_PUT(self):
        self._send(405, {"status": "BLOCKED", "reason": "method_not_allowed"})

    def do_DELETE(self):
        self._send(405, {"status": "BLOCKED", "reason": "method_not_allowed"})

    def do_PATCH(self):
        self._send(405, {"status": "BLOCKED", "reason": "method_not_allowed"})

    def log_message(self, *args):
        pass


def serve(
    host="127.0.0.1", port=8031, auth_token: str | None = None,
    core_grant_source: CoreGrantSource | None = None,
    evidence_root=None, snapshot_only=True,
    authorized_works=None, grant_registry=None,
):
    identity = RuntimeIdentity(bind_address=f"{host}:{port}")
    Handler.host = ExecutionHost(runtime_identity=identity)
    Handler.auth_token = auth_token
    Handler.core_grant_source = core_grant_source
    Handler.evidence_root = evidence_root
    Handler.snapshot_only = True
    # Legacy parameters are deliberately ignored for authorization.
    Handler.authorized_works = None
    Handler.grant_registry = {}
    ThreadingHTTPServer((host, port), Handler).serve_forever()


def main():
    config = load_execution_auth_config()
    # Build a client only; each execution must validate its exact grant online.
    source = build_grant_source()
    evidence_root = os.environ.get("ROOM_HOP_EVIDENCE_ROOT")
    print("execution-host: armed; Core online grant validation configured", flush=True)
    serve(
        "127.0.0.1", 8031, auth_token=config["auth_token"],
        core_grant_source=source, evidence_root=evidence_root, snapshot_only=True,
    )


if __name__ == "__main__":
    main()
