"""Static contract checks for the Work 28 unified registry. These tests are not evidence of live registration."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_unified_registry_v1 import EXPECTED_TOOL_NAMES, GITHUB_3, LEGACY_18, TOOL_SPECS, export_mcp_tools, validate_registry

class UnifiedRegistryTests(unittest.TestCase):
    def test_exactly_21_unique_names(self):
        validate_registry()
        names = tuple(item.name for item in TOOL_SPECS)
        self.assertEqual(names, EXPECTED_TOOL_NAMES)
        self.assertEqual(len(names), 21)
        self.assertEqual(len(set(names)), 21)

    def test_18_legacy_plus_three_github(self):
        self.assertEqual(len(LEGACY_18), 18)
        self.assertEqual(GITHUB_3, ("github_repository", "github_read_file", "github_search_files"))
        self.assertEqual(tuple(s.name for s in TOOL_SPECS[:18]), LEGACY_18)
        self.assertEqual(tuple(s.name for s in TOOL_SPECS[18:]), GITHUB_3)

    def test_observed_argument_contracts(self):
        by_name = {s.name: s.input_schema for s in TOOL_SPECS}
        self.assertEqual(by_name["join_meeting"]["required"], ["meeting_id", "identity_id"])
        self.assertEqual(by_name["start_meeting"]["required"], ["meeting_id", "starter"])
        self.assertEqual(by_name["add_paste_to_meeting"]["required"], ["meeting_id", "text"])
        self.assertIn("identity_id", by_name["add_paste_to_meeting"]["properties"])
        self.assertEqual(by_name["sandbox_create_work"]["required"], ["work_id", "work_name", "identity_id"])
        self.assertEqual(by_name["sandbox_list"]["required"], ["work_id"])
        self.assertEqual(by_name["get_pending_tasks"]["properties"]["limit"]["default"], 20)
        self.assertEqual(by_name["submit_proposal"]["required"], ["identity_id", "meeting_id", "trigger_message_id", "agent_id", "proposal_id", "content"])

    def test_export_uses_mcp_schema_field_names(self):
        tools = export_mcp_tools()
        self.assertEqual(len(tools), 21)
        self.assertTrue(all(set(t) == {"name", "description", "inputSchema"} for t in tools))
        self.assertTrue(all(t["inputSchema"]["additionalProperties"] is False for t in tools))

if __name__ == "__main__":
    unittest.main()
