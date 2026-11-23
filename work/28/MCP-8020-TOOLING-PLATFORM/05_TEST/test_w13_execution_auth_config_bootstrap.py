"""Startup configuration tests for the Core-grant execution boundary."""
from __future__ import annotations

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from execution_host import server as eh_server
from execution_host.server import (
    AUTHORIZED_WORKS_ENV,
    AUTH_TOKEN_ENV,
    load_execution_auth_config,
    normalize_work_id,
)


class NormalizeWorkIdTests(unittest.TestCase):
    def test_canonical_work_ids_are_pinned_and_normalized(self):
        self.assertEqual(normalize_work_id("W28"), "W28")
        self.assertEqual(normalize_work_id(" w28 "), "W28")

    def test_non_canonical_work_ids_are_rejected(self):
        for value in ("28", "work28", "W", "W028x", "", "   ", None, 28):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_work_id(value)


class LoadExecutionAuthConfigTests(unittest.TestCase):
    def test_valid_configuration_loads_without_local_work_authority(self):
        cfg = load_execution_auth_config({
            AUTH_TOKEN_ENV: " trusted-token ",
            AUTHORIZED_WORKS_ENV: "W99",
        })
        self.assertEqual(cfg, {"auth_token": "trusted-token"})

    def test_missing_token_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
            load_execution_auth_config({AUTHORIZED_WORKS_ENV: "W28"})

    def test_blank_token_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
            load_execution_auth_config({AUTH_TOKEN_ENV: "   "})

    def test_local_work_allowlist_is_not_required(self):
        self.assertEqual(
            load_execution_auth_config({AUTH_TOKEN_ENV: "trusted-token"}),
            {"auth_token": "trusted-token"},
        )

    def test_token_value_never_leaks_into_error_messages(self):
        secret = "TOP-SECRET-DO-NOT-PRINT"
        with self.assertRaises(RuntimeError) as ctx:
            load_execution_auth_config({AUTH_TOKEN_ENV: " "})
        self.assertNotIn(secret, str(ctx.exception))


class MainWiringTests(unittest.TestCase):
    def test_main_passes_core_grant_source_to_serve(self):
        captured = {}
        real_serve = eh_server.serve
        real_build = eh_server.build_grant_source
        source = object()

        def fake_serve(host, port, auth_token, core_grant_source, **kwargs):
            captured.update(
                host=host, port=port, auth_token=auth_token,
                core_grant_source=core_grant_source, **kwargs,
            )

        eh_server.serve = fake_serve
        eh_server.build_grant_source = lambda: source
        saved = dict(os.environ)
        try:
            os.environ.clear()
            os.environ.update({
                AUTH_TOKEN_ENV: "trusted-token",
                AUTHORIZED_WORKS_ENV: "W28,W13",
                "ROOM_HOP_CORE_AUTHORITY_URL": "http://127.0.0.1:8000/core",
                "ROOM_HOP_CORE_SERVICE_IDENTITY": "mcp8020",
                "ROOM_HOP_CORE_SERVICE_CREDENTIAL": "service-credential",
            })
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                eh_server.main()
            output = buffer.getvalue()
        finally:
            os.environ.clear()
            os.environ.update(saved)
            eh_server.serve = real_serve
            eh_server.build_grant_source = real_build

        self.assertEqual(captured["auth_token"], "trusted-token")
        self.assertIs(captured["core_grant_source"], source)
        self.assertIs(captured["snapshot_only"], True)
        self.assertIn("Core online grant validation configured", output)
        self.assertNotIn("trusted-token", output)
        self.assertNotIn("service-credential", output)

    def test_main_refuses_to_start_without_configuration(self):
        saved = dict(os.environ)
        try:
            os.environ.clear()
            with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
                eh_server.main()
        finally:
            os.environ.clear()
            os.environ.update(saved)


if __name__ == "__main__":
    unittest.main()
