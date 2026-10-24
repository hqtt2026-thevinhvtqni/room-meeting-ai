# BaoXtra BX42 MR LCK V4.2.8 TEST — bộ lọc Swing D1 → H4 → H1 → M15

## Bản gốc và mức độ xác minh

- Khôi phục từ `BaoXtra_BX42MR_V4_2_7_PRESET_FibM5_Zones2_TTL80_SIGNAL_ONLY.pine` (19/10/2026), **không ghi đè bản gốc**.
- Bản mới: `BaoXtra_BX42MR_V4_2_8_Swing_D1_H4_H1_M15_TEST.pine`, Pine Script v6.
- Đã đối chiếu cấu trúc mã và sự hiện diện các chức năng gốc bằng phép kiểm tra tĩnh. **Chưa biên dịch trong Pine Editor TradingView, chưa backtest hoặc xác nhận chạy trên MT5**.
- Mọi chế độ khác giữ nguyên khi bộ lọc mới ở `OFF`. Không được xem tín hiệu là bảo đảm xác suất thắng.

## Thiết lập thử nghiệm chính xác

1. Mở Pine Editor TradingView trên **máy tính**, tạo script mới, dán nguyên file `.pine` (hoặc `.txt`), bấm **Save** → **Add to chart**. Không chép đè script cũ.
2. Chọn cặp XAUUSD **đúng nguồn giá bạn dùng**, biểu đồ **15 phút (M15)**.
3. `01 | Thị trường / Mode`: `Mode=Swing`, `Trading engine=Legacy SMC`, `HTF mandatory=ON`.
4. `03 | Preset Swing`: `HTF=1D/1 ngày`, EMA HTF 21/50, EMA chart 21/55/200, Swing length=5, OB lookback=20, Locked setup TTL=10.
5. `03A | D1-H4-H1-M15 Swing Confirm`: `Enable=ON`, H4 EMA 21/50, H4 zones=`Any FVG/OB/Fib`, `H1 confirmation=RSI + candle`, H1 RSI BUY >50 / SELL <50, H4 zone touch TTL=24 nến M15. Có thể đổi `FVG or OB` để lọc chặt hơn, `Two zones touched` để tìm hội tụ tại cùng nến, nhưng thường ít tín hiệu hơn.
6. `00 | Execution`: **Signal Only** trong giai đoạn kiểm thử. Không bật alert webhook/n8n có thể điều khiển MT5. Xem dashboard hai hàng mới: `Swing H4/H1 / Filter` và `H4 zone / H1 RSI`.
7. `04 | SMC`: Giữ Fib from 0.382 và Fib to 0.618, không thay những tham số risk/SL/TP đã kiểm thử của bạn.

## Thuật toán bổ sung

- **D1 (nến đã đóng)**: xu hướng EMA 21/50 theo preset Swing; từ chối giao dịch ngược hướng xu hướng khi filter bật.
- **H4 (nến đã đóng)**: phát hiện FVG 3 nến, vùng OB proxy là nến ngược chiều trước nến displacement, Fibonacci 0.382–0.618 từ các pivot xác nhận. OB proxy *không phải* bằng chứng về khối lượng lệnh của tổ chức.
- **M15**: phải **chạm vùng H4** gần đây, sau đó tín hiệu Legacy SMC cũ phải thỏa BOS/CHoCH hoặc sweep/CISD, tạo Locked Setup và retest xác nhận. Không kích hoạt chỉ vì chạm FVG/OB/Fib.
- **H1 (nến đã đóng)**: xác nhận RSI+candle hoặc RSI+EMA hoặc RSI+BOS. Lọc mặc định RSI+candle.
- Bộ lọc có thể **chặn** tín hiệu, không tạo lệnh mới độc lập, không sửa các công thức tính SL/TP/khối lượng của Legacy SMC.
- Các vùng H4 vẽ bằng hai đường biên cho Supply/Demand (ưu tiên FVG → OB proxy → Fib); các vùng OB/FVG/Fib gốc trên M15 vẫn còn.

## Phân biệt hai bộ máy đặc biệt quan trọng

- `Legacy SMC + Swing D1-H4-H1-M15`: dùng TP1/2/3, BE, trailing, portfolio risk và kiểm soát lot **của Legacy SMC**.
- `RSI Momentum`: bộ máy M1 cũ có Dynamic Peak Profit Lock **20–70%**. Mã vẫn được giữ nguyên, nhưng **chưa áp dụng cơ chế MR Peak Profit Lock vào lệnh Swing mới**. Nếu muốn hợp nhất, cần phiên bản nâng cấp riêng và kiểm thử phân bổ lệnh/chốt phần để tránh sửa sai nguyên tắc quản trị vốn.

## Ví dụ kiểm tra XAUUSD, không phải mức cố định trong thuật toán

Khi thấy chart H4 có vùng khoảng 4,050–4,063, không mặc định SELL tại đó. Cần H4 nhận diện vùng, giá hồi chạm vùng, H1 xác nhận SELL và M15 có setup/retest hợp lệ. Nếu không có đủ điều kiện, bảng sẽ hiển thị `WAIT CONFLUENCE`; nếu chart không phải M15 sẽ hiển thị `USE M15`.

## Checklist kiểm thử thủ công

- [ ] Pine Editor **compile PASS** (nếu có lỗi lưu nguyên dòng và thông báo để sửa).
- [ ] Tắt filter → tín hiệu và TP/SL giống bản gốc V4.2.7 trên cùng dữ liệu.
- [ ] Bật filter trên M15 / Swing / HTF=1D → dashboard hiển thị PASS/WAIT hợp lý.
- [ ] Bật filter trên chart H1/H4 → **không** phát tín hiệu Swing mới.
- [ ] H4 zone không có hoặc hết TTL → chặn lệnh.
- [ ] H1 RSI/candle ngược → chặn lệnh.
- [ ] Giá chạm vùng nhưng M15 không có retest → chặn lệnh.
- [ ] Signal Only → không đặt lệnh broker, không phát webhook giao dịch từ module mới.
- [ ] OB/FVG/Fib trên M15 không bị mất; các vùng H4 không chồng nhãn không cần thiết.
- [ ] Nếu thử `Auto Backtest + Alerts` chỉ sau khi đảm bảo alert/bridge live đã tắt, kiểm tra TP1/TP2/TP3 và risk gate bằng Strategy Tester; KHÔNG suy diễn kết quả thành khớp lệnh Exness.

## Thông tin an toàn

Lot 0.01 XAUUSD theo hợp đồng chuẩn 100 oz/lot ≈ 1 oz: SL rộng 27 USD/oz có thể lỗ ~27 USD trước phí và trượt giá. Broker và mã khác có thể có quy mô hợp đồng khác. Dùng tài khoản demo, kiểm tra equity, spread, hợp đồng, margin trước khi tính đến giao dịch thật. Swing giữ qua cuối tuần có rủi ro gap.
