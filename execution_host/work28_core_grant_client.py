"""Work28 Core Execution Authority HTTP client.

The client resolves one grant per request, validates it online before side
effects, and records the final run through the Core authority. It never
downloads a local grant list or follows redirects with authority credentials.
"""
from __future__ import annotations

import ipaddress
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Protocol

from .work28_grant import ExecutionGrant, GrantError

CORE_AUTHORITY_URL_ENV = "ROOM_HOP_CORE_AUTHORITY_URL"
CORE_SERVICE_IDENTITY_ENV = "ROOM_HOP_CORE_SERVICE_IDENTITY"
CORE_SERVICE_CREDENTIAL_ENV = "ROOM_HOP_CORE_SERVICE_CREDENTIAL"
SERVICE_IDENTITY_HEADER = "X-Room-Hop-Service-Identity"
GRANT_TOKEN_HEADER = "X-Room-Hop-Execution-Grant"
_WORK_ID_RE = re.compile(r"^W[0-9]+$")
_GRANT_ID_RE = re.compile(r"^GRANT-[0-9a-fA-F-]{36}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class CoreGrantSource(Protocol):
    def fetch_grant(self, work_id: str, grant_id: str, grant_token: str) -> ExecutionGrant: ...
    def record_run(
        self, *, work_id: str, grant_id: str, grant_token: str,
        source_sha256: str, exit_status: str, output_refs: list[str],
        evidence_refs: list[str], handoff_ids: list[str],
    ) -> dict[str, Any]: ...


def validate_core_grant_url(url: str) -> str:
    """Require HTTPS remotely; allow plaintext HTTP only on loopback."""
    if not isinstance(url, str) or not url.strip():
        raise GrantError("core_authority_url_required")
    try:
        parsed = urllib.parse.urlsplit(url.strip())
        hostname = parsed.hostname
        parsed.port
    except ValueError as exc:
        raise GrantError("core_authority_url_invalid") from exc
    if (
        parsed.scheme not in ("https", "http") or not hostname
        or parsed.username is not None or parsed.password is not None
        or parsed.query or parsed.fragment
    ):
        raise GrantError("core_authority_url_invalid")
    if parsed.scheme == "http":
        host = hostname.rstrip(".").lower()
        loopback = host == "localhost"
        if not loopback:
            try:
                loopback = ipaddress.ip_address(host).is_loopback
            except ValueError:
                loopback = False
        if not loopback:
            raise GrantError("core_authority_https_required")
    return url.strip().rstrip("/")


class RejectRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect; never forward service or grant credentials."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class HttpCoreGrantSource:
    def __init__(
        self, base_url: str, service_identity: str, credential: str,
        timeout: float = 5.0,
    ):
        self.base_url = validate_core_grant_url(base_url)
        if not isinstance(service_identity, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", service_identity):
            raise GrantError("core_service_identity_invalid")
        if not isinstance(credential, str) or not credential.strip():
            raise GrantError("core_service_credential_required")
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
            raise GrantError("core_authority_timeout_invalid")
        self.service_identity = service_identity
        self.credential = credential
        self.timeout = float(timeout)

    def _request(
        self, method: str, path: str, *, body: dict[str, Any] | None = None,
        grant_token: str,
    ) -> dict[str, Any]:
        data = None if body is None else json.dumps(body, separators=(",", ":")).encode("utf-8")
        req = urllib.request.Request(self.base_url + path, data=data, method=method)
        req.add_header("Accept", "application/json")
        req.add_header(SERVICE_IDENTITY_HEADER, self.credential)
        req.add_header("X-Room-Hop-Service-Name", self.service_identity)
        req.add_header(GRANT_TOKEN_HEADER, grant_token)
        if data is not None:
            req.add_header("Content-Type", "application/json")
        opener = urllib.request.build_opener(RejectRedirectHandler())
        try:
            with opener.open(req, timeout=self.timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            try:
                detail = json.loads(exc.read().decode("utf-8")).get("error", "http_error")
            except Exception:
                detail = "http_error"
            if exc.code in (401, 403):
                raise GrantError("core_authority_denied:" + str(detail)) from None
            if exc.code == 404:
                raise GrantError("core_grant_not_found") from None
            if exc.code >= 500:
                raise GrantError("core_authority_unavailable") from None
            raise GrantError("core_authority_http_" + str(exc.code)) from None
        except (urllib.error.URLError, OSError, TimeoutError):
            raise GrantError("core_authority_unreachable") from None
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise GrantError("core_authority_invalid_json") from None
        if not isinstance(payload, dict) or payload.get("status") != "ok":
            raise GrantError("core_authority_invalid_response")
        return payload

    def fetch_grant(self, work_id: str, grant_id: str, grant_token: str) -> ExecutionGrant:
        if not isinstance(work_id, str) or not _WORK_ID_RE.fullmatch(work_id):
            raise GrantError("core_work_id_invalid")
        if not isinstance(grant_id, str) or not _GRANT_ID_RE.fullmatch(grant_id):
            raise GrantError("core_grant_id_invalid")
        if not isinstance(grant_token, str) or not grant_token:
            raise GrantError("core_grant_token_required")
        payload = self._request(
            "GET", "/works/" + work_id + "/execution-grants/" + grant_id,
            grant_token=grant_token,
        )
        raw = payload.get("grant")
        if not isinstance(raw, dict):
            raise GrantError("core_grant_payload_invalid")
        capability = raw.get("capability")
        if not isinstance(capability, dict) or set(capability) != {
            "entry_path", "operation", "expected_source_sha256", "timeout_seconds"
        }:
            raise GrantError("core_grant_capability_invalid")
        entry_path = capability.get("entry_path")
        operation = capability.get("operation")
        source_hash = capability.get("expected_source_sha256")
        timeout = capability.get("timeout_seconds")
        if (
            not isinstance(entry_path, str) or not entry_path
            or not isinstance(operation, str) or operation not in ("RUN_SCRIPT", "RUN_TESTS")
            or not isinstance(source_hash, str) or not _SHA256_RE.fullmatch(source_hash)
            or isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 300
        ):
            raise GrantError("core_grant_capability_invalid")
        if (
            raw.get("work_id") != work_id or raw.get("grant_id") != grant_id
            or raw.get("service_identity") != self.service_identity
            or raw.get("authorized") is not True or raw.get("status") != "active"
        ):
            raise GrantError("core_grant_binding_mismatch")
        roots = {}
        for key in ("work_name", "workspace_root", "execution_workspace", "evidence_root"):
            value = raw.get(key)
            if not isinstance(value, str) or not value.strip():
                raise GrantError("core_grant_context_missing:" + key)
            roots[key] = value
        expiry = raw.get("expires_at_unix")
        if isinstance(expiry, bool) or not isinstance(expiry, (int, float)):
            raise GrantError("core_grant_expiry_invalid")
        return ExecutionGrant(
            grant_id=grant_id,
            work_id=work_id,
            entry_path=entry_path,
            operation=operation,
            expected_source_sha256=source_hash,
            expires_at_unix=float(expiry),
            work_name=roots["work_name"],
            workspace_root=roots["workspace_root"],
            execution_workspace=roots["execution_workspace"],
            evidence_root=roots["evidence_root"],
            service_identity=self.service_identity,
            purpose=raw.get("purpose"),
            status="active",
        )

    def record_run(
        self, *, work_id: str, grant_id: str, grant_token: str,
        source_sha256: str, exit_status: str, output_refs: list[str],
        evidence_refs: list[str], handoff_ids: list[str],
    ) -> dict[str, Any]:
        if not isinstance(work_id, str) or not _WORK_ID_RE.fullmatch(work_id):
            raise GrantError("core_work_id_invalid")
        if not isinstance(grant_id, str) or not _GRANT_ID_RE.fullmatch(grant_id):
            raise GrantError("core_grant_id_invalid")
        payload = self._request(
            "POST", "/works/" + work_id + "/execution-runs",
            body={
                "grant_id": grant_id,
                "source_sha256": source_sha256,
                "exit_status": exit_status,
                "output_refs": list(output_refs or []),
                "evidence_refs": list(evidence_refs or []),
                "handoff_ids": list(handoff_ids or []),
            },
            grant_token=grant_token,
        )
        run = payload.get("run")
        if not isinstance(run, dict):
            raise GrantError("core_run_record_invalid")
        return run


def build_grant_source(environ=None) -> HttpCoreGrantSource:
    env = os.environ if environ is None else environ
    url = env.get(CORE_AUTHORITY_URL_ENV)
    identity = env.get(CORE_SERVICE_IDENTITY_ENV)
    credential = env.get(CORE_SERVICE_CREDENTIAL_ENV)
    if not url:
        raise GrantError("core_authority_url_required")
    if not identity:
        raise GrantError("core_service_identity_required")
    if not credential:
        raise GrantError("core_service_credential_required")
    return HttpCoreGrantSource(url, identity, credential)


__all__ = [
    "CORE_AUTHORITY_URL_ENV", "CORE_SERVICE_IDENTITY_ENV",
    "CORE_SERVICE_CREDENTIAL_ENV", "SERVICE_IDENTITY_HEADER",
    "GRANT_TOKEN_HEADER", "CoreGrantSource", "HttpCoreGrantSource",
    "RejectRedirectHandler", "build_grant_source", "validate_core_grant_url",
]
