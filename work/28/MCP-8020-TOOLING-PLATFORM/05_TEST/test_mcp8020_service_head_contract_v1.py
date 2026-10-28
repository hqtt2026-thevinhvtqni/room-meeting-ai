"""OFF-02: HEAD-contract v54 tests re-authored from superseded PR #18.

PR #18 (branch re-evaluating-work-28-47eaa) was superseded by the a6b14c9
integration slice. These tests restate its two durable intents against the
current HEAD contract:

- the v54 service lists the full 54-tool catalog;
- execution/evidence tools return the honest NOT_IMPLEMENTED envelope
  (status + catalog_version), including when an execution gateway is
  bound (no status promotion without implementation + evidence).

Unlike the tests inherited from PR #18, these are protocol-agnostic and
run in the CI contract runner without the mcp package.
"""
from __future__ import annotations
import sys
import tempfile
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_catalog_v54 import CATALOG_VERSION, NOT_IMPLEMENTED
from mcp8020_room_tools_v54 import RoomProvider
from mcp8020_sandbox_tools_v54 import SandboxProvider
from mcp8020_service_v54 import V54BindingError, create_v54_service


class _CompleteExecutionGateway:
    """Complete 7-handler execution gateway; accepted by fail-closed binding."""

    def sandbox_run_python(self, **kwargs):
        return {"ok": True}

    def sandbox_run_command(self, **kwargs):
        return {"ok": True}

    def sandbox_get_execution_status(self, **kwargs):
        return {"ok": True}

    def sandbox_get_execution_result(self, **kwargs):
        return {"ok": True}

    def sandbox_collect_artifact(self, **kwargs):
        return {"ok": True}

    def sandbox_generate_evidence(self, **kwargs):
        return {"ok": True}

    def sandbox_create_handoff(self, **kwargs):
        return {"ok": True}


class V54HeadCatalogTests(unittest.TestCase):
    """OFF-02: HEAD v54 contract coverage that runs in CI (no mcp dependency)."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.service = create_v54_service(room=RoomProvider(), sandbox=SandboxProvider(self._tmp.name))

    def test_list_tools_returns_54_catalog_entries(self):
        listed = self.service.list_tools()
        self.assertEqual(len(listed), 54)
        self.assertEqual(listed[0]["name"], "room_get_context")
        self.assertTrue(all("inputSchema" in tool for tool in listed))
        self.assertTrue(all("description" in tool for tool in listed))

    def test_honest_not_implemented_envelope_for_execution_tool(self):
        result = self.service.call_tool("sandbox_run_python", {"work_id": "work28", "script": "x.py"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["tool"], "sandbox_run_python")
        self.assertEqual(result["error"]["code"], "NOT_IMPLEMENTED")
        self.assertEqual(result["error"]["status"], NOT_IMPLEMENTED)
        self.assertEqual(result["error"]["catalog_version"], CATALOG_VERSION)

    def test_bound_gateway_does_not_promote_execution_tool_status(self):
        service = create_v54_service(room=RoomProvider(), sandbox=SandboxProvider(self._tmp.name),
                                     execution_gateway=_CompleteExecutionGateway())
        result = service.call_tool("sandbox_run_python", {"work_id": "work28", "script": "x.py"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "NOT_IMPLEMENTED")
        self.assertEqual(result["error"]["status"], NOT_IMPLEMENTED)

    def test_partial_gateway_rejected_fail_closed(self):
        class PartialGateway:
            def sandbox_run_python(self, **kwargs):
                return {}
        with self.assertRaises(V54BindingError):
            create_v54_service(room=RoomProvider(), sandbox=SandboxProvider(self._tmp.name),
                               execution_gateway=PartialGateway())

    def test_unknown_tool_returns_unknown_tool_envelope(self):
        result = self.service.call_tool("no_such_tool", {})
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "UNKNOWN_TOOL")


if __name__ == "__main__":
    unittest.main()
