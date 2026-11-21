import unittest
from urllib.parse import parse_qs, urlparse

from scripts.w118.core_task_adapter import normalize_core_task_snapshot, project_core_task_to_issue
from scripts.w118.github_issue_adapter import (
    GitHubIssueAdapter,
    GitHubIssueError,
    IssueLookupIncomplete,
)


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
FIELD_MAP = {
    "work_id": "identity.work_id",
    "task_id": "identity.task_id",
    "correlation_id": "identity.correlation_id",
    "title": "instruction.title",
    "instruction": "instruction.body",
    "status": "state.status",
    "source_revision": "revision",
    "acceptance_checks": "acceptance",
    "wp_id": "identity.wp_id",
    "priority": "instruction.priority",
    "scope_in": "instruction.scope_in",
    "scope_out": "instruction.scope_out",
    "assigned_identity": "assignment.identity",
    "issue_id": "github.issue_id",
    "source_bindings": "source.bindings",
}


def core_task(title="Implement GitHub mirror", instruction="Mirror the canonical Core Task.", revision="core-rev-001"):
    snapshot = {
        "identity": {
            "work_id": "W118",
            "task_id": "W118-TASK-016",
            "correlation_id": "corr-w118-016",
            "wp_id": "W118-16",
        },
        "instruction": {
            "title": title,
            "body": instruction,
            "priority": "P1",
            "scope_in": ["Issue marker", "readback"],
            "scope_out": ["Task state persistence"],
        },
        "state": {"status": "IN_PROGRESS"},
        "revision": revision,
        "acceptance": [{"id": "AC-1", "description": "Issue body reflects Core snapshot"}],
        "assignment": {"identity": "agent:verified-ka"},
        "github": {"issue_id": None},
        "source": {"bindings": []},
    }
    return normalize_core_task_snapshot(snapshot, field_map=FIELD_MAP)


class FakeGitHub:
    def __init__(self, issues=None):
        self.issues = list(issues or [])
        self.next_number = max([x.get("number", 0) for x in self.issues] + [0]) + 1
        self.calls = []

    def __call__(self, method, path, body):
        self.calls.append((method, path, body))
        parsed = urlparse(path)
        if method == "GET" and parsed.path.endswith("/issues"):
            query = parse_qs(parsed.query)
            page = int(query.get("page", ["1"])[0])
            per_page = int(query.get("per_page", ["100"])[0])
            start = (page - 1) * per_page
            return 200, {}, self.issues[start:start + per_page]
        if method == "POST" and parsed.path.endswith("/issues"):
            issue = {
                "number": self.next_number,
                "title": body["title"],
                "body": body["body"],
                "labels": body.get("labels", []),
                "html_url": f"https://github.com/{REPOSITORY}/issues/{self.next_number}",
            }
            self.next_number += 1
            self.issues.append(issue)
            return 201, {}, issue
        if "/issues/" in parsed.path:
            number = int(parsed.path.rsplit("/", 1)[1])
            issue = next(x for x in self.issues if x["number"] == number)
            if method == "PATCH":
                issue.update(body)
                return 200, {}, issue
            if method == "GET":
                return 200, {}, issue
        raise AssertionError(f"unexpected request: {method} {path}")


class Work118GitHubIssueAdapterTests(unittest.TestCase):
    def setUp(self):
        self.fake = FakeGitHub()
        self.adapter = GitHubIssueAdapter(self.fake, repository=REPOSITORY)

    def mirror(self, task=None):
        return self.adapter.mirror_core_task(
            task or core_task(), lock_lease_id="core-lock-lease-001"
        )

    def test_core_projection_builds_issue_body_with_authority_boundary(self):
        projection = project_core_task_to_issue(core_task())
        self.assertIn("<!-- room-hop-core-task:W118-TASK-016 -->", projection["body"])
        self.assertIn("Core :8000 is the canonical Task/Assignment/Event authority", projection["body"])
        self.assertIn("CI PASS", projection["body"])
        self.assertIn("room-hop/core-task", projection["labels"])

    def test_first_sync_creates_issue_and_verifies_readback(self):
        result = self.mirror()
        self.assertEqual(result["action"], "CREATED")
        self.assertTrue(result["readback_verified"])
        self.assertEqual(result["issue_id"], 1)
        self.assertEqual(result["authority"], "CORE_8000_TASK_AUTHORITY_GITHUB_ISSUE_MIRROR")
        self.assertFalse(result["assignees_mutated"])
        self.assertFalse(result["issue_state_mutated"])
        self.assertEqual(len(self.fake.issues), 1)

    def test_repeated_sync_is_idempotent_and_does_not_duplicate_issue(self):
        first = self.mirror()
        second = self.mirror()
        self.assertEqual(first["issue_id"], second["issue_id"])
        self.assertEqual(second["action"], "UNCHANGED")
        self.assertEqual(len(self.fake.issues), 1)

    def test_changed_core_revision_updates_existing_issue(self):
        self.mirror()
        result = self.mirror(core_task(instruction="Updated instruction from Core.", revision="core-rev-002"))
        self.assertEqual(result["action"], "UPDATED")
        self.assertIn("Updated instruction from Core.", self.fake.issues[0]["body"])
        self.assertIn("core-rev-002", self.fake.issues[0]["body"])

    def test_pull_request_with_same_marker_is_not_treated_as_issue(self):
        pr = {
            "number": 9,
            "title": "Task PR",
            "body": "<!-- room-hop-core-task:W118-TASK-016 -->",
            "pull_request": {"url": "https://api.github.com/pulls/9"},
        }
        fake = FakeGitHub([pr])
        adapter = GitHubIssueAdapter(fake, repository=REPOSITORY)
        result = adapter.mirror_core_task(core_task(), lock_lease_id="core-lock-lease-002")
        self.assertEqual(result["action"], "CREATED")
        self.assertEqual(len(fake.issues), 2)

    def test_incomplete_issue_scan_fails_closed_before_create(self):
        issues = [{"number": i + 1, "title": f"Issue {i}", "body": "no task marker"} for i in range(100)]
        fake = FakeGitHub(issues)
        adapter = GitHubIssueAdapter(fake, repository=REPOSITORY, max_issue_pages=1)
        with self.assertRaises(IssueLookupIncomplete):
            adapter.mirror_core_task(core_task(), lock_lease_id="core-lock-lease-003")
        self.assertFalse(any(call[0] == "POST" for call in fake.calls))

    def test_core_lock_lease_is_required_to_prevent_create_race(self):
        with self.assertRaises(GitHubIssueError):
            self.adapter.mirror_core_task(core_task(), lock_lease_id="")
        self.assertEqual(self.fake.calls, [])

    def test_invalid_core_projection_is_rejected_before_api_call(self):
        with self.assertRaises(GitHubIssueError):
            self.adapter.mirror_core_task({"task_id": "W118-TASK-016"}, lock_lease_id="lock")
        self.assertEqual(self.fake.calls, [])

    def test_invalid_repository_is_rejected(self):
        with self.assertRaises(ValueError):
            GitHubIssueAdapter(self.fake, repository="not-a-repo")


if __name__ == "__main__":
    unittest.main()
