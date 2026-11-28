import sys
import pytest
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_mock import Core, MCPInterface, Conflict, NotFound, AdapterFailure
from work05_google_adapter import FakeGoogleProvider, GoogleWorkspaceAdapter
def stack():
    provider = FakeGoogleProvider(); adapter = GoogleWorkspaceAdapter(provider, parent_id='fake-test-folder'); return MCPInterface(Core(adapter)), provider, adapter
def test_provider_contract_create_read_and_parent_target():
    m, provider, _ = stack(); created = m.request('create', actor='runner', doc_id='core-1', title='Contract'); assert created == {'id':'core-1','title':'Contract','content':'','revision':0}; assert provider.calls[0] == ('create_document','fake-doc-1','fake-test-folder'); assert m.request('read', actor='runner', doc_id='core-1')['id'] == 'core-1'
def test_controlled_update_revision_and_idempotency():
    m, provider, adapter = stack(); m.request('create', actor='runner', doc_id='core-1', title='Contract'); m.request('append', actor='runner', doc_id='core-1', expected_revision=0, op_id='a', text='A\n[SECTION]old'); updated = m.request('section_update', actor='editor', doc_id='core-1', expected_revision=1, op_id='b', text='new'); assert updated['content'] == 'A\n[SECTION]new' and updated['revision'] == 2; duplicate = m.request('section_update', actor='editor', doc_id='core-1', expected_revision=1, op_id='b', text='new'); assert duplicate == updated
    with pytest.raises(Conflict): m.request('append', actor='runner', doc_id='core-1', expected_revision=1, op_id='c', text='stale')
    assert adapter.change_state('core-1')['revision'] == 2
def test_provider_errors_are_normalized_and_recover_once():
    m, provider, _ = stack(); m.request('create', actor='runner', doc_id='core-1', title='Contract'); provider.fail_next = 'UNAVAILABLE'
    with pytest.raises(AdapterFailure, match='UNAVAILABLE'): m.request('append', actor='runner', doc_id='core-1', expected_revision=0, op_id='retry-1', text='A')
    recovered = m.request('append', actor='runner', doc_id='core-1', expected_revision=0, op_id='retry-1', text='A'); assert recovered['content'] == 'A' and recovered['revision'] == 1
def test_not_found_and_invalid_section_are_safe():
    m, _, _ = stack()
    with pytest.raises(NotFound): m.request('read', actor='runner', doc_id='missing')
    m.request('create', actor='runner', doc_id='core-1', title='Contract')
    with pytest.raises(AdapterFailure, match='INVALID_ARGUMENT'): m.request('section_update', actor='editor', doc_id='core-1', expected_revision=0, op_id='bad', text='x')
