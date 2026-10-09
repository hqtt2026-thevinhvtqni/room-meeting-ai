from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .host import ExecutionHost
from .identity import RuntimeIdentity
from .models import WorkContext, ExecutionRequest

class Handler(BaseHTTPRequestHandler):
    host: ExecutionHost | None = None
    def _send(self,code,payload):
        data=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path=='/health':
            if self.host is None: self._send(503,{'status':'BLOCKED','reason':'runtime_not_initialized'}); return
            self._send(200,{'status':'PASS','service':'execution-host','provider':self.host.provider_type,**self.host.identity()}); return
        self._send(404,{'status':'NOT_FOUND'})
    def do_POST(self):
        if self.path!='/execute': self._send(404,{'status':'NOT_FOUND'}); return
        try:
            if self.host is None: raise RuntimeError('runtime_not_initialized')
            body=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0')))); ctx=WorkContext(**body['work_context']); req=ExecutionRequest(**body.get('execution_request',{})); result=self.host.execute_work(ctx,req).as_dict(); self._send(200,result)
        except Exception as exc: self._send(400,{'status':'BLOCKED','reason':type(exc).__name__+':'+str(exc)})
    def log_message(self,*args): pass

def serve(host='127.0.0.1',port=8031):
    identity=RuntimeIdentity(bind_address=f'{host}:{port}')
    Handler.host=ExecutionHost(runtime_identity=identity)
    ThreadingHTTPServer((host,port),Handler).serve_forever()

if __name__=='__main__': serve()
