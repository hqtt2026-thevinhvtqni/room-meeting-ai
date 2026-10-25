from __future__ import annotations
import hmac
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .host import ExecutionHost
from .identity import RuntimeIdentity
from .models import WorkContext, ExecutionRequest

# Trusted header that carries the deployment-issued execution token.
AUTH_HEADER = 'X-Room-Hop-Execution-Auth'

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

class Handler(BaseHTTPRequestHandler):
    host: ExecutionHost | None = None
    auth_token: str | None = None
    def _send(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health':
            if self.host is None: self._send(503,{'status':'BLOCKED','reason':'runtime_not_initialized'}); return
            self._send(200,{'status':'PASS','service':'execution-host','provider':self.host.provider_type,**self.host.identity()}); return
        self._send(404,{'status':'NOT_FOUND'})
    def do_POST(self):
        if self.path!='/execute': self._send(404,{'status':'NOT_FOUND'}); return
        if not authenticate_caller(self.headers.get(AUTH_HEADER), Handler.auth_token):
            self._send(401,{'status':'BLOCKED','reason':'caller_authentication_failed'}); return
        try:
            if self.host is None: raise RuntimeError('runtime_not_initialized')
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            work_context=dict(body['work_context'])
            # Authorization is bound to the authenticated caller. The
            # client-supplied 'authorized' flag is never trusted.
            work_context['authorized']=True
            ctx=WorkContext(**work_context); req=ExecutionRequest(**body.get('execution_request',{})); result=self.host.execute_work(ctx,req).as_dict(); self._send(200,result)
        except Exception as exc: self._send(400,{'status':'BLOCKED','reason':type(exc).__name__+':'+str(exc)})
    def log_message(self,*args): pass

def serve(host='127.0.0.1',port=8031,auth_token: str | None = None):
    identity=RuntimeIdentity(bind_address=f'{host}:{port}')
    Handler.host=ExecutionHost(runtime_identity=identity)
    Handler.auth_token=auth_token
    ThreadingHTTPServer((host,port),Handler).serve_forever()

if __name__=='__main__': serve()
