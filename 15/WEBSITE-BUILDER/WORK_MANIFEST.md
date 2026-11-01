# WORK MANIFEST — WORK 15 / WEBSITE BUILDER

- Work ID: 15
- Work Name: WEBSITE-BUILDER
- Status: ACTIVE — PHASE 0 / WORKSPACE AND ARCHITECTURE BOOTSTRAP
- Authority: Vinh
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Canonical branch: `work/15-room-hop-website-builder`
- Canonical repository root: `15/WEBSITE-BUILDER/`
- Sandbox Work ID: `15`
- Canonical Sandbox project root: `WEBSITE-BUILDER/`
- Source revision pinned during manifest creation: `76ec3857ab7a61aac97a00a2a381deda5a0cd4d1`
- Source tree: `4f65242d007333f06ebbae69df6175bb3a34cb5a`
- Runtime dependency on ROOM-HOP Core :8000 / MCP :8020: required by target architecture; live integration NOT VERIFIED.
- Merge/release: NOT AUTHORIZED by this manifest.

## Purpose
Build an autonomous website-building workflow: user intent → planner → project generation/editing → ROOM-HOP execution architecture → real runtime → browser E2E → evidence.

## Canonical project areas
- `README.md`, `WORK.md`
- `docs/`: requirements, architecture, UX and E2E contracts.
- `decisions/`: approved project decisions.
- `src/`: implementation.
- `tests/`: unit, integration and E2E tests.
- `scripts/`: controlled local execution and validation.
- `evidence/`: logs, reports, runtime and screenshot evidence.

## Non-negotiable boundaries
- Follow ROOM-HOP execution architecture; do not create an independent execution path.
- No direct AI bypass of Core/MCP/Execution Host.
- No fake runtime, mock-as-live, or fabricated PASS.
- Preserve existing source and evidence; no broad rewrite or deletion based on this manifest.
- Sandbox writes do not prove GitHub synchronization. Every source change requires branch/commit attribution and exact readback.
- Separate structure compliance, implementation, test verification, integration, acceptance and release.

## Current verified state
- Project workspace and documentation structure are present.
- Current phase: PHASE 0 — workspace and architecture bootstrap.
- Backend implementation, Core/MCP integration, real runtime, browser E2E, security and release: NOT VERIFIED.
- No acceptance or release claim is made.

## Required next gates
1. Pin and audit the exact source revision before implementation changes.
2. Reconcile requirements and architecture with the ROOM-HOP execution contract.
3. Establish unit and contract tests.
4. Prove real runtime and browser E2E with reproducible evidence.
5. Obtain independent review and authorized acceptance before release.

**Manifest note:** This file records the repository/branch/root/revision read directly from the authoritative GitHub branch at creation time. The branch may advance; update the pinned revision only after a new explicit source audit.
