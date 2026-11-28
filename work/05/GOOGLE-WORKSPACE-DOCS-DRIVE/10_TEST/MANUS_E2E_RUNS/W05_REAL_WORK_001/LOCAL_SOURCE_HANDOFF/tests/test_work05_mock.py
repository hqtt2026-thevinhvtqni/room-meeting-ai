import sys
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
import pytest
from work05_mock import *
@pytest.fixture
def stack():
    a=LocalWorkspaceAdapter(); c=Core(a); return MCPInterface(c), a, c
def test_create_read_append_update(stack):
    m,_,_=stack; assert m.request('create',actor='runner',doc_id='d1',title='Minutes')['revision']==0; assert m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='o1',text='A')['content']=='A'; assert m.request('append',actor='runner',doc_id='d1',expected_revision=1,op_id='o2',text='\n[SECTION]old')['revision']==2; assert m.request('section_update',actor='editor',doc_id='d1',expected_revision=2,op_id='o3',text='new')['content']=='A\n[SECTION]new'
def test_invalid_missing_and_auth(stack):
    m,_,_=stack
    with pytest.raises(DomainError): m.request('bogus')
    with pytest.raises(NotFound): m.request('read',actor='runner',doc_id='missing')
    with pytest.raises(Unauthorized): m.request('read',actor='intruder',doc_id='missing')
def test_idempotency(stack):
    m,_,_=stack; m.request('create',actor='runner',doc_id='d1',title='x'); first=m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='same',text='A'); second=m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='same',text='A'); assert first == second and second['content']=='A' and second['revision']==1
def test_revision_conflict(stack):
    m,_,_=stack; m.request('create',actor='runner',doc_id='d1',title='x'); m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='a',text='A')
    with pytest.raises(Conflict): m.request('append',actor='editor',doc_id='d1',expected_revision=0,op_id='b',text='B')
def test_adapter_failure_and_bounded_recovery(stack):
    m,a,c=stack; m.request('create',actor='runner',doc_id='d1',title='x'); a.fail_next=True
    with pytest.raises(AdapterFailure): m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='r1',text='A')
    assert m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='r1',text='A')['content']=='A'; assert any(x[0]=='append' for x in c.audit)
def test_core_boundary_and_persistence(stack):
    m,a,c=stack; m.request('create',actor='runner',doc_id='d1',title='x'); m.request('append',actor='runner',doc_id='d1',expected_revision=0,op_id='a',text='A'); assert a.read('d1').content=='A' and len(c.audit)==2
