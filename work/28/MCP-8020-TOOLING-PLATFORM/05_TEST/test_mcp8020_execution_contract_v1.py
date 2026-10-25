"""Offline contract tests; they do not exercise Core or the Windows runtime."""
from __future__ import annotations

import unittest

from mcp8020_execution_contract_v1 import (
    ExecutionContractError,
    result_is_verified_pass,
    validate_python_run_request,
)


HASH = "a" * 64


class ExecutionContractV1Tests(unittest.TestCase):
    def valid_request(self):
        return {
            "work_id": "work28",
            "entry_path": "04_CODE/smoke.py",
            "operation": "RUN_SCRIPT",
            "expected_source_sha256": HASH,
        }

    def test_normalizes_work_relative_path_and_defaults_timeout(self):
        req = self.valid_request()
        req["entry_path"] = r"04_CODE\smoke.py"
        out = validate_python_run_request(req)
        self.assertEqual(out["entry_path"], "04_CODE/smoke.py")
        self.assertEqual(out["timeout_seconds"], 30)

    def test_rejects_inline_script_and_identity_fields(self):
        for field in ("script", "identity_id", "authorized", "cwd", "env", "argv"):
            with self.subTest(field=field):
                req = self.valid_request()
                req[field] = "untrusted"
                with self.assertRaises(ExecutionContractError):
                    validate_python_run_request(req)

    def test_rejects_traversal_absolute_drive_and_ambiguous_paths(self):
        for path in ("../secret.py", "/tmp/a.py", r"C:\temp\a.py",
                     "a/../b.py", "folder./x.py", "folder /x.py", "a//b.py", "a\nb.py", "a\x7fb.py"):
            with self.subTest(path=path):
                req = self.valid_request()
                req["entry_path"] = path
                with self.assertRaises(ExecutionContractError):
                    validate_python_run_request(req)

    def test_rejects_bad_hash_operation_and_timeout(self):
        cases = [
            ("expected_source_sha256", "A" * 64),
            ("expected_source_sha256", "z" * 64),
            ("operation", "RUN_COMMAND"),
            ("operation", []),
            ("timeout_seconds", True),
            ("timeout_seconds", 0),
            ("timeout_seconds", 301),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                req = self.valid_request()
                req[field] = value
                with self.assertRaises(ExecutionContractError):
                    validate_python_run_request(req)

    def test_accepts_only_complete_hash_bound_script_pass(self):
        result = {
            "status": "PASS", "exit_code": 0, "source_sha256": HASH,
            "request_id": "req-1", "run_id": "run-1", "work_id": "work28",
            "runtime_identity": "w13-build-a", "evidence_ref": "evidence://run-1",
        }
        self.assertTrue(result_is_verified_pass(result, HASH, "RUN_SCRIPT", "work28"))
        self.assertFalse(result_is_verified_pass(result, "b" * 64, "RUN_SCRIPT", "work28"))
        for field in ("request_id", "run_id", "work_id", "runtime_identity", "evidence_ref"):
            changed = dict(result)
            changed[field] = ""
            with self.subTest(field=field):
                self.assertFalse(result_is_verified_pass(changed, HASH, "RUN_SCRIPT", "work28"))
        changed = dict(result)
        changed["exit_code"] = True
        self.assertFalse(result_is_verified_pass(changed, HASH, "RUN_SCRIPT", "work28"))
        changed = dict(result)
        changed["exit_code"] = 0.0
        self.assertFalse(result_is_verified_pass(changed, HASH, "RUN_SCRIPT", "work28"))
        self.assertFalse(result_is_verified_pass(result, HASH, "RUN_SCRIPT", "work999"))
        self.assertFalse(result_is_verified_pass(result, "not-a-hash", "RUN_SCRIPT", "work28"))

    def test_test_run_requires_nonzero_test_count_and_no_failures(self):
        result = {
            "status": "PASS", "exit_code": 0, "source_sha256": HASH,
            "request_id": "req-1", "run_id": "run-1", "work_id": "work28",
            "runtime_identity": "w13-build-a", "evidence_ref": "evidence://run-1",
            "test_summary": {"total": 2, "failed": 0, "errors": 0},
        }
        self.assertTrue(result_is_verified_pass(result, HASH, "RUN_TESTS", "work28"))
        for summary in (
            {"total": 0, "failed": 0, "errors": 0},
            {"total": 2, "failed": 1, "errors": 0},
            {"total": 2, "failed": 0, "errors": 1},
            {"total": True, "failed": 0, "errors": 0},
            {"total": 2},
        ):
            changed = dict(result, test_summary=summary)
            with self.subTest(summary=summary):
                self.assertFalse(result_is_verified_pass(changed, HASH, "RUN_TESTS", "work28"))
        missing = dict(result)
        del missing["test_summary"]
        self.assertFalse(result_is_verified_pass(missing, HASH, "RUN_TESTS", "work28"))


    def test_execution_contract_is_not_accidentally_live_in_legacy_catalog(self):
        # The candidate contract intentionally differs from v54's legacy
        # script/command schema. Do not activate execution tools by merely
        # injecting a gateway; an explicit reviewed migration is required.
        from mcp8020_catalog_v54 import TOOL_SPECS, NOT_IMPLEMENTED

        by_name = {spec.name: spec for spec in TOOL_SPECS}
        execution_names = (
            "sandbox_run_python", "sandbox_run_command",
            "sandbox_get_execution_status", "sandbox_get_execution_result",
            "sandbox_collect_artifact", "sandbox_generate_evidence",
            "sandbox_create_handoff",
        )
        for name in execution_names:
            with self.subTest(tool=name):
                self.assertEqual(by_name[name].status, NOT_IMPLEMENTED)
        legacy = by_name["sandbox_run_python"].input_schema["properties"]
        self.assertIn("script", legacy)
        self.assertNotIn("entry_path", legacy)
        self.assertNotIn("expected_source_sha256", legacy)


if __name__ == "__main__":
    unittest.main()
