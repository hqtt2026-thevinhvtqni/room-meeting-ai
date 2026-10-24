# PLAN WORK 200 v2.0 — CRYPTO-TRADING-BOT

**Tác giả:** Cla — AI-03 / CTO Code-Debug
**Ngày:** 2026-10-25 (ICT)
**Trạng thái:** PROPOSED — chờ Xu điều phối và Vinh duyệt hướng. Đây KHÔNG phải release approval và KHÔNG phải xác nhận Work 200 hoàn tất.
**Căn cứ:** biên bản `06_EVIDENCE/WORK200_MINUTES_20261025_01.md`, journal entry 001–008, đọc trực tiếp source qua MCP 8030, và kiểm tra độc lập của Cla (xem `06_EVIDENCE/CLA_ASSESSMENT_20261025.md`).
**Quan hệ với v1.0:** `PLAN_WORK200_v1.0.md` giữ nguyên làm tham chiếu. v2.0 là bản thực thi; các phase P0–P4 của v1.0 được ánh xạ sang M0–M5 (mục 6).
**Nguyên tắc:** READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF. Không PASS nếu thiếu evidence. Không giả lập kết quả.

---

## 1. Mục tiêu E2E

Một đường ống paper-only, tất định, có thể kiểm chứng:

nến / tín hiệu BX42 → xác thực dữ liệu → quyết định rủi ro → paper fill → sổ cái danh mục → audit log → backtest/báo cáo → API chỉ-đọc → dashboard.

**Ngoài phạm vi (cho đến khi có quyết định riêng bằng văn bản):** lệnh tiền thật, rút tiền/custody, credential trong repo, cam kết lợi nhuận, kết nối broker/sàn có quyền giao dịch, MT5 chạy lệnh thật.

## 2. Phạm vi quyền

- Chỉ ghi trong Sandbox của Work 200 qua MCP 8030. Working Source là read-only. AI không merge/commit/push.
- Không chạm Core, Work khác, secrets.
- Chỉ xoá file khi Vinh yêu cầu rõ. Các trùng lặp/lệch cấu trúc chỉ được liệt kê và đề xuất.
- Mọi việc cần chạy code mà không có execution host được ủy quyền thì ghi BLOCKED, không suy đoán kết quả.

---

## 3. Đánh giá tổng thể hiện trạng

**Kết luận một dòng:** nền móng an toàn đúng hướng (paper-only, fail-closed, Decimal, không credential), nhưng đang ở mức khung P1 chưa hoàn chỉnh: chưa có sổ cái danh mục, risk engine chưa tự giữ trạng thái, chưa có backtest/report/persistence, và phần lớn bằng chứng chưa đạt mức chạy trong môi trường được ủy quyền. Trạng thái giữ nguyên: ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED.

### 3.1 Bảng thành phần

| Thành phần | Có gì | Trạng thái | Evidence cao nhất hiện có |
|---|---|---|---|
| Domain models, validation nến | `models.py`, `data_validation.py` | Có, còn thiếu | E1 (Cla chạy 6/6 test_core) |
| Risk manager | notional/position/daily-loss, kill switch | Có nhưng không tự giữ trạng thái, xem D1–D3 | E1 |
| Paper broker | fill + fee + slippage, không network | Có, chưa có sổ cái | E1 |
| Strategy baseline | MA crossover | Có nhưng có state ẩn, xem D5 | E1 |
| Signal intake | parse REVIEW_ONLY, allow-list, kiểm tra thời gian, SL/TP | Có, dedup chỉ trong RAM, chưa xác thực nguồn | E1 do BX báo 27/27 (Cla chưa chạy lại) |
| Portfolio / ledger | Không có | Chưa làm | — |
| Backtest runner / metrics / report | Không có | Chưa làm | — |
| Persistence / event log | Không có | Chưa làm | — |
| Dashboard | HTML tĩnh, toàn dữ liệu mock | Prototype | E0 (file tồn tại), chưa QA trình duyệt |
| BX42 Pine | Source 1758 dòng, SHA-256 khớp | Tham chiếu | E0 + hash |
| MT5 v0.1 | 517 dòng MQL5, chỉ tín hiệu | Chưa compile | E1 tĩnh 7/7 (BX báo) |
| MT5 full port | Tài liệu đặc tả 10 work package | Chỉ đặc tả | E0 |

### 3.2 Bằng chứng độc lập của Cla (E1 — giới hạn rõ)

- Cla đọc lại các module lõi qua MCP 8030, dựng lại bản sao trong container của Cla (Python 3.12.3, pytest) rồi chạy `test_core.py`: **6 passed**.
- **Giới hạn:** (a) đây là bản chép lại từ nội dung đọc qua MCP, không phải chạy trong Sandbox; (b) chưa chạy `test_signal_intake.py` (Cla chưa đọc file test đó); (c) không thay thế yêu cầu chạy trong host được ủy quyền (T0.2).
- Cla chạy thêm các probe có mục tiêu. Kết quả nằm ở D1–D6 và trong file đánh giá.

### 3.3 Phát hiện

Mức độ: **H** = chặn việc nối pipeline/tin cậy kết quả; **M** = sai lệch cần sửa trước backtest; **L** = dọn dẹp.

| ID | Mức | Phát hiện | Bằng chứng | Xử lý tại |
|---|---|---|---|---|
| D1 | H | Broker/Risk không tự theo dõi vị thế và PnL ngày. `current_position_notional` và `daily_pnl` do người gọi truyền, mặc định 0. Dùng mặc định thì trần vị thế và trần lỗ ngày vô hiệu. | Probe: trần vị thế 150, gửi 3 lệnh BUY ~100 mỗi lệnh → 3 fills, tổng ~300.15, `halted=False`. | T1.1, T1.2 |
| D2 | H | `approve()` cộng `abs(position) + notional` bất kể chiều lệnh. Lệnh SELL giảm vị thế bị từ chối khi vị thế gần trần, tức không thoát được vị thế. | Probe: long 1800, trần 2000, SELL 500 → `False`. | T1.2 |
| D3 | M | Kill switch chỉ là cờ trong RAM: không bền qua restart, reset không ghi actor/lý do, không có chế độ chỉ-giảm-vị-thế, không có audit. | Đọc source `risk.py`. | T1.2, T1.7 |
| D4 | M | `OrderRequest`/`Candle` nhận `Infinity`; `NaN` ném `InvalidOperation` (không phải `ValueError`) nên xử lý lỗi không đồng nhất. Hiện an toàn nhờ phép so sánh trong risk, không nhờ thiết kế. | Probe P2/P3. | T1.3 |
| D5 | M | `MovingAverageCross` có state ẩn (`_previous_relation`). Cùng input gọi hai lần cho kết quả khác nhau (BUY rồi None), vi phạm tiêu chí "tất định với input cố định". | Probe P5. | T1.4 |
| D6 | M | `validate_candles` không phát hiện khoảng trống thời gian, trộn timeframe, hay dữ liệu cũ, dù tài liệu kiến trúc yêu cầu. | Probe P6/P7: chuỗi thiếu 10 nến 15m vẫn được chấp nhận. | T1.5 |
| D7 | H (khi nối bridge) | Signal intake chưa xác thực nguồn: các cờ `paper_only`, `live_execution` do người gửi tự khai. Dedup `_seen` nằm trong RAM, không giới hạn kích thước. SELL trên SPOT chưa phân biệt đóng vị thế và bán khống. Chưa parse được alert BX421 / BX42_MR. | Đọc `signal_intake.py` + `ALERT_COMPATIBILITY_CONTRACT_V01.md`. | M3 |
| D8 | M | Bộ test mỏng: 6 test lõi, không có test strategy, nến test có O=H=L=C nên không kiểm tra hình học nến; thiếu các kịch bản lỗi mà v1.0 P3 yêu cầu. | Đọc `test_core.py`. | T1.8 |
| D9 | M | Lệch trạng thái kế hoạch: mọi checkbox trong v1.0 vẫn trống dù code đã có; "open product decisions" (sàn, symbol, timeframe) chưa được chốt nhưng code đã mặc định BTCUSDT/OKX/SPOT/15m. | Đọc v1.0, brief, `signal_intake.py`. | T0.3, T0.4 |
| D10 | M | Ba hướng sản phẩm đang trộn trong một Work: bot BTC spot (Python), XAUUSD CFD (Pine/MT5), dashboard. Khác nhau về tick size, hợp đồng, phí, margin. Nguy cơ trộn kết quả. | Integration plan mục 7 + journal entry 005. | T0.3, M6 |
| D11 | L | Không có execution tool trong MCP 8030 nên mọi test từng chạy ngoài Sandbox. Root của sandbox còn thư mục `06_EVIDENCE/` cùng tên journal bên ngoài `CRYPTO-TRADING-BOT/` (Cla chưa đối chiếu nội dung). `list_works` hiển thị `work_name` của Work 200 là `06_EVIDENCE`, lệch với manifest. | `sandbox_list`, `sandbox_list_works`. | T0.1, T0.5 |

### 3.4 Điểm mạnh nên giữ

Paper-only tách bạch và có test từ đầu; `Decimal` cho tiền; không phụ thuộc ngoài (stdlib-only); kỷ luật evidence (hash Pine khớp, báo cáo ghi rõ NOT RUN); tài liệu hợp đồng alert trung thực về giới hạn.

---

## 4. Định hướng (quyết định CTO)

**Thứ tự ưu tiên:** Track A (lõi) → Track B (bridge BX42) → Track C (API + dashboard) → Track D (MT5, đóng băng có điều kiện).
Lý do: B cần Portfolio và Risk của A; C cần dữ liệu thật từ A/B; D phụ thuộc host ngoài (MetaEditor) và chỉ có ý nghĩa khi tín hiệu tham chiếu đã ổn.

**Giả định mặc định (A1–A6).** Plan chạy theo các giả định này để không phải chờ người làm cầu nối. Vinh/Xu có thể ghi đè bằng một dòng trong journal, khi đó Cla cập nhật plan.

| ID | Giả định | Ghi đè nếu |
|---|---|---|
| A1 | Profile đầu tiên: `P-BTC-SPOT-OKX-15M` (BTCUSDT, OKX, SPOT, 15m). Đây là mặc định hiện có của code, nay được chốt rõ. | Vinh chọn sàn/symbol khác |
| A2 | XAUUSD CFD/MT5 là profile riêng `P-XAU-CFD-MT5`, không dùng chung config, dữ liệu hay báo cáo với A1 | Vinh gộp |
| A3 | SPOT chỉ long: SELL chỉ đóng/giảm vị thế đang có, không bán khống | Vinh muốn mô phỏng perp/margin (khi đó cần profile mới) |
| A4 | Stdlib-only. Phụ thuộc mới (pytest-cov, Playwright…) chỉ dùng ở host kiểm thử, ghi ADR và pin phiên bản | — |
| A5 | Kiểm thử engine dùng dữ liệu tổng hợp tất định (synthetic fixtures). Dữ liệu thị trường thật là bước tùy chọn, BLOCKED nếu không có mạng được phép | — |
| A6 | Khớp lệnh backtest ở giá mở của nến kế tiếp sau nến phát tín hiệu; nếu SL và TP cùng chạm trong một nến thì tính SL trước (bảo thủ) | Vinh yêu cầu mô hình khác |

---

## 5. Evidence và định nghĩa trạng thái

**Bậc evidence:**

- **E0** — file tồn tại, đọc lại qua MCP, hash khớp. Chỉ chứng minh sự tồn tại.
- **E1** — chạy cục bộ ngoài host được ủy quyền (container của AI). Ghi: lệnh, phiên bản Python/pytest, exit code, số pass/fail, hash input. Cho kết quả **PASS-LIMITED**.
- **E2** — chạy trong host kiểm thử được ủy quyền, ghi đủ như E1 kèm hash cây `04_CODE`. Mức tối thiểu để PASS task code.
- **E3** — Qw tái chạy độc lập từ artifact và ra cùng kết quả. Bắt buộc cho các task đánh dấu [QA] và cho mọi gate.

**Định nghĩa:**

- **PASS (task):** mọi tiêu chí nghiệm thu của task thỏa với evidence ≥ bậc yêu cầu, đường dẫn evidence được ghi vào journal.
- **PASS-LIMITED:** chỉ có E1. Không được dùng để mở gate.
- **DONE (milestone):** mọi task PASS, Cla review xong, Qw ký E3, journal có entry gate.
- **BLOCKED:** thiếu điều kiện cần (host, mạng, công cụ, quyết định). Phải ghi nguyên nhân, owner, điều kiện gỡ. Tuyệt đối không giả lập kết quả.
- **FAIL:** chạy được nhưng tiêu chí không thỏa. Chuyển Cla triage (Mục 8).

**Mẫu evidence cho mỗi task** (ghi vào `06_EVIDENCE/`): task ID · lệnh · môi trường · exit code · số pass/fail/blocked · hash input/output · file kết quả · giới hạn xác minh.

---

## 6. Lộ trình và task

Kích cỡ tương đối: **S** ≤ 1 phiên làm việc, **M** 1–3 phiên, **L** > 3 phiên. Owner: **BX** thi công, **Qw** QA độc lập, **Xu** điều phối, **Cla** đặc tả/review/debug.
Ánh xạ v1.0: P0 → M0; P1 → M1; P2 → M2; P3 → xuyên suốt (T1.8, mỗi gate) ; P4 → M5.

### M0 — Nền tảng và quản trị (làm trước tiên)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T0.1 | Chốt chính sách evidence và execution host. Nêu rõ host nào được chạy pytest (và trình duyệt cho T4.3). Nếu chưa có thì tuyên bố NO-HOST. | Xu + Cla | — | `EVIDENCE_POLICY.md` có bậc E0–E3, tên host hoặc tuyên bố NO-HOST; mọi task cần E2 mà thiếu host tự động mang nhãn BLOCKED | E0 |
| T0.2 | Chạy lại toàn bộ test hiện có làm baseline. | BX, Qw [QA] | T0.1 | Lệnh `python -m pytest -q` từ `04_CODE`, exit code 0, ghi số test (kỳ vọng core 6 + signal intake 27 = 33, nếu khác thì giải thích), phiên bản môi trường, hash `04_CODE` | E2 → E3 |
| T0.3 | Đóng băng profile và giả định A1–A6. | Cla soạn, Xu duyệt | — | `PROFILES.md`: mỗi profile có sàn/thị trường, tick size, qty step, min notional, fee maker/taker, chế độ cho phép; không trường nào dùng chung giữa A1 và A2 | E0 |
| T0.4 | Đồng bộ trạng thái plan v1.0: chuyển checkbox thành bảng trạng thái có link evidence. | Xu | — | Mỗi mục v1.0 có trạng thái DONE/PARTIAL/NOT RUN và link evidence | E0 |
| T0.5 | Liệt kê trùng lặp cấu trúc (thư mục `06_EVIDENCE/` ở root, `desktop.ini`, `work_name` lệch). Chỉ đề xuất, không xoá. | Xu | — | Báo cáo liệt kê và đề xuất; không file nào bị xoá | E0 |

### M1 — Lõi paper an toàn, bản cứng (Track A)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T1.6 | `InstrumentSpec` + config profile (dataclass + JSON, kiểm tra schema, không secret). | BX | T0.3 | Nạp profile hợp lệ; profile thiếu trường hoặc có số không hữu hạn bị từ chối; chuẩn hoá giá/số lượng theo tick/step có test biên | E2 |
| T1.3 | Kiểm tra số hữu hạn dùng chung (`Infinity`, `NaN`, `-0`) cho Candle, OrderRequest, limits, rates; thống nhất ném `ValueError`. | BX | — | Test bảng cho từng loại đầu vào xấu; không còn `InvalidOperation` lọt ra ngoài; D4 đóng | E2 |
| T1.1 | Portfolio + sổ cái (Decimal): cash, vị thế theo symbol, giá vốn bình quân, realized/unrealized PnL, phí. Spot long-only (A3). | BX | T1.6 | Đẳng thức kế toán `cash + vị thế × giá đánh dấu = equity` đúng trên ≥ 10 kịch bản tính tay; SELL vượt vị thế bị từ chối; tất định (hai lần chạy cho cùng kết quả) | E2 |
| T1.2 | Risk v2: đọc trạng thái từ Portfolio thay vì tham số truyền vào; trả `RiskDecision(approved, reason_code)`; phân biệt lệnh tăng/giảm exposure; thêm trần drawdown, số lệnh/ngày, cooldown, giá cũ, min/max qty. Kill switch có trạng thái ARMED/HALTED, reset cần actor + lý do, ghi event; khi HALTED vẫn cho lệnh giảm vị thế. | BX theo đặc tả S2 của Cla | T1.1, T1.6, T1.7 | Probe D1 và D2 chuyển thành test hồi quy và PASS (3 lệnh vượt trần bị chặn lệnh thứ 2 hoặc 3; SELL giảm vị thế gần trần được duyệt); mỗi `reason_code` có ≥ 1 test; reset không có actor/lý do bị từ chối | E2 → E3 |
| T1.4 | Strategy protocol v2: bất biến theo hợp đồng (state do runner sở hữu, có `reset()` hoặc trạng thái truyền tường minh). | BX | — | Cùng chuỗi nến, hai instance mới và một instance gọi lại sau `reset()` cho cùng đầu ra (so hash đầu ra); D5 đóng | E2 |
| T1.5 | Validation dữ liệu v2 nhận biết timeframe: khoảng trống, trộn nhịp, trùng, sai thứ tự, lẫn symbol, dữ liệu cũ; trả `ValidationReport`, fail-closed. | BX | T1.6 | Test cho từng loại lỗi (kể cả probe P6/P7); chuỗi sạch được chấp nhận; D6 đóng | E2 |
| T1.7 | Event log JSONL append-only, có phiên bản schema, `run_id`, che dữ liệu nhạy cảm. | BX | — | Test xác nhận chuỗi giống khoá (ví dụ `api_key=...`) bị che; mỗi quyết định risk/fill/kill-switch sinh đúng một event | E2 |
| T1.8 | Mở rộng test theo ma trận kịch bản lỗi của v1.0 P3 (dữ liệu hỏng, sàn/dữ liệu ngừng, lệnh bị từ chối, giá cũ, chạm risk limit, kill switch). Dùng nến có O≠H≠L≠C. | BX, Qw [QA] | T1.1–T1.5, T1.7 | `TEST_MATRIX.md` ánh xạ từng kịch bản → test; không kịch bản nào trống; nếu host có coverage thì ghi số liệu dòng lệnh cho các module lõi (không đặt ngưỡng cứng khi chưa có công cụ) | E2 → E3 |
| **G1** | **Gate M1** | Cla review, Qw ký | T1.1–T1.8 | D1–D6 và D8 đóng; toàn bộ test PASS ở E3; không còn lỗi an toàn mức nghiêm trọng chưa xử lý; journal có entry gate | E3 |

### M2 — Backtest và báo cáo (Track A)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T2.6 | Loader CSV OHLCV có băm SHA-256; bộ dữ liệu tổng hợp tất định cho test. | BX | T1.5 | Fixture có hash cố định; file lỗi bị từ chối bởi T1.5 | E2 |
| T2.1 | Backtest runner theo sự kiện: chỉ thấy dữ liệu đến thời điểm t; khớp ở giá mở nến kế tiếp (A6); áp phí + slippage + spread; `run_id`; dấu vân tay config + dữ liệu. | BX theo đặc tả S3 | G1, T2.6 | Chạy hai lần cho cùng báo cáo byte-for-byte; có `config_hash` và `data_hash` trong kết quả | E2 |
| T2.2 | Bộ kiểm tra rò rỉ tương lai (look-ahead). | BX, Qw [QA] | T2.1 | Test biến đổi: sửa các nến sau t thì quyết định tại t không đổi; có một strategy "gian lận" làm đối chứng âm mà bộ kiểm tra phải phát hiện | E3 |
| T2.3 | Tách train/validation/test và walk-forward. | BX | T2.1 | Runner từ chối tối ưu tham số trên đoạn test; ranh giới đoạn được ghi trong báo cáo | E2 |
| T2.4 | Chỉ số: lợi suất, max drawdown, biến động, turnover, phí, mức phơi nhiễm, win/loss, so với mua-giữ. | BX | T2.1 | Giá trị khớp tính tay trên ≥ 3 fixture nhỏ | E2 → E3 |
| T2.5 | Bộ tạo báo cáo Markdown/JSON, kèm tuyên bố giới hạn ("kết quả lịch sử không chứng minh lợi nhuận tương lai"). | BX | T2.4 | Báo cáo đủ các mục tại `ACCEPTANCE_CRITERIA.md` (drawdown, chi phí, phơi nhiễm, benchmark) | E2 |
| T2.7 | (Tùy chọn) Dữ liệu thị trường thật, chỉ đọc, qua endpoint công khai. | BX | T2.6, T0.1 | Có file + hash + nguồn + ngày lấy; không dùng được thì **BLOCKED** (không thay bằng số liệu bịa) | E2 |
| **G2** | **Gate M2** | Cla review, Qw ký | T2.1–T2.6 | Chạy tái lập được, không rò rỉ tương lai (T2.2 PASS), báo cáo đầy đủ | E3 |

### M3 — Bridge tín hiệu BX42 (Track B)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T3.1 | Đặc tả envelope có chữ ký (HMAC-SHA256 bằng `hmac` stdlib; khoá lấy từ biến môi trường, không có trong repo; kèm timestamp + nonce; JSON chuẩn tắc). | Cla (S4) → BX | T0.3 | Test: chữ ký sai, thiếu chữ ký, timestamp lệch, nonce lặp đều bị từ chối; cờ `paper_only`/`live_execution` tự khai không còn là cơ sở tin cậy duy nhất | E2 |
| T3.2 | Parser review-only cho BX421 `MANUAL_REVIEW` và BX42_MR `MANUAL_REVIEW` (định dạng ngăn cách bằng dấu gạch đứng). Các loại `PAPER`, `BACKTEST_AUTO`, `BACKTEST_ADD`, `SL_UPDATE` thành loại sự kiện riêng, không bao giờ thành lệnh vào. Loại lạ hoặc thiếu trường bị từ chối. | BX | T0.3 | Fixture tổng hợp cho từng định dạng trong `ALERT_COMPATIBILITY_CONTRACT_V01.md`; test xác nhận `SL_UPDATE` không sinh BUY/SELL | E2 |
| T3.3 | Kho idempotency bền vững (SQLite stdlib), giới hạn lưu trữ, chống replay qua restart. | BX | T3.1 | Test: khởi động lại tiến trình vẫn từ chối event cũ; hai tiến trình gửi cùng `event_id` chỉ một được nhận; D7 phần dedup đóng | E2 → E3 |
| T3.4 | Tách profile: alert của XAUUSD/CFD bị từ chối ở profile BTC spot và ngược lại. | BX | T0.3, T3.2 | Test chéo profile cho symbol, sàn, thị trường, timeframe | E2 |
| T3.5 | Ngữ nghĩa SPOT: SELL chỉ đóng/giảm vị thế đang có (A3). | BX | T1.1 | SELL khi không có vị thế bị từ chối với reason code riêng | E2 |
| T3.6 | Pipeline: tín hiệu → xác thực dữ liệu → risk → paper broker → sổ cái → audit event. | BX | G1, T3.2–T3.5 | Kịch bản E2E có bảng kết quả kỳ vọng (chấp nhận, bị risk chặn, dữ liệu cũ, kill switch, trùng event); mỗi kịch bản để lại đúng chuỗi audit event | E2 → E3 |
| T3.7 | Mô phỏng thoát lệnh paper (SL/TP1/TP2/TP3) trên các nến sau; nếu SL và TP chạm cùng một nến thì SL trước (A6). | BX | T3.6 | Test bảng trên nến dựng sẵn; tổng PnL khớp tính tay | E2 |
| **G3** | **Gate M3** | Cla review, Qw ký | T3.1–T3.7 | Không có đường nào từ tín hiệu ra lệnh ngoài paper broker; D7 đóng; replay và cross-profile PASS ở E3 | E3 |

### M4 — API chỉ-đọc và dashboard (Track C)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T4.1 | API chỉ-đọc theo hợp đồng trong `DASHBOARD_SCOPE_AND_INTEGRATION_PLAN.md`; mỗi phản hồi có `as_of`, `source`, trạng thái độ tươi; chỉ nhận GET, bind 127.0.0.1. | BX theo đặc tả S5 | T3.6, T2.5 | Test: mọi phương thức khác GET bị từ chối; dữ liệu cũ trả trạng thái `stale`, không thay bằng số giả | E2 |
| T4.2 | Nối dashboard với API; thêm các trạng thái loading/stale/unavailable/error; nhãn DEMO/PAPER rõ ràng. Nút stop: gỡ hoặc vô hiệu hoá cho đến khi có xác thực + nối risk engine + audit + test lỗi. | BX | T4.1 | Không còn giá trị mock hiển thị như dữ liệu thật; nút stop không được mô tả là kill switch hoạt động | E2 |
| T4.3 | QA trình duyệt (desktop + mobile) trên host có trình duyệt. | Qw | T4.2, host | Chụp màn hình/log từng trạng thái; không có host trình duyệt thì **BLOCKED** | E3 |
| **G4** | **Gate M4** | Cla review, Qw ký | T4.1–T4.3 | Như trên | E3 |

### M5 — Quan sát paper trading (v1.0 P4)

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T5.1 | Bộ phát lại dữ liệu ghi sẵn (replay) qua pipeline đầy đủ. | BX | G2, G3 | Replay tất định, cùng dấu vân tay → cùng kết quả | E2 |
| T5.2 | Log chênh lệch giữa fill kỳ vọng và fill paper thực tế. | BX | T5.1 | Mỗi lệch vượt ngưỡng đã định có bản ghi và lý do | E2 |
| T5.3 | Định nghĩa cửa sổ quan sát (độ dài, số chế độ thị trường, ngưỡng cảnh báo) rồi chạy xong cửa sổ và lập quyết định bằng văn bản. Ngưỡng cụ thể do Cla đề xuất và Xu duyệt **trước khi chạy**, không chỉnh sau. | Cla đề xuất, Xu duyệt, BX chạy | T5.2 | Văn bản quyết định kèm evidence, rủi ro còn tồn tại, giới hạn | E3 |
| **G5** | **Gate M5** | Cla review, Qw ký | T5.1–T5.3 | Cửa sổ hoàn tất, quyết định bằng văn bản. **Không** mặc nhiên mở giao dịch thật | E3 |

### M6 — MT5 (Track D, đóng băng có điều kiện)

MT5 giữ theo gate riêng đã nêu trong `MT5_FULL_PORT_V1/`. Không tuyên bố MT5-ready khi thiếu bằng chứng.

| ID | Việc | Owner | Phụ thuộc | Nghiệm thu (đủ) | Evidence |
|---|---|---|---|---|---|
| T6.1 | Kiểm tra tĩnh khớp 179 khai báo input giữa Pine và hai file TSV (đếm bằng script, không đoán). | BX | T0.3 | Số khai báo trích từ Pine khớp tổng dòng hai TSV; ghi lệnh và kết quả | E1 → E2 |
| T6.2 | Điều kiện mở khoá W2–W10: G3 đã PASS **và** có host MetaEditor/terminal demo được ủy quyền. | Xu xác nhận | G3, host | Thiếu một trong hai thì toàn bộ W2–W10 giữ **BLOCKED** | E0 |
| T6.3 | Thực hiện W2–W10 theo `MASTER_IMPLEMENTATION_PLAN.md`. Plan này không viết lại chi tiết. | BX, Qw | T6.2 | DONE theo định nghĩa trong master plan (biên dịch 0 lỗi, input map 100%, parity có tài liệu, kiểm thử thất bại, kiểm tra fill trên DEMO, không có quyền live) | E3 |

---

## 7. Điều kiện cần và đủ theo gate (tóm tắt)

| Gate | Điều kiện cần | Điều kiện đủ |
|---|---|---|
| G1 | Host kiểm thử xác định (T0.1), profile đóng băng (T0.3) | T1.1–T1.8 PASS, D1–D6, D8 đóng, E3 |
| G2 | G1 | T2.1–T2.6 PASS, look-ahead harness phát hiện được strategy gian lận, báo cáo tái lập |
| G3 | G1, T0.3 | T3.1–T3.7 PASS, không đường nào ra khỏi paper broker, replay bền qua restart |
| G4 | G3, G2 (cho báo cáo) | T4.1–T4.3 PASS hoặc phần trình duyệt ghi BLOCKED có lý do |
| G5 | G2, G3 | Cửa sổ quan sát hoàn tất + quyết định bằng văn bản |
| Live | **Không thuộc plan này.** Cần quyết định riêng của Vinh, rà soát bảo mật và ký rủi ro độc lập | — |

## 8. Workstream của Cla (CTO Code-Debug)

1. **Đặc tả** (trước khi BX bắt tay): S1 Profile/InstrumentSpec/Config (T0.3, T1.6); S2 Risk v2 và máy trạng thái kill switch (T1.2); S3 Ngữ nghĩa backtest — thời điểm khớp, quy tắc trong-nến, phí/slippage (T2.1); S4 Envelope + idempotency (T3.1, T3.3); S5 Hợp đồng API (T4.1).
2. **Review gate:** G1–G5. Mỗi review ghi: đã đọc file nào, kiểm tra gì, kết luận PASS/FAIL, lý do. Review chỉ dựa trên evidence, không dựa trên việc file tồn tại.
3. **Debug:** task FAIL được Cla triage trong cùng vòng — tái hiện, xác định nguyên nhân gốc, đề xuất bản vá có test hồi quy. Không "sửa cho qua" bằng cách nới tiêu chí.
4. **ADR log:** mỗi phụ thuộc mới, thay đổi giả định A1–A6 hoặc lệch kiến trúc ghi một ADR ngắn trong `03_ARCHITECTURE/`.
5. **Giữ plan sống:** sau mỗi gate cập nhật `references/task-graph.md` và trạng thái task.

## 9. Sổ rủi ro

| ID | Rủi ro | Tác động | Giảm thiểu |
|---|---|---|---|
| R1 | Không có execution host được ủy quyền | Mọi task E2 BLOCKED, gate không mở | T0.1 chốt sớm; không hạ chuẩn để qua gate |
| R2 | Overfitting khi backtest | Kết quả đẹp nhưng vô nghĩa | T2.3 tách đoạn test; báo cáo luôn kèm tuyên bố giới hạn |
| R3 | Rò rỉ tương lai | Báo cáo sai hệ thống | T2.2 với đối chứng âm |
| R4 | Trộn kết quả BTC spot và XAUUSD CFD | Kết luận sai | Profile tách (A1/A2), test chéo profile T3.4 |
| R5 | Scope creep sang MT5 và dashboard trước khi lõi vững | Chậm, nợ kỹ thuật | Thứ tự track; M6 bị khoá bởi G3 + host |
| R6 | Dashboard/bản demo bị hiểu là dữ liệu thật | Quyết định sai | T4.2 nhãn rõ, trạng thái stale/unavailable |
| R7 | Bí mật lọt vào source/log | Rủi ro bảo mật | Khoá chỉ qua biến môi trường; T1.7 có test che; quét chuỗi khoá trước mỗi gate |
| R8 | Plan lệch thực tế (đã xảy ra với v1.0) | Mất truy vết | T0.4; cập nhật task-graph sau mỗi gate |
| R9 | Dữ liệu thị trường thật không lấy được | Không có backtest thật | A5: engine kiểm bằng dữ liệu tổng hợp; T2.7 ghi BLOCKED nếu cần |

## 10. Năm việc bắt đầu ngay

1. **Xu:** chốt T0.1 (execution host hoặc NO-HOST) và ghi vào journal. Đây là điều kiện cần của gần như mọi gate.
2. **Cla:** soạn S1 (`PROFILES.md` + InstrumentSpec) và S2 (đặc tả Risk v2) để BX có đặc tả trước khi viết code.
3. **BX:** bắt đầu các task không có phụ thuộc: T1.3 (số hữu hạn), T1.4 (strategy bất biến), T1.7 (event log).
4. **BX → Qw:** T0.2 baseline ngay khi có host, so với 6/6 của Cla (E1) và 27/27 BX đã báo.
5. **Xu:** T0.4 đồng bộ trạng thái v1.0 để mọi người cùng nhìn một bảng.

---

*Plan này chỉ lập kế hoạch. Mọi trạng thái trong tài liệu là trạng thái tại thời điểm viết; chưa có PASS nào được tuyên bố cho Work 200. Giao dịch tiền thật: NO-GO.*

**Đính chính (Cla, 2026-10-25):** ở T6.3, cụm "kiểm thử thất bại" nghĩa là "kiểm thử đường lỗi (failure-path tests)", không phải cho phép test thất bại.
