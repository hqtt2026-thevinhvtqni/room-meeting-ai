# TASK GRAPH — Work 200 (v2.0)

Dùng chung cho debug-expert và test-expert. Nguồn chuẩn: `../PLAN_WORK200_v2.0.md`. Khi hai nơi lệch nhau thì plan là chuẩn, và task-graph phải được cập nhật ngay.
Cập nhật: 2026-10-25 · Người lập: Cla. Mọi trạng thái bên dưới = **NOT STARTED** trừ khi ghi khác.

## Bảng task

| ID | Milestone | Owner | Phụ thuộc | Evidence tối thiểu | Trạng thái |
|---|---|---|---|---|---|
| T0.1 | M0 | Xu+Cla | — | E0 | NOT STARTED |
| T0.2 | M0 | BX/Qw | T0.1 | E2→E3 | NOT STARTED (Cla E1: core 6/6) |
| T0.3 | M0 | Cla/Xu | — | E0 | NOT STARTED |
| T0.4 | M0 | Xu | — | E0 | NOT STARTED |
| T0.5 | M0 | Xu | — | E0 | NOT STARTED |
| T1.3 | M1 | BX | — | E2 | NOT STARTED |
| T1.4 | M1 | BX | — | E2 | NOT STARTED |
| T1.7 | M1 | BX | — | E2 | NOT STARTED |
| T1.6 | M1 | BX | T0.3 | E2 | NOT STARTED |
| T1.1 | M1 | BX | T1.6 | E2 | NOT STARTED |
| T1.5 | M1 | BX | T1.6 | E2 | NOT STARTED |
| T1.2 | M1 | BX | T1.1,T1.6,T1.7 | E2→E3 | NOT STARTED |
| T1.8 | M1 | BX/Qw | T1.1–T1.5,T1.7 | E2→E3 | NOT STARTED |
| G1 | M1 | Cla/Qw | T1.1–T1.8 | E3 | NOT STARTED |
| T2.6 | M2 | BX | T1.5 | E2 | NOT STARTED |
| T2.1 | M2 | BX | G1,T2.6 | E2 | NOT STARTED |
| T2.2 | M2 | BX/Qw | T2.1 | E3 | NOT STARTED |
| T2.3 | M2 | BX | T2.1 | E2 | NOT STARTED |
| T2.4 | M2 | BX | T2.1 | E2→E3 | NOT STARTED |
| T2.5 | M2 | BX | T2.4 | E2 | NOT STARTED |
| T2.7 | M2 | BX | T2.6,T0.1 | E2 | NOT STARTED (có thể BLOCKED) |
| G2 | M2 | Cla/Qw | T2.1–T2.6 | E3 | NOT STARTED |
| T3.1 | M3 | Cla→BX | T0.3 | E2 | NOT STARTED |
| T3.2 | M3 | BX | T0.3 | E2 | NOT STARTED |
| T3.3 | M3 | BX | T3.1 | E2→E3 | NOT STARTED |
| T3.4 | M3 | BX | T0.3,T3.2 | E2 | NOT STARTED |
| T3.5 | M3 | BX | T1.1 | E2 | NOT STARTED |
| T3.6 | M3 | BX | G1,T3.2–T3.5 | E2→E3 | NOT STARTED |
| T3.7 | M3 | BX | T3.6 | E2 | NOT STARTED |
| G3 | M3 | Cla/Qw | T3.1–T3.7 | E3 | NOT STARTED |
| T4.1 | M4 | BX | T3.6,T2.5 | E2 | NOT STARTED |
| T4.2 | M4 | BX | T4.1 | E2 | NOT STARTED |
| T4.3 | M4 | Qw | T4.2, host trình duyệt | E3 | NOT STARTED (có thể BLOCKED) |
| G4 | M4 | Cla/Qw | T4.1–T4.3 | E3 | NOT STARTED |
| T5.1 | M5 | BX | G2,G3 | E2 | NOT STARTED |
| T5.2 | M5 | BX | T5.1 | E2 | NOT STARTED |
| T5.3 | M5 | Cla/Xu/BX | T5.2 | E3 | NOT STARTED |
| G5 | M5 | Cla/Qw | T5.1–T5.3 | E3 | NOT STARTED |
| T6.1 | M6 | BX | T0.3 | E1→E2 | NOT STARTED |
| T6.2 | M6 | Xu | G3, host MetaEditor | E0 | NOT STARTED |
| T6.3 | M6 | BX/Qw | T6.2 | E3 | BLOCKED cho đến khi T6.2 PASS |

## Đường găng (critical path)

T0.1 → T0.3 → T1.6 → T1.1 → T1.2 → T1.8 → **G1** → T2.1 → T2.2 → **G2**
G1 → T3.6 (cần T3.2–T3.5) → **G3** → T4.1 → T4.2 → T4.3 → **G4**; G2 + G3 → T5.1 → T5.3 → **G5**.
Chạy song song được ngay: T1.3, T1.4, T1.7, T0.4, T0.5, T3.1, T3.2 (sau T0.3), T6.1.

## Ánh xạ phát hiện → task

| Phát hiện | Task đóng |
|---|---|
| D1 Risk/Broker không tự giữ trạng thái | T1.1, T1.2 |
| D2 SELL giảm vị thế bị chặn | T1.2 |
| D3 Kill switch yếu | T1.2, T1.7 |
| D4 Infinity/NaN | T1.3 |
| D5 Strategy có state ẩn | T1.4 |
| D6 Validation thiếu gap/timeframe | T1.5 |
| D7 Intake chưa xác thực, dedup RAM | T3.1–T3.5 |
| D8 Test mỏng | T1.8 |
| D9 Plan lệch thực tế | T0.3, T0.4 |
| D10 Trộn sản phẩm | T0.3, M6 |
| D11 Thiếu host, cấu trúc lệch | T0.1, T0.5 |

## Quy ước trạng thái

`NOT STARTED` · `IN PROGRESS` · `PASS` · `PASS-LIMITED` (chỉ E1) · `FAIL` · `BLOCKED` (ghi nguyên nhân, owner, điều kiện gỡ).
Task chỉ được chuyển `PASS` khi evidence đạt bậc yêu cầu và đường dẫn evidence đã nằm trong journal.
