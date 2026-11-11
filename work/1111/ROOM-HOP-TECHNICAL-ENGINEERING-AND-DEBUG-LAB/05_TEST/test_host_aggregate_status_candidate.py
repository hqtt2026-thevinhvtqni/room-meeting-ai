"""Candidate regression tests for Work 1111 aggregate test-status fix.

These tests are intentionally staged, not executed. They must be moved into
the canonical test suite and run against the exact source SHA after Core/Host
authorization and runtime prerequisites are resolved.
"""
import json
import sys
from pathlib import Path

from execution_host import ExecutionHost, ExecutionRequest, WorkContext


def make_context(tmp_path: Path, *, test_entrypoint=None) -> WorkContext:
    root = tmp_path
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(exist_ok=True)
    evidence.mkdir(exist_ok=True)
    return WorkContext(
        work_id="W1111",
        work_name="ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB",
        workspace_root=str(root),
        execution_workspace=str(workspace),
        evidence_root=str(evidence),
        authorized=True,  # test fixture only; not a production auth proof
        execution_id="w1111-aggregate-status-regression",
        test_entrypoint=test_entrypoint,
    )


def test_nested_test_failure_must_fail_overall_result(tmp_path):
    ctx = make_context(
        tmp_path,
        test_entrypoint=(
            sys.executable,
            "-c",
            "raise SystemExit(7)",
        ),
    )
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(
            command=(sys.executable, "-c", "print('primary-pass')"),
            run_test=True,
        ),
    )
    assert result.status == "FAILED"
    assert result.exit_code == 7
    final = json.loads(Path(result.evidence_ref).read_text(encoding="utf-8"))
    assert final["primary_command_status"] == "PASS"
    assert final["primary_command_exit_code"] == 0
    assert final["test"]["status"] == "FAILED"
    assert final["stdout_ref"] != final["test"]["stdout_ref"]
    assert Path(final["stdout_ref"]).read_text(encoding="utf-8").strip() == "primary-pass"


def test_missing_test_entrypoint_must_block_overall_result(tmp_path):
    ctx = make_context(tmp_path, test_entrypoint=None)
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(
            command=(sys.executable, "-c", "print('primary-pass')"),
            run_test=True,
        ),
    )
    assert result.status == "BLOCKED"
    final = json.loads(Path(result.evidence_ref).read_text(encoding="utf-8"))
    assert final["test"]["status"] == "BLOCKED"
    assert final["blocker"] == "test_entrypoint_not_bound"


def test_primary_command_failure_cannot_be_overwritten_by_test_pass(tmp_path):
    ctx = make_context(
        tmp_path,
        test_entrypoint=(
            sys.executable,
            "-c",
            "print('test-pass')",
        ),
    )
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(
            command=(sys.executable, "-c", "raise SystemExit(5)"),
            run_test=True,
        ),
    )
    assert result.status == "FAILED"
    assert result.exit_code == 5
