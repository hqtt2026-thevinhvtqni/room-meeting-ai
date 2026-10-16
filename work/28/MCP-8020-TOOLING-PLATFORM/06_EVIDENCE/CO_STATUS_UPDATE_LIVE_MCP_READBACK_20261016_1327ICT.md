# Work 28 — Co status update: live MCP and Sandbox readback

- **Reported by:** Co, Builder — Work 28
- **Reported time:** approximately 2026-10-16 13:27 ICT (+07)
- **Scope:** Work 28 only

## Reported observations (not independently re-probed by Xu in this record)

1. MCP :8020 HTTPS returned HTTP 200.
2. `tools/list` returned a tool list.
3. Sandbox write/readback was reported to match the probe content.
4. Co reported that a Sandbox evidence file was created at `MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/WORK28_MCP_LIVE_READBACK_EVIDENCE_20261016.md`.
5. The reported current tool list did not include `runtime_run_tests` or `github_read_file`.
6. No full E2E run evidence was supplied in this status update.

## Verification boundary

- Xu attempted to read the reported evidence file from branch `work/28-mcp-tooling-platform` using the GitHub connector; it returned NOT_FOUND. This does not prove the file is absent from the ROOM-HOP Sandbox; it means it is not available at that repository path/ref through this read.
- The HTTP 200, live `tools/list`, and Sandbox readback details above remain **Co-reported**, not independently re-probed by Xu in this GitHub update.
- MCP connectivity and file readback do not prove tool registration for the missing tools, approved runtime execution, or end-to-end behavior.

## Next work order

1. Co must persist the exact live evidence into the canonical Work 28 evidence location and provide a readback path that can be checked.
2. Record endpoint identity (redact secrets), timestamp, HTTP status, exact `tools/list` names, request/response evidence, and probe content/hash where the approved environment supports it.
3. Continue implementing/integrating the required adapters through the existing trusted architecture; do not create a duplicate MCP/Core/runtime, bypass Core authorization, or enable arbitrary shell/Python.
4. Run approved tests and actual E2E when a sanctioned runner exists; capture command, exit code, stdout/stderr, test count, revision and log/hash, then read back the produced result.
5. If execution remains unavailable, state the exact capability/schema and error that blocks execution; continue independent code/test work without claiming E2E PASS.

## Current gate

- MCP connectivity: **REPORTED HTTP 200 / tools list available; independent probe not attached here**.
- Sandbox write/readback: **REPORTED PASS for the probe only**.
- `runtime_run_tests`: **NOT OBSERVED in reported tools/list**.
- `github_read_file`: **NOT OBSERVED in reported tools/list**.
- Full E2E: **BLOCKED / NOT PROVEN**.
- Work 28: **ACTIVE / NOT RELEASED**; no merge to `main`.
