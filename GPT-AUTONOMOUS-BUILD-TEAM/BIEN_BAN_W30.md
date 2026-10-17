# BIÊN BẢN WORK 30 — GPT-AUTONOMOUS-BUILD-TEAM

- Work ID: 30
- Người ghi: Xu — Planner / Điều phối
- Ngày: 2026-10-17 (UTC+7)
- Phiên bản: 1.0
- Mục đích: duy trì biên bản song song trên GitHub trong thời gian Sandbox và GitHub chưa đồng bộ tự động.
- Trạng thái: GitHub mirror (bản ghi song song); không tuyên bố đã đồng bộ với Sandbox.

## 1. Quyết định mô hình đội Work 30

1. Cla (Claude) và Go (Grok) lập kế hoạch độc lập qua Sandbox.
2. Qe (Qwen) và Vibe lập kế hoạch độc lập qua GitHub.
3. Xu tổng hợp bốn đề xuất thành một kế hoạch hợp nhất.
4. Anh Vinh phê duyệt kế hoạch hợp nhất trước khi triển khai.
5. Nu là Autonomous Coder (lập trình viên tự chủ), chịu trách nhiệm vòng xây dựng đầu-cuối.
6. Vi là Repair Coder (lập trình viên sửa lỗi), xử lý lỗi có mã định danh và bằng chứng.
7. An kiểm thử độc lập.
8. Cla thực hiện cổng phản biện đối kháng sau An và trước Ka.
9. Ka thực hiện review độc lập; không thay thế cổng phản biện của Cla.
10. Xu bàn giao kết luận theo bằng chứng và trạng thái DONE / PASS / DECISION / BLOCKED.

## 2. Quy tắc điều hành

- Quy trình: READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.
- Không triển khai trước khi anh Vinh phê duyệt kế hoạch hợp nhất.
- Không có bằng chứng thì ghi NOT VERIFIED hoặc BLOCKED, không tự nhận PASS.
- Tệp được tạo không đồng nghĩa người nhận đã ACK.
- Mỗi nhiệm vụ phải có task ID, người nhận, vai trò, thời điểm, ACK tường minh, đầu ra và bằng chứng đọc lại.
- Sau hai lần sửa không hiệu quả cho cùng một lỗi, dừng vá lặp và quay về phân tích nguyên nhân gốc.
- Thay đổi kiến trúc hoặc phạm vi trọng yếu cần anh Vinh quyết định.

## 3. Quyết định tổ chức GitHub

Work 30 được tổ chức trên nhánh riêng song song với Work 27/28, không dùng thư mục số `30/` trên main làm vị trí chính thức.

- Branch dự kiến: `work/30-gpt-autonomous-build-team`
- Ba tài liệu điều hành song song:
  - `GPT-AUTONOMOUS-BUILD-TEAM/BIEN_BAN_W30.md`
  - `GPT-AUTONOMOUS-BUILD-TEAM/NHAT_KY_THI_CONG_W30.md`
  - `GPT-AUTONOMOUS-BUILD-TEAM/PLAN_W30.md`

## 4. Yêu cầu lập kế hoạch độc lập

Task: `W30-PLAN-REQ-002`

Bốn AI Cla, Go, Qe, Vibe cần nộp đề xuất độc lập, có bằng chứng, kiến trúc, blocker, trình tự thi công, kế hoạch kiểm thử, tiêu chí nghiệm thu, rủi ro và rollback. Không đọc đề xuất của nhau trước khi nộp.

Nơi nộp:
- Cla: Sandbox `GPT-AUTONOMOUS-BUILD-TEAM/02_EXTENSION/PLAN_PROPOSALS/CLAUDE_PLAN_PROPOSAL.md`
- Go: Sandbox `GPT-AUTONOMOUS-BUILD-TEAM/02_EXTENSION/PLAN_PROPOSALS/GROK_PLAN_PROPOSAL.md`
- Qe: GitHub `docs/work30/plan-proposals/QWEN_PLAN_PROPOSAL.md` trên nhánh Work 30
- Vibe: GitHub `docs/work30/plan-proposals/VIBE_PLAN_PROPOSAL.md` trên nhánh Work 30

Mỗi người phải ACK theo định dạng:
`ACK — W30-PLAN-REQ-002 — [identity] — [role] — [timestamp UTC+7]`

## 5. Trạng thái tại thời điểm ghi

- Đã tạo yêu cầu lập kế hoạch trong Sandbox và kiểm tra thấy đường dẫn tồn tại.
- Đã ghi biên bản, nhật ký và transcript trong Sandbox.
- Chưa có bằng chứng xác nhận dispatch trực tiếp vào inbox và ACK của từng AI.
- Việc đồng bộ dữ liệu giữa Sandbox và GitHub chưa được xác minh.
- Tài liệu này là bản ghi song song trên GitHub; không được coi là bản sao đồng bộ tự động.

## 6. Nhật ký quyết định

| Ngày | Người thực hiện | Quyết định / hành động | Trạng thái |
|---|---|---|---|
| 2026-10-17 | Vinh / Chủ dự án | Yêu cầu có biên bản, nhật ký và bảng plan trên GitHub song song Sandbox | Đã tiếp nhận yêu cầu |
| 2026-10-17 | Xu / Planner | Chuẩn bị bộ ba tài liệu điều hành trên nhánh Work 30 | Đang tạo và xác minh |
