"""Tests for the staged versioned execution catalog; not live MCP registration."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1] / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from mcp8020_execution_catalog_v1 import (
    EXECUTION_TOOL_SPECS,
    NOT_IMPLEMENTED,
    get_tool_spec,
    tool_names,
    validate_execution_catalog,
)


class ExecutionCatalogV1Tests(unittest.TestCase):
    def test_catalog_is_seven_unique_versioned_staging_tools(self):
        validate_execution_catalog()
        self.assertEqual(len(tool_names()), 7)
        self.assertEqual(len(set(tool_names())), 7)

    def test_every_staged_tool_remains_not_implemented(self):
        self.assertTrue(all(spec.status == NOT_IMPLEMENTED for spec in EXECUTION_TOOL_SPECS))

    def test_run_schemas_bind_work_path_and_source_hash(self):
        for name in ("sandbox_run_python", "sandbox_run_tests"):
            with self.subTest(tool=name):
                spec = get_tool_spec(name)
                self.assertIsNotNone(spec)
                schema = spec.input_schema
                self.assertTrue(
                    {"work_id", "entry_path", "expected_source_sha256"}.issubset(
                        set(schema["required"])
                    )
                )
                self.assertEqual(schema["properties"]["expected_source_sha256"]["pattern"], "^[0-9a-f]{64}$")
                self.assertFalse(
                    {"script", "command", "args", "principal", "cwd", "shell"}
                    & set(schema["properties"])
                )

    def test_all_schemas_are_closed_objects(self):
        for spec in EXECUTION_TOOL_SPECS:
            with self.subTest(tool=spec.name):
                self.assertEqual(spec.input_schema["type"], "object")
                self.assertIs(spec.input_schema["additionalProperties"], False)
                self.assertTrue(set(spec.input_schema["required"]).issubset(spec.input_schema["properties"]))

    def test_legacy_command_tool_is_explicitly_not_in_v1_catalog(self):
        # v54 remains untouched; this staging catalog deliberately renames the
        # old arbitrary-command shape to a hash-bound test-entrypoint operation.
        self.assertNotIn("sandbox_run_command", tool_names())
        self.assertIn("sandbox_run_tests", tool_names())


if __name__ == "__main__":
    unittest.main()
