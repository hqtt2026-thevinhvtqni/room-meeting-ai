"""Stateless adapter from authenticated GitHub webhooks to Core event intents.

Core :8000 assigns event_id/sequence, persists events and owns Task state.
W118 only validates GitHub-specific bindings and returns a normalized intent.
No local event queue, inbox, retry store or Task database is created here.
"""
from __future__ import annotations

from typing import Any, Mapping

from .core_task_adapter import CoreTaskProjection
from .source_binding import SourceBindingError, parse_task_branch, validate_push_payload


class GitHubEventAdapterError(ValueError):
    """GitHub event cannot be safely bound to the canonical Core Task."""


def _intent(
    *,
    task: CoreTaskProjection,
    delivery: Mapping[str, Any],
    kind: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "task_id": task.task_id,
        "correlation_id": task.correlation_id,
        "type": "EVIDENCE_LINKED",
        "producer": {
            "kind": "adapter",
            "identity": "github-webhook",
            "adapter": "w118-github-event-adapter",
        },
        "payload": {"kind": kind, **dict(payload)},
        "provenance": {
            "source": "adapter_synthesized",
            "native_ref": delivery["delivery_id"],
            "raw_sha256": "sha256:" + delivery["payload_sha256"],
        },
    }


def normalize_github_delivery(
    delivery: Mapping[str, Any],
    *,
    core_task: CoreTaskProjection,
    expected_repository: str,
    allowed_ci_workflow: str,
) -> dict[str, Any]:
    """Return NORMALIZED/DEFERRED/UNBOUND/UNHANDLED without persisting state.

    The caller forwards a NORMALIZED event intent to Core's authorized event
    port. Core owns deduplication, event IDs, sequence, persistence and state.
    """
    if not isinstance(delivery, Mapping) or delivery.get("signature_verified") is not True:
        raise GitHubEventAdapterError("delivery must be signature-verified")
    if not isinstance(core_task, CoreTaskProjection):
        raise GitHubEventAdapterError("a normalized canonical Core Task snapshot is required")
    if delivery.get("repository") != expected_repository:
        raise GitHubEventAdapterError("verified delivery repository mismatch")
    event_type = delivery.get("event_type")
    payload = delivery.get("payload")
    if not isinstance(payload, Mapping):
        raise GitHubEventAdapterError("verified GitHub payload must be an object")
    delivery_id = delivery.get("delivery_id")
    payload_sha256 = delivery.get("payload_sha256")
    if not isinstance(delivery_id, str) or not delivery_id:
        raise GitHubEventAdapterError("verified delivery ID is missing")
    if not isinstance(payload_sha256, str) or len(payload_sha256) != 64:
        raise GitHubEventAdapterError("verified payload digest is missing")

    if event_type == "push":
        try:
            binding = validate_push_payload(payload, expected_repository=expected_repository)
        except SourceBindingError as exc:
            raise GitHubEventAdapterError(str(exc)) from exc
        if binding["status"] == "UNBOUND_LEGACY_BRANCH":
            return {
                "status": "UNBOUND",
                "reason": "legacy/aggregate branch has no Core Task binding; no Task event is emitted",
                "binding": binding,
                "event_intent": None,
            }
        if binding["work_id"] != core_task.work_id or binding["task_id"] != core_task.task_id:
            raise GitHubEventAdapterError("push Work/Task binding does not match canonical Core Task")
        if core_task.issue_id is None:
            return {
                "status": "BLOCKED",
                "reason": "Core Task has no verified GitHub Issue link",
                "binding": binding,
                "event_intent": None,
            }
        if binding["issue_id"] != core_task.issue_id:
            raise GitHubEventAdapterError("push Issue ID does not match Core Task Issue link")
        return {
            "status": "NORMALIZED",
            "binding": binding,
            "event_intent": _intent(
                task=core_task,
                delivery=delivery,
                kind="GITHUB_PUSH",
                payload={
                    "repository": binding["repository"],
                    "branch": binding["branch"],
                    "work_id": binding["work_id"],
                    "task_id": binding["task_id"],
                    "issue_id": binding["issue_id"],
                    "head_sha": binding["head_sha"],
                    "commits": binding["commits"],
                    "state_effect": "EVIDENCE_ONLY_NO_TASK_TRANSITION",
                },
            ),
        }

    if event_type == "workflow_run":
        run = payload.get("workflow_run")
        if not isinstance(run, Mapping):
            raise GitHubEventAdapterError("workflow_run payload is missing workflow_run object")
        if run.get("name") != allowed_ci_workflow:
            raise GitHubEventAdapterError("workflow name is not allowlisted")
        branch = run.get("head_branch")
        head_sha = run.get("head_sha")
        run_id = run.get("id")
        conclusion = run.get("conclusion")
        if not isinstance(branch, str) or not isinstance(head_sha, str) or len(head_sha) != 40:
            raise GitHubEventAdapterError("workflow_run requires head_branch and full head_sha")
        if type(run_id) is not int or run_id < 1:
            raise GitHubEventAdapterError("workflow_run requires a positive run ID")
        if conclusion not in {"success", "failure", "cancelled", "timed_out", "action_required"}:
            return {
                "status": "DEFERRED",
                "reason": "workflow run is not completed; no CI evidence event emitted",
                "event_intent": None,
            }
        try:
            branch_binding = parse_task_branch(branch)
        except SourceBindingError as exc:
            raise GitHubEventAdapterError(str(exc)) from exc
        if branch_binding is None:
            return {
                "status": "UNBOUND",
                "reason": "workflow run branch is not task-scoped",
                "event_intent": None,
            }
        if branch_binding["work_id"] != core_task.work_id or branch_binding["task_id"] != core_task.task_id:
            raise GitHubEventAdapterError("CI branch does not match canonical Core Task")
        matched = [
            item for item in core_task.source_bindings
            if item.get("branch") == branch and item.get("head_sha") == head_sha
            and item.get("issue_id") == core_task.issue_id
        ]
        if not matched:
            return {
                "status": "DEFERRED",
                "reason": "CI arrived before Core recorded the matching push evidence; caller must reconcile with Core",
                "event_intent": None,
            }
        return {
            "status": "NORMALIZED",
            "event_intent": _intent(
                task=core_task,
                delivery=delivery,
                kind="GITHUB_ACTIONS_CI_RUN",
                payload={
                    "repository": expected_repository,
                    "workflow_name": run["name"],
                    "run_id": run_id,
                    "run_attempt": run.get("run_attempt"),
                    "branch": branch,
                    "head_sha": head_sha,
                    "conclusion": conclusion,
                    "html_url": run.get("html_url"),
                    "state_effect": "EVIDENCE_ONLY_NO_TASK_OR_ASSIGNMENT_TRANSITION",
                },
            ),
        }

    if event_type == "issues":
        issue = payload.get("issue")
        if not isinstance(issue, Mapping) or issue.get("number") != core_task.issue_id:
            return {
                "status": "UNHANDLED",
                "reason": "Issue event is not linked to this Core Task",
                "event_intent": None,
            }
        return {
            "status": "NORMALIZED",
            "event_intent": _intent(
                task=core_task,
                delivery=delivery,
                kind="GITHUB_ISSUE_OBSERVATION",
                payload={
                    "issue_id": issue.get("number"),
                    "action": payload.get("action"),
                    "state": issue.get("state"),
                    "html_url": issue.get("html_url"),
                    "state_effect": "OBSERVATION_ONLY_CORE_DECIDES_TASK_STATE",
                },
            ),
        }

    return {
        "status": "UNHANDLED",
        "reason": f"event type {event_type!r} has no approved W118 mapping",
        "event_intent": None,
    }
