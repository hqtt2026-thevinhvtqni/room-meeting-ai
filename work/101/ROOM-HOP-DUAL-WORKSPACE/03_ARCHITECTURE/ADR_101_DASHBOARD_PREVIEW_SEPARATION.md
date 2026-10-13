# ADR-101 — Separate Dashboard Preview Folder

- Decision: ACCEPTED / ARCHITECTURE BASELINED
- Authority: Vinh
- Date: 2026-10-13

## Decision
Use `09_DASHBOARD_PREVIEW/` alongside canonical `08_DASHBOARD/`.

## Boundaries
1. `08_DASHBOARD/` remains canonical; Preview is not a second source of truth.
2. Preview is read-only and cannot write directly to Core, Workspace, MCP or GitHub.
3. Missing/stale data must show UNKNOWN, NOT CONNECTED, BLOCKED or NOT VERIFIED, never PASS.
4. File read-back does not prove browser runtime; runtime PASS requires dated evidence in `06_EVIDENCE/`.
5. Sandbox and GitHub use parallel relative paths.
6. Target is identified as repo/branch/root/base; sync remains DRY_RUN and writes disabled.
7. No sync/integration/merge/release without Vinh's explicit approval bound to exact operation, digest, branch and base revision.

Architecture acceptance does not imply tests, browser runtime, live data, two-way sync or E2E PASS.
