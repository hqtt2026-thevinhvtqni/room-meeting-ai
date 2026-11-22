#!/usr/bin/env python3
"""ROOM-HOP Browser V1 Prototype — mock-only local server."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json

ROOT = Path(__file__).parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def do_GET(self):
        if self.path == '/api/health':
            payload = {'status':'ok','service':'room-hop-browser-v1-prototype','mode':'MOCK ONLY','external_api':False,'real_chromium':False}
            body = json.dumps(payload).encode()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().do_GET()
    def log_message(self, fmt, *args):
        print('[server] ' + fmt % args)

if __name__ == '__main__':
    print('ROOM-HOP Browser V1 Prototype listening on http://0.0.0.0:8787')
    ThreadingHTTPServer(('0.0.0.0', 8787), Handler).serve_forever()
