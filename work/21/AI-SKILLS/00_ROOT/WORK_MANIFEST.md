# WORK MANIFEST — WORK 21
- Work ID: 21
- Work Name: AI-SKILLS
- Display Name: 21 — AI-SKILLS
- Product: AI Skills / Agent Skills capability system for ROOM-HOP
- Status: ACTIVE / NORMALIZATION IN PROGRESS
- Created: 2026-10-08
- Updated: 2026-11-20
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu / AI-01
- Architecture Reviewer: Ka / AI-02
- Independent QE: Qw / AI-05
- Sandbox: Work 21 via ROOM-HOP MCP 8030
- Canonical repository: hqtt2026-thevinhvtqni/room-meeting-ai (GitHub synchronization for this normalization: NOT VERIFIED)
- Canonical source path (GitHub mapping established 2026-11-20): branch `work/21-ai-skills`; Work root `work/21/AI-SKILLS/` maps Sandbox `AI-SKILLS/`; root-level records map under `work/21/` with identical filenames. Research note `09_AI_TEMPLATES_PHAN_DONG_GIANG_RESEARCH.md` maps to `work/21/09_AI_TEMPLATES_PHAN_DONG_GIANG_RESEARCH.md`. Base commit: `70ae3fb762bd4719facbf9448919aa2ab9516429` (room-meeting-ai/main). GitHub synchronization: PARTIAL — scoped governance/research records; exact readback pending.
- Standard reference: Work 70, Standard v1.2; DOC-085 (Work Dashboard vs Product Dashboard), DOC-056 (document standardization policy).

## Purpose and scope
Research, design and build reusable, portable, verifiable AI Skills / Agent Skills for ROOM-HOP, integrating with Agent runtime, MCP, A2A, Memory and execution capabilities. Skill is not Model and does not replace Tool/MCP.

## Current lifecycle baseline
- Current phase pointer: 03_ARCHITECT (provisional dashboard pointer; phase/gate authorization NOT VERIFIED).
- Work status: ACTIVE.
- Acceptance: NOT ACCEPTED.
- Release: NOT RELEASED.
- Core integration: NOT VERIFIED.
- Dashboard: local read-only scaffold; browser E2E NOT RUN.
- Independent QE: PENDING.

## Canonical Work folders and mapping
- 00_ROOT: existing governance/manifest records at AI-SKILLS/00_ROOT/.
- 01_DISCOVER: discovery/concept source includes root-level 01_CONCEPT.md and related existing records; mapping is provisional.
- 02_DEFINE: requirements baseline to be reconciled; no migration.
- 03_ARCHITECT: existing architecture at AI-SKILLS/03_ARCHITECTURE/.
- 04_PLAN: research backlog at root-level 07_RESEARCH_BACKLOG.md; plan baseline to be reconciled.
- 05_BUILD: mapping/coordination only at AI-SKILLS/05_BUILD/; not canonical source.
- 06_VERIFY: existing test/evidence areas remain at AI-SKILLS/05_TEST/ and AI-SKILLS/06_EVIDENCE/ until formal mapping is accepted.
- 06_EVIDENCE: existing evidence remains at AI-SKILLS/06_EVIDENCE/.
- 07_ACCEPT: acceptance record not yet established.
- 08_RELEASE: existing release area AI-SKILLS/07_RELEASE/; release not verified.
- 08_DASHBOARD: Work Dashboard at AI-SKILLS/08_DASHBOARD/.
- 09_DASHBOARD_PREVIEW: isolated preview area at AI-SKILLS/09_DASHBOARD_PREVIEW/.
- 09_OPERATE: operations records not yet established.
- 10_AI_DEBUG_HANDOFF: existing debug handoff at AI-SKILLS/10_AI_DEBUG_HANDOFF/.

## Two-dashboard rule
1. Work Dashboard tracks lifecycle, phase, gate, WP, owners, blockers, decisions, evidence and data provenance. It is read-only.
2. Product Dashboard belongs to the AI Skills product only if separately defined in requirements/architecture; it must use product-domain contracts and must not be confused with Work execution status.
3. Dashboard snapshot is local_snapshot, not Core live. Unknown is not PASS; no progress percentage without a defined calculation and evidence.

## Preservation and change control
- Preserve existing files and folders. No source files were moved or deleted in this normalization.
- 05_BUILD is a mapping layer; presence there does not make a file canonical.
- Sandbox is isolated and is not proof of GitHub synchronization. GitHub record sync is performed only on the pinned Work branch and verified by exact-path readback; no direct main writes.
- Pin repository, branch and commit before GitHub changes; use an auditable branch/PR.
- Do not claim PASS without executable evidence and independent review.
- Keep 8020 out of all implementation and verification paths.

## Acceptance criteria
- Manifest and canonical source mapping reconciled.
- Work Dashboard scaffold and data contract verified; preview clearly isolated.
- Document register, lifecycle, WP register and evidence register reconciled.
- Existing source/tests/evidence preserved.
- Schema validation and browser E2E executed and recorded.
- Independent Qw review completed.
- GitHub state reconciled separately from Sandbox.
