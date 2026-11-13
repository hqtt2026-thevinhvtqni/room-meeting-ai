# SỔ QUYẾT ĐỊNH WORK 32 / WORK 32 DECISION LOG
- **STT / Document ID:** DOC-006
- **Priority:** P0
- **Read order:** 6
- **Depends on:** DOC-001
- **Status:** ACTIVE — CANONICAL
- **Version / Updated:** 1.3 / 2026-11-04

This register records decisions already evidenced in Work 32 records; it does not create new architecture approval.

| Decision ID | Decision / recorded constraint | Authority / evidence | Status |
|---|---|---|---|
| D32-001 | CI-first, Python 3.12 hosted runner, least privilege; no Docker requirement | W32-DECISION-20261103-01 in legacy BIEN_BAN.md | RECORDED |
| D32-002 | Retain divergent legacy branch; create clean feature branch from verified main baseline; no blind merge/rebase/cherry-pick | W32-DECISION-20261103-02 in legacy BIEN_BAN.md | RECORDED |
| D32-003 | CI activation and implementation limited to dedicated feature branch; no main merge, secrets mutation or production deploy | W32-DECISION-20261104-04 in legacy BIEN_BAN.md | RECORDED |
| D32-004 | Core public MCP V1 inventory is exactly four tools; lifecycle join/start are Core HTTP operations, not MCP public tools | W32-ADR-002-MCP-PUBLIC-CONTRACT.md | RECORDED |
| D32-005 | Core product Auto E2E and immutable artifact E2E are separate from Dashboard browser integration; mock UI is not product integration proof | Evidence 005/008/009 and W32-REQ-001 | RECORDED |
| D32-006 | Dashboard–Bridge–Workspace–Core implementation remains held until canonical Workspace source/runtime, persistence, authentication/identity and Bridge/Application Service contract are evidenced; no invented adapter/API | W32-REQ-001 and W32-ADR-003-XU-CONTINUATION-DECISION.md | DECIDED — TRACK B BLOCKED / NOT APPROVED |
| D32-007 | CI hardening Track A authorized on work/32-ci-cd-python-ci-v2; exact-SHA run required; coverage remains report-only and strict mode is not authorized | Xu W32-ADR-003; W32-EVIDENCE-011/012 | APPROVED — EXECUTED ON SHA 2a406dabed6fc2ef7c19aa28c2469cf45ccc45bf |
| D32-008 | Pin CI dependency constraints only from observed identical unit/E2E pip-freeze reports; apply same constraints to unit, E2E and immutable artifact jobs; keep coverage report-only | W32-EVIDENCE-013; Xu ADR-003 Track A | EXECUTED — EXACT-SHA RUN #3 PASS ON c7dbe1ade37db4c787099a54560ee79868b8a380 |
| D32-009 | Promote only the isolated deterministic meeting lifecycle suite into UNIT_TESTS after source inspection and exact-SHA verification; keep four environment/design-dependent suites report-only; do not enable strict coverage | W32-EVIDENCE-014; Xu ADR-003 Track A | EXECUTED — RUN #4 PASS ON 3cc8e6e945528c4acda631e9dd3e2f4e50bc983f |

No decision in this log authorizes main merge, production deployment, secrets changes or release. Corrections are added as new rows; historical decisions are not rewritten.


## D32-010 — Adopt Work 70 DOC-057 as mandatory full-read Work Entry Gate
- **Date:** 2026-11-09
- **Authority:** Vinh — Product Owner; Xu — Lifecycle Orchestrator / policy owner within delegated scope
- **Decision:** Work32 adopts Work70 DOC-057 as mandatory P0 Work Entry Gate. DOC-108 is the W32-specific implementation. Each AI/person must complete its own G0–G5 entry record for every assignment, read every canonical controlled document in DOC-055 (P0–P3), the complete DOC-035 journal, DOC-034 minutes, DOC-006 decisions, shared Work70 standards and unique legacy sources identified by the register. Summaries and recent-tail-only reading do not satisfy the gate.
- **Anti-repeat rule:** Every assignment must state completed work with evidence, remaining work, failed/superseded work and the exact next action. DONE/PASS work is not repeated unless a new condition or explicit retest justifies it.
- **Execution boundary:** No product-changing action until the participant's own G0–G5 entry is PASS. Read-only discovery and gate remediation remain allowed.
- **Enforcement qualification:** This is an adopted policy and required operating procedure. Technical MCP/GitHub write enforcement is NOT VERIFIED; do not claim that the tools already block noncompliant writes.
- **Evidence:** DOC-108; W32-LOG-20261109-XU-05.


## D32-011 — F1 repeated-start remediation and Browser Adapter health contract
- **Date-Time:** 2026-11-10 10:04 Asia/Ho_Chi_Minh
- **Authority:** Xu / AI-01 under Vinh's delegated technical decision authority; Product Owner retains final acceptance/release authority.
- **Scope:** W32-ASG-F1-001 / PR #49 / exact baseline SHA 06ac86825febfc83032b58adc19aeb32f706725a.
- **Decision status:** ARCHITECTURE DECIDED; SOURCE WRITE AUTHORIZATION NOT GRANTED.
- **Finding:** Live exact-head source confirms `Adapter.start()` assigns local `executable` only inside `if self.browser is None`, then references it after the branch. When Browser process is retained but BrowserContext/Page is closed, the next start can raise `UnboundLocalError`. Current `/health.browser_started` reports page/context presence and therefore conflates browser-process liveness with context readiness.
- **Decision A — F1 correction:** Resolve `ROOMHOP_BROWSER_EXECUTABLE` before the `if self.browser is None` branch on every `start()` invocation, so the value is always defined in both fresh-launch and retained-browser paths. Preserve the existing launch behavior and do not broaden the patch into unrelated lifecycle/security changes.
- **Decision B — health compatibility:** Add explicit `browser_process_alive` and `context_ready` fields. Retain `browser_started` as a deprecated compatibility alias for the existing page/context-ready meaning (`context_ready`), not browser-process liveness. This avoids silently changing the meaning of an existing field. Document the alias and add assertions for both states.
- **Decision C — regression evidence:** The existing Sandbox proposal `05_BUILD/test_f1_repeated_start_contract.py` is NOT an acceptance test: its Playwright mock does not model `sync_playwright().start()`, it incorrectly requires a non-null explicit executable path, and its second test does not execute two actual workflows. Do not copy it unchanged. Ka must implement the regression within the three DOC-044 in-scope paths: (1) direct `start → _close_context → start`; (2) two actual sequential workflow calls on one Adapter/browser process with fresh context/page identity; (3) health state semantics. Use the exact production API/mocking behavior and do not assert that Playwright-managed mode must have an explicit executable path.
- **Independent review:** Cla's `CLA_F1_REVIEW_CANDIDATE_20261110` is review evidence only, not authorized source. Its Linux unit result (4/4 candidate tests and 41/41 existing contract tests) does not establish Chromium, Windows, full workflow or exact-SHA acceptance. Qw must independently verify the corrected regression and resulting exact SHA; Cla must re-review the exact new SHA.
- **Baseline:** PR #49 remains OPEN / DRAFT / NOT MERGED; base main; head branch `work/32-main-integration-20261109`; head SHA `06ac86825febfc83032b58adc19aeb32f706725a`. No GitHub mutation.
- **Permission:** No source/test/CI/runner/PC/branch/PR/main mutation is authorized by this architecture decision. DOC-044 remains DRAFT — BLOCKED until each participant's own G0–G5 evidence is complete, Qw identity/capability and independent QE route are attributable, Xu issues READY, and Ka ACKs after readback.
- **Not in this decision:** No authorization for WORK09 process termination, static PID/EXE/Owner Repository Variables, workflow shell changes, runner configuration changes, CI dispatch, merge, staging, production or release.

## D32-012 — Áp dụng chuẩn Work 70: tách chuẩn bị, quyền thực thi và nghiệm thu
- Ngày: 2026-11-10; chủ trì: Xu / AI-01; thẩm quyền cuối cùng: Vinh.
- Phạm vi: W32-ASG-F1-001 / F1 repeated-start.
- Quyết định: Áp dụng DOC-042/DOC-044/DOC-057 addenda của Work 70. Theo dõi độc lập PREPARATION, EXECUTION AUTHORIZATION và ACCEPTANCE; không dùng thiếu QE/acceptance evidence để chặn các hoạt động chuẩn bị hợp lệ; không dùng PREPARATION_READY để suy ra quyền sửa source/test.
- Trạng thái hiện tại: Ka = PREPARATION IN PROGRESS (G0 PASS; G1–G3 PARTIAL theo W32-LOG-20261110-145; G4/G5 không được suy ra PASS). Qw = QE PREPARATION REPORTED; identity/runtime và độc lập QE chưa xác minh. EXECUTION AUTHORIZATION = NOT GRANTED. ACCEPTANCE = NOT READY.
- Execution blockers: Ka hoàn tất inventory đọc còn thiếu; Xu xác minh identity/capability và source baseline theo assignment; phải có cách enforce quyền ghi/chạy đúng ba path, đúng nhánh/SHA và môi trường. Tool list MCP 8030 hiện chỉ chứng minh có thao tác Sandbox tổng quát; chưa tìm thấy grant/permission tool có thể cưỡng chế giới hạn path/action. Do đó không cấp source/test write bằng chỉ dẫn văn bản đơn thuần.
- Acceptance blockers (không chặn preparation): Qw identity/runtime và independent QE route/provenance; Qw độc lập retest sau khi có SHA mới; Cla re-review exact SHA; các acceptance criteria khác của DOC-044.
- Quyền hiện hành: Ka tiếp tục read-only full-read reconciliation và participant evidence inventory. Qw chuẩn bị QE test strategy/checklist và bổ sung evidence identity/runtime/independence; không sửa test source, không tự nghiệm thu. Xu điều phối, kiểm tra và thiết kế cơ chế enforce quyền. Không có source/test/CI/runner/PC/PR/main/merge/release authorization.
- Exit: Khi execution-critical prerequisites và tool-level scoped enforcement được chứng minh, Xu phát hành execution authorization riêng và Ka ACK. QE/acceptance được mở ở giai đoạn tương ứng, không gộp vào quyền implementation.

## D32-012 clarification — Full G0–G5 execution guard
- Work70 DOC-057 remains controlling: Ka must achieve participant-specific G0–G5 PASS before protected source/test writes or execution. G0–G3 completion alone is not sufficient.
- Qw future QE identity/independence is an acceptance prerequisite unless the assignment risk or a specific G0–G5 criterion requires it before implementation. It does not stop Ka from continuing permitted preparation.
- The current Ka G1–G3 PARTIAL status and missing tool-level scoped enforcement mean EXECUTION AUTHORIZATION remains NOT GRANTED. This clarification supersedes any shorter wording in D32-012 that could imply a subset of gates is enough.

 
## D32-013 — Xu quyết định cơ cấu sở hữu Core và đường triển khai Authorization Gateway
- **Ngày:** 2026-11-10
- **Chủ trì / Architecture Decision Owner:** Xu / AI-01
- **Thẩm quyền cuối cùng:** Vinh
- **Căn cứ ủy quyền:** Vinh giao Xu toàn quyền quyết định cấu trúc trong Work32; không chuyển giao quyền tối cao của Vinh đối với chính sách bảo mật, protected actions và phát hành.
- **Phạm vi:** Work32 F1 và cấu trúc Core chịu trách nhiệm cho Work-scoped Authorization Gateway; không thay đổi kiến trúc ngoài phạm vi cần thiết.

### 1. Quyết định cơ cấu
1. **Xu / AI-01 — Work Architecture & Decision Owner:** chịu trách nhiệm cấu trúc tổng thể, ranh giới thành phần, quyết định kiến trúc, phân công, điều phối liên-agent, gate review và quyết định có/không cấp execution authorization. Xu không tự xác nhận bằng chứng do mình tạo là independent QE.
2. **Cla / AI-03 — Core Technical Owner (được Xu chỉ định cho phạm vi W32; chờ Cla ACK và xác minh identity/runtime):** chịu trách nhiệm truy vết kỹ thuật Core hiện hữu; xác định service owner/runtime entrypoint, trusted authentication, policy enforcement point, assignment/gate source, persistence/transaction và audit boundary; đề xuất vị trí tích hợp nhỏ nhất có thể cưỡng chế quyền. Cla là technical owner của việc khảo sát và thiết kế kỹ thuật, không được tự phê duyệt execution hoặc tự nghiệm thu.
3. **Vi — Implementation Owner (chỉ khi được giao assignment riêng):** chịu trách nhiệm triển khai source sau khi có kiến trúc được Xu quyết định, G0–G5 của participant PASS và execution grant riêng. Không có quyền sửa source/test ở thời điểm quyết định này.
4. **Ka / AI-02 — CSA / Architecture Reviewer & Work Entry participant:** rà soát kiến trúc, hoàn thiện DOC-116 và bằng chứng gate; không tự phê duyệt hoặc tự cấp quyền.
5. **Qw / AI-05 — Independent QE Owner:** xây dựng và thực hiện kiểm thử độc lập trên đường enforcement thực khi có grant/assignment phù hợp; không tự nghiệm thu kết quả của chính implementer.
6. **An — Test Support:** hỗ trợ kiểm thử theo assignment, không thay thế Qw independent QE.
7. **Vinh — Final Authority:** giữ quyền cuối cùng đối với chính sách bảo mật, reserved actions, thay đổi phạm vi và phát hành.

### 2. Cấu trúc thành phần mục tiêu
- **Core Domain / Work Authority:** một nguồn sự thật cho Work, WP, Assignment, participant, ACK, gate snapshot và trạng thái Work; không tạo parallel Work store.
- **Identity & Trust Adapter:** ánh xạ danh tính runtime đã xác thực sang AI/participant identity; không tin identity do request tự khai.
- **Authorization Policy Engine:** đánh giá Work + assignment + ACK + gate + canonical resource + action + source revision + environment + expiry/revocation.
- **Authorization Enforcement Gateway:** middleware/server-side boundary duy nhất cho protected WRITE/EXECUTE; deny-by-default; không dựa vào prompt hoặc hướng dẫn văn bản.
- **Commit-time Guard:** tái xác minh policy, gate, source SHA/blob, assignment và revocation ngay trước khi ghi/chạy; xử lý race/conflict.
- **Evidence & Audit Ledger:** lưu decision ID, principal, Work/assignment, path/action, source SHA, environment, policy/gate version, command, result, timestamp và recovery reason; audit store unavailable thì protected action DENY.
- **Adapter/Tool Boundary:** Sandbox generic read/write/append/delete không được coi là authorization boundary. Protected path phải đi qua gateway hoặc bị deny. READ-only path vẫn hoạt động theo quyền đọc hiện có.
- **QE Boundary:** positive/negative tests phải đi qua real enforcement route; mock/unit-only chỉ là evidence mức unit, không chứng minh runtime enforcement.

### 3. Luồng thực thi chuẩn
REQUEST → TRUSTED IDENTITY → WORK/ASSIGNMENT/ACK/GATE RESOLUTION → EXACT RESOURCE/ACTION/SHA/ENVIRONMENT POLICY → ALLOW/DENY → COMMIT-TIME REVALIDATION → EXECUTION/WRITE → DURABLE AUDIT → INDEPENDENT QE.
Mọi bước thiếu nguồn sự thật, identity, policy, audit hoặc revalidation phải DENY. WRITE không bao hàm EXECUTE; CI/runner, protected branch, merge, deploy và release là các quyền riêng biệt.

### 4. Phân công kỹ thuật kế tiếp
- Cla: nhận/ACK vai trò Core Technical Owner; lập source/runtime trace read-only, xác định owner thực tế của Core service và báo cáo chính xác route, middleware, policy, store, audit, bypasses và bằng chứng. Nếu Cla không có runtime/source access, phải báo BLOCKED theo format problem/evidence/bottleneck/options/missing condition; không suy đoán.
- Xu: quyết định kiến trúc đích và điểm tích hợp sau khi nhận trace; mọi thay đổi phạm vi/nguồn dữ liệu phải có decision record.
- Ka: tiếp tục remediation G1/G3; không tham gia source/test mutation.
- Vi: chưa triển khai; chờ assignment và execution authorization riêng.
- Qw: chuẩn bị test matrix positive/negative; chỉ chạy khi được cấp quyền test riêng và có môi trường thực.
- Xu sẽ cập nhật DOC-071/DOC-072 hoặc tài liệu canonical tương ứng theo kết quả trace, tránh tạo tài liệu song song không cần thiết.

### 5. Giới hạn quyền và trạng thái
- Quyết định này **chỉ phê duyệt cơ cấu tổ chức và kiến trúc mục tiêu**, không phải phê duyệt implementation.
- Cla ACK vai trò chưa được xác nhận; cho tới khi ACK và identity/runtime được xác minh, Cla status = DESIGNATED / ACK PENDING.
- G0 PARTIAL; G1 BLOCKED; G2 PASS LIMITED (registration/storage only; overall partial); G3 PARTIAL; G4/G5 BLOCKED.
- DOC-117 vẫn là target contract; chưa có bằng chứng Authorization Gateway đã implement/enforce.
- Không source/test/config write, không chạy test/CI, không PC/runner, không branch/PR/main mutation, merge, deploy hoặc release được cấp bởi D32-013.
- Work32 tiếp tục ACTIVE — NOT RELEASED.

**Kết luận:** Xu nắm quyền quyết định cấu trúc và điều phối kiến trúc Work32 theo ủy quyền của Vinh; Cla được chỉ định làm Core Technical Owner cho khảo sát/truy vết kỹ thuật, pending ACK. Implementation và protected execution tiếp tục bị khóa cho tới khi các gate và authorization riêng được hoàn tất.


---

## W32-DECISION-20261114-08 — DOC-125 RESOURCE ISOLATION DESIGN BASELINE

- **Decision owner:** Xu / AI-01, under Vinh's retained final authority.
- **Reviewers:** Ka / AI-02 (CSA) and Cla / AI-03 (CTO), both READ-ONLY.
- **Date:** 2026-11-14; no exact decision time is asserted.
- **Inputs:** DOC-125; Ka CSA review; Cla CTO review; Xu exact-branch source trace.
- **Decision status:** DESIGN DIRECTION APPROVED WITH CONDITIONS; PRODUCT IMPLEMENTATION NOT AUTHORIZED; PROTECTED EXECUTION DENIED.

### 1. Reconciled review outcome

- Ka: REJECT current resource-isolation implementation; APPROVE WITH CONDITIONS the Job Object direction.
- Cla: IMPLEMENTABLE WITH CONDITIONS; no independent GitHub source read in Cla's review session, so its source observations are secondary.
- Xu independently fetched the exact source blobs on branch work/32-main-integration-remediation-20261113 and confirmed that the protected GrantedExecutionHost path calls run_bounded(), whose Windows Popen uses CREATE_NEW_PROCESS_GROUP (not CREATE_SUSPENDED) and taskkill only for cleanup. The separate generic ExecutionHost path in host.py also uses ordinary Popen. Neither path currently establishes a Job Object quota boundary before user code runs.
- Both reviews agree on the non-negotiable barrier: untrusted workload code must not execute until OS containment is configured and verified; every failure must deny execution with no ordinary-Popen fallback.

### 2. Approved design direction

1. **Authority:** Core remains the sole grant and policy authority. Caller-supplied quota numbers are never trusted.
2. **Policy binding:** introduce a versioned Core-authorized resource profile identifier and policy digest. The Host applies the stricter of the Core-authorized profile and a locally configured Host hard ceiling. Missing, malformed, unknown or mismatched policy => DENY. Exact schema and values remain a design task; no quota values are guessed.
3. **Windows enforcement:** use a per-run Windows Job Object backend for job memory, CPU hard-cap, active process count and kill-on-job-close. Use a narrow ResourceBackend interface; unsupported backend denies protected execution.
4. **Launch barrier:** configure and query back all limits; create the process suspended; assign it to the Job (or use a creation-time Job-list mechanism if the spike proves it); verify membership and limits; perform the final online Core validation; only then resume. No user code may execute before that point.
5. **Failure behavior:** any creation/configuration/query/assignment/verification/resume/telemetry failure => terminate what was created, close non-inheritable handles, record BLOCKED and never fall back to ordinary Popen.
6. **Descendants:** no breakaway flags. All descendants must remain in the same Job. If root exits while descendants remain, terminate the Job and do not report PASS. Host cancellation and host-close must terminate the Job; kill-on-job-close is mandatory and must be verified.
7. **Platform:** protected execution on Linux and unsupported platforms remains DENIED until a separate kernel-enforced backend is designed and tested. No Docker.
8. **Privilege boundary:** Job Object is resource/lifecycle containment, not a full security sandbox. A restricted non-admin workload identity and filesystem/network/credential restrictions are separate mandatory design conditions before protected execution can be enabled.
9. **Telemetry:** Run Record must include policy profile/digest, configured and queried limits, Job assignment verification, peak/accounting values where reliable, termination result and evidence references.

### 3. Unresolved design decisions that block implementation

- **D1 — Windows creation mechanism:** prove the preferred creation-time Job-list route on the supported Windows build; compare against CREATE_SUSPENDED + AssignProcessToJobObject. A suspended process orphan must not remain if Host dies before assignment. No fallback if neither method is safe.
- **D2 — Policy schema:** define Core grant binding for resource_profile_id/version/digest and Host hard-ceiling behavior; confirm compatibility with current grant contract.
- **D3 — Cancellation and descendants:** define Host run registry/cancel lifecycle, root-exits-before-child behavior, kill-on-close and deterministic zero-active-process confirmation.
- **D4 — Run Record recovery:** incomplete run after durable run_started remains INDETERMINATE, grant consumed, never PASS. Torn/corrupt journal must fail closed and preserve evidence; do not silently truncate.
- **D5 — Persistence contract:** DOC-123 calls for multi-process lock/SQLite timeout/recovery and append-only Run Record consistency, while the audited Core path currently uses JSONL + OS file lock. Resolve whether SQLite is mandatory before any persistence change; do not silently substitute or migrate stores.
- **D6 — Quota values and measurement:** establish workload baselines on supported Windows and derive limits with documented safety margin. Do not guess memory/CPU/process limits.

### 4. Authorized next work and boundaries

- Xu may prepare a bounded, isolated Windows API proof-of-concept/test specification to resolve D1 and D3; it must not be integrated into the product or run protected Workload commands.
- No product source/test changes, Core schema changes, branch/PR mutation, PC runner dispatch, service/port/configuration changes, protected execution, main integration, deployment or release are authorized by this decision.
- After D1–D6 are resolved, Xu must issue a separate implementation authorization with exact files, branch, test plan and rollback. Ka performs security review; Cla confirms implementation feasibility; independent QE verifies the real enforcement route.
- Vinh retains final acceptance and release authority.

**Disposition:** DOC-125 DESIGN DIRECTION APPROVED WITH CONDITIONS; IMPLEMENTATION NOT AUTHORIZED; H1 resource isolation BLOCKED; protected execution DENIED; Work32 ACTIVE — NOT ACCEPTED — NOT RELEASED.
