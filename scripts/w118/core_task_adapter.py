"""Read-only projection adapter for the canonical ROOM-HOP Core Task API.

W118 does not persist Task state or Assignment state. Core :8000 is the sole
runtime Task/Event authority. W102 owns Agent Loop policy; W52 is a draft
interoperability reference. This module normalizes an approved Core snapshot
into a GitHub-facing projection DTO. It is not a Core schema or state machine.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class CoreTaskContractError(ValueError):
    """Core Task projection is incomplete or inconsistent."""


@dataclass(frozen=True)
class CoreTaskProjection:
    work_id: str
    task_id: str
    correlation_id: str
    title: str
    instruction: str
    status: str
    source_revision: str
    acceptance_checks: tuple[dict[str, Any], ...]
    wp_id: str | None = None
    priority: str | None = None
    scope_in: tuple[str, ...] = ()
    scope_out: tuple[str, ...] = ()
    assigned_identity: str | None = None
    issue_id: int | None = None
    source_bindings: tuple[dict[str, Any], ...] = ()


_REQUIRED_MAP = (
    "work_id", "task_id", "correlation_id", "title",
    "instruction", "status", "source_revision", "acceptance_checks",
)
_OPTIONAL_MAP = (
    "wp_id", "priority", "scope_in", "scope_out",
    "assigned_identity", "issue_id", "source_bindings",
)


def _read_path(snapshot: Mapping[str, Any], path: str) -> Any:
    current: Any = snapshot
    for segment in path.split("."):
        if not isinstance(current, Mapping) or segment not in current:
            raise CoreTaskContractError(f"Core snapshot path is missing: {path}")
        current = current[segment]
    return current


def normalize_core_task_snapshot(
    snapshot: Mapping[str, Any],
    *,
    field_map: Mapping[str, str],
) -> CoreTaskProjection:
    """Normalize Core output using a field map approved by the Core owner.

    No Core field names are guessed here. The integration cannot be enabled
    until the actual Core API schema and field_map are supplied by its owner.
    """
    if not isinstance(snapshot, Mapping):
        raise CoreTaskContractError("Core snapshot must be an object")
    if not isinstance(field_map, Mapping):
        raise CoreTaskContractError("field_map must be an object")
    missing = [key for key in _REQUIRED_MAP if not isinstance(field_map.get(key), str) or not field_map[key].strip()]
    if missing:
        raise CoreTaskContractError("field_map missing required mappings: " + ", ".join(missing))

    values: dict[str, Any] = {}
    for key in _REQUIRED_MAP:
        values[key] = _read_path(snapshot, field_map[key])
    for key in _OPTIONAL_MAP:
        path = field_map.get(key)
        values[key] = _read_path(snapshot, path) if isinstance(path, str) and path.strip() else None

    for key in ("work_id", "task_id", "correlation_id", "title", "instruction", "status", "source_revision"):
        if not isinstance(values[key], str) or not values[key].strip():
            raise CoreTaskContractError(f"normalized Core field {key} must be non-empty")
        values[key] = values[key].strip()

    checks = values["acceptance_checks"]
    if not isinstance(checks, list) or not checks:
        raise CoreTaskContractError("acceptance_checks must be a non-empty list")
    normalized_checks = []
    seen_ids = set()
    for check in checks:
        if not isinstance(check, Mapping):
            raise CoreTaskContractError("each acceptance check must be an object")
        check_id = check.get("id")
        description = check.get("description")
        if not isinstance(check_id, str) or not check_id.strip():
            raise CoreTaskContractError("acceptance check id must be non-empty")
        if check_id in seen_ids:
            raise CoreTaskContractError("acceptance check IDs must be unique")
        if not isinstance(description, str) or not description.strip():
            raise CoreTaskContractError("acceptance check description must be non-empty")
        seen_ids.add(check_id)
        normalized_checks.append(dict(check))

    for key in ("scope_in", "scope_out"):
        value = values[key]
        if value is None:
            values[key] = ()
        elif isinstance(value, list) and all(isinstance(item, str) and item.strip() for item in value):
            values[key] = tuple(item.strip() for item in value)
        else:
            raise CoreTaskContractError(f"{key} must be a list of non-empty strings")

    bindings = values["source_bindings"]
    if bindings is None:
        bindings = []
    if not isinstance(bindings, list) or not all(isinstance(item, Mapping) for item in bindings):
        raise CoreTaskContractError("source_bindings must be a list of objects")

    issue_id = values["issue_id"]
    if issue_id is not None and (type(issue_id) is not int or issue_id < 1):
        raise CoreTaskContractError("issue_id must be a positive integer or null")
    for key in ("wp_id", "priority", "assigned_identity"):
        value = values[key]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise CoreTaskContractError(f"{key} must be a non-empty string or null")

    return CoreTaskProjection(
        work_id=values["work_id"],
        task_id=values["task_id"],
        correlation_id=values["correlation_id"],
        title=values["title"],
        instruction=values["instruction"],
        status=values["status"],
        source_revision=values["source_revision"],
        acceptance_checks=tuple(normalized_checks),
        wp_id=values["wp_id"],
        priority=values["priority"],
        scope_in=values["scope_in"],
        scope_out=values["scope_out"],
        assigned_identity=values["assigned_identity"],
        issue_id=issue_id,
        source_bindings=tuple(dict(item) for item in bindings),
    )


def core_task_issue_marker(task_id: str) -> str:
    if not isinstance(task_id, str) or not task_id.strip():
        raise CoreTaskContractError("task_id must be non-empty")
    return f"<!-- room-hop-core-task:{task_id.strip()} -->"


def project_core_task_to_issue(task: CoreTaskProjection) -> dict[str, Any]:
    """Build a read-only GitHub Issue projection; never mutates Core state."""
    marker = core_task_issue_marker(task.task_id)
    lines = [
        marker,
        f"# {task.title}",
        "",
        f"- Work: `{task.work_id}`",
        f"- Core Task: `{task.task_id}`",
        f"- Correlation: `{task.correlation_id}`",
        f"- Core state: `{task.status}`",
        f"- Core source revision: `{task.source_revision}`",
    ]
    if task.wp_id:
        lines.append(f"- Work Package: `{task.wp_id}`")
    if task.priority:
        lines.append(f"- Priority: `{task.priority}`")
    if task.assigned_identity:
        lines.append(f"- Core assigned identity: `{task.assigned_identity}`")
    lines.extend(["", "## Instruction", task.instruction, "", "## Scope"])
    if task.scope_in:
        lines.extend(["### In scope", *[f"- {item}" for item in task.scope_in]])
    if task.scope_out:
        lines.extend(["### Out of scope", *[f"- {item}" for item in task.scope_out]])
    lines.extend(["", "## Acceptance checks"])
    lines.extend(
        f"- [ ] **{check['id']}** — {check['description']}"
        for check in task.acceptance_checks
    )
    lines.extend([
        "",
        "## Authority boundary",
        "Core :8000 is the canonical Task/Assignment/Event authority. This Issue is a collaboration mirror only.",
        "CI PASS, Issue closure, labels or comments do not independently accept or complete the Core Task.",
    ])
    labels = ["room-hop", "room-hop/core-task"]
    state_label = {
        "PLANNED": "room-hop/state/planned",
        "READY": "room-hop/state/ready",
        "IN_PROGRESS": "room-hop/state/in-progress",
        "BLOCKED": "room-hop/state/blocked",
        "IN_REVIEW": "room-hop/state/in-review",
        "DONE": "room-hop/state/done",
        "CANCELLED": "room-hop/state/cancelled",
    }.get(task.status)
    if state_label:
        labels.append(state_label)
    return {"title": f"[{task.work_id}] {task.title}", "body": "\n".join(lines), "labels": labels}
