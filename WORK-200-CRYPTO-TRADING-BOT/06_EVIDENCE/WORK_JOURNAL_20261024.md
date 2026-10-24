

## Entry 005 — Quyết định kiến trúc MT5 cho Work 200
- **Thời điểm:** 2026-10-24 (Asia/Ho_Chi_Minh; giờ phút chưa được xác nhận bởi công cụ).
- **Người ghi / điều phối:** Xu — AI-01, GPT CEO / Quân sư LAB.
- **Người nhận thực hiện:** Boai (đọc nhật ký này và tiếp tục công việc trong phạm vi Work 200).
- **Trạng thái:** DECISION — chốt hướng kiến trúc; chưa phải PASS triển khai hay nghiệm thu.

### Quyết định
1. Phát triển Work 200 theo hướng **Python làm bộ điều phối + MT5 Adapter làm lớp kết nối + Risk Engine làm cổng kiểm soát + Dashboard**. Giữ Paper Broker hiện có và thiết kế để có thể bổ sung adapter cho sàn crypto khác về sau.
2. Tách chiến lược khỏi broker/execution; chiến lược chỉ tạo tín hiệu. Mọi yêu cầu đặt lệnh phải đi qua Risk Engine và adapter thực thi.
3. Giai đoạn đầu chỉ Research / Backtest / Paper Trading. Nếu broker hỗ trợ sản phẩm crypto trên MT5 thì mới thử tích hợp MT5 Demo; không giả định CFD là coin sở hữu thật.
4. Không bật giao dịch tài khoản thật, không gửi lệnh thật, không yêu cầu hoặc lưu mật khẩu/API key trong Work Sandbox. Giao dịch thật chỉ được xem xét sau khi có bằng chứng kiểm thử, đạt tiêu chí nghiệm thu và được anh Vinh phê duyệt riêng.

### Nhiệm vụ cho Boai
1. Đọc `00_ROOT/WORK_MANIFEST.md`, `00_ROOT/PLAN_WORK200_v1.0.md`, `03_ARCHITECTURE/INITIAL_ARCHITECTURE_PLAN.md`, `05_TEST/ACCEPTANCE_CRITERIA.md`, `04_CODE/` và `02_EXTENSION/DASHBOARD_SCOPE_AND_INTEGRATION_PLAN.md` trước khi sửa.
2. Lập/cập nhật plan triển khai theo chuỗi READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF; ghi phạm vi, phụ thuộc, điều kiện cần và tiêu chí đủ nghiệm thu.
3. Thiết kế interface/protocol cho `BrokerAdapter`, `MT5Adapter` và `PaperBroker`; chuẩn hóa kết quả lệnh, trạng thái kết nối, symbol metadata, tick/ohlcv và lỗi. Không đưa logic chiến lược vào adapter.
4. Thực hiện kiểm tra cấu hình, kết nối và dữ liệu theo kiểu fail-closed: dữ liệu cũ/thiếu, mất kết nối, symbol không được hỗ trợ, spread bất thường hoặc kết quả API không hợp lệ thì không cho phép gửi lệnh.
5. Bổ sung Risk Engine tối thiểu: giới hạn khối lượng/notional, giới hạn lỗ ngày, giới hạn vị thế, SL/TP hợp lệ theo thông số symbol, spread guard, kill switch và kiểm soát trùng lệnh. Không được bỏ qua kiểm soát rủi ro từ bất kỳ đường gọi nào.
6. Nối Dashboard với backend qua API chỉ đọc trước; hiển thị timestamp, nguồn dữ liệu, trạng thái stale/disconnected, mode (`mock`/`paper`/`demo`), vị thế, PnL và trạng thái rủi ro. Loại bỏ mọi khả năng khiến nút UI giả vờ dừng engine; kill switch thực phải gọi backend và được xác nhận, nếu chưa tích hợp thì ghi rõ UI-only.
7. Viết unit tests và integration tests cho Paper Broker, adapter qua mock/fake terminal, validation, risk rejection, mất kết nối, dữ liệu stale, lỗi gửi lệnh và kill switch. Chạy test trong môi trường khả dụng; nếu không có môi trường thực thi thì ghi BLOCKED, không tự tuyên bố PASS.
8. Ghi từng thay đổi và bằng chứng vào nhật ký/evidence. Không ghi đè các nội dung Work không liên quan; không sửa thư mục lạ ngoài phạm vi Work 200. Không commit/push hoặc tuyên bố GitHub đồng bộ nếu chưa thực hiện bằng công cụ có bằng chứng.

### Điều kiện cần
- Đã đọc các tài liệu gốc và xác định cấu trúc code hiện tại.
- Có contract rõ cho adapter, dữ liệu và kết quả thực thi.
- Các cổng rủi ro được áp dụng trước mọi đường gửi lệnh.
- Có môi trường kiểm thử xác định; nếu thiếu terminal MT5 thì dùng mock/fake để kiểm thử logic và ghi rõ giới hạn.

### Điều kiện đủ nghiệm thu giai đoạn này
- Các test xác minh hành vi an toàn: không gửi lệnh khi chưa kết nối, dữ liệu không hợp lệ/cũ, symbol không hỗ trợ, vượt giới hạn rủi ro hoặc kill switch bật.
- Paper mode hoạt động độc lập với MT5; mock/demo không bị hiển thị nhầm là dữ liệu live.
- Dashboard thể hiện nguồn và thời điểm dữ liệu cùng trạng thái backend chính xác.
- Có báo cáo test với lệnh chạy, số test pass/fail/blocked và bằng chứng; không dùng PASS nếu chưa chạy.
- Chưa có lệnh giao dịch tiền thật trong giai đoạn này.

### Nhật ký quyết định / giới hạn
- MQL5 EA vẫn là lựa chọn thay thế hoặc adapter triển khai về sau; quyết định hiện tại ưu tiên Python + MT5 Adapter để tái sử dụng chiến lược, Risk Engine và Dashboard.
- Sản phẩm giao dịch cụ thể, broker, symbol và khung thời gian chưa được chốt; không tự giả định hay tối ưu chiến lược theo dữ liệu không có.
- **Trạng thái bàn giao:** Boai được chỉ định đọc entry này và tiếp tục triển khai trong Work 200; entry này tự nó không chứng minh Boai đã đọc hoặc đã bắt đầu.


## Entry 006 — ĐÍNH CHÍNH TÊN AI NHẬN NHIỆM VỤ
- **Thời điểm:** 2026-10-24.
- **Người ghi:** Xu — AI-01.
- **Phạm vi:** Đính chính Entry 005 trong nhật ký Work 200.
- **ĐÍNH CHÍNH CHÍNH THỨC:** Tên AI nhận nhiệm vụ là **BX**, không phải “Boai”. Mọi chỗ trong Entry 005 ghi “Boai” được hiểu và áp dụng là **BX**. BX là AI được giao đọc nhật ký, tiếp tục triển khai Work 200 theo đúng phạm vi, nhiệm vụ, điều kiện cần, tiêu chí nghiệm thu và giới hạn an toàn đã nêu tại Entry 005.
- **Trạng thái:** Đã ghi đính chính qua MCP 8030. Việc BX đã đọc hoặc bắt đầu thực hiện chưa được xác minh; không tuyên bố PASS/DONE nếu chưa có bằng chứng.
