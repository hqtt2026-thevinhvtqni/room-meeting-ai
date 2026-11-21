# WORK 118 — HQTT GITHUB WORKFLOW AUTOMATION

**Tên tiếng Việt:** Tự động hóa quy trình GitHub và điều phối thực thi HQTT AI  
**Tên tiếng Anh:** HQTT GitHub Workflow Automation  
**Mã Work:** W118  
**Issue chính:** [#65](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65)  
**Trạng thái:** ACTIVE — BUILD / VERIFY (OWNER AUTHORIZED)  
**Phạm vi hiện tại:** Xây dựng và kiểm chứng Auto E2E v2 trên branch riêng; runtime event E2E và nghiệm thu còn chờ gate.

## 1. Mục tiêu
Kết nối Issue → Assignment → Branch → Commit/Push → CI → Failure handling hoặc Review → Acceptance → Merge → Work Journal/Dashboard thành một luồng có thể truy vết và điều phối được.

## 2. Vấn đề cần giải quyết
Issue và Push hiện có thể tồn tại như các hoạt động riêng lẻ. Chưa có bằng chứng về một cơ chế end-to-end bảo đảm sự kiện GitHub kích hoạt đúng tác nhân, đúng hành động, cập nhật trạng thái và lưu bằng chứng.

## 3. Nguyên tắc
- Một nguồn sự thật cho mỗi loại tài liệu; mọi trạng thái phải có bằng chứng.
- CI PASS chỉ xác nhận các job đã cấu hình chạy đạt; không thay thế review hoặc nghiệm thu.
- CI FAIL phải tạo đường xử lý có giới hạn, có người/AI phụ trách và không retry vô hạn.
- Không tự động merge chỉ vì CI PASS.
- Mọi mutation phải có actor identity, quyền tối thiểu, provenance, idempotency và audit log.
- Không giả lập tích hợp. Thiếu quyền, API contract hoặc runtime evidence thì ghi BLOCKED.
- Work 70 là chuẩn vòng đời và Dashboard; W118 thiết kế cơ chế GitHub/ROOM-HOP để hiện thực hóa, không tạo quy trình Work trùng lặp.

## 4. Phạm vi hệ thống
GitHub Issues, Branches, Commits, Pull Requests, GitHub Actions, Webhooks/API, ROOM-HOP coordinator, Work Journal, Evidence và Dashboard.

## 5. Ngoài phạm vi giai đoạn đầu
Không tự ý thay đổi branch protection, secrets/tokens, quyền tổ chức, tự động merge production hoặc triển khai diện rộng trước khi có kiến trúc được duyệt và thử nghiệm giới hạn.

## 6. Các giai đoạn
1. DISCOVER: kiểm kê workflow, quyền, event, CI, API và cách các Work đang vận hành.
2. DEFINE: chốt yêu cầu, trạng thái, actor, quyền, bằng chứng và tiêu chí.
3. ARCHITECT: thiết kế event-driven flow, idempotency, retry, security và audit.
4. PLAN: chia Work Packages và kế hoạch thử nghiệm.
5. BUILD: triển khai theo phê duyệt.
6. VERIFY: kiểm thử end-to-end, lỗi, lặp sự kiện, quyền và truy vết.
7. ACCEPT: review độc lập và nghiệm thu.
8. OPERATE: theo dõi vận hành, sự cố và cải tiến.

## 7.1 Kiến trúc hai quy trình khép kín Sandbox–GitHub (BUILD BASELINE — OWNER AUTHORIZED)

- [TD-118-012 — Kiến trúc hai quy trình khép kín Sandbox–GitHub](../02_DEFINE/TD-118-012_KIEN-TRUC-HAI-QUY-TRINH-KHEP-KIN-SANDBOX-GITHUB.md)
- [W118-13/16 — Task Lifecycle & Source Binding implementation](../05_BUILD/W118-13_16_TASK-LIFECYCLE-AND-SOURCE-BINDING.md)
- [W118-13/16 — Test Matrix](../06_TEST/W118-13_16-TASK-LIFECYCLE-SOURCE-BINDING-TEST-MATRIX.md)
- [DC-118-004 — Brief phản biện kiến trúc (tham khảo, không chặn BUILD)](../02_DEFINE/DC-118-004_BRIEF-PHAN-BIEN-KIEN-TRUC-HAI-QUY-TRINH.md)
- Nhật ký: Entry 069 trong [NHAT-KY-THI-CONG.md](../EVIDENCE/NHAT-KY-THI-CONG.md)

## 7. Liên kết
- GitHub Issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65
- Work 70 — Product Lifecycle & Work Dashboard: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/tree/main/work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD

## 8. Điều kiện chuyển giai đoạn
Điều kiện lịch sử chờ phản biện đã được thay thế bởi chỉ thị trực tiếp của Vinh ngày 2026-11-21: Xu tự quyết định kỹ thuật và BUILD theo phương án A, không cần chờ Ka/Cla/Qw phản biện. Xu chịu trách nhiệm thiết kế, triển khai, kiểm thử và ghi nhật ký; Vinh giữ quyền nghiệm thu sản phẩm, merge và release. Không bỏ qua kiểm soát bảo mật, identity, quyền, bằng chứng hoặc gate phát hành.


## Amendment — Owner authorization to BUILD (2026-11-20)

Vinh explicitly authorized Ka to decide the Auto E2E system architecture and continue implementation on GitHub through the acceptance handoff. Xu and Vinh retain independent and final acceptance authority. This decision supersedes the earlier planning-only phase restriction for W118 implementation; it does not waive security controls, independent review, evidence requirements or release gates.

Current implementation branch: `work/118-auto-e2e-v2`, created from canonical `main` SHA `41e8397600505d94434b5830e7aea1a012db77a2`. The earlier PR #66 remains unmerged and is not the implementation base.

Current phase: **BUILD / VERIFY — ACTIVE, NOT RELEASED**.


## Current implementation snapshot — 2026-11-20

- **PR:** [#67](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/67), OPEN / mergeable / not merged.
- **Branch:** `work/118-auto-e2e-v2`, synchronized with Main; 0 commits behind; 220 commits ahead.
- **Latest verified CI:** [Run #44758608904](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44758608904), 52 unit/contract tests PASS; artifact ID `14638958067`.
- **Security hardening:** trusted review policy checkout, W118-only ACK scope, separate owner acceptance/independent review permissions, role-map schema 1.1, explicit review evidence provenance, owner-authorized direct fault injection, and diagnostics idempotency across closed Issues.
- **Review:** Xu Stage A pending; Vinh Stage B non-release integration authorization pending.
- **Runtime:** real handoff/ACK/review/diagnostics event E2E has not run; PR synchronize jobs skip event-specific workflows.
- **State:** ACTIVE — BUILD / VERIFY — NOT RELEASED.


## Scope reconciliation and product acceptance boundary — 2026-11-21

The product objective in Issue #65 is broader than Auto E2E validation alone. The full lifecycle includes Issue Management, AI Assignment and verified ACK, Execution Tracking, Issue–Branch–Commit–Push binding, CI feedback, Work Journal/Evidence, and Work 70 Dashboard projection.

- **Current disposition:** W118-10 Auto E2E is a partial automation layer, not proof of the complete Work Management product.
- **Required reconciliation:** [RA-118-001 — Scope comparison and completion plan](../04_PLAN/RA-118-001_BANG-DOI-CHIEU-PHAM-VI-VA-KE-HOACH-HOAN-THIEN.md), Priority P0 / Read order 12.
- Proposed W118-13..W118-19 remain pending Xu independent review; no new Work is created.
- GitHub Assignee, ACK, execution-start, CI result, Work acceptance and release are separate states.
- Work 70 remains the source of truth for the Work Dashboard; W118 must not create a second Dashboard or mutate its schema without approval.


## Owner directive — proceed without multi-agent review (2026-11-21)

Vinh instructed Xu to proceed with building the two closed-loop Sandbox–GitHub workflows according to Xu's technical judgment, without waiting for multi-agent consultation. TD-118-012 is the owner-authorized build baseline. Implementation remains incremental on `work/118-auto-e2e-v2`; no rebase, merge to main, release, permission/secret/branch-protection change, or Work 70 schema mutation is authorized by this directive. Final product acceptance remains with Vinh.


## Build progress — W118-13 / W118-16 (2026-11-21)

- Sandbox Task Registry and state-transition contract implemented in `scripts/w118/task_lifecycle.py`.
- GitHub push source-binding validator implemented in `scripts/w118/source_binding.py` and wired into the W118 push validation workflow.
- Exact-head validation at `5e131e108a7195ca1ff5ae96b3fadb119e4bc31b`: 86 tests PASS; push and PR validate jobs SUCCESS. Artifact ID `14696186741`.
- Current push branch is an aggregate legacy branch, so source binding reports `UNBOUND_LEGACY_BRANCH` and does not infer a Task. Task-specific push runtime test is pending.
- Agent dispatch/verified ACK, GitHub Issue mirror, Sandbox API deployment, CI-to-Task reconciliation and Work 70 projection remain NOT IMPLEMENTED / NOT VERIFIED.
