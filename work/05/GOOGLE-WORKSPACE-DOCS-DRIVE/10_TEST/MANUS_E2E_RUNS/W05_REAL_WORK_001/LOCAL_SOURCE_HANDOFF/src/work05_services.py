"""Local-only ROOM-HOP boundary harness.

MCP :8020 forwards JSON requests to Core :8000; Core owns the existing
business logic and LocalWorkspaceAdapter. No Google APIs or credentials.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from work05_mock import LocalWorkspaceAdapter, Core, MCPInterface, DomainError, NotFound, Conflict, Unauthorized, AdapterFailure

def error_status(exc):
    if isinstance(exc, Unauthorized): return 403
    if isinstance(exc, NotFound): return 404
    if isinstance(exc, Conflict): return 409
    if isinstance(exc, (DomainError, AdapterFailure)): return 400
    return 500

def make_handler(interface, downstream=None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def _send(self, status, payload):
            data = json.dumps(payload).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
        def do_GET(self):
            if self.path == '/health': self._send(200, {'status':'ok'}); return
            self._send(404, {'error':'not_found'})
        def do_POST(self):
            try:
                length = int(self.headers.get('Content-Length','0')); payload = json.loads(self.rfile.read(length) or b'{}')
                if downstream:
                    req = Request(downstream, data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'}, method='POST')
                    with urlopen(req, timeout=3) as resp: self._send(resp.status, json.loads(resp.read()))
                    return
                result = interface.request(**payload); self._send(200, {'ok': True, 'result': result})
            except HTTPError as exc: self._send(exc.code, {'error':'downstream_error','detail':exc.read().decode()})
            except (URLError, TimeoutError) as exc: self._send(503, {'error':'core_unavailable','detail':str(exc)})
            except Exception as exc: self._send(error_status(exc), {'error':type(exc).__name__, 'detail':str(exc)})
    return Handler

def build_servers(core_host='127.0.0.1', core_port=8000, mcp_host='127.0.0.1', mcp_port=8020, adapter=None):
    adapter = adapter or LocalWorkspaceAdapter(); core = Core(adapter); interface = MCPInterface(core); core_server = ThreadingHTTPServer((core_host, core_port), make_handler(interface)); mcp_server = ThreadingHTTPServer((mcp_host, mcp_port), make_handler(None, f'http://{core_host}:{core_port}/request')); return core_server, mcp_server
if __name__ == '__main__':
    import threading
    core_server, mcp_server = build_servers(); threading.Thread(target=core_server.serve_forever, daemon=True).start(); print('CORE_READY 8000', flush=True); print('MCP_READY 8020', flush=True)
    try: mcp_server.serve_forever()
    except KeyboardInterrupt: pass
    finally: core_server.shutdown(); mcp_server.shutdown()
