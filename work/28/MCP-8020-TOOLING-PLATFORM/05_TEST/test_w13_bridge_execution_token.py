"""Execution token wiring tests for the WEE -> W13 bridge.

After the W13 /execute boundary was hardened (caller authentication +
per-Work allow-list), the WEE bridge still POSTed without the trusted
token, so every real call would now receive 401. These tests lock:

* the bridge sends the deployment token via the pinned auth header;
* a missing token sends no header (fail-closed server will reject);
* the token is taken from ROOM_HOP_EXECUTION_AUTH_TOKEN by default;
* HTTP status failures surface as execution_host_http_<code> (not as
  unreachable), and the token value never leaks into any blocker.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from urllib import error as urllib_error

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from execution_host import wee_bridge
from execution_host.wee_bridge import ExecutionHostBridge
from execution_host.server import AUTH_HEADER


class _Response:
    def __init__(self, status, payload):
        self.status = status
        self._payload = payload
    def read(self):
        return self._payload
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False


class _UrllibFake:
    def __init__(self, status=200, payload=None, http_error=None):
        self.captured = []
        self.status = status
        self.payload = payload or {}
        self.http_error = http_error
    def Request(self, url, data=None, headers=None, method=None):
        self.captured.append({'url': url, 'data': data,
                              'headers': dict(headers or {}), 'method': method})
        return SimpleNamespace(url=url)
    def urlopen(self, req, timeout=None):
        if self.http_error is not None:
            raise self.http_error
        return _Response(self.status, json.dumps(self.payload).encode())


def context():
    return {'work_id': 'W28', 'work_name': 'MCP-TOOLING',
            'workspace_root': '/w', 'execution_workspace': '/w/run',
            'evidence_root': '/w/evidence', 'authorized': True,
            'execution_id': 'exec-1'}


def request_body():
    return {'command': ['python3', '-c', 'print(1)'], 'timeout_seconds': 10}


class BridgeExecutionTokenTests(unittest.TestCase):
    def setUp(self):
        import os
        self._saved_env = dict(os.environ)
        os.environ.pop('ROOM_HOP_EXECUTION_AUTH_TOKEN', None)
        os.environ.pop('EXECUTION_HOST_URL', None)
    def tearDown(self):
        import os
        os.environ.clear()
        os.environ.update(self._saved_env)

    def patch_urllib(self, **kwargs):
        fake = _UrllibFake(**kwargs)
        self._real_request = wee_bridge.request
        wee_bridge.request = fake
        self.addCleanup(setattr, wee_bridge, 'request', self._real_request)
        return fake

    def invoke(self, fake, **bridge_kwargs):
        bridge = ExecutionHostBridge(transport=None, **bridge_kwargs)
        return bridge.invoke(context(), request_body())

    def test_sends_deployment_token_in_pinned_header(self):
        fake = self.patch_urllib(payload={'status': 'PASS', 'exit_code': 0})
        result = self.invoke(fake, auth_token='secret-token')
        headers = fake.captured[0]['headers']
        self.assertEqual(headers.get(AUTH_HEADER), 'secret-token')
        self.assertEqual(result.status, 'PASS')

    def test_without_token_no_auth_header_is_sent(self):
        fake = self.patch_urllib(payload={'status': 'PASS', 'exit_code': 0})
        result = self.invoke(fake)
        self.assertNotIn(AUTH_HEADER, fake.captured[0]['headers'])
        self.assertEqual(result.status, 'PASS')

    def test_token_defaults_to_environment_variable(self):
        import os
        os.environ['ROOM_HOP_EXECUTION_AUTH_TOKEN'] = 'env-token'
        fake = self.patch_urllib(payload={'status': 'PASS', 'exit_code': 0})
        self.invoke(fake)
        self.assertEqual(fake.captured[0]['headers'].get(AUTH_HEADER), 'env-token')

    def test_http_401_surfaces_exact_code_and_not_unreachable(self):
        fake = self.patch_urllib(
            http_error=urllib_error.HTTPError(
                'http://127.0.0.1:8031/execute', 401,
                'caller_authentication_failed', None, None))
        result = self.invoke(fake, auth_token='secret-token')
        self.assertEqual(result.status, 'BLOCKED')
        self.assertEqual(result.blocker, 'execution_host_http_401')

    def test_http_403_surfaces_exact_code(self):
        fake = self.patch_urllib(
            http_error=urllib_error.HTTPError(
                'http://127.0.0.1:8031/execute', 403,
                'caller_not_authorized_for_work', None, None))
        result = self.invoke(fake, auth_token='secret-token')
        self.assertEqual(result.blocker, 'execution_host_http_403')

    def test_token_value_never_leaks_into_blockers(self):
        fake = self.patch_urllib(
            http_error=urllib_error.HTTPError(
                'http://127.0.0.1:8031/execute', 401,
                'caller_authentication_failed', None, None))
        result = self.invoke(fake, auth_token='secret-token')
        self.assertNotIn('secret-token', result.blocker or '')
        self.assertNotIn('secret-token', json.dumps(result.as_dict()))


if __name__ == "__main__":
    unittest.main()
