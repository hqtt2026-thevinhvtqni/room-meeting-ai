# Xu source audit — Work 28 MCP tooling
- **Audit time:** 2026-10-16 20:08 ICT (UTC+07:00)
- **Auditor:** Xu — Planner / Chief Strategy Architect (CSA), Work 28 orchestration and acceptance
- **Decision authority:** Vinh — Work Owner / Decision Authority
- **Build owner:** Co — Builder, Work 28
- **Independent reviewer:** Ka — Chief Strategy Architect (CSA)
- **Repository/branch:** `hqtt2026-thevinhvtqni/room-meeting-ai` / `work/28-mcp-tooling-platform`

## READ → TRACE → ANALYZE

### Source files read from the Work 28 branch
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/runtime_tools_v1.py`
  - Source SHA: `5bba7ffc83ad9f28a9a2e64566f713b56c09b0df`
  - Adapter-only contract; calls injected Core route; does not itself spawn processes. Request allowlist includes RUN_TESTS/RUN_SCRIPT; caller identity/command/workspace fields are not forwarded by `execution_submit`.
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/sandbox_tools_v1.py`
  - Source SHA: `6682a4812b199dc1d1384d5eee28866c9b7ba459`
  - Uses an injected provider; validates Work-relative paths and has bounded read/search constants.
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/github_tools_v1.py`
  - Source SHA: `c0a29e4a9f27144ed31e59bf4c535bad88506861`
  - Uses an injected authenticated provider; guarded repository-relative paths and branch policy.
- `work/28/MCP-8020-TOOLING-PLATFORM/04_CODE/mcp_tool_registration_v1.py`
  - Source SHA: `6fa703050c23402cc9961be0a04234f20bf4ef01`
  - Declares 13 named tools and registers them on an injected MCP instance. Its own docstring says it must be called by the existing FastMCP startup after trusted providers are injected; the helper alone does not prove startup integration or live registration.
- `work/28/MCP-8020-TOOLING-PLATFORM/05_TEST/test_mcp_tool_registration_v1.py`
  - Source SHA: `d73b99932cda5b9813a91909d54c65fd9398db34`
  - Includes a fake-MCP test asserting 13 names and rejection of a missing decorator. This is a unit/contract test source, not proof of the live MCP registry.
- `.github/workflows/work28-mcp-tooling.yml`
  - Uses Python 3.12 and `python -m unittest discover -s 05_TEST -v` under the Work 28 tooling directory. A workflow definition is not a test result; inspect the run for the exact commit before declaring PASS.

## Findings / gate status

1. **DONE — source read:** the four adapter/registration modules and the Work 28 workflow above were read through GitHub branch `work/28-mcp-tooling-platform`.
2. **BLOCKED — live integration not proven:** source includes a registration helper, but the files read do not prove it is imported/called by the actual MCP :8020 startup or that the 13 tools appear in the live `tools/list`.
3. **BLOCKED — E2E not proven:** Co's earlier HTTP 200 and Sandbox readback remain reported observations; Xu has not independently reproduced them with raw request/response evidence.
4. **BLOCKED — runner tool availability:** Co reported `runtime_run_tests` and `github_read_file` were absent from the observed live tool list. Source presence of `github_read_file` as a handler is not equivalent to live registration.
5. **BLOCKED — test results:** reading test code or workflow YAML is not execution evidence. No fresh exit code, complete test inventory, logs, or test run bound to the latest source revision was retrieved in this audit.
6. **No unsupported code edit:** Xu did not guess the live MCP entrypoint/provider wiring. Until the real startup entrypoint and trusted provider bindings are traced, connecting these adapters speculatively could create an unapproved path or bypass Core.

## Required implementation path

- **Co — Builder:** identify the exact existing MCP :8020 startup module and trusted Core/Sandbox/GitHub provider bindings from Work 28 evidence/source; show the exact import/call path and then wire the 13 adapters into that existing instance only if authorization and provider contracts are evidenced.
- **Ka — independent reviewer:** verify startup integration, exact live `tools/list`, per-tool behavior, Core authorization and isolation; write findings with source/test/evidence links.
- **Xu — orchestrator/acceptance:** review the resulting commit and evidence, run/read back the authorized GitHub Actions result when available, and record accept/reject per gate.
- Capture exact timestamp, endpoint (secrets redacted), raw `tools/list`, request/response, test command, exit code, stdout/stderr, test count, source revision, log SHA-256, and readback.
- Preserve existing tools and the flow AI → MCP :8020 → Core :8000 → authorized capability/runtime. No duplicate server, Core bypass, unrestricted shell/Python, Work 13 edits, PC edits, service restarts, or live registry changes without explicit approved authority.

## Current decision
**Work 28 = ACTIVE / NOT RELEASED. Live registration and full E2E = BLOCKED / NOT PROVEN. No merge to `main`.** This is a source audit and handoff, not a claim that runtime integration has been completed.
