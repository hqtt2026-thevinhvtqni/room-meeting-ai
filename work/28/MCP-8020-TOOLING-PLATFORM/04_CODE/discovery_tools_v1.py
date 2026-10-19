"""Work 28 capability discovery tools v1.

Provides introspection of the MCP :8020 tool surface and capability registry.
All discovery tools are read-only and do not expose secrets or runtime internals.
"""
from __future__ import annotations
from typing import Any, Mapping, Protocol

class DiscoveryBlocked(RuntimeError):
    """Discovery service is unavailable or incomplete."""


class DiscoveryProvider(Protocol):
    """Interface for the actual MCP registry introspection."""
    def list_tools(self) -> list[Mapping[str, Any]]:
        """Return the list of registered MCP tools with their schemas."""
        ...

    def get_tool_schema(self, tool_name: str) -> Mapping[str, Any]:
        """Return the JSON schema for a specific registered tool."""
        ...

    def get_server_info(self) -> Mapping[str, Any]:
        """Return non-secret server metadata (name, version, capabilities)."""
        ...


class DiscoveryToolsV1:
    """Read-only discovery of MCP :8020 capabilities.
    
    These tools query the live MCP registry, not a static list.
    They do not expose implementation details or secrets.
    """
    
    def __init__(self, provider: DiscoveryProvider | None):
        self._provider = provider
    
    def _ready(self) -> DiscoveryProvider:
        if self._provider is None:
            raise DiscoveryBlocked("MCP registry provider is not configured")
        return self._provider
    
    def capability_discover(self, include_schemas: bool = False) -> dict[str, Any]:
        """Return the list of registered MCP tool names and optionally their schemas.
        
        This is the canonical source for live tool discovery. Do not use
        hardcoded tool lists as the source of truth.
        
        Args:
            include_schemas: If True, include JSON schemas for each tool.
                           Default False to reduce payload size.
        
        Returns:
            dict with:
                - tool_names: list of registered tool names
                - tool_count: integer count
                - schemas: dict mapping tool_name to schema (if include_schemas=True)
                - server_info: non-secret metadata about the MCP server
        
        Raises:
            DiscoveryBlocked: If the MCP registry cannot be queried
        """
        provider = self._ready()
        
        # Get server info first
        server_info = provider.get_server_info()
        if not isinstance(server_info, Mapping):
            raise DiscoveryBlocked("MCP registry returned malformed server info")
        
        # Get tool list
        tools = provider.list_tools()
        if not isinstance(tools, list):
            raise DiscoveryBlocked("MCP registry returned malformed tool list")
        
        result: dict[str, Any] = {
            "tool_names": [t.get("name", "") for t in tools if isinstance(t, Mapping)],
            "tool_count": len(tools),
            "server_info": dict(server_info),
        }
        
        if include_schemas:
            schemas = {}
            for tool in tools:
                if isinstance(tool, Mapping):
                    name = tool.get("name")
                    if name and isinstance(name, str):
                        try:
                            schema = provider.get_tool_schema(name)
                            if isinstance(schema, Mapping):
                                schemas[name] = dict(schema)
                        except Exception:
                            # Individual tool schema failure should not block discovery
                            schemas[name] = {"error": "schema_unavailable"}
            result["schemas"] = schemas
        
        return result
    
    def capability_check(self, tool_name: str) -> dict[str, Any]:
        """Check if a specific tool is registered and return its metadata.
        
        Args:
            tool_name: The name of the tool to check
        
        Returns:
            dict with:
                - name: the tool name
                - registered: boolean indicating if the tool is registered
                - schema: the tool schema if registered (optional)
        
        Raises:
            DiscoveryBlocked: If the MCP registry cannot be queried
        """
        provider = self._ready()
        
        tools = provider.list_tools()
        if not isinstance(tools, list):
            raise DiscoveryBlocked("MCP registry returned malformed tool list")
        
        tool_names = {t.get("name") for t in tools if isinstance(t, Mapping)}
        registered = tool_name in tool_names
        
        result: dict[str, Any] = {
            "name": tool_name,
            "registered": registered,
        }
        
        if registered:
            try:
                schema = provider.get_tool_schema(tool_name)
                if isinstance(schema, Mapping):
                    result["schema"] = dict(schema)
            except Exception:
                result["schema"] = {"error": "schema_unavailable"}
        
        return result
