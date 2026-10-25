"""Regression tests for Work 28 pure contracts (v1.3.0).

Canonical command from the Work 28 root:
    python -m unittest discover -s 05_TEST -t . -v

These tests do not prove Core authorization, OS isolation, or live E2E.
Cover: Trust Boundary, Authorization fail-closed, Path security, Resource limits.
"""
import importlib
import math
import sys
import unittest
from pathlib import Path
from types import MappingProxyType

# Resolve imports from the canonical Work 28 platform root regardless of cwd.
# This keeps pytest collection reliable when invoked from the repository root.
_PLATFORM_ROOT = Path(__file__).resolve().parents[1]
if str(_PLATFORM_ROOT) not in sys.path:
    sys.path.insert(0, str(_PLATFORM_ROOT))

_c = importlib.import_module("04_CODE.tool_contracts")
ToolResult = _c.ToolResult
ToolStatus = _c.ToolStatus
OperationKind = _c.OperationKind
ExecutionOperation = _c.ExecutionOperation
SandboxOperation = _c.SandboxOperation
TrustedPrincipal = _c.TrustedPrincipal
WorkContext = _c.WorkContext
AuthorizedSandboxRequest = _c.AuthorizedSandboxRequest
bounded_limit = _c.bounded_limit
normalize_status = _c.normalize_status
new_request_id = _c.new_request_id
new_run_id = _c.new_run_id
result_from_exception = _c.result_from_exception
validate_relative_work_path = _c.validate_relative_work_path
validate_request_id = _c.validate_request_id
validate_run_id = _c.validate_run_id
validate_sha256 = _c.validate_sha256
CONTRACT_VERSION = _c.CONTRACT_VERSION
DEFAULT_MAX_READ_BYTES = _c.DEFAULT_MAX_READ_BYTES
DEFAULT_MAX_WRITE_BYTES = _c.DEFAULT_MAX_WRITE_BYTES
DEFAULT_MAX_LIST_ENTRIES = _c.DEFAULT_MAX_LIST_ENTRIES
DEFAULT_MAX_APPEND_BYTES = _c.DEFAULT_MAX_APPEND_BYTES


def _valid_principal():
    return TrustedPrincipal(principal_id="agent-go-001", source="core-session")


def _valid_context(ops=("READ", "LIST", "CREATE", "WRITE", "APPEND", "DELETE")):
    return WorkContext(work_id="28", principal=_valid_principal(), allowed_operations=ops)


class ContractValidationTests(unittest.TestCase):
    def test_contract_version_is_1_3_0(self):
        self.assertEqual(CONTRACT_VERSION, "1.3.0")

    # ----- Path security (existing + expanded) -----
    def test_valid_relative_paths(self):
        self.assertEqual(validate_relative_work_path("03_ARCHITECTURE/plan.md"), "03_ARCHITECTURE/plan.md")
        self.assertEqual(validate_relative_work_path("tài_liệu/biên_bản.md"), "tài_liệu/biên_bản.md")

    def test_rejects_traversal_absolute_unc_and_ads(self):
        paths = ("../secret", "a/../../secret", "/etc/passwd", r"C:\secret", r"C:secret",
                 r"\\server\share", "file.txt:secret", "file.txt::$DATA", r"..\x",
                 "a//b", "a/./b", ".", "")
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_relative_work_path(path)

    def test_rejects_unicode_confusables_and_format_chars(self):
        for path in ("．．／secret", "a\u202eb", "a\u200bb", "a\u0085b", "a\x7fb", "a\uff0fb",
                     "a\u2028b", "a\u2029b", "a\u1680b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_relative_work_path(path)

    def test_rejects_literal_backslash(self):
        with self.assertRaises(ValueError):
            validate_relative_work_path("dir\\file.md")

    def test_rejects_windows_reserved_and_ambiguous_names(self):
        paths = ("CON", "NUL.txt", "COM1", "LPT9.log", "file.txt.", "file.txt ", ".../x",
                 "~/.ssh", "%USERPROFILE%/x", "$HOME/x", "a/*", "a/?", "-option",
                 ".git/config", ".env", ".env.local", ".envrc", ".git-credentials",
                 ".npmrc", ".netrc", ".pypirc", "id_rsa", "credentials", "desktop.ini")
        for path in paths:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_relative_work_path(path)

    def test_rejects_oversized_and_untrimmed_paths(self):
        with self.assertRaises(ValueError):
            validate_relative_work_path("x" * 1025)
        for path in (" x", "x "):
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_relative_work_path(path)

    # ----- Trust Boundary -----
    def test_trusted_principal_rejects_caller_source(self):
        for src in ("caller", "client", "user-supplied", "identity_id", "Caller", "CLIENT"):
            with self.subTest(src=src), self.assertRaisesRegex(ValueError, "must not be caller-supplied"):
                TrustedPrincipal(principal_id="p1", source=src)

    def test_trusted_principal_accepts_server_source(self):
        p = TrustedPrincipal(principal_id="agent-go-001", source="core-session")
        self.assertEqual(p.principal_id, "agent-go-001")
        self.assertEqual(p.source, "core-session")

    def test_trusted_principal_rejects_bad_id(self):
        with self.assertRaises(ValueError):
            TrustedPrincipal(principal_id="", source="core-session")
        with self.assertRaises(ValueError):
            TrustedPrincipal(principal_id="a b", source="core-session")

    def test_work_context_requires_principal_and_ops(self):
        p = _valid_principal()
        ctx = WorkContext(work_id="28", principal=p, allowed_operations=("READ", "LIST"))
        self.assertTrue(ctx.permits("READ"))
        self.assertFalse(ctx.permits("DELETE"))
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=p, allowed_operations=())
        with self.assertRaises(ValueError):
            WorkContext(work_id="", principal=p, allowed_operations=("READ",))

    # ----- Authorization fail-closed -----
    def test_auth_request_rejects_missing_operation_permission(self):
        ctx = _valid_context(ops=("READ", "LIST"))
        with self.assertRaisesRegex(ValueError, "not in allowed_operations"):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=SandboxOperation.DELETE, relative_path="file.md",
            )

    def test_auth_request_rejects_missing_path_for_non_list(self):
        ctx = _valid_context()
        with self.assertRaisesRegex(ValueError, "relative_path is required"):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx, operation=SandboxOperation.READ,
            )

    def test_auth_request_rejects_missing_content_for_write(self):
        ctx = _valid_context()
        with self.assertRaisesRegex(ValueError, "content is required"):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=SandboxOperation.WRITE, relative_path="file.md",
            )

    def test_auth_request_accepts_valid_read(self):
        ctx = _valid_context()
        req = AuthorizedSandboxRequest(
            request_id="req-1", work_context=ctx,
            operation=SandboxOperation.READ, relative_path="06_EVIDENCE/note.md",
        )
        self.assertEqual(req.operation, SandboxOperation.READ)
        self.assertEqual(req.relative_path, "06_EVIDENCE/note.md")

    def test_auth_request_rejects_traversal_path(self):
        ctx = _valid_context()
        with self.assertRaises(ValueError):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=SandboxOperation.READ, relative_path="../secret",
            )

    # ----- Resource limits -----
    def test_resource_limits_defaults(self):
        ctx = _valid_context()
        req = AuthorizedSandboxRequest(
            request_id="req-1", work_context=ctx,
            operation=SandboxOperation.LIST,
        )
        self.assertEqual(req.max_read_bytes, DEFAULT_MAX_READ_BYTES)
        self.assertEqual(req.max_list_entries, DEFAULT_MAX_LIST_ENTRIES)
        self.assertEqual(req.max_write_bytes, DEFAULT_MAX_WRITE_BYTES)
        self.assertEqual(req.max_append_bytes, DEFAULT_MAX_APPEND_BYTES)

    def test_write_content_exceeds_limit(self):
        ctx = _valid_context()
        big = "x" * (DEFAULT_MAX_WRITE_BYTES + 1)
        with self.assertRaisesRegex(ValueError, "exceeds max_write_bytes"):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=SandboxOperation.WRITE, relative_path="big.md",
                content=big, max_write_bytes=DEFAULT_MAX_WRITE_BYTES,
            )

    def test_append_content_exceeds_limit(self):
        ctx = _valid_context()
        big = "y" * (DEFAULT_MAX_APPEND_BYTES + 1)
        with self.assertRaisesRegex(ValueError, "exceeds max_append_bytes"):
            AuthorizedSandboxRequest(
                request_id="req-1", work_context=ctx,
                operation=SandboxOperation.APPEND, relative_path="log.md",
                content=big, max_append_bytes=DEFAULT_MAX_APPEND_BYTES,
            )

    def test_bounded_limit_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            bounded_limit(0)
        with self.assertRaises(ValueError):
            bounded_limit(99999999, maximum=1000)
        with self.assertRaises(ValueError):
            bounded_limit(True)

    # ----- Existing execution / result tests (preserved) -----
    def test_request_and_run_ids_are_server_generated_shape(self):
        request_id, run_id = new_request_id(), new_run_id()
        self.assertTrue(request_id.startswith("req-"))
        self.assertTrue(run_id.startswith("run-"))
        self.assertEqual(validate_run_id(run_id), run_id)

    def test_sha256_must_be_lowercase_hex(self):
        self.assertEqual(validate_sha256("a" * 64), "a" * 64)
        with self.assertRaises(ValueError):
            validate_sha256("A" * 64)

    def test_status_lifecycle_does_not_collapse_to_fail(self):
        self.assertEqual(normalize_status("QUEUED"), ToolStatus.QUEUED)
        self.assertEqual(normalize_status("success-ish"), ToolStatus.FAIL)

    def test_execution_must_declare_operation(self):
        with self.assertRaisesRegex(ValueError, "identify RUN_SCRIPT or RUN_TESTS"):
            ToolResult("req-1", ToolStatus.FAIL, "failed", operation_kind=OperationKind.EXECUTION)

    def test_execution_operation_only_with_execution(self):
        with self.assertRaisesRegex(ValueError, "only valid when operation_kind=EXECUTION"):
            ToolResult("req-1", ToolStatus.PASS, "ok",
                       operation_kind=OperationKind.READ,
                       execution_operation=ExecutionOperation.RUN_TESTS)

    def test_execution_fields_rejected_on_non_execution(self):
        with self.assertRaisesRegex(ValueError, "run_id is only valid"):
            ToolResult("req-1", ToolStatus.PASS, "ok", operation_kind=OperationKind.READ, run_id="run-1")

    def test_execution_pass_with_evidence_serializes_enums(self):
        result = ToolResult("req-1", ToolStatus.PASS, "tests passed",
                            evidence_ref="evidence/run-1/FINAL_RESULT.json",
                            operation_kind=OperationKind.EXECUTION,
                            execution_operation=ExecutionOperation.RUN_TESTS,
                            run_id="run-" + "a" * 32, exit_code=0, source_sha256="a" * 64,
                            test_summary={"tests_run": 3, "failures": 0, "errors": 0, "skipped": 0})
        payload = result.to_dict()
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["contract_version"], "1.3.0")
        import json
        json.dumps(payload)

    def test_test_summary_rejects_nan_and_non_string_keys(self):
        with self.assertRaisesRegex(ValueError, "NaN|Infinity"):
            ToolResult("req-1", ToolStatus.PASS, "bad",
                       evidence_ref="e", operation_kind=OperationKind.EXECUTION,
                       execution_operation=ExecutionOperation.RUN_TESTS,
                       run_id="run-" + "b" * 32, exit_code=0, source_sha256="b" * 64,
                       test_summary={"tests_run": 1, "failures": 0, "errors": 0, "skipped": 0,
                                     "score": float("nan")})
        with self.assertRaisesRegex(ValueError, "keys must be strings"):
            ToolResult("req-1", ToolStatus.PASS, "bad",
                       evidence_ref="e", operation_kind=OperationKind.EXECUTION,
                       execution_operation=ExecutionOperation.RUN_TESTS,
                       run_id="run-" + "c" * 32, exit_code=0, source_sha256="c" * 64,
                       test_summary={1: "bad", "tests_run": 1, "failures": 0, "errors": 0, "skipped": 0})

    def test_test_summary_deep_freeze_nested(self):
        nested = {"tests_run": 2, "failures": 0, "errors": 0, "skipped": 0,
                  "details": {"suite": "core", "cases": ["a", "b"]}}
        result = ToolResult("req-1", ToolStatus.PASS, "ok",
                            evidence_ref="e", operation_kind=OperationKind.EXECUTION,
                            execution_operation=ExecutionOperation.RUN_TESTS,
                            run_id="run-" + "d" * 32, exit_code=0, source_sha256="d" * 64,
                            test_summary=nested)
        with self.assertRaises(TypeError):
            result.test_summary["tests_run"] = 99  # type: ignore
        with self.assertRaises(TypeError):
            result.test_summary["details"]["suite"] = "x"  # type: ignore
        self.assertIsInstance(result.test_summary["details"]["cases"], tuple)

    def test_result_from_exception_does_not_leak(self):
        result = result_from_exception("req-1", PermissionError("C:/private/token=secret"))
        self.assertEqual(result.status, ToolStatus.NOT_FOUND)
        self.assertNotIn("private", result.message)

    def test_non_execution_results_remain_distinct(self):
        result = ToolResult("req-1", ToolStatus.BLOCKED, "adapter unavailable")
        self.assertEqual(result.to_dict()["status"], "BLOCKED")
        self.assertEqual(result.to_dict()["contract_version"], "1.3.0")


if __name__ == "__main__":
    unittest.main()
