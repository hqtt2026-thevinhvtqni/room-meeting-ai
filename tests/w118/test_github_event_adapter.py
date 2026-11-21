import hashlib
import hmac
import json
import unittest
import uuid

from scripts.w118.core_task_adapter import normalize_core_task_snapshot
from scripts.w118.github_event_adapter import (
    GitHubEventAdapterError,
    normalize_github_delivery,
)
from scripts.w118.github_webhook_verifier import verify_github_webhook


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
SECRET = "test-secret-value-with-at-least-32-characters"
WORKFLOW = "W118 Auto E2E Validation"
FIELD_MAP = {
    "work_id": "identity.work_id",
    "task_id": "identity.task_id",
    "correlation_id": "identity.correlation_id",
    "title": "instruction.title",
    "instruction": "instruction.body",
    "status": "state.status",
    "source_revision": "revision",
    "acceptance_checks": "acceptance",
    "issue_id": "github.issue_id",
    "source_bindings": "source.bindings",
}


def core_task(*, issue_id=65, source_bindings=None):
    snapshot = {
        "identity": {"work_id": "W118", "task_id": "W118-TASK-016", "correlation_id": "corr-016"},
        "instruction": {"title": "Task", "body": "Do the work."},
        "state": {"status": "IN_PROGRESS"},
        "revision": "core-rev-1",
        "acceptance": [{"id": "AC-1", "description": "Evidence is bound"}],
        "github": {"issue_id": issue_id},
        "source": {"bindings": source_bindings or []},
    }
    return normalize_core_task_snapshot(snapshot, field_map=FIELD_MAP)


def delivery(event_type, payload):
    body = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()
    return verify_github_webhook(
        raw_body=body,
        secret=SECRET,
        signature_header="sha256=" + signature,
        delivery_id=str(uuid.uuid4()),
        event_type=event_type,
        expected_repository=REPOSITORY,
        received_at="2026-11-21T13:00:00Z",
    )


def push_payload(*, branch="work/W118/task-W118-TASK-016", task_id="W118-TASK-016", issue_id=65):
    sha = "a" * 40
    message = f"Implement source binding\n\nWork-ID: W118\nTask-ID: {task_id}\nIssue: #{issue_id}"
    commit = {"id": sha, "message": message}
    return {
        "repository": {"full_name": REPOSITORY},
        "ref": "refs/heads/" + branch,
        "after": sha,
        "forced": False,
        "deleted": False,
        "commits": [commit],
        "head_commit": {"id": sha, "message": message},
    }


def workflow_payload(*, branch="work/W118/task-W118-TASK-016", head_sha="a" * 40, name=WORKFLOW, conclusion="success"):
    return {
        "repository": {"full_name": REPOSITORY},
        "workflow_run": {
            "name": name, "head_branch": branch, "head_sha": head_sha,
            "id": 1234, "run_attempt": 1, "conclusion": conclusion,
            "html_url": "https://github.com/example/repo/actions/runs/1234",
        },
    }


class GitHubEventAdapterTests(unittest.TestCase):
    def test_task_scoped_push_maps_to_core_evidence_intent(self):
        verified = delivery("push", push_payload())
        result = normalize_github_delivery(
            verified, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
        )
        self.assertEqual(result["status"], "NORMALIZED")
        intent = result["event_intent"]
        self.assertEqual(intent["type"], "EVIDENCE_LINKED")
        self.assertEqual(intent["task_id"], "W118-TASK-016")
        self.assertEqual(intent["payload"]["kind"], "GITHUB_PUSH")
        self.assertEqual(intent["payload"]["head_sha"], "a" * 40)
        self.assertNotIn("event_id", intent)
        self.assertNotIn("seq", intent)

    def test_aggregate_branch_is_unbound_and_emits_no_event(self):
        verified = delivery("push", push_payload(branch="work/118-auto-e2e-v2"))
        result = normalize_github_delivery(
            verified, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
        )
        self.assertEqual(result["status"], "UNBOUND")
        self.assertIsNone(result["event_intent"])

    def test_push_task_mismatch_is_rejected(self):
        verified = delivery("push", push_payload(task_id="W118-TASK-999"))
        with self.assertRaises(GitHubEventAdapterError):
            normalize_github_delivery(
                verified, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
            )

    def test_push_issue_mismatch_is_rejected(self):
        verified = delivery("push", push_payload(issue_id=66))
        with self.assertRaises(GitHubEventAdapterError):
            normalize_github_delivery(
                verified, core_task=core_task(issue_id=65), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
            )

    def test_push_without_core_issue_link_is_blocked(self):
        verified = delivery("push", push_payload())
        result = normalize_github_delivery(
            verified, core_task=core_task(issue_id=None), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIsNone(result["event_intent"])

    def test_ci_before_core_push_evidence_is_deferred_without_local_queue(self):
        verified = delivery("workflow_run", workflow_payload())
        result = normalize_github_delivery(
            verified, core_task=core_task(source_bindings=[]),
            expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW,
        )
        self.assertEqual(result["status"], "DEFERRED")
        self.assertIsNone(result["event_intent"])

    def test_ci_with_exact_core_source_binding_maps_to_evidence_only(self):
        binding = {"branch": "work/W118/task-W118-TASK-016", "head_sha": "a" * 40, "issue_id": 65}
        verified = delivery("workflow_run", workflow_payload())
        result = normalize_github_delivery(
            verified, core_task=core_task(source_bindings=[binding]),
            expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW,
        )
        self.assertEqual(result["status"], "NORMALIZED")
        intent = result["event_intent"]
        self.assertEqual(intent["payload"]["kind"], "GITHUB_ACTIONS_CI_RUN")
        self.assertEqual(intent["payload"]["conclusion"], "success")
        self.assertEqual(intent["payload"]["state_effect"], "EVIDENCE_ONLY_NO_TASK_OR_ASSIGNMENT_TRANSITION")
        self.assertNotIn("event_id", intent)
        self.assertNotIn("seq", intent)

    def test_unapproved_workflow_is_rejected(self):
        verified = delivery("workflow_run", workflow_payload(name="untrusted workflow"))
        with self.assertRaises(GitHubEventAdapterError):
            normalize_github_delivery(
                verified, core_task=core_task(source_bindings=[{
                    "branch": "work/W118/task-W118-TASK-016", "head_sha": "a" * 40, "issue_id": 65,
                }]), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW,
            )

    def test_ci_failure_is_evidence_not_task_verdict(self):
        binding = {"branch": "work/W118/task-W118-TASK-016", "head_sha": "a" * 40, "issue_id": 65}
        verified = delivery("workflow_run", workflow_payload(conclusion="failure"))
        result = normalize_github_delivery(
            verified, core_task=core_task(source_bindings=[binding]),
            expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW,
        )
        self.assertEqual(result["event_intent"]["payload"]["conclusion"], "failure")
        self.assertEqual(result["event_intent"]["payload"]["state_effect"], "EVIDENCE_ONLY_NO_TASK_OR_ASSIGNMENT_TRANSITION")

    def test_issue_close_is_observation_only(self):
        verified = delivery("issues", {
            "repository": {"full_name": REPOSITORY},
            "action": "closed",
            "issue": {"number": 65, "state": "closed", "html_url": "https://github.com/example/repo/issues/65"},
        })
        result = normalize_github_delivery(
            verified, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
        )
        self.assertEqual(result["status"], "NORMALIZED")
        self.assertEqual(result["event_intent"]["payload"]["state_effect"], "OBSERVATION_ONLY_CORE_DECIDES_TASK_STATE")

    def test_unlinked_issue_is_not_mapped_to_core_task(self):
        verified = delivery("issues", {
            "repository": {"full_name": REPOSITORY},
            "action": "closed",
            "issue": {"number": 999, "state": "closed"},
        })
        result = normalize_github_delivery(
            verified, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
        )
        self.assertEqual(result["status"], "UNHANDLED")
        self.assertIsNone(result["event_intent"])

    def test_unverified_delivery_is_rejected(self):
        fake = {"signature_verified": False, "repository": REPOSITORY}
        with self.assertRaises(GitHubEventAdapterError):
            normalize_github_delivery(
                fake, core_task=core_task(), expected_repository=REPOSITORY, allowed_ci_workflow=WORKFLOW
            )


if __name__ == "__main__":
    unittest.main()
