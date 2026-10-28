# Work 28 — OFF-01/OFF-02 offline test deployment & CI evidence
Date: 2026-10-28 (UTC)
Deployed by: Vibe (Work agent, per Xu deployment order for OFF-01/OFF-02)
Branch: work/28-mcp-tooling-platform
Commit: ce1fb954c981a14da12f16e4f0f29d57941fde0d
Commit message: test(work28): OFF-01/OFF-02 - unified server factory fail-closed tests + HEAD v54 contract tests

## Scope

Per Xu decision (backlog 2026-10-28), only offline test additions were
deployed. No runtime code, no W27 bridge wiring, no execution gate change.

## Files added (05_TEST only)

1. test_mcp8020_unified_server_v1.py — OFF-01
   - factory builds server with complete providers (31-tool registry)
   - fail-closed when a provider is None (Work28ProviderBlocked)
   - fail-closed when a required handler is missing (Work28ProviderBlocked)
   - class guarded by @unittest.skipUnless(HAS_MCP): skips in CI where the
     mcp package is not installed; full factory verification requires a
     Sandbox-side runner with mcp installed.

2. test_mcp8020_service_head_contract_v1.py — OFF-02 (protocol-agnostic, runs in CI)
   - list_tools returns 54 catalog entries, first tool room_get_context
   - honest NOT_IMPLEMENTED envelope for execution tools with current HEAD
     shape: error.code, error.status, error.catalog_version (54.0.0-draft1)
   - binding a complete ExecutionGateway does NOT promote tool status
   - partial gateway binding is rejected fail-closed (V54BindingError)
   - unknown tool returns UNKNOWN_TOOL envelope
   These restate the two durable intents of superseded PR #18 against the
   HEAD contract (integration slice a6b14c9).

## CI result (read from GitHub, run #184)

- Workflow: Work 28 MCP Tooling Tests (path-filtered: work/28/**)
- Run #184 on commit ce1fb95: COMPLETED SUCCESSFULLY, duration 19s
- Previous run #183 (commit 599bb59): completed successfully, 17s
- Known CI annotations (unchanged, release checklist REL-01): Node 20
  deprecation for checkout@v4 / setup-python@v5; ubuntu-latest label
  migration notice.

## Limitations (honest boundary)

- The exact unittest counters (tests run / skipped) for run #184 were not
  retrieved in this pass: raw job logs require an authenticated session and
  the public API was rate-limited at the time of reading. CI conclusion
  (success) is read from the GitHub Actions run listing, not inferred.
- OFF-01 tests are expected to SKIP in CI (mcp package not installed in the
  contract runner). Skip is not PASS: full factory verification must be
  produced by the Sandbox-side runner with mcp available, per the two-source
  evidence rule (OFF-05).
- CI green on offline tests is NOT evidence of runtime integration. No E2E
  claim is made.

## Status

- Work 28: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED
- Execution gate: CLOSED
- PR #18: still open; superseded by a6b14c9; closing remains a separate
  authorized action, not performed here.
- Next candidates per Xu backlog: OFF-03 (Sandbox side), OFF-04, RUN-01..04
  remain runtime-gated.
