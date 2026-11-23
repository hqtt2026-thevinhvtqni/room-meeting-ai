"""WP15: Execution Host caller auth + per-Work authorization (fail-closed)."""
from __future__ import annotations

import unittest

from execution_host.server import (
    AUTH_TOKEN_ENV,
    AUTHORIZED_WORKS_ENV,
    authenticate_caller,
    authorize_work,
    load_execution_auth_config,
    normalize_work_id,
)


class NormalizeWorkIdTests(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(normalize_work_id("w28"), "W28")
        self.assertEqual(normalize_work_id("W12"), "W12")

    def test_rejects_bad(self):
        for bad in ("", "28", "WORK28", "W", "W-28", 28):
            with self.assertRaises((ValueError, TypeError)):
                normalize_work_id(bad)  # type: ignore[arg-type]


class AuthenticateCallerTests(unittest.TestCase):
    def test_match(self):
        self.assertTrue(authenticate_caller("secret-token", "secret-token"))

    def test_mismatch_and_empty(self):
        self.assertFalse(authenticate_caller("a", "b"))
        self.assertFalse(authenticate_caller("", "token"))
        self.assertFalse(authenticate_caller("token", ""))
        self.assertFalse(authenticate_caller(None, "token"))  # type: ignore[arg-type]
        self.assertFalse(authenticate_caller("token", None))  # type: ignore[arg-type]


class AuthorizeWorkTests(unittest.TestCase):
    def test_allow_listed(self):
        works = frozenset({"W28", "W12"})
        self.assertTrue(authorize_work("W28", works))
        self.assertTrue(authorize_work("w28", works))

    def test_not_listed_or_unarmed(self):
        works = frozenset({"W28"})
        self.assertFalse(authorize_work("W99", works))
        self.assertFalse(authorize_work("W28", None))  # type: ignore[arg-type]
        self.assertFalse(authorize_work("W28", frozenset()))
        self.assertFalse(authorize_work("28", works))


class LoadAuthConfigTests(unittest.TestCase):
    def test_loads(self):
        env = {
            AUTH_TOKEN_ENV: " deploy-token ",
            AUTHORIZED_WORKS_ENV: "W99",
        }
        cfg = load_execution_auth_config(env)
        self.assertEqual(cfg, {"auth_token": "deploy-token"})

    def test_missing_token_is_blocked_but_local_work_allowlist_is_not_required(self):
        with self.assertRaises(RuntimeError):
            load_execution_auth_config({AUTHORIZED_WORKS_ENV: "W28"})
        self.assertEqual(
            load_execution_auth_config({AUTH_TOKEN_ENV: "t"}),
            {"auth_token": "t"},
        )


if __name__ == "__main__":
    unittest.main()
