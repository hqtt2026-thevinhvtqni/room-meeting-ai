"""Product-ready Google Workspace connection boundary for Work 05.

Secrets stay inside CredentialStore and trusted backend services. Public
methods return sanitized metadata only. Real OAuth/API clients are injected
or constructed by a deployment-specific connector; this module never logs,
returns, or stores authorization codes in normal state.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from urllib.parse import urlencode
import base64, hashlib, json, os, secrets, time
from cryptography.fernet import Fernet, InvalidToken

CONNECTION_STATES={'NOT_CONNECTED','CONNECTING','CONNECTED','REAUTH_REQUIRED','ERROR','DISCONNECTED'}
def now(): return datetime.now(timezone.utc).isoformat()
def safe_error(exc): return 'provider authentication or connection error'

class ReauthRequiredError(ValueError):
    """The Google refresh credential is no longer valid; user action is required."""

class RefreshOutcomeUnknownError(RuntimeError):
    """Refresh may have succeeded remotely; do not replay the refresh request."""

def _provider_error_code(exc):
    code = getattr(exc, 'error', None) or getattr(exc, 'code', None)
    response = getattr(exc, 'response', None)
    if not code and response is not None:
        payload = getattr(response, 'json', None)
        if callable(payload):
            try:
                body = payload()
                if isinstance(body, dict):
                    code = body.get('error')
            except Exception:
                pass
    return code

def _provider_status(exc):
    response = getattr(exc, 'response', None)
    return (getattr(exc, 'status_code', None) or getattr(exc, 'status', None)
            or getattr(response, 'status_code', None))
@dataclass
class Connection:
    connection_id: str; room_id: str; user_id: str; provider: str='google_workspace'; status: str='NOT_CONNECTED'
    account_identity: str=''; provider_account_id: str=''; scopes: tuple=(); created_at: str=''; updated_at: str=''; last_tested_at: str=''; credential_ref: str=''
    def safe(self): return {'connection_id':self.connection_id,'room_id':self.room_id,'user_id':self.user_id,'provider':self.provider,'status':self.status,'account_identity':self.account_identity,'scopes':list(self.scopes),'created_at':self.created_at,'updated_at':self.updated_at,'last_tested_at':self.last_tested_at}
class CredentialStore:
    def save(self, connection_id, credential): raise NotImplementedError
    def load(self, connection_id): raise NotImplementedError
    def delete(self, connection_id): raise NotImplementedError
    def exists(self, connection_id): raise NotImplementedError
class EncryptedFileCredentialStore(CredentialStore):
    def __init__(self, directory, encryption_key=None):
        key=encryption_key or os.environ.get('W05_CREDENTIAL_STORE_KEY')
        if not key: raise ValueError('credential store encryption key is required at runtime')
        try: self.cipher=Fernet(key)
        except Exception as exc: raise ValueError('invalid credential store encryption key') from exc
        self.directory=Path(directory); self.directory.mkdir(parents=True,exist_ok=True); self.directory.chmod(0o700)
    def _path(self, connection_id): return self.directory/(hashlib.sha256(connection_id.encode()).hexdigest()+'.enc')
    def save(self, connection_id, credential):
        if not isinstance(credential,dict): raise ValueError('credential must be a mapping')
        path=self._path(connection_id); tmp=path.with_suffix('.tmp'); tmp.write_bytes(self.cipher.encrypt(json.dumps(credential,separators=(',',':')).encode())); tmp.chmod(0o600); tmp.replace(path); return connection_id
    def load(self, connection_id):
        try: return json.loads(self.cipher.decrypt(self._path(connection_id).read_bytes()).decode())
        except FileNotFoundError: raise KeyError(connection_id)
        except (InvalidToken,ValueError,TypeError) as exc: raise ValueError('credential store entry invalid') from exc
    def delete(self, connection_id):
        path=self._path(connection_id)
        if path.exists(): path.unlink()
    def exists(self, connection_id): return self._path(connection_id).is_file()
@dataclass
class OAuthState:
    state_hash: str; room_id: str; user_id: str; redirect_uri: str; expires_at: float; consumed: bool=False
class OAuthStateStore:
    def __init__(self, ttl_seconds=600): self.ttl=ttl_seconds; self._items={}; self._lock=Lock()
    def issue(self, room_id, user_id, redirect_uri):
        raw=secrets.token_urlsafe(32); digest=hashlib.sha256(raw.encode()).hexdigest()
        with self._lock: self._items[digest]=OAuthState(digest,room_id,user_id,redirect_uri,time.time()+self.ttl)
        return raw
    def consume(self, raw_state, room_id, user_id, redirect_uri):
        if not raw_state: raise ValueError('invalid oauth state')
        digest=hashlib.sha256(raw_state.encode()).hexdigest()
        with self._lock:
            item=self._items.get(digest)
            if not item or item.consumed or item.expires_at < time.time() or item.room_id!=room_id or item.user_id!=user_id or item.redirect_uri!=redirect_uri: raise ValueError('invalid oauth state')
            item.consumed=True; return item
@dataclass(frozen=True)
class OAuthConfig:
    client_id: str; redirect_uri: str; authorization_endpoint: str; scopes: tuple
class ConnectionManager:
    def __init__(self, credential_store, oauth_config, oauth_client, metadata=None, state_store=None):
        self.store=credential_store; self.oauth=oauth_config; self.client=oauth_client
        self.states=state_store or OAuthStateStore(); self.connections=metadata or {}; self.audit=[]
        self._lock=Lock(); self._refresh_locks={}; self._refresh_locks_guard=Lock()
    def _refresh_lock_for(self, connection_id):
        # Retain locks for the manager lifetime. Evicting a lock while another
        # caller already holds its reference can split one connection into two
        # independent critical sections.
        with self._refresh_locks_guard:
            return self._refresh_locks.setdefault(connection_id, Lock())
    def _get_owned(self, room_id, user_id, connection_id):
        c=self.connections.get(connection_id)
        if not c or c.room_id!=room_id or c.user_id!=user_id: raise PermissionError('connection not available')
        return c
    def safe_metadata(self, room_id, user_id, connection_id): return self._get_owned(room_id,user_id,connection_id).safe()
    def start_oauth(self, room_id, user_id):
        state=self.states.issue(room_id,user_id,self.oauth.redirect_uri); connection_id='conn_'+secrets.token_urlsafe(16); created=now(); self.connections[connection_id]=Connection(connection_id,room_id,user_id,status='CONNECTING',created_at=created,updated_at=created,credential_ref='credential:'+connection_id)
        params={'client_id':self.oauth.client_id,'redirect_uri':self.oauth.redirect_uri,'response_type':'code','scope':' '.join(self.oauth.scopes),'state':state,'access_type':'offline','prompt':'consent'}
        return {'connection_id':connection_id,'authorization_url':self.oauth.authorization_endpoint+'?'+urlencode(params)}
    def callback(self, room_id, user_id, connection_id, params):
        c=self._get_owned(room_id,user_id,connection_id)
        try:
            self.states.consume(params.get('state',''),room_id,user_id,self.oauth.redirect_uri)
            if params.get('error'): raise ValueError('provider authorization denied')
            code=params.get('code');
            if not code: raise ValueError('authorization code missing')
            token=self.client.exchange_code(code,self.oauth.redirect_uri); identity=self.client.identity(token); self.store.save(connection_id,token)
            with self._lock:
                c.status='CONNECTED'; c.account_identity=identity.get('email',''); c.provider_account_id=identity.get('id',''); c.scopes=tuple(identity.get('scopes',self.oauth.scopes)); c.updated_at=now(); c.last_tested_at=c.updated_at; self.audit.append(('connected',connection_id,room_id,user_id,c.account_identity))
            return c.safe()
        except Exception as exc:
            with self._lock: c.status='ERROR'; c.updated_at=now(); self.audit.append(('connect_error',connection_id,room_id,user_id,type(exc).__name__))
            raise ValueError(safe_error(exc)) from None
    def test_connection(self, room_id, user_id, connection_id, client_factory):
        c=self._get_owned(room_id,user_id,connection_id)
        if c.status not in {'CONNECTED','REAUTH_REQUIRED'}: raise ValueError('connection is not usable')
        try:
            identity=client_factory(self.store.load(connection_id)).test_connection(); c.status='CONNECTED'; c.last_tested_at=now(); c.updated_at=c.last_tested_at; c.account_identity=identity.get('email',c.account_identity); self.audit.append(('tested',connection_id,room_id,user_id)); return c.safe()
        except Exception as exc:
            c.status='REAUTH_REQUIRED' if getattr(exc,'reauth_required',False) else 'ERROR'; c.updated_at=now(); self.audit.append(('test_error',connection_id,room_id,user_id,type(exc).__name__)); raise ValueError(safe_error(exc)) from None
    def refresh(self, room_id, user_id, connection_id, expected_access_token=None):
        """Refresh once per connection; concurrent stale callers reuse the winner.

        The caller may pass expected_access_token from the credential used by
        its failed API request. If omitted, a pre-lock credential snapshot is
        used as the stale-call marker. Refresh transport/5xx ambiguity is never
        replayed and never deletes the stored credential.
        """
        c=self._get_owned(room_id,user_id,connection_id)
        before=self.store.load(connection_id)
        expected=(expected_access_token if expected_access_token is not None
                  else before.get('access_token'))
        lock=self._refresh_lock_for(connection_id)
        with lock:
            c=self._get_owned(room_id,user_id,connection_id)
            current=self.store.load(connection_id)
            if expected is not None and current.get('access_token') != expected:
                # Another caller refreshed this same connection while we waited.
                return c.safe()
            try:
                refreshed=self.client.refresh(current)
                if not isinstance(refreshed, dict) or not refreshed.get('access_token'):
                    raise RefreshOutcomeUnknownError('refresh response did not contain an access token')
                self.store.save(connection_id,refreshed)
                c.status='CONNECTED'; c.updated_at=now()
                self.audit.append(('refreshed',connection_id,room_id,user_id))
                return c.safe()
            except Exception as exc:
                code=_provider_error_code(exc)
                status=_provider_status(exc)
                with self._lock:
                    c.updated_at=now()
                    self.audit.append(('refresh_error',connection_id,room_id,user_id,
                                       code or status or type(exc).__name__))
                if code == 'invalid_grant':
                    # The refresh credential is definitively invalid. Remove
                    # only the unusable credential; keep sanitized audit history.
                    self.store.delete(connection_id)
                    c.status='REAUTH_REQUIRED'
                    raise ReauthRequiredError('reauthentication required') from None
                if (isinstance(exc, RefreshOutcomeUnknownError) or
                    (isinstance(status, int) and status >= 500) or
                    isinstance(exc, (TimeoutError, ConnectionError))):
                    # Google may have rotated the refresh token despite a lost
                    # response. Preserve the stored credential and stop here.
                    c.status='ERROR'
                    raise RefreshOutcomeUnknownError(
                        'refresh outcome unknown; automatic replay is prohibited'
                    ) from None
                c.status='REAUTH_REQUIRED'
                raise ReauthRequiredError('reauthentication required') from None
    def disconnect(self, room_id, user_id, connection_id):
        c=self._get_owned(room_id,user_id,connection_id)
        self.store.delete(connection_id); c.status='DISCONNECTED'; c.updated_at=now()
        self.audit.append(('disconnected',connection_id,room_id,user_id))
        # Do not evict the lock here: a concurrent waiter may already hold a
        # reference to it. Connection IDs are unique and the map is manager-scoped.
        return c.safe()
    def credential_for_operation(self, room_id, user_id, connection_id):
        c=self._get_owned(room_id,user_id,connection_id)
        if c.status!='CONNECTED': raise PermissionError('connection is not connected')
        return self.store.load(connection_id)
class ConnectionBoundOperations:
    def __init__(self, manager, provider_factory): self.manager=manager; self.provider_factory=provider_factory
    def create_document(self, room_id, user_id, connection_id, title): return self.provider_factory(self.manager.credential_for_operation(room_id,user_id,connection_id)).create_document(title)
class ConnectionAPI:
    def __init__(self, manager): self.manager=manager
    def connect(self, room_id, user_id): return self.manager.start_oauth(room_id,user_id)
    def callback(self, room_id, user_id, connection_id, callback_params): return self.manager.callback(room_id,user_id,connection_id,callback_params)
    def get(self, room_id, user_id, connection_id): return self.manager.safe_metadata(room_id,user_id,connection_id)
    def test(self, room_id, user_id, connection_id, client_factory): return self.manager.test_connection(room_id,user_id,connection_id,client_factory)
    def disconnect(self, room_id, user_id, connection_id): return self.manager.disconnect(room_id,user_id,connection_id)
