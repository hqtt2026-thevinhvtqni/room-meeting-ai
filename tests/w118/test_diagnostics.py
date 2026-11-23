import unittest

from scripts.w118.diagnostics import (
    build_plan,
    diagnostic_key,
    find_existing_issue,
    update_marker,
)


class Work118DiagnosticsTests(unittest.TestCase):
    def test_key_is_stable_for_same_workflow_and_commit(self):
        self.assertEqual(
            diagnostic_key(1234, "a" * 40),
            diagnostic_key("1234", "A" * 40),
        )

    def test_key_separates_workflows_and_commits(self):
        sha = "b" * 40
        self.assertNotEqual(diagnostic_key(1, sha), diagnostic_key(2, sha))
        self.assertNotEqual(diagnostic_key(1, sha), diagnostic_key(1, "c" * 40))

    def test_invalid_workflow_or_sha_is_rejected(self):
        with self.assertRaises(ValueError):
            diagnostic_key("not-numeric", "a" * 40)
        with self.assertRaises(ValueError):
            diagnostic_key(1, "not-a-sha")

    def test_retry_attempt_has_distinct_update_marker(self):
        self.assertNotEqual(update_marker(55, 1), update_marker(55, 2))
        self.assertEqual(update_marker("55", "1"), "<!-- w118-diagnostic-update:55:1 -->")

    def test_existing_issue_is_reused_by_exact_key(self):
        key = diagnostic_key(9, "d" * 40)
        issues = [
            {"number": 100, "body": "unrelated"},
            {"number": 101, "body": f"diagnostic\n<!-- {key} -->"},
        ]
        self.assertEqual(find_existing_issue(issues, key), "101")

    def test_plan_contains_issue_and_attempt_idempotency(self):
        key = diagnostic_key(9, "e" * 40)
        plan = build_plan([{"number": 102, "body": f"<!-- {key} -->"}], 9, "e" * 40, 77, 2, scan_complete=True)
        self.assertEqual(plan["existing_issue"], "102")
        self.assertEqual(plan["update_marker"], "<!-- w118-diagnostic-update:77:2 -->")


    def test_closed_issue_is_reused_by_exact_key(self):
        key = diagnostic_key(19, "f" * 40)
        issues = [
            {"number": 201, "state": "closed", "body": f"resolved\n<!-- {key} -->"},
        ]
        self.assertEqual(find_existing_issue(issues, key), "201")


    def test_embedded_quoted_and_fenced_markers_fail_closed(self):
        key = diagnostic_key(31, "a" * 40)
        marker = f"<!-- {key} -->"
        for body in (f"quoted {marker}", f"> {marker}", f"```\n{marker}\n```", f"prefix {marker} suffix"):
            with self.subTest(body=body), self.assertRaises(ValueError):
                find_existing_issue([{"number": 301, "body": body}], key)

    def test_duplicate_marker_across_issues_fails_closed(self):
        key = diagnostic_key(32, "b" * 40)
        marker = f"<!-- {key} -->"
        issues = [{"number": 302, "body": marker}, {"number": 303, "body": marker}]
        with self.assertRaisesRegex(ValueError, "multiple Issues"):
            find_existing_issue(issues, key)

    def test_scan_completeness_is_required_by_default(self):
        with self.assertRaisesRegex(ValueError, "scan is incomplete"):
            build_plan([], 34, "d" * 40, 89, 1)

    def test_incomplete_scan_blocks_diagnostic_plan(self):
        with self.assertRaisesRegex(ValueError, "scan is incomplete"):
            build_plan([], 33, "c" * 40, 88, 1, scan_complete=False)

if __name__ == "__main__":
    unittest.main()
