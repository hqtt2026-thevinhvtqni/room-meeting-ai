# DC-118-004 — BRIEF PHẢN BIỆN KIẾN TRÚC HAI QUY TRÌNH KHÉP KÍN SANDBOX–GITHUB

- **Work:** W118
- **Document ID:** DC-118-004
- **Tài liệu phản biện:** TD-118-012 — Sandbox–GitHub Dual Closed-Loop Architecture
- **Trạng thái:** CONSULTATION REQUEST — NOT APPROVED
- **Phương án được Vinh chọn:** A — Sandbox khởi phát, GitHub kiểm soát phiên bản
- **Ngày:** 2026-11-21 (UTC+07:00)

## 1. Mục tiêu xin ý kiến

Phản biện kiến trúc hai quy trình:
- A. Plan → WP → Task → Issue → Agent Assignment → Dispatch → ACK → Execute → Verify → Accept/Close.
- B. Sandbox → GitHub Branch/Commit/Push → CI → Sandbox Reconcile → PR/Review → Acceptance Gate.

Không xin triển khai code trong vòng phản biện này. Không thay đổi workflow, permission, token, branch protection, W70 schema, PR merge hoặc release.

## 2. Phạm vi ý kiến

| Reviewer | Trọng tâm | Câu hỏi cần trả lời |
|---|---|---|
| Ka — CSA / Build Lead | Tính khả thi và tương thích code hiện hữu | Phần nào tái sử dụng được? Gap nào thật sự cần WP mới? Contract nào xung đột với workflow/role-map hiện có? |
| Cla — CTO / Runtime & Security | Runtime architecture, event transport, trust boundary | Dispatch/ACK identity, webhook/API, replay, idempotency, lease, recovery và least privilege có khả thi không? |
| Qw — QE/QA | Test architecture và evidence | State transition, negative/security, race, retry, crash-window, lost event và Dashboard parity đã có đủ test không? |
| Xu — Independent Reviewer | Tổng hợp và phản biện độc lập | Kiến trúc có nhất quán, đủ an toàn, đo được và không lẫn CI PASS với acceptance không? |
| Vinh — Product Owner | Quyết định sản phẩm | Xác nhận ranh giới authority, acceptance, merge/release và ưu tiên triển khai. |

## 3. Mẫu phản hồi bắt buộc

Mỗi reviewer ghi:
1. **DECISION:** APPROVE / APPROVE WITH CONDITIONS / REVISE / BLOCKED.
2. **Findings:** mã phát hiện, mức P0/P1/P2, mô tả và tác động.
3. **Evidence:** file/path/line, code path, runtime/API evidence; nếu chưa có thì ghi NOT VERIFIED.
4. **Recommendation:** thay đổi cụ thể trong TD-118-012.
5. **Test gaps:** test ID cần thêm hoặc điều kiện test chưa khả thi.
6. **Authority/security:** principal, permission, trust boundary, owner decision còn thiếu.
7. **Implementation gate:** điều kiện tiên quyết trước khi code.

Không ghi PASS nếu chỉ đọc thiết kế; phân biệt DESIGN REVIEW với RUNTIME TEST.

## 4. Các điểm phải phản biện

- Sandbox Task Registry là nguồn chuẩn Task state; GitHub Issue là mirror — có ngoại lệ không?
- Agent Registry, capability matching, dispatch receipt, ACK nonce và runtime identity.
- Tách ASSIGNED / DISPATCHED / ACKED / STARTED / IN_PROGRESS / COMPLETED.
- Issue–Branch–Commit–Push binding và xử lý multi-task PR.
- GitHub event transport, duplicate/out-of-order/lost event, reconciliation.
- CI PASS/FAIL routing, exact SHA, retry cap và repair assignment.
- Journal/Evidence Register/W70 Dashboard ownership; không tự ý sửa W70 schema.
- Review / QE verification / Vinh acceptance / merge / release separation.
- Các error code, fail-closed behavior, test matrix và acceptance gates.

## 5. Quy tắc vòng phản biện

- Chỉ cập nhật hồ sơ tài liệu; không code.
- Mọi ý kiến phải được gắn reviewer, timestamp, document revision và evidence.
- Xu lập bảng disposition: ACCEPT / MODIFY / REJECT / DEFER cho từng đề xuất.
- Chỉ một bản TD-118-012 cuối cùng và một Biên bản kiến trúc được dùng làm nguồn chuẩn.
- Nếu còn blocker P0 hoặc authority chưa rõ, giữ DRAFT/BLOCKED; không mở BUILD.

## 6. Đầu ra cần bàn giao

- Phản biện riêng của Ka, Cla, Qw.
- Bảng tổng hợp và xử lý mâu thuẫn của Xu.
- Biên bản kiến trúc chính thức với decision IDs.
- Nhật ký thi công ghi toàn bộ đọc/trace/thiết kế/ý kiến/quyết định.
- Implementation plan theo WP, test plan và gate được duyệt.

**Kết luận:** DC-118-004 là yêu cầu phản biện kiến trúc, không phải giấy phép triển khai.
