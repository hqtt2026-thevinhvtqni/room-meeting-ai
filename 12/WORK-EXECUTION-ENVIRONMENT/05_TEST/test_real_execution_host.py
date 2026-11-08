import pytest
from wee.bridge.real_host import RealExecutionHost, WorkIsolationError
from wee.models import WorkContext

def ctx(tmp_path, workspace=None):
    root=tmp_path/'work'; root.mkdir(exist_ok=True)
    return WorkContext('12','WORK-EXECUTION-ENVIRONMENT','repo',str(root),'main',str(workspace or root),'head',{}, {}, ['true'], {}, str(root/'06_EVIDENCE'),'host-test')

def test_real_host_requires_explicit_enable(tmp_path):
    with pytest.raises(RuntimeError): RealExecutionHost()

def test_real_host_isolates_bound_workspace(tmp_path):
    host=RealExecutionHost(enabled=True)
    outside=tmp_path/'outside'; outside.mkdir()
    with pytest.raises(WorkIsolationError): host.workspace_info(ctx(tmp_path, outside))

def test_missing_external_adapters_are_explicit(tmp_path):
    context=ctx(tmp_path); host=RealExecutionHost(enabled=True)
    report=host.discover(context)
    by_name={x['name']:x for x in report['capabilities']}
    assert by_name['github']['status']=='NOT_CONFIGURED'
    assert by_name['ci']['status']=='NOT_CONFIGURED'
    assert host.github_verify(context)['status']=='NOT_CONFIGURED'
    assert host.ci_verify(context,'head')['status']=='NOT_CONFIGURED'


def test_real_host_refuses_process_when_process_permission_is_off(tmp_path):
    context=ctx(tmp_path)
    host=RealExecutionHost(enabled=True,allow_processes=False,evidence_root=context.evidence_root)
    result=host.execute(["python3","-c","print('must-not-run')"],context)
    assert result.status=="BLOCKED"
    assert result.blocker=="process_permission_not_granted"


def test_real_host_enforces_execution_timeout(tmp_path):
    context=ctx(tmp_path)
    host=RealExecutionHost(enabled=True,allow_processes=True,evidence_root=context.evidence_root)
    result=host.execute(["python3","-c","import time; time.sleep(2)"],context,timeout_seconds=0.05)
    assert result.status=="FAILED"
    assert result.timed_out is True
    assert result.blocker=="execution_timeout"
    assert result.process_tree_cleanup_verified is False


def test_real_host_does_not_forward_unapproved_environment_secrets(tmp_path,monkeypatch):
    context=ctx(tmp_path)
    monkeypatch.setenv("ROOM_HOP_TEST_SECRET","do-not-forward-this-secret")
    host=RealExecutionHost(enabled=True,allow_processes=True,evidence_root=context.evidence_root)
    result=host.execute(
        ["python3","-c","import os; print(os.getenv('ROOM_HOP_TEST_SECRET','missing'))"],
        context,
        timeout_seconds=5,
    )
    assert result.status=="PASS"
    assert "missing" in open(result.stdout_ref,encoding="utf-8").read()
    assert "do-not-forward-this-secret" not in open(result.stdout_ref,encoding="utf-8").read()
