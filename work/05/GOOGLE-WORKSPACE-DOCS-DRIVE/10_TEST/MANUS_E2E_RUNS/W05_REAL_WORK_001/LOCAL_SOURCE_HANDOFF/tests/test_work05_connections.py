import json, sys, tempfile, threading
from concurrent.futures import ThreadPoolExecutor
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


class ProviderRefreshError(Exception):
    def __init__(self, message, *, error=None, status_code=None):
        super().__init__(message)
        self.error = error
        self.status_code = status_code


def connected_manager(tmp_path, client=None):
    m, store, default_client = manager(tmp_path)
    client = client or default_client
    m.client = client
    started = m.start_oauth('room-a', 'user-a')
    from urllib.parse import parse_qs, urlparse
    state = parse_qs(urlparse(started['authorization_url']).query)['state'][0]
    m.callback('room-a', 'user-a', started['connection_id'], {'state': state, 'code': 'x'})
    return m, store, client, started['connection_id']


def test_rt06_concurrent_refresh_is_single_flight_per_connection(tmp_path):
    entered = threading.Event()
    release = threading.Event()

    class BlockingClient(OAuthClient):
        def __init__(self):
            super().__init__()
            self.calls = 0
            self.guard = threading.Lock()

        def refresh(self, credential):
            with self.guard:
                self.calls += 1
            entered.set()
            assert release.wait(timeout=3)
            return {'access_token': 'fresh-access', 'refresh_token': 'rotated-refresh'}

    client = BlockingClient()
    m, store, _, cid = connected_manager(tmp_path, client)
    old_access = store.load(cid)['access_token']
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(m.refresh, 'room-a', 'user-a', cid, old_access)
                   for _ in range(3)]
        assert entered.wait(timeout=2)
        release.set()
        results = [future.result(timeout=3) for future in futures]

    assert client.calls == 1
    assert all(result['status'] == 'CONNECTED' for result in results)
    assert store.load(cid) == {
        'access_token': 'fresh-access',
        'refresh_token': 'rotated-refresh',
    }


def test_rt08_invalid_grant_erases_unusable_credential_and_requires_reauth(tmp_path):
    class InvalidGrantClient(OAuthClient):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def refresh(self, credential):
            self.calls += 1
            raise ProviderRefreshError('invalid refresh token', error='invalid_grant',
                                       status_code=400)

    client = InvalidGrantClient()
    m, store, _, cid = connected_manager(tmp_path, client)
    with pytest.raises(ValueError, match='reauthentication required'):
        m.refresh('room-a', 'user-a', cid)

    assert client.calls == 1
    assert not store.exists(cid)
    assert m.safe_metadata('room-a', 'user-a', cid)['status'] == 'REAUTH_REQUIRED'
    assert any(item[0] == 'refresh_error' for item in m.audit)


def test_rt14_refresh_503_is_not_replayed_and_preserves_credential(tmp_path):
    class UnavailableClient(OAuthClient):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def refresh(self, credential):
            self.calls += 1
            raise ProviderRefreshError('upstream unavailable', status_code=503)

    client = UnavailableClient()
    m, store, _, cid = connected_manager(tmp_path, client)
    before = store.load(cid)

    from work05_connections import RefreshOutcomeUnknownError
    with pytest.raises(RefreshOutcomeUnknownError, match='automatic replay is prohibited'):
        m.refresh('room-a', 'user-a', cid)

    assert client.calls == 1
    assert store.exists(cid)
    assert store.load(cid) == before
    assert m.safe_metadata('room-a', 'user-a', cid)['status'] == 'ERROR'


def test_refresh_timeout_is_not_replayed_and_preserves_credential(tmp_path):
    class TimeoutClient(OAuthClient):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def refresh(self, credential):
            self.calls += 1
            raise TimeoutError('response lost')

    client = TimeoutClient()
    m, store, _, cid = connected_manager(tmp_path, client)
    before = store.load(cid)
    from work05_connections import RefreshOutcomeUnknownError
    with pytest.raises(RefreshOutcomeUnknownError):
        m.refresh('room-a', 'user-a', cid)

    assert client.calls == 1
    assert store.load(cid) == before
