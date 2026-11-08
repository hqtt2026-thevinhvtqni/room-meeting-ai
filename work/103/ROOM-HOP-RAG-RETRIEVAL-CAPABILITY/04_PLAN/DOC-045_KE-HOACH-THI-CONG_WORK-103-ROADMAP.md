# KẾ HOẠCH THI CÔNG WORK 103 / WORK 103 IMPLEMENTATION ROADMAP
- **STT / Document ID:** DOC-045
- **Priority:** P0
- **Read order:** 7
- **Depends on:** DOC-001; DOC-034
- **Status:** ACTIVE — REBASELINE REQUIRED
- **Version / Updated:** 1.0 / 2026-11-08
- **Owner:** Xu / AI-01
- **Authority:** Vinh

# KẾ HOẠCH THI CÔNG — WORK 103
- **Chủ trì kế hoạch nguồn:** Xu — AI-01
- **Ngày cập nhật nguồn:** 2026-10-26 (UTC+07:00)
- **Trạng thái nguồn:** ACTIVE

| Gate kỹ thuật nguồn | Đầu việc | Phụ trách nguồn | Điều kiện cần | Điều kiện đủ / bằng chứng theo nguồn | Trạng thái tại kế hoạch cũ |
|---|---|---|---|---|---|
| G0 | Đối soát manifest, kiến trúc, code và test từ Sandbox | Xu | Sandbox Work 103 đọc được | Các file nguồn được đọc và đồng bộ lên branch | PASS cho đồng bộ file |
| G1 | Kiến trúc retrieval + ranh giới Core/MCP | Xu/Cla | Đọc Work Manifest và Work 28 contract | Tài liệu kiến trúc nêu luồng, quyền, abstention và gate vector DB | DONE tài liệu; chưa sign-off độc lập |
| G2 | Unit tests | Qc thực thi / Xu điều phối | Code và test có mặt trên branch | Test runner chạy thành công; lưu log và exit code | BLOCKED theo kế hoạch nguồn |
| G3 | Evaluation baseline | Qc thực thi / Qw kiểm thử | Eval set có nhãn, metric định nghĩa trước | Baseline và ablation tái lập trên cùng corpus fingerprint | BLOCKED theo kế hoạch nguồn |
| G4 | Tích hợp MCP/Core | Cla kiến trúc; Qc code; Qw QA | Contract Core được đối soát với Work 28 | E2E MCP → Core → retrieval, gồm positive/negative authorization và citation readback | CHƯA THỰC HIỆN |
| G5 | Handoff | Xu | G2–G4 có bằng chứng | Hồ sơ bàn giao, các gate và giới hạn rõ ràng | PENDING |

## Bước tiếp theo ghi trong kế hoạch nguồn
1. Chạy unit tests trên đúng commit và lưu stdout/stderr, exit code, timestamp.
2. Chuẩn hóa evaluation set, xác minh metric.
3. Chạy kiểm thử âm tính: query rỗng, top_k không hợp lệ, nguồn ngoài allowlist, file không hỗ trợ, prompt injection và trường hợp không có bằng chứng.
4. Đối soát Work 28 contract trước khi thay đổi MCP/Core production code.
5. Chỉ chuyển trạng thái khi đủ bằng chứng.

## Quy tắc quản trị cập nhật
Bảng trên là ảnh chụp kế hoạch lịch sử ngày 2026-10-26, không phải trạng thái hiện tại. Kế hoạch hiện hành phải được tái lập theo Work Package register và lifecycle gates G0–G9 của Work 70. Không được hiểu CI PASS của các suite hiện có là tích hợp ROOM-HOP PASS hoặc Release PASS.
