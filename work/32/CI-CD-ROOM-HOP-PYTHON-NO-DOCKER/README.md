# Work 32 — CI/CD for ROOM-HOP (Python, no Docker)

- Document Number: W32-README-001
- Priority order: P1 — Work overview and current acceptance state
- Owner / final authority: Vinh
- Coordinator: Xu (AI-01)
- Execution owner: Ka — CSA / Architecture & Backend Owner (delegated)
- Sandbox Work ID: 32
- GitHub repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Canonical implementation branch: `work/32-ci-cd-python-ci-v2`
- Work documents: `work/32/CI-CD-ROOM-HOP-PYTHON-NO-DOCKER/`

## Current status — 2026-11-04

- **CI:** PASS — GitHub Actions push / pull-request / manual-dispatch workflow operational.
- **Unit gate:** PASS — 157 deterministic Python 3.12 tests.
- **Core product Auto E2E:** PASS — 39 tests, including full live HTTP → MCP stdio → persistent transcript → close → final artifact → readback journey; 1 warning. **Dashboard→Core browser E2E:** BLOCKED / NOT RUN because the separately maintained Dashboard still uses a mock bridge.
- **CD:** BLOCKED / NOT RUN — no attested staging/VPS target, protected deployment environment, deployment credentials, health-check target or tested rollback.
- **Release:** NOT RELEASED.
- **Overall:** ACTIVE — NOT RELEASED pending CD target evidence, branch governance and independent review.

## Exact validated evidence

- Final validated SHA: `ecb263a2d53786e71bdca8eed336b303506c06b4`.
- Successful GitHub Actions run #65: `41722744353`.
- CI architecture/security hardening run #58: `41719864578` (SUCCESS, SHA-pinned workflow), SHA `4d70e2fce18982cfdd8c3487dee1d15c2ca51fd3`, SUCCESS; 157 unit passed and 38 E2E passed (1 warning).
- The workflow fetches the exact triggering SHA without submodule recursion, uses Python 3.12, read-only `contents: read`, bounded job timeouts, `pip check`, `compileall`, independent unit/E2E jobs and 14-day JUnit artifacts.
- GitHub Actions dependencies are pinned to audited commit SHAs; see `03_ARCHITECTURE/CICD_TARGET_ARCHITECTURE.md`.
- Full artifact digests and MCP contract evidence: `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.

## Scope / guardrails

No Docker requirement. No Core or live-service architecture change. No two-way Sandbox↔GitHub sync. No automatic merge, secrets mutation or production deploy. Vinh authorized Ka to implement and push Work 32 changes only to the dedicated feature branch and activate branch-scoped CI; that authorization does not authorize main merge or production release.

The Work branch is currently diverged from main (65 ahead / 32 behind at the latest comparison); no merge, rebase or cherry-pick has been performed. Independent Vibe review and safe branch reconciliation remain required before integration.


## Product-level evidence and boundary

- Full Core product journey evidence: `06_EVIDENCE/W32-EVIDENCE-005-PRODUCT-AUTO-E2E-20261104.md`.
- Unit: 157 passed. Product Auto E2E: 39 passed, 1 warning.
- Dashboard source audit: `hqtt2026-thevinhvtqni/hqtt-Dashboard-note`, branch `hqtt-ai-project-structure-082c9`, HEAD `32e41f43d2fdd6b8314185bbaa57bc8b04b41641`; `App.tsx` still selects `createMockBridge()`. UI-to-Core product integration is not claimed.
- Overall Work 32 remains ACTIVE — NOT RELEASED until Dashboard integration scope is resolved, independent review is complete, branch governance is reconciled, and CD gates are evidenced.
