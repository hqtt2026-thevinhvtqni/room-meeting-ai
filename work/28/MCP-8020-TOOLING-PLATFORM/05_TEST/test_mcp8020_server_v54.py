"""MCP adapter smoke test. Skipped when the mcp package is unavailable (CI contract runner)."""
from __future__ import annotations
import sys
import tempfile
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

from mcp8020_room_tools_v54 import RoomProvider
from mcp8020_sandbox_tools_v54 import SandboxProvider
from mcp8020_service_v54 import create_v54_service

@unittest.skipUnless(HAS_MCP, "the mcp package is not installed; live MCP verification remains BLOCKED")
class ServerV54Tests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.service = create_v54_service(room=RoomProvider(), sandbox=SandboxProvider(self._tmp.name))

    def test_factory_returns_named_mcp_server(self):
        from mcp8020_server_v54 import create_work28_v54_server
        server = create_work28_v54_server(self.service)
        self.assertEqual(server.name, "room-hop-work28-mcp8020-v54")

if __name__ == "__main__":
    unittest.main()
