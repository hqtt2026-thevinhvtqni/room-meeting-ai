# APDS — CHECKLIST NGHIỆM THU WORK 50

Trạng thái mặc định của từng mục: CHƯA XÁC MINH. Chỉ đánh PASS khi có bằng chứng kiểm tra phù hợp.

| ID | Tiêu chí | Bằng chứng cần có | Trạng thái |
|---|---|---|---|
| APDS-01 | Có charter, mục tiêu, phạm vi và authority boundary | Hồ sơ + quyết định | CHƯA XÁC MINH |
| APDS-02 | Có cấu trúc tài liệu sản phẩm tham chiếu | APDS_STANDARD_v1.0.md | CHƯA XÁC MINH |
| APDS-03 | Có lifecycle và gate G0–G7 | Tiêu chuẩn + review | CHƯA XÁC MINH |
| APDS-04 | Có vai trò, RACI/phân quyền và trách nhiệm nghiệm thu | Mô hình vai trò + review | CHƯA XÁC MINH |
| APDS-05 | Có tiêu chí kiểm thử phần mềm và AI | Test strategy + AI evaluation plan | CHƯA XÁC MINH |
| APDS-06 | Có bảo mật, quản trị dữ liệu và kiểm soát công cụ | Policy/threat model/checklist | CHƯA XÁC MINH |
| APDS-07 | Có tiêu chí hiệu năng, độ tin cậy và kiểm soát chi phí | Metrics/thresholds theo use case | CHƯA XÁC MINH |
| APDS-08 | Có phát hành, rollback, backup/restore và incident response | Runbook/release checklist | CHƯA XÁC MINH |
| APDS-09 | Có evidence contract và traceability yêu cầu–test–evidence | Evidence schema + traceability sample | CHƯA XÁC MINH |
| APDS-10 | Có change control và quản lý phiên bản | Change workflow + decision record | CHƯA XÁC MINH |
| APDS-11 | Có template charter và hồ sơ Work chính thức | Template + ba hồ sơ điều hành | CHƯA XÁC MINH |
| APDS-12 | Thử nghiệm trên ít nhất một sản phẩm mẫu | Kế hoạch, kết quả, lỗi và evidence | CHƯA XÁC MINH |
| APDS-13 | Có review độc lập và giải quyết nhận xét | Review record | CHƯA XÁC MINH |
| APDS-14 | Vinh phê duyệt hoặc yêu cầu sửa đổi | Quyết định rõ ràng | CHƯA XÁC MINH |
| APDS-15 | Sandbox/GitHub được đối chiếu; không tuyên bố sync nếu chưa có evidence | Đọc lại và so sánh hồ sơ | CHƯA XÁC MINH |

## Quy tắc kết luận
- Work 50 chỉ có thể được kết luận nghiệm thu theo từng gate; không suy ra toàn bộ APDS PASS từ việc đã tạo tài liệu.
- APDS chỉ được triển khai bắt buộc toàn HQTT sau quyết định phê duyệt của Vinh.
- Mục chưa có evidence phải giữ CHƯA XÁC MINH hoặc BLOCKED.

| APDS-16 | Có danh mục vai trò AI dùng chung và liên kết từ APDS | AI_ROLE_CATALOG_v1.0.md + tham chiếu trong APDS | CHƯA XÁC MINH |
| APDS-17 | Sản phẩm mẫu có ma trận phân công AI, trách nhiệm, quyền hạn, đầu ra và tiêu chí nghiệm thu | Ma trận phân công được review | CHƯA XÁC MINH |
| APDS-18 | Khi MCP lỗi, công việc độc lập vẫn có thể tiếp tục trên GitHub và được ghi log | Commit, nhật ký và trạng thái phụ thuộc | CHƯA XÁC MINH |
| APDS-19 | Sau khi MCP phục hồi, Sandbox/GitHub được đối chiếu trước khi đồng bộ, có kiểm tra đọc lại hai phía | Báo cáo diff/sync và bằng chứng đọc lại | CHƯA XÁC MINH |
