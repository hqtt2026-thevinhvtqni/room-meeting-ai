import unittest
from urllib.parse import parse_qs, urlparse

from scripts.w118.core_task_adapter import normalize_core_task_snapshot, project_core_task_to_issue
from scripts.w118.github_issue_adapter import (
    GitHubIssueAdapter,
    GitHubIssueError,
    IssueLookupDuplicate,
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


def core_task(title="Implement GitHub mirror", instruction="Mirror the canonical Core Task.", revision="core-rev-001", issue_id=None):
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
        "github": {"issue_id": issue_id},
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
        self.adapter = GitHubIssueAdapter(
            self.fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )

    def mirror(self, task=None, adapter=None):
        return (adapter or self.adapter).mirror_core_task(
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
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )
        result = adapter.mirror_core_task(core_task(), lock_lease_id="core-lock-lease-002")
        self.assertEqual(result["action"], "CREATED")
        self.assertEqual(len(fake.issues), 2)

    def test_incomplete_issue_scan_fails_closed_before_create(self):
        issues = [{"number": i + 1, "title": f"Issue {i}", "body": "no task marker"} for i in range(100)]
        fake = FakeGitHub(issues)
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY, max_issue_pages=1,
            lease_validator=lambda lease_id, task: True,
        )
        with self.assertRaises(IssueLookupIncomplete):
            adapter.mirror_core_task(core_task(), lock_lease_id="core-lock-lease-003")
        self.assertFalse(any(call[0] == "POST" for call in fake.calls))

    def test_core_lock_lease_is_required_to_prevent_create_race(self):
        with self.assertRaises(GitHubIssueError):
            self.adapter.mirror_core_task(core_task(), lock_lease_id="")
        self.assertEqual(self.fake.calls, [])

    def test_duplicate_task_markers_fail_closed_without_post_or_patch(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        issues = [
            {"number": 11, "title": "First", "body": marker},
            {"number": 12, "title": "Second", "body": marker},
        ]
        fake = FakeGitHub(issues)
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )
        with self.assertRaises(IssueLookupDuplicate):
            self.mirror(adapter=adapter)
        self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_persisted_core_issue_id_must_match_unique_marker_issue(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        issue = {"number": 17, "title": "Existing", "body": marker}
        fake = FakeGitHub([issue])
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )
        with self.assertRaisesRegex(GitHubIssueError, "does not match Core"):
            self.mirror(task=core_task(issue_id=18), adapter=adapter)
        self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_persisted_core_issue_id_with_no_marker_issue_never_creates(self):
        fake = FakeGitHub([])
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )
        with self.assertRaisesRegex(GitHubIssueError, "persisted issue_id"):
            self.mirror(task=core_task(issue_id=19), adapter=adapter)
        self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_complete_scan_finds_issue_on_later_page_and_rejects_cross_page_duplicate(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        unrelated = [
            {"number": i + 1, "title": f"Unrelated {i}", "body": "no task marker"}
            for i in range(100)
        ]
        match = {"number": 101, "title": "Task mirror", "body": marker}
        fake = FakeGitHub(unrelated + [match])
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY, max_issue_pages=3,
            lease_validator=lambda lease_id, task: True,
        )
        result = self.mirror(task=core_task(issue_id=101), adapter=adapter)
        self.assertEqual(result["issue_id"], 101)
        self.assertEqual(result["action"], "UPDATED")
        self.assertEqual(sum(1 for method, path, _ in fake.calls if method == "GET" and path.endswith("/issues?state=all&per_page=100&page=1")), 1)
        self.assertTrue(any("page=2" in path for method, path, _ in fake.calls if method == "GET"))

        duplicate = {"number": 102, "title": "Duplicate", "body": marker}
        fake.issues.append(duplicate)
        fake.calls.clear()
        with self.assertRaises(IssueLookupDuplicate):
            self.mirror(task=core_task(issue_id=101), adapter=adapter)
        self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_matching_persisted_core_issue_id_is_the_only_accepted_issue(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        issue = {"number": 23, "title": "Existing", "body": marker}
        fake = FakeGitHub([issue])
        adapter = GitHubIssueAdapter(
            fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: True,
        )
        result = self.mirror(task=core_task(issue_id=23), adapter=adapter)
        self.assertEqual(result["issue_id"], 23)
        self.assertEqual(result["action"], "UPDATED")
        self.assertFalse(any(method == "POST" for method, _, _ in fake.calls))

    def test_lease_validation_is_mandatory_and_fail_closed(self):
        no_validator = GitHubIssueAdapter(self.fake, repository=REPOSITORY)
        with self.assertRaisesRegex(GitHubIssueError, "validator is not configured"):
            self.mirror(adapter=no_validator)
        rejecting = GitHubIssueAdapter(
            self.fake, repository=REPOSITORY,
            lease_validator=lambda lease_id, task: False,
        )
        with self.assertRaisesRegex(GitHubIssueError, "not authoritatively validated"):
            self.mirror(adapter=rejecting)
        self.assertEqual(self.fake.calls, [])

    def test_lease_validator_exception_fails_closed_before_github_api(self):
        def unavailable(lease_id, task):
            raise RuntimeError("Core authority unavailable")
        adapter = GitHubIssueAdapter(
            self.fake, repository=REPOSITORY, lease_validator=unavailable,
        )
        with self.assertRaisesRegex(GitHubIssueError, "validation failed"):
            self.mirror(adapter=adapter)
        self.assertEqual(self.fake.calls, [])

    def test_invalid_core_projection_is_rejected_before_api_call(self):
        with self.assertRaises(GitHubIssueError):
            self.adapter.mirror_core_task({"task_id": "W118-TASK-016"}, lock_lease_id="lock")
        self.assertEqual(self.fake.calls, [])

    def test_invalid_repository_is_rejected(self):
        with self.assertRaises(ValueError):
            GitHubIssueAdapter(self.fake, repository="not-a-repo")


    def test_embedded_or_quoted_marker_fails_closed_without_write(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        for body in (f"Quoted text: {marker}", f"> {marker}", f"```\n{marker}\n```", f"prefix {marker} suffix"):
            fake = FakeGitHub([{"number": 31, "title": "Unrelated", "body": body}])
            adapter = GitHubIssueAdapter(fake, repository=REPOSITORY, lease_validator=lambda lease_id, task: True)
            with self.subTest(body=body), self.assertRaises(IssueLookupDuplicate):
                self.mirror(adapter=adapter)
            self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_repeated_marker_within_one_issue_fails_closed_without_write(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        fake = FakeGitHub([{"number": 32, "title": "Ambiguous", "body": f"{marker}\n{marker}"}])
        adapter = GitHubIssueAdapter(fake, repository=REPOSITORY, lease_validator=lambda lease_id, task: True)
        with self.assertRaises(IssueLookupDuplicate):
            self.mirror(adapter=adapter)
        self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_markers_inside_long_mixed_or_unclosed_fences_fail_closed(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        fenced_bodies = (
            f"````markdown\n```\n{marker}\n```\n````",
            f"~~~~markdown\n~~~\n{marker}\n~~~\n~~~~",
            f"````outer\n```inner\n{marker}\n```\n````",
            f"````unclosed\n{marker}",
        )
        for body in fenced_bodies:
            fake = FakeGitHub([{"number": 41, "title": "Fenced marker", "body": body}])
            adapter = GitHubIssueAdapter(fake, repository=REPOSITORY, lease_validator=lambda lease_id, task: True)
            with self.subTest(body=body), self.assertRaises(IssueLookupDuplicate):
                self.mirror(adapter=adapter)
            self.assertFalse(any(method in ("POST", "PATCH") for method, _, _ in fake.calls))

    def test_marker_after_closed_long_fence_is_accepted(self):
        marker = "<!-- room-hop-core-task:W118-TASK-016 -->"
        body = f"````markdown\nexample\n````\n{marker}"
        fake = FakeGitHub([{"number": 42, "title": "Existing", "body": body}])
        adapter = GitHubIssueAdapter(fake, repository=REPOSITORY, lease_validator=lambda lease_id, task: True)
        result = self.mirror(task=core_task(issue_id=42), adapter=adapter)
        self.assertEqual(result["issue_id"], 42)

    def test_repository_requires_nonempty_valid_components(self):
        for repository in ("/room-meeting-ai", "owner/", " owner/repo", "owner/repo ", "owner//repo", "owner/repo/name"):
            with self.subTest(repository=repository), self.assertRaises(ValueError):
                GitHubIssueAdapter(self.fake, repository=repository)

if __name__ == "__main__":
    unittest.main()
