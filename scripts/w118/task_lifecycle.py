"""W118 Sandbox Task Register adapter with separate Task and Assignment lifecycles.

Task status follows the Work-level status vocabulary (PLANNED/READY/
IN_PROGRESS/BLOCKED/IN_REVIEW/DONE/CANCELLED). Assignment status follows the
separate dispatch/ACK/execution contract. GitHub Issue/source/CI observations
are append-only evidence and never imply Task acceptance.

The SQLite implementation is an operational transaction store for the Sandbox
adapter. The canonical W118 Task Register remains a Work-owned Sandbox record;
this module must be wired to that record by the runtime service before it is
treated as production authority.
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


TASK_STATUSES = {"PLANNED", "READY", "IN_PROGRESS", "BLOCKED", "IN_REVIEW", "DONE", "CANCELLED"}
TASK_TRANSITIONS = {
    "PLANNED": {"READY", "CANCELLED"},
    "READY": {"IN_PROGRESS", "BLOCKED", "CANCELLED"},
    "IN_PROGRESS": {"IN_REVIEW", "BLOCKED", "CANCELLED"},
    "BLOCKED": {"READY", "IN_PROGRESS", "CANCELLED"},
    "IN_REVIEW": {"DONE", "BLOCKED", "IN_PROGRESS"},
    "DONE": set(),
    "CANCELLED": set(),
}
TASK_TARGET_ROLES = {
    "READY": {"owner", "orchestrator"},
    "IN_PROGRESS": {"orchestrator"},
    "BLOCKED": {"owner", "orchestrator", "verifier", "executor"},
    "IN_REVIEW": {"orchestrator"},
    "DONE": {"owner"},
    "CANCELLED": {"owner", "orchestrator"},
}

ASSIGNMENT_STATUSES = {
    "UNASSIGNED", "PROPOSED", "DISPATCHED", "ACKNOWLEDGED", "IN_PROGRESS",
    "SUBMITTED", "ACCEPTED", "REJECTED", "BLOCKED", "CANCELLED",
}
ASSIGNMENT_TRANSITIONS = {
    "UNASSIGNED": {"PROPOSED"},
    "PROPOSED": {"DISPATCHED", "CANCELLED"},
    "DISPATCHED": {"ACKNOWLEDGED", "BLOCKED", "CANCELLED"},
    "ACKNOWLEDGED": {"IN_PROGRESS", "BLOCKED", "CANCELLED"},
    "IN_PROGRESS": {"SUBMITTED", "BLOCKED", "CANCELLED"},
    "SUBMITTED": {"ACCEPTED", "REJECTED", "BLOCKED"},
    "BLOCKED": {"PROPOSED", "DISPATCHED", "CANCELLED"},
    "REJECTED": {"PROPOSED", "CANCELLED"},
    "ACCEPTED": set(),
    "CANCELLED": set(),
}
ASSIGNMENT_TARGET_ROLES = {
    "PROPOSED": {"orchestrator"},
    "DISPATCHED": {"orchestrator"},
    "ACKNOWLEDGED": {"executor"},
    "IN_PROGRESS": {"executor"},
    "SUBMITTED": {"executor"},
    "ACCEPTED": {"verifier"},
    "REJECTED": {"verifier"},
    "BLOCKED": {"executor", "orchestrator", "verifier"},
    "CANCELLED": {"owner", "orchestrator"},
}

_TASK_DETAILS = {
    "READY": set(),
    "IN_PROGRESS": set(),
    "BLOCKED": {"reason"},
    "IN_REVIEW": {"review_request_ref"},
    "DONE": set(),
    "CANCELLED": {"reason"},
}
_ASSIGNMENT_REQUIRED_DETAILS = {
    "PROPOSED": (
        "assignment_id", "assigned_agent_id", "assigned_principal",
        "assignment_policy_version", "capability_match", "assignment_evidence_ref",
    ),
    "DISPATCHED": ("dispatch_id", "dispatch_receipt_ref"),
    "ACKNOWLEDGED": ("dispatch_id", "ack_event_id", "ack_nonce_ref"),
    "SUBMITTED": ("result_ref",),
    "BLOCKED": ("reason",),
    "REJECTED": ("reason",),
    "CANCELLED": ("reason",),
}
_ASSIGNMENT_DETAILS = {
    "PROPOSED": set(_ASSIGNMENT_REQUIRED_DETAILS["PROPOSED"]),
    "DISPATCHED": set(_ASSIGNMENT_REQUIRED_DETAILS["DISPATCHED"]),
    "ACKNOWLEDGED": set(_ASSIGNMENT_REQUIRED_DETAILS["ACKNOWLEDGED"]),
    "IN_PROGRESS": set(),
    "SUBMITTED": set(_ASSIGNMENT_REQUIRED_DETAILS["SUBMITTED"]),
    "ACCEPTED": set(),
    "REJECTED": set(_ASSIGNMENT_REQUIRED_DETAILS["REJECTED"]),
    "BLOCKED": set(_ASSIGNMENT_REQUIRED_DETAILS["BLOCKED"]),
    "CANCELLED": set(_ASSIGNMENT_REQUIRED_DETAILS["CANCELLED"]),
}
_TASK_ID_RE = re.compile(r"^(W[0-9]{3,4})-TASK-[0-9]{3,6}$")


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
    """Validate and normalize the W118 Work-level Task Register record."""
    if not isinstance(task, Mapping):
        raise TaskValidationError("task must be an object")
    result = dict(task)
    if result.get("schema_version", "1.0") != "1.0":
        raise TaskValidationError("unsupported Task schema_version")
    result["schema_version"] = "1.0"
    for field in ("work_id", "wp_id", "task_id", "title", "objective", "owner_principal"):
        result[field] = _non_empty(result.get(field), field)
    task_match = _TASK_ID_RE.fullmatch(result["task_id"])
    if not task_match or task_match.group(1) != result["work_id"]:
        raise TaskValidationError("task_id must use W###-TASK-### and match work_id")
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
    normalized = []
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
        normalized.append(criterion)
    result["acceptance_criteria"] = normalized
    if result["task_id"] in result["dependencies"]:
        raise TaskValidationError("a Task cannot depend on itself")
    result["status"] = "PLANNED"
    result["assignment_status"] = "UNASSIGNED"
    result["version"] = 1
    result["evidence_refs"] = []
    return result


class TaskRegistry:
    """SQLite transaction store for the Sandbox-owned W118 Task Register."""

    def __init__(self, database: str | Path = ":memory:") -> None:
        self._db = sqlite3.connect(str(database), isolation_level=None)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.execute("PRAGMA journal_mode = WAL")
        self._db.execute("PRAGMA synchronous = FULL")
        self._db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                work_id TEXT NOT NULL,
                status TEXT NOT NULL,
                assignment_status TEXT NOT NULL,
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

    @staticmethod
    def _hash(payload: Mapping[str, Any]) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def create_task(
        self, task: Mapping[str, Any], *, actor_principal: str, actor_role: str,
        identity_verified: bool, event_id: str, occurred_at: str,
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
        request_hash = self._hash(normalized)
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
                "INSERT INTO tasks(task_id, work_id, status, assignment_status, version, payload_json, created_at, updated_at) "
                "VALUES (?, ?, 'PLANNED', 'UNASSIGNED', 1, ?, ?, ?)",
                (normalized["task_id"], normalized["work_id"], payload_json, occurred_at, occurred_at),
            )
            self._db.execute(
                "INSERT INTO task_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    event_id, normalized["task_id"], "task.created", None, "PLANNED",
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

    def _append_event(
        self, *, event_id: str, task_id: str, event_type: str,
        from_state: str | None, to_state: str, actor_principal: str, actor_role: str,
        occurred_at: str, idempotency_key: str, request_hash: str,
        evidence_refs: Sequence[str], details: Mapping[str, Any],
    ) -> None:
        self._db.execute(
            "INSERT INTO task_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event_id, task_id, event_type, from_state, to_state,
                actor_principal, actor_role, occurred_at, idempotency_key, request_hash,
                json.dumps(list(evidence_refs), sort_keys=True),
                json.dumps(dict(details), sort_keys=True),
            ),
        )

    def link_issue(
        self, task_id: str, issue_id: int, issue_url: str, *,
        actor_principal: str, actor_role: str, identity_verified: bool,
        expected_version: int, event_id: str, idempotency_key: str,
        occurred_at: str, evidence_refs: Sequence[str],
    ) -> dict[str, Any]:
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if actor_role != "orchestrator":
            raise TransitionDenied("only the orchestrator may link a GitHub Issue")
        if type(issue_id) is not int or issue_id < 1:
            raise TaskValidationError("issue_id must be a positive integer")
        issue_url = _non_empty(issue_url, "issue_url")
        if not issue_url.startswith("https://github.com/"):
            raise TaskValidationError("issue_url must be a GitHub HTTPS URL")
        event_id = _non_empty(event_id, "event_id")
        idempotency_key = _non_empty(idempotency_key, "idempotency_key")
        occurred_at = _timestamp(occurred_at)
        if not evidence_refs or not all(isinstance(x, str) and x.strip() for x in evidence_refs):
            raise TaskValidationError("Issue link requires readback evidence_refs")
        request = {"task_id": task_id, "issue_id": issue_id, "issue_url": issue_url,
                   "evidence_refs": list(evidence_refs)}
        request_hash = self._hash(request)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("Issue-link idempotency key reused with different content")
                self._db.execute("COMMIT")
                return {"task": self.get_task(task_id), "replayed": True}
            row = self._db.execute(
                "SELECT status, version, payload_json FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if not row:
                raise KeyError(f"unknown task_id: {task_id}")
            if row["version"] != expected_version:
                raise VersionConflict("stale Task version for Issue link")
            if row["status"] not in {"READY", "IN_PROGRESS"}:
                raise TransitionDenied("Task must be READY or IN_PROGRESS before Issue link")
            current = json.loads(row["payload_json"])
            if current.get("issue_id") not in (None, issue_id):
                raise TransitionDenied("Task is already linked to a different GitHub Issue")
            updated = dict(current)
            updated.update({"issue_id": issue_id, "issue_url": issue_url,
                            "version": row["version"] + 1, "updated_at": occurred_at})
            updated["evidence_refs"] = list(dict.fromkeys(current.get("evidence_refs", []) + list(evidence_refs)))
            self._db.execute(
                "UPDATE tasks SET version = ?, payload_json = ?, updated_at = ? WHERE task_id = ?",
                (row["version"] + 1, json.dumps(updated, sort_keys=True, separators=(",", ":")),
                 occurred_at, task_id),
            )
            self._append_event(
                event_id=event_id, task_id=task_id, event_type="github.issue_linked",
                from_state=row["status"], to_state=row["status"], actor_principal=actor_principal,
                actor_role=actor_role, occurred_at=occurred_at, idempotency_key=idempotency_key,
                request_hash=request_hash, evidence_refs=evidence_refs,
                details={"issue_id": issue_id, "issue_url": issue_url},
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {"task": self.get_task(task_id), "replayed": False}

    def transition_task(
        self, task_id: str, to_status: str, *,
        actor_principal: str, actor_role: str, identity_verified: bool,
        expected_version: int, event_id: str, idempotency_key: str,
        occurred_at: str, evidence_refs: Sequence[str] = (),
        details: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if to_status not in TASK_STATUSES:
            raise TaskValidationError(f"unknown Task status: {to_status}")
        event_id = _non_empty(event_id, "event_id")
        idempotency_key = _non_empty(idempotency_key, "idempotency_key")
        occurred_at = _timestamp(occurred_at)
        if type(expected_version) is not int or expected_version < 1:
            raise TaskValidationError("expected_version must be a positive integer")
        if not isinstance(evidence_refs, (list, tuple)) or not all(
            isinstance(x, str) and x.strip() for x in evidence_refs
        ):
            raise TaskValidationError("evidence_refs must be a list of non-empty strings")
        if details is None:
            details_dict = {}
        elif isinstance(details, Mapping):
            details_dict = dict(details)
        else:
            raise TaskValidationError("details must be an object")
        unknown = set(details_dict) - _TASK_DETAILS.get(to_status, set())
        if unknown:
            raise TaskValidationError("unsupported Task detail fields: " + ", ".join(sorted(unknown)))
        for field in _TASK_DETAILS.get(to_status, set()):
            if field not in details_dict:
                continue
            _non_empty(details_dict[field], f"details.{field}")
        request = {"task_id": task_id, "to_status": to_status, "actor_principal": actor_principal,
                   "actor_role": actor_role, "expected_version": expected_version,
                   "evidence_refs": list(evidence_refs), "details": details_dict}
        request_hash = self._hash(request)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("Task status idempotency key reused with different content")
                self._db.execute("COMMIT")
                return {"task": self.get_task(task_id), "replayed": True}
            row = self._db.execute(
                "SELECT status, assignment_status, version, payload_json FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
            if not row:
                raise KeyError(f"unknown task_id: {task_id}")
            if row["version"] != expected_version:
                raise VersionConflict(f"expected Task version {expected_version}, current is {row['version']}")
            from_status = row["status"]
            if to_status not in TASK_TRANSITIONS.get(from_status, set()):
                raise TransitionDenied(f"Task status transition {from_status} -> {to_status} is not allowed")
            if actor_role not in TASK_TARGET_ROLES.get(to_status, set()):
                raise TransitionDenied(f"role '{actor_role}' cannot transition Task to {to_status}")
            current_payload = json.loads(row["payload_json"])
            if actor_role == "owner" and actor_principal != current_payload.get("owner_principal"):
                raise TransitionDenied("owner principal does not match Task owner")
            if to_status == "IN_PROGRESS" and row["assignment_status"] not in {"ACKNOWLEDGED", "IN_PROGRESS"}:
                raise TransitionDenied("Task can enter IN_PROGRESS only after Assignment ACKNOWLEDGED")
            if to_status == "IN_REVIEW" and row["assignment_status"] != "SUBMITTED":
                raise TransitionDenied("Task can enter IN_REVIEW only after Assignment SUBMITTED")
            if to_status == "DONE":
                if actor_principal != json.loads(row["payload_json"]).get("owner_principal"):
                    raise TransitionDenied("DONE requires the Task owner principal")
                if row["assignment_status"] != "ACCEPTED":
                    raise TransitionDenied("Task DONE requires Assignment ACCEPTED")
                if not evidence_refs:
                    raise TaskValidationError("Task DONE requires acceptance evidence")
            if to_status in {"BLOCKED", "CANCELLED"} and not details_dict.get("reason"):
                raise TaskValidationError(f"Task {to_status} requires details.reason")
            current = json.loads(row["payload_json"])
            updated = dict(current)
            updated.update(details_dict)
            updated.update({"status": to_status, "version": row["version"] + 1, "updated_at": occurred_at})
            updated["evidence_refs"] = list(dict.fromkeys(current.get("evidence_refs", []) + list(evidence_refs)))
            self._db.execute(
                "UPDATE tasks SET status = ?, version = ?, payload_json = ?, updated_at = ? WHERE task_id = ?",
                (to_status, row["version"] + 1, json.dumps(updated, sort_keys=True, separators=(",", ":")),
                 occurred_at, task_id),
            )
            self._append_event(
                event_id=event_id, task_id=task_id, event_type="task.status_changed",
                from_state=from_status, to_state=to_status, actor_principal=actor_principal,
                actor_role=actor_role, occurred_at=occurred_at, idempotency_key=idempotency_key,
                request_hash=request_hash, evidence_refs=evidence_refs, details=details_dict,
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {"task": self.get_task(task_id), "replayed": False}

    def transition_assignment(
        self, task_id: str, to_status: str, *,
        actor_principal: str, actor_role: str, identity_verified: bool,
        expected_version: int, event_id: str, idempotency_key: str,
        occurred_at: str, evidence_refs: Sequence[str] = (),
        details: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if to_status not in ASSIGNMENT_STATUSES:
            raise TaskValidationError(f"unknown Assignment status: {to_status}")
        event_id = _non_empty(event_id, "event_id")
        idempotency_key = _non_empty(idempotency_key, "idempotency_key")
        occurred_at = _timestamp(occurred_at)
        if type(expected_version) is not int or expected_version < 1:
            raise TaskValidationError("expected_version must be a positive integer")
        if not isinstance(evidence_refs, (list, tuple)) or not all(
            isinstance(x, str) and x.strip() for x in evidence_refs
        ):
            raise TaskValidationError("evidence_refs must be a list of non-empty strings")
        if details is None:
            details_dict = {}
        elif isinstance(details, Mapping):
            details_dict = dict(details)
        else:
            raise TaskValidationError("details must be an object")
        unknown = set(details_dict) - _ASSIGNMENT_DETAILS.get(to_status, set())
        if unknown:
            raise TaskValidationError("unsupported Assignment detail fields: " + ", ".join(sorted(unknown)))
        for field in _ASSIGNMENT_REQUIRED_DETAILS.get(to_status, ()):
            if field not in details_dict:
                raise TaskValidationError(f"Assignment {to_status} requires details.{field}")
            if field == "capability_match":
                values = details_dict[field]
                if not isinstance(values, list) or not values or not all(
                    isinstance(x, str) and x.strip() for x in values
                ):
                    raise TaskValidationError("capability_match must be a non-empty string list")
            else:
                _non_empty(details_dict[field], f"details.{field}")
        request = {"task_id": task_id, "to_status": to_status, "actor_principal": actor_principal,
                   "actor_role": actor_role, "expected_version": expected_version,
                   "evidence_refs": list(evidence_refs), "details": details_dict}
        request_hash = self._hash(request)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("Assignment idempotency key reused with different content")
                self._db.execute("COMMIT")
                return {"task": self.get_task(task_id), "replayed": True}
            row = self._db.execute(
                "SELECT status, assignment_status, version, payload_json FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
            if not row:
                raise KeyError(f"unknown task_id: {task_id}")
            if row["version"] != expected_version:
                raise VersionConflict(f"expected Task version {expected_version}, current is {row['version']}")
            from_status = row["assignment_status"]
            if to_status not in ASSIGNMENT_TRANSITIONS.get(from_status, set()):
                raise TransitionDenied(
                    f"Assignment status transition {from_status} -> {to_status} is not allowed"
                )
            if actor_role not in ASSIGNMENT_TARGET_ROLES.get(to_status, set()):
                raise TransitionDenied(f"role '{actor_role}' cannot transition Assignment to {to_status}")
            current = json.loads(row["payload_json"])
            if actor_role == "owner" and actor_principal != current.get("owner_principal"):
                raise TransitionDenied("owner principal does not match Task owner")
            if actor_role == "executor" and to_status in {
                "ACKNOWLEDGED", "IN_PROGRESS", "SUBMITTED", "BLOCKED"
            }:
                if actor_principal != current.get("assigned_principal"):
                    raise TransitionDenied("executor principal does not match active Assignment")
            if to_status == "ACKNOWLEDGED" and details_dict["dispatch_id"] != current.get("dispatch_id"):
                raise TransitionDenied("ACK dispatch_id does not match active dispatch")
            if to_status == "ACCEPTED" and not evidence_refs:
                raise TaskValidationError("Assignment ACCEPTED requires verification evidence")
            updated = dict(current)
            updated.update(details_dict)
            updated.update({
                "assignment_status": to_status,
                "version": row["version"] + 1,
                "updated_at": occurred_at,
            })
            updated["evidence_refs"] = list(dict.fromkeys(current.get("evidence_refs", []) + list(evidence_refs)))
            self._db.execute(
                "UPDATE tasks SET assignment_status = ?, version = ?, payload_json = ?, updated_at = ? WHERE task_id = ?",
                (to_status, row["version"] + 1, json.dumps(updated, sort_keys=True, separators=(",", ":")),
                 occurred_at, task_id),
            )
            self._append_event(
                event_id=event_id, task_id=task_id, event_type="assignment.status_changed",
                from_state=from_status, to_state=to_status, actor_principal=actor_principal,
                actor_role=actor_role, occurred_at=occurred_at, idempotency_key=idempotency_key,
                request_hash=request_hash, evidence_refs=evidence_refs, details=details_dict,
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {"task": self.get_task(task_id), "replayed": False}

    def record_observation(
        self, task_id: str, event_type: str, *,
        actor_principal: str, actor_role: str, identity_verified: bool,
        event_id: str, idempotency_key: str, occurred_at: str,
        evidence_refs: Sequence[str] = (), details: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Append external source/CI evidence without changing Task or Assignment status."""
        self._require_verified_actor(actor_principal, actor_role, identity_verified)
        if actor_role != "orchestrator":
            raise TransitionDenied("only the orchestrator may record external observations")
        if event_type not in {
            "source.push_bound", "ci.run_completed", "github.issue_observed", "github.issue_closed"
        }:
            raise TaskValidationError("external observation event type is not allowlisted")
        event_id = _non_empty(event_id, "event_id")
        idempotency_key = _non_empty(idempotency_key, "idempotency_key")
        occurred_at = _timestamp(occurred_at)
        if not isinstance(evidence_refs, (list, tuple)) or not all(
            isinstance(x, str) and x.strip() for x in evidence_refs
        ):
            raise TaskValidationError("evidence_refs must be a list of non-empty strings")
        if not isinstance(details, Mapping) or not details:
            raise TaskValidationError("external observation requires a details object")
        details_dict = dict(details)
        request = {"task_id": task_id, "event_type": event_type, "actor_principal": actor_principal,
                   "actor_role": actor_role, "evidence_refs": list(evidence_refs), "details": details_dict}
        request_hash = self._hash(request)
        self._db.execute("BEGIN IMMEDIATE")
        try:
            prior = self._db.execute(
                "SELECT request_hash FROM task_events WHERE idempotency_key = ?", (idempotency_key,)
            ).fetchone()
            if prior:
                if prior["request_hash"] != request_hash:
                    raise IdempotencyConflict("observation idempotency key reused with different content")
                self._db.execute("COMMIT")
                return {"task": self.get_task(task_id), "replayed": True}
            row = self._db.execute(
                "SELECT status FROM tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
            if not row:
                raise KeyError(f"unknown task_id: {task_id}")
            self._append_event(
                event_id=event_id, task_id=task_id, event_type=event_type,
                from_state=row["status"], to_state=row["status"], actor_principal=actor_principal,
                actor_role=actor_role, occurred_at=occurred_at, idempotency_key=idempotency_key,
                request_hash=request_hash, evidence_refs=evidence_refs, details=details_dict,
            )
            self._db.execute("COMMIT")
        except Exception:
            self._db.execute("ROLLBACK")
            raise
        return {"task": self.get_task(task_id), "replayed": False}

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
