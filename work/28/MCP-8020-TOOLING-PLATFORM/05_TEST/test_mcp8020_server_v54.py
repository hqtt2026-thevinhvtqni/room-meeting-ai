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

    def test_list_tools_handler_returns_54_catalog_entries(self):
        import asyncio
        from mcp.types import ListToolsRequest
        from mcp8020_server_v54 import create_work28_v54_server
        server = create_work28_v54_server(self.service)
        handler = server.request_handlers[ListToolsRequest]
        result = asyncio.run(handler(ListToolsRequest(method="tools/list")))
        tools = result.root.tools
        self.assertEqual(len(tools), 54)
        self.assertEqual(tools[0].name, "room_get_context")

    def test_call_tool_handler_returns_honest_not_implemented_envelope(self):
        import asyncio, json
        from mcp.types import CallToolRequest
        from mcp8020_server_v54 import create_work28_v54_server
        server = create_work28_v54_server(self.service)
        handler = server.request_handlers[CallToolRequest]
        request = CallToolRequest(method="tools/call",
                                  params={"name": "sandbox_run_python",
                                          "arguments": {"work_id": "w1", "script": "main.py"}})
        result = asyncio.run(handler(request))
        payload = json.loads(result.root.content[0].text)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "NOT_IMPLEMENTED")
        self.assertNotIn("PASS", json.dumps(payload))

    def test_execution_gateway_injection_stays_fail_closed_blocked(self):
        import asyncio, json
        from mcp.types import CallToolRequest
        from mcp8020_execution_gateway_v54 import ExecutionGateway, BlockedExecutionClient
        from mcp8020_server_v54 import create_work28_v54_server
        gateway = ExecutionGateway(BlockedExecutionClient())
        service = create_v54_service(room=RoomProvider(), sandbox=SandboxProvider(self._tmp.name),
                                     execution=gateway)
        server = create_work28_v54_server(service)
        handler = server.request_handlers[CallToolRequest]
        request = CallToolRequest(method="tools/call",
                                  params={"name": "sandbox_run_python",
                                          "arguments": {"work_id": "w1", "script": "main.py"}})
        result = asyncio.run(handler(request))
        payload = json.loads(result.root.content[0].text)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "BLOCKED")
        # The gateway answer must never be presented as a success/PASS.
        self.assertNotIn("PASS", json.dumps(payload))
        # Catalog status must never be promoted by wiring alone.
        from mcp8020_catalog_v54 import NOT_IMPLEMENTED, tool_status
        self.assertEqual(tool_status("sandbox_run_python"), NOT_IMPLEMENTED)

if __name__ == "__main__":
    unittest.main()
