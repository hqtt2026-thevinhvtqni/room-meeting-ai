# DOC-063 — KIẾN TRÚC THỰC THI WORK ENTRY AUTHORIZATION VÀ DENY-TO-RECOVERY

- **Document ID:** DOC-063
- **Priority:** P0
- **Read order:** 63
- **Date:** 2026-11-01
- **Owner:** Xu / AI-01
- **Authority:** Vinh
- **Status:** DRAFT — DESIGN ONLY / NOT APPROVED / NOT IMPLEMENTED
- **Depends on:** DOC-001; DOC-004; DOC-005; DOC-043; DOC-044; DOC-057; DOC-061; DOC-062

## 1. Mục tiêu

Chuyển DOC-057 từ quy định chính sách thành hợp đồng kỹ thuật có thể kiểm thử. Mọi thao tác có tác động phải được kiểm tra quyền tại điểm thực thi; từ chối phải an toàn, có giải thích và có đường khôi phục. Tài liệu này không tự cấp quyền, không thay đổi gate, không phê duyệt API route/schema và không cho phép sửa Core trước khi G4 cùng source ownership được xác minh.

## 2. Phạm vi enforcement

Áp dụng cho mọi command làm thay đổi artifact, mã nguồn, dữ liệu, trạng thái Work/WP, cấu hình, quyền, migration hoặc release. Read-only discovery, đọc tài liệu, kiểm tra trạng thái và thu thập evidence vẫn được phép nếu principal có quyền đọc.

Không coi UI disable, prompt, lời khai role từ client, tên AI, nội dung DOC-054 hay cờ `authorized=true` do caller gửi là bằng chứng quyền.

## 3. Authorization decision input

Mỗi lần gọi công cụ có tác động phải được đánh giá từ nguồn tin cậy phía server:

- principal_id và identity assurance từ authentication middleware;
- work_id, wp_id, assignment_id;
- actor role và accountable owner lấy từ registry có thẩm quyền;
- allowed_actions và resource scope cụ thể;
- canonical repository/path/ref hoặc resource identifier;
- source revision/hash mà assignment được cấp dựa trên;
- gate snapshot và WP state tại thời điểm thực thi;
- issued_at, expires_at, revoked_at và policy_version;
- correlation_id, command_id/idempotency key và expected_version.

Client chỉ được yêu cầu hành động; không được tự khai các trường identity, role, gate PASS hay permission. Nếu bất kỳ nguồn bắt buộc nào không đọc được, stale, mâu thuẫn hoặc không xác minh được thì từ chối fail-closed đối với protected write.

## 4. Authorization evaluation order

1. Authenticate principal; nếu không có principal hợp lệ: DENY UNAUTHENTICATED.
2. Resolve Work và resource; không tiết lộ dữ liệu ngoài scope khi trả lỗi.
3. Resolve assignment đang hiệu lực và ACK có thể kiểm chứng; không có: DENY ASSIGNMENT_MISSING.
4. Resolve role, allowed action và resource scope; không khớp: DENY SCOPE_OR_ACTION_FORBIDDEN.
5. Revalidate source revision, expiry và revocation; stale/expired/revoked: DENY AUTHORIZATION_STALE.
6. Re-read authoritative gate/WP state; predecessor gate chưa PASS hoặc WP chưa READY/ACTIVE hợp lệ: DENY GATE_NOT_SATISFIED.
7. Validate command schema, expected_version, idempotency key và domain transition.
8. Chỉ sau tất cả kiểm tra mới cho phép domain handler thực thi mutation.
9. Ghi audit decision; mutation và audit phải atomic hoặc dùng cơ chế consistency/reconciliation được phê duyệt.

Mỗi bước phải có reason code ổn định và audit provenance. Không dùng thứ tự kiểm tra để làm lộ sự tồn tại của Work/resource mà principal không có quyền đọc.

## 5. Policy result contract

Authorization evaluator trả một trong hai kết quả:

- ALLOW: principal, Work, assignment, action, resource scope, policy version, source revision và expiry đã được xác minh.
- DENY: stable reason_code, safe_message, blocked_action, scope, evidence_refs, remediation_steps, allowed_safe_actions, responsible_owner, recheck_condition, unlock_criteria và support_route.

DENY không được chứa secret, token, stack trace nhạy cảm hoặc dữ liệu Work ngoài quyền đọc. Không được biến DENY thành PASS bằng retry tự động.

## 6. DENY-to-RECOVERY contract

Mọi DENY phải tạo được một Recovery Guidance record (bản hướng dẫn khắc phục) hoặc trả nội dung tương đương có cấu trúc:

| Trường | Yêu cầu |
|---|---|
| decision_id | ID duy nhất để truy vết |
| reason_code | Mã lý do ổn định, máy đọc được |
| blocked_action / scope | Thao tác và phạm vi bị chặn |
| evidence_refs | Bằng chứng xác định nguyên nhân; nếu chưa có ghi rõ NOT AVAILABLE |
| impact | Ảnh hưởng nếu không khắc phục |
| remediation | Hành động cụ thể, theo thứ tự |
| allowed_safe_actions | Việc read-only/khắc phục vẫn được phép |
| owner | Người/role chịu trách nhiệm xử lý |
| recheck | Điều kiện và cách đánh giá lại |
| unlock_criteria | Điều kiện rõ ràng để mở khóa |
| support_route | Nơi chuyển cấp khi owner không xử lý được |
| expires_at | Thời hạn hiệu lực của hướng dẫn nếu phụ thuộc trạng thái thay đổi |

Recovery guidance không tự thay đổi quyền hoặc state. Sau khi khắc phục, hệ thống phải chạy lại toàn bộ authorization evaluation từ đầu.

## 7. Reason code catalog — đề xuất

| Reason code | Điều kiện | Hướng khắc phục mặc định |
|---|---|---|
| UNAUTHENTICATED | Principal không hợp lệ/không tồn tại | Đăng nhập hoặc khôi phục identity; sau đó retry |
| WORK_NOT_FOUND_OR_NOT_VISIBLE | Work không tồn tại hoặc caller không được phép biết | Kiểm tra Work ID qua owner; không tiết lộ existence |
| ASSIGNMENT_MISSING | Không có assignment hợp lệ | Owner tạo assignment qua kênh chính thức và ghi nhận ACK |
| ACK_NOT_VERIFIED | Chưa có xác nhận nhận việc có bằng chứng | AI/person được giao xác nhận qua kênh được hỗ trợ |
| ROLE_MISMATCH | Role không phù hợp action | Owner điều chỉnh assignment/role; không tự nâng quyền |
| SCOPE_OR_ACTION_FORBIDDEN | Action/resource ngoài scope | Thu hẹp action hoặc xin phê duyệt assignment mới |
| AUTHORIZATION_STALE | Hết hạn, revoked hoặc source revision đổi | Revalidate assignment và cấp authorization mới |
| GATE_NOT_SATISFIED | Gate predecessor chưa PASS | Hoàn tất criteria, thu evidence và xin authority đánh giá |
| WP_NOT_READY | WP chưa đủ DoR hoặc chưa READY | Hoàn thiện WP baseline, owner/reviewer, dependencies và acceptance |
| EVIDENCE_REQUIRED | Thiếu/stale/không đọc được evidence | Bổ sung evidence có provenance; không dùng file tồn tại làm PASS |
| VERSION_CONFLICT | expected_version cũ | Đọc lại authoritative state; reconcile trước khi gửi command mới |
| IDEMPOTENCY_CONFLICT | Cùng key nhưng payload khác | Dùng command ID mới sau khi xác minh outcome cũ |
| POLICY_UNAVAILABLE | Policy/authority service không sẵn sàng | Giữ nguyên trạng thái; chỉ tiếp tục read-only/khắc phục an toàn |
| PATH_NOT_CANONICAL | Path ngoài canonical root/repo mapping | Tra DOC-003/DOC-036, xác định canonical path và được owner duyệt |
| SOURCE_REVISION_CHANGED | Source commit/hash khác baseline | Review diff, cập nhật assignment và tái cấp quyền |
| UNKNOWN_DENY | Lỗi không phân loại được | Fail-closed, giữ nguyên state, chuyển owner/security support |

Reason code catalog là đề xuất; phải được owner kiến trúc và Core owner phê duyệt trước khi trở thành API literal.

## 8. Audit và chống giả mạo

Audit record tối thiểu: decision_id, timestamp UTC, principal_id, Work/WP/assignment IDs, action/resource, allow/deny, reason_code, policy_version, source revision, gate/WP snapshot version, correlation_id, command_id và evidence references. Không ghi secret hoặc credential.

- Không cho caller tự tạo audit actor/role.
- Audit phải append-only hoặc có cơ chế tamper-evident được phê duyệt.
- Retry cùng command_id/payload phải trả outcome đã lưu; payload khác phải bị từ chối.
- Rejected command không được đổi authoritative state/version.
- Mất audit/persistence dependency thì protected write không được tiếp tục.

## 9. Bộ kiểm thử bắt buộc trước khi tuyên bố enforcement

Positive tests:
1. Principal hợp lệ, assignment ACK, scope/action khớp, source revision còn hiệu lực, gate PASS, WP READY và evidence đủ → ALLOW.
2. Read-only discovery với quyền đọc hợp lệ vẫn chạy khi G4 chưa PASS.
3. Recheck sau remediation chỉ ALLOW khi toàn bộ điều kiện đã đạt.

Negative/security tests:
1. Không authentication.
2. Client giả mạo actor_id/role/authorized/gate PASS.
3. Thiếu assignment hoặc ACK.
4. Assignment của AI khác, Work khác hoặc WP khác.
5. Action/path ngoài scope.
6. Assignment hết hạn hoặc revoked.
7. Source commit/hash thay đổi.
8. Gate chưa PASS hoặc WP DRAFT/BLOCKED.
9. Evidence thiếu, stale, hash mismatch hoặc store unavailable.
10. expected_version cũ; hai command cạnh tranh cùng version.
11. Idempotency key lặp với payload giống và payload khác.
12. Policy/audit service unavailable.
13. DENY response không rò rỉ secret hoặc Work ngoài quyền đọc.
14. Mọi DENY có remediation, owner, recheck, unlock criteria và support route.

Mỗi test phải lưu commit/version, fixture, environment, command, raw result và verifier. Implementer không tự ký independent QE. Test chưa chạy phải ghi NOT RUN; không suy ra PASS từ thiết kế test.

## 10. Phân lớp trách nhiệm

- Core owner: authentication, authoritative identity/authorization, policy enforcement boundary, persistence và audit atomicity.
- Lifecycle Engine: pure domain transition evaluator; không tự authenticate hoặc tự cấp quyền.
- Assignment/Work registry: cung cấp assignment, ACK, scope, source revision, expiry và revocation có provenance.
- Tool gateway/execution host: enforcement point trước protected action; không tin UI/client.
- Dashboard: read-only; hiển thị DENY và recovery guidance, không cấp quyền.
- AI adapter: chuyển request/result; không tự nâng role hoặc diễn giải DENY thành ALLOW.
- Independent QE: chạy positive/negative tests và xác minh bằng chứng.
- Xu: điều phối đối soát và tích hợp; Vinh giữ authority phê duyệt sản phẩm/gate/release.

## 11. Điều kiện chuyển từ DRAFT sang implementation-ready

Tất cả điều kiện sau phải được xác minh riêng:
1. G4 PASS theo DOC-004 bởi authority hợp lệ.
2. WP baseline được Vinh phê duyệt; từng WP thực thi đạt DoR.
3. Core owner được xác định và xác nhận source/API/auth contract.
4. DOC-061 runtime contract được architecture authority chốt.
5. Assignment và ACK của từng participant có evidence; permission gắn Work/WP/action/resource/source revision.
6. Canonical source repository/path/branch/commit được xác định; nhánh diverged không được merge mù.
7. Test plan và independent QE owner được xác nhận.
8. Rollback/recovery và audit strategy được phê duyệt.

Thiếu bất kỳ điều kiện nào: giữ DRAFT / NOT AUTHORIZED. Read-only investigation, contract refinement và test design vẫn có thể tiếp tục nếu được phép.

## 12. Kết luận hiện tại

- DOC-057 policy: ACTIVE.
- Technical enforcement: NOT VERIFIED / NOT IMPLEMENTED.
- DOC-063: DRAFT / DESIGN ONLY.
- DOC-060 gate namespace: PROPOSAL ONLY; không dùng namespace đề xuất như luật có hiệu lực.
- Manifest current phase: 01_DISCOVER PLANNED; G0/G1 NOT_READY.
- G4: NOT READY / NOT PASS.
- Core Work authorization boundary: NOT VERIFIED.
- Independent QE: NOT RUN.
- BUILD implementation: NOT AUTHORIZED.
- ACCEPT/RELEASE: NOT GRANTED / NOT RELEASED.

**Nguyên tắc khóa:** DENY phải chỉ ra đường khắc phục; nhưng recovery guidance không phải quyền thực thi. Chỉ authorization evaluation mới có thể mở khóa protected action.


---

## ADDENDUM 2026-11-02 — KA INDEPENDENT REVIEW: RECOVERY STORE SEPARATION & COMMIT-TIME AUTHORIZATION

**Status:** DESIGN REQUIREMENTS ADDED / NOT APPROVED / NOT IMPLEMENTED  
**Reviewer:** Ka / AI-02 — CSA / Independent Architecture Reviewer  
**Source record:** DOC-035, entry “2026-11-02 02:01:53 +07:00 — Ka / AI-02 — Phản biện độc lập Work Entry Gate và phản hồi chỉ đạo của Xu”  
**Authority:** Vinh; Core owner approval required for Core/API/storage contract.

### 13.1 P0.3 — Separate Work Entry / Recovery data from protected product data

The system MUST distinguish at least two authorization scopes and storage boundaries:

1. **Work Entry / Recovery scope:** submission of participant evidence, Work Entry evaluation inputs, DENY records, recovery guidance, remediation evidence and recheck requests.
2. **Protected Product scope:** source files, product artifacts, Work/WP authoritative state, configuration, lifecycle transitions, release records and other protected mutations.

Rules:
- Permission to submit Work Entry or remediation evidence MUST NOT imply permission to write protected product resources.
- A participant may submit evidence but MUST NOT set GATE_PASS, overwrite evaluator decisions, alter authoritative gate state, or change another participant's evidence.
- Gate evaluation and state transition remain server/authority-owned operations, not caller-controlled fields.
- The recovery store may be a logically isolated namespace/service or a physically separate store. The implementation choice requires Core owner architecture approval; this document does not assume a database or storage technology.
- Every record must carry provenance: authenticated principal, Work/assignment/scope, source revision, evidence hash/reference, timestamp, policy/evaluator version and correlation/command ID as applicable.
- Read/write permissions for this scope must be independently tested against protected product endpoints and resources.

Required tests:
- Recovery-evidence submission is allowed for an authorized remediation scope while protected product mutation remains denied.
- Caller-supplied GATE_PASS, evaluator result or authoritative state mutation is rejected.
- Evidence for another Work/participant or outside assignment scope is rejected.
- Recovery-store unavailability does not silently fall back to protected product storage or local/client storage.

### 13.2 P0.4 — Authorization validity at commit time; race and revocation safety

Authorization MUST remain valid at the point the protected mutation commits, not merely when the request first arrives.

Required contract:
1. Bind the authorization decision to principal, Work, WP, assignment, action, resource, source revision, policy version and authoritative Gate/WP snapshot/version.
2. Revalidate or enforce an equivalent concurrency guarantee at commit time. If assignment is revoked, scope changes, source revision changes, Gate/WP state changes, or authorization expires before commit, the mutation MUST fail without changing authoritative state.
3. Use a Core-owner-approved transaction, lock, compare-and-swap, fencing token or equivalent mechanism appropriate to the actual persistence topology. No specific mechanism is presumed until Core is traced.
4. Protected mutation and its audit record MUST be atomic or have an explicitly approved durable outbox/reconciliation protocol. Missing audit/persistence dependency MUST fail closed.
5. Retry with the same command/idempotency key and same payload MUST return the recorded outcome without duplicate mutation. Same key with different payload MUST be rejected.
6. External side effects that cannot participate in the Core transaction require an approved outbox, reconciliation and/or compensation design; do not claim atomicity without evidence.

Required tests:
- Revoke assignment after initial authorization but before commit; mutation is denied.
- Change source revision or Gate/WP snapshot between validation and commit; stale command is rejected.
- Two concurrent commands target the same expected version; at most one commits and the other receives a deterministic conflict.
- Simulate audit write failure and persistence failure; no un-audited protected mutation is committed.
- Retry same command/payload; exactly one mutation. Retry same key/different payload; reject.
- Exercise partial external side effect and prove approved reconciliation/compensation behavior, or explicitly classify the path unsupported and fail closed.

### 13.3 Ownership and evidence boundary

- **Core owner:** approve authoritative identity/authorization, transaction/concurrency, persistence and audit contract; identify actual enforcement boundary.
- **Ka / AI-02:** independent architecture review of trust boundary, storage separation and commit-time validity; no implementation ownership implied by this addendum.
- **Vi:** source-trace all Core write paths and report actual transaction/auth/audit behavior with file/symbol/test evidence.
- **An:** independent negative/race/idempotency/evidence-failure tests; distinguish test design from executed runtime evidence.
- **Xu / AI-01:** integrate findings and maintain DOC-063/DOC-055/DOC-035; no unilateral Core contract approval.
- **Vinh:** policy, Gate namespace and BUILD authorization decisions.

### 13.4 Current disposition

- Ka review findings P0.3/P0.4: RECORDED AS DESIGN REQUIREMENTS.
- Recovery/Protected data separation: NOT IMPLEMENTED / NOT VERIFIED.
- Commit-time authorization and race safety: NOT IMPLEMENTED / NOT VERIFIED.
- Core owner contract: PENDING.
- Vi source trace and An independent QE: PENDING EVIDENCE.
- DOC-063 remains DRAFT / DESIGN ONLY / NOT APPROVED.
- DOC-060 remains PROPOSAL ONLY; no namespace activation.
- G4 remains NOT READY / NOT PASS; BUILD remains NOT AUTHORIZED.

This addendum refines the design requirements only. It does not change DOC-057 policy, authorize Core changes, grant permissions, alter Gate state, or claim runtime enforcement.
