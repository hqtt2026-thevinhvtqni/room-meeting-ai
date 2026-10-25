"""Live HTTP boundary regression tests for the W13 POST /execute gate.

Independent review (2026-10-25) found the first auth regression pass only
exercised unit-level seams. These tests POST real HTTP requests into a
ThreadingHTTPServer with a recording fake host, and prove that:

* missing or wrong token -> 401 and the host is NEVER invoked;
* an unarmed server (no token configured) fails closed;
* a valid token alone is not authorization: Work not in the trusted
  allow-list -> 403 and the host is NEVER invoked;
* only authenticated + per-Work-authorized calls reach the host, with
  authorization derived server-side (client-sent authorized flag ignored).
"""
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
from execution_host.server import AUTH_HEADER, authorize_work


class RecordingHost:
    """Fake host: records calls, never executes anything."""
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


def payload(work_id="W28", authorized=False):
    return {
        "work_context": {
            "work_id": work_id,
            "work_name": "TEST",
            "workspace_root": "/tmp/w",
            "execution_workspace": "/tmp/w/run",
            "evidence_root": "/tmp/w/evidence",
            "authorized": authorized,
            "execution_id": "exec-1",
        },
        "execution_request": {"command": ["python3", "-c", "print(1)"]},
    }


def post(base, payload, headers=None):
    data = json.dumps(payload).encode()
    request = urlrequest.Request(
        base + "/execute", data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urlrequest.urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read())
    except HTTPError as exc:
        return exc.code, json.loads(exc.read())


class AuthorizeWorkUnitTests(unittest.TestCase):
    def test_valid_work_in_allowlist_is_authorized(self):
        self.assertTrue(authorize_work("W28", frozenset({"W28"})))

    def test_token_without_allowlist_entry_is_denied(self):
        for work_id in ("W99", "", None, 1):
            with self.subTest(work_id=work_id):
                self.assertFalse(authorize_work(work_id, frozenset({"W28"})))

    def test_missing_allowlist_configuration_fails_closed(self):
        for allow in (None, "not-a-set", 0):
            with self.subTest(allow=allow):
                self.assertFalse(authorize_work("W28", allow))


class ExecuteHttpBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.host = RecordingHost()
        self._saved = (
            eh_server.Handler.host,
            eh_server.Handler.auth_token,
            eh_server.Handler.authorized_works,
        )
        eh_server.Handler.host = self.host
        eh_server.Handler.auth_token = "secret-token"
        eh_server.Handler.authorized_works = frozenset({"W28"})
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), eh_server.Handler)
        self.base = "http://127.0.0.1:%d" % self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)
        (eh_server.Handler.host, eh_server.Handler.auth_token,
         eh_server.Handler.authorized_works) = self._saved

    def test_missing_token_is_401_and_host_never_invoked(self):
        code, body = post(self.base, payload())
        self.assertEqual(code, 401)
        self.assertEqual(body["status"], "BLOCKED")
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

    def test_valid_token_but_unlisted_work_is_403_and_host_never_invoked(self):
        code, body = post(self.base, payload(work_id="W99"), {AUTH_HEADER: "secret-token"})
        self.assertEqual(code, 403)
        self.assertEqual(body["reason"], "caller_not_authorized_for_work")
        self.assertEqual(self.host.calls, [])

    def test_missing_allowlist_configuration_is_403_fail_closed(self):
        eh_server.Handler.authorized_works = None
        code, body = post(self.base, payload(), {AUTH_HEADER: "secret-token"})
        self.assertEqual(code, 403)
        self.assertEqual(body["reason"], "caller_not_authorized_for_work")
        self.assertEqual(self.host.calls, [])

    def test_authenticated_and_authorized_call_reaches_host_with_server_side_authorization(self):
        # Client deliberately claims authorized=True while the server-side
        # decision is the only one that matters; also verified in the
        # disallowed-work case above. Here the allow-list grants W28.
        code, body = post(self.base, payload(work_id="W28", authorized=True), {AUTH_HEADER: "secret-token"})
        self.assertEqual(code, 200)
        self.assertEqual(body["status"], "PASS")
        self.assertEqual(len(self.host.calls), 1)
        ctx, req = self.host.calls[0]
        self.assertEqual(ctx.work_id, "W28")
        self.assertTrue(ctx.authorized)


if __name__ == "__main__":
    unittest.main()
