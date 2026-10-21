# KẾ HOẠCH THI CÔNG — XU — WORK 50

- Work ID: 50
- Chủ sở hữu / người quyết định: Vinh
- Chủ kế hoạch / điều phối: Xu (AI-01)
- Ngày lập: 2026-10-20 (UTC+07:00)
- Trạng thái: PLAN RECORDED — chưa nghiệm thu

## Mục tiêu
Xây dựng, kiểm chứng và trình phê duyệt tiêu chuẩn APDS để các Work phát triển sản phẩm CNTT/AI có cấu trúc, quy trình, trách nhiệm và bằng chứng nhất quán.

## Quy trình bắt buộc
READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.

## Các giai đoạn và cổng nghiệm thu

### G0 — Initiation / Khởi tạo
Đầu ra:
- Product/Work charter, mục tiêu, phạm vi, người quyết định.
- Danh sách nguồn, phụ thuộc, rủi ro ban đầu.
- Hồ sơ điều hành chính thức và nhật ký.
Gate: mục tiêu, chủ sở hữu, phạm vi và quyền hạn được xác định.

### G1 — Discovery / Khám phá bài toán
Đầu ra:
- Problem statement, người dùng, quy trình hiện tại.
- Giá trị kinh doanh, giới hạn phạm vi, giả định.
- Chỉ số thành công và cách đo.
Gate: bài toán và kết quả mong đợi có thể kiểm tra.

### G2 — Requirements / Yêu cầu
Đầu ra:
- Yêu cầu chức năng và phi chức năng.
- Yêu cầu hành vi AI, dữ liệu, tích hợp, quyền hạn.
- Tiêu chí nghiệm thu gắn từng yêu cầu.
Gate: yêu cầu có thể truy vết và kiểm thử; tiêu chí chưa rõ phải ghi OPEN/BLOCKED.

### G3 — Architecture / Kiến trúc
Đầu ra:
- Sơ đồ ngữ cảnh hệ thống và thành phần.
- Hợp đồng API/dữ liệu, luồng quyền hạn.
- Quyết định kiến trúc, mô hình đe dọa, triển khai và phục hồi.
Gate: có phương án được người có thẩm quyền xem xét; rủi ro và phụ thuộc trọng yếu được ghi nhận.

### G4 — Build / Phát triển
Đầu ra:
- Kế hoạch chia việc, nhánh, review, CI.
- Code/config/tài liệu theo phạm vi đã duyệt.
- Unit test và contract test khi phù hợp.
Gate: thay đổi có review và có thể tái lập; không được tự mở rộng phạm vi.

### G5 — Verify / Kiểm chứng
Đầu ra:
- Kế hoạch kiểm thử và kết quả.
- AI evaluation (đánh giá AI) trên tập dữ liệu/case đã duyệt.
- Kiểm thử chức năng, tích hợp, E2E, bảo mật, hiệu năng và phục hồi theo rủi ro.
- Danh sách lỗi, bằng chứng, tiêu chí đạt/chưa đạt.
Gate: từng tiêu chí được đánh dấu PASS/FAIL/BLOCKED/CHƯA XÁC MINH dựa trên bằng chứng cụ thể.

### G6 — Release / Phát hành
Đầu ra:
- Release checklist, phiên bản, cấu hình và quyền truy cập.
- Kế hoạch triển khai, rollback (quay lui), backup và restore.
- Phê duyệt phát hành của người có thẩm quyền.
Gate: mọi điều kiện bắt buộc đã đạt; không bỏ qua gate bằng cách đổi nhãn trạng thái.

### G7 — Operate & Handoff / Vận hành và bàn giao
Đầu ra:
- Runbook, hướng dẫn người dùng, giám sát, cảnh báo và xử lý sự cố.
- Chủ sở hữu vận hành, chi phí, lịch bảo trì và chính sách dữ liệu.
- Danh sách giới hạn đã biết và các việc còn mở.
Gate: người nhận bàn giao xác nhận trách nhiệm, quyền truy cập và bằng chứng.

## Quy tắc đánh giá sản phẩm AI Production
Đánh giá theo rủi ro và use case, ít nhất xem xét:
1. Functional correctness — đúng chức năng.
2. AI quality — chất lượng đầu ra trên bộ đánh giá đã duyệt.
3. Tool/agent reliability — độ tin cậy khi gọi công cụ và thực hiện workflow.
4. Safety & security — an toàn, bảo mật, phân quyền, chống lộ dữ liệu.
5. Data governance — nguồn, quyền sử dụng, lưu giữ, xóa và backup.
6. Performance & availability — độ trễ, thông lượng và tính sẵn sàng.
7. Cost control — chi phí theo tác vụ/phiên/sản phẩm.
8. Observability — log, metrics, trace, correlation ID khi áp dụng.
9. Recovery — backup/restore, rollback và xử lý sự cố.
10. Reproducibility — phiên bản model, prompt, config, code và bộ test.
11. Human oversight — chuyển người xử lý, phê duyệt thao tác rủi ro.
12. Release & ownership — người chịu trách nhiệm và điều kiện bàn giao.

Không đặt một ngưỡng số chung cho mọi sản phẩm. Chủ sản phẩm phải đề xuất ngưỡng có căn cứ; người có thẩm quyền phê duyệt trước khi kiểm thử.

## Quy tắc bằng chứng
Mỗi bằng chứng cần có khi phù hợp:
- Evidence ID; Product/Work/Task ID; Requirement ID.
- Người/AI thực hiện và vai trò.
- Ngày giờ UTC+07:00.
- Loại bằng chứng, đường dẫn/link, phiên bản/commit/model/config.
- Lệnh kiểm tra, exit code, log hoặc artifact.
- Kết quả, reviewer và hash khi cần bảo đảm toàn vẹn.

Commit không tự chứng minh test đã PASS. Log riêng lẻ không tự chứng minh E2E hoàn chỉnh.

## Vai trò đề xuất
- Product Owner: xác định vấn đề, giá trị và phạm vi; Vinh là người quyết định cuối cùng.
- Planner/Architect: phân rã công việc, phụ thuộc, kiến trúc và kế hoạch.
- Coder/Builder: thực hiện thay đổi trong quyền hạn.
- QE/QA: thiết kế/chạy kiểm thử độc lập với người xây dựng khi khả thi.
- Reviewer/Security Reviewer: phản biện thiết kế, code, rủi ro và bằng chứng.
- Release/Operations Owner: phát hành, theo dõi, phục hồi và nhận bàn giao.
- Approver: quyết định cuối cùng theo phân quyền; không tự gán PASS thay cho bằng chứng.

## Quản lý Work và thay đổi
Mỗi Work cần ghi: ID, tên, mục tiêu, phạm vi, Work cha/Product ID, người phụ trách, người test/review/phê duyệt, trạng thái, deliverables, tiêu chí nghiệm thu, phụ thuộc, rủi ro, bằng chứng và lịch sử thay đổi.

Luồng thay đổi: đề xuất → phân tích tác động/phụ thuộc/rủi ro → phê duyệt → thực hiện → kiểm thử → cập nhật bằng chứng và phiên bản. Thay đổi liên quan dữ liệu, bảo mật, kiến trúc, API hoặc quyền công cụ phải được đánh giá lại.

## Việc theo thứ tự ưu tiên
1. G0: xác minh Work 50 trong Sandbox và đối chiếu hồ sơ GitHub.
2. G1: rà soát APDS v1.0 và các tiêu chí nghiệm thu.
3. G2: chọn sản phẩm mẫu; xác định use case và rủi ro.
4. G3: lập bản đồ yêu cầu ↔ tiêu chí ↔ test ↔ evidence.
5. G4: chạy đánh giá thử; ghi lỗi và đề xuất sửa tiêu chuẩn.
6. G5: reviewer độc lập xem xét kết quả.
7. G6: trình Vinh quyết định phê duyệt/sửa/từ chối.
8. G7: nếu được duyệt, phát hành phiên bản chuẩn và kế hoạch rollout từng Work.

## Ràng buộc
- Không merge vào main khi chưa có phê duyệt riêng.
- Không tự sửa Protected Core hoặc baseline frozen.
- Không tuyên bố Sandbox/GitHub đồng bộ nếu chưa đọc lại và so sánh.
- Tất cả hoạt động quan trọng phải ghi vào NHAT_KY_HOP_THI_CONG.md.

## Bổ sung phạm vi — Dashboard AI theo từng Work (2026-10-21)

Mục tiêu: chuẩn hóa mô hình dashboard dùng chung để mỗi Work có một dashboard riêng theo dõi tiến độ, vai trò AI, deliverables, blocker, reviewer và evidence.

Thứ tự triển khai:
1. DONE tài liệu: tạo `01_STANDARD/WORK_AI_DASHBOARD_MODEL_v1.0.md` và `02_TEMPLATES/WORK_AI_DASHBOARD_TEMPLATE.md`.
2. Cập nhật checklist APDS: APDS-20 đến APDS-23; các mục vẫn CHƯA XÁC MINH cho tới khi review/kiểm thử thực tế.
3. Review cấu trúc dashboard hiện có trong ROOM-HOP trước khi chọn tái sử dụng hay xây mới; không tạo dashboard runtime trùng lặp.
4. Chọn Work 50 làm pilot read-only MVP trên GitHub, hiển thị rõ branch/revision nguồn và trạng thái Sandbox/MCP là chưa xác minh nếu chưa truy cập được.
5. Kiểm thử UI/API và truy vết từ summary đến role → task → deliverable → evidence; kiểm tra DONE/PASS, thiếu dữ liệu, lỗi nguồn và xung đột.
6. Sau MCP phục hồi, thêm Sandbox như nguồn thứ hai ở chế độ đọc/đối chiếu trước; chỉ xây sync có kiểm soát sau khi có diff/conflict/approval flow.

Không tuyên bố dashboard đã chạy thật: hiện mới hoàn thành tài liệu mô hình và template trên GitHub. Chưa tạo UI/API/runtime.
