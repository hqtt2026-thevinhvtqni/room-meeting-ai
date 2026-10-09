import json
from execution_host.wee_bridge import ExecutionHostBridge

class FakeTransport:
    def __init__(self, code=200, payload=None, error=None): self.code=code; self.payload=payload or {}; self.error=error; self.calls=[]
    def __call__(self,url,body,timeout):
        self.calls.append((url,json.loads(body),timeout))
        if self.error: raise self.error
        return self.code,json.dumps(self.payload).encode()

def context(**overrides):
    value=dict(work_id='W-any',work_name='generic',workspace_root='/w',execution_workspace='/w/run',evidence_root='/w/evidence',authorized=True,execution_id='e-1'); value.update(overrides); return value

def request_body(): return {'command':['python3','-c','print(1)'],'timeout_seconds':10}
def test_request_schema_and_authoritative_binding():
    fake=FakeTransport(payload={'execution_id':'e-1','work_id':'W-any','status':'PASS','exit_code':0,'evidence_ref':'/w/evidence/e-1/FINAL_RESULT.json','cleanup':{'process_reaped':True}})
    result=ExecutionHostBridge('http://host:8031',transport=fake).invoke(context(),request_body())
    assert result.status=='PASS'; assert fake.calls[0][0]=='http://host:8031/execute'; assert fake.calls[0][1]['work_context']['work_id']=='W-any'; assert result.evidence_ref.endswith('FINAL_RESULT.json')
def test_nested_pass_response_preserves_result():
    fake=FakeTransport(payload={'result':{'execution_id':'e-2','work_id':'W-any','status':'PASS','exit_code':0,'evidence_ref':'evidence/x','stdout_ref':'out','stderr_ref':'err','artifacts':['a'], 'cleanup':{'process_reaped':True}}})
    result=ExecutionHostBridge(transport=fake).invoke(context(execution_id='e-2'),request_body()); assert result.as_dict()['artifacts']==['a']; assert result.cleanup['process_reaped']
def test_blocked_response_is_not_promoted():
    fake=FakeTransport(code=403,payload={'status':'BLOCKED','blocker':'unauthorized'}); result=ExecutionHostBridge(transport=fake).invoke(context(),request_body()); assert result.status=='BLOCKED'; assert result.blocker=='unauthorized'
def test_missing_authority_is_blocked_without_network():
    fake=FakeTransport(); result=ExecutionHostBridge(transport=fake).invoke(context(authorized=False),request_body()); assert result.status=='BLOCKED'; assert result.blocker=='execution_not_authorized'; assert not fake.calls
def test_timeout_or_network_error_is_blocked():
    fake=FakeTransport(error=TimeoutError('down')); result=ExecutionHostBridge(transport=fake).invoke(context(),request_body()); assert result.status=='BLOCKED'; assert result.blocker.startswith('execution_host_unreachable:')
def test_endpoint_is_configurable_and_work_generic():
    fake=FakeTransport(payload={'status':'PASS','execution_id':'e-1','work_id':'W-99','exit_code':0}); result=ExecutionHostBridge('http://example.test:9',transport=fake).invoke(context(work_id='W-99'),request_body()); assert result.status=='PASS'; assert fake.calls[0][0]=='http://example.test:9/execute'
