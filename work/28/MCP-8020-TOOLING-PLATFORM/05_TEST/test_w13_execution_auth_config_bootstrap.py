"""Startup configuration wiring tests for the W13 execution boundary.

Independent review (2026-10-25) required that the entrypoint explicitly load
the trusted configuration: setting the environment variables alone must be
provable to reach serve(), missing or malformed configuration must fail
loudly at startup, the Work id format must be pinned, and the token value
must never appear in messages, logs, or evidence.
"""
from __future__ import annotations

import io
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
        self.assertEqual(normalize_work_id('W28'), 'W28')
        self.assertEqual(normalize_work_id(' w28 '), 'W28')

    def test_non_canonical_work_ids_are_rejected(self):
        for value in ('28', 'work28', 'W', 'W028x', '', '   ', None, 28):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_work_id(value)


class LoadExecutionAuthConfigTests(unittest.TestCase):
    def env(self, token='trusted-token', works='W28'):
        return {AUTH_TOKEN_ENV: token, AUTHORIZED_WORKS_ENV: works}

    def test_valid_configuration_loads(self):
        config = load_execution_auth_config(self.env(works='W28, W13'))
        self.assertEqual(config['auth_token'], 'trusted-token')
        self.assertEqual(config['authorized_works'], frozenset({'W28', 'W13'}))

    def test_missing_token_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
            load_execution_auth_config({AUTHORIZED_WORKS_ENV: 'W28'})

    def test_blank_token_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
            load_execution_auth_config(self.env(token='   '))

    def test_missing_allowlist_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, AUTHORIZED_WORKS_ENV):
            load_execution_auth_config(self.env(works=''))

    def test_malformed_work_id_fails_loudly_and_pins_format(self):
        # '28' is deliberately rejected: the canonical form is W28.
        with self.assertRaisesRegex(ValueError, 'W<number>'):
            load_execution_auth_config(self.env(works='W28, 28'))

    def test_token_value_never_leaks_into_error_messages(self):
        secret = 'TOP-SECRET-DO-NOT-PRINT'
        try:
            load_execution_auth_config(self.env(token=secret, works='28'))
            self.fail('expected failure')
        except (RuntimeError, ValueError) as exc:
            self.assertNotIn(secret, str(exc))


class MainWiringTests(unittest.TestCase):
    def test_main_passes_loaded_configuration_to_serve(self):
        captured = {}
        real_serve = eh_server.serve

        def fake_serve(host, port, auth_token, authorized_works):
            captured.update(host=host, port=port,
                             auth_token=auth_token, authorized_works=authorized_works)

        eh_server.serve = fake_serve
        env = {AUTH_TOKEN_ENV: 'trusted-token', AUTHORIZED_WORKS_ENV: 'W28, W13'}
        original = dict
        try:
            import os
            saved = dict(os.environ)
            os.environ.clear()
            os.environ.update(env)
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                eh_server.main()
            output = buffer.getvalue()
        finally:
            os.environ.clear()
            os.environ.update(saved)
            eh_server.serve = real_serve
        self.assertEqual(captured['auth_token'], 'trusted-token')
        self.assertEqual(captured['authorized_works'], frozenset({'W28', 'W13'}))
        # Startup announces the armed works but never the token.
        self.assertIn('W28', output)
        self.assertIn('W13', output)
        self.assertNotIn('trusted-token', output)

    def test_main_refuses_to_start_without_configuration(self):
        import os
        saved = dict(os.environ)
        os.environ.pop(AUTH_TOKEN_ENV, None)
        os.environ.pop(AUTHORIZED_WORKS_ENV, None)
        try:
            with self.assertRaisesRegex(RuntimeError, AUTH_TOKEN_ENV):
                eh_server.main()
        finally:
            os.environ.clear()
            os.environ.update(saved)


if __name__ == "__main__":
    unittest.main()
