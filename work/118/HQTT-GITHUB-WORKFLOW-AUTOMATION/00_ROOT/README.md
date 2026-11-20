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

## 7. Liên kết
- GitHub Issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/65
- Work 70 — Product Lifecycle & Work Dashboard: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/tree/main/work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD

## 8. Điều kiện chuyển giai đoạn
Điều kiện lịch sử trước BUILD: hoàn thiện Biên bản kiến trúc/thiết kế, phản biện và Vinh phê duyệt. Điều kiện này đã được Vinh thay thế bằng quyết định ủy quyền BUILD ngày 2026-11-20 cho Ka. Xu vẫn giữ quyền phản biện/ nghiệm thu độc lập và Vinh giữ nghiệm thu cuối; không bỏ qua kiểm soát bảo mật, bằng chứng, hoặc gate phát hành.


## Amendment — Owner authorization to BUILD (2026-11-20)

Vinh explicitly authorized Ka to decide the Auto E2E system architecture and continue implementation on GitHub through the acceptance handoff. Xu and Vinh retain independent and final acceptance authority. This decision supersedes the earlier planning-only phase restriction for W118 implementation; it does not waive security controls, independent review, evidence requirements or release gates.

Current implementation branch: `work/118-auto-e2e-v2`, created from canonical `main` SHA `41e8397600505d94434b5830e7aea1a012db77a2`. The earlier PR #66 remains unmerged and is not the implementation base.

Current phase: **BUILD / VERIFY — ACTIVE, NOT RELEASED**.


## Current implementation snapshot — 2026-11-20

- **PR:** [#67](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/67), OPEN / mergeable / not merged.
- **Branch:** `work/118-auto-e2e-v2`, synchronized with Main; 0 commits behind.
- **Latest verified CI:** [Run #44758133788](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44758133788), 52 unit/contract tests PASS; artifact ID `14639616906`.
- **Security hardening:** trusted review policy checkout, W118-only ACK scope, separate owner acceptance/independent review permissions, role-map schema 1.1, explicit review evidence provenance, owner-authorized direct fault injection, and diagnostics idempotency across closed Issues.
- **Review:** Xu Stage A pending; Vinh Stage B non-release integration authorization pending.
- **Runtime:** real handoff/ACK/review/diagnostics event E2E has not run; PR synchronize jobs skip event-specific workflows.
- **State:** ACTIVE — BUILD / VERIFY — NOT RELEASED.
