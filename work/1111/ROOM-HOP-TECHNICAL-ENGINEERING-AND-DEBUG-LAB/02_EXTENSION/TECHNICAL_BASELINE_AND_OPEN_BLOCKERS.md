
# TECHNICAL BASELINE & OPEN BLOCKERS — WORK 1111

Ngày khảo sát: 2026-11-08  
Nguồn thao tác: ROOM-HOP MCP 8030, Sandbox Works và hồ sơ kỹ thuật đã lưu.  
Phạm vi: baseline ban đầu, không phải nghiệm thu toàn hệ thống.

## 1. Source-of-truth và môi trường

| Lớp | Vai trò tạm xác định | Bằng chứng / giới hạn |
|---|---|---|
| GitHub | Nguồn chuẩn cho source code và revision đã phát hành | W32 audit phân biệt exact branch/SHA; W1111 chưa tự truy vấn HEAD hiện tại |
| Sandbox | Không gian AI đọc/ghi hồ sơ, candidate và phối hợp | MCP context xác nhận Sandbox read/write |
| Working Source qua MCP | Read-only | get_room_context |
| PC | Runtime/working copy cục bộ, cần đối chiếu theo exact path/SHA | W70 log ghi nhận working tree dirty và parity chưa xác minh |
| MCP 8030 | File operations trong Sandbox | get_room_structure; không có process/pytest execution trong capability list |
| Git merge/commit/push | Không thuộc quyền AI trong MCP boundary hiện tại | get_room_context |

Đây là mô hình vận hành ban đầu. Chưa coi GitHub/Sandbox/PC đã đồng bộ.

## 2. Bản đồ thành phần ROOM-HOP (danh mục cần xác minh)

- Core :8000 — authority / application truth.
- Dashboard :3000 — render-only, không được dùng làm authority.
- Workspace :8010 — workspace/application layer.
- Gateway :8040 — gateway.
- Event Listener :8050 — event intake.
- Agent Runtime :8051 — runtime agent.
- Build MCP :8030 — Sandbox build/file operations.
- Execution Host :8031 — execution host cần xác minh contract và đường gọi thực.
- Adapter / Browser Agent — cần phân biệt source, process, health, contract và E2E evidence.
- Agent Registry / Principal / Policy / Token — cần kiểm tra mapping identity và quyền theo hồ sơ canonical.

Tên/cổng ở trên là baseline danh mục từ hồ sơ dự án; trạng thái live của từng service chưa được xác minh trong lượt này.

## 3. Nút thắt đã có bằng chứng

### B-1111-01 — GitHub/Sandbox drift (W32)
- Evidence: audit 2026-11-07 ghi 6/6 cặp file DRIFT.
- Impact: review hoặc test trên mirror cũ có thể xác nhận sai revision.
- Next: lập mapping exact branch + SHA + path + blob/hash; chỉ đồng bộ theo change control, không overwrite mù.

### B-1111-02 — Windows Browser E2E / release gate (W32)
- Evidence: Run #133, SHA 554ebe3145e8b13206b50d8722879b0bae3db094; Windows job SKIPPED; release gate FAILURE.
- Impact: W32 chưa RELEASED; hosted tests không thay thế Windows live lane.
- Next: xác minh runner readiness và service provenance theo đúng hồ sơ; không bypass readiness guard.

### B-1111-03 — Thiếu execution adapter qua MCP
- Evidence: MCP capability/context và W102 integration gap ledger.
- Impact: không thể tuyên bố pytest đã chạy chỉ từ việc tạo/đọc file; không có stdout/stderr, exit code hay test result thực.
- Next: khảo sát công cụ execution host/CI có thể truy cập; thiết lập exact-SHA run evidence và readback.

### B-1111-04 — PC/GitHub/Sandbox parity chưa xác minh (W70)
- Evidence: DOC-035 ngày 2026-11-08; PC working tree dirty, mirror path mismatch.
- Impact: thao tác đồng bộ hoặc cleanup có thể phá thay đổi chưa commit.
- Next: chỉ read-only inventory; path/hash mapping; không reset/clean/stash/checkout hoặc overwrite.

### B-1111-05 — Inventory noise (W09)
- Evidence: sandbox listing có 4,127 entries, bao gồm .venv, site-packages, __pycache__.
- Impact: khó phân biệt source, dependency cache và runtime artifacts.
- Next: phân loại file-level; chưa xóa/di chuyển.

## 4. Những gì chưa được xác minh
- GitHub main và từng branch HEAD tại thời điểm hiện tại.
- Live health/contract của các service và ports.
- Registry identity/principal/policy/token đầy đủ.
- Runner/service state thực tế trên PC.
- Pytest execution trong MCP session.
- Exact SHA parity GitHub↔Sandbox↔PC.
- Dependency graph hoàn chỉnh giữa các Work.

## 5. Kết luận baseline
DISCOVER = PARTIAL.  
Không có source mutation, Git mutation, PC mutation, test execution hoặc release action trong lượt khảo sát này.  
Các kết luận được giới hạn đúng theo hồ sơ đã đọc; cần bổ sung kiểm chứng live trước khi nâng trạng thái.

## Bổ sung/correction sau GitHub source trace — 2026-11-08
Nhận định "không có execution host" sẽ là sai. Source GitHub main có Execution Host :8031 và code thực thi process thật. Kết luận đúng là: MCP 8030 không expose process/pytest action trong phiên hiện tại; live service :8031 và revision được deploy chưa được xác minh. Branch work/28-mcp-tooling-platform có handler hardening riêng, nhưng main vẫn trả source handler khác; không đồng nhất hai nhánh. DOC-061 trên GitHub main còn ghi nhận các giới hạn auth/grant/snapshot và potential false aggregate PASS. Chi tiết và SHA được lưu tại 03_ARCHITECTURE/EXECUTION_HOST_SOURCE_TRACE.md.

## 2026-11-08 — AUTO E2E assignment: Core authority and runtime blockers

- MCP 8030 connector surface in this session is file-only; no process/pytest/runtime execution action is exposed.
- GitHub main source review confirms Core HTTP adapter currently exposes Identity/Meeting routes only; MeetingService/MeetingManager are Meeting-specific. Work-scoped execution grant/run API, Work authority persistence and authorization enforcement are not evidenced. W70 DOC-071 records Core owner NOT IDENTIFIED and runtime NOT VERIFIED.
- W28 Core authority blocker confirms the proposed execution-grant contract remains DESIGN/PROPOSED, NOT APPROVED, NOT IMPLEMENTED and NOT WIRED. Do not invent/call the proposed route; direct MCP→W13 bypass remains prohibited.
- GitHub main Execution Host POST /execute constructs WorkContext from caller JSON; caller-supplied authorized boolean is not caller authentication or a Work grant. Work13 canonical Sandbox server remains pre-hardening and enables process execution without HTTP principal auth.
- W28 hardened handler exists only on a separate branch and uses shared bearer token + static Work allow-list; this is not per-agent/assignment authorization and no deployment proof exists.
- Source defect: ExecutionHost.execute_work() stores nested test result but returns top-level status from primary command. A passing primary command can mask a nested test BLOCKED/FAILED/TIMEOUT. Regression coverage is absent in the inspected test file.
- W13 canonical runtime identity record is BLOCKED (startup NOT_EXECUTED; health/execute/identity NOT_OBSERVED). Historical narrow HTTP E2E PASS does not prove current Core→MCP→Host E2E.
- PC is required for read-only current runtime attestation (PID, command line, build hash, bind address, config presence) and later controlled live execution/deployment. Current loopback 127.0.0.1:8031 is not an independent cloud host.
- Disposition: Core authority BLOCKED; Host authentication BLOCKED; runtime NOT VERIFIED; aggregate test propagation SOURCE DEFECT FOUND; full E2E BLOCKED. No source, Core, PC, task-board, Git commit/push/merge or runtime mutation performed.
- Canonical runbook created: 02_EXTENSION/AUTO_E2E_REMEDIATION_GATE_AND_PC_HANDOFF_20261108.md. No PASS claimed.


## ADDENDUM — 2026-11-09 — IMPLEMENTATION STATUS AFTER PR #48 (NO HISTORY REWRITE)
- Revision scope: branch `work/w1111-core-execution-authority-v1-2`, draft PR #48, CI run `42454767666`, as referenced by the current W1111 assignment/baseline. These identifiers are anchors from recorded evidence; this addendum does not independently re-fetch or re-run the workflow.
- Recorded CI result: 33 passed (16 Core/Core HTTP + 6 W12 host + 11 W13 bridge/integrated E2E). Claim scope is source-level CI for that branch/revision only.
- This does NOT establish production/live PC/cloud E2E, deployed runtime parity, service restart, current PID source identity, Core journal durability after restart, or Sandbox/GitHub parity.
- Core authority V1.2 implementation is recorded as present on the branch and draft PR #48; do not describe it as merged to `main`, deployed, or owner-approved unless a separate exact evidence/decision supports that claim.
- Outstanding configuration/deployment gates remain: actual :8000 launcher integration without duplicate listener; local service credential provisioning; durable journal path; canonical Work policy and exact source hash; WEE service environment/private Core URL; exact W12/W13 deployment; runtime module path/hash/PID attestation; positive and negative live probes; journal persistence and Sandbox/GitHub parity.
- PC PID 16484 historical record remains not restarted; no live POST /execute is evidenced by the cited baseline.


<!-- C01 SOURCE PRESERVATION: top-level legacy source; prior content preserved verbatim on 2026-11-09 UTC+7 -->


## 2026-11-08 — CO — UPDATE AFTER APPROVED IMPLEMENTATION
- Core Execution Authority V1.2 (DR-1..DR-4) has source implementation on branch work/w1111-core-execution-authority-v1-2; draft PR #48; main remains untouched.
- GitHub Actions run 42454767666 succeeded: 16 Core/Core HTTP tests + 6 W12 host tests + 11 W13 bridge/integrated E2E tests = 33 passed.
- Integrated CI path: real Core FastAPI routes → WEE service identity/grant → W13 HTTP grant validation → canonical W12 RealExecutionHost → FINAL_RESULT.json → Core append-only RUN_RECORDED.
- Source-level CI E2E is PASS. Production/live PC/cloud E2E remains NOT PASS.
- Remaining blockers: integrate Core HTTP app with actual :8000 launcher (do not create duplicate listener); generate/store service credential locally; configure durable journal path; configure at least one canonical Work policy and exact source hash; configure WEE service env and private Core URL; deploy/restart exact W12/W13 source; verify runtime module path/hash/PID; execute positive/negative live probes; verify Core journal survives restart and Sandbox/GitHub parity.
- Current PID 16484 was not restarted and no live POST /execute was sent. PC handoff is required now for deployment/configuration and Windows runtime attestation.
<!-- END C01 SOURCE PRESERVATION -->


## ADDENDUM — 2026-11-10 09:28 UTC+7 — Co pre-PC review

- Rechecked C01 legacy pointers: all three outer files contain LEGACY_NOTICE and point to canonical documents.
- Rechecked C03/C04/C06/C07 artifacts: present/readable. C04 remains DRAFT pending explicit owner decision; C06 is a static gap inventory; C07 is a read-only PowerShell handoff and has not been run on PC.
- C02 is PARTIAL: branch `cf9d7ce7bd7ea476ead5cb64a65ac2f06698a55f` root host source blob `a914d36b14bdb5b3207282e7e8a989484421ccdc` propagates nested FAILED/BLOCKED/TIMEOUT when the primary command passes and preserves primary failure. The canonical test file lacks explicit `run_test=False` and nested TIMEOUT coverage; the Sandbox candidate patch is empty. Do not mark C02 DONE.
- PR #48 remains OPEN/DRAFT. CI run #42732254869 passed on `9bbeed63dfbdcc6a00b8bdb31c3db1b00b812197`. Current branch/PR head is `cf9d7ce7bd7ea476ead5cb64a65ac2f06698a55f`, one docs-only commit ahead and zero behind; compare shows only DOC-003 journal changed (+13 lines). Thus code/test content is unchanged since the successful run, but no run is attached directly to cf9d.
- C09 remote-transport TLS patch and three regression tests are recorded in PR body; this remains source/CI evidence, not live deployment.
- Remaining PC-dependent gates: Core :8000 actual launcher/module identity; :8031 PID/executable/command line/CWD/module import/source hashes; current Git branch/HEAD/dirty tree; presence-only secret configuration; after owner review, controlled positive/negative live probes and journal persistence.
- No PC, runtime, secret, merge, push, or release operation was performed. Full live E2E remains BLOCKED / NOT VERIFIED.

## Addendum 2026-11-10 10:45 UTC+7 — C02 follow-up
- C02 regression coverage expanded from 5 to 8 tests on PR #48 branch.
- Added nested TIMEOUT propagation, nested execution-error BLOCKED, and primary TIMEOUT preservation tests.
- Commit: 611a6ff3f71207c0af746278bb282c0ffcaf45cd; test blob: 61bc96d15f04d6218d22d7119856fedbfdf62401.
- GitHub readback confirms all 8 tests exist. Exact-HEAD workflow/status lookup immediately after push returned no records; C02 remains PARTIAL / WAITING_FOR_EXACT_HEAD_CI. No pytest PASS claim.
- PR #48 remains OPEN/DRAFT/unmerged. No PC/runtime action and no local Git dirty-tree mutation.
- Evidence: ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/06_EVIDENCE/C02_AGGREGATE_STATUS_REGRESSION_FOLLOWUP_20261110.md.
## Addendum 2026-11-10 10:46 UTC+7 — C02 timeout-test robustness
- Both new timeout regression tests use 0.5-second timeout against a 2-second sleep to reduce process-startup flakiness.
- Follow-up commit 647d4aa2b159a9e4dacd86d8b71fe68e820deab5; current test blob 7af2c39007274cfc4c69e3f5fc3f79ce77c632cf; 8 tests confirmed by GitHub readback.
- Exact-HEAD workflow and combined status are still empty; C02 remains PARTIAL / WAITING_FOR_EXACT_HEAD_CI.