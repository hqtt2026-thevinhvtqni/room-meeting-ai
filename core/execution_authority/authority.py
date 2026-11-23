"""Execution authority service: enrolled identities, Work-scoped grants.

Contract V1.2: DR-1 (Core-enrolled service identity, port-agnostic),
DR-2 (separate short-lived grant token, server-side validation, token value
never stored or logged), INV-2/INV-5 (grants bound and checkable, fail-closed
on every error branch). Credentials are injected per deployment; only their
SHA-256 digests are kept in memory, and grant records store the token hash,
never the token value.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
import time
import uuid
from pathlib import Path
from typing import Any

GRANT_ACTIVE = "active"
GRANT_EXPIRED = "expired"
GRANT_REVOKED = "revoked"

EXIT_STATUSES = ("PASS", "FAIL", "TIMEOUT", "BLOCKED")
CAPABILITY_OPERATIONS = {"RUN_SCRIPT", "RUN_TESTS"}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def validate_execution_capability(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {
        "entry_path", "operation", "expected_source_sha256", "timeout_seconds"
    }:
        raise ValueError("capability_fields_invalid")
    entry = value["entry_path"]
    if not isinstance(entry, str) or not entry.strip():
        raise ValueError("capability_entry_path_invalid")
    entry = entry.replace(chr(92), "/")
    if entry.startswith("/") or ":" in entry or any(part in ("", ".", "..") for part in entry.split("/")):
        raise ValueError("capability_entry_path_invalid")
    operation = value["operation"]
    if not isinstance(operation, str) or operation not in CAPABILITY_OPERATIONS:
        raise ValueError("capability_operation_invalid")
    digest = value["expected_source_sha256"]
    if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
        raise ValueError("capability_source_sha256_invalid")
    timeout = value["timeout_seconds"]
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= 300:
        raise ValueError("capability_timeout_invalid")
    return {"entry_path": entry, "operation": operation,
            "expected_source_sha256": digest, "timeout_seconds": timeout}



class ExecutionAuthorityConfigError(RuntimeError):
    """Raised when the deployment configuration is missing or malformed."""


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_enrolled_identities(raw: str | None) -> dict[str, str]:
    """Parse name=credential pairs into name -> sha256(credential)."""
    if not isinstance(raw, str) or not raw.strip():
        raise ExecutionAuthorityConfigError("no enrolled service identities configured")
    identities: dict[str, str] = {}
    for item in raw.split(","):
        item = item.strip()
        if "=" not in item:
            raise ExecutionAuthorityConfigError("enrolled identity entry must be name=credential")
        name, credential = item.split("=", 1)
        if not name.strip() or not credential.strip():
            raise ExecutionAuthorityConfigError("enrolled identity name and credential must be non-empty")
        identities[name.strip()] = _sha256(credential)
    return identities


def load_works_registry(path: str | None) -> dict[str, dict[str, Any]]:
    """Load the Works registry JSON: work_id -> work fields + allowed_identities."""
    if not isinstance(path, str) or not path.strip():
        raise ExecutionAuthorityConfigError("no works registry file configured")
    try:
        raw = Path(path).read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, ValueError) as exc:
        raise ExecutionAuthorityConfigError("works registry unreadable: " + type(exc).__name__) from exc
    if not isinstance(data, dict) or not data:
        raise ExecutionAuthorityConfigError("works registry must be a non-empty mapping")
    works: dict[str, dict[str, Any]] = {}
    for work_id, entry in data.items():
        if not isinstance(work_id, str) or not re.fullmatch(r"W[0-9]+", work_id):
            raise ExecutionAuthorityConfigError("work ids must match W<number>")
        if not isinstance(entry, dict):
            raise ExecutionAuthorityConfigError("work entry must be a mapping")
        for key in ("work_name", "workspace_root", "execution_workspace", "evidence_root"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                raise ExecutionAuthorityConfigError("work entry missing or malformed: " + key)
        allowed = entry.get("allowed_identities")
        if not isinstance(allowed, list) or not allowed or not all(isinstance(n, str) and n.strip() for n in allowed):
            raise ExecutionAuthorityConfigError("allowed_identities must be non-empty strings")
        if "capability_required" in entry and not isinstance(entry["capability_required"], bool):
            raise ExecutionAuthorityConfigError("capability_required must be boolean")
        works[work_id] = entry
    return works


class ExecutionAuthority:
    """Fail-closed grant issuer and recorder over the append-only store."""

    def __init__(self, *, store: Any, enrolled_identities: dict[str, str], works: dict[str, dict[str, Any]], default_grant_seconds: int = 300) -> None:
        if not callable(getattr(store, "append", None)) or not callable(getattr(store, "get", None)):
            raise ExecutionAuthorityConfigError("store must provide append/get")
        if not isinstance(enrolled_identities, dict) or not enrolled_identities:
            raise ExecutionAuthorityConfigError("at least one enrolled service identity is required")
        if not isinstance(works, dict) or not works:
            raise ExecutionAuthorityConfigError("at least one authorized Work is required")
        if isinstance(default_grant_seconds, bool) or not isinstance(default_grant_seconds, int) or default_grant_seconds < 1:
            raise ExecutionAuthorityConfigError("default_grant_seconds must be a positive integer")
        self._store = store
        self._identities = dict(enrolled_identities)
        self._works = works
        self._default_grant_seconds = default_grant_seconds

    def authenticate(self, provided_credential: str | None) -> str:
        if not isinstance(provided_credential, str) or not provided_credential:
            raise PermissionError("caller_authentication_failed")
        provided_hash = _sha256(provided_credential)
        for name, digest in self._identities.items():
            if hmac.compare_digest(provided_hash, digest):
                return name
        raise PermissionError("caller_authentication_failed")

    def is_identity_allowed_for_work(self, service_identity: str | None, work_id: str | None) -> bool:
        """Public read-only authorization surface (contract V1.2, DR-1).

        True only when the authenticated service identity is enrolled in the
        work's allowed_identities. Read-only, no side effects, and no detail
        is disclosed on denial: callers get a bare False.
        """
        work = self._works.get(work_id)
        if not isinstance(work, dict):
            return False
        allowed = work.get("allowed_identities")
        if not isinstance(allowed, list):
            return False
        return isinstance(service_identity, str) and service_identity in allowed

    def _grant_state(self, grant: dict[str, Any]) -> str:
        for record in self._store.records("revoke"):
            if record.get("grant_id") == grant["record_id"]:
                return GRANT_REVOKED
        if float(grant.get("expires_at_unix", 0)) <= time.time():
            return GRANT_EXPIRED
        return GRANT_ACTIVE

    def issue_grant(self, service_identity: str, work_id: str, purpose: str, *, capability: dict[str, Any] | None = None, grant_seconds: int | None = None) -> dict[str, Any]:
        if work_id not in self._works:
            raise LookupError("unknown_work")
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("purpose must be a non-empty string")
        scope = validate_execution_capability(capability) if capability is not None else None
        if scope is None and self._works[work_id].get("capability_required", False):
            raise ValueError("capability_required")
        seconds = self._default_grant_seconds if grant_seconds is None else grant_seconds
        if isinstance(seconds, bool) or not isinstance(seconds, int) or seconds < 1:
            raise ValueError("grant_seconds must be a positive integer")
        for record in self._store.records("grant"):
            if (record.get("service_identity") == service_identity and record.get("work_id") == work_id
                    and self._grant_state(record) == GRANT_ACTIVE):
                raise FileExistsError("grant_already_active")
        work = self._works[work_id]
        token = secrets.token_urlsafe(32)
        grant_id = "GRANT-" + str(uuid.uuid4())
        grant = {
            "record_id": grant_id,
            "grant_id": grant_id,
            "record_type": "grant",
            "service_identity": service_identity,
            "work_id": work_id,
            "work_name": work["work_name"],
            "workspace_root": work["workspace_root"],
            "execution_workspace": work["execution_workspace"],
            "evidence_root": work["evidence_root"],
            "purpose": purpose,
            "capability": scope,
            "authorized": True,
            "created_at_unix": time.time(),
            "expires_at_unix": time.time() + seconds,
            "token_sha256": _sha256(token),
        }
        self._store.append(grant)
        public = dict(grant)
        public.pop("token_sha256")
        public["grant_token"] = token
        return public

    def grant_status(self, grant_id: str) -> dict[str, Any]:
        grant = self._store.get(grant_id)
        if grant is None or grant.get("record_type") != "grant":
            raise LookupError("unknown_grant")
        public = dict(grant)
        public.pop("token_sha256", None)
        public["status"] = self._grant_state(grant)
        return public

    def revoke_grant(self, grant_id: str) -> dict[str, Any]:
        grant = self._store.get(grant_id)
        if grant is None or grant.get("record_type") != "grant":
            raise LookupError("unknown_grant")
        self._store.append({"record_id": "REVOKE-" + str(uuid.uuid4()), "record_type": "revoke", "grant_id": grant_id, "revoked_at_unix": time.time()})
        return self.grant_status(grant_id)

    def validate_grant_token(self, grant_id: str, token: str) -> dict[str, Any]:
        """Server-side DR-2 validation: active grant AND matching token."""
        grant = self._store.get(grant_id)
        if grant is None or grant.get("record_type") != "grant":
            raise LookupError("unknown_grant")
        if self._grant_state(grant) != GRANT_ACTIVE:
            raise PermissionError("grant_not_active")
        if not isinstance(token, str) or not token or not hmac.compare_digest(_sha256(token), grant["token_sha256"]):
            raise PermissionError("grant_token_mismatch")
        public = dict(grant)
        public.pop("token_sha256", None)
        public["status"] = GRANT_ACTIVE
        return public

    def record_run(self, grant_id: str, *, source_sha256: str, exit_status: str, output_refs: list[str], evidence_refs: list[str], handoff_ids: list[str]) -> dict[str, Any]:
        grant = self._store.get(grant_id)
        if grant is None or grant.get("record_type") != "grant":
            raise LookupError("unknown_grant")
        if self._grant_state(grant) != GRANT_ACTIVE:
            raise PermissionError("grant_not_active")
        if not isinstance(source_sha256, str) or not _SHA256_RE.fullmatch(source_sha256):
            raise ValueError("source_sha256_invalid")
        expected = (grant.get("capability") or {}).get("expected_source_sha256")
        if expected is not None and (not isinstance(expected, str) or not hmac.compare_digest(source_sha256, expected)):
            raise PermissionError("source_sha256_grant_mismatch")
        if expected is None and self._works[grant["work_id"]].get("capability_required", False):
            raise PermissionError("grant_capability_missing")
        if exit_status not in EXIT_STATUSES:
            raise ValueError("exit_status must be one of " + ",".join(EXIT_STATUSES))
        if not isinstance(evidence_refs, list) or not evidence_refs:
            raise ValueError("evidence_refs must be a non-empty list")
        for refs in (output_refs, evidence_refs, handoff_ids):
            if not isinstance(refs, list) or not all(isinstance(r, str) and r.strip() for r in refs):
                raise ValueError("reference lists must contain non-empty strings")
        run = {
            "record_id": "RUN-" + str(uuid.uuid4()),
            "record_type": "run",
            "grant_id": grant_id,
            "work_id": grant["work_id"],
            "service_identity": grant["service_identity"],
            "source_sha256": source_sha256,
            "exit_status": exit_status,
            "output_refs": list(output_refs),
            "evidence_refs": list(evidence_refs),
            "handoff_ids": list(handoff_ids),
            "recorded_at_unix": time.time(),
        }
        self._store.append(run)
        return dict(run)
