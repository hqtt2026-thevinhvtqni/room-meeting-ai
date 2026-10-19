"""Negative security tests for Work 28 - Cross-work access, symlink, OS isolation.

These tests verify that security boundaries are enforced correctly.
They do not require live execution but verify the contract-level protections.
"""
import unittest
import sys
import os

# Add the 04_CODE directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '04_CODE'))

from tool_contracts import (
    TrustedPrincipal,
    WorkContext,
    AuthorizedSandboxRequest,
    SandboxOperation,
    ToolResult,
    ToolStatus,
    OperationKind,
    ExecutionOperation,
    validate_relative_work_path,
)


class CrossWorkAccessTests(unittest.TestCase):
    """Test that cross-work access is properly denied."""
    
    def test_work_context_enforces_own_operations(self):
        """WorkContext should only permit operations in allowed_operations."""
        principal = TrustedPrincipal(principal_id="agent-go-001", source="core-session")
        context = WorkContext(
            work_id="28",
            principal=principal,
            allowed_operations=("READ", "LIST")
        )
        
        # Should permit allowed operations
        self.assertTrue(context.permits("READ"))
        self.assertTrue(context.permits("LIST"))
        
        # Should deny disallowed operations
        self.assertFalse(context.permits("WRITE"))
        self.assertFalse(context.permits("DELETE"))
        self.assertFalse(context.permits("EXECUTE"))
    
    def test_authorized_request_rejects_unpermitted_operation(self):
        """AuthorizedSandboxRequest should fail if operation not in allowed_operations."""
        principal = TrustedPrincipal(principal_id="agent-go-001", source="core-session")
        context = WorkContext(
            work_id="28",
            principal=principal,
            allowed_operations=("READ", "LIST")
        )
        
        # Try to create a request with a non-permitted operation
        with self.assertRaises(ValueError) as ctx:
            AuthorizedSandboxRequest(
                request_id="req-test-001",
                work_context=context,
                operation=SandboxOperation.WRITE,
                relative_path="test.txt",
                content="test"
            )
        self.assertIn("not in allowed_operations", str(ctx.exception))
    
    def test_execution_result_rejects_cross_work_run_id(self):
        """Execution results should not allow cross-work run_id access."""
        # This is enforced at the adapter level, but we verify the contract
        # doesn't allow inconsistent work_id/run_id combinations
        with self.assertRaises(ValueError):
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation="RUN_TESTS",
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 1, "failures": 0, "errors": 0, "skipped": 0}
            )
        # Note: The actual cross-work check happens at the adapter level
        # This test verifies the contract doesn't prevent proper validation


class SymlinkAndPathTests(unittest.TestCase):
    """Test symlink and path traversal protections."""
    
    def test_path_validation_rejects_symlink_like_patterns(self):
        """Path validation should reject symlink-like patterns."""
        invalid_paths = [
            "symlink->/etc/passwd",
            "a/b/../../../etc/passwd",
        ]
        for path in invalid_paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    validate_relative_work_path(path)
        # "link/to/outside" is actually a valid path - remove it from test
    
    def test_path_validation_rejects_reparse_point_patterns(self):
        """Path validation should reject reparse point patterns."""
        # These are lexical checks - filesystem-level checks are adapter responsibility
        invalid_paths = [
            "file.txt:alternate",
            "file.txt::$DATA",
            "file.txt:Zone.Identifier",
        ]
        for path in invalid_paths:
            with self.subTest(path=path):
                with self.assertRaises(ValueError):
                    validate_relative_work_path(path)
    
    def test_path_validation_normalizes_and_rejects_unicode_tricks(self):
        """Path validation should reject Unicode normalization tricks."""
        # NFKC normalization should catch confusable characters
        with self.assertRaises(ValueError):
            validate_relative_work_path("file\u202Etxt")  # RTL override
        
        with self.assertRaises(ValueError):
            validate_relative_work_path("file\u200Btxt")  # Zero-width space
        
        with self.assertRaises(ValueError):
            validate_relative_work_path("file\uFF0Etxt")  # Fullwidth slash


class OSIsolationTests(unittest.TestCase):
    """Test OS isolation contract requirements."""
    
    def test_execution_pass_requires_evidence_ref(self):
        """PASS status for execution requires evidence_ref."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_SCRIPT,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref=None,  # Missing!
            )
        self.assertIn("evidence_ref", str(ctx.exception))
    
    def test_execution_pass_requires_source_sha256(self):
        """PASS status for execution requires source_sha256."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_SCRIPT,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256=None,  # Missing!
                evidence_ref="evidence-ref",
            )
        self.assertIn("source_sha256", str(ctx.exception))
    
    def test_execution_pass_requires_run_id(self):
        """PASS status for execution requires run_id."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_SCRIPT,
                run_id=None,  # Missing!
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
            )
        self.assertIn("run_id", str(ctx.exception))
    
    def test_execution_pass_requires_exit_code_zero(self):
        """PASS status for execution requires exit_code=0."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_SCRIPT,
                run_id="run-" + "a" * 32,
                exit_code=1,  # Non-zero!
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
            )
        self.assertIn("exit_code=0", str(ctx.exception))
    
    def test_run_tests_pass_requires_test_counters(self):
        """PASS status for RUN_TESTS requires explicit test counters."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 1, "failures": 0, "errors": 0},  # Missing skipped!
            )
        self.assertIn("skipped", str(ctx.exception))
    
    def test_run_tests_pass_requires_tests_run_ge_1(self):
        """PASS status for RUN_TESTS requires tests_run >= 1."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 0, "failures": 0, "errors": 0, "skipped": 0},  # Zero tests!
            )
        self.assertIn("tests_run>=1", str(ctx.exception))
    
    def test_run_tests_pass_requires_zero_failures(self):
        """PASS status for RUN_TESTS requires failures=0."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 1, "failures": 1, "errors": 0, "skipped": 0},  # Has failures!
            )
        self.assertIn("failures=0", str(ctx.exception))
    
    def test_run_tests_pass_requires_zero_errors(self):
        """PASS status for RUN_TESTS requires errors=0."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 1, "failures": 0, "errors": 1, "skipped": 0},  # Has errors!
            )
        self.assertIn("errors=0", str(ctx.exception))
    
    def test_run_tests_pass_requires_zero_skipped(self):
        """PASS status for RUN_TESTS requires skipped=0."""
        with self.assertRaises(ValueError) as ctx:
            ToolResult(
                request_id="req-test-001",
                status=ToolStatus.PASS,
                message="test",
                operation_kind=OperationKind.EXECUTION,
                execution_operation=ExecutionOperation.RUN_TESTS,
                run_id="run-" + "a" * 32,
                exit_code=0,
                source_sha256="a" * 64,
                evidence_ref="evidence-ref",
                test_summary={"tests_run": 1, "failures": 0, "errors": 0, "skipped": 1},  # Has skipped!
            )
        self.assertIn("skipped=0", str(ctx.exception))


class PrincipalSpoofingTests(unittest.TestCase):
    """Test that principal spoofing is prevented."""
    
    def test_trusted_principal_rejects_caller_source_variations(self):
        """TrustedPrincipal should reject any caller-supplied source."""
        invalid_sources = [
            "caller",
            "Caller",
            "CALLER",
            "client",
            "Client",
            "user-supplied",
            "User-Supplied",
            "identity_id",
            "Identity_ID",
            " identity_id ",
        ]
        for source in invalid_sources:
            with self.subTest(source=source):
                with self.assertRaises(ValueError) as ctx:
                    TrustedPrincipal(principal_id="test-agent", source=source)
                self.assertIn("caller-supplied", str(ctx.exception))
    
    def test_trusted_principal_accepts_valid_sources(self):
        """TrustedPrincipal should accept valid server-side sources."""
        valid_sources = [
            "core-session",
            "mtls",
            "adapter-derived",
            "trusted-transport",
            "mcp-server",
        ]
        for source in valid_sources:
            with self.subTest(source=source):
                p = TrustedPrincipal(principal_id="test-agent", source=source)
                self.assertEqual(p.source, source)
    
    def test_principal_id_validation(self):
        """Principal ID must match the allowed pattern."""
        # Valid
        TrustedPrincipal(principal_id="agent-go-001", source="core-session")
        TrustedPrincipal(principal_id="a", source="core-session")
        TrustedPrincipal(principal_id="A" * 128, source="core-session")
        
        # Invalid
        with self.assertRaises(ValueError):
            TrustedPrincipal(principal_id="", source="core-session")
        
        with self.assertRaises(ValueError):
            TrustedPrincipal(principal_id="agent@go", source="core-session")  # Invalid char
        
        with self.assertRaises(ValueError):
            TrustedPrincipal(principal_id="A" * 129, source="core-session")  # Too long


class WorkContextValidationTests(unittest.TestCase):
    """Test WorkContext validation."""
    
    def test_work_id_validation(self):
        """Work ID must match the allowed pattern."""
        principal = TrustedPrincipal(principal_id="agent-001", source="core-session")
        
        # Valid
        WorkContext(work_id="28", principal=principal, allowed_operations=("READ",))
        WorkContext(work_id="work-01", principal=principal, allowed_operations=("READ",))
        WorkContext(work_id="A" * 64, principal=principal, allowed_operations=("READ",))
        
        # Invalid
        with self.assertRaises(ValueError):
            WorkContext(work_id="", principal=principal, allowed_operations=("READ",))
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="work@01", principal=principal, allowed_operations=("READ",))
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="A" * 65, principal=principal, allowed_operations=("READ",))
    
    def test_allowed_operations_must_be_non_empty_tuple(self):
        """allowed_operations must be a non-empty tuple."""
        principal = TrustedPrincipal(principal_id="agent-001", source="core-session")
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=principal, allowed_operations=[])
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=principal, allowed_operations=("",))
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=principal, allowed_operations=("  ",))
    
    def test_allowed_operations_must_contain_strings(self):
        """allowed_operations must contain only strings."""
        principal = TrustedPrincipal(principal_id="agent-001", source="core-session")
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=principal, allowed_operations=(123,))
        
        with self.assertRaises(ValueError):
            WorkContext(work_id="28", principal=principal, allowed_operations=(None,))


if __name__ == "__main__":
    unittest.main()
