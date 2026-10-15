"""CLA proposed regression tests (RED against contract 1.1.0).

Proposal only; NOT placed in 05_TEST. Each test asserts the SECURE behaviour required by
PROPOSED_EXECUTION_TOOL_CONTRACT_V1 / E2E blueprint. A failing test = open finding.
Run from the Work 28 root:  python -m unittest cla_red_tests -v
(copy this file to the Work 28 root under the name cla_red_tests.py to run it)

Executed by Cla on 2026-10-12 in Cla's own container (NOT canonical runtime) against a verbatim
copy of 04_CODE/tool_contracts.py (sha256 of the copy: 25b1e6856929f8a849346842daaaa23ade11242537d68a23006504ea4df90f3b):
    exit=1, Ran 15 tests, FAILED (failures=24, errors=1); 15 of 15 tests not passing.
Ka's own suite on the same copy: python -m unittest discover -s 05_TEST -t .  -> exit=0, Ran 17 tests, OK.
Checksum of the runnable file (sha256): 892c2b507cc34c5d1cb4cd1ac42da9b14083d7fab8fb7b981613b0252a59ef09
"""
import importlib, json, subprocess, unittest

c = importlib.import_module("04_CODE.tool_contracts")
TR, TS, OK, EO = c.ToolResult, c.ToolStatus, c.OperationKind, c.ExecutionOperation
V = c.validate_relative_work_path
GOOD = dict(operation_kind=OK.EXECUTION, execution_operation=EO.RUN_TESTS,
            run_id="run-" + "0" * 32, exit_code=0, evidence_ref="evidence/run/FINAL.json", source_sha256="a" * 64)
FULL = {"tests_run": 3, "failures": 0, "errors": 0, "skipped": 0}


class N01_ExecutionFieldsCannotBeMisdeclared(unittest.TestCase):
    def test_execution_operation_requires_execution_kind(self):
        with self.assertRaises(ValueError):
            TR("req-1", TS.PASS, "x", operation_kind=OK.DIAGNOSTIC, execution_operation=EO.RUN_TESTS)

    def test_execution_fields_rejected_on_non_execution_result(self):
        with self.assertRaises(ValueError):
            TR("req-1", TS.PASS, "x", operation_kind=OK.READ, run_id="run-" + "0" * 32, exit_code=0)


class N03_SummaryAndFieldStrictness(unittest.TestCase):
    def test_missing_failure_counters_is_not_pass(self):
        with self.assertRaises(ValueError):
            TR("req-1", TS.PASS, "x", test_summary={"tests_run": 3}, **GOOD)

    def test_all_tests_skipped_is_not_pass(self):
        with self.assertRaises(ValueError):
            TR("req-1", TS.PASS, "x", test_summary={"tests_run": 3, "failures": 0, "errors": 0, "skipped": 3}, **GOOD)

    def test_exit_code_must_be_real_int_zero(self):
        for bad in (False, 0.0):
            with self.subTest(exit_code=bad), self.assertRaises(ValueError):
                g = dict(GOOD, exit_code=bad)
                TR("req-1", TS.PASS, "x", test_summary=FULL, **g)

    def test_run_id_must_have_server_generated_shape(self):
        with self.assertRaises(ValueError):
            TR("req-1", TS.PASS, "x", test_summary=FULL, **dict(GOOD, run_id="x"))


class N05_Immutability(unittest.TestCase):
    def test_external_mutation_cannot_change_validated_summary(self):
        d = dict(FULL)
        r = TR("req-1", TS.PASS, "x", test_summary=d, **GOOD)
        d["tests_run"] = 0
        self.assertGreaterEqual(r.to_dict()["test_summary"]["tests_run"], 1)


class N04_ExceptionMapping(unittest.TestCase):
    def test_malformed_runtime_reply_is_not_caller_error(self):
        st = c.result_from_exception("req-1", json.JSONDecodeError("bad", "{", 0)).status
        self.assertIn(st, (TS.FAIL, TS.BLOCKED))

    def test_subprocess_timeout_maps_consistently_with_timeout_error(self):
        a = c.result_from_exception("req-1", TimeoutError("x")).status
        b = c.result_from_exception("req-2", subprocess.TimeoutExpired("cmd", 1)).status
        self.assertEqual(a, b)

    def test_error_path_never_raises_on_bad_request_id(self):
        c.result_from_exception("bad\nid", RuntimeError("x"))

    def test_evidence_check_failure_is_not_invalid_request(self):
        st = c.result_from_exception("req-1", ValueError("execution PASS missing authoritative evidence: run_id")).status
        self.assertNotEqual(st, TS.INVALID_REQUEST)


class N06_ValidatorResidual(unittest.TestCase):
    def test_more_secret_and_credential_names_protected(self):
        for p in (".env.local", ".envrc", ".git-credentials", ".npmrc", ".netrc", ".pypirc", "a/id_rsa", "a/credentials"):
            with self.subTest(path=p), self.assertRaises(ValueError):
                V(p)

    def test_line_paragraph_and_other_separators_rejected(self):
        for p in ("a\u2028b", "a\u2029b", "a\u1680b"):
            with self.subTest(path=p), self.assertRaises(ValueError):
                V(p)

    def test_mixed_script_homoglyph_rejected(self):
        with self.assertRaises(ValueError):
            V("\u0430dmin/x")

    def test_backslash_is_not_silently_rewritten(self):
        with self.assertRaises(ValueError):
            V("a\\b")


if __name__ == "__main__":
    unittest.main()
