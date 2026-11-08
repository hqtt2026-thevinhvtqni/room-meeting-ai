# DOC-010 — REVISION LEDGER / SỔ THEO DÕI PHIÊN BẢN

Ngày lập: 2026-11-08 (UTC+7)
Work: 1111 — ROOM-HOP Technical Engineering & Debug Lab
Repository: hqtt2026-thevinhvtqni/room-meeting-ai
Canonical branch: main

## 1. Revision anchor

| Layer | Revision / evidence | Disposition |
|---|---|---|
| GitHub main | Latest commit returned by repository commit search: c3ba11597563d2dc62d031d169a457c4d29276b3 | Observed anchor; not PC/runtime attestation |
| Sandbox Work 1111 | work_id=1111; canonical folder ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/ | Read/write collaboration surface |
| PC working copy | No live PC query performed in this session | NOT VERIFIED |
| Runtime :8031 | No live endpoint called | NOT VERIFIED |

## 2. GitHub file blob anchors (main)

| Canonical path | Blob SHA | Readback |
|---|---|---|
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/README.md | 79a454ed1b61ae2f2d7f5b70bafbaf286706c080 | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/00_ROOT/DOC-003_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md | 9aa6c07944cf7472835a6ec77040b89ed5dadc7f | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/01_DISCOVER/DOC-005_DANH-MUC-KHAO-SAT_TECHNICAL-INVENTORY.md | 0de35a68ff0e8bccd5fba5bf87c3036be002d0b0 | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/02_EXTENSION/DOC-006_BASELINE-KY-THUAT_TECHNICAL-BASELINE-AND-OPEN-BLOCKERS.md | 10d0b46a0c146a65b3c39007bba10f2915dedad1 | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/03_ARCHITECT/DOC-007_TRUY-VET-EXECUTION-HOST_EXECUTION-HOST-SOURCE-TRACE.md | eb51d7e87b29311c9de974762644016acbd841af | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/04_PLAN/DOC-008_KE-HOACH-TRIEN-KHAI_IMPLEMENTATION-PLAN.md | cddf9b91e74b8c1aa7a004813f6a89876ad56d0d | PASS |
| work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/05_BUILD/00_ROOT/AI_TASK_BOARD.md | 361acd7a4f37458477b0e8d7d0939c0bebeb4025 | PASS |

Blob SHA identifies file content, not commit SHA. Values are observed fetch_file results from ref=main during this session.

## 3. Parity and drift rules

1. Compare exact canonical path first, then blob/content hash; filename similarity is not proof of equivalence.
2. GitHub commit SHA, file blob SHA, Sandbox readback, PC working-tree state and deployed runtime build hash are distinct evidence types.
3. Do not mark GitHub↔Sandbox↔PC parity PASS unless the same file/revision is compared at each claimed layer.
4. Any path alias, renamed file, missing mirror or different content is recorded as DRIFT / NOT PRESENT / NOT VERIFIED, never silently normalized.
5. Never overwrite PC or Sandbox from GitHub without a scoped change record and preservation check.
6. Every test result must name exact repository, branch, commit SHA, environment and artifact reference.

## 4. Current disposition

- GitHub Work scaffold readback: PASS (14/14 per DOC-003 journal entry).
- Sandbox↔GitHub content parity: PASS only for six previously byte-compared mirrored documents, as recorded in DOC-003; this ledger does not expand that claim.
- GitHub↔PC parity: NOT VERIFIED.
- Sandbox↔PC parity: NOT VERIFIED.
- Current :8031 deployed revision: NOT VERIFIED.
- Agent participation/ACK: NOT VERIFIED unless a task-specific journal claim exists.

## 5. Update protocol

Append a dated addendum; do not rewrite historical observations. Record observer, exact paths, revisions, hashes, method, evidence, result and remaining uncertainty.


## ADDENDUM — 2026-11-09 — C05 REVISION ANCHORS / DOC-003 SANDBOX CONTINUATION

### Revision anchors observed
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- Latest GitHub main commit returned by repository commit search at this check: `024e2c9797da091b83c2e0ea5e3ac7f3b593eafb` (message: test(core): verify Core HTTP mount fails closed). This is a GitHub commit-search anchor, not a PC/runtime attestation.
- PR #48: `https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/48`, draft integration branch `work/w1111-core-execution-authority-v1-2`.
- Branch head immediately before this DOC-010 update: `423f8192ca1cdb8181d3964cc47bc08d0f5ff9b6` (C05 DOC-003 continuation sync). This update itself will advance the branch head; see C05 journal entry for the resulting commit.
- C02 source/test commits on that branch: host source commit `65cf53af2a8a656ef83327ea2718c2c65f994bf7`; test additions commit `3edd072fcec184dca936c510f98ebbe42064ed30`; timeout-test stabilization commit `e2c9e7e1508eacff390f4ac2e9117230601df7ab`.
- Latest observed PR #48 host blob SHA: `a914d36b14bdb5b3207282e7e8a989484421ccdc`; latest observed C02 test blob SHA: `b5d190772d6458e2cdc3b2df3203053121e725be`.
- Prior CI run `42454767666` was successful (33 tests) on an earlier branch revision. Workflow-run lookup for C02 code commit `e2c9e7e1508eacff390f4ac2e9117230601df7ab` returned no PR-triggered workflow runs in the connector response. Therefore the prior CI result is not attributed to the updated C02 source SHA; exact-SHA CI remains NOT VERIFIED.

### DOC-003 synchronization
- Canonical Sandbox journal path: `ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/00_ROOT/NHAT_KY_THI_CONG.md`.
- GitHub DOC-003 path: `work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/00_ROOT/DOC-003_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md`.
- Exact UTF-8 prefix comparison: first 12,928 bytes of Sandbox journal matched GitHub DOC-003 byte-for-byte before sync.
- Appended the Sandbox journal continuation beginning at byte offset 12,928 after preserving the existing GitHub-specific addenda. No prior GitHub text was overwritten.
- GitHub DOC-003 new blob SHA after readback: `95588af96a7e7f07000d9f640f41263042a8ee73`.
- GitHub DOC-003 main blob remains `b5c6d2a24ce030546b8997ffe9e6d64f26f190a0`; this sync was written to the PR #48 branch only, not main.
- The existing GitHub-specific addenda and the Sandbox continuation were both retained; this was append-only synchronization, not a semantic deduplication or whole-file parity claim.

### Work 1111 Sandbox file Git-blob SHA-1 anchors
Computed from exact Sandbox readback using Git blob framing (`blob <UTF-8 byte length>\0<content>`); these are Sandbox content identifiers, not GitHub branch blob IDs.

| Sandbox canonical path (relative to Work 1111) | UTF-8 bytes | Git blob SHA-1 |
|---|---:|---|
| `00_ROOT/NHAT_KY_THI_CONG.md` | 60,962 | `648bae486c1e2cf70c27c5968a35207b1bfc97b2` |
| `02_EXTENSION/TECHNICAL_BASELINE_AND_OPEN_BLOCKERS.md` | 10,411 | `ef657d06b48272dfdd9cba2c410996e7fde60a5d` |
| `02_EXTENSION/AUTO_E2E_REMEDIATION_GATE_AND_PC_HANDOFF_20261108.md` | 11,288 | `3cc1740052b015cea46e2c315d53fd5b192f6c86` |
| `03_ARCHITECTURE/EXECUTION_HOST_LINES_RECONCILIATION_20261109.md` | 6,462 | `4b535cc5612e2e4c002c729c1ff71adf2f39ca32` |
| `03_ARCHITECTURE/PR48_SELF_REVIEW_PACKAGE_20261109.md` | 7,957 | `63f6e4b19292e23f6ba21f2921e7fd3f0436fc3e` |
| `02_EXTENSION/APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md` | 4,463 | `b48b6a691c784d309e7dfe2ce213cd6b3cfc9ad9` |
| `06_EVIDENCE/PC_READONLY_ATTESTATION_PACK_20261109.md` | 7,626 | `3aaef246487bf222b80875ecd9e17638fd78b492` |
| `01_DISCOVER/INVENTORY_CLASSIFICATION_W09_W102_20261109.md` | 5,121 | `392b9b6fda70e39346f0ec21cd4a5a63580df7b0` |

### Parity limits
- DOC-003 Sandbox continuation ↔ PR #48 branch: append operation acknowledged and GitHub fetch readback returned blob SHA above; the exact 12,928-byte prefix was verified before write.
- DOC-003 GitHub main was not changed.
- W1111 source/docs Sandbox ↔ GitHub branch parity is NOT VERIFIED for all eight files above; the table is a Sandbox hash baseline only.
- PC source/runtime parity remains NOT VERIFIED. No PC or runtime action was performed.


## ADDENDUM — 2026-11-09 — C08 HASH COMPLETION + LATEST DOC-003 REVISION

- Branch head immediately before this ledger update: `c8e325b318277cad727865d9597750ba7aed7fad`.
- Latest DOC-003 branch blob after appending the post-C05 journal delta: `6732228d0e0ff6d8e777b4b1ead1da1da1ef2fcc`; readback confirms C08 completion correction is present.
- Latest Sandbox canonical journal Git blob SHA-1: `53ba2e336b53a031081b43f0a4e9487123772299` (64,757 UTF-8 bytes).
- Latest W09/W102 inventory + duplicate-hash manifest Sandbox Git blob SHA-1: `a942ff67e4de487774878e312d9fdd089250ae72` (23,224 UTF-8 bytes).
- W102 pair 3 correction: file-only counts are 61 files vs 62; 61 common paths SHA-256 MATCH 61/61; archive-only README.md. Across all four W102 pairs, 73/73 shared files SHA-256 MATCH. Tree-shape extras remain; no cleanup performed.
- C08 final disposition: W09 inventory 4,127/4,127 classified; W102 duplicate hash inventory complete; READY FOR CLA REVIEW.

### CI query qualification correction
- The workflow file `.github/workflows/core-execution-authority.yml` defines both `pull_request` and `push` triggers for branch `work/w1111-core-execution-authority-v1-2`, plus `workflow_dispatch`.
- The GitHub connector's `fetch_commit_workflow_runs` action explicitly filters to pull-request-triggered runs only. Its empty result for C02 commit `e2c9e7e1508eacff390f4ac2e9117230601df7ab` therefore means **no PR-triggered run was returned**, not proof that no push-triggered run exists.
- No general workflow-run listing/dispatch action is exposed in the connected GitHub toolset, and the public Actions page could not be fetched in this session. Exact-SHA CI status for C02 remains **NOT VERIFIED**. Do not claim CI failure or PASS from the empty filtered result.


## FINAL ADDENDUM — 2026-11-09 — C05 POST-C08 JOURNAL SYNC READBACK

- Branch head immediately before this DOC-010 update: `93a9eff7d180956625900a8e85509b51fbacfafc`.
- DOC-003 latest branch blob after syncing the final C08/CI-scope journal delta: `3b49bd58fea1b165dbea90cfc7e6ddd25463d7b6`; GitHub readback succeeded and includes the latest journal continuation.
- Latest Sandbox canonical journal Git blob SHA-1: `62c3f4609065af28fcbedf18678f49b32a0ebf66` (66,192 UTF-8 bytes).
- Latest W09/W102 inventory manifest Sandbox Git blob SHA-1 remains `a942ff67e4de487774878e312d9fdd089250ae72` (23,224 UTF-8 bytes).
- C08: 4,127/4,127 W09 entries classified; W102 shared file hashes 73/73 MATCH across all four requested pairs; extra files/directories remain preserved and documented.
- C02: workflow defines push and pull_request triggers. The connected commit-workflow query only exposes pull_request-triggered runs; exact-SHA push-run status remains NOT VERIFIED. Prior run 42454767666 is not attributed to updated C02 SHA.
- This ledger update is docs-only on PR #48 branch. No main, PC, runtime, merge or release action.
