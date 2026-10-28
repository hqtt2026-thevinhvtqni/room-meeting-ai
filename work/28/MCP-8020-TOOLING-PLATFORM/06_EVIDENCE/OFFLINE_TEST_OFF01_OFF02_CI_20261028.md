# Work 28 — OFF-01/OFF-02/OFF-04 offline test deployment & CI evidence

Date: 2026-10-28 (UTC)
Canonical branch: `work/28-mcp-tooling-platform`
Work status: `ACTIVE / INTEGRATION BLOCKED / NOT RELEASED`
Execution gate: `CLOSED`

## Scope and changes

- OFF-01 factory tests: `05_TEST/test_mcp8020_unified_server_v1.py`
- OFF-02 HEAD v54 service/catalog contract tests: `05_TEST/test_mcp8020_service_head_contract_v1.py`
- OFF-04 v1 boundary negative tests: `05_TEST/test_mcp8020_execution_contract_v1.py`
- CI now installs the official MCP SDK 1.x before running Work 28 tests, so OFF-01 is exercised instead of silently skipped: `.github/workflows/work28-mcp-tooling.yml`

Relevant commits:
- `ce1fb954c981a14da12f16e4f0f29d57941fde0` — initial OFF-01/OFF-02 tests
- `6e87fe46d0558542a965197d342850dfa2169371` — initial evidence
- `6c9488a0a22c218d1115d28ce85168497e4a7ab4` — OFF-04 negative tests
- `921b446cc8188324490e094b2878bc210a60b9a1` — install MCP SDK in CI to execute OFF-01

## CI evidence

### Run #185 — baseline before adding MCP SDK

- Run ID: `40722707346`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40722707346
- Commit: `6e87fe46d0558542a965197d342850dfa2169371`
- Result: `success`
- Raw job log: `Ran 319 tests in 8.700s`; `OK (skipped=7)`
- OFF-02: all 5 contract tests executed and passed.
- OFF-01: 3 factory tests skipped because `mcp` was absent. Skip was not treated as PASS.

### Run #187 — factory tests and OFF-04 tests enabled

- Run ID: `40724748310`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40724748310
- Commit: `921b446cc8188324490e094b2878bc210a60b9a1`
- Result: `success`
- Raw job log: `Ran 321 tests in 8.708s`; `OK` (no skipped count in the unittest summary).
- OFF-01: all 3 tests executed and passed:
  - factory constructs a named unified MCP server with complete providers;
  - factory fails closed when a required handler is missing;
  - factory fails closed when a provider is `None`.
- OFF-02: all 5 v54 HEAD-contract tests remain in the suite and passed.
- OFF-04: both new negative tests passed:
  - missing `expected_source_sha256` is rejected by the v1 validator;
  - the legacy v54-style request carrying caller-supplied `script/args` is rejected at the v1 boundary.
- Known non-fatal cleanup warning remains: `fatal: No url found for submodule path 'room-meeting-ai' in .gitmodules`. The workflow conclusion is still success. Node.js action deprecation warning also remains.

## OFF-04 interpretation

These tests establish rejection at the contract boundary only. They do not implement a v54→v1→W13 transformation, do not authorize a caller, do not map `entry_path` to a caller-controlled `command`, and do not prove any live execution. A reviewed fixed-policy mapping and the required source/hash/runtime evidence remain mandatory before any wiring.

## OFF-03 Sandbox read-response diagnostic

Same-path probes against Work ID `28` reproduced two distinct behaviors:

1. For an existing file, `sandbox_read` returned an empty object `{}`, while `sandbox_read_probe` returned the file contents. Reproduced for:
   - `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_SYNC_RECHECK_20261028_2037.md`
   - `MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_w13_core_client_v1.py`
2. For `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/OFFLINE_TEST_OFF01_OFF02_CI_20261028.md`, both read functions returned `FileNotFoundError` in Sandbox although the file exists on GitHub. This indicates that particular evidence file is not present at that Sandbox-relative path; it is not evidence that the read-response bug explains every failure.

Conclusion: ordinary `sandbox_read` response handling is unreliable for existing files; use the probe only as a diagnostic cross-check, not as proof of a general fix. No source was overwritten and no Sandbox file was deleted. The underlying tool/server response-shape defect remains unresolved.

## Status and boundaries

- OFF-01 factory tests: `PASS in GitHub CI`; independent Sandbox-side runner corroboration remains pending.
- OFF-02 contract tests: `PASS in GitHub CI`.
- OFF-04 negative boundary tests: `PASS in GitHub CI`; no transformation/wiring implemented.
- OFF-03: `BLOCKED` — read/probe response inconsistency reproduced; server/tool fix not yet made.
- Work 28: `ACTIVE / INTEGRATION BLOCKED / NOT RELEASED`.
- Execution gate: `CLOSED`.
- No claim of runtime integration or end-to-end execution is made.

## Follow-up verification by Xu — 2026-10-28

### OFF-03 recheck using the correct Work-relative paths

A fresh same-path check against existing Sandbox files reproduced the response-shape discrepancy:

- `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/XU_SYNC_RECHECK_20261028_2037.md`: `sandbox_read` returned an empty object; `sandbox_read_probe` returned `status=ok` with the full text (3,260 bytes).
- `MCP-8020-TOOLING-PLATFORM/04_CODE/mcp8020_w13_core_client_v1.py`: `sandbox_read` returned an empty object; `sandbox_read_probe` returned `status=ok` with the full text (6,915 bytes).

The initial failed attempt used the wrong Work-relative prefix and is not counted as evidence of a read defect. The two results above use the correct path beneath Work ID `28`.

### Independent Sandbox-runner availability

The currently exposed MCP 8030 Work 28 tool surface in this session provides list/read/probe/create/write/append/delete operations, but no callable `run_python`, `run_tests`, or equivalent execution tool. Therefore Xu cannot truthfully claim independent Sandbox-side test execution from this interface. GitHub CI remains the only newly verified test-runner evidence for OFF-01/OFF-02/OFF-04 in this pass. The separate Sandbox-runner evidence requirement remains BLOCKED pending an approved runner capability.

### Disposition

- OFF-03: `BLOCKED` — reproduced at the tool response boundary; no evidence that the deployed MCP 8030 handler was changed or restarted. The Work 28 helper module `tool_sandbox_read_harden.py` is a source artifact, not proof of deployment.
- Independent Sandbox runner for OFF-01/OFF-05: `BLOCKED` — execution capability is not exposed through the available MCP 8030 tools in this session.
- No execution gate change; Work 28 remains `ACTIVE / INTEGRATION BLOCKED / NOT RELEASED`.
