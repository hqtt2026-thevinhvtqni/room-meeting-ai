"""Fail-closed classifier for structured Python/pytest execution results.

No process execution happens here. Input must be a structured result returned
by the authorized execution host and its pytest-report adapter.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

ENVIRONMENT_ERROR_CODES = {
    "PYTHON_NOT_FOUND",
    "PYTEST_NOT_FOUND",
    "DEPENDENCY_INSTALL_FAILED",
    "VENV_CREATE_FAILED",
    "RUNTIME_UNAVAILABLE",
    "HOST_UNREACHABLE",
}
POLICY_ERROR_CODES = {
    "POLICY_DENIED",
    "DENIED",
    "WORKSPACE_ESCAPE",
    "AUTHORIZATION_FAILED",
    "ISOLATION_UNAVAILABLE",
}


def _non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def classify_pytest_result(
    result: Mapping[str, Any],
    *,
    allowed_skips: int = 0,
) -> dict[str, str | int | None]:
    """Return a conservative status/reason pair.

    PASS requires a launched process, exit code 0, a structured summary with
    at least one collected and at least one passed test, and no failures/errors
    or unapproved skips. A runtime's own PASS label is never sufficient.
    """
    if not isinstance(result, Mapping):
        return {"status": "PENDING EVIDENCE", "reason": "invalid_result_shape"}
    if not _non_negative_int(allowed_skips):
        return {"status": "POLICY_BLOCKED", "reason": "invalid_allowed_skips"}

    error_code = result.get("error_code")
    if isinstance(error_code, str) and error_code in POLICY_ERROR_CODES:
        return {"status": "POLICY_BLOCKED", "reason": error_code}
    if isinstance(error_code, str) and error_code in ENVIRONMENT_ERROR_CODES:
        return {"status": "ENV_BLOCKED", "reason": error_code}

    status = str(result.get("status", "")).upper()
    if status in {"DENIED", "POLICY_BLOCKED"}:
        return {"status": "POLICY_BLOCKED", "reason": "execution_denied"}
    if status == "TIMEOUT" or result.get("timed_out") is True:
        return {"status": "TIMEOUT", "reason": "execution_timeout"}

    if result.get("launched") is not True:
        return {"status": "ENV_BLOCKED", "reason": "process_not_launched"}

    exit_code = result.get("exit_code")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        return {"status": "PENDING EVIDENCE", "reason": "missing_or_invalid_exit_code"}

    summary = result.get("test_summary")
    if not isinstance(summary, Mapping):
        return {"status": "PENDING EVIDENCE", "reason": "missing_structured_test_summary"}

    collected = summary.get("collected")
    passed = summary.get("passed")
    failed = summary.get("failed")
    skipped = summary.get("skipped")
    errors = summary.get("errors", 0)

    if not all(_non_negative_int(v) for v in (collected, passed, failed, skipped, errors)):
        return {"status": "PENDING EVIDENCE", "reason": "invalid_or_missing_test_counts"}

    if collected == 0 or exit_code == 5:
        return {"status": "COLLECTION_FAILED", "reason": "zero_tests_collected"}
    if failed > 0 or errors > 0:
        return {"status": "TEST_FAILED", "reason": "test_failures_or_errors"}
    if skipped > allowed_skips:
        return {"status": "TEST_FAILED", "reason": "unapproved_skipped_tests"}
    if exit_code != 0:
        return {"status": "TEST_FAILED", "reason": "nonzero_exit_code"}
    if passed == 0:
        return {"status": "TEST_FAILED", "reason": "no_tests_passed"}
    if passed + skipped != collected:
        return {"status": "PENDING EVIDENCE", "reason": "inconsistent_test_counts"}

    return {
        "status": "PASS",
        "reason": "tests_collected_and_passed",
        "collected": collected,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "exit_code": exit_code,
    }
