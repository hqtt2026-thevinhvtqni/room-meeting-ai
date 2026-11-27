import unittest

from scripts.w118.source_binding import (
    SourceBindingError,
    parse_commit_trailers,
    parse_task_branch,
    validate_commit_binding,
    validate_push_payload,
)


REPOSITORY = "hqtt2026-thevinhvtqni/room-meeting-ai"
BRANCH = "work/W118/task-W118-TASK-013"
SHA1 = "a" * 40
SHA2 = "b" * 40
MESSAGE = """Implement W118 Task lifecycle

Work-ID: W118
Task-ID: W118-TASK-013
Issue: #65
"""


def push_payload(**overrides):
    payload = {
        "repository": {"full_name": REPOSITORY},
        "ref": f"refs/heads/{BRANCH}",
        "after": SHA2,
        "deleted": False,
        "commits": [{"id": SHA1, "message": MESSAGE}, {"id": SHA2, "message": MESSAGE}],
        "head_commit": {"id": SHA2, "message": MESSAGE},
    }
    payload.update(overrides)
    return payload


class Work118SourceBindingTests(unittest.TestCase):
    def test_parses_task_scoped_branch(self):
        self.assertEqual(
            parse_task_branch(BRANCH),
            {"work_id": "W118", "task_id": "W118-TASK-013"},
        )

    def test_legacy_aggregate_branch_is_unbound_not_guessed(self):
        result = validate_push_payload(
            push_payload(ref="refs/heads/work/118-auto-e2e-v2"),
            expected_repository=REPOSITORY,
        )
        self.assertEqual(result["status"], "UNBOUND_LEGACY_BRANCH")
        self.assertEqual(result["enforcement"], "NOT_APPLICABLE")
        self.assertIn("no Task state may be inferred", result["reason"])

    def test_valid_push_binds_repository_work_task_issue_and_sha(self):
        result = validate_push_payload(push_payload(), expected_repository=REPOSITORY)
        self.assertEqual(result["status"], "BOUND")
        self.assertEqual(result["enforcement"], "PASS")
        self.assertEqual(result["work_id"], "W118")
        self.assertEqual(result["task_id"], "W118-TASK-013")
        self.assertEqual(result["issue_id"], 65)
        self.assertEqual(result["head_sha"], SHA2)
        self.assertEqual(result["state_effect"], "EVIDENCE_ONLY_NO_TASK_TRANSITION")

    def test_rejects_wrong_repository(self):
        with self.assertRaises(SourceBindingError):
            validate_push_payload(push_payload(), expected_repository="someone/else")

    def test_rejects_branch_work_task_prefix_mismatch(self):
        with self.assertRaises(SourceBindingError):
            parse_task_branch("work/W117/task-W118-TASK-013")

    def test_rejects_missing_commit_trailers(self):
        with self.assertRaises(SourceBindingError):
            parse_commit_trailers("quick fix")

    def test_rejects_duplicate_commit_trailers(self):
        with self.assertRaises(SourceBindingError):
            parse_commit_trailers(MESSAGE + "Issue: #66\n")

    def test_rejects_commit_task_mismatch(self):
        bad = MESSAGE.replace("W118-TASK-013", "W118-TASK-014")
        with self.assertRaises(SourceBindingError):
            validate_commit_binding(bad, work_id="W118", task_id="W118-TASK-013", issue_id=65)

    def test_rejects_mixed_issue_ids_in_one_push(self):
        other = MESSAGE.replace("#65", "#66")
        payload = push_payload(commits=[
            {"id": SHA1, "message": MESSAGE},
            {"id": SHA2, "message": other},
        ])
        with self.assertRaises(SourceBindingError):
            validate_push_payload(payload, expected_repository=REPOSITORY)

    def test_rejects_head_sha_mismatch(self):
        payload = push_payload(head_commit={"id": SHA1, "message": MESSAGE})
        with self.assertRaises(SourceBindingError):
            validate_push_payload(payload, expected_repository=REPOSITORY)

    def test_rejects_force_push(self):
        with self.assertRaises(SourceBindingError):
            validate_push_payload(push_payload(forced=True), expected_repository=REPOSITORY)

    def test_rejects_head_sha_not_in_commits(self):
        payload = push_payload(commits=[{"id": SHA1, "message": MESSAGE}])
        with self.assertRaises(SourceBindingError):
            validate_push_payload(payload, expected_repository=REPOSITORY)

    def test_rejects_branch_deletion(self):
        with self.assertRaises(SourceBindingError):
            validate_push_payload(push_payload(deleted=True), expected_repository=REPOSITORY)

    def test_rejects_missing_push_commits(self):
        with self.assertRaises(SourceBindingError):
            validate_push_payload(push_payload(commits=[]), expected_repository=REPOSITORY)


if __name__ == "__main__":
    unittest.main()
