# WORK 70 — REPOSITORY LAYOUT & SYNC CONTRACT

Date: 2026-10-30
Status: ACTIVE — readback verification required after every sync

## Authoritative locations
- Sandbox: Work ID 70, root ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/.
- GitHub repository: hqtt2026-thevinhvtqni/room-meeting-ai.
- GitHub main: Work 70 lifecycle/root documentation, canonical Work records, evidence index and Dashboard.
- GitHub branch work/70/05-build: only the Work 70 05_BUILD mapping/engineering-coordination subtree. It is not a canonical source repository and does not own original Work records or product source files.
- Product source repositories and canonical artifact stores must be declared explicitly in the Work Manifest or mapping register. Never infer canonical ownership from a folder or branch name.

## Sync mapping
Sandbox Work 70 root → GitHub main:
- README.md, LEGACY_SCAFFOLD_NOTICE.md
- 00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN
- 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE
- DASHBOARD

Sandbox Work 70 / 05_BUILD → GitHub branch work/70/05-build:
- 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE
- 05_TEST, 06_EVIDENCE, 07_RELEASE, 10_AI_DEBUG_HANDOFF

## Ownership and sync rules
1. Work root contains canonical lifecycle records and approved Work documents.
2. 05_BUILD is a mapping/execution layer. It may store mapping indexes, references, temporary working copies and non-canonical execution metadata; it must point to canonical originals by stable ID, canonical path/URI and exact version/commit.
3. Product source code is canonical only in the source repository/path declared for the Work or artifact. The 05_BUILD branch is not automatically the source repository.
4. A mapping is not a copy. Do not create or maintain a second authoritative document/source file under 05_BUILD.
5. If a tool requires a local working copy, label it TEMPORARY, record its origin and version, and discard or reconcile it under the approved workflow; never publish it as canonical.
6. Cross-phase verified evidence is registered at top-level 06_EVIDENCE. 05_BUILD/06_EVIDENCE is staging only.
7. Preserve existing 05_BUILD files during transition. Classify them as canonical candidate, mapping, temporary copy or legacy/unclassified before any move, rewrite or deletion.
8. No silent moves, renames, deletes, branch changes or merges.
9. Before updating an existing GitHub file, fetch its current blob SHA.
10. After every write, read back from GitHub and Sandbox and compare exact content.
11. A successful write response is not a verification result.
12. Do not merge work/70/05-build into main or claim release until scoped review and acceptance.
13. Do not use MCP 8020 for Work 70; MCP 8030 is the approved Sandbox route.

## Current sync checkpoint
- Root and Dashboard files were synchronized to GitHub main; exact readback comparisons matched for audited paths.
- 05_BUILD files were synchronized to work/70/05-build; prior readback comparisons matched for audited paths.
- This checkpoint does not assert that 05_BUILD has completed canonical-source classification, Dashboard runtime tests, Core integration, acceptance or release.
