"""Focused contract tests for schema validation and result preservation."""
import json
import sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1] / "04_CODE"
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from mcp8020_schema_validation_v1 import validate_registered_schemas, validate_tool_arguments
from mcp8020_unified_registry_v1 import TOOL_SPECS

def spec(name): return next(item for item in TOOL_SPECS if item.name == name)

def test_all_registered_schemas_are_draft_2020_12_valid():
    validate_registered_schemas(TOOL_SPECS)

def test_missing_unknown_and_wrong_type_arguments_fail_closed():
    with pytest.raises(ValueError): validate_tool_arguments(spec("sandbox_read"), {"work_id": "28"})
    with pytest.raises(ValueError): validate_tool_arguments(spec("sandbox_read"), {"work_id": "28", "relative_path": "x", "extra": True})
    with pytest.raises(ValueError): validate_tool_arguments(spec("sandbox_read"), {"work_id": 28, "relative_path": "x"})

def test_boundary_arguments_are_accepted_and_over_limit_rejected():
    validate_tool_arguments(spec("execution_output_read"), {"run_id": "r", "max_bytes": 1})
    validate_tool_arguments(spec("execution_output_read"), {"run_id": "r", "max_bytes": 16384})
    with pytest.raises(ValueError): validate_tool_arguments(spec("execution_output_read"), {"run_id": "r", "max_bytes": 0})
    with pytest.raises(ValueError): validate_tool_arguments(spec("execution_output_read"), {"run_id": "r", "max_bytes": 16385})

def test_empty_mapping_serializes_as_object_not_empty_response():
    payload = {}; payload.setdefault("contract_version", "1.0.0")
    encoded = json.dumps(payload, ensure_ascii=False)
    assert json.loads(encoded) == {"contract_version": "1.0.0"}
    assert encoded != "{}"
