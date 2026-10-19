"""Work 28 MCP registration surface for the v1 runtime, sandbox and GitHub adapters.

Call register_work28_tools() from the existing FastMCP server startup after injecting
trusted providers. This module creates no server, runtime, filesystem or credentials.
"""
from __future__ import annotations
from typing import Any
from runtime_tools_v1 import RuntimeToolsV1
from sandbox_tools_v1 import SandboxToolsV1
from github_tools_v1 import GitHubToolsV1
from discovery_tools_v1 import DiscoveryToolsV1


def register_work28_tools(mcp: Any, runtime: RuntimeToolsV1,
                          sandbox: SandboxToolsV1, github: GitHubToolsV1,
                          discovery: DiscoveryToolsV1 | None = None) -> list[str]:
    """Register stable, explicitly named tools on an existing MCP server instance."""
    required = (
        ("execution_submit", runtime.execution_submit),
        ("execution_status", runtime.execution_status),
        ("execution_output_read", runtime.execution_output_read),
        ("sandbox_search", sandbox.sandbox_search),
        ("sandbox_stat", sandbox.sandbox_stat),
        ("sandbox_read_range", sandbox.sandbox_read_range),
        ("sandbox_write", sandbox.sandbox_write),
        ("github_repository", github.github_repository),
        ("github_read_file", github.github_read_file),
        ("github_search_files", github.github_search_files),
        ("github_create_branch", github.github_create_branch),
        ("github_create_file", github.github_create_file),
        ("github_update_file", github.github_update_file),
    )
    
    # Add discovery tools if provider is available
    if discovery is not None:
        required = required + (
            ("capability_discover", discovery.capability_discover),
            ("capability_check", discovery.capability_check),
        )
    decorator = getattr(mcp, "tool", None)
    if not callable(decorator):
        raise TypeError("existing MCP instance must expose a callable tool decorator")
    registered: list[str] = []
    for name, handler in required:
        try:
            decorated = decorator(name=name)(handler)
        except TypeError:
            # Do not silently fall back to unnamed tools: name stability is part of the contract.
            raise TypeError(f"MCP tool decorator does not support explicit name for {name}")
        if decorated is None:
            raise RuntimeError(f"MCP registration returned no handler for {name}")
        registered.append(name)
    return registered
