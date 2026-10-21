"""Work 28 v54 MCP :8020 adapter.

Wraps the protocol-agnostic V54Service in an MCP Server. The mcp package is
imported lazily so contract tests can run in CI without it. This adapter does
not open a listener; the existing HTTP host owns transport and lifecycle.
"""
from __future__ import annotations
import json
from typing import Any
from mcp8020_catalog_v54 import CATALOG_VERSION
from mcp8020_service_v54 import V54Service

class V54DependencyMissing(RuntimeError):
    pass

def create_work28_v54_server(service: V54Service) -> Any:
    try:
        from mcp.server import Server
        from mcp.types import TextContent, Tool
    except ImportError as exc:
        raise V54DependencyMissing("the mcp package is required for the server adapter: " + str(exc))
    server = Server("room-hop-work28-mcp8020-v54")

    @server.list_tools()
    async def list_tools() -> list[Any]:
        return [Tool(name=t["name"], description=t["description"], inputSchema=t["inputSchema"]) for t in service.list_tools()]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[Any]:
        result = service.call_tool(name, arguments or {})
        payload = dict(result)
        payload.setdefault("contract_version", CATALOG_VERSION)
        return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, default=str))]

    return server
