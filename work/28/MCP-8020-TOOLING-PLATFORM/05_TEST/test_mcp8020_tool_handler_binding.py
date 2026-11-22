"""Contract tests for canonical 31-tool handler binding.

Source-level tests only until an approved runner executes them.
"""
import sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1] / "04_CODE"
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from mcp8020_unified_registry_v1 import TOOL_SPECS
from mcp8020_tool_handler_binding import ToolBindingError, bind_handlers, register_tools

def _handlers():
    return {key: (lambda **kwargs: {}) for key in {spec.handler for spec in TOOL_SPECS}}

def test_binding_requires_all_canonical_handler_keys():
    with pytest.raises(ToolBindingError, match="missing handlers"):
        bind_handlers({})

def test_binding_accepts_exact_canonical_handler_set_and_returns_31_names():
    bound = bind_handlers(_handlers())
    assert len(bound) == 31
    assert set(bound) == {spec.name for spec in TOOL_SPECS}

def test_binding_rejects_extra_handler_key():
    handlers = _handlers(); handlers["unregistered"] = lambda **kwargs: {}
    with pytest.raises(ToolBindingError, match="unexpected handlers"):
        bind_handlers(handlers)

def test_binding_rejects_incompatible_handler_signature():
    handlers = _handlers(); handlers["sandbox_read"] = lambda required_only: {}
    with pytest.raises(ToolBindingError, match="signature"):
        bind_handlers(handlers)

def test_register_tools_preserves_empty_mapping_as_callable_result():
    seen = []
    count = register_tools(lambda **kwargs: seen.append(kwargs), _handlers())
    assert count == 31
    assert len(seen) == 31
    assert {item["name"] for item in seen} == {spec.name for spec in TOOL_SPECS}
    assert all(callable(item["handler"]) for item in seen)
    assert seen[0]["handler"]() == {}
