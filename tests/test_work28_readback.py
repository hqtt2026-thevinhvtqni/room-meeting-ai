"""WP19: evidence readback + snapshot_only mode."""
from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib import error, request

from execution_host.host import ExecutionHost
from execution_host.server import Handler
from execution_host.work28_dispatch import DispatchError, dispatch_execute
from execution_host.work28_evidence import seal_evidence
from execution_host.work28_readback import ReadbackError, load_sealed_result


class ReadbackUnitTests(unittest.TestCase):
    def test_load_ok(self):
        with tempfile.TemporaryDirectory() as td:
            seal_evidence(
                evidence_root=td,
                execution_id="run-a",
                payload={"grant_id": "g", "status": "PASS"},
            )
            out = load_sealed_result(evidence_root=td, execution_id="run-a")
            self.assertEqual(out["result"]["grant_id"], "g")

    def test_reject_traversal(self):
        with self.assertRaises(ReadbackError):
            load_sealed_result(evidence_root="/tmp", execution_id="../etc")

    def test_not_found(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ReadbackError):
                load_sealed_result(evidence_root=td, execution_id="missing")


class SnapshotOnlyTests(unittest.TestCase):
    def test_command_refused(self):
        with self.assertRaises(DispatchError) as ctx:
            dispatch_execute(
                ExecutionHost(),
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": ".",
                    "execution_workspace": ".",
                    "evidence_root": ".",
                    "authorized": True,
                },
                body={"mode": "command", "execution_request": {"command": ["true"]}},
                grant_registry={},
                snapshot_only=True,
            )
        self.assertIn("snapshot_only", str(ctx.exception))


class HttpReadbackTests(unittest.TestCase):
    def test_http_readback_200_and_401(self):
        with tempfile.TemporaryDirectory() as td:
            seal_evidence(
                evidence_root=td,
                execution_id="wp19-e",
                payload={"grant_id": "g19", "status": "PASS"},
            )
            token = "wp19-token"
            Handler.host = ExecutionHost()
            Handler.auth_token = token
            Handler.authorized_works = frozenset({"W28"})
            Handler.grant_registry = {}
            Handler.evidence_root = td
            Handler.snapshot_only = False
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            port = httpd.server_address[1]
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            try:
                req = request.Request(
                    f"http://127.0.0.1:{port}/evidence/wp19-e", method="GET"
                )
                with self.assertRaises(error.HTTPError) as ctx:
                    request.urlopen(req, timeout=5)
                self.assertEqual(ctx.exception.code, 401)
                req2 = request.Request(
                    f"http://127.0.0.1:{port}/evidence/wp19-e",
                    headers={"X-Room-Hop-Execution-Auth": token},
                    method="GET",
                )
                with request.urlopen(req2, timeout=5) as resp:
                    self.assertEqual(resp.status, 200)
                    data = json.loads(resp.read().decode())
                self.assertEqual(data["result"]["grant_id"], "g19")
                self.assertIn("evidence_sha256", data)
            finally:
                httpd.shutdown()
                httpd.server_close()


if __name__ == "__main__":
    unittest.main()
