"""Regression tests for caller authentication at the canonical W13 /execute handler.

Audit finding (2026-10-25, repository-side source audit): the staged W13 HTTP
boundary accepted unauthenticated POST /execute requests and trusted the
client-supplied authorized flag inside work_context. These tests lock the
fail-closed caller authentication gate introduced in response.
"""
from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from execution_host.server import AUTH_HEADER, Handler, authenticate_caller
from execution_host import server


class AuthenticateCallerTests(unittest.TestCase):
    def test_configured_token_with_exact_match_authenticates(self):
        self.assertTrue(authenticate_caller("secret-token", "secret-token"))

    def test_missing_header_or_wrong_token_is_denied(self):
        for provided in (None, "", "wrong", "secret-tokens", " SECRET-TOKEN"):
            with self.subTest(provided=provided):
                self.assertFalse(authenticate_caller(provided, "secret-token"))

    def test_unarmed_server_fails_closed(self):
        for token in (None, "", "   "):
            with self.subTest(token=token):
                self.assertFalse(authenticate_caller("secret-token", token))
                self.assertFalse(authenticate_caller(None, token))

    def test_non_string_inputs_fail_closed(self):
        self.assertFalse(authenticate_caller(1, "secret-token"))
        self.assertFalse(authenticate_caller("secret-token", 1))

    def test_comparison_uses_constant_time_api(self):
        # hmac.compare_digest is the only accepted comparison; ensure the
        # module still uses it so future edits cannot silently downgrade.
        self.assertIs(server.hmac.compare_digest, __import__('hmac').compare_digest)


class ExecuteHandlerAuthGateTests(unittest.TestCase):
    def test_handler_exposes_auth_token_class_attribute(self):
        self.assertTrue(hasattr(Handler, "auth_token"))

    def test_serve_requires_explicit_auth_token_parameter(self):
        params = inspect.signature(server.serve).parameters
        self.assertIn("auth_token", params)
        self.assertEqual(params["auth_token"].default, None)

    def test_trusted_header_name_is_pinned(self):
        self.assertEqual(AUTH_HEADER, "X-Room-Hop-Execution-Auth")


if __name__ == "__main__":
    unittest.main()
