"""Core-owned, fail-closed Work execution authority.

Credentials are configured as SHA-256 digests; raw service credentials are
never persisted. Grants are Work/purpose scoped, short-lived and represented
in an append-only hash-chained JSONL journal. The grant token is returned once
at issuance and is never stored or logged in clear text.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_WORK_ID = re.compile(r"^W[0-9]+$")
_ALLOWED_RUN_STATES = {"PASS", "FAILED", "BLOCKED", "TIMEOUT", "DENIED", "CANCELLED"}


class ExecutionAuthorityConfigError(RuntimeError):
    pass


class ExecutionAuthorityStoreError(RuntimeError):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _canonical(value: dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class AppendOnlyExecutionStore:
    """Append-only, fsynced JSONL event store with a verifiable hash chain.

    A lock file serializes writers across processes. A stale lock fails closed;
    it is never silently removed because doing so could permit concurrent writes.
    """

    def __init__(self, path: str | Path, *, lock_wait_seconds: float = 2.0) -> None:
        self.path = Path(path).expanduser().resolve()
        self.lock_path = self.path.with_name(self.path.name + ".lock")
        self.lock_wait_seconds = lock_wait_seconds
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read_verified(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        events: list[dict[str, Any]] = []
        previous = "0" * 64
        try:
            with self.path.open("r", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    event = json.loads(line)
                    supplied = event.pop("record_sha256", None)
                    if event.get("previous_sha256") != previous or not isinstance(supplied, str):
                        raise ExecutionAuthorityStoreError("execution_store_chain_invalid")
                    calculated = hashlib.sha256(_canonical(event)).hexdigest()
                    if not hmac.compare_digest(supplied, calculated):
                        raise ExecutionAuthorityStoreError("execution_store_chain_invalid")
                    event["record_sha256"] = supplied
                    previous = supplied
                    events.append(event)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ExecutionAuthorityStoreError("execution_store_unreadable") from exc
        return events

    def read_events(self) -> list[dict[str, Any]]:
        return self._read_verified()

    def append(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        lock_fd: int | None = None
        deadline = time.monotonic() + self.lock_wait_seconds
        while lock_fd is None:
            try:
                lock_fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.write(lock_fd, str(os.getpid()).encode("ascii"))
                os.fsync(lock_fd)
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise ExecutionAuthorityStoreError("execution_store_busy_or_stale_lock")
                time.sleep(0.025)
        try:
            events = self._read_verified()
            previous = events[-1]["record_sha256"] if events else "0" * 64
            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "recorded_at": _iso(_utcnow()),
                "previous_sha256": previous,
                **payload,
            }
            digest = hashlib.sha256(_canonical(event)).hexdigest()
            record = {**event, "record_sha256": digest}
            encoded = _canonical(record) + b"\n"
            fd = os.open(self.path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600)
            try:
                written = os.write(fd, encoded)
                if written != len(encoded):
                    raise ExecutionAuthorityStoreError("execution_store_short_write")
                os.fsync(fd)
            finally:
                os.close(fd)
            return record
        finally:
            if lock_fd is not None:
                os.close(lock_fd)
            try:
                os.unlink(self.lock_path)
            except FileNotFoundError:
                pass


class ExecutionAuthority:
    """Core's sole authority for service identity and Work-scoped grants."""

    def __init__(
        self,
        *,
        identity_credential_sha256: dict[str, str],
        work_policies: dict[str, dict[str, Any]],
        store_path: str | Path,
        default_grant_seconds: int = 300,
        max_grant_seconds: int = 900,
    ) -> None:
        if not identity_credential_sha256 or not work_policies:
            raise ExecutionAuthorityConfigError("execution_authority_registry_empty")
        self._credential_digests: dict[str, str] = {}
        for identity, digest in identity_credential_sha256.items():
            if not isinstance(identity, str) or not identity.strip() or not isinstance(digest, str) or not _SHA256.fullmatch(digest):
                raise ExecutionAuthorityConfigError("invalid_identity_credential_registry")
            self._credential_digests[identity] = digest.lower()
        self._work_policies: dict[str, dict[str, Any]] = {}
        for work_id, policy in work_policies.items():
            if not isinstance(work_id, str) or not _WORK_ID.fullmatch(work_id) or not isinstance(policy, dict):
                raise ExecutionAuthorityConfigError("invalid_work_policy_registry")
            allowed = policy.get("allowed_identities")
            if not isinstance(allowed, list) or not allowed or any(x not in self._credential_digests for x in allowed):
                raise ExecutionAuthorityConfigError("invalid_work_identity_binding")
            required = ("work_name", "workspace_root", "execution_workspace", "evidence_root", "source_sha256")
            if any(not isinstance(policy.get(k), str) or not policy[k].strip() for k in required):
                raise ExecutionAuthorityConfigError("incomplete_work_execution_binding")
            root = Path(policy["workspace_root"]).resolve()
            for key in ("execution_workspace", "evidence_root"):
                child = Path(policy[key]).resolve()
                try:
                    child.relative_to(root)
                except ValueError as exc:
                    raise ExecutionAuthorityConfigError("work_path_outside_root") from exc
            if not isinstance(policy.get("source_sha256"), str) or not _SHA256.fullmatch(policy["source_sha256"]):
                raise ExecutionAuthorityConfigError("invalid_work_source_sha256")
            purposes = policy.get("allowed_purposes", ["pytest_run"])
            if not isinstance(purposes, list) or not purposes or any(not isinstance(x, str) or not x.strip() for x in purposes):
                raise ExecutionAuthorityConfigError("invalid_allowed_purposes")
            self._work_policies[work_id] = {**policy, "allowed_purposes": list(purposes)}
        if not (1 <= default_grant_seconds <= max_grant_seconds <= 900):
            raise ExecutionAuthorityConfigError("invalid_grant_lifetime_policy")
        self.default_grant_seconds = default_grant_seconds
        self.max_grant_seconds = max_grant_seconds
        self.store = AppendOnlyExecutionStore(store_path)

    @classmethod
    def from_env(cls) -> "ExecutionAuthority":
        identities_raw = os.getenv("ROOM_HOP_EXECUTION_IDENTITIES_JSON")
        works_raw = os.getenv("ROOM_HOP_EXECUTION_WORKS_JSON")
        store_path = os.getenv("ROOM_HOP_EXECUTION_STORE_PATH")
        if not identities_raw or not works_raw or not store_path:
            raise ExecutionAuthorityConfigError("execution_authority_not_configured")
        try:
            identities = json.loads(identities_raw)
            works = json.loads(works_raw)
        except json.JSONDecodeError as exc:
            raise ExecutionAuthorityConfigError("execution_authority_config_invalid_json") from exc
        return cls(identity_credential_sha256=identities, work_policies=works, store_path=store_path)

    def authenticate(self, credential: Any) -> str:
        if not isinstance(credential, str) or len(credential) < 24:
            raise PermissionError("caller_authentication_failed")
        candidate = hashlib.sha256(credential.encode("utf-8")).hexdigest()
        matched: str | None = None
        for identity, expected in self._credential_digests.items():
            if hmac.compare_digest(candidate, expected):
                matched = identity
        if matched is None:
            raise PermissionError("caller_authentication_failed")
        return matched

    def is_identity_allowed_for_work(self, identity: str, work_id: str) -> bool:
        policy = self._work_policies.get(work_id)
        return bool(policy and identity in policy["allowed_identities"])

    def issue_grant(
        self, identity: str, work_id: str, purpose: str, grant_seconds: int | None = None,
        *, max_timeout_seconds: int = 60,
    ) -> dict[str, Any]:
        policy = self._work_policies.get(work_id)
        if policy is None:
            raise KeyError("unknown_work")
        if not self.is_identity_allowed_for_work(identity, work_id):
            raise PermissionError("caller_not_authorized_for_work")
        if not isinstance(purpose, str) or purpose not in policy["allowed_purposes"]:
            raise PermissionError("execution_purpose_not_allowed")
        lifetime = self.default_grant_seconds if grant_seconds is None else grant_seconds
        if not isinstance(lifetime, int) or isinstance(lifetime, bool) or not (1 <= lifetime <= self.max_grant_seconds):
            raise ValueError("invalid_grant_lifetime")
        if not isinstance(max_timeout_seconds, int) or isinstance(max_timeout_seconds, bool) or not (1 <= max_timeout_seconds <= 3600):
            raise ValueError("invalid_max_timeout_seconds")
        token = secrets.token_urlsafe(32)
        grant_id = "GRANT-" + uuid.uuid4().hex
        issued = _utcnow()
        expires = issued + timedelta(seconds=lifetime)
        self.store.append("GRANT_ISSUED", {
            "grant_id": grant_id,
            "work_id": work_id,
            "identity": identity,
            "purpose": purpose,
            "max_timeout_seconds": max_timeout_seconds,
            "issued_at": _iso(issued),
            "expires_at": _iso(expires),
            "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
            "status": "active",
        })
        return {
            "grant_id": grant_id,
            "grant_token": token,
            "execution_token_ref": grant_id,
            "work_id": work_id,
            "work_name": policy["work_name"],
            "workspace_root": policy["workspace_root"],
            "execution_workspace": policy["execution_workspace"],
            "evidence_root": policy["evidence_root"],
            "source_sha256": policy["source_sha256"],
            "purpose": purpose,
            "max_timeout_seconds": max_timeout_seconds,
            "expires_at": _iso(expires),
            "authorized": True,
        }

    def _grant_events(self, grant_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        events = self.store.read_events()
        grant_events = [e for e in events if e.get("grant_id") == grant_id]
        issued = next((e for e in grant_events if e.get("event_type") == "GRANT_ISSUED"), None)
        if issued is None:
            raise KeyError("unknown_grant")
        return issued, grant_events

    def validate_grant_token(self, grant_id: str, token: str) -> dict[str, Any]:
        if not isinstance(token, str) or not token:
            raise PermissionError("execution_grant_invalid")
        issued, events = self._grant_events(grant_id)
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        if not hmac.compare_digest(digest, issued["token_sha256"]):
            raise PermissionError("execution_grant_invalid")
        if any(e.get("event_type") == "GRANT_REVOKED" for e in events):
            raise PermissionError("execution_grant_revoked")
        if _utcnow() >= datetime.fromisoformat(issued["expires_at"]):
            raise PermissionError("execution_grant_expired")
        return {
            "grant_id": grant_id,
            "work_id": issued["work_id"],
            "identity": issued["identity"],
            "purpose": issued["purpose"],
            "max_timeout_seconds": issued.get("max_timeout_seconds", 60),
            "issued_at": issued["issued_at"],
            "expires_at": issued["expires_at"],
            "status": "active",
            **{k: self._work_policies[issued["work_id"]][k] for k in (
                "work_name", "workspace_root", "execution_workspace", "evidence_root", "source_sha256"
            )},
        }

    def get_grant_status(self, grant_id: str) -> dict[str, Any]:
        issued, events = self._grant_events(grant_id)
        if any(e.get("event_type") == "GRANT_REVOKED" for e in events):
            status = "revoked"
        elif _utcnow() >= datetime.fromisoformat(issued["expires_at"]):
            status = "expired"
        else:
            status = "active"
        return {
            "grant_id": grant_id,
            "work_id": issued["work_id"],
            "identity": issued["identity"],
            "purpose": issued["purpose"],
            "issued_at": issued["issued_at"],
            "expires_at": issued["expires_at"],
            "status": status,
        }

    def revoke_grant(self, grant_id: str) -> dict[str, Any]:
        status = self.get_grant_status(grant_id)
        if status["status"] != "active":
            raise PermissionError("execution_grant_not_active")
        self.store.append("GRANT_REVOKED", {"grant_id": grant_id, "work_id": status["work_id"]})
        return {"grant_id": grant_id, "status": "revoked"}

    def record_run(
        self, grant_id: str, *, grant_token: str, source_sha256: str, exit_status: str,
        output_refs: list[str], evidence_refs: list[str], handoff_ids: list[str],
    ) -> dict[str, Any]:
        # Revalidate the bearer grant immediately before the append side effect.
        self.validate_grant_token(grant_id, grant_token)
        issued, _ = self._grant_events(grant_id)
        if not isinstance(source_sha256, str) or not _SHA256.fullmatch(source_sha256):
            raise ValueError("invalid_source_sha256")
        if exit_status not in _ALLOWED_RUN_STATES:
            raise ValueError("invalid_exit_status")
        for name, values in (("output_refs", output_refs), ("evidence_refs", evidence_refs), ("handoff_ids", handoff_ids)):
            if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
                raise ValueError("invalid_" + name)
        return self.store.append("RUN_RECORDED", {
            "grant_id": grant_id,
            "work_id": issued["work_id"],
            "identity": issued["identity"],
            "source_sha256": source_sha256.lower(),
            "exit_status": exit_status,
            "output_refs": list(output_refs),
            "evidence_refs": list(evidence_refs),
            "handoff_ids": list(handoff_ids),
        })


__all__ = [
    "ExecutionAuthority", "ExecutionAuthorityConfigError",
    "ExecutionAuthorityStoreError", "AppendOnlyExecutionStore",
]
