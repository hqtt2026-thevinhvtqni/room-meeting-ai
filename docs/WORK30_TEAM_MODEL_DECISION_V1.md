# WORK 30 — TEAM MODEL DECISION V1

Status: DECISION RECORDED / EXECUTION NOT VERIFIED

## W30-DEC-007 — Vinh thống nhất mô hình đội AI Work 30
Ngày ghi nhận: 2026-10-17 (UTC+07:00; không tự suy diễn giờ-phút nếu chưa có timestamp hệ thống)
Người xác nhận: Vinh
Người ghi nhận: Xu — Planner

DECISION:
Vinh xác nhận thống nhất mô hình đội AI Work 30 về mặt thiết kế/quy trình.

MÔ HÌNH ĐÃ THỐNG NHẤT:
1. PLAN: Claude (Cla) và Grok (Go) đề xuất độc lập qua Sandbox; Qwen (Qe) và Vibe đề xuất độc lập qua GitHub. Xu tổng hợp thành một Plan duy nhất, chỉ ra điểm đồng thuận/khác biệt/rủi ro và trình Vinh phê duyệt trước khi thi công.
2. BUILD: Nu là Autonomous Coder thi công toàn trình; Vi là Repair Coder xử lý lỗi theo defect ID và bằng chứng.
3. TEST: An kiểm thử độc lập theo tiêu chí nghiệm thu.
4. CHALLENGE: Cla phản biện độc lập khi sản phẩm gần hoàn thành, sau kiểm thử của An và trước Ka review; phát hiện phải có bằng chứng, mức độ nghiêm trọng và điều kiện xác minh.
5. REVIEW: Ka review độc lập, xem xét cả bằng chứng E2E, báo cáo An, phát hiện/đóng lỗi của Cla và các rủi ro còn lại.
6. HANDOFF: Xu tổng hợp trạng thái DONE/PASS/DECISION/BLOCKED dựa trên bằng chứng, trình Vinh quyết định.

GATES:
- Không thi công trước khi Vinh phê duyệt Plan.
- Không tự xác nhận PASS; thiếu bằng chứng là BLOCKED/NOT VERIFIED.
- Mọi nhiệm vụ phải có task ID, người nhận rõ ràng, timestamp, ACK thực tế và bằng chứng đầu ra.
- Sau hai lần sửa không thành công cùng một lỗi, dừng vá lặp và quay lại phân tích nguyên nhân/Plan.
- Ka vẫn phải tự review; Cla không thay thế Ka. Cla không thay thế An và không tự xác nhận việc sửa lỗi của chính mình.

TRẠNG THÁI:
DECISION RECORDED — mô hình được thống nhất về mặt thiết kế.
Implementation/dispatch to all agents, recipient ACKs, multi-vendor independent proposals, and full E2E operation are NOT VERIFIED until direct evidence is captured.
