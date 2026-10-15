"""WORK 28 - tests for the WP6 contract runner logic.

These tests exercise the pure decision/parsing logic of
run_work28_contract_runner.py only. They do NOT execute the canonical
command, spawn processes, or write evidence; live-run evidence must come
from an approved runner per the Work 28 test plan.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "04_CODE"))

import run_work28_contract_runner as runner  # noqa: E402


class ParseUnittestOutputTests(unittest.TestCase):
    def test_ok_run(self):
        text = "test_x (05_TEST.test_a.A) ... ok\n\n" \
               "----------------------------------------------------------------------\n" \
               "Ran 1 test in 0.001s\n\nOK\n"
        parsed = runner.parse_unittest_output(text)
        self.assertEqual(parsed["tests_run"], 1)
        self.assertEqual(parsed["failures"], 0)
        self.assertEqual(parsed["errors"], 0)
        self.assertTrue(parsed["ok_line_found"])

    def test_failed_with_counters(self):
        text = "Ran 3 tests in 0.01s\n\nFAILED (failures=1, errors=2, skipped=1)\n"
        parsed = runner.parse_unittest_output(text)
        self.assertEqual(parsed["tests_run"], 3)
        self.assertEqual(parsed["failures"], 1)
        self.assertEqual(parsed["errors"], 2)
        self.assertEqual(parsed["skipped"], 1)
        self.assertTrue(parsed["failed_line_found"])

    def test_failed_without_counters_counts_as_at_least_one_failure(self):
        parsed = runner.parse_unittest_output("Ran 2 tests in 0.1s\n\nFAILED\n")
        self.assertEqual(parsed["tests_run"], 2)
        self.assertGreaterEqual(parsed["failures"], 1)

    def test_zero_tests(self):
        parsed = runner.parse_unittest_output("Ran 0 tests in 0.000s\n\nOK\n")
        self.assertEqual(parsed["tests_run"], 0)

    def test_empty_output_never_crashes(self):
        parsed = runner.parse_unittest_output("")
        self.assertEqual(parsed["tests_run"], 0)
        self.assertIsNone(parsed["parse_error"])


class DecideStatusTests(unittest.TestCase):
    def test_pass_requires_exit_zero_and_tests(self):
        parsed = {"tests_run": 5, "failures": 0, "errors": 0, "skipped": 0}
        self.assertEqual(runner.decide_status(0, parsed), runner.PASS)

    def test_zero_tests_green_process_is_failure(self):
        parsed = {"tests_run": 0, "failures": 0, "errors": 0, "skipped": 0}
        self.assertEqual(runner.decide_status(0, parsed), runner.FAIL)

    def test_nonzero_exit_is_failure(self):
        parsed = {"tests_run": 5, "failures": 0, "errors": 0, "skipped": 0}
        self.assertEqual(runner.decide_status(1, parsed), runner.FAIL)

    def test_failures_present_is_failure_even_with_exit_zero(self):
        parsed = {"tests_run": 5, "failures": 2, "errors": 0, "skipped": 0}
        self.assertEqual(runner.decide_status(0, parsed), runner.FAIL)

    def test_timeout_is_blocked_never_pass(self):
        parsed = {"tests_run": 5, "failures": 0, "errors": 0, "skipped": 0}
        self.assertEqual(runner.decide_status(0, parsed, timeout_hit=True), runner.BLOCKED)

    def test_parse_error_is_blocked(self):
        parsed = {"tests_run": 5, "failures": 0, "errors": 0, "skipped": 0, "parse_error": "x"}
        self.assertEqual(runner.decide_status(0, parsed), runner.BLOCKED)


class SafetyTests(unittest.TestCase):
    def test_safe_join_rejects_traversal(self):
        with self.assertRaises(ValueError):
            runner._safe_join("/tmp/root", "..", "escape")

    def test_safe_join_rejects_absolute(self):
        with self.assertRaises(ValueError):
            runner._safe_join("/tmp/root", "/etc")

    def test_safe_join_allows_relative(self):
        joined = runner._safe_join("/tmp/root", "06_EVIDENCE")
        self.assertEqual(joined, os.path.join("/tmp/root", "06_EVIDENCE"))

    def test_request_id_ascii_and_prefixed(self):
        rid = runner.new_request_id()
        self.assertTrue(rid.startswith("W28-RUN-"))
        self.assertTrue(all(32 <= ord(c) < 127 for c in rid))

    def test_sha256_shape(self):
        h = runner.sha256_text("abc")
        self.assertEqual(len(h), 64)
        int(h, 16)  # must be hex


class VerdictTests(unittest.TestCase):
    def test_zero_tests_verdict_mentions_zero_tests(self):
        v = runner.summarize_verdict(runner.FAIL, 0, {"tests_run": 0, "failures": 0, "errors": 0})
        self.assertIn("zero tests", v)


if __name__ == "__main__":
    unittest.main()