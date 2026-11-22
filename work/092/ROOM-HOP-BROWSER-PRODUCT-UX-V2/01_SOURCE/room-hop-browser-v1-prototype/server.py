#!/usr/bin/env python3
"""Optional TEST_ONLY static preview server; never binds a shared service port."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json

ROOT = Path(__file__).parent
PREVIEW_HOST = "127.0.0.1"
# Ask the operating system to choose an available ephemeral port; avoid a hard-coded service port.
PREVIEW_PORT = 0


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            payload = {
                "status": "ok",
                "service": "room-hop-browser-v1-prototype",
                "mode": "TEST_ONLY",
                "external_api": False,
                "real_chromium": False,
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        print("[TEST_ONLY preview] " + fmt % args)


def serve():
    httpd = ThreadingHTTPServer((PREVIEW_HOST, PREVIEW_PORT), Handler)
    host, port = httpd.server_address[:2]
    print(f"TEST_ONLY preview ready at http://{host}:{port} (loopback; OS-assigned port)")
    try:
        httpd.serve_forever()
    finally:
        httpd.server_close()


if __name__ == "__main__":
    serve()
