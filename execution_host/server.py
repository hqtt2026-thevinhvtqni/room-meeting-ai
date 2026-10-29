from __future__ import annotations
import hmac
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .host import ExecutionHost
from .identity import RuntimeIdentity
from .models import WorkContext, ExecutionRequest
from .work28_dispatch import DispatchError, dispatch_execute
from .work28_grant import ExecutionGrant, GrantError
from .work28_grant_registry import load_grant_registry
from .work28_core_grant_client import build_grant_source
from .work28_readback import ReadbackError, load_sealed_result
from .work28_evidence import EvidenceError
from .work28_readiness import readiness_report
from .work28_bounds import MAX_SNAPSHOT_BYTES, MAX_OUTPUT_CHARS, MAX_GLOBAL_CONCURRENT

AUTH_HEADER = 'X-Room-Hop-Execution-Auth'
AUTH_TOKEN_ENV = 'ROOM_HOP_EXECUTION_AUTH_TOKEN'
AUTHORIZED_WORKS_ENV = 'ROOM_HOP_AUTHORIZED_WORKS'
WORK_ID_PATTERN = re.compile(r'W\d+')

def normalize_work_id(value):
    if not isinstance(value, str):
        raise ValueError('work_id must be a string')
    normalized = value.strip().upper()
    if not normalized or not WORK_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            'Work id must match the canonical W<number> format, e.g. W28;'
            ' got: %r' % (value,)
        )
    return normalized

def authenticate_caller(provided, auth_token):
    if not isinstance(auth_token, str) or not auth_token:
        return False
    if not isinstance(provided, str) or not provided:
        return False
    return hmac.compare_digest(provided, auth_token)

def authorize_work(work_id, authorized_works):
    if not isinstance(authorized_works, (set, frozenset)) or not authorized_works:
        return False
    try:
        normalized = normalize_work_id(work_id)
    except (TypeError, ValueError):
        return False
    return normalized in authorized_works

def load_execution_auth_config(environ=None):
    env = os.environ if environ is None else environ
    token = env.get(AUTH_TOKEN_ENV)
    if not isinstance(token, str) or not token.strip():
        raise RuntimeError(
            AUTH_TOKEN_ENV + ' must be set to a non-empty execution token'
            ' issued by the trusted deployment configuration'
        )
    raw_works = env.get(AUTHORIZED_WORKS_ENV)
    if not isinstance(raw_works, str) or not raw_works.strip():
        raise RuntimeError(
            AUTHORIZED_WORKS_ENV + ' must list at least one canonical Work id'
            ' (comma-separated, e.g. W28)'
        )
    works = frozenset(
        normalize_work_id(part) for part in raw_works.split(',')
    )
    return {'auth_token': token.strip(), 'authorized_works': works}

class Handler(BaseHTTPRequestHandler):
    host: ExecutionHost | None = None
    auth_token: str | None = None
    authorized_works: frozenset | None = None
    grant_registry: dict | None = None
    evidence_root: str | None = None
    snapshot_only: bool = False
    def _send(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health':
            if self.host is None: self._send(503,{'status':'BLOCKED','reason':'runtime_not_initialized'}); return
            grants = Handler.grant_registry or {}
            ready = readiness_report(
                grant_count=len(grants),
                evidence_root_configured=bool(Handler.evidence_root),
                snapshot_only=bool(Handler.snapshot_only),
                core_grant_url_set=bool(os.environ.get('ROOM_HOP_CORE_GRANT_URL')),
            )
            payload = {
                'status': 'PASS',
                'service': 'execution-host',
                'provider': self.host.provider_type,
                **self.host.identity(),
                'snapshot_only': bool(Handler.snapshot_only),
                'grants_loaded': len(grants),
                'evidence_root_configured': bool(Handler.evidence_root),
                'bounds': {
                    'max_snapshot_bytes': MAX_SNAPSHOT_BYTES,
                    'max_output_chars': MAX_OUTPUT_CHARS,
                    'max_global_concurrent': MAX_GLOBAL_CONCURRENT,
                },
                'readiness': ready,
            }
            self._send(200, payload); return
        if self.path.startswith('/evidence/'):
            if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
                self._send(401,{'status':'BLOCKED','reason':'caller_authentication_failed'}); return
            if not Handler.evidence_root:
                self._send(503,{'status':'BLOCKED','reason':'evidence_root_not_configured'}); return
            exec_id = self.path[len('/evidence/'):].strip('/')
            try:
                payload = load_sealed_result(
                    evidence_root=Handler.evidence_root,
                    execution_id=exec_id,
                )
                self._send(200, payload)
            except ReadbackError as exc:
                code = 404 if 'not_found' in str(exc) else 400
                self._send(code, {'status': 'BLOCKED', 'reason': type(exc).__name__ + ':' + str(exc)})
            except EvidenceError as exc:
                self._send(409, {'status': 'BLOCKED', 'reason': type(exc).__name__ + ':' + str(exc)})
            return
        self._send(404,{'status':'NOT_FOUND'})
    def do_POST(self):
        if self.path!='/execute': self._send(404,{'status':'NOT_FOUND'}); return
        if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
            self._send(401,{'status':'BLOCKED','reason':'caller_authentication_failed'}); return
        try:
            if self.host is None: raise RuntimeError('runtime_not_initialized')
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            work_context=dict(body['work_context'])
            if not authorize_work(work_context.get('work_id'), Handler.authorized_works):
                self._send(403,{'status':'BLOCKED','reason':'caller_not_authorized_for_work'}); return
            work_context['authorized']=True
            result = dispatch_execute(
                self.host,
                work_context=work_context,
                body=body,
                grant_registry=Handler.grant_registry,
                snapshot_only=Handler.snapshot_only,
            )
            self._send(200, result)
        except (DispatchError, GrantError) as exc:
            self._send(400, {'status': 'BLOCKED', 'reason': type(exc).__name__ + ':' + str(exc)})
        except Exception as exc: self._send(400,{'status':'BLOCKED','reason':type(exc).__name__+':'+str(exc)})
    def log_message(self,*args): pass

def serve(host='127.0.0.1',port=8031,auth_token: str | None = None, authorized_works=None, grant_registry=None, evidence_root=None, snapshot_only=False):
    identity=RuntimeIdentity(bind_address=f'{host}:{port}')
    Handler.host=ExecutionHost(runtime_identity=identity)
    Handler.auth_token=auth_token
    Handler.authorized_works=frozenset(authorized_works) if authorized_works else None
    Handler.grant_registry=dict(grant_registry) if grant_registry else {}
    Handler.evidence_root=evidence_root
    Handler.snapshot_only=bool(snapshot_only)
    ThreadingHTTPServer((host,port),Handler).serve_forever()

def main():
    config = load_execution_auth_config()
    announced = ', '.join(sorted(config['authorized_works']))
    try:
        grants = build_grant_source().fetch_grants()
    except Exception:
        grants = load_grant_registry()
    print('execution-host: armed; authorized works: ' + announced +
          '; grants=' + str(len(grants)), flush=True)
    evidence_root = os.environ.get('ROOM_HOP_EVIDENCE_ROOT')
    snapshot_only = os.environ.get('ROOM_HOP_SNAPSHOT_ONLY', '').strip() in ('1', 'true', 'TRUE', 'yes')
    serve('127.0.0.1', 8031, grant_registry=grants, evidence_root=evidence_root, snapshot_only=snapshot_only, **config)

if __name__=='__main__': main()
