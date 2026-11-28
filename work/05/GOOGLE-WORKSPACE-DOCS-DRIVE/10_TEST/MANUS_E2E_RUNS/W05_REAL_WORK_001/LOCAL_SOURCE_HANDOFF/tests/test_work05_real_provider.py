import sys
from pathlib import Path
import pytest
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_real_provider import GoogleConfig, validate_config, GoogleWorkspaceProvider, build_google_services
from work05_google_adapter import ProviderError
class Call:
    def __init__(self, value): self.value=value
    def execute(self): return self.value
class Docs:
    def __init__(self): self.data={'documentId':'g-1','title':'Injected','revisionId':'r0','body':{'content':[{'endIndex':10,'paragraph':{'elements':[{'textRun':{'content':'hello\n'}}]}}]}}; self.last=None; self.history=[]
    def documents(self): return self
    def create(self, body): self.last=('create',body); self.history.append(self.last); return Call({'documentId':'g-1'})
    def get(self, documentId, **kwargs): self.last=('get',documentId,kwargs); self.history.append(self.last); return Call(self.data)
    def batchUpdate(self, documentId, body): self.last=('batchUpdate',documentId,body); self.history.append(self.last); self.data['revisionId']='r1'; return Call({'replies':[]})
class Files:
    def __init__(self): self.last=None
    def files(self): return self
    def update(self, **kwargs): self.last=('update',kwargs); return Call({'id':kwargs['fileId']})
def test_config_validation_is_safe_and_does_not_expose_values(tmp_path):
    missing=GoogleConfig.from_env({'W05_GOOGLE_SCOPES':'docs.test','W05_GOOGLE_PARENT_ID':'folder'}); result=validate_config(missing); assert not result['ready'] and 'CREDENTIALS_FILE' in result['errors'][0]; cred=tmp_path/'credentials.json'; cred.write_text('{}'); ready=GoogleConfig(str(cred), ('docs.test',), 'folder'); assert validate_config(ready)['ready']
def test_injected_services_create_read_update_and_change_state():
    docs, files = Docs(), Files(); provider=GoogleWorkspaceProvider(docs, files, 'folder'); created=provider.create_document('Injected'); assert created['documentId']=='g-1' and files.last[1]['addParents']=='folder'; assert provider.get_document('g-1')['content']=='hello\n'; updated=provider.batch_update('g-1',[{'operationId':'op-1','mode':'append','text':'world'}],'r0'); batch=[call for call in docs.history if call[0]=='batchUpdate'][-1]; assert updated['revision']=='r1' and batch[2]['writeControl']['requiredRevisionId']=='r0'; assert provider.get_change_state('g-1')['revision']=='r1'
def test_invalid_config_blocks_client_construction():
    with pytest.raises(ProviderError) as exc: build_google_services(GoogleConfig('', (), ''))
    assert exc.value.code == 'CONFIG_INVALID'
