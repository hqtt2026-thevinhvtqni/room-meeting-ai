"""Sandbox-owned Work 118 task contract and fail-closed lifecycle registry.

This module is the first executable slice of Loop A. It intentionally does not
call GitHub, dispatch agents, or claim runtime identity verification. Callers
must supply identity_verified=True only after a trusted runtime verifier has
validated the principal. SQLite is the local Sandbox task/event store.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


class TaskValidationError(ValueError):
    """A Task record or transition payload violates the W118 contract."""


class TransitionDenied(PermissionError):
    """The requested transition is invalid or the actor lacks authority."""


class VersionConflict(RuntimeError):
    """The caller's expected Task version is stale."""


class IdempotencyConflict(RuntimeError):
    """An idempotency key was reused for a different operation."""


TASK_STATES = {
    "DRAFT", "READY", "ISSUE_LINKED", "ASSIGNED", "DISPATCHED", "ACKED",
    "STARTED", "IN_PROGRESS", "BLOCKED", "COMPLETED", "VERIFYING",
    "VERIFIED", "ACCEPTED", "CLOSED", "REJECTED", "CANCELLED", "EXPIRED",
}

ALLOWED_TRANSITIONS = {
    "DRAFT": {"READY", "CANCELLED"},
    "READY": {"ISSUE_LINKED", "CANCELLED"},
    "ISSUE_LINKED": {"ASSIGNED", "BLOCKED", "CANCELLED"},
    "ASSIGNED": {"DISPATCHED", "BLOCKED", "EXPIRED"},
    "DISPATCHED": {"ACKED", "BLOCKED", "EXPIRED"},
    "ACKED": {"STARTED", "BLOCKED", "EXPIRED"},
    "STARTED": {"IN_PROGRESS", "BLOCKED"},
    "IN_PROGRESS": {"COMPLETED", "BLOCKED"},
    "BLOCKED": {"ASSIGNED", "CANCELLED", "EXPIRED"},
    "COMPLETED": {"VERIFYING"},
    "VERIFYING": {"VERIFIED", "REJECTED", "BLOCKED"},
    "VERIFIED": {"ACCEPTED", "REJECTED"},
    "ACCEPTED": {"CLOSED"},
    "REJECTED": {"ASSIGNED", "CANCELLED"},
    "EXPIRED": {"ASSIGNED", "CANCELLED"},
    "CANCELLED": set(),
    "CLOSED": set(),
}

TARGET_ROLES = {
    "READY": {"owner"},
    "ISSUE_LINKED": {"orchestrator"},
    "ASSIGNED": {"orchestrator"},
    "DISPATCHED": {"orchestrator"},
    "ACKED": {"executor"},
    "STARTED": {"executor"},
    "IN_PROGRESS": {"executor"},
    "BLOCKED": {"executor", "orchestrator", "verifier"},
    "COMPLETED": {"executor"},
    "VERIFYING": {"orchestrator"},
    "VERIFIED": {"verifier"},
    "ACCEPTED": {"owner"},
    "CLOSED": {"orchestrator"},
    "REJECTED": {"verifier", "owner"},
    "CANCELLED": {"owner"},
    "EXPIRED": {"orchestrator"},
}

_REQUIRED_TASK_STRINGS = (
    "work_id", "wp_id", "task_id", "title", "objective", "owner_principal",
)
_REQUIRED_DETAILS = {
    "ISSUE_LINKED": ("issue_id", "issue_url"),
    "ASSIGNED": ("assignment_id", "assigned_agent_id", "assigned_principal"),
    "DISPATCHED": ("dispatch_id",),
    "ACKED": ("dispatch_id", "ack_event_id", "ack_nonce_ref"),
    "COMPLETED": ("result_ref",),
    "VERIFYING": ("result_ref",),
    "CLOSED": ("issue_sync_verified",),
}
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _non_empty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TaskValidationError(f"{field} must be a non-empty string")
    return value.strip()


def _timestamp(value: str) -> str:
    value = _non_empty(value, "occurred_at")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TaskValidationError("occurred_at must be ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise TaskValidationError("occurred_at must include a timezone")
    return value


def validate_task_record(task: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize the versioned Sandbox Task contract."""
    if not isinstance(task, Mapping):
        raise TaskValidationError("task must be an object")
    result = dict(task)
    version = result.get("schema_version", "1.0")
    if version != "1.0":
        raise TaskValidationError("unsupported task schema_version")
    result["schema_version"] = version

    for field in _REQUIRED_TASK_STRINGS:
        result[field] = _non_empty(result.get(field), field)
    if not _ID_RE.fullmatch(result["task_id"]):
        raise TaskValidationError("task_id contains unsupported characters")

    if result.get("priority") not in {"P0", "P1", "P2", "P3"}:
        raise TaskValidationError("priority must be P0, P1, P2 or P3")
    if result.get("risk_level") not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        raise TaskValidationError("risk_level must be LOW, MEDIUM, HIGH or CRITICAL")

    for field in ("scope_in", "scope_out", "required_capabilities", "dependencies"):
        value = result.get(field)
        if not isinstance(value, list) or not all(isinstance(x, str) and x.strip() for x in value):
            raise TaskValidationError(f"{field} must be a list of non-empty strings")
        result[field] = [x.strip() for x in value]

    criteria = result.get("acceptance_criteria")
    if not isinstance(criteria, list) or not criteria:
        raise TaskValidationError("acceptance_criteria must be a non-empty list")
    normalized_criteria = []
    seen = set()
    for item in criteria:
        if not isinstance(item, Mapping):
            raise TaskValidationError("each acceptance criterion must be an object")
        criterion = dict(item)
        criterion_id = _non_empty(criterion.get("id"), "acceptance_criteria.id")
        if criterion_id in seen:
            raise TaskValidationError("acceptance criterion IDs must be unique")
        seen.add(criterion_id)
        criterion["description"] = _non_empty(criterion.get("description"), "acceptance_criteria.description")
        criterion["verification_method"] = _non_empty(
            criterion.get("verification_method"), "acceptance_criteria.verification_method"
        )
        criterion["id"] = criterion_id
        normalized_criteria.append(criterion)
    result["acceptance_criteria"] = normalized_criteria

    if result.get("task_id") in result["dependencies"]:
        raise TaskValidationError("a Task cannot depend on itself")
    result["state"] = "DRAFT"
    result["version"] = 1
    return result


class TaskRegistry:
    """SQLite Task Registry with append-only events and optimistic concurrency."""

    def __init__(self, database: str | Path = ":memory:") -> None:
        self._db = sqlite3.connect(str(database), isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                work_id TEXT NOT NULL,
                state TEXT NOT NULL,
                version INTEGER NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task_events (
                event_id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL REFERENCES tasks(task_id),
                event_type TEXT NOT NULL,
                from_state TEXT,
                to_state TEXT NOT NULL,
                actor_principal TEXT NOT NULL,
                actor_role TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                idempotency_key TEXT NOT NULL UNIQUE,
                request_hash TEXT NOT NULL,
                evidence_refs_json TEXT NOT NULL,
                details_json TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_task_events_task_time
                ON task_events(task_id, occurred_at, event_id);
            """
        )

    def close(self) -> None:
        self._db.close()

    def __enter__(self) -> "TaskRegistry":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    @staticmethod
    def _require_verified_actor(actor_principal: str, actor_role: str, identity_verified: bool) -> None:
        _non_empty(actor_principal, "actor_principal")
        if actor_role not in {"owner", "orchestrator", "executor", "verifier"}:
            raise TransitionDenied("unknown actor_role")
        if identity_verified is not True:
            raise TransitionDenied("actor identity is not verified; fail closed")

    def create_task(
        self,
        task: Mapping[str, Any],
        *,
        actor_principal: str,
        actor_role: str,
        identity_verified: bool,
        event_id: str,
        occurred_at: str,
    ) -> dict[str, Any]:
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if actor_role != "owner":
            raise TransitionDenied("only an owner may create a Task")
        event_id = _non_empty(event_id, "event_id")
        occurred_at = _timestamp(occurred_at)
        normalized = validate_task_record(task)
        if normalized["owner_principal"] != actor_principal:
            raise TransitionDenied("creator must match owner_principal")
        payload_json = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
        request_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        idempotency_key = f"task.create:{normalized['task_id']}"
        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("Task create key reused with different content")
                self._db.execute("COMMIT")
                return self.get_task(normalized["task_id"])
            self._db.execute(
                "INSERT INTO tasks(task_id, work_id, state, version, payload_json, created_at, updated_at) "
                "VALUES (?, ?, 'DRAFT', 1, ?, ?, ?)",
                (normalized["task_id"], normalized["work_id"], payload_json, occurred_at, occurred_at),
            )
            self._db.execute(
                "INSERT INTO task_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id, normalized["task_id"], "task.created", None, "DRAFT",
                    actor_principal, actor_role, occurred_at, idempotency_key, request_hash, "[]", "{}",
                ),
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return self.get_task(normalized["task_id"])

    def get_task(self, task_id: str) -> dict[str, Any]:
        row = self._db.execute("SELECT payload_json FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
        if not row:
            raise KeyError(f"unknown task_id: {task_id}")
        return json.loads(row["payload_json"])

    def list_events(self, task_id: str) -> list[dict[str, Any]]:
        rows = self._db.execute(
            "SELECT * FROM task_events WHERE task_id = ? ORDER BY rowid", (task_id,)
        ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "task_id": row["task_id"],
                "event_type": row["event_type"],
                "from_state": row["from_state"],
                "to_state": row["to_state"],
                "actor_principal": row["actor_principal"],
                "actor_role": row["actor_role"],
                "occurred_at": row["occurred_at"],
                "idempotency_key": row["idempotency_key"],
                "evidence_refs": json.loads(row["evidence_refs_json"]),
                "details": json.loads(row["details_json"]),
            }
            for row in rows
        ]

    def transition_task(
        self,
        task_id: str,
        to_state: str,
        *,
        actor_principal: str,
        actor_role: str,
        identity_verified: bool,
        expected_version: int,
        event_id: str,
        idempotency_key: str,
        occurred_at: str,
        evidence_refs: Sequence[str] = (),
        details: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if to_state not in TASK_STATES:
            raise TaskValidationError(f"unknown Task state: {to_state}")
        event_id = _non_empty(event_id, "event_id")
        idempotency_key = _non_empty(idempotency_key, "idempotency_key")
        occurred_at = _timestamp(occurred_at)
        if not isinstance(expected_version, int) or expected_version < 1:
            raise TaskValidationError("expected_version must be a positive integer")
        if not isinstance(evidence_refs, (list, tuple)) or not all(
            isinstance(x, str) and x.strip() for x in evidence_refs
        ):
            raise TaskValidationError("evidence_refs must be a list of non-empty strings")
        details_dict = dict(details or {})
        if not isinstance(details_dict, dict):
            raise TaskValidationError("details must be an object")
        request_body = {
            "task_id": task_id, "to_state": to_state, "actor_principal": actor_principal,
            "actor_role": actor_role, "expected_version": expected_version,
            "evidence_refs": list(evidence_refs), "details": details_dict,
        }
        request_hash = hashlib.sha256(
            json.dumps(request_body, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("idempotency key reused with different transition")
                self._db.execute("COMMIT")
                return {"task": self.get_task(task_id), "replayed": True}

            row = self._db.execute(
                "SELECT state, version, payload_json FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if not row:
                raise KeyError(f"unknown task_id: {task_id}")
            current = json.loads(row["payload_json"])
            from_state = row["state"]
            if row["version"] != expected_version:
                raise VersionConflict(
                    f"expected Task version {expected_version}, current version is {row['version']}"
                )
            if to_state not in ALLOWED_TRANSITIONS.get(from_state, set()):
                raise TransitionDenied(f"transition {from_state} -> {to_state} is not allowed")
            if actor_role not in TARGET_ROLES.get(to_state, set()):
                raise TransitionDenied(f"role '{actor_role}' cannot transition Task to {to_state}")
            for field in _REQUIRED_DETAILS.get(to_state, ()):
                if field not in details_dict:
                    raise TaskValidationError(f"{to_state} requires details.{field}")
                if field == "issue_id":
                    if not isinstance(details_dict[field], int) or details_dict[field] < 1:
                        raise TaskValidationError("details.issue_id must be a positive integer")
                elif field == "issue_sync_verified":
                    if details_dict[field] is not True:
                        raise TaskValidationError("Issue close requires successful GitHub readback")
                else:
                    _non_empty(details_dict[field], f"details.{field}")

            if to_state in {"ACKED", "STARTED", "IN_PROGRESS", "COMPLETED"}:
                if actor_principal != current.get("assigned_principal"):
                    raise TransitionDenied("executor principal does not match active assignment")
            if to_state == "ACKED" and details_dict["dispatch_id"] != current.get("dispatch_id"):
                raise TransitionDenied("ACK dispatch_id does not match active dispatch")
            if to_state in {"VERIFIED", "ACCEPTED"} and not evidence_refs:
                raise TaskValidationError(f"{to_state} requires at least one evidence reference")
            if to_state in {"CANCELLED", "EXPIRED", "REJECTED", "BLOCKED"}:
                _non_empty(details_dict.get("reason"), f"{to_state}.reason")

            updated = dict(current)
            updated.update(details_dict)
            updated.update({
                "state": to_state,
                "version": row["version"] + 1,
                "updated_at": occurred_at,
            })
            updated["evidence_refs"] = list(dict.fromkeys(
                list(current.get("evidence_refs", [])) + list(evidence_refs)
            ))
            payload_json = json.dumps(updated, sort_keys=True, separators=(",", ":"))
            self._db.execute(
                "UPDATE tasks SET state = ?, version = ?, payload_json = ?, updated_at = ? WHERE task_id = ?",
                (to_state, row["version"] + 1, payload_json, occurred_at, task_id),
            )
            self._db.execute(
                "INSERT INTO task_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id, task_id, "task.state_changed", from_state, to_state,
                    actor_principal, actor_role, occurred_at, idempotency_key, request_hash,
                    json.dumps(list(evidence_refs), sort_keys=True),
                    json.dumps(details_dict, sort_keys=True),
                ),
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {"task": self.get_task(task_id), "replayed": False}
