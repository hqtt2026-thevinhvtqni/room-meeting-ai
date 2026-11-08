from __future__ import annotations

from pathlib import Path

import pytest

from execution_host import ExecutionHost, ExecutionRequest, WorkContext
from execution_host.security import HostError
from execution_host.source_snapshot import SourceSnapshotError, workspace_source_sha256


def make_context(tmp_path: Path, *, test_entrypoint=None) -> WorkContext:
    root = tmp_path / "work"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    return WorkContext(
        work_id="W28",
        work_name="W28",
        workspace_root=str(root),
        execution_workspace=str(workspace),
        evidence_root=str(evidence),
        authorized=True,
        execution_id="test-run",
        test_entrypoint=test_entrypoint,
    )


def test_workspace_snapshot_is_deterministic_and_content_sensitive(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    file = workspace / "test_sample.py"
    file.write_text("print('one')", encoding="utf-8")
    first = workspace_source_sha256(workspace)
    assert workspace_source_sha256(workspace) == first
    file.write_text("print('two')", encoding="utf-8")
    assert workspace_source_sha256(workspace) != first


def test_workspace_snapshot_rejects_symlink(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    target = tmp_path / "outside.txt"
    target.write_text("outside", encoding="utf-8")
    link = workspace / "escape.txt"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation unavailable on this runner")
    with pytest.raises(SourceSnapshotError, match="source_snapshot_symlink_rejected"):
        workspace_source_sha256(workspace)


def test_nested_test_failure_propagates_to_top_level(tmp_path):
    ctx = make_context(tmp_path, test_entrypoint=("python3", "-c", "raise SystemExit(7)"))
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(command=("python3", "-c", "print('build-ok')"), run_test=True),
    )
    assert result.status == "FAILED"
    assert result.evidence_ref
    payload = __import__("json").loads(Path(result.evidence_ref).read_text(encoding="utf-8"))
    assert payload["test"]["status"] == "FAILED"
    assert payload["status"] == "FAILED"


def test_missing_nested_test_entrypoint_blocks_overall_pass(tmp_path):
    ctx = make_context(tmp_path)
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(command=("python3", "-c", "print('build-ok')"), run_test=True),
    )
    assert result.status == "BLOCKED"
    assert result.blocker == "test_entrypoint_not_bound"


def test_primary_failure_is_not_overwritten_by_nested_test_pass(tmp_path):
    ctx = make_context(tmp_path, test_entrypoint=("python3", "-c", "print('test-ok')"))
    result = ExecutionHost().execute_work(
        ctx,
        ExecutionRequest(command=("python3", "-c", "raise SystemExit(5)"), run_test=True),
    )
    assert result.status == "FAILED"
