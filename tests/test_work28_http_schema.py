"""WP23: Content-Type, body key allowlist, method 405."""
from __future__ import annotations

import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib import error, request

from execution_host.host import ExecutionHost
from execution_host.server import Handler


def _start():
    token = "wp23-token"
    Handler.host = ExecutionHost()
    Handler.auth_token = token
    Handler.authorized_works = frozenset({"W28"})
    Handler.grant_registry = {}
    Handler.evidence_root = None
    Handler.snapshot_only = False
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, port, token


class ContentTypeTests(unittest.TestCase):
    def test_415_without_json(self):
        httpd, port, token = _start()
        try:
            req = request.Request(
                f"http://127.0.0.1:{port}/execute",
                data=b'{"work_context":{"work_id":"W28"}}',
                headers={
                    "Content-Type": "text/plain",
                    "X-Room-Hop-Execution-Auth": token,
                },
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            self.assertEqual(ctx.exception.code, 415)
        finally:
            httpd.shutdown()
            httpd.server_close()


class BodyKeyTests(unittest.TestCase):
    def test_400_unknown_key(self):
        httpd, port, token = _start()
        try:
            payload = {
                "work_context": {
                    "work_id": "W28",
                    "work_name": "W",
                    "workspace_root": "/tmp",
                    "execution_workspace": "/tmp",
                    "evidence_root": "/tmp",
                    "authorized": False,
                },
                "evil_key": True,
            }
            req = request.Request(
                f"http://127.0.0.1:{port}/execute",
                data=json.dumps(payload).encode(),
                headers={
                    "Content-Type": "application/json",
                    "X-Room-Hop-Execution-Auth": token,
                },
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            self.assertEqual(ctx.exception.code, 400)
            body = ctx.exception.read().decode()
            self.assertIn("unknown_body_keys", body)
        finally:
            httpd.shutdown()
            httpd.server_close()


class MethodNotAllowedTests(unittest.TestCase):
    def test_405_put(self):
        httpd, port, token = _start()
        try:
            req = request.Request(
                f"http://127.0.0.1:{port}/execute",
                data=b"{}",
                headers={
                    "Content-Type": "application/json",
                    "X-Room-Hop-Execution-Auth": token,
                },
                method="PUT",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            self.assertEqual(ctx.exception.code, 405)
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
