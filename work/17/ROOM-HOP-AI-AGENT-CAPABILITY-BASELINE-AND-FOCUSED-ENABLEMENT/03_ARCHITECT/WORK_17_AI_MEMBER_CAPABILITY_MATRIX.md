# MA TRẬN NĂNG LỰC AI MEMBER — WORK 17 (G2)

- Work ID: 17 · Ngày lập: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Nguồn khai báo: DOC-010 AI Identity Register v1.1 (W0000/.../AI_TEAM_AND_TOKEN_USAGE.md) — chỉ đạt cấp E0, không phải bằng chứng runtime (theo tiêu chí ở 02_DEFINE).
- Thông tin trạng thái ban đầu được lấy từ Journal Entry 002 (ngày 2026-11-19).

## Ma trận (khung bắt buộc điền)

| Member | Trạng thái nhật ký hiện tại | Identity/session | Dispatch/ACK | Quyền & policy | Tool/provider | Execution | Evidence ghi nhận | Token telemetry | Xung đột cần xử lý |
|--------|------------------------------|------------------|--------------|----------------|---------------|-----------|--------------------|-----------------|--------------------|
| AI-01 (Xu / coordinator) | Đang hoạt động ghi journal W17 | UNASSESSED | CHƯA chứng minh private-session delivery/ACK | UNASSESSED | UNASSESSED | UNASSESSED | Journal W17 (E0/E1) | NOT_AVAILABLE | — |
| AI-02 … AI-05 | Roster TODC-010 khai báo | NOT VERIFIED (phần lớn, theo DOC-010 tự nhận) | TO ĐƯỢC chứng minh | Required DOC-043 role matrix đối soát import | UNASSESSED | UNASSESSED | — | NOT_AVAILABLE | — |
| AI-06 | Roster khai báo | NOT VERIFIED | TO ĐƯỢC chứng minh | UNASSESSED | UNASSESSED | UNASSESSED | — | NOT_AVAILABLE | Mapping conflict DOC-010 |
| AI-07 | Roster khai báo | NOT VERIFIED | TO ĐƯỢC chứng minh | UNASSESSED | UNASSESSED | UNASSESSED | — | NOT_AVAILABLE | Mapping conflict DOC-010 |
| AI-08 | Roster khai báo | NOT VERIFIED | TO ĐƯỢC chứng minh | UNASSESSED | UNASSESSED | UNASSESSED | — | NOT_AVAILABLE | Mapping conflict DOC-010 |

## Quy tắc điền bổ sung

1. Mỗi ô phải điền bằng trạng thái taxonomy (RUNTIME_VERIFIED / NOT_VERIFIED / CONFLICT ...) + cấp evidence (E0–E4) + đường dẫn bằng chứng; cấm điền "Có".
2. Điền xong phải đọc lại ngược về nguồn (DOC-010, DOC-043 AI-ROLE-PERMISSION-MATRIX, journal các Work dispatch).
3. Ma trận này là điều kiện bắt buộc để chốt G2; ô nào thiếu evidence câm giữ NOT_VERIFIED.
4. Khi có dispatch/ACK thật lần đầu tiên (GAP-01), cập nhật cả DOC-010 version mới, ghi Decision Log (DOC-006), không ghi đè nhật ký cũ.

## Định nghĩa chấp nhận bảng này (G2 exit criteria)

- 100% member có trạng thái identity/session + dispatch/ACK reconciliation rõ ràng.
- 100% ô mang link evidence hoặc nhãn NOT_VERIFIED/UNASSESSED.
- Mọi xung đột (GAP-05, GAP-09) được chốt quyết định của Vinh trước khi xây GAP khác lên trên.
