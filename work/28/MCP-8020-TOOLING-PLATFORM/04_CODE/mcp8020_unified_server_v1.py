"""Fail-closed low-level MCP server factory for Work 28's unified 31-tool registry.
The existing HTTP host owns transport/lifecycle. This factory does not open a listener.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from mcp.server import Server
from mcp.types import TextContent, Tool

from mcp8020_unified_registry_v1 import TOOL_SPECS, validate_registry
from mcp8020_schema_validation_v1 import validate_provider_handler_signature, validate_tool_arguments


class Work28ProviderBlocked(RuntimeError):
    pass


_BOUNDARIES = {
    "core": "core",
    "sandbox": "sandbox",
    "sandbox_extension": "sandbox_extensions",
    "proposal": "proposals",
    "github": "github",
    "runtime": "runtime",
}



def create_work28_server(
    *,
    core: Any,
    sandbox: Any,
    sandbox_extensions: Any,
    proposals: Any,
    github: Any,
    runtime: Any,
) -> Server:
    validate_registry()
    providers = {
        "core": core,
        "sandbox": sandbox,
        "sandbox_extensions": sandbox_extensions,
        "proposals": proposals,
        "github": github,
        "runtime": runtime,
    }
    handlers: dict[str, Any] = {}
    for spec in TOOL_SPECS:
        provider = providers[_BOUNDARIES[spec.boundary]]
        handler = getattr(provider, spec.handler, None) if provider is not None else None
        if not callable(handler):
            raise Work28ProviderBlocked(f"required provider handler unavailable: {spec.name}")
        try:
            validate_provider_handler_signature(spec, handler)
        except ValueError as exc:
            raise Work28ProviderBlocked(
                f"required provider handler signature incompatible: {spec.name}"
            ) from exc
        handlers[spec.name] = handler

    server = Server("room-hop-work28-mcp8020")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(name=spec.name, description=spec.description, inputSchema=spec.input_schema)
            for spec in TOOL_SPECS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        spec = next((item for item in TOOL_SPECS if item.name == name), None)
        if spec is None:
            raise ValueError(f"unknown Work 28 tool: {name}")
        args = {} if arguments is None else arguments
        validated_args = validate_tool_arguments(spec, args)
        result = handlers[name](**validated_args)
        if hasattr(result, "__await__"):
            result = await result
        payload = dict(result) if isinstance(result, Mapping) else {"result": result}
        payload.setdefault("contract_version", "1.0.0")
        return [
            TextContent(
                type="text",
                text=json.dumps(payload, ensure_ascii=False, default=str),
            )
        ]

    return server
