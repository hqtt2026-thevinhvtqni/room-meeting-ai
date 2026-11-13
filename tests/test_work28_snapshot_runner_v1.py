import hashlib
from pathlib import Path

import pytest

from execution_host.work28_contract import SourceSnapshot, Work28ContractError
from execution_host.work28_snapshot_runner_v1 import run_snapshot


def make_snapshot(path: Path) -> SourceSnapshot:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return SourceSnapshot("W13", path.name, digest, f"sha256:{digest}:test/{path.name}", path)


def test_runner_uses_fixed_mapping_and_never_passes_arbitrary_argv(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('ok')\n", encoding="utf-8")
    result = run_snapshot(snapshot=make_snapshot(script), operation="RUN_SCRIPT", timeout_seconds=5)
    assert result.exit_code == 0
    assert result.stdout.strip() == "ok"
    # Process-tree cleanup is not yet independently verified by this staged seam.
    assert result.status == "BLOCKED"
    assert result.cleanup_verified is False


def test_runner_refuses_snapshot_changed_after_hash_check(tmp_path):
    script = tmp_path / "source.py"
    script.write_text("print('before')\n", encoding="utf-8")
    snapshot = make_snapshot(script)
    script.write_text("print('after')\n", encoding="utf-8")
    with pytest.raises(Work28ContractError, match="snapshot_changed_after_validation"):
        run_snapshot(snapshot=snapshot, operation="RUN_SCRIPT", timeout_seconds=5)


def test_runner_rejects_unsupported_operation(tmp_path):
    script = tmp_path / "source.py"
    script.write_text("print('ok')\n", encoding="utf-8")
    with pytest.raises(Work28ContractError, match="unsupported_operation"):
        run_snapshot(snapshot=make_snapshot(script), operation="RUN_COMMAND", timeout_seconds=5)


def test_runner_timeout_never_claims_pass_or_cleanup(tmp_path):
    script = tmp_path / "slow.py"
    script.write_text("import time\ntime.sleep(5)\n", encoding="utf-8")
    result = run_snapshot(snapshot=make_snapshot(script), operation="RUN_SCRIPT", timeout_seconds=1)
    assert result.status == "BLOCKED"
    assert result.timed_out is True
    assert result.cleanup_verified is False
