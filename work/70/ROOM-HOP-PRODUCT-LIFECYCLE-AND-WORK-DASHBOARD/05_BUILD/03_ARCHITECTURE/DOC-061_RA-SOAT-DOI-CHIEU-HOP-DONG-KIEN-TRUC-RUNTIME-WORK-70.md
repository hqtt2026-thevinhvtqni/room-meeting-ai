# DOC-061 — RÀ SOÁT ĐỐI CHIẾU HỢP ĐỒNG KIẾN TRÚC RUNTIME WORK 70

- **STT / Document ID:** DOC-061
- **Priority:** P1
- **Read order:** 61
- **Depends on:** DOC-004; DOC-005; DOC-010; DOC-033; DOC-049; DOC-054; DOC-055; DOC-060
- **Status:** DRAFT — SOURCE RECONCILIATION COMPLETE / CONTRACT APPROVAL PENDING / IMPLEMENTATION NOT VERIFIED
- **Version / Updated:** 1.0 / 2026-11-01
- **Owner:** Ka / AI-02
- **Role:** CSA / Architecture & Independent Review
- **Authority:** Xu coordinates integration; Vinh retains product acceptance and release authority.

## 1. Mục đích và phạm vi

Tài liệu này đối chiếu WORK70_KA_ARCHITECTURE_CONTRACT_V1.md với state machine, lifecycle gate matrix, Dashboard/Core read contract và mã Core hiện hành. Đây là phụ lục kỹ thuật để khóa các sự thật đã xác minh trước khi Xu review hợp đồng v1.

Không phê duyệt API route, database schema, permission, provider, gate namespace hoặc implementation. Không sửa Core, Lifecycle Engine hay Dashboard. Không thay thế DOC-004/DOC-005/DOC-010.

## 2. Kết quả đối chiếu nguồn chuẩn

| Nguồn | Kết quả đối chiếu | Hiệu lực |
|---|---|---|
| DOC-004 v1.2 | Lifecycle gate G0–G9; PASS chỉ do authority đánh giá trên evidence | ACTIVE |
| DOC-005 v1.2 | Work, Phase, Gate và Work Package có state machine riêng | ACTIVE |
| DOC-010 v1.0 | Dashboard read-only; Core endpoint Work chỉ là đề xuất; local snapshot không phải Core live | ACTIVE |
| DOC-049 v1.1 | Evidence-first; implementation phải ở source repo/branch đã khai báo; không tự approve G5 | ACTIVE |
| DOC-054 v1.0 | Ka contract; Co Engine; Vi adapter/Dashboard; Qw independent QE; Xu tích hợp | ACTIVE / ASSIGNMENT READY; dispatch acknowledgement chưa được xác minh |
| DOC-060 | Gate namespace/identifier separation | PROPOSAL ONLY / NOT APPROVED |
| Core main | Router `room_hop_mcp/adapter/http_server.py` đăng ký `/identities` và các Meeting routes; không có Work-scoped route trong router được kiểm tra | READ-ONLY SOURCE OBSERVATION |
| GitHub branch `work/70/05-build` | So với main: branch ahead 34, behind 370, merge base `fc6a19888765d174aea9aea839620338ac9f71e8`; compare trả về 14 file Work 70 dạng tài liệu được thêm, không có bằng chứng code Engine/Core/Dashboard tích hợp | DIVERGED / DO NOT MERGE BLINDLY |
| Sandbox 05_BUILD | `04_CODE` chỉ có `.gitkeep`; `05_TEST` hiện có kế hoạch nghiệm thu storage/export với trạng thái NOT EXECUTED | IMPLEMENTATION NOT VERIFIED |

## 3. State contract — bắt buộc tách biệt

Không dùng một trường `status` chung để đại diện tất cả các lớp.

### 3.1 Work lifecycle state — theo DOC-005

- Chuỗi chuẩn: `NOT_STARTED → ACTIVE → (BLOCKED ↔ ACTIVE) → ACCEPTED → RELEASED → OPERATING → CLOSED`.
- `CANCELLED` cần owner có thẩm quyền và reason.
- Reopen Work đã CLOSED phải có transition được audit và reason.

### 3.2 Phase state — theo DOC-005

`NOT_STARTED | PLANNED | ACTIVE | BLOCKED | DONE | CANCELLED`.

Chỉ một phase hiện tại. Phase chỉ DONE khi exit gate tương ứng PASS. Phase sau không được current khi predecessor gate chưa giải quyết.

### 3.3 Lifecycle gate state — theo DOC-004/DOC-005

`NOT_READY | PENDING | PASS | FAIL | WAIVED`.

WAIVED không tương đương PASS; phải có approver, rationale, scope và expiry/review date. Thiếu, stale, mâu thuẫn hoặc không xác minh được evidence không thể PASS.

### 3.4 Work Package state — theo DOC-005

`DRAFT → READY → IN_PROGRESS → IN_REVIEW → DONE`.

Bất kỳ trạng thái active nào có thể chuyển BLOCKED. Review bị từ chối quay lại IN_PROGRESS kèm findings. CANCELLED cần owner decision và reason.

### 3.5 Gate namespace

DOC-004 dùng Lifecycle Gate G0–G9. DOC-054 dùng Integration Gate G0–G4. DOC-060 đề xuất tách namespace nhưng chưa được Vinh phê duyệt. Vì vậy không được tự đặt LC/WE/INT hoặc diễn giải các gate này thành cùng một hệ. Mọi API/schema triển khai phải chờ Xu chốt cách tham chiếu mà không làm thay đổi hiệu lực DOC-004/DOC-054.

## 4. Runtime authority contract

1. **Lifecycle Engine:** domain evaluator thuần; kiểm tra transition legality, predecessor gate, dependency và evidence. Không tự cấp quyền caller, không tự lưu authoritative Work state, không bypass Core.
2. **Core:** boundary có thẩm quyền cho identity, authorization, Work state, version, persistence, decision và canonical evidence metadata. Core xác thực actor từ principal đáng tin cậy; không nhận actor role do client tự khai.
3. **Dashboard:** read-only projection từ Core. Không ghi DB/Sandbox, không gọi Engine trực tiếp, không approve gate, không trigger release.
4. **Evidence storage:** chỉ được coi là canonical khi Core/approved backend trả artifact identity + metadata và read-after-write integrity được xác minh. Sandbox/local browser cache không phải production persistence.
5. **Events/audit:** append-only provenance cho hành động đã commit; không trở thành nguồn authority độc lập.
6. **AI adapter:** provider-neutral adapter; thay adapter không được làm thay đổi domain state machine hoặc Core authority.

## 5. Logical command contract — chưa phải API route được duyệt

### Request fields đề xuất

- `work_id`: stable Work identifier.
- `command_id`: idempotency key.
- `expected_version`: optimistic concurrency precondition.
- `target_state` hoặc command type: chỉ giá trị hợp lệ theo DOC-005; chưa khóa tên field/API.
- `reason`: bắt buộc ở transition mà policy yêu cầu.
- `evidence_refs`: immutable references đáp ứng guard tương ứng.
- `actor`: lấy từ authenticated principal phía server; không tin actor/role trong body.

### Accepted result tối thiểu

`command_id, work_id, outcome, previous_state, current_state, new_version, transition_id, timestamp, audit_ref`.

### Rejected result tối thiểu

`command_id, work_id, outcome=rejected, stable_reason_code, current_state/version (nếu an toàn), no_mutation=true, recovery_guidance`.

Reason code hiện chỉ là candidate mapping: `UNAUTHENTICATED`, `FORBIDDEN`, `WORK_NOT_FOUND`, `INVALID_TRANSITION`, `GUARD_NOT_SATISFIED`, `EVIDENCE_REQUIRED`, `VERSION_CONFLICT`, `IDEMPOTENCY_CONFLICT`, `VALIDATION_ERROR`. Chưa được coi là literal API hiện hành.

### Invariants bắt buộc

- Authorization và toàn bộ guard phải qua trước mutation.
- Rejected command không thay đổi authoritative state/version.
- Cùng command_id + cùng payload chỉ có tối đa một effect; retry trả outcome đã ghi.
- Cùng command_id + payload khác phải reject.
- Hai command cạnh tranh cùng expected_version không thể cùng commit.
- State và audit phải atomic hoặc có consistency/recovery protocol được mô tả và test.
- Event delivery mặc định at-least-once cho đến khi có bằng chứng khác; consumer deduplicate theo event/transition ID.
- Stale/missing data phải hiện UNKNOWN/STALE/NOT_VERIFIED, không suy diễn PASS.

## 6. Core capability boundary — hiện trạng thực tế

Đã fetch và kiểm tra mã trên GitHub main `bb259c5186f31073691bc92bfa2f52430f19451b`:

- `room_hop_mcp/adapter/http_server.py`: có `/identities`, `/meetings`, `/meetings/{id}`, transcript, paste và Meeting lifecycle routes. Không thấy Work registry, Work lifecycle, Work package, Work evidence hoặc Work export routes trong router này.
- `core/meeting_manager.py` và `core/meeting_service.py`: là Meeting-centric; không được tái sử dụng Meeting artifact operation như generic Work evidence API.
- Router được kiểm tra chưa chứng minh được Work-scoped AuthN/AuthZ, version/transaction contract, idempotency, audit/outbox, storage registry hay export service. Không kết luận chúng không tồn tại ở mọi nơi; các capability này remain NOT VERIFIED cho đến khi owner Core xác định đúng service/route và test.
- Không tự thêm `/api/v1/works/*` vào Core trong phạm vi WP70-KA. Các endpoint ở DOC-010 là proposal, không phải route đã tồn tại.

## 7. Dashboard contract

Dashboard chỉ đọc projection được Core authorize; tối thiểu phải tách:
- `work_status` — Work lifecycle;
- `current_phase` + phase status;
- lifecycle gate status;
- integration/build verification status;
- WP status;
- source mode: `core_live | core_cached | local_snapshot | sample`;
- `generated_at/as_of`, revision/version và freshness.

Không được gộp phase DONE với gate PASS, WP DONE với Work ACCEPTED, hay local snapshot với Core live. Với HTTP/network/auth failure: UNKNOWN hoặc STALE theo DOC-010; không dùng optimistic state.

## 8. Quyết định kiến trúc đang khóa / chưa khóa

### Đã khóa bởi nguồn chuẩn
- Core là authority; Dashboard read-only.
- Work/Phase/Gate/WP là các state domain riêng.
- Không dùng Meeting save_artifact làm Work evidence store.
- Không tạo nguồn dữ liệu thứ hai.
- Không tuyên bố Core live, persistent storage, export hoặc release nếu chưa có runtime evidence.

### Chưa khóa — cần Xu đối chiếu với Core owner
- API route, DTO/schema version và error envelope.
- Auth principal/permission scope thực tế.
- Aggregate version, concurrency và transaction boundary.
- Idempotency store/retention.
- Audit/event schema, outbox và replay guarantee.
- Evidence registry, storage provider, retention và download authorization.
- Snapshot consistency, freshness threshold, pagination/filter.
- Gate namespace tương thích DOC-060 proposal và DOC-054.

## 9. Kiểm thử hợp đồng độc lập tối thiểu

Mỗi test phải có fixture, independent oracle, request/response, authoritative before/after state, command và raw evidence.

| ID | Ca kiểm thử | Kết quả bắt buộc |
|---|---|---|
| K70-01 | Transition hợp lệ, đúng actor/evidence/version | Một commit, một audit/transition |
| K70-02 | Illegal edge | Reject; state/version không đổi |
| K70-03 | Thiếu predecessor gate/evidence | Reject; no mutation |
| K70-04 | Actor không đủ quyền | Deny; no mutation; không lộ dữ liệu |
| K70-05 | Replay cùng command ID/payload | Cùng outcome; một effect |
| K70-06 | Reuse command ID với payload khác | Idempotency conflict |
| K70-07 | Concurrent command cùng expected_version | Tối đa một commit |
| K70-08 | Persistence failure | Không có partial state/audit |
| K70-09 | Event transport outage | Event durable/recoverable hoặc contract lỗi rõ |
| K70-10 | Dashboard thử write/bypass | Không có write path; server deny |
| K70-11 | Projection stale | Version/as-of/freshness hiển thị |
| K70-12 | Missing dependency/evidence | UNKNOWN/NOT_VERIFIED; không PASS |

Qw phải sở hữu oracle và báo cáo độc lập; implementer không tự xác nhận PASS.

## 10. Trạng thái WP70-KA và handoff

- Source reconciliation: **DONE — READ-ONLY REVIEW**.
- Architecture contract v1: **DRAFT — NOT APPROVED**.
- Core Work API/auth contract: **BLOCKED / NOT VERIFIED**.
- Branch integration: **BLOCKED — DIVERGED (34 ahead / 370 behind)**; không merge/rebase tự động.
- Runtime implementation, tests và E2E: **NOT RUN / NOT VERIFIED**.
- Release: **NOT RELEASED**.

### Handoff cho Xu
1. Review DOC-061 và quyết định contract fields/namespace; không thay đổi DOC-004/DOC-005 nếu chưa có quyết định có thẩm quyền.
2. Chỉ định/nhận xác nhận từ Core owner về AuthN/AuthZ, transaction/version, idempotency và event boundary.
3. Điều phối Co/Vi theo DOC-054; xác minh ACK riêng từng AI trước khi ghi nhận bắt đầu.
4. Chuyển bộ test K70-01..12 cho Qw xây dựng độc lập.
5. Không tích hợp branch Work 70 vào main cho đến khi có kế hoạch đối chiếu 370 commit behind, xác nhận nguồn thay đổi và kiểm thử hồi quy.

### Chữ ký

- Người thực hiện: **Ka / AI-02**
- Chức danh: **CSA / Architecture & Independent Review**
- Ngày: **2026-11-01**
- Kết luận: **SOURCE RECONCILIATION COMPLETE / CONTRACT APPROVAL PENDING / NOT RELEASED**


---

## 11. Addendum — canonical WP baseline and BUILD authorization reconciliation (2026-11-01)

This addendum supersedes any interpretation of Sections 2, 8 or 10 that could imply 05_BUILD implementation is already authorized.

### 11.1 Higher-authority planning sources

Read-only GitHub main inspection of DOC-052 v1.4, DOC-053 v0.1, DOC-010 and DOC-004/005 establishes:

- DOC-052: Manifest current phase remains `03_ARCHITECT`; G3/G4/G5 are NOT PASS; G4 PLAN exit is NOT PASS. DOC-052 explicitly says DOC-011 remains the Work-level planning authority.
- DOC-053: the six-row structured WP register at `04_PLAN/WORK_PACKAGE_REGISTER.json` is `DRAFT_NOT_APPROVED`; all proposed WP statuses remain DRAFT. It does not open G4 or authorize READY/ACTIVE.
- DOC-036 (as referenced by DOC-052/053): the branch `05_BUILD/00_ROOT/BUILD_REGISTER.json` and schema are legacy candidates; canonical target/version is NOT ESTABLISHED.
- DOC-010: Dashboard endpoints are proposals, not verified Core routes; source mode must distinguish core_live, core_cached, local_snapshot and sample.
- DOC-004: G4 is the PLAN→BUILD exit gate; it requires approved roadmap, WPs, owners, dependencies, acceptance criteria and test strategy.

### 11.2 Corrected execution interpretation

- DOC-054 being `ACTIVE / ASSIGNMENT READY` is an assignment specification, not evidence that G4 passed, that each proposed owner accepted, or that any WP is READY.
- DOC-061 is a technical reconciliation draft, not an approved architecture baseline and not BUILD authorization.
- No WP may be represented as READY/IN_PROGRESS under the proposed baseline until Product Owner approves DOC-053/baseline and G4 is validly evaluated.
- Permitted now: source audit, architecture reconciliation, isolated non-authoritative prototypes expressly labelled DRAFT/NOT FOR INTEGRATION, and test design. Do not merge prototypes, migrate the branch register, or change authoritative Work status.
- Co/Vi/Qw dispatch remains unconfirmed until each agent's own ACK/artefact is evidenced.

### 11.3 Required unblock sequence

1. Xu reconciles DOC-011 summaries against DOC-053 six records, requirements, dependencies, priority, owner/reviewer confirmations and 05_BUILD mapping; no fabricated requirement refs or estimates.
2. Vinh approves/revises the Work-level WP baseline and scope/priority decisions.
3. Architecture authority reviews DOC-061 + the original runtime contract and records approved interface decisions; unresolved Core capabilities remain explicit.
4. Xu evaluates G4 against DOC-004 with evidence and authorized decision; no automatic PASS from document presence.
5. Only after G4 PASS and WP DoR may the relevant WP enter READY/ACTIVE and code integration proceed.
6. Qw independently validates the transition and subsequent implementation; G5/G6 remain separate.

### 11.4 Status correction

- Source reconciliation: DONE (read-only).
- DOC-061 technical contract: DRAFT / REVIEW REQUIRED.
- Work-level WP baseline: DRAFT_NOT_APPROVED.
- G4 PLAN→BUILD: NOT PASS.
- Build implementation/integration: NOT AUTHORIZED by current evidence.
- Safe preparatory audit/test design: ACTIVE.
- RELEASE: NOT RELEASED.

Prepared and signed: **Ka / AI-02 — CSA / Architecture & Independent Review**  
Date: **2026-11-01**  
Priority: **P0 clarification to DOC-061 (document remains P1)**.


---

## 12. Xu đính chính nguồn và trạng thái — 2026-11-01

Phần 11 của addendum trước có các tham chiếu sai và được đính chính như sau; giữ nguyên phần lịch sử để bảo toàn dấu vết:

1. **DOC-053** theo DOC-055 là `09_OPERATE/PHASE_EXECUTION_PLAYBOOK.md` — Hướng dẫn thực thi giai đoạn Vận hành. DOC-053 không phải Work Package register.
2. Đường dẫn `04_PLAN/WORK_PACKAGE_REGISTER.json` và `04_PLAN/WORK_PACKAGE_REGISTER.md` đã được kiểm tra trực tiếp trong Sandbox ngày 2026-11-01 và trả về `FileNotFoundError`. Không có căn cứ nói DOC-053 chứa một WP register tại các đường dẫn này.
3. **DOC-011 / 04_PLAN/IMPLEMENTATION_ROADMAP.md** là kế hoạch Work-level hiện hành, liệt kê sáu WP từ WP-70-01 đến WP-70-06.
4. **DOC-036 / 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md** phân loại BUILD_REGISTER.json/Markdown và các schema trong 05_BUILD là CANONICAL CANDIDATE; canonical target/version chưa được thiết lập.
5. **DOC-001 Manifest v1.4** hiện ghi current phase pointer là `01_DISCOVER (PLANNED; G0/G1 NOT_READY)`. Tham chiếu trong phần 11 rằng Manifest hiện trỏ `03_ARCHITECT` là không chính xác.
6. BUILD Register JSON có sáu record WP và một số status khác với DOC-011. Các status đó là dữ liệu trong hồ sơ candidate, không được dùng để ghi đè DOC-011 hoặc cấp quyền thực thi.
7. DOC-062 tại `04_PLAN/DOC-062_DE-XUAT-CHUAN-HOA-GOI-CONG-VIEC_WORK-PACKAGE-BASELINE-RECONCILIATION-PROPOSAL.md` là bản đối chiếu/đề xuất mới. DOC-062 vẫn DRAFT, chưa được Vinh phê duyệt.

**Trạng thái đã hiệu chỉnh:** DOC-011 là Work-level plan hiện hành; DOC-062 là đề xuất baseline; DOC-053 là Operate Playbook; Build Register/schema là candidate; Manifest current phase = 01_DISCOVER PLANNED, G0/G1 NOT_READY; G4 NOT READY / NOT PASS; Build implementation chưa được mở; RELEASE NOT RELEASED.

Người đính chính: Xu / AI-01. Đây là đính chính nội dung tham chiếu, không phải sửa quyết định hay tự cấp quyền.


## ADDENDUM 12 — BỘ KIỂM THỬ ĐỘC LẬP CHO BASELINE WP VÀ ĐIỀU KIỆN G4
- **Document ID:** DOC-061 (bổ sung, không tạo DOC-ID mới)
- **Priority:** P1
- **Read order:** 61
- **Date-Time:** 2026-11-01 (+07:00)
- **Author / Title:** Ka / AI-02 — CSA, Architecture & Independent Review
- **Status:** TEST DESIGN ONLY / NOT EXECUTED / NOT AN APPROVAL

### A. Nguồn chuẩn đã đối chiếu
1. DOC-011 v1.3 (GitHub main, blob SHA `1ed01cf7405c4e962c1d250ca82572b2fad5c069`): sáu WP summary; WP-70-04 BLOCKED/NOT VERIFIED; WP-70-05 DESIGN ONLY; WP-70-06 PLANNED; WP baseline draft; không mở G4.
2. DOC-036 v1.0 (branch `work/70/05-build`, blob SHA `a9a14fb845328c3e1273769f502b3486465c3bbd`): mapping branch chỉ là coordination; target/version chưa xác lập; cấm migrate trước phê duyệt.
3. DOC-045 v1.0 (GitHub main, blob SHA `3748b5c6510156ad513dc56d7c23d2148f98a1c5`): 04_PLAN là nơi duy nhất sở hữu WP plan cấp Work; Product Owner duyệt baseline; nếu G2/G3 chưa PASS chỉ được tạo draft/scenario, không phát hành execution baseline.
4. DOC-052 v1.4 (GitHub main, blob SHA `a29b8bcc3d29a39e1657ac14263b777e9245fee8`): G3/G4/G5 chưa PASS; independent QE, Core live integration, browser E2E và Sandbox sync chưa được chứng minh.
5. DOC-060 v1.0-draft: đề xuất tách namespace Lifecycle G0–G9, Work Entry G0–G5 và Integration G0–G4; proposal-only, chưa được Vinh phê duyệt/triển khai. Không dùng namespace mới như luật có hiệu lực và không diễn giải gate trần nếu thiếu tài liệu nguồn.
6. DOC-046 Build Process: BUILD chỉ bắt đầu khi G4 PASS, WP READY, DoR đạt, owner/reviewer và canonical source được xác nhận. Vì thế test thiết kế dưới đây không phải lệnh BUILD.

### B. Ma trận kiểm thử hợp đồng WP — thiết kế, chưa chạy
| Test ID | Điều kiện kiểm tra | Kết quả bắt buộc | Failure classification |
|---|---|---|---|
| K70-WP-01 | Đúng 6 WP IDs WP-70-01..06, duy nhất, không thiếu/trùng | PASS khi tập ID khớp chính xác | FAIL |
| K70-WP-02 | Mỗi WP có objective/outcome, scope/exclusions, deliverables và acceptance criteria | Không có trường bắt buộc rỗng/TBD không có owner/trigger | NOT READY |
| K70-WP-03 | Traceability về DOC-008 requirements, DOC-009 architecture/ADR và acceptance | Mọi deliverable có trace link kiểm chứng được | BLOCKED nếu baseline nguồn chưa approved |
| K70-WP-04 | Owner, implementer, independent reviewer, decision authority | Role rõ; reviewer không tự review output mình; ACK/permission có evidence | BLOCKED |
| K70-WP-05 | Dependency graph | Không cycle; predecessor có exit criteria và owner | FAIL nếu cycle; BLOCKED nếu dependency chưa xác nhận |
| K70-WP-06 | Estimate/capacity | Range, confidence, basis, assumptions; UNKNOWN/TBD có cách lấy dữ liệu | NOT READY |
| K70-WP-07 | DoR/DoD và verification/evidence plan | Mỗi WP có entry/exit, test scope, evidence producer/verifier/location | NOT READY |
| K70-WP-08 | Source ownership/mapping | Canonical repo/path/ref/version/hash xác định; branch 05_BUILD không bị coi là canonical source | BLOCKED |
| K70-WP-09 | State transition guard | DRAFT không thể tự chuyển READY/ACTIVE; cần approved baseline, G4 decision và DoR | FAIL nếu transition vượt gate |
| K70-WP-10 | Gate authority and provenance | Quyết định G4 có authority, timestamp, exact baseline version, scope và evidence | BLOCKED nếu thiếu |
| K70-WP-11 | Gate namespace ambiguity | Mỗi gate reference gắn document/namespace cụ thể; DOC-060 chỉ áp dụng sau phê duyệt | NOT READY / ambiguity |
| K70-WP-12 | Migration safety | Legacy branch originals preserved; no move/delete/overwrite absent approval, backup/hash, QE | FAIL nếu destructive mutation trái quy trình |
| K70-WP-13 | Negative fixtures | Missing owner, self-review, cyclic dependency, missing acceptance, stale source ref, unauthorized READY, unverified route | Từng fixture phải bị reject đúng lý do |
| K70-WP-14 | Independent reproducibility | QE chạy lại cùng commit/version, schema, fixtures; lưu raw output và environment | NOT RUN cho đến khi QE thực thi |

### C. Trình tự mở khóa có kiểm soát
1. Xu chuẩn bị bản reconciliation duy nhất giữa sáu summary của DOC-011 và sáu record DOC-053; ghi từng khác biệt về objective, deliverable, scope, dependencies, acceptance, owner/reviewer, estimate và source mapping. Không tự đổi status.
2. Xu làm rõ các gate tham chiếu đang dùng: phân biệt Lifecycle, Work Entry và Integration Gate bằng nguồn tài liệu; trình DOC-060 cho Vinh quyết định. Trước khi được duyệt, giữ nguyên namespace hiện hành và ghi rõ document context, không sửa hồi tố.
3. Vinh quyết định WP baseline và các trade-off/priority/commitment thuộc Product Owner. Ka chỉ review hợp đồng/kiến trúc, không tự phê duyệt baseline.
4. Xu đánh giá G4 theo DOC-004/DOC-045, chỉ ghi PASS khi đủ criteria và authority decision có evidence. Không suy ra G4 PASS từ DOC-054 assignment hay DOC-061.
5. Chỉ sau G4 PASS: từng WP riêng lẻ phải đạt DoR, owner/reviewer ACK, source mapping và permission; chỉ WP đó mới được chuyển READY/ACTIVE theo state machine.
6. Qw/independent QE thực thi K70-WP-01..14 và lưu raw evidence; implementer không tự chứng nhận độc lập.
7. DOC-036 mapping/migration chỉ được cập nhật sau authorization; bảo toàn nguyên trạng branch originals đến khi QE xác minh hash/readback.

### D. Kết luận trạng thái sau lần rà soát này
- Source reconciliation bổ sung: DONE (read-only).
- WP contract test design: DONE / NOT EXECUTED.
- Gate namespace ambiguity: IDENTIFIED; DOC-060 remains PROPOSAL ONLY.
- WP baseline: DRAFT_NOT_APPROVED.
- G3/G4: NOT PASS theo DOC-052.
- BUILD implementation/integration: NOT AUTHORIZED.
- QE: NOT RUN / PENDING.
- Acceptance/release: NOT GRANTED / NOT RELEASED.

**Boundary:** Addendum này là thiết kế kiểm thử và handoff kỹ thuật, không sửa DOC-011/DOC-053/DOC-060, không di chuyển legacy files, không mở gate và không thay thế quyết định của Vinh/Xu.


---

## Addendum 2026-11-01 — Recheck WEE / Execution Host and current branch baseline

**Classification:** READ-ONLY SOURCE TRACE — NOT IMPLEMENTATION APPROVAL / NOT QE / NOT GATE PASS.

### 1. Current repository baseline

A fresh GitHub compare at this review found:
- `main` HEAD: `21190f8449656ac65a2b5682621e1c4f75a0d6dd`.
- `work/70/05-build`: 34 commits ahead and 379 commits behind `main`.
- Merge base: `fc6a19888765d174aea9aea839620338ac9f71e8`.
- Compare reports 14 files added on the Build branch, all within the Work 70 `05_BUILD` subtree.
- Result remains DIVERGED. No merge, rebase, cherry-pick or force update is authorized by this review.

This supersedes the earlier 34-ahead / 370-behind observation as the latest measured branch relationship; historical journal entries remain unchanged.

### 2. New source discovered on main: `wee/`

Read-only inspection of `wee/controller.py`, `wee/authority.py`, `wee/models.py`, `wee/cli.py`, `wee/readiness.py` and related bridge files found a generic Work E2E execution spine:
- `CanonicalWorkAuthority` resolves a JSON authority binding with Work/repository/branch/workspace/expected HEAD/runtime/browser/test/CI/evidence fields.
- `WorkContext` binds that authority record to an execution ID.
- `EvidenceStore` writes execution-scoped evidence files.
- `LifecycleController` records RESOLVE, BIND, VALIDATE, PREPARE, EXECUTE and TEST stage outcomes.
- `wee/bridge/real_host.py` contains a real subprocess execution adapter and optional process/browser/GitHub/CI adapter slots.

**Important execution limitation found in the current controller:** the default host is `LocalExecutionHost`; `LifecycleController.run()` records EXECUTE PASS after capability discovery, does not invoke the bound test entrypoint, and then returns TEST BLOCKED with `test_execution_not_available_in_sandbox_boundary`. The controller therefore does not currently demonstrate the complete Plan→Build→Test→Review→Accept→Release Work lifecycle. Its own result is BLOCKED at TEST, not PASS.

### 3. Integration-test boundary

`tests/test_work13_wee_integration.py` directly invokes `Work13ExecutionHostAdapter.execute(...)` and asserts a Work 13 process result. It does not call `LifecycleController.run()`; therefore it is evidence for that adapter's direct process execution path, not evidence that the generic controller completes its lifecycle. GitHub code search for `LifecycleController` found its package/CLI and this integration test; no dedicated controller lifecycle test was located in the inspected search results. Search absence is not proof that no test exists elsewhere.

### 4. Separate Execution Host package

The repository also contains `execution_host/host.py`, a more developed process execution host with context validation, command validation, timeout handling, output redaction, process cleanup, artifact collection and execution evidence. It exposes an execution-host capability surface; this source trace did not establish that it is wired into `wee.LifecycleController`, the Work 70 lifecycle state machine, Core authorization, Work Package registry or Dashboard.

Consequently:
- Do not treat `wee/` as the Work 70 Lifecycle Engine without a contract and integration proof.
- Do not treat `execution_host/` as Work 70 lifecycle governance or authorization.
- Do not duplicate either package before architecture owners compare responsibilities and dependency boundaries.
- Do not infer Work 70 readiness from Work 13 adapter tests.

### 5. Core API recheck

The current `main` version of `room_hop_mcp/adapter/http_server.py` still registers Identity and Meeting routes only. The inspected `API_CONTRACT.md` describes Meeting/Identity HTTP behavior, not Work-scoped lifecycle, Work Package, evidence registry or export APIs. The proposed `/api/v1/works/{work_id}/...` routes in Work 70 documentation remain proposals, not verified Core endpoints.

This is a bounded source observation of the inspected router/contract, not proof that no Work-related implementation exists in any other module. Core Work API/auth/evidence capabilities remain NOT VERIFIED.

### 6. Updated technical disposition

| Area | Current evidence-based disposition |
|---|---|
| WEE authority/context/evidence primitives | Source exists on main; Work 70 integration NOT VERIFIED |
| WEE lifecycle controller | Partial orchestration; stops BLOCKED at TEST |
| WEE direct Work 13 adapter test | Test source exists; does not exercise controller lifecycle |
| Separate execution_host | Source exists; Work 70 lifecycle/authorization wiring NOT VERIFIED |
| Core Work API and Work authorization | NOT VERIFIED |
| Work 70 lifecycle integration | NOT IMPLEMENTED / NOT VERIFIED |
| Build branch | DIVERGED: 34 ahead / 379 behind; DO NOT MERGE BLINDLY |
| G4 / BUILD authorization | NOT READY / NOT PASS |
| Independent QE | NOT RUN |

### 7. Recommended next technical sequence

1. Architecture reconciliation: map `wee/`, `execution_host/`, Work 70 Lifecycle Engine, Core and Dashboard responsibilities without merging code.
2. Add controller-level tests proving every stage, including actual invocation of the bound test entrypoint, negative/timeout behavior, and no false EXECUTE PASS on discovery-only results.
3. Establish the trusted authorization boundary before any protected Work mutation; client-provided `authorized` or role flags must not be treated as authority.
4. Identify the Core owner and verify the actual Work-scoped API/auth/evidence contract.
5. Reconcile the Build branch only after a file-level ownership/diff plan and preservation evidence exist.

**Boundary:** this addendum is read-only source analysis. It does not approve DOC-061 architecture, authorize BUILD, alter any Gate, or certify any runtime test.


---

## Addendum 2026-11-02 — Ka WP70-KA-RUNTIME source-level architecture reconciliation

**Classification:** INDEPENDENT SOURCE REVIEW / DESIGN FINDINGS ONLY / NOT IMPLEMENTATION APPROVAL / NOT QE / NOT GATE PASS.  
**Reviewer:** Ka / AI-02 — CSA / Architecture Reviewer — WP70-KA-RUNTIME.  
**Journal evidence:** DOC-035 entry timestamped 2026-11-02 02:17:51 +07:00.  
**Reviewed source baseline stated by Ka:** GitHub main `21190f8449656ac65a2b5682621e1c4f75a0d6dd`.  
**Source limitation:** Ka could not fetch DOC-061 from `work/70/05-build` and did not retry Sandbox read; DOC-016/DOC-017 were not directly read in this review. Findings below are source-level observations from the enumerated source files, not a complete reconciliation of all architecture documents.

### 1. Confirmed findings from inspected source

1. **WEE LifecycleController is partial.** `LifecycleController.run()` uses `LocalExecutionHost` capability discovery; it records EXECUTE PASS after discovery, does not invoke the bound test entrypoint, and returns TEST BLOCKED with `test_execution_not_available_in_sandbox_boundary`. Discovery must not be represented as execution. Controller E2E is not demonstrated.
2. **There are multiple execution paths with unclear ownership.** `wee/bridge/real_host.py` contains a real process execution adapter; `execution_host/host.py` is a separate, more developed execution host; `ExecutionHostBridge` forwards requests to `:8031`. No inspected evidence proves which is the single Work 70 execution boundary or that the server endpoint is bound to the same authorization/evidence contract. Do not build a third engine/host.
3. **ExecutionHost caller authorization is too weak for DOC-063.** The inspected models/bridge/security path carries and checks caller-provided `authorized: bool`; no signed/scoped authorization proof or server-side re-resolution of principal, assignment, source revision, Gate/WP snapshot, expiry/revocation or policy version is visible in those inspected files. The server HTTP/auth middleware was not located, so this is a confirmed gap in the reviewed client/model/host contract, not proof that no external perimeter exists.
4. **Potential false aggregate PASS.** `ExecutionHost.execute_work()` returns top-level status from the primary command while attaching test execution as nested `result['test']` when `run_test=True`. A successful primary command with a failing test may therefore still produce top-level PASS. Existing inspected tests do not exercise this failure combination.
5. **Bridge response identity binding is not strict.** `ExecutionHostBridge.invoke()` accepts returned Work/execution IDs and falls back to caller context when absent; the inspected path does not reject mismatched returned IDs. Tests inspected cover several transport cases but not mismatched identity binding/forged response correlation.
6. **Core Work capabilities remain NOT VERIFIED.** The inspected Core HTTP adapter exposes Identity and Meeting routes through MeetingService; Work/WP registry, assignment/ACK, lifecycle, Work authorization, Evidence Registry and export routes were not found in that inspected router. This is bounded to inspected scope, not a claim about every repository module.
7. **Evidence persistence in inspected components is local-file based.** WEE `EvidenceStore` writes JSON files; ExecutionHost writes stdout/stderr and `FINAL_RESULT.json` under `evidence_root`. No Core-backed Work Evidence Registry, transactional audit coupling, command idempotency store, commit-time authorization recheck or outbox/reconciliation path was demonstrated.

### 2. Component capability and ownership disposition

| Component | Classification | Current boundary / gap |
|---|---|---|
| CanonicalWorkAuthority | EXISTING / LOCAL FILE AUTHORITY | JSON binding; Core-backed identity/assignment/ACK/Gate resolution not demonstrated |
| WEE LifecycleController | PARTIAL | Controller stops BLOCKED at TEST; discovery-only EXECUTE PASS semantics need correction |
| WEE LocalExecutionHost | EXISTING / LOCAL | Capability discovery/helper, not production Work 70 execution evidence |
| WEE RealExecutionHost | EXISTING / SEPARATE IMPLEMENTATION | Overlaps ExecutionHost; Work 70 authority integration unverified |
| Work13ExecutionHostAdapter | EXISTING / WORK13-SPECIFIC | Direct adapter test is not generic LifecycleController E2E |
| ExecutionHost | EXISTING / STANDALONE HOST | Caller boolean authorization; aggregate test result risk; local evidence path |
| ExecutionHostBridge | EXISTING / CLIENT BRIDGE | No strict response Work/execution identity binding in inspected path |
| Core HTTP adapter | VERIFIED FOR INSPECTED ROUTER ONLY | Work/WP/AuthZ/Evidence/Export not found in inspected router |
| Evidence Registry | NOT VERIFIED | Local files do not prove canonical Work evidence persistence |
| Dashboard | CONTRACT EXISTS / LIVE INTEGRATION NOT VERIFIED | Must remain read-only; no local fixture presented as Core live |
| Independent QE | PARTIAL TEST COVERAGE | Controller E2E, authorization boundary, aggregation, identity binding and race/revocation not evidenced |

### 3. Runtime paths observed — not an approved target architecture

- `CanonicalWorkAuthority(JSON) → WorkContext → LifecycleController → LocalExecutionHost.discover() → EXECUTE marked PASS → TEST BLOCKED`.
- Separate Work 13 adapter path: `Work13ExecutionHostAdapter → WEE RealExecutionHost.execute() → local evidence files`.
- Separate host path: `ExecutionHostBridge → HTTP :8031 /execute → ExecutionHost → local evidence files`.
- Inspected Core path: `HTTP Adapter → MeetingService → MeetingManager` (Meeting domain).

These paths must not be conflated into one verified Work 70 lifecycle runtime.

### 4. Required architecture and test decisions

- Keep WEE LifecycleController as an orchestration candidate, but future approved contract must distinguish DISCOVER from EXECUTE. EXECUTE PASS requires actual command invocation and result. TEST PASS requires invocation of the bound test entrypoint, successful exit/result, matching Work/execution correlation and persisted evidence.
- Compare the deployed server/runtime, security model, process boundary, test runner and evidence path for WEE RealExecutionHost versus ExecutionHost; select/reuse one authoritative host after ownership and integration proof. Do not create a third host.
- Replace caller boolean authorization as authority with server-side resolution and scoped proof bound to principal, Work/WP/assignment, action/resource, source revision, Gate/WP version, policy version, expiry/revocation and idempotency key.
- Define aggregate result: overall PASS only if required command, bound tests and required evidence/artifact checks all pass. Test failure, timeout or missing evidence must yield FAIL/BLOCKED.
- Reject bridge responses whose Work ID or execution ID differs from the request; audit mismatch.
- Extend independent tests to controller E2E, discovery-vs-execution false PASS, successful command + failing test, missing test runner, spoofed authorization boolean, wrong Work/execution response, revocation/source/Gate version changes, audit/evidence failure and idempotent retry.
- Keep Core Work routes/storage and Dashboard live integration NOT VERIFIED pending Vi's independent trace. No Core owner/server auth contract was established by this review.

### 5. Ka review disposition and open deliverables

- Ka source-level architecture review: FINDINGS RECORDED / DESIGN REVIEW ONLY.
- DOC-061 direct fetch on `work/70/05-build`: BLOCKED / NOT_FOUND during Ka's review; DOC-016/DOC-017 not directly read in that review.
- Core owner and actual `:8031` server authorization contract: NOT VERIFIED.
- Controller E2E: NOT VERIFIED; inspected controller path returns TEST BLOCKED.
- Independent QE: NOT RUN BY KA.
- The source findings provide a capability matrix and runtime-flow observations, but a separately approved target runtime diagram, final component ownership matrix and integration contract remain pending Xu/Ka reconciliation with DOC-016/DOC-017 and Vi/An evidence.
- No code, Core, Engine, Dashboard, Gate, state, assignment or permissions changed.
- G4: NOT READY / NOT PASS. BUILD implementation: NOT AUTHORIZED. Work 70: ACTIVE / NOT ACCEPTED / NOT RELEASED.

This addendum records Ka's source review without turning findings into implementation approval or changing any Gate/authority.


## Addendum 2026-11-02 — Existing test inventory for controller / ExecutionHost gap

**Classification:** TEST-SOURCE INVENTORY ONLY / NOT EXECUTED / NOT QE.

Additional source inspected:
- `tests/test_execution_host.py`, blob `183cba2959db9d9fb00751055efdeddd09c14a64`.
- `wee/cli.py`, blob `e745cfcd10a03b6cf87153bdf9321a207246fd18`.
- `wee/readiness.py`, blob `f765568e4567476b36ba21090b5fc06663abdb00`.

`tests/test_execution_host.py` contains 10 named tests: valid execution/evidence; invalid context/unauthorized; workspace escape; cwd escape; forbidden command/injection; timeout/cleanup; secret redaction; missing Git authority/unavailable adapters; artifact isolation; service lifecycle. The inspected test names do not include `run_test=True` with a failing test, top-level aggregate status, caller-boolean spoofing across a server boundary, bridge response Work/execution ID mismatch, commit-time revocation, Gate/source version race, audit persistence failure or idempotent duplicate command behavior.

`wee/cli.py` directly resolves a `CanonicalWorkAuthority` binding, constructs `WorkContext`, then calls `LifecycleController(...).run()`. `wee/readiness.py` runs only `LocalExecutionHost.discover()` and reports capability readiness; WEE READY is not evidence of a completed Work lifecycle or test execution.

**Test gap classification:**
- ExecutionHost unit coverage: PARTIAL (10 named tests; actual test run not performed by Xu).
- LifecycleController E2E: NOT VERIFIED in this source inventory.
- Test result aggregation: NOT COVERED by named existing tests inspected.
- Server authorization and response binding: NOT COVERED by the inspected bridge/host test files.
- Race/revocation/idempotency/audit atomicity: NOT COVERED by the inspected named tests.

This inventory informs An's independent QA assignment; it does not pre-empt An's test conclusions and does not claim tests failed or passed.


## Addendum 2026-11-02 — Xu reconciliation of Vi Core trace with DOC-016/DOC-017

**Classification:** READ-ONLY SOURCE RECONCILIATION / DESIGN ONLY / NOT IMPLEMENTATION AUTHORIZATION.

### Evidence integrated
- Vi / WP70-VI-CORE-TRACE draft: `05_BUILD/10_AI_DEBUG_HANDOFF/DRAFT_VI_WP70_CORE_TRACE_20261102.md`, dated 2026-11-02, signature `[KÝ: VI | CODER]`. It records router blob `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d`, MeetingService blob `0b80a81663c1be328c41878a6762d16d95378aab`, API_CONTRACT blob `29b33cfd4aca4252d9786965f7e54b519a77f72b`, and Dashboard snapshot blob `2c4fd26b833147e0e9e39747a5bfa95d70ba2a8d`.
- DOC-016 — Storage & File Export Architecture: `05_BUILD/03_ARCHITECTURE/STORAGE_AND_EXPORT_ARCHITECTURE.md`, design proposal only.
- DOC-017 — Core Capability Gap Assessment: `05_BUILD/03_ARCHITECTURE/CORE_CAPABILITY_GAP_ASSESSMENT.md`, read-only source review; integration not verified.
- DOC-035 records Ka's runtime review, Xu's source spot-check and An's QA preparation. These remain distinct evidence classes.

### Reconciliation result
1. **Core API boundary — CONSISTENT.** Vi's fetched router/API contract observations agree with DOC-016/DOC-017 and Ka/Xu's bounded source review: inspected HTTP router and API contract expose Identity/Meeting capabilities; no Work/WP/lifecycle/evidence/export routes were found in that inspected scope. This is not proof that no implementation exists elsewhere in the repository.
2. **Meeting artifact boundary — CONSISTENT.** MeetingService.save_artifact is Meeting-domain behavior and is not a generic Work Evidence Registry or storage/export service. Do not repurpose it.
3. **Dashboard data source — CONFIRMED LOCAL SNAPSHOT.** Vi traced Dashboard index to relative `PRODUCT_STATUS.json`; the snapshot declares `source_mode=local_snapshot`, timestamp `2026-10-30T09:10:00+07:00`, and WP70-04 Core read integration BLOCKED. Dashboard is not Core-live and must not be represented as such.
4. **Proposed API routes — DESIGN ONLY.** Routes in DASHBOARD_CORE_READ_CONTRACT remain proposed and are not verified endpoints. No adapter should call guessed routes or silently fall back to a local snapshot while claiming live data.
5. **Storage/export — DESIGN ONLY.** DOC-016's Core-owned metadata, managed Storage Adapter, immutable evidence, integrity/read-after-write, audit and export requirements remain target design. No generic Core Work evidence registry, storage or export implementation is evidenced by the inspected sources.
6. **Scope limits — PRESERVED.** Vi's code-search absence and router inspection are bounded observations, not repository-wide proof. Runtime Core behavior was NOT RUN. DOC-016/DOC-017 retain their canonical-candidate/migration-pending status; this addendum does not promote them to approved implementation contracts.

### Remaining reconciliation / decision items
- Core owner must identify whether a Work registry/evidence service exists outside the inspected router and provide canonical source paths, revisions, auth boundary and tests; if absent, the Core owner must own the proposal and implementation decision.
- Ka/Xu must finish selecting one authoritative lifecycle/execution-host path and reconcile the target contract with DOC-005, DOC-010, DOC-016, DOC-017, DOC-054, DOC-057 and DOC-063. Do not create a third execution host.
- Vi's report remains DRAFT and explicitly reports Work Entry G0-G5 not all PASS; no participant-specific implementation authorization is evidenced. Dashboard adapter implementation remains NOT AUTHORIZED.
- An's runtime QA remains NOT RUN / EXECUTION BLOCKED. Source inventories are not runtime test results.
- DOC-060 gate namespace remains PROPOSAL ONLY and requires Vinh's decision. No gate IDs or authority changed here.

### Xu disposition
- Core Work API/auth/persistence/evidence/export: NOT VERIFIED in inspected scope.
- Dashboard Core-live integration: BLOCKED; local snapshot only.
- DOC-016/DOC-017: consistent with Vi/Ka/Xu evidence; no conflict requiring a design change identified in this reconciliation.
- G4: NOT READY / NOT PASS. BUILD: NOT AUTHORIZED. Work 70: ACTIVE / NOT ACCEPTED / NOT RELEASED.
- No source code, Core, database, Engine, Dashboard, Gate, state, assignment, permission or release status changed.


## Correction / Addendum 2026-11-02 — Xu locates the :8031 HTTP server entrypoint

**Supersedes the earlier bounded statement that the authoritative :8031 server handler was not identified.** The earlier search was incomplete; this addendum corrects the record without erasing the prior audit trail.

### Newly inspected source
| Path | Branch | Blob SHA | Finding |
|---|---|---|---|
| `execution_host/server.py` | `main` | `45aec57525b5d55bb63544b7bd7fd23062e06151` | Defines `POST /execute`; parses request JSON; constructs `WorkContext(**body['work_context'])` and `ExecutionRequest`; calls `self.host.execute_work(ctx, req)`; returns result. |
| `execution_host/identity.py` | `main` | `517dbb36bbdbfa3b606a6dec98c82612e12eeefa` | RuntimeIdentity includes instance/build hash/process metadata; default bind address string is 127.0.0.1:8031. Identity is runtime metadata, not caller authentication. |
| `execution_host/models.py` | `main` | `2488b7c95cf3784fc26eaf677044fe5ab0866420` | WorkContext contains caller-populated `authorized: bool`. |
| `execution_host/security.py` | `main` | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | `validate_context()` checks required fields and `ctx.authorized`; no signed/scoped authorization proof is represented in this contract. |

### Confirmed source observations and limits
1. `server.py`'s Handler checks the path and runtime initialization, but the inspected `do_POST()` contains no authentication header/token/principal validation or server-side Work/assignment/Gate authorization resolution before constructing WorkContext and invoking the host.
2. `serve(host='127.0.0.1', port=8031)` binds a standard `ThreadingHTTPServer` to the supplied host/port; default is loopback. This reduces default network exposure but is not an authorization mechanism. A reverse proxy, OS boundary, firewall or external perimeter may exist elsewhere; that deployment perimeter was NOT VERIFIED.
3. The handler trusts request-body `work_context` fields, including `authorized`; the host security layer validates that boolean, not a signed/scoped authority proof. The previously confirmed client-side boolean gap therefore reaches the inspected server entrypoint.
4. `GET /health` returns runtime identity metadata; it does not authenticate a caller or prove Core authorization.
5. GitHub code searches for `execution_host.server`, `python -m execution_host.server`, `execution_host/server.py`, and `serve(port=8031)` did not locate a repository launch/deployment reference. Search is not exhaustive; actual process startup, reverse proxy, network exposure and PC deployment remain NOT VERIFIED.

### Security disposition
- **Confirmed source-level concern:** the inspected HTTP handler has no visible request authentication or server-side authorization re-resolution; caller-controlled `authorized: bool` is passed to host validation.
- **Not established:** whether the deployed PC process is actually running this server, whether it is exposed beyond loopback, or whether a separate trusted perimeter wraps it.
- **Required before any Work 70 execution integration:** identify the deployed process/build hash and bind address; inspect any proxy/firewall/service wrapper; establish authenticated principal binding; server-side resolve Work/WP/assignment/action/source/Gate/policy/expiry/revocation; revalidate at commit/execute boundary; reject caller-supplied authority booleans; add positive and negative HTTP-boundary tests.
- This strengthens DOC-063 design requirements but does not implement them. Do not enable :8031 for Work 70 or treat health PASS as authorization.

### Test gaps to assign to An after authorized runner exists
- POST /execute with `authorized=true` but no authenticated principal must be DENIED.
- Spoofed Work ID, assignment, role, Gate PASS, source revision, expiry or policy version must be rejected/re-resolved server-side.
- Missing/malformed/duplicate JSON keys and oversized bodies must fail safely (additional review; not yet tested).
- Runtime identity/build hash must be captured and bound to the execution evidence.
- Loopback-only binding and any proxy exposure must be verified in the deployed environment.

**Status:** SOURCE TRACE UPDATED / STATIC ONLY / NO RUNTIME TEST / NO CODE CHANGE. Work 70 G4 remains NOT READY / NOT PASS; BUILD NOT AUTHORIZED.


## Reconciliation correction 2026-11-02 — Recheck Co's prior Work 28 :8031 trace

**Reason:** Xu's previous addendum inspected GitHub main only and repeated a source-level conclusion without reconciling Co's earlier Work 28 hardening. That was incomplete. This correction supersedes the prior unqualified statement about the :8031 boundary. No historical journal entry is deleted.

### 1. Work 28 source and Co evidence located
- Work 28 branch: work/28-mcp-tooling-platform, HEAD at time of review a652c49fdc738424a27c6408b386df2dd1af4540.
- Co's evidence: work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/REPO_SIDE_W13_HANDLER_AUTH_HARDENING_20261025.md, blob 8e420fa16000eaa9d480a112a813c678e69a6331.
- Current hardened branch execution_host/server.py, blob 87644127a9a2df638b5677758cfc4d0c883b2985.
- Co's record identifies handler auth fix 1f0e6916bf317b0e5bebed819f100ec08ac35945, per-Work allow-list follow-up 5d52cf2e6b4e4e5d758327c5925ea7c5345a1822, startup bootstrap dc91ffc71bc5985ac1056c78182708f87a039ba2, syntax correction 769b13fed8b070d8cacf987cb8729eab5c8df998, plus later bridge token and staged client work. Co explicitly records source/CI evidence separately from deployment proof.

### 2. What Co implemented on Work 28 branch
- POST /execute requires X-Room-Hop-Execution-Auth; token compare uses hmac.compare_digest; absent/unarmed/wrong token returns 401 before host invocation.
- Server-side Work allow-list uses ROOM_HOP_AUTHORIZED_WORKS, canonical W<number>; an unlisted Work or missing allow-list returns 403 before host invocation. Handler overwrites work_context.authorized=True only after token + allow-list checks; caller-supplied boolean is not the gate.
- main() loads ROOM_HOP_EXECUTION_AUTH_TOKEN and ROOM_HOP_AUTHORIZED_WORKS; missing/blank/malformed config raises before startup. The __main__ path calls main(), which forwards the loaded values into serve(). Token is not printed.
- Handler also limits request body to 256 KiB, requires JSON, rejects unknown top-level keys, and returns 405 for PUT/DELETE/PATCH. Evidence readback route requires the same token.
- Co's test inventory: test_w13_execute_handler_http_boundary.py covers real local HTTP handler behavior (401 missing/wrong/unarmed, 403 unlisted Work, authenticated + allow-listed call reaches fake host); test_w13_execution_auth_config_bootstrap.py checks env loading, fail-loud, Work ID normalization and main→serve wiring; test_w13_execute_handler_auth.py covers token comparison and API seam. Co's report records CI green after the clean rebuild and handler-level tests, not deployed service proof.

### 3. Important remaining limits in the hardened Work 28 source
- Authentication is a shared bearer token, not a caller identity: the handler proves possession of one configured token; it does not itself resolve a distinct AI/principal identity or assignment from Core.
- Work allow-list is static deployment configuration: it scopes the token to a set of Work IDs, but is not a dynamic per-assignment/role/action decision.
- Core grant source is optional and has a fallback: build_grant_source() uses ROOM_HOP_CORE_GRANT_URL when configured, otherwise a local file registry. main() catches any Core grant fetch exception and falls back to load_grant_registry(). Therefore the code does not prove that live Core grants are being used; a Core outage can fall back to a local registry. The inspected Work 28 audit says the Core :8000 execution-grant API did not exist in the audited Core package; proposed contract remained design-only.
- Command mode remains possible by default: dispatch_execute() defaults to mode='command'; this calls the general ExecutionHost.execute_work() with caller-supplied execution_request. snapshot_only is enabled only when ROOM_HOP_SNAPSHOT_ONLY is set to a truthy value; its default is false. The stricter grant/hash-bound work28_snapshot path is a separate mode. Do not equate token + allow-list with mandatory immutable-snapshot execution.
- Network boundary: Work 28 main() explicitly binds 127.0.0.1:8031 over the standard HTTP server (not TLS). No reverse-proxy, remote ingress, Windows service, scheduled task or firewall policy configuration was identified in the inspected Work 28 repository tree. Actual PC firewall/proxy/service-manager state remains NOT VERIFIED.
- Readiness is not release proof: work28_readiness.py reports os_isolation=NOT_VERIFIED, release=NOT_RELEASED, and core_grant_live=BLOCKED when the Core grant URL is not set. /health reports readiness metadata; it does not prove the deployed process has the intended source or a secure network perimeter.

### 4. Cross-check against canonical Work 13 Sandbox and PC evidence
- Current Work 13 Sandbox file EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/server.py is the pre-hardening implementation: it has no auth header check, no token configuration, and directly deserializes caller WorkContext/ExecutionRequest before calling the host. This agrees with Co's section 12 cross-Work comparison.
- Work 13 handoff 03_ARCHITECTURE/PC_INTEGRATION_HANDOFF.md identifies intended package startup as python -m execution_host.server, default bind 127.0.0.1:8031. It includes a manual command but is not a Windows service/automatic startup registration.
- Sandbox execution_host_start.err.log records a failed direct-file launch (python .../server.py) with ImportError: attempted relative import with no known parent package; that failure is consistent with invoking a package module as a file rather than python -m. It is not proof the correct module startup succeeded.
- 06_EVIDENCE/W13_CANONICAL_PC_RUNTIME_ATTESTATION_BLOCKER_LOG.md records a historical PID 5188, listener 127.0.0.1:8031 and /health PASS on 2026-10-08, but explicitly says /execute was not validly exercised in that attestation. W13_CANONICAL_RUNTIME_IDENTITY_FINAL_RESULT.json later records canonical startup NOT_EXECUTED, health/execute/runtime identity NOT_OBSERVED. EXECUTION-CURRENT.json contains an older narrower HTTP E2E PASS, but it does not prove the current source revision or Work 28 hardening is deployed.
- Xu's MCP read of the canonical Work 13 Sandbox confirms its current stored server.py is still the old unauthenticated version. This is source-state evidence, not a live PC process inspection.

### 5. Corrected disposition
| Layer | Correct status |
|---|---|
| Work 28 hardened source + tests | SOURCE HARDENING PRESENT; CI/handler-level evidence recorded by Co |
| GitHub main | STALE relative to Work 28 hardened server; still contains old handler at reviewed revision |
| Work 13 canonical Sandbox source | PRE-HARDENING / NOT SYNCED |
| Work 13 deployed PC process and exact build hash | NOT VERIFIED against Work 28 hardened source |
| Startup configuration on actual PC | Intended module entrypoint known; actual service manager/autostart/config loading NOT VERIFIED |
| Network exposure / firewall / proxy | Default source bind loopback; actual host firewall/proxy state NOT VERIFIED |
| Core identity/grant authority | NOT VERIFIED; Work 28 static allow-list + shared token are not full DOC-063 principal/assignment authorization |
| Work 70 use of :8031 | NOT AUTHORIZED until source sync, trusted startup config, deployed identity, scoped authorization, snapshot mode, isolation and live negative/positive E2E are verified |

**Xu's corrected conclusion:** Co's prior Work 28 trace is valid and materially more complete than Xu's previous main-only check. Do not repeat the source audit. The remaining Work 70 task is a controlled source/revision alignment and deployment attestation of the canonical Work 13 runtime, plus verification of actual network/service configuration. No code or deployment changes are made by this addendum.
