"""Contract checks for the Work 28 v54 54-tool catalog. Not evidence of live registration."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_catalog_v54 import (BROWSER_TOOLS, COMPUTER_TOOLS, EXPECTED_GROUP_COUNTS, EXPECTED_TOTAL, GROUP_BROWSER,
                                 GROUP_COMPUTER, GROUP_ROOM, GROUP_SANDBOX, IMPLEMENTED, NOT_IMPLEMENTED, ROOM_TOOLS,
                                 SANDBOX_TOOLS, TOOL_SPECS, export_mcp_tools, implemented_tool_names,
                                 not_implemented_tool_names, validate_catalog)

class CatalogV54Tests(unittest.TestCase):
    def test_exactly_54_unique_names_in_catalog_order(self):
        validate_catalog()
        names = tuple(spec.name for spec in TOOL_SPECS)
        self.assertEqual(len(names), EXPECTED_TOTAL)
        self.assertEqual(len(set(names)), EXPECTED_TOTAL)

    def test_group_counts_and_membership_match_catalog_doc(self):
        self.assertEqual(len(ROOM_TOOLS), 10)
        self.assertEqual(len(SANDBOX_TOOLS), 21)
        self.assertEqual(len(COMPUTER_TOOLS), 6)
        self.assertEqual(len(BROWSER_TOOLS), 17)
        counts = {}
        for spec in TOOL_SPECS:
            counts[spec.group] = counts.get(spec.group, 0) + 1
        self.assertEqual(counts, EXPECTED_GROUP_COUNTS)
        self.assertEqual(ROOM_TOOLS[0], "room_get_context")
        self.assertEqual(ROOM_TOOLS[-1], "room_submit_proposal")
        self.assertEqual(SANDBOX_TOOLS[0], "sandbox_list_works")
        self.assertEqual(SANDBOX_TOOLS[-1], "sandbox_create_handoff")
        self.assertEqual(BROWSER_TOOLS[-1], "browser_wait_for_change")

    def test_every_schema_is_a_closed_object(self):
        for spec in TOOL_SPECS:
            self.assertEqual(spec.input_schema["type"], "object", spec.name)
            self.assertIs(spec.input_schema["additionalProperties"], False, spec.name)
            for key in spec.input_schema["required"]:
                self.assertIn(key, spec.input_schema["properties"], spec.name + ":" + key)

    def test_status_split_is_explicit_and_honest(self):
        implemented = implemented_tool_names()
        blocked = not_implemented_tool_names()
        self.assertEqual(len(implemented) + len(blocked), 54)
        self.assertEqual(len(implemented), 24)
        implemented_by_group = {}
        for spec in TOOL_SPECS:
            if spec.status == IMPLEMENTED:
                implemented_by_group[spec.group] = implemented_by_group.get(spec.group, 0) + 1
        self.assertEqual(implemented_by_group, {GROUP_ROOM: 10, GROUP_SANDBOX: 14})
        for name in ("sandbox_run_python", "sandbox_run_command", "sandbox_generate_evidence", "computer_screenshot", "browser_open"):
            self.assertIn(name, blocked)
            self.assertNotIn(name, implemented)

    def test_export_uses_mcp_schema_field_names(self):
        tools = export_mcp_tools()
        self.assertEqual(len(tools), 54)
        self.assertTrue(all(set(t) == {"name", "description", "inputSchema"} for t in tools))

    def test_not_implemented_descriptions_state_the_reason(self):
        for spec in TOOL_SPECS:
            if spec.status == NOT_IMPLEMENTED:
                self.assertIn("not available in this build", spec.description, spec.name)

if __name__ == "__main__":
    unittest.main()
