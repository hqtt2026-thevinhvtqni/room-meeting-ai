# Work 28 — New Toolset v1: Runtime, Sandbox, GitHub

Date: 2026-10-16
Status: IMPLEMENTED IN BRANCH / UNIT TESTS ADDED / LIVE MCP REGISTRATION NOT YET VERIFIED

## Added modules

- 04_CODE/runtime_tools_v1.py: execution_submit, execution_status, execution_output_read. Typed allowlisted operations only; caller-supplied identity, authorization, arbitrary command, workspace path and evidence root are never forwarded. Uses injected authenticated Core transport and never spawns processes.
- 04_CODE/sandbox_tools_v1.py: sandbox_search, sandbox_stat, sandbox_read_range, sandbox_write. Work-relative path validation, bounded search/read, rejects traversal/drive/UNC/ADS forms. Mutations require provider-confirmed readback verification.
- 04_CODE/github_tools_v1.py: github_repository, github_read_file, github_search_files, github_create_branch, github_create_file, github_update_file. Authenticated provider boundary; rejects writes to main/master; updates require expected blob SHA and a returned commit SHA.
- 05_TEST/test_new_tool_adapters_v1.py: unit tests for validation, fail-closed behavior, bounded inputs, readback requirement and allowlisted runtime request fields.

## Integration contract

These modules are adapters/contracts, not evidence of live MCP registration. The hosting MCP server must register their public methods and inject the existing authenticated Core/Sandbox/GitHub providers. No alternate execution host, direct filesystem bypass or self-authorized identity is introduced. Missing providers fail closed.

## Acceptance status

- Source files added on branch work/28-mcp-tooling-platform.
- Tests are added; execute them from the target Work 28 test environment before claiming PASS.
- Live MCP tools/list, Core authorization, sandbox provider wiring, GitHub provider wiring, runtime isolation and end-to-end readback remain unverified.
- Work 28 remains ACTIVE / NOT LOCKED. Do not merge or claim full E2E PASS from adapter unit tests alone.


## Registration surface added

- 04_CODE/mcp_tool_registration_v1.py exposes register_work28_tools() for the existing FastMCP instance.
- It names and registers 13 tools: 3 runtime, 4 sandbox and 6 GitHub.
- 05_TEST/test_mcp_tool_registration_v1.py adds registration contract tests.
- Latest recorded source commit for registration tests: 56254786f3b83565204fad45439e4a6342b5dccd.

## Important boundary

The registration function is ready to be called by the existing server startup, but it has not been wired into the deployed MCP :8020 entrypoint in this commit series. Therefore the 13 new tools are implemented in the Work 28 branch, not yet confirmed in live tools/list. Do not represent them as already available to agents at runtime.
