"""WP5 fail-closed regressions for online Core grant validation."""
from __future__ import annotations

import os
import unittest
from unittest.mock import Mock, patch
from urllib.error import URLError

from execution_host.server import main
from execution_host.work28_core_grant_client import (
    CORE_AUTHORITY_URL_ENV,
    CORE_SERVICE_IDENTITY_ENV,
    CORE_SERVICE_CREDENTIAL_ENV,
    HttpCoreGrantSource,
    RejectRedirectHandler,
    build_grant_source,
)
from execution_host.work28_grant import GrantError


VALID_ENV = {
    CORE_AUTHORITY_URL_ENV: "http://127.0.0.1:8000/core/execution-authority",
    CORE_SERVICE_IDENTITY_ENV: "mcp8020",
    CORE_SERVICE_CREDENTIAL_ENV: "test-service-credential",
}
VALID_GRANT_ID = "GRANT-12345678-1234-1234-1234-123456789abc"


class CoreGrantSourceFailClosedTests(unittest.TestCase):
    def test_missing_core_url_is_blocked(self):
        with self.assertRaisesRegex(GrantError, "core_authority_url_required"):
            build_grant_source(environ={})

    def test_missing_service_identity_or_credential_is_blocked(self):
        env = dict(VALID_ENV)
        env.pop(CORE_SERVICE_IDENTITY_ENV)
        with self.assertRaisesRegex(GrantError, "core_service_identity_required"):
            build_grant_source(environ=env)
        env = dict(VALID_ENV)
        env.pop(CORE_SERVICE_CREDENTIAL_ENV)
        with self.assertRaisesRegex(GrantError, "core_service_credential_required"):
            build_grant_source(environ=env)

    def test_configured_core_authority_selects_http_source(self):
        source = build_grant_source(environ=VALID_ENV)
        self.assertIsInstance(source, HttpCoreGrantSource)
        self.assertEqual(source.service_identity, "mcp8020")

    def test_remote_plain_http_core_url_is_rejected(self):
        env = dict(VALID_ENV)
        env[CORE_AUTHORITY_URL_ENV] = "http://core.example:8000/core"
        with self.assertRaisesRegex(GrantError, "core_authority_https_required"):
            build_grant_source(environ=env)

    def test_core_url_with_userinfo_is_rejected(self):
        env = dict(VALID_ENV)
        env[CORE_AUTHORITY_URL_ENV] = "https://user:secret@core.example/core"
        with self.assertRaisesRegex(GrantError, "core_authority_url_invalid"):
            build_grant_source(environ=env)

    def test_core_url_with_query_is_rejected(self):
        env = dict(VALID_ENV)
        env[CORE_AUTHORITY_URL_ENV] = "https://core.example/core?access_token=secret"
        with self.assertRaisesRegex(GrantError, "core_authority_url_invalid"):
            build_grant_source(environ=env)

    def test_redirect_handler_refuses_all_redirect_destinations(self):
        handler = RejectRedirectHandler()
        self.assertIsNone(handler.redirect_request(
            None, None, 302, "Found", {}, "https://attacker.example/steal"
        ))

    def test_unreachable_core_does_not_return_local_grants(self):
        source = HttpCoreGrantSource("http://127.0.0.1:1/core", "mcp8020", "credential", timeout=0.01)
        with patch("urllib.request.OpenerDirector.open", side_effect=URLError("offline")):
            with self.assertRaisesRegex(GrantError, "core_authority_unreachable"):
                source.fetch_grant("W28", VALID_GRANT_ID, "grant-token")

    def test_server_startup_fails_closed_when_core_source_configuration_fails(self):
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test"},
        ), patch(
            "execution_host.server.build_grant_source",
            side_effect=GrantError("core_authority_unreachable"),
        ), patch("execution_host.server.serve") as serve, patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(GrantError, "core_authority_unreachable"):
                main()
        serve.assert_not_called()


class CorePerRequestModeTests(unittest.TestCase):
    def test_main_passes_core_source_without_preloading_grant_list(self):
        source = Mock()
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test"},
        ), patch("execution_host.server.build_grant_source", return_value=source), patch(
            "execution_host.server.serve"
        ) as serve, patch.dict(os.environ, {}, clear=True):
            main()
        self.assertIs(serve.call_args.kwargs["core_grant_source"], source)
        self.assertIs(serve.call_args.kwargs["snapshot_only"], True)
        self.assertFalse(hasattr(source, "fetch_grants") and source.fetch_grants.called)

    def test_snapshot_only_environment_cannot_enable_legacy_command_mode(self):
        source = Mock()
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test"},
        ), patch("execution_host.server.build_grant_source", return_value=source), patch(
            "execution_host.server.serve"
        ) as serve, patch.dict(os.environ, {"ROOM_HOP_SNAPSHOT_ONLY": "false"}, clear=True):
            main()
        self.assertIs(serve.call_args.kwargs["snapshot_only"], True)


if __name__ == "__main__":
    unittest.main()
