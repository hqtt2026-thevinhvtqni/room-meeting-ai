# BIÊN BẢN — WORK 103: ROOM-HOP-RAG-RETRIEVAL-CAPABILITY

- **Người điều phối:** Xu — AI-01, GPT CEO / Quân sư LAB
- **Chủ quyền quyết định:** Vinh
- **Ngày cập nhật:** 2026-10-26 (UTC+07:00)
- **Trạng thái:** ACTIVE — chưa nghiệm thu toàn trình

## Phạm vi đã thống nhất
1. Xây Retrieval Capability có truy vết nguồn cho ROOM-HOP; không tạo Core thứ hai, không dựng RAG Layer độc lập.
2. Giữ Core :8000 là nguồn sự thật duy nhất; MCP :8020 là cổng công cụ, không truy cập kho dữ liệu trực tiếp; Dashboard :3000 chỉ render.
3. Bắt đầu với lexical retrieval và metadata rõ ràng. Chỉ thêm embedding/vector database khi tập đánh giá chứng minh có lợi ích đáng kể.
4. Đoạn trích truy xuất là dữ liệu không đáng tin cậy; không thực thi chỉ dẫn nhúng trong tài liệu. Không đủ bằng chứng thì phải abstain (từ chối kết luận do thiếu bằng chứng).

## Quyết định ghi nhận ngày 2026-10-26
- Tiếp tục tự chủ PLAN → BUILD → VERIFY → HANDOFF, không chờ sign-off cho các bước nằm trong phạm vi.
- Đồng bộ những tài sản có thể đọc lại từ Sandbox Work 103 lên đúng branch GitHub.
- Không coi kết quả baseline cục bộ là bằng chứng của tích hợp MCP/Core.
- Chưa sửa context/PROJECT_STATE.md trong đợt đồng bộ này; trạng thái Work được ghi tại hồ sơ Work để tránh tuyên bố toàn dự án đã thay đổi.

## Gate nghiệm thu
- G1: kiến trúc và hợp đồng retrieval được ghi nhận.
- G2: unit tests được chạy, log/exit code được lưu.
- G3: bộ đánh giá có nhãn và baseline tái lập được, có kiểm tra âm tính và trường hợp không có bằng chứng.
- G4: tích hợp qua MCP → Core → retrieval service được chạy E2E với quyền truy cập và citations.
- G5: handoff có trạng thái, commit, giới hạn và bước tiếp theo.

**Quy tắc:** Không có bằng chứng chạy thực tế thì không đánh dấu PASS. Hoàn thành tài liệu/code trong Sandbox không đồng nghĩa đã tích hợp production.
