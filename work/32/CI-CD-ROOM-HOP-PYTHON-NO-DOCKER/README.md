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
- **Auto E2E:** PASS — 38 tests, including live local HTTP and isolated MCP stdio subprocess roundtrip; 1 warning.
- **CD:** BLOCKED / NOT RUN — no attested staging/VPS target, protected deployment environment, deployment credentials, health-check target or tested rollback.
- **Release:** NOT RELEASED.
- **Overall:** ACTIVE — NOT RELEASED pending CD target evidence, branch governance and independent review.

## Exact validated evidence

- Final validated SHA: `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa`.
- Successful GitHub Actions run #61: `41720062142`.
- CI architecture/security hardening run #58: `41719864578` (SUCCESS, SHA-pinned workflow), SHA `4d70e2fce18982cfdd8c3487dee1d15c2ca51fd3`, SUCCESS; 157 unit passed and 38 E2E passed (1 warning).
- The workflow fetches the exact triggering SHA without submodule recursion, uses Python 3.12, read-only `contents: read`, bounded job timeouts, `pip check`, `compileall`, independent unit/E2E jobs and 14-day JUnit artifacts.
- GitHub Actions dependencies are pinned to audited commit SHAs; see `03_ARCHITECTURE/CICD_TARGET_ARCHITECTURE.md`.
- Full artifact digests and MCP contract evidence: `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.

## Scope / guardrails

No Docker requirement. No Core or live-service architecture change. No two-way Sandbox↔GitHub sync. No automatic merge, secrets mutation or production deploy. Vinh authorized Ka to implement and push Work 32 changes only to the dedicated feature branch and activate branch-scoped CI; that authorization does not authorize main merge or production release.

The Work branch is currently diverged from main (61 ahead / 31 behind at the latest comparison); no merge, rebase or cherry-pick has been performed. Independent Vibe review and safe branch reconciliation remain required before integration.
