"""Work 28 MCP stdio subprocess contract test.

This proves the low-level Work 28 Server factory speaks the real MCP stdio
protocol and publishes the locked tool/schema inventory. Providers are
deliberately inert test doubles: this is G3 transport/contract evidence only,
NOT product execution, Core authorization, Sandbox, Runtime, or deployed E2E.
"""
from __future__ import annotations

import asyncio
import os
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CODE_DIR = REPO_ROOT / "work" / "28" / "MCP-8020-TOOLING-PLATFORM" / "04_CODE"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

try:
    from mcp import ClientSession
    from mcp.client.stdio import StdioServerParameters, stdio_client
    HAS_MCP_STDIO = True
except ImportError:
    HAS_MCP_STDIO = False

from mcp8020_unified_registry_v1 import TOOL_SPECS


_SERVER_SCRIPT = r"""
import asyncio
import sys
sys.path.insert(0, sys.argv[1])
from mcp.server.stdio import stdio_server
from mcp8020_unified_server_v1 import create_work28_server

class InertProvider:
    def __getattr__(self, name):
        def handler(**kwargs):
            return {"handler": name, "accepted": True}
        return handler

async def main():
    provider = InertProvider()
    server = create_work28_server(
        core=provider,
        sandbox=provider,
        sandbox_extensions=provider,
        proposals=provider,
        github=provider,
        runtime=provider,
    )
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )

asyncio.run(main())
"""


@unittest.skipUnless(
    HAS_MCP_STDIO,
    "MCP Python SDK v1 stdio client is unavailable; G3 remains BLOCKED",
)
class Work28McpStdioContractTests(unittest.TestCase):
    def test_real_stdio_subprocess_exposes_exact_tool_and_schema_inventory(self):
        expected_names = [spec.name for spec in TOOL_SPECS]
        expected_schemas = {
            spec.name: spec.input_schema
            for spec in TOOL_SPECS
        }

        async def exercise():
            env = dict(os.environ)
            env["PYTHONPATH"] = str(CODE_DIR)
            params = StdioServerParameters(
                command=sys.executable,
                args=["-c", _SERVER_SCRIPT, str(CODE_DIR)],
                env=env,
                cwd=str(REPO_ROOT),
            )
            async with stdio_client(params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await asyncio.wait_for(session.initialize(), timeout=15)
                    result = await asyncio.wait_for(session.list_tools(), timeout=15)
                    observed_names = [tool.name for tool in result.tools]
                    observed_schemas = {
                        tool.name: tool.inputSchema
                        for tool in result.tools
                    }
                    self.assertEqual(observed_names, expected_names)
                    self.assertEqual(observed_schemas, expected_schemas)

        asyncio.run(exercise())


if __name__ == "__main__":
    unittest.main()
