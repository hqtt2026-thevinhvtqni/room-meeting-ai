# WORK 10 — SAFETY POLICY

**Status:** LOCKED (Specification)
**Owner:** Work 10 — COMPUTER-AGENT
**Last update:** 2026-10-04

---

## 1. Purpose

Safety Policy bảo vệ hệ thống, dữ liệu và người dùng khỏi hành vi không kiểm soát của Agent.

Mọi action và workflow **phải** tuân thủ policy này trước khi thực thi.

---

## 2. Retry Policy

| Loại                | Giới hạn mặc định | Ghi chú                              |
|---------------------|-------------------|--------------------------------------|
| Action-level retry  | tối đa 2 lần      | Chỉ retry lỗi transient (timeout, network) |
| Workflow-level retry| tối đa 1 lần      | Chỉ khi recovery được khai báo rõ    |
| Infinite retry      | **CẤM**           | Phải fail hoặc BLOCKED               |

- Retry phải có backoff (tối thiểu 500ms).
- Sau khi hết retry → chuyển sang FAIL hoặc BLOCKED.

---

## 3. Timeout Policy

| Phạm vi             | Timeout mặc định | Hành vi khi vượt |
|---------------------|------------------|------------------|
| Single action       | 30 giây          | FAIL action      |
| Wait action         | theo `value` (max 120s) | FAIL        |
| Entire workflow     | 10 phút          | BLOCKED          |
| Observation / extract | 15 giây        | FAIL             |

Timeout phải được ghi vào evidence.

---

## 4. Destructive Actions Policy

Các action được coi là **destructive** (cần policy riêng):

- Xóa file / folder
- Mua hàng / thanh toán
- Thay đổi tài khoản / mật khẩu / quyền
- Gửi email / tin nhắn ra ngoài
- Download / upload file nhạy cảm
- Đóng session quan trọng

### Quy tắc:

1. Destructive action **phải** được khai báo rõ trong workflow (`"destructive": true`).
2. Runtime phải kiểm tra policy trước khi thực thi.
3. Nếu không có explicit allow → **REJECT / BLOCKED**.
4. Mọi destructive action phải được log đầy đủ vào evidence.

---

## 5. Boundary Policy (Screenshot / Extract / Download)

- `screenshot`, `extract`, `download` **chỉ được phép** trong phạm vi Work hiện tại.
- Không được:
  - Chụp / trích xuất dữ liệu ngoài domain được phép
  - Lưu file ra ngoài sandbox của Work
  - Gửi dữ liệu quan sát ra bên ngoài mà không qua channel chính thức
- Observation data mặc định chỉ tồn tại trong session + evidence của Work.

---

## 6. Target Resolution Safety

- Target phải resolve được một cách deterministic.
- Nếu target mơ hồ (nhiều element khớp) → FAIL hoặc yêu cầu disambiguation.
- Không được dùng fuzzy matching nguy hiểm cho destructive action.

---

## 7. Failure Handling

Khi vi phạm Safety Policy:

- Action → `status: blocked` hoặc `fail`
- Workflow → chuyển sang **BLOCKED**
- Ghi rõ lý do trong evidence (`policy_violation: ...`)

---

## 8. Principle

> Agent autonomy ≠ unlimited authority  
> Safety Policy là lớp bảo vệ cao hơn quyền tự quyết của Agent.

---

## 9. Versioning

Policy này là **LOCKED**.  
Mọi nới lỏng (tăng retry, bỏ destructive check...) phải được review và cập nhật WORK_MANIFEST.
