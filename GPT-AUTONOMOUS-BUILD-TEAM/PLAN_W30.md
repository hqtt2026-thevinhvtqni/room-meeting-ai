# WORK 30 — BẢNG PLAN / KẾ HOẠCH HỢP NHẤT

- Work ID: 30
- Chủ trì kế hoạch: Xu — Planner
- Chủ dự án / người phê duyệt: Vinh
- Ngày khởi tạo: 2026-10-17 (UTC+7)
- Trạng thái tổng thể: ACTIVE — kế hoạch hợp nhất chưa được phê duyệt
- Branch GitHub dự kiến: `work/30-gpt-autonomous-build-team`
- Đây là bảng plan song song; chưa có đồng bộ tự động được xác minh với Sandbox.

## A. Cổng và trình tự

| ID | Công việc | Chủ trì | Đầu vào | Đầu ra / bằng chứng cần có | Trạng thái |
|---|---|---|---|---|---|
| W30-P01 | Kiểm tra hiện trạng Sandbox, GitHub branch, runtime và tài liệu | Cla / Go / Qe / Vibe độc lập | Cùng brief W30-PLAN-REQ-002 | Nguồn đã đọc, kết quả, lỗi đọc, đường dẫn/commit | PENDING |
| W30-P02 | Nộp bốn đề xuất độc lập trước khi đọc bản của nhau | Cla / Go / Qe / Vibe | W30-PLAN-REQ-002 | Bốn file proposal + bằng chứng đọc lại + ACK | PENDING — dispatch/ACK chưa xác minh |
| W30-P03 | So sánh và hợp nhất kế hoạch | Xu | Bốn proposal đã xác minh | Plan hợp nhất, bảng đồng thuận/bất đồng, blocker và quyết định cần Vinh | BLOCKED — chờ proposal |
| W30-P04 | Phê duyệt phạm vi và kiến trúc | Vinh | Plan hợp nhất | Quyết định APPROVE / REVISE / REJECT được ghi lại | BLOCKED — chờ W30-P03 |
| W30-P05 | Thi công E2E tự chủ | Nu | Plan được Vinh phê duyệt | Build report, mã nguồn, log runtime và bằng chứng đầu-cuối | NOT STARTED — cấm build trước phê duyệt |
| W30-P06 | Sửa lỗi theo defect ID | Vi | Defect có tái hiện và bằng chứng | Patch có phạm vi, test trước/sau, commit | NOT STARTED |
| W30-P07 | Kiểm thử độc lập | An | Build candidate + test plan | Kết quả unit/integration/security/real E2E và log | NOT STARTED |
| W30-P08 | Phản biện đối kháng độc lập | Cla | Kết quả test của An và candidate đóng băng | Challenge report: lỗ hổng, edge cases, thiếu bằng chứng | NOT STARTED |
| W30-P09 | Review độc lập | Ka | Candidate, test evidence, challenge report và xử lý phát hiện | Review report và quyết định | NOT STARTED |
| W30-P10 | Handoff theo bằng chứng | Xu | Toàn bộ bằng chứng và quyết định | DONE / PASS / DECISION / BLOCKED, known gaps, hướng dẫn vận hành | NOT STARTED |

## B. Yêu cầu kiểm thử cho kế hoạch hợp nhất
1. Unit tests (kiểm thử đơn vị) cho hợp đồng dữ liệu, state machine, router và path safety.
2. Integration tests (kiểm thử tích hợp) qua các ranh giới ROOM-HOP, có kiểm tra lỗi và timeout.
3. Real E2E (đầu-cuối thật) qua MCP → Core → Workspace; không dùng mock để tuyên bố runtime thật.
4. Negative/security tests (kiểm thử lỗi và bảo mật): đường dẫn ngoài sandbox, command allowlist bypass, secrets, identity/permission, giả mạo ACK, bằng chứng thiếu hoặc sai.
5. Regression tests (kiểm thử hồi quy) cho lỗi đã phát hiện.
6. Mỗi test ghi lệnh chạy, môi trường, thời điểm, exit code, kết quả, artifact và commit/source revision.

## C. Tiêu chí nghiệm thu dự kiến — cần được plan hợp nhất xác nhận
- Bốn proposal độc lập có thể truy cập và được đọc lại.
- Mọi task có ID, recipient, ACK thực tế, trạng thái và bằng chứng; file xuất hiện không thay thế ACK.
- Không build trước phê duyệt của Vinh.
- Real E2E đi hết luồng ROOM-HOP được xác nhận bằng log và artifact truy vết được.
- Security negative tests và regression tests đạt; mọi ngoại lệ đều ghi rõ.
- An, Cla và Ka tạo ba báo cáo độc lập theo đúng thứ tự cổng.
- Không còn blocker P0/P1 chưa có quyết định xử lý.
- Có hướng dẫn triển khai, rollback và handoff đủ để tái chạy.

## D. Quy tắc quyết định và dừng
- DONE: hành động đã hoàn tất và có bằng chứng.
- PASS: tiêu chí kiểm thử cụ thể đạt với bằng chứng.
- DECISION: cần quyết định của Vinh.
- BLOCKED: thiếu quyền, đầu vào, công cụ, ACK hoặc bằng chứng.
- Sau hai lần sửa không hiệu quả cùng một defect: dừng vá lặp, phân tích nguyên nhân gốc.
- Thay đổi kiến trúc/phạm vi trọng yếu phải xin Vinh duyệt.
- Đây là kế hoạch khung ban đầu, chưa phải kế hoạch cuối được phê duyệt. Xu sẽ hợp nhất lại sau khi có đủ bốn proposal.
