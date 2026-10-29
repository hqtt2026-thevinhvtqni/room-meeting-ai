"""WP22: HTTP body size limit + evidence tamper 409 + audit JSONL sink."""
from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib import error, request

from execution_host.host import ExecutionHost
from execution_host.server import Handler, MAX_REQUEST_BODY_BYTES
from execution_host.work28_evidence import seal_evidence
from execution_host.work28_audit import clear_audits_for_tests, record_audit


class HttpBodyLimitTests(unittest.TestCase):
    def test_413_when_body_too_large(self):
        token = "wp22-token"
        Handler.host = ExecutionHost()
        Handler.auth_token = token
        Handler.authorized_works = frozenset({"W28"})
        Handler.grant_registry = {}
        Handler.evidence_root = None
        Handler.snapshot_only = False
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            over = MAX_REQUEST_BODY_BYTES + 1
            req = request.Request(
                f"http://127.0.0.1:{port}/execute",
                data=b"{}",
                headers={
                    "Content-Type": "application/json",
                    "Content-Length": str(over),
                    "X-Room-Hop-Execution-Auth": token,
                },
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            self.assertEqual(ctx.exception.code, 413)
        finally:
            httpd.shutdown()
            httpd.server_close()


class EvidenceTamperHttpTests(unittest.TestCase):
    def test_409_on_tampered_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = seal_evidence(
                evidence_root=td,
                execution_id="wp22-tamper",
                payload={"grant_id": "g", "status": "PASS"},
            )
            Path(sealed["evidence_ref"]).write_text(
                '{"tampered": true}\n', encoding="utf-8"
            )
            token = "wp22-token"
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
                    f"http://127.0.0.1:{port}/evidence/wp22-tamper",
                    headers={"X-Room-Hop-Execution-Auth": token},
                    method="GET",
                )
                with self.assertRaises(error.HTTPError) as ctx:
                    request.urlopen(req, timeout=5)
                self.assertEqual(ctx.exception.code, 409)
            finally:
                httpd.shutdown()
                httpd.server_close()


class AuditJsonlSinkTests(unittest.TestCase):
    def setUp(self):
        clear_audits_for_tests()

    def test_sink_writes_jsonl(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "audit.jsonl"
            record_audit({"grant_id": "g22", "status": "PASS"}, sink_path=path)
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 1)
            row = json.loads(lines[0])
            self.assertEqual(row["grant_id"], "g22")
            self.assertNotIn("token", row)


if __name__ == "__main__":
    unittest.main()
