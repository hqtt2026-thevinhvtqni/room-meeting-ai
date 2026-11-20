# W113 — PHƯƠNG ÁN KIẾN TRÚC THAM VẤN ĐỘC LẬP
- DOC-ID: DOC-015
- Mã nghiệp vụ dự kiến: PA-W113-20261112-001 (PROPOSED — CHƯA ĐƯỢC XU CẤP / CHƯA PHÁT HÀNH)
- Phiên bản: 1.0 — DRAFT / CONSULTATION ONLY
- Work: 113 — ROOM-HOP-UNIVERSAL-DASHBOARD
- Nguồn tham vấn: W70-AI-CONSULT-01
- Người soạn: Co — AI-07 / Coder Assistant
- Chủ trì tổng hợp: Xu — AI-01
- Chủ sở hữu / thẩm quyền cuối: Vinh
- Thời điểm: 2026-11-12 21:45 UTC+7
- Trạng thái: DRAFT — WAITING FOR XU SYNTHESIS AND VINH DECISION
- Phạm vi: kiến trúc và governance; không phải lệnh thi công.

## 1. Mục đích
Ghi nhận ý kiến kiến trúc độc lập của Co cho định hướng ROOM-HOP cộng tác đa AI và Dashboard. Đây là tài liệu tham vấn, không thay thế quyết định của Vinh, không cấp quyền triển khai.

## 2. FACT / ASSUMPTION / RECOMMENDATION
### FACT — dữ liệu đã kiểm tra
- W113 Sandbox có DOC-001..DOC-014 và cấu trúc lifecycle; DOC-008 Product Architecture đang DRAFT, API/runtime contracts chưa xác minh.
- W113 DOC-013 ghi G0–G5 NOT ASSESSED; product source NOT DECLARED; UI implementation NOT STARTED; Browser/Mobile E2E NOT RUN; acceptance/release NOT AUTHORIZED.
- W113 DOC-004 đã ghi baseline: một Dashboard product role-adaptive; domain owners giữ authority; Dashboard không phải nguồn dữ liệu; W70 là governing lifecycle standard.
- W52 có tài liệu A2A contract, state machine, permission matrix và error/retry/cancel. Tài liệu thiết kế không tự chứng minh runtime dispatch/ACK.
- W113 DOC-008 quy định Dashboard đọc qua API/Bridge contracts đã xác minh; không truy cập DB/filesystem trực tiếp.
- W113 Sandbox read/write evidence không tự chứng minh GitHub parity hoặc runtime behavior.

### ASSUMPTION — cần tiếp tục xác minh
- Chưa đủ bằng chứng rằng ROOM có thể dispatch trực tiếp vào mọi AI session đang hoạt động.
- Chưa đủ bằng chứng về authenticated recipient ACK enforced trước execution.
- Chưa đủ bằng chứng Core có API/owner/service thực thi grant lifecycle và run ledger đầy đủ.
- Chưa đủ bằng chứng W113 Dashboard đang đọc live data từ Core.
- Chưa đủ bằng chứng về lease/lock thực tế để ngăn concurrent edits.

### RECOMMENDATION
Chọn Hybrid Multi-Agent làm kiến trúc mục tiêu để Xu tổng hợp; chưa phê duyệt thi công.

## 3. Kiến trúc cộng tác đa AI
Đề xuất Hybrid: Manager-led orchestration kết hợp Peer-to-Peer collaboration có kiểm soát.
- Vinh: Product Owner / Final Authority.
- Xu: Lifecycle Orchestrator; phân rã, điều phối, xử lý dependency và escalation.
- Core: authority cho identity/authorization và các lifecycle records thuộc domain Core thực sự sở hữu.
- Agent Runtime: adapter, session reference, context, dispatch, progress và handoff.
- Execution Host: enforcement tại ranh giới thực thi, process/filesystem/command policy, run result.
- Independent Reviewer: kiểm tra độc lập, không tự nghiệm thu phần mình làm.
- Peer-to-Peer chỉ dùng cho trao đổi chuyên môn; assignment, scope, quyền, trạng thái chính thức và acceptance phải đi qua authority có thẩm quyền.

## 4. Session và dispatch
Ba phương thức tích hợp cần phân biệt:
1. NATIVE_CONNECTOR: chỉ tuyên bố hoạt động khi connector/provider xác minh hỗ trợ định tuyến tới phiên hiện tại.
2. SESSION_HANDOFF: gói context/task để AI tiếp tục trong phiên hiện tại khi khả thi; có thể cần thao tác tiếp nhận.
3. API_ADAPTER: giao tiếp qua API được cấp phép và xác thực.
session_ref chỉ là tham chiếu, không phải credential và không chứng minh phiên còn hoạt động. Không chia sẻ token/cookie giữa AI. Khi mất phiên phải đánh dấu UNKNOWN/EXPIRED, không tự nhận một phiên khác là phiên cũ.

Không phản hồi không đồng nghĩa FAILED. DELIVERY_UNKNOWN phải đối soát trước retry. Retry cần idempotency; cancellation chỉ xác nhận khi runtime có bằng chứng dừng.

## 5. Task và state model
Không dùng một state machine duy nhất. Tách bốn lifecycle liên kết bằng IDs:
- Assignment: DRAFT/READY/DISPATCHED/ACKNOWLEDGED/IN_PROGRESS/IN_REVIEW/DONE; ngoại lệ BLOCKED/REJECTED/CANCELLED/EXPIRED.
- Transport: CREATED/SEND_ATTEMPTED/DELIVERED/DELIVERY_UNKNOWN/DELIVERY_FAILED.
- Execution: NOT_STARTED/RUNNING/RESULT_SUBMITTED/FAILED/CANCELLED/TIMED_OUT.
- Review: NOT_REVIEWED/REVIEWING/APPROVED/REQUEST_CHANGES/BLOCKED.
HANDOFF là event/transfer record có source owner, target owner, receipt và context; không thay thế DONE.
IDs tối thiểu: work_id, wp_id, assignment_id, task_id, dispatch_id, attempt_id, event_id, ai_id, session_ref, review_id, evidence_ref, correlation_id.

Mỗi assignment cần owner, coordinator, reviewer, scope, prohibited actions, baseline revision, dependencies, deliverables, acceptance criteria, permission grant reference và expiry.

## 6. Code ownership và dependencies
- Mỗi WP có một accountable owner.
- Sử dụng branch/worktree riêng khi khả thi; khóa/lease theo file hoặc vùng code khi cần.
- Kiểm tra starting SHA và phát hiện source drift.
- Không ghi đè thay đổi người khác; conflict tạo finding và reconcile.
- Reviewer không sửa evidence gốc.
- Dependency graph phải không chu trình; chỉ task phụ thuộc bị chặn khi prerequisite tương ứng chưa đạt.

## 7. Runtime authority và Run Record
Phân lớp:
- Core / Control Plane: identity, authorization, assignment authority, permission grant lifecycle, audit metadata.
- Agent Runtime / Agent Plane: adapters, sessions, context, dispatch, handoff.
- Execution Host / Execution Plane: kiểm tra quyền thực tế trước hành động; process, filesystem, command, network policy và kết quả.
- Evidence services: logs, artifacts, hashes, provenance, test results.
- Dashboard / Presentation Plane: read projection; không tự cấp quyền hoặc nghiệm thu.

Run Record tối thiểu gồm run_id, principal/ai_id, assignment/task, session/adapter reference, grant, source baseline, hành động thực tế, timestamps, exit code, output/error refs, artifact hash, test result và reviewer/evidence refs. Không có run record/evidence thì không được tuyên bố đã thực thi.

## 8. Hai Dashboard và dữ liệu
Đồng ý phân biệt:
- Work Execution Dashboard: Work/WP/assignment, AI/session, dispatch/ACK, execution, blockers, dependency, logs, evidence, review và gates.
- Product Dashboard: product capabilities, user journeys, service quality, business KPIs, alerts, version/release.
Có thể dùng chung navigation shell/design system/identity provider, nhưng không tạo hai authority hoặc database song song.
Mọi datum phải truy về domain owner, source_ref, source_revision/hash, observed_at, freshness và verification status. UNKNOWN/STALE phải hiển thị trung thực.

## 9. Kế thừa domain ownership
Đề xuất kế thừa, không viết lại:
- W01 Gateway; W02 Authorization; W11 AI member/identity adapter (theo đúng quyền sở hữu đã xác minh).
- W12 execution environment; W13 execution host; W14 nếu là owner sản phẩm/runtime hợp nhất theo hồ sơ hiện hành.
- W16 Workflow; W30 autonomous build practices; W52 AI communication/A2A; W70 lifecycle governance; W71 Meeting; W76 trigger; W102 agent loop; W113 dashboard; W114 graph/provenance projection.
Các Work nêu trên cần đối chiếu manifest và contract hiện hành trước khi giao thay đổi. W114 không tạo Task Registry thứ hai; W52 không tạo Core Identity; W113 không tạo operational database; W71 transcript không thay thế ACK; Dashboard không truy cập DB/filesystem trực tiếp.

## 10. Rủi ro chính
- Critical: identity spoofing; dispatch không có recipient ACK; execution vượt scope; self-approval.
- High: concurrent edit; duplicate retry; session loss; stale dashboard; mất provenance.
Điều kiện kiểm soát: authenticated principal; recipient ACK readback enforced trước RUNNING; idempotency; lease/revoke/fencing; independent review; immutable evidence references; source freshness.

## 11. Phân vai đề xuất
- Vinh: Owner / Final Approver.
- Xu / AI-01: Coordinator / Lifecycle Orchestrator.
- Ka / AI-02: Independent Architecture Reviewer.
- Cla / AI-03: Technical Lead khi được giao và xác minh capability.
- Kha / AI-04: Product Strategist.
- Qw / AI-05: Independent QE.
- Go / AI-06: Finance/assurance; chỉ review kỹ thuật khi đủ năng lực phạm vi.
- Co / AI-07: Coder/Executor; không tự nghiệm thu code của mình.
Vai trò là đề xuất; quyền thực tế phải được xác minh theo identity, capability và assignment.

## 12. Roadmap kiến nghị
0. Architecture reconciliation: đối chiếu W70/W52/W113/W114/W12/W13/W14; xác minh Core API/owner, session, ACK, grant, run record.
1. Contract & governance: Task/Event/Permission/Session-ACK/Review/Evidence contracts.
2. Controlled pilot: 1 coordinator + 1 executor + 1 independent reviewer + một task ít rủi ro.
3. Runtime integration: adapter, authenticated ACK gate, grant/revoke, idempotency, Run Record.
4. Dashboard integration: read projections, source provenance, freshness, role authorization.
5. Production readiness: security, concurrency, failure recovery, audit, independent QE, owner acceptance.
Không làm Dashboard live trước khi xác minh data contract.

## 13. Kiểm thử/acceptance targets — CHƯA RUN
T01 task creation; T02 identity/capability; T03 delivery receipt; T04 authenticated ACK; T05 session continuity; T06 Host execution; T07 out-of-scope denial; T08 concurrent edit; T09 retry idempotency; T10 lost connection; T11 revoke; T12 handoff; T13 independent review; T14 evidence hash/provenance; T15 Dashboard source correctness; T16 source drift; T17 Core unavailable/stale projection; T18 recovery.
PASS chỉ khi có source revision, environment, input/expected/actual, action/log, exit code, artifacts/hash, executor và independent reviewer. Chưa có bằng chứng thì NOT_VERIFIED, không PASS.

## 14. Bất đồng/điều chỉnh
- Không dùng một state machine chung cho mọi lifecycle.
- Không dùng Meeting làm task authority.
- session_ref không chứng minh session active.
- Không mặc định Core API đã tồn tại chỉ vì Core được chỉ định là authority.
- Dashboard không tự ghi trạng thái/acceptance.
- Không mở Peer-to-Peer unrestricted.
- Không triển khai đồng thời mọi adapter.

## 15. Quyết nghị kiến nghị
Xu tổng hợp các ý kiến đa AI và bất đồng; trình Vinh quyết định. Chỉ sau khi Vinh phê duyệt, biên bản/quyết định đúng thẩm quyền được phát hành, Work Entry/G0–G5 và assignment/scope được đáp ứng mới xem xét mở thi công.
Không có nội dung nào trong tài liệu này là quyết định triển khai.

## 16. Trạng thái
CONSULTATION SUBMITTED — WAITING FOR XU SYNTHESIS AND VINH FINAL DECISION.
