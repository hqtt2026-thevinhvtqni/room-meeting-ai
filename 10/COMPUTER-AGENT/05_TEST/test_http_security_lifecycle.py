from __future__ import annotations

import json
import os
import sys
import threading
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer

PROJECT = Path(__file__).resolve().parent.parent
CODE = PROJECT / "04_CODE"
sys.path.insert(0, str(CODE))

import agent_api


TOKEN = "test-only-token-never-use-in-production"
ORIGIN = "http://127.0.0.1:3000"


class RecordingAdapter:
    def __init__(self, entered=None, release=None):
        self.entered = entered
        self.release = release
        self.closed = False
        self.calls = []

    def start(self):
        self.calls.append("start")

    def click(self, target):
        self.calls.append(("click", target))
        if self.entered:
            self.entered.set()
        if self.release:
            if not self.release.wait(3):
                raise TimeoutError("test adapter release timed out")
        return {"clicked": target}

    def close(self):
        self.closed = True
        self.calls.append("close")


class HttpSecurityLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {
            "COMPUTER_AGENT_TOKEN": TOKEN,
            "COMPUTER_AGENT_ALLOWED_ORIGINS": ORIGIN,
            "COMPUTER_AGENT_MAX_BODY_BYTES": "1048576",
            "COMPUTER_AGENT_MAX_ACTIONS": "100",
        }, clear=False)
        self.env.start()
        self.adapters = []
        self.factory_patch = patch.object(
            agent_api, "build_adapter", side_effect=self._build_adapter
        )
        self.factory_patch.start()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), agent_api.Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.factory_patch.stop()
        self.env.stop()

    def _build_adapter(self):
        adapter = self.adapter_factory()
        self.adapters.append(adapter)
        return adapter

    def adapter_factory(self):
        return RecordingAdapter()

    def _request(self, payload=None, *, token=TOKEN, origin=ORIGIN, content_type="application/json"):
        data = json.dumps(payload or {
            "task": "click once",
            "actions": [{"type": "click", "target": "Go"}],
        }).encode()
        headers = {"Content-Type": content_type, "Content-Length": str(len(data))}
        if token is not None:
            headers["Authorization"] = f"Bearer {token}"
        if origin is not None:
            headers["Origin"] = origin
        req = urllib.request.Request(self.base + "/agent/execute", data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status, response.headers, response.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.headers, exc.read()

    def test_missing_and_wrong_token_fail_closed(self):
        self.assertEqual(self._request(token=None)[0], 401)
        self.assertEqual(self._request(token="wrong")[0], 401)
        self.assertEqual(self.adapters, [])

    def test_hostile_origin_rejected_before_adapter_creation(self):
        status, _, body = self._request(origin="https://evil.example")
        self.assertEqual(status, 403)
        self.assertIn(b"origin_not_allowed", body)
        self.assertEqual(self.adapters, [])

    def test_non_json_rejected_before_adapter_creation(self):
        self.assertEqual(self._request(content_type="text/plain")[0], 400)
        self.assertEqual(self.adapters, [])

    def test_empty_verification_is_rejected_before_adapter_creation(self):
        payload = {"task": "invalid verification", "actions": [{"type": "click", "target": "Go"}],
                   "verification": {"checks": []}}
        status, _, body = self._request(payload)
        self.assertEqual(status, 400)
        self.assertIn(b"verification_checks_must_be_non_empty_list", body)
        self.assertEqual(self.adapters, [])

    def test_approved_origin_gets_exact_cors_header(self):
        status, headers, _ = self._request()
        self.assertEqual(status, 200)
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), ORIGIN)
        self.assertEqual(self.adapters[0].calls[-1], "close")
        self.assertTrue(self.adapters[0].closed)

    def test_adapter_close_failure_does_not_return_pass(self):
        class CloseFailAdapter(RecordingAdapter):
            def close(self):
                raise RuntimeError("close failed")
        with patch.object(agent_api, "build_adapter", return_value=CloseFailAdapter()):
            status, _, body = self._request()
        self.assertEqual(status, 500)
        self.assertIn(b"adapter_close_failed", body)

    def test_process_wide_lease_blocks_second_http_request_until_close(self):
        entered = threading.Event()
        release = threading.Event()
        first_adapter = RecordingAdapter(entered, release)
        created = []

        def factory():
            created.append(first_adapter if not created else RecordingAdapter())
            return created[-1]

        with patch.object(agent_api, "build_adapter", side_effect=factory):
            first_result = {}
            def first_request():
                first_result["response"] = self._request()
            request_thread = threading.Thread(target=first_request, daemon=True)
            request_thread.start()
            self.assertTrue(entered.wait(2), "first request did not enter adapter")
            second_status, _, second_body = self._request()
            self.assertEqual(second_status, 409)
            self.assertIn(b"execution_busy", second_body)
            self.assertEqual(len(created), 1, "second request must not construct an adapter")
            self.assertFalse(first_adapter.closed, "adapter closed while action still active")
            release.set()
            request_thread.join(timeout=5)
            self.assertFalse(request_thread.is_alive())
            self.assertEqual(first_result["response"][0], 200)
            self.assertTrue(first_adapter.closed)
            self.assertEqual(first_adapter.calls.count(("click", "Go")), 1)
            self.assertEqual(first_adapter.calls[-1], "close")


if __name__ == "__main__":
    unittest.main(verbosity=2)
