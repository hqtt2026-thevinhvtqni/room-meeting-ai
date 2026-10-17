> **QUY ĐỊNH BẮT BUỘC — KHAI BÁO NGƯỜI THAM DỰ**
> - Mỗi AI/người tham gia phải ghi rõ **tên/identity, chức danh/vai trò, thời điểm tham gia hoặc thời điểm nghe Xu (UTC+7)**.
> - Khi Xu phổ biến yêu cầu, người nhận phải ghi nhận thời điểm đã nghe/đọc chỉ thị và xác nhận bằng ACK tường minh; không được suy diễn là đã nghe chỉ vì có tên trong danh sách.
> - Mẫu ghi nhận: `[YYYY-MM-DD HH:mm:ss UTC+7] — [Tên AI/người] — [Chức danh] — Đã nghe/đọc chỉ thị của Xu — ACK: [ACK/NACK/CHƯA XÁC NHẬN]`.
> - Thư ký phải cập nhật mục tham dự/ACK trong biên bản. Nếu không có bằng chứng, ghi `CHƯA XÁC NHẬN`, không ghi nhận là đã tham dự.
> - Người ghi biên bản: Xu — Planner / Điều phối — thời điểm cập nhật: 2026-10-17 22:20:16 UTC+7.
>
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

## 7. Nội dung xây dựng Plan — yêu cầu ghi nhận trong biên bản

Xu điều phối lập kế hoạch theo các cổng sau; đây là kế hoạch khung, chưa được xem là phê duyệt thi công:

1. **Khảo sát và truy vết:** kiểm tra Sandbox, nhánh GitHub Work 30, mã nguồn, cấu hình và bằng chứng runtime; ghi rõ nguồn nào đọc được/không đọc được.
2. **Lập kế hoạch độc lập:** Cla, Go, Qe, Vibe cùng nhận brief W30-PLAN-REQ-002; mỗi AI nộp proposal riêng, không đọc proposal của người khác trước khi nộp.
3. **Giao việc và ACK:** mỗi task phải có task ID, người nhận, vai trò, thời điểm nghe/nhận chỉ thị, ACK tường minh, đường dẫn đầu ra và bằng chứng đọc lại. Tệp xuất hiện không thay thế ACK.
4. **Hợp nhất:** Xu so sánh bốn đề xuất, tách sự thật đã chứng minh khỏi giả thuyết, ghi rõ điểm đồng thuận/bất đồng, blocker và quyết định cần Vinh.
5. **Phê duyệt:** Vinh phê duyệt hoặc yêu cầu sửa kế hoạch hợp nhất. Không triển khai code trước khi có phê duyệt.
6. **Thi công:** Nu phụ trách vòng xây dựng đầu-cuối; Vi xử lý defect có mã định danh và bằng chứng; sau hai lần sửa không hiệu quả cùng lỗi phải dừng vá lặp để phân tích nguyên nhân gốc.
7. **Xác minh độc lập:** An kiểm thử; Cla phản biện đối kháng sau An; Ka review độc lập sau cổng Cla. Phải có unit, integration, real E2E qua MCP → Core → Workspace, security-negative và regression evidence.
8. **Bàn giao:** Xu kết luận DONE / PASS / DECISION / BLOCKED; nêu rõ phạm vi đã xác minh, phần còn thiếu, hướng dẫn tái chạy và rollback.

### Tiêu chí không được bỏ qua
- Không có bằng chứng thì ghi NOT VERIFIED/BLOCKED, không tự nhận PASS.
- Không được ghi AI đã nghe Xu hoặc ACK nếu chưa có bằng chứng tường minh.
- Sandbox và GitHub là hai nguồn riêng cho đến khi có bằng chứng đồng bộ.
- Bảng kế hoạch theo dõi tại `GPT-AUTONOMOUS-BUILD-TEAM/PLAN_W30.md`; kế hoạch hiện chưa được Vinh phê duyệt.
