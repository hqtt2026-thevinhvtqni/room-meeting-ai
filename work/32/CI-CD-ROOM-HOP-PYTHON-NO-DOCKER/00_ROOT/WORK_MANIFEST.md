# Work 32 — Manifest

- Name: CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Owner/final authority: Vinh
- Coordinator: Xu (AI-01)
- Date: 2026-10-24, Asia/Ho_Chi_Minh
- Status: CI WORKFLOW ACTIVE AND EXACT-SHA VALIDATED; BOUNDED UNIT + AUTO E2E PASS; CD / RELEASE NOT AUTHORIZED
- Sandbox ID: 32
- GitHub branch: work/32-ci-cd-room-hop-python-no-docker

## Goal
Survey and design evidence-first CI/CD for existing Python ROOM-HOP without Docker. Supplemental scope: remove the Tester dependency on Vinh's PC by providing repeatable Python/pytest execution through the existing authorized Work 12/13 Execution Host contract, plus fail-closed test-result classification.

## Guardrails
No Docker requirement; no live-service or MAIN SOURCE changes; no auto-merge or production deploy. Vinh explicitly authorized Ka on 2026-11-04 to implement and push Work 32 changes only to the dedicated feature branch and activate branch-scoped CI/Auto E2E. This authorization does not permit main merge, production deployment, secrets changes, or bypass of independent review. CD remains a separate gated phase. Core :8000 remains the single source of truth and must never be installed inside Sandbox. Sandbox is the AI build zone; MAIN SOURCE remains read-only for AI build operations. The full ROOM-HOP source tree is not copied into this Work.

## Integration boundaries
- Work 12 owns the Work Execution Environment contract.
- Work 13 owns the canonical Execution Host service/bridge (POST /execute).
- Work 27 owns the sandbox runtime adapter/contract and must not be duplicated.
- Work 32 owns the Python CI candidate, environment/test evidence classification and acceptance plan.
- Work 51 consumes this capability for the Coder–Tester loop.
- Current evidence: live execution capability is not attested through the current ROOM-HOP route; no pytest result is claimed.


## Current evidence snapshot — 2026-11-04

- Canonical implementation branch: `work/32-ci-cd-python-ci-v2`.
- Validated commit: `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`.
- GitHub Actions run #50 / `41719444619`: SUCCESS.
- Python 3.12 bounded unit gate: 157 passed.
- Auto E2E gate: 38 passed, 1 warning; includes live HTTP roundtrip and isolated MCP stdio subprocess roundtrip.
- Artifact evidence and SHA-256 digests: `06_EVIDENCE/W32-EVIDENCE-004-MCP-CONTRACT-STDIO-E2E-20261104.md`.
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`; branch comparison: 52 ahead / 31 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No merge/rebase/cherry-pick; main unchanged.
- CD / deployment remains BLOCKED until a real staging target, ownership, approved credentials/environment, health check, and tested rollback are evidenced.
- Release status: ACTIVE — NOT RELEASED.
