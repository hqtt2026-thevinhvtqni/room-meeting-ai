# Work 28 — MCP Tooling Platform

Work 28 is maintained in parallel in the ROOM-HOP Sandbox and this repository branch, following the Work 98 ONT Care layout convention.

- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/28-mcp-tooling-platform`
- Work path: `work/28/MCP-8020-TOOLING-PLATFORM/`
- Evidence path: `work/28/06_EVIDENCE/`
- Authorization authority: Core :8000
- MCP adapter: :8020
- Execution must use an approved isolated runtime; no unrestricted shell, duplicate execution host, or Core bypass.

## Current state (2026-10-15)

- Work status: ACTIVE / NOT LOCKED.
- The PC startup script reported MCP Meeting :8020 started, but the assistant connector returned `UNAVAILABLE: Connection failed` on a recent attempt; end-to-end connectivity remains BLOCKED pending re-verification.
- MCP Build :8030 did not listen during that startup attempt; tracked separately.
- Python/runtime execution, full MCP → Core → approved runtime → evidence E2E, source transfer/import gates, and release remain BLOCKED/NO-GO wherever stated in the evidence.
- GitHub source synchronization does not mean tests passed or runtime is deployed.

## Layout and workflow

The `MCP-8020-TOOLING-PLATFORM` directory preserves the Work structure, including architecture, code, tests, evidence, and the append-only journal. Sandbox-root checkpoints are copied to `work/28/06_EVIDENCE/`.

Edit in VS Code on this branch, push changes to this branch, and use GitHub Actions results as test evidence. Do not merge to `main` or lock Work 28 until acceptance gates pass.
