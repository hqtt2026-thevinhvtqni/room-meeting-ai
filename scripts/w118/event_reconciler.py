"""Reconcile authenticated GitHub push/CI events into the Sandbox Task event log.

The reconciler records evidence-only observations. It never promotes CI PASS
to VERIFIED/ACCEPTED and never changes Task lifecycle state on webhook receipt.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

from scripts.w118.source_binding import (
    SourceBindingError,
    parse_task_branch,
    validate_push_payload,
)
from scripts.w118.task_lifecycle import TaskRegistry
from scripts.w118.webhook_inbox import WebhookInbox


SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_CI_WORKFLOWS = {"W118 Auto E2E Validation"}


class ReconciliationError(RuntimeError):
    """Authenticated event cannot be safely mapped to a Sandbox Task."""


def reconcile_delivery(
    inbox: WebhookInbox,
    registry: TaskRegistry,
    delivery_id: str,
    *,
    expected_repository: str,
    service_principal: str = "room-hop:event-listener",
) -> dict[str, Any]:
    """Process one pending webhook; out-of-order CI events remain PENDING."""
    delivery = inbox.get_delivery(delivery_id)
    if delivery["processing_state"] == "PROCESSED":
        return {
            "status": "ALREADY_PROCESSED",
            "delivery_id": delivery_id,
            "result": delivery.get("result"),
        }
    if delivery["processing_state"] != "PENDING":
        raise ReconciliationError("delivery is not pending")

    event_type = delivery["event_type"]
    payload = delivery["payload"]
    repository = payload.get("repository", {}).get("full_name") if isinstance(payload.get("repository"), Mapping) else None
    if repository != expected_repository:
        raise ReconciliationError("stored webhook repository does not match reconciler configuration")

    if event_type == "push":
        try:
            binding = validate_push_payload(payload, expected_repository=expected_repository)
        except SourceBindingError as exc:
            raise ReconciliationError(str(exc)) from exc
        if binding["status"] == "UNBOUND_LEGACY_BRANCH":
            result = {
                "decision": "UNBOUND_LEGACY_BRANCH",
                "branch": binding["branch"],
                "task_state_changed": False,
            }
            inbox.mark_processed(delivery_id, result)
            return {"status": "PROCESSED_UNBOUND", "delivery_id": delivery_id, **result}

        try:
            task = registry.get_task(binding["task_id"])
        except KeyError as exc:
            raise ReconciliationError("push references an unknown Sandbox Task") from exc
        if task.get("work_id") != binding["work_id"]:
            raise ReconciliationError("push Work ID does not match Sandbox Task")
        if task.get("issue_id") != binding["issue_id"]:
            raise ReconciliationError("push Issue ID does not match linked Sandbox Task")

        observation = registry.record_observation(
            binding["task_id"],
            "source.push_bound",
            actor_principal=service_principal,
            actor_role="orchestrator",
            identity_verified=True,
            event_id=delivery_id,
            idempotency_key=f"github:{delivery_id}",
            occurred_at=delivery["received_at"],
            evidence_refs=[
                f"github://delivery/{delivery_id}",
                f"github://commit/{binding['head_sha']}",
            ],
            details={
                "delivery_id": delivery_id,
                "repository": binding["repository"],
                "branch": binding["branch"],
                "work_id": binding["work_id"],
                "task_id": binding["task_id"],
                "issue_id": binding["issue_id"],
                "head_sha": binding["head_sha"],
                "commit_shas": [item["commit_sha"] for item in binding["commits"]],
            },
        )
        result = {
            "decision": "PUSH_BOUND",
            "task_id": binding["task_id"],
            "issue_id": binding["issue_id"],
            "head_sha": binding["head_sha"],
            "observation_replayed": observation["replayed"],
            "task_state_changed": False,
        }
        inbox.mark_processed(delivery_id, result)
        return {"status": "PROCESSED", "delivery_id": delivery_id, **result}

    if event_type == "workflow_run":
        action = payload.get("action")
        run = payload.get("workflow_run")
        if not isinstance(run, Mapping):
            raise ReconciliationError("workflow_run payload is missing workflow_run object")
        if run.get("name") not in ALLOWED_CI_WORKFLOWS:
            raise ReconciliationError("workflow_run name is not authorized for W118 Task reconciliation")
        if action != "completed" or run.get("status") != "completed":
            result = {"decision": "IGNORED_NON_COMPLETION", "task_state_changed": False}
            inbox.mark_processed(delivery_id, result)
            return {"status": "PROCESSED_IGNORED", "delivery_id": delivery_id, **result}

        branch = run.get("head_branch")
        branch_binding = parse_task_branch(branch)
        if branch_binding is None:
            result = {
                "decision": "UNBOUND_LEGACY_BRANCH",
                "branch": branch,
                "task_state_changed": False,
            }
            inbox.mark_processed(delivery_id, result)
            return {"status": "PROCESSED_UNBOUND", "delivery_id": delivery_id, **result}

        head_sha = run.get("head_sha")
        run_id = run.get("id")
        run_attempt = run.get("run_attempt", 1)
        conclusion = run.get("conclusion")
        if not isinstance(head_sha, str) or not SHA_RE.fullmatch(head_sha):
            raise ReconciliationError("workflow_run head_sha is invalid")
        if type(run_id) is not int or run_id < 1 or type(run_attempt) is not int or run_attempt < 1:
            raise ReconciliationError("workflow_run ID/attempt is invalid")
        if conclusion not in {"success", "failure", "cancelled", "timed_out", "action_required", "stale"}:
            raise ReconciliationError("workflow_run conclusion is missing or unsupported")

        try:
            task = registry.get_task(branch_binding["task_id"])
        except KeyError as exc:
            raise ReconciliationError("workflow_run references an unknown Sandbox Task") from exc
        if task.get("work_id") != branch_binding["work_id"]:
            raise ReconciliationError("workflow_run Work ID does not match Sandbox Task")

        push_evidence = [
            event for event in registry.list_events(branch_binding["task_id"])
            if event["event_type"] == "source.push_bound"
            and event["details"].get("branch") == branch
            and event["details"].get("head_sha") == head_sha
        ]
        if not push_evidence:
            return {
                "status": "DEFERRED",
                "delivery_id": delivery_id,
                "reason": "matching source.push_bound event has not been reconciled yet",
                "task_state_changed": False,
            }

        run_url = run.get("html_url")
        if not isinstance(run_url, str) or not run_url.startswith("https://github.com/"):
            raise ReconciliationError("workflow_run html_url is invalid")
        observation = registry.record_observation(
            branch_binding["task_id"],
            "ci.run_completed",
            actor_principal=service_principal,
            actor_role="orchestrator",
            identity_verified=True,
            event_id=delivery_id,
            idempotency_key=f"github:{delivery_id}",
            occurred_at=delivery["received_at"],
            evidence_refs=[run_url, f"github://commit/{head_sha}"],
            details={
                "delivery_id": delivery_id,
                "repository": expected_repository,
                "branch": branch,
                "work_id": branch_binding["work_id"],
                "task_id": branch_binding["task_id"],
                "head_sha": head_sha,
                "run_id": run_id,
                "run_attempt": run_attempt,
                "conclusion": conclusion,
                "run_url": run_url,
            },
        )
        decision = "CI_PASS_EVIDENCE_ONLY" if conclusion == "success" else "CI_FAIL_EVIDENCE_ONLY"
        result = {
            "decision": decision,
            "task_id": branch_binding["task_id"],
            "run_id": run_id,
            "head_sha": head_sha,
            "conclusion": conclusion,
            "observation_replayed": observation["replayed"],
            "task_state_changed": False,
        }
        inbox.mark_processed(delivery_id, result)
        return {"status": "PROCESSED", "delivery_id": delivery_id, **result}

    return {
        "status": "DEFERRED_UNSUPPORTED_EVENT",
        "delivery_id": delivery_id,
        "reason": f"no reconciler handler for event type {event_type}",
        "task_state_changed": False,
    }
