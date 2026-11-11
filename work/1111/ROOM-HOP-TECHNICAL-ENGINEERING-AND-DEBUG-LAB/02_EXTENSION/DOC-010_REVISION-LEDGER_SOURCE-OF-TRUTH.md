# DOC-010 — REVISION LEDGER / SỔ THEO DÕI PHIÊN BẢN

Ngày lập: 2026-11-08 (UTC+7)
Work: 1111 — ROOM-HOP Technical Engineering & Debug Lab
Repository: hqtt2026-thevinhvtqni/room-meeting-ai
Canonical branch: main

## 1. Revision anchor

| Layer | Revision / evidence | Disposition |
|---|---|---|
| GitHub main | Latest commit returned by repository commit search: c3ba11597563d2dc62d031d169a457c4d29276b3 | Search result is the current observed anchor; not PC/runtime attestation |
| Sandbox Work 1111 | work_id=1111; canonical folder ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/ | Read/write collaboration surface |
| PC working copy | No live PC query performed in this session | NOT VERIFIED; do not infer clean/dirty or parity |
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

Note: blob SHA identifies file content, not commit SHA. The above are observed GitHub fetch_file results from ref=main during this session.

## 3. Parity and drift rules

1. Compare exact canonical path first, then blob/content hash; filename similarity is not proof of equivalence.
2. A GitHub commit SHA, file blob SHA, Sandbox readback, PC working-tree state and deployed runtime build hash are distinct evidence types.
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


## 2026-11-10 — Addendum: current GitHub revision snapshot (Co, UTC+7)

Observation method: GitHub REST refs, PR #48 metadata, commit compare, workflow run/job and exact source fetch. This is a point-in-time read, not PC/runtime attestation.

| Object | Observed revision/state | Evidence scope |
|---|---|---|
| Repository default branch `main` | `a112e5a5a6a9d947285475d4dec66b3968ced0a4` | Current ref at observation time |
| PR #48 head branch | `work/w1111-core-execution-authority-v1-2` | PR remains OPEN / DRAFT |
| PR #48 current head | `cf9d7ce7bd7ea476ead5cb64a65ac2f06698a55f` | Branch ref and PR head agree |
| Successful CI run | `42732254869` on `9bbeed63dfbdcc6a00b8bdb31c3db1b00b812197` | Workflow job and three pytest steps completed SUCCESS |
| Compare CI SHA → current PR SHA | `ahead=1, behind=0` | Only changed file is DOC-003 journal (+13 lines); no source/test changed after tested SHA |
| Root aggregate host source | blob `a914d36b14bdb5b3207282e7e8a989484421ccdc` | PR branch `execution_host/host.py` |
| Aggregate host authority tests | blob `c8e03e7fbd8a7da78ae1ba61ed67cffc5dfc7b09` | PR branch `tests/test_execution_host_authority.py` |

### Journal synchronization disposition

Sandbox canonical journal and GitHub DOC-003 are NOT byte-identical. They share the first 17,860 characters, then diverge (for example, one sentence differs in the T01 revision-ledger entry); GitHub DOC-003 is 20,529 characters and Sandbox journal is larger. Do not replace either copy wholesale. A controlled merge/reconciliation is required before claiming DOC-003 parity.

### Current gate

- PR #48: OPEN / DRAFT; not merged.
- Source/CI: successful for SHA `9bbeed63dfbdcc6a00b8bdb31c3db1b00b812197`; current PR head `cf9d7ce7bd7ea476ead5cb64a65ac2f06698a55f` adds only a journal documentation commit.
- Sandbox↔GitHub DOC-003: DRIFT / NOT BYTE-PARITY.
- PC↔GitHub and PC↔Sandbox: NOT VERIFIED.
- Live Core/Host E2E: BLOCKED / NOT VERIFIED.
