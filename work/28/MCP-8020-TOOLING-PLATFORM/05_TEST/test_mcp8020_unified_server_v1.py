"""OFF-01: direct tests for the mcp8020_unified_server_v1 factory.

Covers successful construction with complete providers and fail-closed
rejection when a required provider/handler is missing. The unified server
module imports the mcp package at import time; when mcp is unavailable
(CI contract runner without a requirements install) these tests skip and
no live-registration claim is made.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

try:
    import mcp  # noqa: F401
    HAS_MCP = True
except ImportError:
    HAS_MCP = False


class _CompleteProvider:
    """Answers every handler lookup with a callable echo handler."""

    def __getattr__(self, name):
        def handler(**kwargs):
            return {"echo": name}
        return handler


class _PartialGithubProvider:
    """Deliberately missing github_create_branch/create_file/update_file to prove fail-closed binding."""

    def github_repository(self, **kwargs):
        return {}

    def github_read_file(self, **kwargs):
        return {}

    def github_search_files(self, **kwargs):
        return {}


@unittest.skipUnless(HAS_MCP, "the mcp package is not installed; unified-server factory verification remains BLOCKED")
class UnifiedServerFactoryTests(unittest.TestCase):
    """OFF-01: create_work28_server() success and fail-closed binding."""

    def _complete_providers(self):
        return {
            "core": _CompleteProvider(),
            "sandbox": _CompleteProvider(),
            "sandbox_extensions": _CompleteProvider(),
            "proposals": _CompleteProvider(),
            "github": _CompleteProvider(),
            "runtime": _CompleteProvider(),
        }

    def test_factory_builds_server_with_complete_providers(self):
        from mcp8020_unified_server_v1 import create_work28_server
        server = create_work28_server(**self._complete_providers())
        self.assertEqual(server.name, "room-hop-work28-mcp8020")

    def test_factory_fail_closed_when_provider_is_none(self):
        from mcp8020_unified_server_v1 import Work28ProviderBlocked, create_work28_server
        providers = self._complete_providers()
        providers["sandbox"] = None
        with self.assertRaises(Work28ProviderBlocked):
            create_work28_server(**providers)

    def test_factory_fail_closed_when_handler_missing(self):
        from mcp8020_unified_server_v1 import Work28ProviderBlocked, create_work28_server
        providers = self._complete_providers()
        providers["github"] = _PartialGithubProvider()
        with self.assertRaises(Work28ProviderBlocked):
            create_work28_server(**providers)


if __name__ == "__main__":
    unittest.main()
