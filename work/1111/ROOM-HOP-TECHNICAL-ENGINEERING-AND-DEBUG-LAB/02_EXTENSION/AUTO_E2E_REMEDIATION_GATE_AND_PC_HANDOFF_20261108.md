# AUTO E2E REMEDIATION GATE & PC HANDOFF — W1111
**Ngày:** 2026-11-08  
**Giờ:** 12:40 UTC+7  
**Người thực hiện:** Co — AI Technical Reviewer / Coder
**Chỉ thị:** Thực hiện toàn trình Core → Execution Host → Sandbox → GitHub; tự xử lý trong phạm vi công cụ/quyền; không báo tiến độ trung gian; chỉ yêu cầu PC khi cần thao tác/runtime không thể truy cập từ phiên này.

## 1. Kết luận kiến trúc đã xác minh
### 1.1 MCP 8030
- get_room_structure trả capability file-only: sandbox_list/read/create/write/append/delete/create_work/list_works.
- Không có process execution, pytest, shell, runtime attach hoặc Core execution action trong connector surface hiện tại.
- Không thể dùng thao tác file Sandbox để tuyên bố process/pytest đã chạy.

### 1.2 Core
Đối chiếu source GitHub main:
- room_hop_mcp/adapter/http_server.py — blob 54cb3ecbce2e6b13083f31c14f0c1f0738f1457d: routes /identities và Meeting lifecycle; không có Work execution-grant/run route.
- core/meeting_service.py — blob 0b80a81663c1be328c41878a6762d16d95378aab: Meeting-specific service.
- core/meeting_manager.py — blob d4d7b28f0f0df9208648d0870c42cb6e451eda50: Meeting file persistence; không phải Work authority store.
- core/agent_registry.py — blob 7e4b98e68fa1a208ebd5788d9235d9c222e402a3: registry không enforce permissions/authority.
- core/principal_registry.py — blob 1eda0c80f413c1405415f92e0e2ff3b82a43b5ef: principal registry không phải Work authorization middleware.
- W70 DOC-071 (GitHub blob 12f11320dc9da89b27de21313b698224d74519ce) kết luận Core owner NOT IDENTIFIED; Work/WP/Assignment/Evidence service, authoritative persistence và Work-scoped authorization chưa được xác minh.
- W28 evidence VI_CORE_AUTHORITY_DEPENDENCY_BLOCKER_20261103.md xác nhận nhánh work/28-mcp-tooling-platform không có execution-grant/run API; contract đề xuất còn DESIGN/PROPOSED, NOT APPROVED, NOT IMPLEMENTED, NOT WIRED. Không được tự gọi route đề xuất hoặc giả lập grant.

### 1.3 Execution Host
- GitHub main execution_host/server.py blob 45aec57525b5d55bb63544b7bd7fd23062e06151: POST /execute dựng WorkContext trực tiếp từ body; handler không thể hiện HTTP principal authentication/Work grant enforcement.
- execution_host/models.py blob 2488b7c95cf3784fc26eaf677044fe5ab0866420: WorkContext nhận authorized: bool từ caller; đây không phải chứng minh authorization.
- execution_host/host.py blob 977b5bc5072eaf0a3ad054aecd22491483d621b1: chạy subprocess và ghi evidence. Khi run_test=True, kết quả test được đặt ở nested result['test'] nhưng top-level status vẫn lấy status của command chính. Trường hợp test con BLOCKED/FAILED có thể bị báo PASS giả.
- Work 13 Sandbox canonical EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/server.py là pre-hardening, khởi tạo W12ExecutionAdapter với allow_processes=True, không có HTTP auth header gate.
- Work 13 w12_adapter.py từ chối run_test, collect_artifacts và timeout override; bridge mặc định 127.0.0.1:8031.
- W28 hardened server blob 87644127a9a2df638b5677758cfc4d0c883b2985 chỉ nằm trên branch riêng; shared bearer token + static Work allow-list không tạo per-agent principal/assignment authority. Không có bằng chứng branch đó đã được deploy hoặc chạy.

### 1.4 Runtime / PC
- W13 canonical runtime identity FINAL_RESULT: BLOCKED; canonical startup NOT_EXECUTED; health/execute/runtime identity NOT_OBSERVED.
- EXECUTION-CURRENT.json ghi một HTTP E2E PASS lịch sử nhưng contract bridge tests chưa chạy; không chứng minh Core→MCP→W13 live E2E hoặc current deployment.
- Endpoint hiện ghi trong handoff là loopback 127.0.0.1:8031; loopback không phải host độc lập có thể được Core/cloud gọi từ xa.
- PC process/PID/build hash/auth config hiện tại chưa được xác minh. Cần PC cho runtime attestation và bất kỳ bước triển khai/khởi chạy Host nào trên PC. Không gửi lệnh /execute cho đến khi Core-derived authority contract được phê duyệt và kiểm chứng.

## 2. Gate status
| Gate | Status | Điều kiện đóng |
|---|---|---|
| MCP file I/O | VERIFIED | Đã đọc/ghi/readback file Sandbox |
| Core Work authority API | BLOCKED | Core owner + contract được Vinh phê duyệt + source/runtime route + authz tests |
| Host HTTP authentication | BLOCKED | Authenticated principal, Work grant, fail-closed tests; không dùng caller boolean |
| Host runtime deployment | NOT VERIFIED | PID, startup provenance, source/build hash, bind/network boundary |
| Host → Sandbox workspace | PARTIAL / NOT VERIFIED | Exact Work binding, path containment, process evidence and readback |
| Aggregate test result | SOURCE DEFECT FOUND | Fix top-level status propagation + regression test for nested failure/block |
| GitHub sync from execution | NOT VERIFIED | Host/Core-mediated branch operation with approved authority and remote SHA readback |
| Full E2E | BLOCKED | Positive + negative live tests through MCP → Core → Host → Sandbox → GitHub |

## 3. Safe implementation order
1. Pin exact Core source/runtime and identify accountable Core owner; do not invent routes.
2. Obtain approval for Core Execution Authority contract (principal derived server-side; Work grant; append-only run record; immutable source snapshot/hash; evidence references).
3. Implement Core-owned authenticated route and canonical Work binding; add negative tests for forged identity/authorized/path/work_id.
4. Harden the canonical Host handler to accept only Core-authenticated scoped grants, not caller-provided authorized=true; configure private service-to-service transport and bounded body/timeouts.
5. Correct aggregate result propagation: overall PASS requires command PASS AND test PASS AND evidence integrity/cleanup verified; nested BLOCKED/FAILED/TIMEOUT must propagate.
6. Bind Sandbox workspace to canonical Work ID and immutable source SHA; reject traversal/symlink/reparse escape.
7. Wire MCP execution tools only through Core; keep direct MCP→localhost:8031 prohibited.
8. Run positive and negative E2E; collect request/run ID, source SHA, runtime identity, exit code, stdout/stderr, FINAL_RESULT, artifact hashes, cleanup and GitHub remote readback.
9. Remove laptop dependency by deploying the approved Host/runner in a managed environment reachable privately by Core, with managed secrets and persistent evidence. PC-hosted loopback is only a temporary local lane, not the target architecture.

## 4. PC handoff — required only for runtime/deployment stage
When requested, collect read-only:
- Listener PID for TCP 8031, executable path and full command line.
- Service/process startup mechanism and working directory.
- Runtime /health identity (instance_id, build_hash, PID, platform, bind_address) and compare with source SHA.
- Current PC working tree/branch/head and source file hashes.
- Do not expose token values; report only whether required secret/config variables exist.
- Do not start/stop/restart, patch, or send POST /execute until authorization boundary and rollback are approved.

## 5. Change boundary
- No Core source mutation, no Work 13 source mutation, no Host deployment change, no Git commit/push/merge, no PC action, no /execute invocation in this pass.
- No Task Board status/ACK changed.
- No PASS claim for runtime, pytest or E2E.
- This runbook records verified source findings and explicit prerequisites; it is not a release approval.
## 6. Explicit Core approval checkpoint
- Existing canonical proposal: Work 28 Sandbox / MCP-8020-TOOLING-PLATFORM/03_ARCHITECTURE/PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md (V1.2).
- Its current status is DESIGN/PROPOSED — NOT APPROVED, NOT IMPLEMENTED, NOT WIRED. It explicitly assigns final approval to Vinh and requires DR-1..DR-4 plus gates 1–5 in order.
- Co will not infer approval from the general delegation, invent endpoints, create a parallel authority service, or bypass Core directly to W13.
- Required decision: Vinh approves or declines V1.2. If approved, Co can continue Core-side implementation planning within the approved boundary; if declined, the architecture must be revised before implementation.


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
