import json, sys, time
from urllib.request import Request, urlopen
import pytest
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_services import build_servers
@pytest.fixture(scope='module')
def services():
    core, mcp = build_servers(); import threading; threading.Thread(target=core.serve_forever, daemon=True).start(); threading.Thread(target=mcp.serve_forever, daemon=True).start(); time.sleep(0.05); yield; mcp.shutdown(); core.shutdown()
def call(payload):
    req=Request('http://127.0.0.1:8020/request', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'}, method='POST')
    with urlopen(req, timeout=2) as r: return r.status, json.loads(r.read())
def test_health_and_mcp_to_core_create_read(services):
    with urlopen('http://127.0.0.1:8000/health') as r: assert json.loads(r.read())['status']=='ok'
    with urlopen('http://127.0.0.1:8020/health') as r: assert json.loads(r.read())['status']=='ok'
    status, body=call({'action':'create','actor':'runner','doc_id':'http-1','title':'Boundary'}); assert status==200 and body['result']['revision']==0; status, body=call({'action':'read','actor':'runner','doc_id':'http-1'}); assert status==200 and body['result']['title']=='Boundary'
def test_boundary_append_idempotency_and_conflict(services):
    status, first=call({'action':'append','actor':'runner','doc_id':'http-1','expected_revision':0,'op_id':'http-op','text':'A'}); assert status==200 and first['result']['revision']==1; status, second=call({'action':'append','actor':'runner','doc_id':'http-1','expected_revision':0,'op_id':'http-op','text':'A'}); assert status==200 and second==first
    req=Request('http://127.0.0.1:8020/request', data=json.dumps({'action':'append','actor':'runner','doc_id':'http-1','expected_revision':0,'op_id':'stale','text':'B'}).encode(), headers={'Content-Type':'application/json'}, method='POST')
    with pytest.raises(Exception) as e: urlopen(req, timeout=2)
    assert getattr(e.value, 'code', None)==409
def test_boundary_not_found_and_invalid(services):
    req=Request('http://127.0.0.1:8020/request', data=json.dumps({'action':'read','actor':'runner','doc_id':'missing'}).encode(), headers={'Content-Type':'application/json'}, method='POST')
    with pytest.raises(Exception) as e: urlopen(req, timeout=2)
    assert getattr(e.value, 'code', None)==404
def test_full_boundary_with_fake_google_adapter():
    from work05_google_adapter import FakeGoogleProvider, GoogleWorkspaceAdapter
    provider = FakeGoogleProvider(); core, mcp = build_servers(core_port=18000, mcp_port=18020, adapter=GoogleWorkspaceAdapter(provider, 'fake-folder')); import threading; threading.Thread(target=core.serve_forever, daemon=True).start(); threading.Thread(target=mcp.serve_forever, daemon=True).start(); time.sleep(0.05)
    def post(payload):
        req=Request('http://127.0.0.1:18020/request', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'}, method='POST')
        with urlopen(req, timeout=2) as r: return r.status, json.loads(r.read())
    status, created=post({'action':'create','actor':'runner','doc_id':'fake-core-1','title':'Fake E2E'}); assert status == 200 and created['result']['id'] == 'fake-core-1'; status, updated=post({'action':'append','actor':'runner','doc_id':'fake-core-1','expected_revision':0,'op_id':'fake-op','text':'provider'}); assert status == 200 and updated['result']['content'] == 'provider'; status, duplicate=post({'action':'append','actor':'runner','doc_id':'fake-core-1','expected_revision':0,'op_id':'fake-op','text':'provider'}); assert status == 200 and duplicate == updated; assert any(call[0] == 'batch_update' for call in provider.calls); mcp.shutdown(); core.shutdown()
