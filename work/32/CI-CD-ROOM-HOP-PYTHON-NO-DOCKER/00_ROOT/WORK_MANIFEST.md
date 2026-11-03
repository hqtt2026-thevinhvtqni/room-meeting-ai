# Work 32 — Manifest

- Name: CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- Owner/final authority: Vinh
- Coordinator: Xu (AI-01)
- Date: 2026-10-24, Asia/Ho_Chi_Minh
- Status: BASELINE SURVEY RECORDED; SUPPLEMENTAL PYTEST RUNTIME BUILD IN PROGRESS; LIVE EXECUTION BLOCKED
- Sandbox ID: 32
- GitHub branch: work/32-ci-cd-room-hop-python-no-docker

## Goal
Survey and design evidence-first CI/CD for existing Python ROOM-HOP without Docker. Supplemental scope: remove the Tester dependency on Vinh's PC by providing repeatable Python/pytest execution through the existing authorized Work 12/13 Execution Host contract, plus fail-closed test-result classification.

## Guardrails
No Docker requirement; no live-service or MAIN SOURCE changes; no auto-merge, commit, push or deploy by AI; no CI activation before Vinh approves the baseline and plan. Core :8000 remains the single source of truth and must never be installed inside Sandbox. Sandbox is the AI build zone; MAIN SOURCE remains read-only for AI build operations. The full ROOM-HOP source tree is not copied into this Work.

## Integration boundaries
- Work 12 owns the Work Execution Environment contract.
- Work 13 owns the canonical Execution Host service/bridge (POST /execute).
- Work 27 owns the sandbox runtime adapter/contract and must not be duplicated.
- Work 32 owns the Python CI candidate, environment/test evidence classification and acceptance plan.
- Work 51 consumes this capability for the Coder–Tester loop.
- Current evidence: live execution capability is not attested through the current ROOM-HOP route; no pytest result is claimed.
