# BaoXtra BX42MR MT5 Swing Semi-Auto v0.1

**Build:** 2026-10-24 | **Input:** BaoXtra BX42MR V4.2.8 Pine v6 | **Status:** MQL5 source created, **not yet compiled in MetaEditor/MT5**.

## VI — Tính năng đã chuyển

- Nền tảng: Expert Advisor phân tích cho **MetaTrader 5 desktop trên Windows hoặc VPS**, không đặt lệnh.
- Chỉ chạy trên biểu đồ **M15**, dùng nến **đã đóng**: D1 EMA21/50, H4 EMA21/50, H4 FVG (3 nến), OB proxy (nến đối chiều trước displacement), vùng Fib 0.382–0.618 từ swing pivot xác nhận, H1 RSI14 và nến/EMA.
- M15: cấu trúc **BOS breakout** + nến displacement, lưu setup (lock), đợi **bar M15 sau** chạm OB/FVG/Fib + nến xác nhận. H4 phải có zone touch trong tối đa 24 nến M15 và đủ trend H1/D1/H4.
- Tín hiệu đầu ra: **BUY/SELL plan** với giá tham chiếu `Entry`, `SL`, `TP1`, `TP2`, `TP3`; vẽ 5 đường ngang trên chart và vùng H4 bằng cặp đường.
- Xử lý mỗi nến M15 mới, cập nhật dashboard qua `Comment()`; `Alert` và `SendNotification()` là tùy chọn (mặc định tắt).
- **Không có API broker, OrderSend, CTrade hay thực hiện đặt lệnh**. `InpPreviewLot=0.01` chưa dùng để thực hiện lệnh và không phải sizing được xác minh. Không hứa hẹn tỷ lệ thắng.

## VI — Chưa chuyển 1:1 từ Pine

- Sweep → CISD trigger, CHoCH phân biệt với BOS, ZigZag toàn phần, cơ chế score 70/100, cho phép 3 lệnh pyramiding, TP partial fills, BE/Trailing theo fill thật, Momentum M1 peak profit lock, backtest engine nội bộ Pine, phiên/blackout/giới hạn lỗ ngày, cơ chế volume sizing/safety full parity, alert pipes `BX421` / `BX42_MR`.
- Đây là **MQL5 Swing filter và kế hoạch giao dịch THAM KHẢO v0.1**, không phải port đầy đủ 1.758 dòng Pine.
- Không xem mức Entry/SL/TP dự kiến là báo giá khớp chắc chắn; spread, slippage và stop level của sàn có thể khác.

## VI — Cài đặt MT5 trên Windows, máy tính hoặc VPS

1. Mở **MetaTrader 5 desktop** trên máy tính, đăng nhập **tài khoản demo**.
2. `File` → `Open Data Folder` → `MQL5` → `Experts` → chép `BaoXtra_BX42MR_MT5_Swing_SemiAuto_v0_1.mq5` vào.
3. Nhấn **F4** mở **MetaEditor**, tìm file trong `Experts`, nhấn **F7 Compile**. Nếu có lỗi, lưu log đầy đủ; gói này **chưa được biên dịch xác nhận** trên MetaEditor.
4. Vào MT5, chọn mã XAUUSD theo **đúng hậu tố sàn** (`XAUUSD`, `XAUUSDm`...), khung **M15**, kéo EA vào chart. Nên **tắt Algo Trading toàn cục** khi kiểm thử; EA chỉ đọc dữ liệu và báo kế hoạch.
5. Nạp lịch sử M15/H1/H4/D1. Đợi nến M15 mới đóng rồi xem dashboard bên trái biểu đồ và đường Entry/SL/TP1-3. Nếu màn hình trống, kiểm tra `Experts` / `Journal` logs, timeframe, dữ liệu biểu đồ.
6. `View` → `Strategy Tester`, chọn EA, XAUUSD M15, **Every tick based on real ticks**, bật Visual mode; kiểm tra logic/line/alert và ghi PASS/FAIL. Vì EA không đặt lệnh, **không dùng Profit Factor/PnL ở Strategy Tester** để đánh giá lợi nhuận.
7. Mọi tín hiệu chỉ dành cho manual review. Đối chiếu bid/ask, `SYMBOL_TRADE_CONTRACT_SIZE`, min lot, step, stop distance, margin trước khi tự đặt lệnh demo.

## VI — Xem trên iPhone / MT5 Trade

Ứng dụng **MetaTrader 5 trên iPhone không chạy file EA `.mq5`**. EA chạy trong MT5 desktop/VPS; anh có thể nhận **push** trên iPhone rồi tự đặt lệnh qua app.

- Trong MT5 iPhone → **Messages** lấy **MetaQuotes ID**, bật iOS Settings → Notifications → MetaTrader 5.
- Trên MT5 desktop → **Tools → Options → Notifications** → Enable Push Notifications → nhập MetaQuotes ID → Test.
- Sau khi test nhận tin thành công, bật `InpPushToMobile=true` trong EA. Tín hiệu từ EA chỉ là thông báo kế hoạch, **không đặt lệnh tự động**.
- Dữ liệu chart và các đường do EA vẽ trên PC **không được đồng bộ như chỉ báo có thể chạy trên app điện thoại**.

## EN — Architecture & safeguards

This is a review-only, closed-bar Swing prototype. M15 entry plans are conditioned on D1 trend, H4 zone touch and H1 confirmation; no orders or network/webhooks are sent. It is not a Pine-exact port. Compilation, parity and Strategy Tester visual validation must occur in an actual MetaTrader 5/MetaEditor terminal before accepting a release. Use a demo account only for discretionary testing.

## Roadmap / Next gate

1. MetaEditor compilation with zero errors and evidence.
2. D1/H4/H1/M15 comparison with TradingView Pine V4.2.8 on identical price feed/time alignment; document differences in CFD data and session boundaries.
3. Port Sweep→CISD, CHoCH, score and risk engine with deterministic replay.
4. Only then consider separate demo-only order execution and mobile management via authorized bridge/n8n; do not activate live trading by default.
