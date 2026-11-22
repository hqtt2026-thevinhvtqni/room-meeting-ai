"""Fail-closed handler binding for the canonical Work 28 registry.

The host must provide approved Core/Sandbox/Proposal/GitHub/Runtime handlers.
This module does not create providers, execution hosts, or authorization claims.
"""
from __future__ import annotations
from collections.abc import Callable, Mapping
from typing import Any
from mcp8020_schema_validation_v1 import validate_provider_handler_signature
from mcp8020_unified_registry_v1 import TOOL_SPECS, export_mcp_tools, validate_registry

Handler = Callable[..., Any]

class ToolBindingError(RuntimeError):
    """Raised when the canonical registry cannot be safely bound."""

def bind_handlers(handlers: Mapping[str, Handler]) -> dict[str, Handler]:
    """Return an exact tool-name map or fail before any registration occurs."""
    validate_registry()
    expected_keys = {spec.handler for spec in TOOL_SPECS}
    provided = set(handlers)
    missing = sorted(expected_keys - provided); extra = sorted(provided - expected_keys)
    if missing or extra:
        details = []
        if missing: details.append("missing handlers: " + ", ".join(missing))
        if extra: details.append("unexpected handlers: " + ", ".join(extra))
        raise ToolBindingError("; ".join(details))
    for spec in TOOL_SPECS:
        try: validate_provider_handler_signature(spec, handlers[spec.handler])
        except ValueError as exc: raise ToolBindingError(str(exc)) from exc
    return {spec.name: handlers[spec.handler] for spec in TOOL_SPECS}

def register_tools(register_fn: Callable[..., Any], handlers: Mapping[str, Handler]) -> int:
    """Register canonical metadata and bound handlers through a host adapter."""
    if not callable(register_fn): raise ToolBindingError("registration adapter must be callable")
    bound = bind_handlers(handlers)
    for tool in export_mcp_tools():
        register_fn(name=tool["name"], description=tool["description"], input_schema=tool["inputSchema"], handler=bound[tool["name"]])
    return len(bound)
