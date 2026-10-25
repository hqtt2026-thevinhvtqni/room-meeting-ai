from __future__ import annotations
import hmac
import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .host import ExecutionHost
from .identity import RuntimeIdentity
from .models import WorkContext, ExecutionRequest

# Trusted header that carries the deployment-issued execution token.
AUTH_HEADER = 'X-Room-Hop-Execution-Auth'

# Trusted environment variables for the deployment configuration. The token
# value is never logged, echoed, or written into evidence.
AUTH_TOKEN_ENV = 'ROOM_HOP_EXECUTION_AUTH_TOKEN'
AUTHORIZED_WORKS_ENV = 'ROOM_HOP_AUTHORIZED_WORKS'

# Canonical Work id format pinned for the execution boundary: W<number>.
WORK_ID_PATTERN = re.compile(r'W\d+')

def normalize_work_id(value):
    """Validate and normalize a Work id against the pinned W<number> format."""
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
    """Fail-closed caller authentication for the POST /execute boundary.

    auth_token comes only from the trusted deployment configuration. A request
    is authenticated only when it presents the exact configured token via
    constant-time comparison. An unarmed server (no token configured) never
    authenticates anything.
    """
    if not isinstance(auth_token, str) or not auth_token:
        return False
    if not isinstance(provided, str) or not provided:
        return False
    return hmac.compare_digest(provided, auth_token)

def authorize_work(work_id, authorized_works):
    """Fail-closed per-Work authorization for an already authenticated caller.

    authorized_works comes only from the trusted deployment configuration
    
(the Core :8000 authority chain). Authentication alone never grants
    execution rights; a Work must be explicitly allow-listed.
    """
    if not isinstance(work_id, str) or not work_id:
        return False
    if not isinstance(authorized_works, (set, frozenset)):
        return False
    return work_id in authorized_works

def load_execution_auth_config(environ=None):
    """Load and validate the trusted execution auth configuration at startup.

    Raises loudly on missing or malformed configuration so an unconfigured
    service can never start silently. The token value never appears in the
    error messages.
    """
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
    def _send(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health':
            if self.host is None: self._send(503,{'status':'BLOCKED','reason':'runtime_not_initialized'}); return
            self._s
end(200,{'status':'PASS','service':'execution-host','provider':self.host.provider_type,**self.host.identity()}); return
        self._send(404,{'status':'NOT_FOUND'})
    def do_POST(self):
        if self.path!='/execute': self._send(404,{'status':'NOT_FOUND'}); return
        if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
            self._send(401,{'status':'BLOCKED','reason':'caller_authentication_failed'}); return
        try:
            if self.host is None: raise RuntimeError('runtime_not_initialized')
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            work_context=dict(body['work_context'])
            # Authorization is decided server-side per Work for the
            # authenticated caller; the client-supplied 'authorized' flag is
            # never trusted. A token alone grants no execution rights.
            if not authorize_work(work_context.get('work_id'), Handler.authorized_works):
                self._send(403,{'status':'BLOCKED','reason':'caller_not_authorized_for_work'}); return
            work_context['authorized']=True
            ctx=WorkContext(**work_context); req=ExecutionRequest(**body.get('execution_request',{})); result=self.host.execute_work(ctx,req).as_dict(); self._send(200,result)
        except Exception as exc: self._send(400,{'status':'BLOCKED','reason':type(exc).__name__+':'+str(exc)})
    def log_message(self,*args): pass

def serve(host='127.0.0.1',port=8031,auth_token: str | None = None, authorized_works=None):
    identity=RuntimeIdentity(bind_address=f'{host}:{port}')
    Handler.host=ExecutionHost(runtime_identity=identity)
    Handler.auth_token=auth_token
    Handler.authorized_works=frozenset(authorized_works) if authorized_works else None
    ThreadingHTTPServer((host,port),Handler).serve_forever()

def main():
    config = load_execution_auth_config()
    # The token value is never printed or logged; only the authorized
    # Work ids
 and the bind address are announced at startup.
    announced = ', '.join(sorted(config['authorized_works']))
    print('execution-host: armed; authorized works: ' + announced, flush=True)
    serve('127.0.0.1', 8031, **config)

if __name__=='__main__': main()
