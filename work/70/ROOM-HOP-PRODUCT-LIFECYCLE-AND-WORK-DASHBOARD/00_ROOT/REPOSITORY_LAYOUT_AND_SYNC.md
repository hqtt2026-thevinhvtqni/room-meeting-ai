# WORK 70 — REPOSITORY LAYOUT & SYNC CONTRACT

Date: 2026-10-30
Status: ACTIVE — readback verification required after every sync

## Authoritative locations
- Sandbox: Work ID `70`, root `ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/`.
- GitHub repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- GitHub `main`: Work 70 lifecycle/root documentation, evidence index and Dashboard.
- GitHub branch `work/70/05-build`: only the `work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/05_BUILD/` subtree.
- The branch is scoped to 05_BUILD; it is not a replacement for the repository main branch or the entire Work 70 root.

## Sync mapping
Sandbox Work 70 root → GitHub main:
- README.md, LEGACY_SCAFFOLD_NOTICE.md
- 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN
- 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE
- DASHBOARD

Sandbox Work 70 / 05_BUILD → GitHub branch work/70/05-build:
- 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE
- 05_TEST, 06_EVIDENCE, 07_RELEASE, 10_AI_DEBUG_HANDOFF

## Change and verification rules
1. Do not move or copy unrelated Work folders.
2. Do not use MCP 8020 for Work 70; Build MCP 8030 is the approved Sandbox route.
3. Before updating an existing GitHub file, fetch its current blob SHA.
4. After every write, read back from GitHub and Sandbox and compare exact content.
5. A successful write response is not a verification result.
6. Do not merge `work/70/05-build` into main or claim a release until the scoped branch has been reviewed and accepted.
7. Keep branch scope and Sandbox mapping explicit in handoff notes.

## Current sync checkpoint
- Root and Dashboard files are synchronized to GitHub main; exact readback comparisons matched for the audited root and Dashboard paths.
- 05_BUILD files are synchronized to `work/70/05-build`; exact readback comparisons matched for the audited build files, and all nine canonical child directories have .gitkeep markers.
- This checkpoint does not assert that the feature branch is merged, the Dashboard is runtime-tested, or Core is integrated.
