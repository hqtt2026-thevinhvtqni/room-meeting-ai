from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator


class AuthorityError(RuntimeError):
    def __init__(self, code: str, status_code: int = 403):
        super().__init__(code)
        self.code = code
        self.status_code = status_code


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _canonical(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


@contextmanager
def _file_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            if handle.read(1) == b"":
                handle.seek(0)
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class ExecutionAuthority:
    """Core-owned grant authority with an append-only, hash-chained journal."""

    def __init__(
        self,
        *,
        identities: dict[str, dict[str, Any]],
        works: dict[str, dict[str, Any]],
        store_path: str | Path,
        agent_registry: Any = None,
        clock=_utcnow,
    ):
        self.identities = identities
        self.works = works
        self.store_path = Path(store_path).resolve()
        self.lock_path = self.store_path.with_suffix(self.store_path.suffix + ".lock")
        self.agent_registry = agent_registry
        self.clock = clock
        self._thread_lock = threading.RLock()
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        with self._locked():
            self._read_state()

    @classmethod
    def from_env(cls, *, agent_registry: Any = None) -> "ExecutionAuthority | None":
        raw_identities = os.getenv("ROOM_HOP_EXECUTION_IDENTITIES_JSON", "")
        raw_works = os.getenv("ROOM_HOP_EXECUTION_WORKS_JSON", "")
        store_path = os.getenv("ROOM_HOP_EXECUTION_STORE_PATH", "")
        if not raw_identities or not raw_works or not store_path:
            return None
        try:
            identities = json.loads(raw_identities)
            works = json.loads(raw_works)
        except (TypeError, json.JSONDecodeError):
            return None
        if not isinstance(identities, dict) or not isinstance(works, dict):
            return None
        return cls(
            identities=identities,
            works=works,
            store_path=store_path,
            agent_registry=agent_registry,
        )

    @contextmanager
    def _locked(self) -> Iterator[None]:
        with self._thread_lock:
            with _file_lock(self.lock_path):
                yield

    def _read_state(self) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
        grants: dict[str, dict[str, Any]] = {}
        runs: list[dict[str, Any]] = []
        previous = "0" * 64
        if not self.store_path.exists():
            return grants, runs
        try:
            with self.store_path.open("r", encoding="utf-8") as stream:
                for number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    event = json.loads(line)
                    supplied_hash = event.pop("event_hash", None)
                    supplied_previous = event.get("previous_hash")
                    if supplied_previous != previous:
                        raise AuthorityError("authority_journal_chain_invalid", 503)
                    expected = _sha256(previous.encode("ascii") + _canonical(event))
                    if not isinstance(supplied_hash, str) or not hmac.compare_digest(
                        supplied_hash, expected
                    ):
                        raise AuthorityError("authority_journal_hash_invalid", 503)
                    previous = supplied_hash
                    kind = event.get("event_type")
                    payload = event.get("payload")
                    if not isinstance(payload, dict):
                        raise AuthorityError("authority_journal_payload_invalid", 503)
                    if kind == "grant_issued":
                        if payload["grant_id"] in grants:
                            raise AuthorityError("authority_journal_duplicate_grant", 503)
                        grants[payload["grant_id"]] = dict(payload)
                    elif kind == "grant_revoked":
                        grant = grants.get(payload.get("grant_id"))
                        if grant is None:
                            raise AuthorityError("authority_journal_revoke_target_missing", 503)
                        grant["status"] = "revoked"
                        grant["revoked_at"] = payload["revoked_at"]
                        grant["revoked_by"] = payload["revoked_by"]
                    elif kind == "run_started":
                        runs.append({"start": dict(payload), "completion": None})
                    elif kind == "run_completed":
                        match = next((item for item in runs if item["start"].get("run_id") == payload.get("run_id")), None)
                        if match is None or match["completion"] is not None:
                            raise AuthorityError("authority_journal_run_transition_invalid", 503)
                        match["completion"] = dict(payload)
                    else:
                        raise AuthorityError("authority_journal_event_unknown", 503)
        except AuthorityError:
            raise
        except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError):
            raise AuthorityError("authority_journal_unreadable", 503) from None
        return grants, runs

    def _append(self, event_type: str, payload: dict[str, Any]) -> None:
        grants, runs = self._read_state()
        previous = "0" * 64
        if self.store_path.exists():
            with self.store_path.open("r", encoding="utf-8") as stream:
                for line in stream:
                    if line.strip():
                        previous = json.loads(line)["event_hash"]
        event = {
            "event_type": event_type,
            "occurred_at": _iso(self.clock()),
            "previous_hash": previous,
            "payload": payload,
        }
        event_hash = _sha256(previous.encode("ascii") + _canonical(event))
        stored = dict(event)
        stored["event_hash"] = event_hash
        with self.store_path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(stored, sort_keys=True, ensure_ascii=False) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def _identity(self, service_id: str, credential: str, *, kind: str) -> dict[str, Any]:
        if not service_id or not credential:
            raise AuthorityError("service_identity_required", 401)
        if not isinstance(credential, str) or len(credential) < 32:
            raise AuthorityError("service_credential_invalid", 401)
        record = self.identities.get(service_id)
        if not isinstance(record, dict) or record.get("kind") != kind:
            raise AuthorityError("service_identity_not_enrolled", 403)
        expected = record.get("credential_sha256", "")
        if (
            not isinstance(expected, str)
            or len(expected) != 64
            or any(ch not in "0123456789abcdef" for ch in expected)
        ):
            raise AuthorityError("service_credential_config_invalid", 503)
        actual = _sha256(credential.encode("utf-8"))
        if not hmac.compare_digest(expected, actual):
            raise AuthorityError("service_credential_invalid", 401)
        principal_id = record.get("principal_id")
        if kind == "agent":
            if not principal_id or self.agent_registry is None:
                raise AuthorityError("agent_principal_not_configured", 503)
            try:
                if not self.agent_registry.exists(principal_id):
                    raise AuthorityError("agent_principal_unresolved", 403)
            except AuthorityError:
                raise
            except Exception:
                raise AuthorityError("agent_registry_unavailable", 503) from None
        return {"service_id": service_id, "kind": kind, "principal_id": principal_id}

    def _work_policy(self, work_id: str) -> dict[str, Any]:
        policy = self.works.get(work_id)
        if not isinstance(policy, dict):
            raise AuthorityError("work_not_authorized", 403)
        required = (
            "work_name", "allowed_identities", "allowed_host_identities",
            "allowed_assignments", "allowed_tasks", "workspace_root",
            "execution_workspace", "evidence_root", "source_sha256",
            "environment_id", "test_entrypoint", "max_timeout_seconds",
        )
        if any(key not in policy for key in required):
            raise AuthorityError("work_policy_incomplete", 503)
        for key in ("allowed_identities", "allowed_host_identities", "allowed_assignments", "allowed_tasks"):
            if not isinstance(policy[key], list) or not policy[key] or not all(isinstance(item, str) and item for item in policy[key]):
                raise AuthorityError("work_policy_scope_invalid", 503)
        source_hash = policy["source_sha256"]
        if not isinstance(source_hash, str) or len(source_hash) != 64 or any(ch not in "0123456789abcdef" for ch in source_hash):
            raise AuthorityError("work_policy_source_hash_invalid", 503)
        if not isinstance(policy["environment_id"], str) or not policy["environment_id"]:
            raise AuthorityError("work_policy_environment_invalid", 503)
        try:
            root = Path(policy["workspace_root"]).resolve(strict=True)
            workspace = Path(policy["execution_workspace"]).resolve(strict=True)
            evidence = Path(policy["evidence_root"]).resolve()
            canonical_workspace = (root / "workspace").resolve()
            canonical_workspace.relative_to(root)
            workspace.relative_to(canonical_workspace)
            evidence.relative_to(root)
            try:
                evidence.relative_to(workspace)
            except ValueError:
                pass
            else:
                raise ValueError("evidence_root_inside_execution_workspace")
            if not root.is_dir() or not workspace.is_dir():
                raise ValueError("not_directory")
        except (OSError, ValueError, TypeError):
            raise AuthorityError("work_policy_paths_invalid", 503) from None
        command = policy["test_entrypoint"]
        if (
            not isinstance(command, list) or len(command) < 2
            or not all(isinstance(part, str) and part for part in command)
        ):
            raise AuthorityError("work_test_entrypoint_invalid", 503)
        executable = Path(command[0]).stem.lower()
        pytest_command = executable in {"pytest", "pytest.exe"} or (
            executable in {"python", "python3", "python.exe", "python3.exe"}
            and len(command) >= 3 and command[1:3] == ["-m", "pytest"]
        )
        if not pytest_command:
            raise AuthorityError("work_test_entrypoint_not_pytest", 503)
        if isinstance(policy["max_timeout_seconds"], bool) or not isinstance(policy["max_timeout_seconds"], int) or not (
            1 <= policy["max_timeout_seconds"] <= 3600
        ):
            raise AuthorityError("work_timeout_policy_invalid", 503)
        return policy

    def issue_grant(
        self,
        *,
        work_id: str,
        service_id: str,
        credential: str,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        actor = self._identity(service_id, credential, kind="agent")
        policy = self._work_policy(work_id)
        purpose = request.get("purpose")
        assignment_id = request.get("assignment_id")
        task_id = request.get("task_id")
        host_identity_id = request.get("host_identity_id")
        source_sha256 = request.get("source_sha256")
        environment_id = request.get("environment_id")
        timeout = request.get("requested_timeout_seconds")
        if timeout is None:
            timeout = policy["max_timeout_seconds"]
        if purpose != "pytest_run":
            raise AuthorityError("execution_purpose_not_allowed", 403)
        if service_id not in policy["allowed_identities"]:
            raise AuthorityError("agent_not_allowed_for_work", 403)
        if not assignment_id or assignment_id not in policy["allowed_assignments"]:
            raise AuthorityError("assignment_not_authorized", 403)
        if not task_id or task_id not in policy["allowed_tasks"]:
            raise AuthorityError("task_not_authorized", 403)
        if not host_identity_id or host_identity_id not in policy["allowed_host_identities"]:
            raise AuthorityError("execution_host_not_authorized", 403)
        if source_sha256 != policy["source_sha256"]:
            raise AuthorityError("source_revision_not_authorized", 409)
        if request.get("test_entrypoint") != policy["test_entrypoint"]:
            raise AuthorityError("test_entrypoint_not_authorized", 403)
        if environment_id != policy["environment_id"]:
            raise AuthorityError("execution_environment_not_authorized", 403)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout < 1 or timeout > policy["max_timeout_seconds"]:
            raise AuthorityError("execution_timeout_not_authorized", 403)

        token = secrets.token_urlsafe(32)
        now = self.clock()
        try:
            ttl = min(int(policy.get("grant_ttl_seconds", 300)), 900)
        except (TypeError, ValueError):
            raise AuthorityError("grant_ttl_policy_invalid", 503) from None
        if ttl < 1:
            raise AuthorityError("grant_ttl_policy_invalid", 503)
        grant_id = "eg_" + secrets.token_hex(16)
        grant = {
            "grant_id": grant_id,
            "token_sha256": _sha256(token.encode("utf-8")),
            "status": "active",
            "work_id": work_id,
            "work_name": policy["work_name"],
            "purpose": purpose,
            "issuer_service_id": service_id,
            "principal_id": actor["principal_id"],
            "host_identity_id": host_identity_id,
            "assignment_id": assignment_id,
            "task_id": task_id,
            "source_sha256": source_sha256,
            "environment_id": environment_id,
            "workspace_root": str(Path(policy["workspace_root"]).resolve()),
            "execution_workspace": str(Path(policy["execution_workspace"]).resolve()),
            "evidence_root": str(Path(policy["evidence_root"]).resolve()),
            "test_entrypoint": list(policy["test_entrypoint"]),
            "max_timeout_seconds": timeout,
            "policy_version": str(policy.get("policy_version", "1")),
            "issued_at": _iso(now),
            "expires_at": _iso(now + timedelta(seconds=ttl)),
        }
        with self._locked():
            self._append("grant_issued", grant)
        return {
            "grant_id": grant_id,
            "grant_token": token,
            "work_id": work_id,
            "principal_id": actor["principal_id"],
            "assignment_id": assignment_id,
            "task_id": task_id,
            "expires_at": grant["expires_at"],
            "policy_version": grant["policy_version"],
        }

    def _find_grant(self, work_id: str, grant_id: str) -> dict[str, Any]:
        grants, _ = self._read_state()
        grant = grants.get(grant_id)
        if grant is None or grant.get("work_id") != work_id:
            raise AuthorityError("grant_not_found", 404)
        if grant.get("status") != "active":
            raise AuthorityError("grant_not_active", 403)
        try:
            if self.clock() >= datetime.fromisoformat(grant["expires_at"]):
                raise AuthorityError("grant_expired", 403)
        except (KeyError, ValueError):
            raise AuthorityError("grant_record_invalid", 503) from None
        return grant

    def validate_grant(
        self,
        *,
        work_id: str,
        grant_id: str,
        token: str,
        host_service_id: str,
        host_credential: str,
    ) -> dict[str, Any]:
        host = self._identity(host_service_id, host_credential, kind="host")
        with self._locked():
            grant = self._find_grant(work_id, grant_id)
            actual = _sha256(token.encode("utf-8"))
            if not hmac.compare_digest(grant["token_sha256"], actual):
                raise AuthorityError("grant_token_invalid", 401)
            if grant["host_identity_id"] != host["service_id"]:
                raise AuthorityError("grant_host_binding_mismatch", 403)
            return {
                key: value for key, value in grant.items()
                if key != "token_sha256"
            }

    def revoke_grant(
        self,
        *,
        work_id: str,
        grant_id: str,
        service_id: str,
        credential: str,
    ) -> dict[str, Any]:
        actor = self._identity(service_id, credential, kind="agent")
        with self._locked():
            grant = self._find_grant(work_id, grant_id)
            if grant["issuer_service_id"] != service_id:
                raise AuthorityError("grant_revoke_not_permitted", 403)
            payload = {
                "grant_id": grant_id,
                "work_id": work_id,
                "revoked_by": actor["principal_id"],
                "revoked_at": _iso(self.clock()),
            }
            self._append("grant_revoked", payload)
        return {"grant_id": grant_id, "status": "revoked", "revoked_at": payload["revoked_at"]}

    def grant_status(
        self,
        *,
        work_id: str,
        grant_id: str,
        service_id: str,
        credential: str,
    ) -> dict[str, Any]:
        self._identity(service_id, credential, kind="agent")
        with self._locked():
            grants, _ = self._read_state()
            grant = grants.get(grant_id)
            if grant is None or grant.get("work_id") != work_id:
                raise AuthorityError("grant_not_found", 404)
            if grant["issuer_service_id"] != service_id:
                raise AuthorityError("grant_status_not_permitted", 403)
            state = grant.get("status", "invalid")
            if state == "active" and self.clock() >= datetime.fromisoformat(grant["expires_at"]):
                state = "expired"
            return {
                "grant_id": grant_id,
                "work_id": work_id,
                "status": state,
                "principal_id": grant["principal_id"],
                "host_identity_id": grant["host_identity_id"],
                "expires_at": grant["expires_at"],
            }

    def start_run(
        self,
        *,
        work_id: str,
        grant_id: str,
        token: str,
        host_service_id: str,
        host_credential: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        host = self._identity(host_service_id, host_credential, kind="host")
        with self._locked():
            grants, runs = self._read_state()
            grant = grants.get(grant_id)
            if grant is None or grant.get("work_id") != work_id:
                raise AuthorityError("grant_not_found", 404)
            if grant.get("status") != "active":
                raise AuthorityError("grant_not_active", 403)
            if self.clock() >= datetime.fromisoformat(grant["expires_at"]):
                raise AuthorityError("grant_expired", 403)
            actual = _sha256(token.encode("utf-8"))
            if not hmac.compare_digest(grant["token_sha256"], actual):
                raise AuthorityError("grant_token_invalid", 401)
            if grant["host_identity_id"] != host["service_id"]:
                raise AuthorityError("grant_host_binding_mismatch", 403)
            required = ("run_id", "command", "source_sha256", "environment_id", "started_at")
            if any(key not in record for key in required):
                raise AuthorityError("run_start_record_incomplete", 422)
            if record["source_sha256"] != grant["source_sha256"]:
                raise AuthorityError("run_source_binding_mismatch", 409)
            if record["environment_id"] != grant["environment_id"]:
                raise AuthorityError("run_environment_binding_mismatch", 409)
            if record["command"] != grant["test_entrypoint"]:
                raise AuthorityError("run_command_binding_mismatch", 409)
            if any(item["start"].get("run_id") == record["run_id"] for item in runs):
                raise AuthorityError("run_id_already_recorded", 409)
            if any(item["start"].get("grant_id") == grant_id for item in runs):
                raise AuthorityError("grant_already_used", 409)
            payload = {
                **record,
                "grant_id": grant_id,
                "work_id": work_id,
                "principal_id": grant["principal_id"],
                "issuer_service_id": grant["issuer_service_id"],
                "host_identity_id": host["service_id"],
                "assignment_id": grant["assignment_id"],
                "task_id": grant["task_id"],
                "purpose": grant["purpose"],
                "run_state": "STARTED",
                "recorded_at": _iso(self.clock()),
            }
            self._append("run_started", payload)
        return {"run_id": record["run_id"], "grant_id": grant_id, "status": "started"}

    def complete_run(
        self,
        *,
        work_id: str,
        grant_id: str,
        token: str,
        host_service_id: str,
        host_credential: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        host = self._identity(host_service_id, host_credential, kind="host")
        with self._locked():
            grants, runs = self._read_state()
            grant = grants.get(grant_id)
            if grant is None or grant.get("work_id") != work_id:
                raise AuthorityError("grant_not_found", 404)
            actual = _sha256(token.encode("utf-8"))
            if not hmac.compare_digest(grant["token_sha256"], actual):
                raise AuthorityError("grant_token_invalid", 401)
            if grant["host_identity_id"] != host["service_id"]:
                raise AuthorityError("grant_host_binding_mismatch", 403)
            required = (
                "run_id", "finished_at", "status", "exit_code",
                "evidence_sha256",
            )
            if any(key not in record for key in required):
                raise AuthorityError("run_completion_record_incomplete", 422)
            started = next(
                (item for item in runs if item["start"].get("run_id") == record["run_id"]),
                None,
            )
            if started is None or started["completion"] is not None:
                raise AuthorityError("run_start_not_found_or_already_completed", 409)
            start_record = started["start"]
            if start_record.get("grant_id") != grant_id or start_record.get("work_id") != work_id:
                raise AuthorityError("run_grant_binding_mismatch", 409)
            if (
                start_record.get("command") != grant["test_entrypoint"]
                or start_record.get("source_sha256") != grant["source_sha256"]
                or start_record.get("environment_id") != grant["environment_id"]
            ):
                raise AuthorityError("run_start_binding_invalid", 409)
            payload = {
                **record,
                "started_at": start_record["started_at"],
                "command": start_record["command"],
                "source_sha256": start_record["source_sha256"],
                "environment_id": start_record["environment_id"],
                "grant_id": grant_id,
                "work_id": work_id,
                "principal_id": grant["principal_id"],
                "issuer_service_id": grant["issuer_service_id"],
                "host_identity_id": host["service_id"],
                "assignment_id": grant["assignment_id"],
                "task_id": grant["task_id"],
                "purpose": grant["purpose"],
                "grant_status_at_completion": grant.get("status"),
                "run_state": "COMPLETED",
                "recorded_at": _iso(self.clock()),
            }
            self._append("run_completed", payload)
        return {"run_id": record["run_id"], "grant_id": grant_id, "status": "completed"}

    def record_run(self, **kwargs) -> dict[str, Any]:
        """Backward-compatible alias for completing an already-started Run Record."""
        return self.complete_run(**kwargs)
