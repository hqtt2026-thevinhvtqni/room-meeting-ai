"""Service-level tests: schema validation, fail-closed binding, real handler flows.

Covers test layers 1-4 of the catalog: schema/invalid-input, handler binding,
path-boundary negatives, and deterministic unit flows with real temp sandboxes.
"""
from __future__ import annotations
import os
import sys
import tempfile
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_catalog_v54 import TOOL_SPECS, implemented_tool_names, not_implemented_tool_names
from mcp8020_room_tools_v54 import RoomProvider
from mcp8020_sandbox_tools_v54 import SandboxProvider
from mcp8020_service_v54 import V54BindingError, create_v54_service

class ServiceV54TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.sandbox = SandboxProvider(self._tmp.name)
        self.room = RoomProvider()
        self.service = create_v54_service(room=self.room, sandbox=self.sandbox, computer=None, browser=None)

    def call(self, name, **kwargs):
        return self.service.call_tool(name, kwargs)

class ToolsListCallFlowTests(ServiceV54TestCase):
    def test_tools_list_returns_all_54(self):
        tools = self.service.list_tools()
        self.assertEqual(len(tools), 54)
        self.assertEqual(tools[0]["name"], "room_get_context")
        self.assertEqual(tools[-1]["name"], "browser_wait_for_change")

    def test_every_published_tool_answers_list_then_call(self):
        # Layer 2: each published tool maps to a handler or an explicit NOT_IMPLEMENTED status.
        for tool in self.service.list_tools():
            name = tool["name"]
            result = self.service.call_tool(name, {})
            self.assertIsInstance(result, dict, name)
            self.assertIn("ok", result, name)
            if name in not_implemented_tool_names():
                self.assertFalse(result["ok"], name)
                self.assertEqual(result["error"]["code"], "NOT_IMPLEMENTED", name)
            else:
                # implemented tools either succeed (no required args) or reject empty args
                self.assertIn(result["ok"], (True, False), name)
                if result["ok"] is False:
                    self.assertEqual(result["error"]["code"], "INVALID_INPUT", name)

    def test_unknown_tool_is_rejected(self):
        result = self.call("does_not_exist")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "UNKNOWN_TOOL")

class RoomFlowTests(ServiceV54TestCase):
    def test_meeting_and_proposal_flow(self):
        started = self.call("room_start_meeting", title="Work 28 review", identity_id="agent-x")
        self.assertTrue(started["ok"], started)
        meeting_id = started["data"]["meeting_id"]
        joined = self.call("room_join_meeting", meeting_id=meeting_id, identity_id="agent-y")
        self.assertTrue(joined["ok"], joined)
        appended = self.call("room_append_meeting_message", meeting_id=meeting_id, content="hello room", speaker="agent-y")
        self.assertTrue(appended["ok"], appended)
        transcript = self.call("room_get_transcript", meeting_id=meeting_id)
        self.assertEqual(transcript["data"]["segments"][0]["content"], "hello room")
        meeting = self.call("room_get_meeting", meeting_id=meeting_id)
        self.assertEqual(meeting["data"]["meeting"]["meeting_id"], meeting_id)
        listed = self.call("room_list_meetings")
        self.assertEqual(listed["data"]["total"], 1)
        proposal = self.call("room_submit_proposal", identity_id="agent-x", content="adopt v54 catalog", evidence_refs=["03_ARCHITECTURE/WORK28_TOOL_CONTRACT_CATALOG_V1_54.md"])
        self.assertTrue(proposal["ok"], proposal)
        tasks = self.call("room_get_pending_tasks", owner="agent-x")
        self.assertEqual(tasks["data"]["total"], 1)
        context = self.call("room_get_context")
        self.assertTrue(context["ok"])
        structure = self.call("room_get_structure")
        self.assertTrue(structure["ok"])

    def test_missing_meeting_is_not_found(self):
        result = self.call("room_get_meeting", meeting_id="MTG-9999")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "NOT_FOUND")

class SandboxFlowTests(ServiceV54TestCase):
    def test_file_operation_flow(self):
        created = self.call("sandbox_create_work", work_id="work28", work_name="Work 28", identity_id="agent-x")
        self.assertTrue(created["ok"], created)
        written = self.call("sandbox_write", work_id="work28", path="docs/readme.md", content="# Work 28 v54\n54-tool catalog.\n")
        self.assertTrue(written["ok"], written)
        sha = written["data"]["sha256"]
        self.assertEqual(len(sha), 64)
        read = self.call("sandbox_read", work_id="work28", path="docs/readme.md")
        self.assertTrue(read["ok"], read)
        self.assertIn("54-tool", read["data"]["content"])
        appended = self.call("sandbox_append", work_id="work28", path="docs/readme.md", content="extra line\n")
        self.assertTrue(appended["ok"], appended)
        meta = self.call("sandbox_read_file_metadata", work_id="work28", path="docs/readme.md")
        self.assertTrue(meta["ok"], meta)
        self.assertGreater(meta["data"]["size"], 0)
        found = self.call("sandbox_search", work_id="work28", query="54-tool")
        self.assertTrue(found["ok"], found)
        self.assertEqual(len(found["data"]["matches"]), 1)
        listed = self.call("sandbox_list", work_id="work28", path="docs")
        self.assertEqual(listed["data"]["entries"][0]["name"], "readme.md")
        mkdir = self.call("sandbox_create_directory", work_id="work28", path="docs/sub")
        self.assertTrue(mkdir["ok"], mkdir)
        copied = self.call("sandbox_copy_file", work_id="work28", source_path="docs/readme.md", destination_path="docs/sub/copy.md")
        self.assertTrue(copied["ok"], copied)
        moved = self.call("sandbox_move_file", work_id="work28", source_path="docs/sub/copy.md", destination_path="docs/sub/renamed.md")
        self.assertTrue(moved["ok"], moved)
        manifest = self.call("sandbox_get_manifest", work_id="work28")
        self.assertTrue(manifest["ok"], manifest)
        paths = [f["path"] for f in manifest["data"]["files"]]
        self.assertIn("readme.md".replace("readme", os.path.join("docs", "readme").replace("docs", "docs")), paths)
        validated = self.call("sandbox_validate_path", work_id="work28", path="docs/readme.md", operation="READ")
        self.assertTrue(validated["ok"], validated)
        self.assertTrue(validated["data"]["allowed"])
        deleted = self.call("sandbox_delete", work_id="work28", path="docs/readme.md", confirm_delete=True)
        self.assertTrue(deleted["ok"], deleted)
        works = self.call("sandbox_list_works")
        self.assertEqual(works["data"]["total"], 1)

    def test_delete_requires_explicit_confirmation(self):
        self.call("sandbox_create_work", work_id="work28", work_name="Work 28")
        self.call("sandbox_write", work_id="work28", path="a.txt", content="x")
        refused = self.call("sandbox_delete", work_id="work28", path="a.txt", confirm_delete=False)
        self.assertFalse(refused["ok"])
        self.assertEqual(refused["error"]["code"], "POLICY_REFUSED")

    def test_write_requires_overwrite_policy_for_existing_file(self):
        self.call("sandbox_create_work", work_id="work28", work_name="Work 28")
        first = self.call("sandbox_write", work_id="work28", path="a.txt", content="one")
        self.assertTrue(first["ok"], first)
        second = self.call("sandbox_write", work_id="work28", path="a.txt", content="two")
        self.assertFalse(second["ok"])
        self.assertEqual(second["error"]["code"], "ALREADY_EXISTS")
        third = self.call("sandbox_write", work_id="work28", path="a.txt", content="two", overwrite=True)
        self.assertTrue(third["ok"], third)

class SandboxSecurityTests(ServiceV54TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.call("sandbox_create_work", work_id="work28", work_name="Work 28")

    def test_path_traversal_is_rejected(self):
        result = self.call("sandbox_read", work_id="work28", path="../outside.txt")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "PATH_ESCAPE")

    def test_absolute_path_is_rejected(self):
        result = self.call("sandbox_read", work_id="work28", path="/etc/passwd")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "INVALID_PATH")

    def test_symlink_escape_is_rejected(self):
        outside = Path(self._tmp.name) / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        link = Path(self._tmp.name) / "work28" / "link.txt"
        os.symlink(outside, link)
        result = self.call("sandbox_read", work_id="work28", path="link.txt")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "PATH_ESCAPE")

    def test_cross_work_access_is_rejected(self):
        self.call("sandbox_create_work", work_id="other", work_name="Other")
        self.call("sandbox_write", work_id="other", path="secret.txt", content="data")
        result = self.call("sandbox_read", work_id="work28", path="../other/secret.txt")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "PATH_ESCAPE")

    def test_unknown_work_is_not_found(self):
        result = self.call("sandbox_list", work_id="ghost")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"]["code"], "NOT_FOUND")

class SchemaValidationTests(ServiceV54TestCase):
    def test_missing_required_argument(self):
        result = self.call("sandbox_read", work_id="work28")
        self.assertFalse(result["ok"])
        self.assertIn("missing required argument", result["error"]["message"])

    def test_unknown_argument_is_rejected(self):
        result = self.call("room_get_context", selector="main", extra="nope")
        self.assertFalse(result["ok"])
        self.assertIn("unsupported argument", result["error"]["message"])

    def test_wrong_type_is_rejected(self):
        result = self.call("room_list_meetings", limit="twenty")
        self.assertFalse(result["ok"])
        self.assertIn("invalid type", result["error"]["message"])

    def test_invalid_work_id_pattern_is_rejected(self):
        result = self.call("sandbox_create_work", work_id="../bad", work_name="Bad")
        self.assertFalse(result["ok"])
        self.assertIn("pattern", result["error"]["message"])

    def test_enum_and_bounds_are_enforced(self):
        result = self.call("sandbox_validate_path", work_id="work28", path="a", operation="EXEC")
        self.assertFalse(result["ok"])
        self.assertIn("enum", result["error"]["message"].lower())
        result = self.call("room_list_meetings", limit=0)
        self.assertFalse(result["ok"])

class BindingTests(ServiceV54TestCase):
    def test_binding_is_fail_closed(self):
        with self.assertRaises(V54BindingError):
            create_v54_service(room=None, sandbox=self.sandbox)
        with self.assertRaises(V54BindingError):
            create_v54_service(room=self.room, sandbox=None)

    def test_computer_and_browser_providers_are_optional_until_implemented(self):
        service = create_v54_service(room=self.room, sandbox=self.sandbox, computer=None, browser=None)
        self.assertEqual(len(service.list_tools()), 54)

class NotImplementedGroupTests(ServiceV54TestCase):
    def test_execution_and_agent_tools_report_not_implemented(self):
        for name in ("sandbox_run_python", "sandbox_run_command", "sandbox_get_execution_status", "sandbox_generate_evidence", "sandbox_create_handoff", "computer_screenshot", "browser_open", "browser_drag_drop"):
            result = self.service.call_tool(name, {})
            self.assertFalse(result["ok"], name)
            self.assertEqual(result["error"]["code"], "NOT_IMPLEMENTED", name)
            self.assertEqual(result["error"]["status"], "NOT_IMPLEMENTED", name)

if __name__ == "__main__":
    unittest.main()
