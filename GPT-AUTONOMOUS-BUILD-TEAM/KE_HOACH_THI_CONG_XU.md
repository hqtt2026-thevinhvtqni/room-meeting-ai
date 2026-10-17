# KẾ HOẠCH THI CÔNG — WORK 30 (E2E — AUTOMATIC)

- Work ID: 30 — GPT-AUTONOMOUS-BUILD-TEAM
- Chủ trì kế hoạch: Xu — Planner / Điều phối (bản kế hoạch điều hành theo quy trình AGENTS.md §06)
- Người thực thi phiên này: Agent VS Code — Engineering Operations (đọc và xây dựng phương án **độc lập**, không đọc đề xuất của AI khác trước khi nộp)
- Ngày khởi tạo bản thi công: 2026-10-17 (UTC+7)
- Chế độ vận hành: **E2E — AUTOMATIC** (toàn trình trong một phiên: READ → TRACE → ANALYZE → BUILD → VERIFY → HANDOFF)
- Branch thi công: `work/30-gpt-autonomous-build-team`
- Trạng thái kế hoạch: ĐÃ LẬP — thi công tự chủ đã thực hiện ở chế độ "không phá vỡ cam kết hợp đồng"; các hạng mục cần quyết định phạm vi được ghi DECISION, không tự ý làm.

## 0. Căn cứ và giới hạn quyền

1. Read theo Context Contract (AGENTS.md §05.1): AGENTS.md → PROJECT_STATE.md → XU_CORE.md → XU_SESSION.md → meetings/ → XU_MEMORY.md. Đã đọc đủ trước khi hành động.
2. Quyết định nền: W30-DEC-004 (Plan loop), W30-DEC-005 (Nu/Vi), W30-DEC-007 (mô hình đội), cổng phản biện Cla, yêu cầu W30-PLAN-REQ-001/002.
3. Kỷ luật bằng chứng: file write ≠ ACK; thiếu bằng chứng = BLOCKED/NOT VERIFIED; không tự nhận PASS.
4. Không sửa Protected Core (`XU_CORE.md`, `XU_MEMORY.md`) — không có CORE_EDIT_AUTH. Không xóa bằng chứng lịch sử.
5. Ràng buộc quan trọng phát hiện được khi trace: **Plan hợp nhất chưa được Vinh phê duyệt chính thức** (BIEN_BAN_W30 §7 ghi rõ "kế hoạch khung, chưa được xem là phê duyệt thi công"). Do đó phiên E2E-Automatic này chỉ thực hiện phần **không xung đột với gate**: khảo sát, truy vết, proposal độc lập, kiểm kê bằng chứng, sửa các lỗi môi trường/reproducible không chạm ranh giới kiến trúc, và đóng băng ứng viên bàn giao. Mọi việc thay đổi phạm vi hợp đồng công khai (MCP tools, maxLength schema) để lại dưới dạng DECISION.

## 1. Đầu việc và phụ thuộc

| ID | Đầu việc | Phụ trách | Phụ thuộc | Tiêu chí nghiệm thu | Bằng chứng cần có |
|---|---|---|---|---|---|
| T-01 | Đọc context + kiểm kê hồ sơ Work 30 (Sandbox mirror `30/`, GitHub `GPT-AUTONOMOUS-BUILD-TEAM/`, docs/) | Agent (role Nu) | — | Nêu được vị trí bản chính thức ba hồ sơ, trạng thái mirror | Mục "Current-state trace" trong proposal |
| T-02 | Truy vết runtime: môi trường Python, dependencies, chạy toàn bộ regression suite | Agent (Nu) | T-01 | Có danh sách test pass/fail kèm lệnh chạy và exit code | Log pytest lưu tại `06_EVIDENCE`/tệp evidence, đường dẫn ghi trong Nhật ký |
| T-03 | Phân tích 4 test fail, tách nguyên nhân: lỗi portability môi trường vs lỗi thiết kế chưa triển khai vs thiếu công cụ | Agent (Nu) | T-02 | Mỗi defect có ID, tái hiện, expected/actual, suspected cause | Defect register trong proposal + Nhật ký |
| T-04 | Sửa defect W30-DEF-001 (hard-code `python.exe` trong adapter/test W13) theo hướng smallest safe fix, giữ Windows-compat | Agent (Vi-scope) | T-03 | `tests/test_work13_wee_integration.py` PASS trên Linux và không regress trên Windows | Diff commit + pytest output |
| T-05 | Nộp đề xuất lập kế hoạch độc lập theo format W30-PLAN-REQ (A→M) | Agent (planner GitHub channel) | T-01..T-04 | Proposal đầy đủ 13 mục, mọi claim gắn nhãn VERIFIED/INFERRED/UNKNOWN | `docs/work30/plan-proposals/` + ACK mẫu trong Nhật ký |
| T-06 | Chạy xác minh lại toàn trình sau sửa (regression + targeted) | Agent (Nu) | T-04 | Suite chạy sạch trừ các lỗi đã ghi nhận là DECISION/BLOCKED có chủ đích | Log verify cuối kỳ |
| T-07 | Đóng băng candidate, ghi bảng trạng thái DONE/PASS/DECISION/BLOCKED, cập nhật ba hồ sơ điều hành | Agent + Xu governance | T-06 | Nhật ký có mốc kết thúc, PLAN_W30 cập nhật cột trạng thái, không có PASS ảo | Commit SHA + readback |
| T-08 | Bàn giao cho Vinh: các quyết định cần duyệt (phạm vi MCP tools, F4 maxLength, dispatch/ACK hạ tầng) | Xu | T-07 | Danh sách DECISION rõ ràng, mỗi cái có phương án và hệ quả | Mục "Decisions needed from Vinh" |

## 2. Phụ trách kênh đề xuất (theo W30-PLAN-REQ-002)

- Qe (Qwen) — kênh GitHub: `docs/work30/plan-proposals/QWEN_PLAN_PROPOSAL.md` ← agent này nộp tại đây (identity-bound tự khai, ACK tự ghi theo mẫu).
- Vibe — kênh GitHub: `docs/work30/plan-proposals/VIBE_PLAN_PROPOSAL.md` — CHƯA XÁC MINH (không có mặt trong phiên này).
- Cla, Go — kênh Sandbox: các đường dẫn `.../PLAN_PROPOSALS/` — BLOCKED/NOT VERIFIED (endpoint Sandbox không khả dụng trong môi trường làm việc này).

## 3. Ghi chú chống phân tán hồ sơ (§06)

- Bản chính thức ba hồ sơ điều hành Work 30 hiện hành: `GPT-AUTONOMOUS-BUILD-TEAM/BIEN_BAN_W30.md`, `GPT-AUTONOMOUS-BUILD-TEAM/PLAN_W30.md`, `GPT-AUTONOMOUS-BUILD-TEAM/NHAT_KY_THI_CONG_W30.md` (nhánh `work/30-gpt-autonomous-build-team`).
- Thư mục số `30/GPT-AUTONOMOUS-BUILD-TEAM/` là mirror cấu trúc, README của nó tự khai "not yet a complete byte-for-byte mirror" — giữ nguyên, không tạo bản Biên bản/Kế hoạch/Nhật ký thứ hai.
- Báo cáo kỹ thuật (proposal, log test) là bằng chứng riêng, được liên kết từ Nhật ký, không thay thế ba hồ sơ trên.

## 4. Bước tiếp theo ngay sau phiên này

1. Xu hợp nhất bốn proposal (hiện mới có 1/4 có artifact trong repo này) → trình Vinh phê duyệt Plan hợp nhất.
2. Sau phê duyệt: Nu build theo Plan đã duyệt; Vi xử lý defect còn mở; An/Cla/Ka chạy ba cổng độc lập.
3. Hạ tầng Sandbox read/dispatch cần repair riêng (defect W30-DEF-004) trước khi tuyên bố kênh A hoạt động.

[Signed: XU — PLAN OWNER / bản thi công lập theo ủy quyền quy trình §06]
