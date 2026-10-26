# KẾ HOẠCH THI CÔNG — WORK 103

- **Chủ trì kế hoạch:** Xu — AI-01, GPT CEO / Quân sư LAB
- **Ngày cập nhật:** 2026-10-26 (UTC+07:00)
- **Trạng thái tổng:** ACTIVE
- **Nguyên tắc:** READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF

| Gate | Đầu việc | Phụ trách | Điều kiện cần | Điều kiện đủ / bằng chứng | Trạng thái |
|---|---|---|---|---|---|
| G0 | Đối soát manifest, kiến trúc, code và test từ Sandbox | Xu | Sandbox Work 103 đọc được | Các file nguồn được đọc và đồng bộ lên branch | PASS: commit đồng bộ được trả về |
| G1 | Kiến trúc retrieval + ranh giới Core/MCP | Xu/Cla | Đọc Work Manifest và Work 28 contract | Tài liệu kiến trúc nêu luồng, quyền, abstention và gate vector DB | DONE: tài liệu đã đồng bộ; chưa sign-off kiến trúc độc lập |
| G2 | Unit tests | Qc thực thi / Xu điều phối | Code và test có mặt trên branch | Test runner chạy thành công; lưu log và exit code | BLOCKED: chưa có log chạy test từ môi trường hiện tại |
| G3 | Evaluation baseline | Qc thực thi / Qw kiểm thử | Eval set có nhãn, metric định nghĩa trước | Baseline và ablation tái lập trên cùng corpus fingerprint | BLOCKED: số liệu trong phiên shell khác chưa được đồng bộ/đối soát vào branch |
| G4 | Tích hợp MCP/Core | Cla chủ trì kiến trúc; Qc code; Qw QA | Contract Core được đối soát với Work 28 | E2E MCP → Core → retrieval, gồm positive/negative authorization và citation readback | CHƯA THỰC HIỆN |
| G5 | Handoff | Xu | G2–G4 có bằng chứng | Hồ sơ bàn giao, các gate và giới hạn rõ ràng | PENDING |

## Bước tiếp theo
1. Chạy lại unit tests trên đúng commit của branch, lưu stdout/stderr, exit code và thời điểm UTC+07:00.
2. Chuẩn hóa evaluation set, xác minh metric không bị đánh lừa bởi việc mọi gold source cùng đứng hạng 1.
3. Chạy kiểm thử âm tính: query rỗng, top_k không hợp lệ, nguồn ngoài allowlist, file không hỗ trợ, dữ liệu prompt-injection, không có bằng chứng.
4. Đối soát Work 28 contract trước khi thay đổi bất kỳ MCP/Core production code nào.
5. Chỉ chuyển sang DONE sau khi đủ bằng chứng các gate được yêu cầu; hiện chưa tuyên bố DONE.
