import tempfile, time
from pathlib import Path
import pytest
from execution_host import WorkContext, ExecutionRequest, ExecutionHost
from execution_host.security import HostError

def ctx(tmp, authorized=True, **kw):
    root=Path(tmp); ws=root/'workspace'; ev=root/'evidence'; ws.mkdir(exist_ok=True); ev.mkdir(exist_ok=True)
    data=dict(work_id='13',work_name='EXECUTION-HOST-INFRASTRUCTURE',workspace_root=str(root),execution_workspace=str(ws),evidence_root=str(ev),authorized=authorized,execution_id='test-execution')
    data.update(kw); return WorkContext(**data)

def test_valid_execution_and_evidence(tmp_path):
    c=ctx(tmp_path); r=ExecutionHost().execute_work(c,ExecutionRequest(command=('python3','-c','print("ok")'))); assert r.status=='PASS'; assert Path(r.evidence_ref).exists()
def test_invalid_context_and_unauthorized(tmp_path):
    with pytest.raises(HostError): ExecutionHost().execute_command(ctx(tmp_path,False),['python3','-c','print(1)'])
def test_workspace_escape(tmp_path):
    outside=tmp_path/'outside'; outside.mkdir(); c=ctx(tmp_path,execution_workspace=str(outside))
    with pytest.raises(HostError): ExecutionHost().execute_command(c,['python3','-c','print(1)'])
def test_cwd_escape(tmp_path):
    c=ctx(tmp_path)
    with pytest.raises(HostError):
        from execution_host.security import validate_cwd
        validate_cwd(tmp_path,Path(c.execution_workspace))
def test_forbidden_and_injection(tmp_path):
    c=ctx(tmp_path)
    for cmd in (['curl','x'],['python3','-c','print(1);','rm']):
        with pytest.raises(HostError): ExecutionHost().execute_command(c,cmd)
def test_timeout_and_cleanup(tmp_path):
    c=ctx(tmp_path); r=ExecutionHost().execute_work(c,ExecutionRequest(command=('python3','-c','import time; time.sleep(2)'),timeout_seconds=.05)); assert r.status=='TIMEOUT'; assert r.cleanup['process_reaped']
def test_secret_redaction(tmp_path):
    c=ctx(tmp_path); r=ExecutionHost().execute_work(c,ExecutionRequest(command=('python3','-c','print("token=supersecret")'))); assert 'supersecret' not in r.stdout
def test_missing_git_authority_and_unavailable_adapters(tmp_path):
    c=ctx(tmp_path); h=ExecutionHost(); assert h.git_validate(c)['status']=='BLOCKED'; assert h.browser_execute(c,{})['status']=='NOT_CONFIGURED'; assert h.verify_head(c,'x')['status']=='NOT_CONFIGURED'; assert h.verify_ci(c,'x')['status']=='NOT_CONFIGURED'
def test_artifact_isolation(tmp_path):
    c=ctx(tmp_path); (Path(c.execution_workspace)/'a.txt').write_text('a'); r=ExecutionHost().execute_work(c,ExecutionRequest(command=('python3','-c','print(1)'),collect_artifacts=('a.txt',))); assert len(r.artifacts)==1; assert Path(r.artifacts[0]).is_relative_to(Path(c.evidence_root))
def test_service_lifecycle(tmp_path):
    import sys
    c=ctx(tmp_path); h=ExecutionHost()
    # Use sys.executable so Windows CI does not depend on a "python3" shim.
    s=h.start_service('x',[sys.executable,'-c','import time; time.sleep(5)'],c)
    assert s['status']=='PASS'
    assert s.get('job_object') in ('ATTACHED','NOT_ATTACHED')
    if sys.platform.startswith('win'):
        assert s.get('job_object')=='ATTACHED'
    assert h.service_status('x',c)['status']=='PASS'
    stop=h.stop_service('x',c)
    assert stop['status']=='PASS'
    assert stop.get('process_reaped') is True
