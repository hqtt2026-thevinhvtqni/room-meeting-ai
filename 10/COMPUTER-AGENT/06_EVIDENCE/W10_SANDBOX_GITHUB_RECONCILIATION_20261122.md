# WORK 10 — SANDBOX / GITHUB RECONCILIATION
- Record: W10-SYNC-20261122-01
- Date-Time: 2026-11-22 04:48 (UTC+07:00)
- Executor: Co — AI-07 / End-to-End Architecture & Implementation Lead
- Scope: read-only inventory + documentation/evidence synchronization
- Canonical repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Canonical branch: `work/10-computer-agent-mirror`
- Branch HEAD before this synchronization: `7ea300b2d3d14552f9dfc31038b83b59d1dc2ab6`
- Protected baseline retained: `0cad66c59560450d68b06e76a659a6c44104e811`

## 1. Inventory result
- Sandbox Work ID 10: 151 listed entries under `COMPUTER-AGENT/`.
- GitHub canonical branch before this record: 38 listed entries under `10/COMPUTER-AGENT/`.
- Shared paths: 37.
- Sandbox-only paths: 114.
- GitHub-only path: `05_TEST/HOST_E2E_RUNBOOK.md`.
- This is a path inventory, not a claim that all shared file contents match.

## 2. Documentation/evidence synchronized Sandbox → GitHub
The following seven paths were written to the canonical branch and then fetched back from GitHub. Every readback was compared byte-for-byte as decoded UTF-8 text with Sandbox; all seven comparisons were EXACT MATCH.

| Sandbox path | GitHub path | Result |
|---|---|---|
| `00_ROOT/WORK_MANIFEST.md` | `10/COMPUTER-AGENT/00_ROOT/WORK_MANIFEST.md` | UPDATED / EXACT |
| `00_ROOT/SYNC_POLICY.md` | `10/COMPUTER-AGENT/00_ROOT/SYNC_POLICY.md` | UPDATED / EXACT |
| `README.md` | `10/COMPUTER-AGENT/README.md` | UPDATED / EXACT |
| `BIEN_BAN_W10.md` | `10/COMPUTER-AGENT/BIEN_BAN_W10.md` | CREATED / EXACT |
| `NHAT_KY_THI_CONG_W10.md` | `10/COMPUTER-AGENT/NHAT_KY_THI_CONG_W10.md` | CREATED / EXACT |
| `06_EVIDENCE/W10_P0_ACCEPTANCE_INTEGRITY_AMENDMENT_20261119_07.md` | same relative path under `10/COMPUTER-AGENT/` | CREATED / EXACT |
| `06_EVIDENCE/W10_P0_ACCEPTANCE_MANIFEST_V7.schema.json` | same relative path under `10/COMPUTER-AGENT/` | CREATED / EXACT |

GitHub commit SHAs returned by the write operations:
- Manifest: `6663b10c729da74f53cd6d7f4395a8ac7edf9b49`
- Sync Policy v1.2: `9ef90e4b797ecb1a062b9292ec9f8d7b6b04757e`
- README: `a0975639ea03ed13e85b15d625404d7dd02efefe`
- Work minutes: `a0576cd1d7102bac0e90d443f54ec4bf7e6eedfb`
- Construction journal: `9cdb66aa0ebcbb227aa588c4ef02d31e119378b1`
- P0 amendment v7: `c85e335e7b30fbb65069ba49911773c316cc4574`
- P0 schema v7: `41a1873f5cfb5aa48e2b03b92a2d0707c4ee2b17`

## 3. Source/test divergence — NOT synchronized
Static content comparison confirms the following Sandbox files differ from the canonical branch:
- `04_CODE/agent_api.py`
- `04_CODE/agent_runtime.py`
- `04_CODE/models.py`
- `04_CODE/browser_adapter.py`
- `05_TEST/test_p0_p5.py`

The Sandbox also contains `05_TEST/test_http.py`, which is absent from the canonical branch. The canonical branch's current code remains the older implementation. These differences are not overwritten or promoted in this synchronization.

Reason: the latest Work 10 P0 acceptance amendment dated 2026-11-19 explicitly records P0 implementation as BLOCKED / NOT AUTHORIZED, validator and host tests NOT RUN, and An's independent re-review still pending. Copying the Sandbox runtime/tests into the canonical branch now would bypass those gates and would not establish verified source parity.

## 4. Protected boundaries
- The three locked contracts remain unchanged: `ACTION_CONTRACT.md`, `WORKFLOW_CONTRACT.md`, `SAFETY_POLICY.md`.
- No force push, history rewrite, merge, release, or production change.
- No code or test file was promoted.
- The separate `Computer-Agent` repository was not treated as canonical and was not modified.

## 5. Current disposition
- Documentation/governance/evidence sync: **COMPLETE for the seven paths listed above; readback exact**.
- Full Sandbox ↔ GitHub synchronization: **PARTIAL / NOT COMPLETE**.
- Source parity G0: **BLOCKED**.
- Runtime/security/host validation gates: **BLOCKED / NOT RUN** as recorded in the current Work 10 manifest and P0 amendment.
- Work 10: **ACTIVE — NOT RELEASED**.

## 6. Next authorized sequence
1. Reconcile the remaining 114 Sandbox-only paths into KEEP / UPDATE / CONFLICT / SANDBOX-ONLY classes; do not bulk-copy cache, generated, or proposal artifacts.
2. Obtain An's independent re-review of the V7 acceptance design and required authorization for P0 implementation.
3. On an approved child branch, implement only the accepted changes; preserve the three locked contracts.
4. Run exact-revision offline/HTTP tests and supported Windows/Chromium host validation; retain source hashes and artifacts.
5. Reconcile accepted source/test files to the canonical branch and repeat exact readback.

**No PASS is claimed for runtime tests, PC execution, Chromium E2E, or release.**


## Correction — independent review status (2026-11-22 04:49 UTC+07:00)
The original reconciliation text said An's independent review was pending. That statement reflected the V7 amendment's next-step note but was stale: the Sandbox already contains `10_AI_DEBUG_HANDOFF/03_VALIDATION/AN_P0_DESIGN_REVIEW_RESULT_20261119_07.md`, dated 2026-11-19. An completed the static review and left AN-V7-F01..F04 OPEN/BLOCKED; AN-V6-F01..F03 are not ready to close. P0 implementation remains BLOCKED / NOT AUTHORIZED. The seven-path exact-match sync result and source/test divergence findings above are unchanged.


## Final snapshot after follow-on V8 and CI records — 2026-11-22 04:54 (UTC+07:00)
- Current inventory: Sandbox 155 entries; GitHub branch 44 entries; 43 shared paths; 112 Sandbox-only paths; 1 GitHub-only path (`05_TEST/HOST_E2E_RUNBOOK.md`). Counts include directories and files.
- In addition to the first seven governance/evidence files, the reconciliation report, V8 design amendment, An V8 review task and GitHub Actions CI evidence were also created on both sides and read back as exact UTF-8 matches. WORK_MANIFEST and construction journal updates were also read back as exact matches.
- The five production source/test files remain divergent: `agent_api.py`, `agent_runtime.py`, `models.py`, `browser_adapter.py`, `test_p0_p5.py`; `test_http.py` remains Sandbox-only. No source/test promotion occurred.
- GitHub Actions run #29 (ID 44953846300) passed syntax, offline contract tests and real Chromium E2E on commit `afa7c084104e336b63cbd1cd37dd4bfe21a4a23b`; its scope is Ubuntu 24.04 GitHub runner code only. The subsequent branch commit `e7e3397c1034f4a3225e6dff07b4be3f387b4647` changed the journal only, not production code.
- An's V7 review is complete and findings remain open. V8 design proposal and An review task are mirrored; task acknowledgement/review is still pending.
- Disposition unchanged: documentation/evidence mirror materially improved; full Sandbox/GitHub parity remains PARTIAL / NOT COMPLETE; G0 and P0 remain BLOCKED; Work 10 ACTIVE — NOT RELEASED.


## Full path inventory disposition — 2026-11-22 06:32 (UTC+07:00)

A new complete path inventory was generated from the live Sandbox listing and GitHub branch tree:
- Sandbox: 157 files under `COMPUTER-AGENT/`.
- GitHub branch: 64 files under `10/COMPUTER-AGENT/`.
- Shared paths: 64.
- Sandbox-only files: 93.
- GitHub-only files: 0.
- One Sandbox-only `.github/` directory contains the Sandbox-local workflow copy.

All accepted source/test/architecture/config files are in the shared set and were compared exactly in the independent source/test batches. The three LOCKED contracts are exact-match. Selected current governance, evidence, Dashboard, runbook and handover files were also read back and compared after updates.

The 93 Sandbox-only files have explicit KEEP / SANDBOX-ONLY disposition in `06_EVIDENCE/W10_FULL_PATH_INVENTORY_DISPOSITION_20261122.md`: generated caches/locks/runtime outputs (10), original/reference/preview material (8), historical evidence/design records (47), immutable AI debug handoff archive (26), superseded 2026-11-17 handover (1), transcript archive (1). They are intentionally not bulk-synced to the canonical branch.

Disposition: accepted source/test/architecture/config parity is PASS for the current shared set; path inventory reconciliation is complete by explicit dispositions. Directory trees are not identical by design. Work 10 remains ACTIVE — NOT RELEASED.


## Inventory count correction — 2026-11-22 06:33 (UTC+07:00)

The inventory document itself was added to both Sandbox and GitHub after the preceding snapshot. Updated live counts: Sandbox 158 files, GitHub 65 files, shared 65, Sandbox-only 93, GitHub-only 0, plus one Sandbox-only `.github/` directory. The 93 KEEP/SANDBOX-ONLY file dispositions remain unchanged.


## W10-ROOM-HOP-BOUNDARY-AND-PORT-3010-20261122-01 — 2026-11-22 06:35 (UTC+07:00)

Co xác lập ranh giới tích hợp: Work10 là local Computer Agent provider, loopback-only; W24 giữ Core authorization + authenticated PC transport; W112 giữ cross-Work contracts; W14 giữ canonical W12/W13/W14 execution boundary; W113 giữ shared Dashboard ingress port 3000. Work10 standalone Dashboard chuyển sang loopback port 3010, không chiếm port 3000. Không remote expose API, không bypass Core, không thay W14, không sửa các Work khác. Handoff: `06_EVIDENCE/W10_ROOM_HOP_INTEGRATION_BOUNDARY_HANDOFF_20261122.md`. Integration runtime W10↔W24/W14/W113 còn NOT IMPLEMENTED / NOT VERIFIED.

## W10-INVENTORY-COUNT-CORRECTION-20261122-02 — 2026-11-22 06:36 (UTC+07:00)

Sau khi tạo và đồng bộ integration boundary handoff, snapshot mới: Sandbox 159 files; GitHub 66 files; shared 66; Sandbox-only 93; GitHub-only 0. Một thư mục `.github/` chỉ ở Sandbox. 93 Sandbox-only file dispositions không đổi. Inventory report đã được cập nhật.


## Inventory count correction — 2026-11-22 06:38 (UTC+07:00)

After adding the Run #104 evidence and POSIX cleanup remediation evidence to both Sandbox and GitHub, the current inventory is Sandbox 161 files; GitHub 68 files; shared 68; Sandbox-only 93; GitHub-only 0; one Sandbox-only `.github/` directory. The 93 Sandbox-only KEEP dispositions are unchanged.
