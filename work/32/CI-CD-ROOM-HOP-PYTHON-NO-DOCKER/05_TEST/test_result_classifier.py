"""Unit tests for the Work 32 evidence classifier; run via unittest or pytest."""
import sys
import unittest
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1] / "04_CODE"
sys.path.insert(0, str(CODE_ROOT))

from python_test_runtime.result_classifier import classify_pytest_result


def good_result(**overrides):
    result = {
        "status": "PASS",
        "launched": True,
        "exit_code": 0,
        "test_summary": {
            "collected": 3,
            "passed": 3,
            "failed": 0,
            "skipped": 0,
            "errors": 0,
        },
    }
    result.update(overrides)
    return result


class TestPytestResultClassifier(unittest.TestCase):
    def test_pass_requires_real_run_and_structured_counts(self):
        self.assertEqual(classify_pytest_result(good_result())["status"], "PASS")

    def test_zero_collected_is_not_pass(self):
        result = good_result(test_summary={
            "collected": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0
        })
        self.assertEqual(classify_pytest_result(result)["status"], "COLLECTION_FAILED")

    def test_pytest_exit_code_five_is_collection_failure(self):
        result = good_result(exit_code=5)
        self.assertEqual(classify_pytest_result(result)["status"], "COLLECTION_FAILED")

    def test_missing_summary_is_pending_evidence(self):
        result = good_result()
        result.pop("test_summary")
        self.assertEqual(classify_pytest_result(result)["status"], "PENDING EVIDENCE")

    def test_missing_exit_code_is_pending_evidence(self):
        result = good_result(exit_code=None)
        self.assertEqual(classify_pytest_result(result)["status"], "PENDING EVIDENCE")

    def test_process_not_launched_is_environment_blocked(self):
        result = good_result(launched=False, exit_code=None, test_summary=None)
        self.assertEqual(classify_pytest_result(result)["status"], "ENV_BLOCKED")

    def test_dependency_failure_is_environment_blocked(self):
        result = good_result(error_code="DEPENDENCY_INSTALL_FAILED")
        self.assertEqual(classify_pytest_result(result)["status"], "ENV_BLOCKED")

    def test_isolation_failure_is_policy_blocked(self):
        result = good_result(error_code="ISOLATION_UNAVAILABLE")
        self.assertEqual(classify_pytest_result(result)["status"], "POLICY_BLOCKED")

    def test_timeout_is_not_pass(self):
        result = good_result(status="TIMEOUT", timed_out=True)
        self.assertEqual(classify_pytest_result(result)["status"], "TIMEOUT")

    def test_failure_is_test_failed(self):
        result = good_result(exit_code=1, test_summary={
            "collected": 3, "passed": 2, "failed": 1, "skipped": 0, "errors": 0
        })
        self.assertEqual(classify_pytest_result(result)["status"], "TEST_FAILED")

    def test_unapproved_skip_is_not_pass(self):
        result = good_result(test_summary={
            "collected": 3, "passed": 2, "failed": 0, "skipped": 1, "errors": 0
        })
        self.assertEqual(classify_pytest_result(result)["status"], "TEST_FAILED")

    def test_explicitly_allowed_skip_can_pass(self):
        result = good_result(test_summary={
            "collected": 3, "passed": 2, "failed": 0, "skipped": 1, "errors": 0
        })
        self.assertEqual(classify_pytest_result(result, allowed_skips=1)["status"], "PASS")

    def test_all_skipped_is_not_pass_even_if_policy_allows_skips(self):
        result = good_result(test_summary={
            "collected": 3, "passed": 0, "failed": 0, "skipped": 3, "errors": 0
        })
        self.assertEqual(
            classify_pytest_result(result, allowed_skips=3)["status"],
            "TEST_FAILED",
        )

    def test_inconsistent_counts_are_pending_evidence(self):
        result = good_result(test_summary={
            "collected": 3, "passed": 2, "failed": 0, "skipped": 0, "errors": 0
        })
        self.assertEqual(classify_pytest_result(result)["status"], "PENDING EVIDENCE")

    def test_invalid_allowed_skip_policy_fails_closed(self):
        self.assertEqual(
            classify_pytest_result(good_result(), allowed_skips=-1)["status"],
            "POLICY_BLOCKED",
        )


if __name__ == "__main__":
    unittest.main()
