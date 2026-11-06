# DOC-002 — DISCOVER BRIEF / BÁO CÁO KHÁM PHÁ

## Problem statement
ROOM-HOP cần một cơ chế kích hoạt AI thống nhất. Các nhu cầu hiện có gồm lịch định kỳ, sự kiện từ hệ thống/GitHub, điều kiện ngưỡng, lệnh thủ công và sự kiện vòng đời Work. Nếu mỗi Work tự tạo scheduler hoặc trigger riêng, sẽ phát sinh trùng lặp, thiếu audit, không nhất quán về quyền và khó quan sát.

## User and system outcomes
- Người quản trị khai báo Trigger một lần, theo dõi được trạng thái và lịch sử.
- AI chỉ nhận nhiệm vụ sau khi sự kiện hợp lệ, điều kiện đúng và policy cho phép.
- Có thể tạm dừng, vô hiệu hóa, mô phỏng và truy vết từng lần chạy.
- Dashboard cho thấy trigger nào đã đăng ký, điều kiện nào được đánh giá, kết quả dispatch/ACK và bằng chứng.

## Trigger taxonomy
- TIME: kích hoạt theo lịch.
- EVENT: kích hoạt bởi sự kiện đã xác thực.
- CONDITION: kích hoạt khi biểu thức đạt điều kiện.
- MANUAL: kích hoạt theo lệnh đã xác thực.
- COMPOSITE: kết hợp nhiều nguồn/điều kiện, chỉ triển khai sau khi semantics được chốt.

## Discovery questions
1. Event sources nào là authoritative và có webhook/polling contract?
2. Core identity, Work/WP authorization và audit API nào sẽ được dùng?
3. AI dispatch transport nào có thật, hỗ trợ receipt/ACK ra sao?
4. Trigger cần độ trễ, throughput, retention và availability mục tiêu nào?
5. Những action nào bắt buộc human approval?
6. Quy tắc timezone, daylight-saving, retry, dedupe và replay?
7. Trigger configuration versioning và rollback được quản lý thế nào?

## Constraints
- Không giả định private-session dispatch đã tồn tại.
- Không tự suy diễn AI ID từ display name.
- Không tin payload từ bên ngoài nếu chưa xác thực chữ ký/nguồn.
- Không để event payload chứa prompt injection điều khiển policy hoặc cấp quyền.
- Không chạy protected action nếu authorization/audit không sẵn sàng.

## Discovery status
DRAFT / evidence collection pending. Danh sách câu hỏi trên chưa được xem là đã giải quyết.
