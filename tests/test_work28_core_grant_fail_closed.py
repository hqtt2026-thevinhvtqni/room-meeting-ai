"""WP5 fail-closed regressions for Core grant authority and command mode defaults."""
from __future__ import annotations

import os
import unittest
from unittest.mock import Mock, patch
from urllib.error import URLError

from execution_host.server import main
from execution_host.work28_core_grant_client import (
    CORE_GRANT_URL_ENV,
    HttpCoreGrantSource,
    build_grant_source,
)
from execution_host.work28_grant import GrantError


class CoreGrantSourceFailClosedTests(unittest.TestCase):
    def test_missing_core_url_is_blocked_not_local_file_fallback(self):
        with self.assertRaisesRegex(GrantError, "core_grant_url_required"):
            build_grant_source(environ={})

    def test_configured_https_core_url_selects_http_source(self):
        source = build_grant_source(environ={CORE_GRANT_URL_ENV: "https://core.example.test/grants"})
        self.assertIsInstance(source, HttpCoreGrantSource)

    def test_plain_http_core_url_is_rejected(self):
        with self.assertRaisesRegex(GrantError, "core_grant_url_must_be_https"):
            build_grant_source(environ={CORE_GRANT_URL_ENV: "http://127.0.0.1:8000/grants"})

    def test_core_url_with_userinfo_query_or_fragment_is_rejected(self):
        for url in (
            "https://user:pass@core.example.test/grants",
            "https://core.example.test/grants?token=secret",
            "https://core.example.test/grants#fragment",
        ):
            with self.subTest(url=url), self.assertRaisesRegex(GrantError, "core_grant_url_must_be_https"):
                HttpCoreGrantSource(url)

    def test_unreachable_core_does_not_return_local_grants(self):
        source = HttpCoreGrantSource("https://core.example.test/grants", timeout=0.01)
        opener = Mock()
        opener.open.side_effect = URLError("offline")
        with patch("urllib.request.build_opener", return_value=opener):
            with self.assertRaisesRegex(GrantError, "core_grant_unreachable"):
                source.fetch_grants()
        opener.open.assert_called_once()

    def test_redirect_is_rejected_without_following_destination(self):
        from execution_host.work28_core_grant_client import _NoRedirectHandler
        handler = _NoRedirectHandler()
        req = Mock()
        self.assertIsNone(
            handler.redirect_request(
                req, Mock(), 302, "Found", {"Location": "https://attacker.example/steal"}, 
                "https://attacker.example/steal",
            )
        )

    def test_server_startup_fails_closed_when_core_grant_source_fails(self):
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test", "authorized_works": frozenset({"W28"})},
        ), patch(
            "execution_host.server.build_grant_source",
            side_effect=GrantError("core_grant_unreachable"),
        ), patch("execution_host.server.serve") as serve, patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(GrantError, "core_grant_unreachable"):
                main()
        serve.assert_not_called()


class SnapshotOnlyDefaultTests(unittest.TestCase):
    def test_unset_snapshot_only_defaults_to_true(self):
        source = Mock()
        source.fetch_grants.return_value = {}
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test", "authorized_works": frozenset({"W28"})},
        ), patch("execution_host.server.build_grant_source", return_value=source), patch(
            "execution_host.server.serve"
        ) as serve, patch.dict(os.environ, {}, clear=True):
            main()
        self.assertIs(serve.call_args.kwargs["snapshot_only"], True)

    def test_explicit_false_cannot_enable_command_mode(self):
        source = Mock()
        source.fetch_grants.return_value = {}
        with patch(
            "execution_host.server.load_execution_auth_config",
            return_value={"auth_token": "test", "authorized_works": frozenset({"W28"})},
        ), patch("execution_host.server.build_grant_source", return_value=source), patch(
            "execution_host.server.serve"
        ) as serve, patch.dict(os.environ, {"ROOM_HOP_SNAPSHOT_ONLY": "false"}, clear=True):
            main()
        self.assertIs(serve.call_args.kwargs["snapshot_only"], True)


if __name__ == "__main__":
    unittest.main()
