# KT-118-009 — KẾ HOẠCH KIỂM THỬ BỔ SUNG (VÒNG NGHIỆM THU ĐỘC LẬP)

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Ngày:** 2026-11-20
- **Phạm vi:** chỉ lập bằng chứng và truy vết; KHÔNG sửa mã trong vòng nghiệm thu (theo phương án của Xu).
- **Người thực hiện:** Xu kiểm thử độc lập; Vibe hỗ trợ lên lịch và ghi hồ sơ.

## 1. Danh sách test bổ sung
| ID | Test | Cách thực hiện | Bằng chứng mong đợi | Ghi đè gap |
|---|---|---|---|---|
| T-01 | handoff-brief runtime | tạo issue test, gắn label w118-handoff | comment bot hướng dẫn nhận việc xuất hiện | AC-R2 |
| T-02 | ack anti-spoof (không đáng tin) | từ tài khoản khác, comment ACKED-test | v1 vẫn ghi nhận (đúng thiết kế pilot) — kết quả dùng làm căn cứ đề xuất role-file v1.2 | AC-R1 |
| T-03 | actor mapping | Xu đối chiếu login thực thi với bảng vai trò Work | bản ghi xác nhận/không xác nhận kèm tên mapping | AC-R1 |
| T-04 | ci-failure-diagnostics | re-run thủ công Run #1 (FAILED cũ) hoặc khởi tạo runs thật có FAIL có kiểm soát | issue diagnostics w118-blocked được tạo/cập nhật 1 lần | AC-R3 + AC-R4 |
| T-05 | W118 tự lắng nghe FAIL của mình | đề xuất thêm workflow W118 vào danh sách workflows của workflow_run (sau vòng test, cần ACK riêng) | bằng chứng diagnostic khi chính pilot FAIL | AC-R4 |
| T-06 | PR và Evidence register | đối chiếu nội dung w118-coordination-ci.yml (PR #66) vs w118-workflow-automation.yml (main) | bảng so sánh tính năng, đề nghị 1 nguồn sự thật | AC-R5 + AC-R6 |

## 2. Quy tắc vòng kiểm thử
- Không push code thay đổi gì trong vòng này (workflow/templates/evidence script).
- Mọi kết quả ghi Entry mới của NHAT-KY-THI-CONG.md kèm run URL + SHA + kết quả.
- Khoanh vùng rủi ro trước khi đề sửa: nếu T-01..T-02 có kết quả không mong muốn, chỉ ghi observation, không rollback.
- Kết thúc vòng: cập nhật lại STATUS.md với trạng thái cuối mới rồi mới trình nghiệm thu lại.

## 3. Khối liên quan
- Run #2 đã ghi trong nhật ký Entry 008 (SUCCESS 6 giây).
- Run #1 FAIL (YAML L55) hiện được đánh giá: trước vòng test chỉ dùng làm bằng chứng "workflow validate hỏng — bots bị chặn trước khi thực thi", KHÔNG dùng chứng minh ci-failure-diagnostics.
