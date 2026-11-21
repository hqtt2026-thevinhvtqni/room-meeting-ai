import hashlib
import hmac
import json
import unittest

from scripts.w118.event_reconciler import ReconciliationError, reconcile_delivery
from scripts.w118.task_lifecycle import TaskRegistry
from scripts.w118.webhook_inbox import WebhookInbox


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
SECRET = "w118-reconciler-test-secret-at-least-32-chars"
BRANCH = "work/W118/task-W118-TASK-001"
SHA = "a" * 40
COMMIT_MESSAGE = """Implement task slice

Work-ID: W118
Task-ID: W118-TASK-001
Issue: #65
"""


def signed_ingest(inbox, delivery_id, event_type, payload):
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    signature = "sha256=" + hmac.new(SECRET.encode(), raw, hashlib.sha256).hexdigest()
    return inbox.ingest(
        delivery_id=delivery_id,
        event_type=event_type,
        signature_header=signature,
        secret=SECRET,
        raw_body=raw,
        expected_repository=REPOSITORY,
        received_at="2026-11-21T07:00:00Z",
    )


def push_payload(branch=BRANCH, issue_id=65):
    message = COMMIT_MESSAGE.replace("#65", f"#{issue_id}")
    return {
        "repository": {"full_name": REPOSITORY},
        "ref": f"refs/heads/{branch}",
        "after": SHA,
        "deleted": False,
        "forced": False,
        "commits": [{"id": SHA, "message": message}],
        "head_commit": {"id": SHA, "message": message},
    }


def workflow_payload(conclusion="success", branch=BRANCH, sha=SHA, name="W118 Auto E2E Validation"):
    return {
        "repository": {"full_name": REPOSITORY},
        "action": "completed",
        "workflow_run": {
            "name": name,
            "status": "completed",
            "conclusion": conclusion,
            "head_branch": branch,
            "head_sha": sha,
            "id": 44880001,
            "run_attempt": 1,
            "html_url": "https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44880001",
        },
    }


class Work118EventReconcilerTests(unittest.TestCase):
    def setUp(self):
        self.inbox = WebhookInbox()
        self.registry = TaskRegistry()
        task = {
            "schema_version": "1.0",
            "work_id": "W118",
            "wp_id": "W118-13",
            "task_id": "W118-TASK-001",
            "title": "Reconcile GitHub events",
            "objective": "Bind push and CI events to the correct Task",
            "scope_in": ["push", "workflow_run"],
            "scope_out": [],
            "priority": "P0",
            "acceptance_criteria": [{
                "id": "AC-1", "description": "Exact SHA evidence is recorded",
                "verification_method": "event reconciliation tests",
            }],
            "required_capabilities": ["python"],
            "risk_level": "MEDIUM",
            "dependencies": [],
            "owner_principal": "owner:vinh",
        }
        self.registry.create_task(
            task, actor_principal="owner:vinh", actor_role="owner",
            identity_verified=True, event_id="evt-task-create",
            occurred_at="2026-11-21T06:00:00Z",
        )
        self.registry.transition_task(
            "W118-TASK-001", "READY",
            actor_principal="owner:vinh", actor_role="owner", identity_verified=True,
            expected_version=1, event_id="evt-task-ready", idempotency_key="idem-task-ready",
            occurred_at="2026-11-21T06:01:00Z",
        )
        self.registry.link_issue(
            "W118-TASK-001", 65, "https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65",
            actor_principal="room:orchestrator", actor_role="orchestrator", identity_verified=True,
            expected_version=2, event_id="evt-issue-linked", idempotency_key="idem-issue-linked",
            occurred_at="2026-11-21T06:02:00Z", evidence_refs=["github://issues/65/readback"],
        )

    def tearDown(self):
        self.inbox.close()
        self.registry.close()

    def reconcile(self, delivery):
        return reconcile_delivery(
            self.inbox, self.registry, delivery,
            expected_repository=REPOSITORY,
        )

    def test_push_event_binds_to_exact_task_issue_and_sha_without_state_change(self):
        delivery = "123e4567-e89b-12d3-a456-426614174001"
        signed_ingest(self.inbox, delivery, "push", push_payload())
        result = self.reconcile(delivery)
        self.assertEqual(result["status"], "PROCESSED")
        self.assertEqual(result["decision"], "PUSH_BOUND")
        task = self.registry.get_task("W118-TASK-001")
        self.assertEqual(task["status"], "READY")
        self.assertEqual(task["version"], 3)
        observation = self.registry.list_events("W118-TASK-001")[-1]
        self.assertEqual(observation["event_type"], "source.push_bound")
        self.assertEqual(observation["details"]["head_sha"], SHA)

    def test_legacy_aggregate_push_is_processed_unbound_without_task_mutation(self):
        delivery = "123e4567-e89b-12d3-a456-426614174002"
        signed_ingest(self.inbox, delivery, "push", push_payload(branch="work/118-auto-e2e-v2"))
        result = self.reconcile(delivery)
        self.assertEqual(result["status"], "PROCESSED_UNBOUND")
        self.assertEqual(result["decision"], "UNBOUND_LEGACY_BRANCH")
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 3)

    def test_ci_event_before_push_is_deferred_then_reconciled_after_push(self):
        ci_delivery = "123e4567-e89b-12d3-a456-426614174003"
        push_delivery = "123e4567-e89b-12d3-a456-426614174004"
        signed_ingest(self.inbox, ci_delivery, "workflow_run", workflow_payload())
        deferred = self.reconcile(ci_delivery)
        self.assertEqual(deferred["status"], "DEFERRED")
        self.assertEqual(self.inbox.get_delivery(ci_delivery)["processing_state"], "PENDING")

        signed_ingest(self.inbox, push_delivery, "push", push_payload())
        self.assertEqual(self.reconcile(push_delivery)["decision"], "PUSH_BOUND")
        ci = self.reconcile(ci_delivery)
        self.assertEqual(ci["decision"], "CI_PASS_EVIDENCE_ONLY")
        self.assertEqual(self.registry.get_task("W118-TASK-001")["status"], "READY")
        self.assertEqual(self.registry.list_events("W118-TASK-001")[-1]["event_type"], "ci.run_completed")

    def test_ci_failure_is_recorded_as_evidence_not_task_acceptance_or_state_change(self):
        push_delivery = "123e4567-e89b-12d3-a456-426614174005"
        ci_delivery = "123e4567-e89b-12d3-a456-426614174006"
        signed_ingest(self.inbox, push_delivery, "push", push_payload())
        self.reconcile(push_delivery)
        signed_ingest(self.inbox, ci_delivery, "workflow_run", workflow_payload(conclusion="failure"))
        result = self.reconcile(ci_delivery)
        self.assertEqual(result["decision"], "CI_FAIL_EVIDENCE_ONLY")
        self.assertEqual(self.registry.get_task("W118-TASK-001")["state"], "ISSUE_LINKED")

    def test_wrong_issue_binding_is_blocked_and_delivery_remains_pending(self):
        delivery = "123e4567-e89b-12d3-a456-426614174007"
        signed_ingest(self.inbox, delivery, "push", push_payload(issue_id=66))
        with self.assertRaises(ReconciliationError):
            self.reconcile(delivery)
        self.assertEqual(self.inbox.get_delivery(delivery)["processing_state"], "PENDING")

    def test_unapproved_workflow_name_is_rejected(self):
        push_delivery = "123e4567-e89b-12d3-a456-426614174008"
        ci_delivery = "123e4567-e89b-12d3-a456-426614174009"
        signed_ingest(self.inbox, push_delivery, "push", push_payload())
        self.reconcile(push_delivery)
        signed_ingest(self.inbox, ci_delivery, "workflow_run", workflow_payload(name="Other Workflow"))
        with self.assertRaises(ReconciliationError):
            self.reconcile(ci_delivery)

    def test_processed_delivery_is_not_applied_twice(self):
        delivery = "123e4567-e89b-12d3-a456-426614174010"
        signed_ingest(self.inbox, delivery, "push", push_payload())
        first = self.reconcile(delivery)
        second = self.reconcile(delivery)
        self.assertEqual(first["decision"], "PUSH_BOUND")
        self.assertEqual(second["status"], "ALREADY_PROCESSED")
        self.assertEqual(len(self.registry.list_events("W118-TASK-001")), 4)


if __name__ == "__main__":
    unittest.main()
