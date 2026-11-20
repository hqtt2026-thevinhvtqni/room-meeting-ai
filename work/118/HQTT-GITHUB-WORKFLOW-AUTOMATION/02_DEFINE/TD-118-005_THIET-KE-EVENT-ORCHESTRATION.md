# TD-118-005 — THIẾT KẾ EVENT ORCHESTRATION (W118-04)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT — chờ phản biện.

## 1. Ma trận sự kiện v1 (GitHub-native, không webhook)
| Sự kiện | Điều kiện | Hành động tự động | Actor chịu trách nhiệm |
|---|---|---|---|
| issue.opened + label handoff | label do người gán | workflow comment hướng dẫn nhận việc mới | Xu tổng hợp |
| issue_comment có magic-token | body đầu chứa "ACKED-<role> <số issue>" | tick nhận việc, ghi evidence row OPERATION | actor AI được mapping |
| pull_request.opened | title có mã Work | auto-gán checklist review độc lập | reviewer chỉ định |
| push trên main chạm path Work | có evidence-write job | ghi evidence row RUNTIME | bot evidence |
| workflow failure | bất kỳ job FAIL | diagnostics issue + label blocked theo TD-118-006 | actor pending |

Trong v1 KHÔNG có hoạt động mutation tự động nào khác; mọi mutation vẫn cần người/AI comment ACK kèm bằng chứng.

## 2. Xác thực nhận việc (trả lời câu hỏi 2 BB-118-001)
- Assignee GitHub chỉ là đề cử. Nhận việc chỉ có hiệu lực khi có comment magic-token ACKED-<ROLE> <so issue> từ chính actor AI (tạo bởi hệ thống của nó, không phải người gõ thay).
- Workflow nhận comment kiểm tra author + so với mapping role cố định trong file cấu hình docs của Work (role → github login), sau đó ghi evidence row OPERATION (state RECORDED). Không khớp thì chỉ cảnh báo, không tick.

## 3. Anti-spoof
- Token ACK chỉ hợp lệ khi comment do chính tác nhân tạo, hoặc được người đúng role trong mapping xác nhận lại ít nhất 1 lần trong cùng Work.
- V1 chọn phương án đơn giản: mapping role-file + người reviewer xác nhận role của GitHub login lần đầu xuất hiện.

## 4. Giới hạn v1
- ROOM-HOP không nghe realtime: state sync chỉ qua evidence register và Dashboard đọc từ đó.
- Event không có label/magic-token bị bỏ qua cố ý (fail-closed).
