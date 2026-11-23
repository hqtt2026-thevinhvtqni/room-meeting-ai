"""Live HTTP boundary tests: execution requires a Core-issued scoped grant."""
from __future__ import annotations

import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import HTTPError

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from execution_host import server as eh_server
from execution_host.models import ExecutionResult
from execution_host.server import AUTH_HEADER, GRANT_TOKEN_HEADER, authorize_work
from execution_host.work28_grant import GrantError


class RecordingHost:
    provider_type = "FAKE_TEST_HOST"

    def __init__(self):
        self.calls = []

    def execute_work(self, ctx, req):
        self.calls.append((ctx, req))
        return ExecutionResult(
            execution_id=ctx.execution_id or "exec-1",
            work_id=ctx.work_id,
            status="PASS",
            exit_code=0,
        )


class DenyCoreGrantSource:
    def fetch_grant(self, work_id, grant_id, grant_token):
        raise GrantError("core_authority_denied:work_not_authorized")

    def record_run(self, **kwargs):
        raise AssertionError("record_run must not run after grant denial")


def payload(work_id="W28"):
    return {
        "work_id": work_id,
        "grant_id": "GRANT-12345678-1234-1234-1234-123456789abc",
        "work28_request": {
            "work_id": work_id,
            "entry_path": "src/main.py",
            "operation": "RUN_SCRIPT",
            "expected_source_sha256": "a" * 64,
            "timeout_seconds": 30,
        },
    }


def legacy_payload():
    return {
        "work_context": {
            "work_id": "W28", "work_name": "TEST",
            "workspace_root": "/tmp/w", "execution_workspace": "/tmp/w/run",
            "evidence_root": "/tmp/w/evidence", "authorized": True,
            "execution_id": "exec-1",
        },
        "execution_request": {"command": ["python3", "-c", "print(1)"]},
    }


def post(base, body, headers=None):
    req = urlrequest.Request(
        base + "/execute", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=5) as response:
            return response.status, json.loads(response.read())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read())


class AuthorizeWorkUnitTests(unittest.TestCase):
    def test_legacy_local_allowlist_helper_is_not_authority(self):
        self.assertTrue(authorize_work("W28", frozenset({"W28"})))
        self.assertFalse(authorize_work("W99", frozenset({"W28"})))
        self.assertFalse(authorize_work("W28", None))


class ExecuteHttpBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.host = RecordingHost()
        self._saved = (
            eh_server.Handler.host,
            eh_server.Handler.auth_token,
            eh_server.Handler.authorized_works,
            eh_server.Handler.snapshot_only,
            eh_server.Handler.core_grant_source,
        )
        eh_server.Handler.host = self.host
        eh_server.Handler.auth_token = "secret-token"
        eh_server.Handler.authorized_works = None
        eh_server.Handler.snapshot_only = False
        eh_server.Handler.core_grant_source = None
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), eh_server.Handler)
        self.base = "http://127.0.0.1:%d" % self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)
        (
            eh_server.Handler.host,
            eh_server.Handler.auth_token,
            eh_server.Handler.authorized_works,
            eh_server.Handler.snapshot_only,
            eh_server.Handler.core_grant_source,
        ) = self._saved

    def test_missing_token_is_401_and_host_never_invoked(self):
        code, body = post(self.base, payload())
        self.assertEqual(code, 401)
        self.assertEqual(body["reason"], "caller_authentication_failed")
        self.assertEqual(self.host.calls, [])

    def test_wrong_token_is_401_and_host_never_invoked(self):
        code, body = post(self.base, payload(), {AUTH_HEADER: "wrong-token"})
        self.assertEqual(code, 401)
        self.assertEqual(body["reason"], "caller_authentication_failed")
        self.assertEqual(self.host.calls, [])

    def test_unarmed_server_fails_closed_over_live_http(self):
        eh_server.Handler.auth_token = None
        code, body = post(self.base, payload(), {AUTH_HEADER: "secret-token"})
        self.assertEqual(code, 401)
        self.assertEqual(body["reason"], "caller_authentication_failed")
        self.assertEqual(self.host.calls, [])

    def test_valid_transport_token_without_core_source_is_503(self):
        code, body = post(
            self.base, payload(),
            {AUTH_HEADER: "secret-token", GRANT_TOKEN_HEADER: "grant-token"},
        )
        self.assertEqual(code, 503)
        self.assertEqual(body["reason"], "core_grant_source_not_configured")
        self.assertEqual(self.host.calls, [])

    def test_core_denial_is_403_and_host_never_invoked(self):
        eh_server.Handler.core_grant_source = DenyCoreGrantSource()
        code, body = post(
            self.base, payload("W99"),
            {AUTH_HEADER: "secret-token", GRANT_TOKEN_HEADER: "grant-token"},
        )
        self.assertEqual(code, 403)
        self.assertIn("core_authority_denied", body["reason"])
        self.assertEqual(self.host.calls, [])

    def test_caller_supplied_work_context_and_command_are_rejected(self):
        code, body = post(
            self.base, legacy_payload(),
            {AUTH_HEADER: "secret-token", GRANT_TOKEN_HEADER: "grant-token"},
        )
        self.assertEqual(code, 400)
        self.assertIn("unknown_body_keys", body["reason"])
        self.assertEqual(self.host.calls, [])


if __name__ == "__main__":
    unittest.main()
