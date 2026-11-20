# B-118-010 — PLAN REMEDIATION SẴN SÀNG CHO 6 GAP (áp dụng SAU vòng kiểm thử)

- **Work:** W118
- **Ngày:** 2026-11-20
- **Ràng buộc:** KHÔNG áp dụng trong vòng nghiệm thu độc lập của Xu (theo đề nghị NOT ACCEPTED 2026-11-20 + phê duyệt Issue #65); chỉ soạn sẵn để áp ngay khi vòng test đóng.

## R-X (fix cho từng AC-R)
| Gap | Fix | File đích | Trạng thái soạn |
|---|---|---|---|
| AC-R1 | ack job kiểm tra mapping role: nếu env không kèm actor hợp lệ trong danh sách xác thực trước -> chỉ comment cảnh báo "ACK UNVERIFIED", không ghi evidence row OPERATION | w118-workflow-automation.yml | CHƯA — chờ đối chiếu role-file thật từ Xu (T-03) |
| AC-R2 | test bằng tay T-01 khi label tồn tại; nếu cần tự-tạo label thì thêm step ensure-label như luồng block | đã xác minh được khi Xu thực hiện | CHỜ T-01 |
| AC-R3 | chính w118-workflow-automation thêm listener tự FAIL của mình (workflow_run cho "W118 Workflow Automation Pilot") | w118-workflow-automation.yml | SOẠN ĐƯỢC — thêm 1 value workflows + filter conclusion |
| AC-R4 | gộp cùng fix AC-R3: mọi workflow-run failure bất kỳ ai (kể cả W118) đều tạo diagnostics | w118-workflow-automation.yml | SOẠN ĐƯỢC |
| AC-R5 | quyết canonical theo TD-118-011; PR #66 không merge nguyên trạng | PR #66 | ĐỀ XUẤT ĐÃ GHI |
| AC-R6 | pilot v2: evidence row JSON ghi vào register theo schema v1.2 khi W70 ACK; trước đó evidence ghi dạng memory + diagnostics issue | w118 + Work 70 register | CHỜ ACK v1.2 |

## Điều kiện áp dụng
- Xu kết thúc vòng test với báo cáo Entry mới + đóng register gap.
- Vinh ACK "APPLY B-118-010" rõ ràng trên Issue #65 (do ngữ cảnh freeze đang mở).
- Có thể áp dụng từng fix một theo thứ tự AC-R3 -> AC-R4 -> AC-R1 -> AC-R5 -> AC-R6 để evidence từng bước rõ ràng.
