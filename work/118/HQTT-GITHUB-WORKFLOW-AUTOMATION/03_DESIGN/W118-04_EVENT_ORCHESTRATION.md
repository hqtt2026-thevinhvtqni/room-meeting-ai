# W118-04 — THIẾT KẾ EVENT ORCHESTRATION (ROOM-HOP)

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện

## 1. Ràng buộc môi trường thực tế (từ Work 103)

- GitHub connector hiện có KHÔNG có tool Actions/Webhooks — chỉ đọc/push file, đọc Issue/PR/kết quả CI.
- Bảo mật: KHÔNG thiết lập branch protection, secrets, credentials (cam kết Entry 002).
- Do đó: **POLLING-DRIVEN ROOM-HOP** là phương án khả thi ngay; webhook thật BLOCKED (chờ W118-09 sau G3, kèm phê duyệt secret riêng).

## 2. Mô hình Polling → Event → Actor → Action

1. `list_issues` theo `status/queued` → nhận việc (đổi label `status/in-progress` + comment "đã nhận" kèm evidence timestamp).
2. Tạo branch `work/<số>` → thực thi theo acceptance criteria của Issue.
3. Đọc kết quả CI qua trang commit-checks (không cần auth) — trả lời câu hỏi #4 BB-118-001: đủ, không phụ thuộc token.
4. Issue labels làm **hàng đợi trạng thái** thay event push (xử lý Gap #1 trong phạm vi khả thi hiện tại).

## 3. Ma trận Event → Actor → Action → Permission → Result

| Event | Actor | Action | Permission | Result |
|---|---|---|---|---|
| Issue tạo + `status/queued` | Vibe/ROOM-HOP | Đổi label, comment nhận việc | issue write | Event log |
| Branch + push | Vibe | Commit theo W118-02 | contents write | Commit SHA ghi evidence |
| CI PASS | Vibe | Ghi evidence, đổi `status/in-review` | issue write | Evidence entry |
| CI FAIL (không intentional) | Vibe | Tạo/gắn sub-issue `type/fix`, `status/failed-ci`, link run | issue write | Diagnostic entry (idempotent) |
| CI FAIL (intentional debt) | Vibe | KHÔNG sinh fix-issue; chỉ cập nhật evidence | issue write | Debt register link |
| Review phê duyệt | Ka/Xu/Vinh (độc lập) | `status/accepted`, merge qua PR | merge | Entry nghiệm thu |
| Dashboard sync | ROOM-HOP/Vibe | Đọc EVIDENCE_REGISTER + labels → Work Journal | contents write | Dashboard state |

## 4. Giới hạn đã ghi

- Không có push realtime GitHub → ROOM-HOP (webhook); ghi là `limitation` trong W118-08. Nếu cần realtime trong pilot phải đi qua GitHub App/secret và được phê duyệt riêng.
