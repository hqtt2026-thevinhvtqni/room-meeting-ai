"""WP16/WP17: dispatch grant→snapshot; HTTP auth E2E; work_id equivalence."""
from __future__ import annotations

import hashlib
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib import error, request

from execution_host.host import ExecutionHost
from execution_host.server import Handler
from execution_host.work28_dispatch import DispatchError, dispatch_execute
from execution_host.work28_grant import GrantError, issue_grant_for_tests


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class DispatchUnitTests(unittest.TestCase):
    def test_command_mode_rejects_work28_fields(self):
        host = ExecutionHost()
        with self.assertRaises(DispatchError):
            dispatch_execute(
                host,
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": ".",
                    "execution_workspace": ".",
                    "evidence_root": ".",
                    "authorized": True,
                },
                body={"mode": "command", "execution_grant_id": "x"},
                grant_registry={},
            )

    def test_snapshot_requires_registry_grant(self):
        host = ExecutionHost()
        with self.assertRaises(GrantError):
            dispatch_execute(
                host,
                work_context={
                    "work_id": "28",
                    "work_name": "W",
                    "workspace_root": ".",
                    "execution_workspace": ".",
                    "evidence_root": ".",
                    "authorized": True,
                },
                body={
                    "mode": "work28_snapshot",
                    "execution_grant_id": "missing",
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "a.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": "a" * 64,
                    },
                },
                grant_registry={},
            )

    def test_snapshot_pipeline_ok(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            host_root = base / "root"
            host_root.mkdir()
            (host_root / "job.py").write_bytes(b'print("wp16")\n')
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            digest = _sha(b'print("wp16")\n')
            grant = issue_grant_for_tests(
                grant_id="g16",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            result = dispatch_execute(
                ExecutionHost(),
                work_context={
                    "work_id": "28",
                    "work_name": "WORK28",
                    "workspace_root": str(host_root),
                    "execution_workspace": str(ws),
                    "evidence_root": str(ev),
                    "authorized": False,
                    "execution_id": "wp16",
                },
                body={
                    "mode": "work28_snapshot",
                    "execution_grant_id": "g16",
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "job.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                        "timeout_seconds": 15,
                    },
                },
                grant_registry={"g16": grant},
            )
            self.assertEqual(result.get("dispatch_mode"), "work28_snapshot")
            self.assertEqual(result.get("grant_id"), "g16")
            if result.get("status") == "PASS":
                self.assertIn("wp16", result.get("stdout_summary") or "")


class HttpBoundaryTests(unittest.TestCase):
    def test_http_401_without_token(self):
        token = "test-token-wp16"
        Handler.host = ExecutionHost()
        Handler.auth_token = token
        Handler.authorized_works = frozenset({"W28"})
        Handler.grant_registry = {}
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            req = request.Request(
                f"http://127.0.0.1:{port}/execute",
                data=json.dumps({"work_context": {"work_id": "W28"}}).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with self.assertRaises(error.HTTPError) as ctx:
                request.urlopen(req, timeout=5)
            self.assertEqual(ctx.exception.code, 401)
        finally:
            httpd.shutdown()
            httpd.server_close()


class WorkIdEquivTests(unittest.TestCase):
    def test_w28_and_28(self):
        from execution_host.work28_work_id import work_ids_equivalent
        self.assertTrue(work_ids_equivalent("W28", "28"))
        self.assertTrue(work_ids_equivalent("28", "w28"))
        self.assertFalse(work_ids_equivalent("W28", "W12"))
        self.assertFalse(work_ids_equivalent("28", "280"))


class HttpE2EGrantSnapshotTests(unittest.TestCase):
    def test_http_200_work28_snapshot_with_token_and_grant(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            host_root = base / "root"
            host_root.mkdir()
            body_src = b'print("wp17-http")\n'
            (host_root / "job.py").write_bytes(body_src)
            ws = host_root / "workspace"
            ev = host_root / "evidence"
            ws.mkdir()
            ev.mkdir()
            digest = _sha(body_src)
            grant = issue_grant_for_tests(
                grant_id="g17",
                work_id="28",
                entry_path="job.py",
                operation="RUN_SCRIPT",
                expected_source_sha256=digest,
            )
            token = "wp17-secret-token"
            Handler.host = ExecutionHost()
            Handler.auth_token = token
            Handler.authorized_works = frozenset({"W28"})
            Handler.grant_registry = {"g17": grant}
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
            port = httpd.server_address[1]
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                payload = {
                    "mode": "work28_snapshot",
                    "execution_grant_id": "g17",
                    "work_context": {
                        "work_id": "W28",
                        "work_name": "WORK28",
                        "workspace_root": str(host_root),
                        "execution_workspace": str(ws),
                        "evidence_root": str(ev),
                        "authorized": False,
                        "execution_id": "wp17-http",
                    },
                    "work28_request": {
                        "work_id": "28",
                        "entry_path": "job.py",
                        "operation": "RUN_SCRIPT",
                        "expected_source_sha256": digest,
                        "timeout_seconds": 15,
                    },
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
                with request.urlopen(req, timeout=15) as resp:
                    self.assertEqual(resp.status, 200)
                    data = json.loads(resp.read().decode())
                self.assertEqual(data.get("dispatch_mode"), "work28_snapshot")
                self.assertEqual(data.get("grant_id"), "g17")
                if data.get("status") == "PASS":
                    self.assertIn("wp17-http", data.get("stdout_summary") or "")
            finally:
                httpd.shutdown()
                httpd.server_close()

    def test_http_403_work_not_allowlisted(self):
        token = "wp17-secret-token"
        Handler.host = ExecutionHost()
        Handler.auth_token = token
        Handler.authorized_works = frozenset({"W28"})
        Handler.grant_registry = {}
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            payload = {
                "work_context": {
                    "work_id": "W99",
                    "work_name": "X",
                    "workspace_root": "/tmp",
                    "execution_workspace": "/tmp",
                    "evidence_root": "/tmp",
                    "authorized": True,
                },
                "execution_request": {"command": ["python3", "-c", "print(1)"]},
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
            self.assertEqual(ctx.exception.code, 403)
        finally:
            httpd.shutdown()
            httpd.server_close()


class GrantRegistryLoadTests(unittest.TestCase):
    def test_load_from_json_file(self):
        from execution_host.work28_grant_registry import load_grant_registry
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "grants.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "grant_id": "g-file",
                            "work_id": "28",
                            "entry_path": "a.py",
                            "operation": "RUN_SCRIPT",
                            "expected_source_sha256": "a" * 64,
                        }
                    ]
                ),
                encoding="utf-8",
            )
            reg = load_grant_registry(path=path)
            self.assertIn("g-file", reg)
            self.assertEqual(reg["g-file"].entry_path, "a.py")


if __name__ == "__main__":
    unittest.main()
