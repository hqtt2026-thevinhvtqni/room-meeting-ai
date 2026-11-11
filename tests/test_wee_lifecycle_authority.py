from __future__ import annotations

from pathlib import Path

from wee.controller import LifecycleController
from wee.models import EvidenceStore, WorkContext


class GrantedHostStub:
    def __init__(self, result):
        self.result = result
        self.called = 0

    def discover(self, context):
        return {"status": "PASS", "authority": "CORE_ONLINE"}

    def execute_authorized(self, context):
        self.called += 1
        assert context.work_id == "W32"
        assert context.assignment_id == "W32-EXECUTION-AUTHORITY"
        return dict(self.result)


def context(tmp_path):
    root = tmp_path / "root"
    workspace = root / "workspace"
    evidence = root / "evidence"
    workspace.mkdir(parents=True)
    evidence.mkdir()
    return WorkContext(
        work_id="W32",
        work_name="ROOM-HOP-WORK-32",
        repository="hqtt2026-thevinhvtqni/room-meeting-ai",
        repository_root=str(root),
        branch="work/32-core-owned-execution-authority-20261112",
        execution_workspace=str(workspace),
        expected_head="a" * 40,
        runtime={},
        browser={},
        test_entrypoint=["python", "-m", "pytest", "-q"],
        ci_target={},
        evidence_root=str(evidence),
        execution_id="w32-lifecycle-test",
        assignment_id="W32-EXECUTION-AUTHORITY",
        task_id="W32-P0-PYTEST",
        environment_id="w32-local-ci",
        host_identity_id="host-8031",
        requested_timeout_seconds=60,
    )


def test_lifecycle_controller_uses_core_granted_host_and_records_real_test_pass(tmp_path):
    ctx = context(tmp_path)
    host = GrantedHostStub({
        "status": "PASS",
        "work_id": "W32",
        "run_id": "run-1",
        "grant_id": "grant-1",
        "run_record_persisted": True,
        "exit_code": 0,
    })
    result = LifecycleController(ctx, EvidenceStore(Path(ctx.evidence_root)), host=host).run()

    assert result["status"] == "PASS"
    assert host.called == 1
    assert (Path(result["evidence"]) / "runtime" / "granted-execution.json").exists()


def test_lifecycle_controller_never_treats_discovery_as_execution(tmp_path):
    ctx = context(tmp_path)
    result = LifecycleController(
        ctx,
        EvidenceStore(Path(ctx.evidence_root)),
    ).run()

    assert result["status"] == "BLOCKED"
    assert result["blocker"] == "core_grant_execution_adapter_not_configured"


def test_lifecycle_controller_does_not_fake_pass_when_pytest_fails(tmp_path):
    ctx = context(tmp_path)
    host = GrantedHostStub({
        "status": "FAILED",
        "work_id": "W32",
        "run_id": "run-2",
        "grant_id": "grant-2",
        "run_record_persisted": True,
        "exit_code": 1,
    })
    result = LifecycleController(ctx, EvidenceStore(Path(ctx.evidence_root)), host=host).run()

    assert result["status"] == "FAILED"
    assert result["blocker"] == "test_execution_failed"
    final = (Path(result["evidence"]) / "FINAL_RESULT.json").read_text(encoding="utf-8")
    assert '"TEST": "FAILED"' in final
