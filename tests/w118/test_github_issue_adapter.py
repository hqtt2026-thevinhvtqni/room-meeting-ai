import unittest
from urllib.parse import parse_qs, urlparse

from scripts.w118.github_issue_adapter import (
    GitHubIssueAdapter,
    IssueLookupIncomplete,
    build_task_issue_body,
    task_issue_marker,
)


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"


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


def task():
    return {
        "work_id": "W118",
        "wp_id": "W118-13",
        "task_id": "W118-TASK-013",
        "title": "Implement Task lifecycle",
        "objective": "Provide versioned Task state transitions",
        "priority": "P0",
        "owner_principal": "owner:vinh",
        "scope_in": ["Task contract", "event history"],
        "scope_out": ["Live Agent dispatch"],
        "acceptance_criteria": [{
            "id": "AC-1",
            "description": "Transitions are authorized",
            "verification_method": "unit tests",
        }],
    }


class Work118GitHubIssueAdapterTests(unittest.TestCase):
    def test_builds_issue_body_with_stable_task_marker_and_authority_boundary(self):
        body = build_task_issue_body(task())
        self.assertIn(task_issue_marker("W118-TASK-013"), body)
        self.assertIn("Work-ID", body)
        self.assertIn("CI success does not constitute Task acceptance", body)

    def test_first_sync_creates_issue_and_verifies_readback(self):
        fake = FakeGitHub()
        adapter = GitHubIssueAdapter(REPOSITORY, "test-token", transport=fake)
        result = adapter.mirror_task(task())
        self.assertEqual(result["action"], "CREATED")
        self.assertTrue(result["readback_verified"])
        self.assertEqual(result["issue_id"], 1)
        self.assertFalse(result["assignees_mutated"])
        self.assertFalse(result["issue_state_mutated"])
        self.assertEqual(len(fake.issues), 1)

    def test_repeated_sync_is_idempotent_and_does_not_duplicate_issue(self):
        fake = FakeGitHub()
        adapter = GitHubIssueAdapter(REPOSITORY, "test-token", transport=fake)
        first = adapter.mirror_task(task())
        second = adapter.mirror_task(task())
        self.assertEqual(first["issue_id"], second["issue_id"])
        self.assertEqual(second["action"], "UNCHANGED")
        self.assertEqual(len(fake.issues), 1)

    def test_existing_issue_is_updated_and_read_back(self):
        fake = FakeGitHub()
        adapter = GitHubIssueAdapter(REPOSITORY, "test-token", transport=fake)
        adapter.mirror_task(task())
        updated_task = {**task(), "objective": "Track full authorized Task lifecycle"}
        result = adapter.mirror_task(updated_task)
        self.assertEqual(result["action"], "UPDATED")
        self.assertIn("Track full authorized Task lifecycle", fake.issues[0]["body"])

    def test_pull_request_with_same_marker_is_not_treated_as_issue(self):
        pr = {
            "number": 9,
            "title": "Task PR",
            "body": task_issue_marker("W118-TASK-013"),
            "pull_request": {"url": "https://api.github.com/pulls/9"},
        }
        fake = FakeGitHub([pr])
        adapter = GitHubIssueAdapter(REPOSITORY, "test-token", transport=fake)
        result = adapter.mirror_task(task())
        self.assertEqual(result["action"], "CREATED")
        self.assertEqual(len(fake.issues), 2)

    def test_incomplete_issue_scan_fails_closed_before_create(self):
        issues = [
            {"number": i + 1, "title": f"Issue {i}", "body": "no task marker"}
            for i in range(100)
        ]
        fake = FakeGitHub(issues)
        adapter = GitHubIssueAdapter(
            REPOSITORY, "test-token", transport=fake, max_issue_pages=1
        )
        with self.assertRaises(IssueLookupIncomplete):
            adapter.mirror_task(task())
        self.assertFalse(any(call[0] == "POST" for call in fake.calls))

    def test_invalid_task_id_is_rejected_before_api_call(self):
        fake = FakeGitHub()
        adapter = GitHubIssueAdapter(REPOSITORY, "test-token", transport=fake)
        with self.assertRaises(ValueError):
            adapter.mirror_task({**task(), "task_id": "bad task id"})
        self.assertEqual(fake.calls, [])

    def test_invalid_repository_and_missing_token_are_rejected(self):
        with self.assertRaises(ValueError):
            GitHubIssueAdapter("not-a-repo", "token")
        with self.assertRaises(ValueError):
            GitHubIssueAdapter(REPOSITORY, "")


if __name__ == "__main__":
    unittest.main()
