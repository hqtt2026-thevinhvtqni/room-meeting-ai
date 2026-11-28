import json, sys, tempfile
from pathlib import Path
import pytest
from cryptography.fernet import Fernet
sys.path.insert(0, '/home/ubuntu/w05_e2e_work001/src')
from work05_connections import EncryptedFileCredentialStore, OAuthConfig, ConnectionManager, ConnectionBoundOperations
class OAuthClient:
    def __init__(self): self.refresh_fail=False; self.last_code=None
    def exchange_code(self, code, redirect_uri): self.last_code=code; return {'access_token':'a-secret','refresh_token':'r-secret'}
    def identity(self, token): return {'id':'acct-1','email':'user@example.com','scopes':['documents','drive']}
    def refresh(self, credential):
        if self.refresh_fail: raise RuntimeError('revoked')
        return {'access_token':'new-a','refresh_token':'r-secret'}
class Provider:
    def __init__(self, credential): self.credential=credential
    def create_document(self, title): return {'title':title,'credential_seen':bool(self.credential)}
def manager(tmp_path):
    store=EncryptedFileCredentialStore(tmp_path/'credentials', Fernet.generate_key()); client=OAuthClient(); config=OAuthConfig('client-id','https://app.example/callback','https://accounts.example/auth',('documents','drive')); return ConnectionManager(store,config,client),store,client
def test_oauth_state_single_use_callback_and_sanitized_metadata(tmp_path):
    m,store,client=manager(tmp_path); started=m.start_oauth('room-a','user-a'); cid=started['connection_id']; url=started['authorization_url']; assert 'state=' in url
    from urllib.parse import parse_qs, urlparse
    state=parse_qs(urlparse(url).query)['state'][0]; safe=m.callback('room-a','user-a',cid,{'state':state,'code':'one-time-code'}); encoded=json.dumps(safe)
    assert safe['status']=='CONNECTED' and safe['account_identity']=='user@example.com'; assert 'access_token' not in encoded and 'refresh_token' not in encoded and not store._path(cid).read_bytes().startswith(b'{')
    with pytest.raises(ValueError): m.callback('room-a','user-a',cid,{'state':state,'code':'replay'})
def test_state_owner_and_room_isolation(tmp_path):
    m,_,_=manager(tmp_path); started=m.start_oauth('room-a','user-a')
    with pytest.raises(PermissionError): m.safe_metadata('room-b','user-b',started['connection_id'])
    with pytest.raises(ValueError): m.callback('room-a','user-a',started['connection_id'],{'state':'wrong','code':'x'})
def test_refresh_failure_requires_reauth_and_disconnect_removes_credential(tmp_path):
    m,store,client=manager(tmp_path); started=m.start_oauth('room-a','user-a'); from urllib.parse import parse_qs,urlparse
    state=parse_qs(urlparse(started['authorization_url']).query)['state'][0]; m.callback('room-a','user-a',started['connection_id'],{'state':state,'code':'x'}); client.refresh_fail=True
    with pytest.raises(ValueError, match='reauthentication required'): m.refresh('room-a','user-a',started['connection_id'])
    assert m.safe_metadata('room-a','user-a',started['connection_id'])['status']=='REAUTH_REQUIRED'; safe=m.disconnect('room-a','user-a',started['connection_id']); assert safe['status']=='DISCONNECTED' and not store.exists(started['connection_id'])
    with pytest.raises(PermissionError): m.credential_for_operation('room-a','user-a',started['connection_id'])
def test_connection_bound_operation_never_accepts_credential_argument(tmp_path):
    m,_,_=manager(tmp_path); started=m.start_oauth('room-a','user-a'); from urllib.parse import parse_qs,urlparse
    state=parse_qs(urlparse(started['authorization_url']).query)['state'][0]; m.callback('room-a','user-a',started['connection_id'],{'state':state,'code':'x'}); captured=[]
    def factory(credential): captured.append(credential); return Provider(credential)
    result=ConnectionBoundOperations(m,factory).create_document('room-a','user-a',started['connection_id'],'Doc'); assert result['title']=='Doc' and captured[0]['access_token']=='a-secret'; assert 'credential' not in json.dumps(m.safe_metadata('room-a','user-a',started['connection_id']))
