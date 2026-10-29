"""WP21: audit scrub + readiness never claims RELEASE."""
from __future__ import annotations

import hashlib
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib import request

from execution_host.work28_audit import (
    clear_audits_for_tests,
    recent_audits,
    record_audit,
)
from execution_host.work28_readiness import readiness_report
from execution_host.host import ExecutionHost
from execution_host.server import Handler
from execution_host.work28_dispatch import dispatch_execute
from execution_host.work28_grant import issue_grant_for_tests


class AuditTests(unittest.TestCase):
    def setUp(self):
        clear_audits_for_tests()

    def test_scrubs_secrets(self):
        entry = record_audit(
            {
                "grant_id": "g",
                "token": "SECRET",
                "auth_token": "SECRET2",
                "status": "PASS",
            }
        )
        self.assertNotIn("token", entry)
        self.assertNotIn("auth_token", entry)
        self.assertEqual(entry["grant_id"], "g")

    def test_dispatch_records_audit(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            host_root = base / "root"
            host_root.mkdir()
            body = b'print("wp21")\n'
            (host_root / "job.py").write_bytes(body)
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            digest = hashlib.sha256(body).hexdigest()
            grant = issue_grant_for_tests(
                grant_id="g21",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            dispatch_execute(
                ExecutionHost(),
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": str(host_root),
                    "execution_workspace": str(ws),
                    "evidence_root": str(ev),
                    "authorized": True,
                    "execution_id": "wp21",
                },
                body={
                    "mode": "work28_snapshot",
                    "execution_grant_id": "g21",
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "job.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                        "timeout_seconds": 15,
                    },
                },
                grant_registry={"g21": grant},
            )
            events = recent_audits()
            self.assertTrue(any(e.get("grant_id") == "g21" for e in events))


class ReadinessTests(unittest.TestCase):
    def test_never_release(self):
        r = readiness_report(
            grant_count=5,
            evidence_root_configured=True,
            snapshot_only=True,
            core_grant_url_set=True,
        )
        self.assertFalse(r["release_allowed"])
        self.assertEqual(r["gates"]["release"], "NOT_RELEASED")
        self.assertEqual(r["gates"]["mcp_execution_tools"], "CLOSED")
        self.assertEqual(r["gates"]["os_isolation"], "NOT_VERIFIED")


class HealthTests(unittest.TestCase):
    def test_health_includes_readiness(self):
        Handler.host = ExecutionHost()
        Handler.auth_token = "t"
        Handler.authorized_works = frozenset({"W28"})
        Handler.grant_registry = {}
        Handler.evidence_root = None
        Handler.snapshot_only = True
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = httpd.server_address[1]
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            with request.urlopen(f"http://127.0.0.1:{port}/health", timeout=5) as resp:
                data = json.loads(resp.read().decode())
            self.assertEqual(data["status"], "PASS")
            self.assertTrue(data["snapshot_only"])
            self.assertIn("readiness", data)
            self.assertFalse(data["readiness"]["release_allowed"])
            self.assertIn("bounds", data)
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
