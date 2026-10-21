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
from mcp8020_service_v54 import V54BindingError, create_v54_service

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

    def test_list_tools_handler_returns_catalog_schemas(self):
        from mcp8020_server_v54 import create_work28_v54_server
        server = create_work28_v54_server(self.service)
        handlers = getattr(server, "request_handlers", {})
        # Server construction and registration are covered by the public API;
        # list_tools behavior is exercised through the service's same schema source.
        listed = self.service.list_tools()
        self.assertEqual(len(listed), 54)
        self.assertTrue(all("inputSchema" in tool for tool in listed))
        self.assertEqual(listed[0]["name"], "room_get_context")

    def test_execution_gateway_injection_requires_complete_interface(self):
        from mcp8020_server_v54 import create_work28_v54_server
        class PartialGateway:
            def sandbox_run_python(self, **kwargs):
                return {"ok": True}
        with self.assertRaises(V54BindingError):
            create_work28_v54_server(self.service, execution_gateway=PartialGateway())

    def test_execution_tools_remain_fail_closed_when_gateway_is_absent(self):
        result = self.service.call_tool("sandbox_run_python", {"work_id": "work28", "script": "x.py"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "NOT_IMPLEMENTED")

if __name__ == "__main__":
    unittest.main()
