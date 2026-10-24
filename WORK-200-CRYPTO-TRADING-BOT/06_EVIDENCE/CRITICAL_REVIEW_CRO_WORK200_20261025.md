# CRITICAL REVIEW — CRO độc lập — Work 200 (hiện trạng Work + PLAN v2.0)

**Ngày:** 2026-10-25 · **Người lập:** Clr — CRO (phản biện độc lập, không phải người thi công)
**Phương pháp:** đọc qua MCP 8030 (`sandbox_list_works`, `sandbox_list`, `sandbox_read`). KHÔNG chạy code, KHÔNG tạo chứng cứ. Bậc evidence của review này: **E0** (đọc source/tài liệu). Các nhận định về hành vi code bên dưới đến từ đọc source, ghi rõ "chưa chạy".

**Đã đọc:** `PLAN_WORK200_v2.0.md`, `WORK_MANIFEST.md`, `references/task-graph.md`, `ACCEPTANCE_CRITERIA.md`, `04_CODE/crypto_bot/{models,risk,paper_broker,signal_intake}.py`, `05_TEST/tests/{test_core,test_signal_intake}.py`, `02_EXTENSION/CORE_PAPER_SAFETY_V0_2/crypto_bot/{models,data_validation,strategy,risk,paper_broker}.py`, `06_EVIDENCE/{WORK_JOURNAL_20261024,WORK200_MINUTES_20261025_01,CLA_ASSESSMENT_20261025,KA_CSA_REVIEW_PLAN_WORK200_V2_20261025,CFO_ASSESSMENT_AND_FINANCIAL_PLAN_20261025,IMPLEMENTATION_STATUS_20261024}.md`, và `06_EVIDENCE/WORK_JOURNAL_20261024.md` ở root Sandbox.
**Chưa đọc (không nhận định):** `dashboard/index.html`, file `.pine`, `.mq5`, hai TSV, `ALERT_COMPATIBILITY_CONTRACT_V01.md`, `BX428_*_VERIFY*.md`, `INITIAL_ARCHITECTURE_PLAN.md`, `PLAN_WORK200_v1.0.md`, `data_validation.py`/`strategy.py` của 04_CODE (chỉ dùng mô tả D5/D6 của Cla).

---

## 1. Verdict: **CONCERN**

Hướng đi đúng (paper-only, fail-closed, evidence-first, NO-GO tiền thật) và các tài liệu không nói quá bằng chứng. Nhưng plan v2.0 được lập trên một bức tranh hiện trạng **chưa đầy đủ** (bỏ sót một nhánh core đã tồn tại), **mâu thuẫn với một quyết định kiến trúc đã ghi**, và Track B có **mâu thuẫn mục tiêu nội tại**. Chưa nên cho BX bắt đầu code T1.1/T1.2/T1.4/T1.5 cho đến khi các điều kiện C1–C4 (mục 3) được xử lý. Không phải REJECT vì không có lỗi làm mất an toàn paper-only; các lỗi dưới đây là lỗi thiết kế/quản trị cần sửa trước khi tốn công thi công.

---

## 2. Phản biện chi tiết

### [LOGIC]

**L1 — Có một nhánh core thứ hai mà plan không biết đến.**
`02_EXTENSION/CORE_PAPER_SAFETY_V0_2/crypto_bot/*` đã chứa (đọc nguyên văn):
- `models.py`: kiểm tra `isinstance(Decimal)` + `is_finite()` cho Candle/OrderRequest → đóng phần lớn **D4**.
- `strategy.py`: "Stateless", không còn `_previous_relation` → đóng **D5**.
- `data_validation.py`: tham số `timeframe`, một symbol/series, phát hiện khoảng trống → đóng một phần **D6** (chưa có stale/trộn nhịp).
- `risk.py`: `reduce_only`, kiểm tra hữu hạn, tính `projected = current + delta` theo chiều lệnh → đóng một phần **D2**.
- `paper_broker.py`: broker tự giữ `cash`, `positions`, `cost_basis`, `realized_pnl`, SELL ≤ holdings (không short spot) → phủ một phần **D1**, **T1.1**, **A3**.

Nhưng: plan §3.3 và `task-graph.md` ghi T1.1–T1.5 **NOT STARTED**; probe D1–D6 chỉ chạy trên bản 04_CODE; `CLA_ASSESSMENT` §1 không liệt kê v0_2; không entry journal nào (001–010) nhắc v0.2; v0_2 **không có test nào** (`05_TEST/tests/` chỉ có `test_core.py`, `test_signal_intake.py`; `pyproject.toml` theo mô tả trỏ `pythonpath=.` tại `04_CODE`). Hậu quả: BX làm theo plan sẽ viết lại từ đầu thứ đã có (phá ceiling CFO), hoặc trộn/ghi đè giữa hai nhánh; G1 "hash cây `04_CODE`" sẽ chứng nhận nhánh không phải nhánh tốt hơn.

**L2 — Plan mâu thuẫn quyết định kiến trúc của Xu mà không có ADR.**
`06_EVIDENCE/WORK_JOURNAL_20261024.md` (root Sandbox) Entry 005 = DECISION: Python điều phối + **MT5 Adapter** + `BrokerAdapter`/`MT5Adapter`/`PaperBroker` protocol, giao BX. Plan v2.0 không có task BrokerAdapter/MT5Adapter nào, khoá MT5 ở Track D, và không nêu bác/sửa quyết định đó. Ka (K5) và Cla (D11) mới ghi nhận thư mục `06_EVIDENCE/` ở root "trùng tên"; nội dung thực tế **không phải bản sao** mà là một journal khác với Entry 005/006 khác hẳn journal trong `CRYPTO-TRADING-BOT/06_EVIDENCE/`. Đang có hai nguồn sự thật.

**L3 — Track B tự mâu thuẫn mục tiêu.**
A1 = BTCUSDT/OKX/SPOT; A3 = spot long-only; T3.4 từ chối alert XAUUSD ở profile BTC. Trong khi, theo journal (nested Entry 005 của Xu) và integration plan, BX42 được test ban đầu trên **XAUUSD M15, HTF D1/H4/H1** — tức profile A2, mà A2 không có track thực thi (M6 bị khoá). Hệ quả suy ra: alert thật của BX42 sẽ bị từ chối ở A1; G3 chỉ PASS được trên fixture tổng hợp; một nửa tín hiệu (SELL) vô nghĩa với spot long-only. G3 khi đó không chứng minh được "bridge BX42". *(Chưa đọc file Pine nên chưa xác nhận Pine có chạy được trên BTC; điểm này cần Cla xác nhận.)*

**L4 — T3.1 (HMAC) có thể không khả thi với nguồn alert thật.**
Theo hiểu biết của tôi (chưa xác minh trong phiên này): webhook từ alert TradingView gửi nội dung mẫu tĩnh và không tự ký HMAC. Plan không nói ai ký. Nếu cần relay đáng tin giữ khoá, đó là một thành phần mới + bề mặt tấn công mới chưa có trong scope, kèm câu hỏi khoá nằm đâu/quay vòng thế nào.

**L5 — Plan âm thầm đổi chuẩn nghiệm thu.**
`ACCEPTANCE_CRITERIA.md`: "tests run in the **actual Sandbox environment**". Plan: E2 = "host kiểm thử được ủy quyền", A5 = dữ liệu tổng hợp. Mà Sandbox 8030 không có công cụ chạy code (journal Entry 003, `IMPLEMENTATION_STATUS`). Hoặc tiêu chí gốc không bao giờ đạt được, hoặc plan đã hạ chuẩn mà chưa có phê duyệt bằng văn bản của Vinh. Thêm nữa, T0.4 chỉ đồng bộ v1.0; `ACCEPTANCE_CRITERIA.md` vẫn toàn ô trống.

**L6 — Ceiling không có cơ sở đo.**
Plan §6 định nghĩa cỡ S/M/L nhưng **không task nào được gán cỡ**. CFO đặt ceiling "≤ 15–18 phiên đến G2" và "chi phí rất thấp/trung bình" mà không có số đo; không có điều kiện dừng khi vượt.

**L7 — Thiếu độc lập vai trò.**
Cla là tác giả plan, tác giả đặc tả S1–S5, người chạy probe, người triage debug **và** reviewer gate G1–G5 cho chính các đặc tả đó. Qw (E3) là bù trừ duy nhất, nhưng chưa có artifact/evidence nào của Qw; Ka chỉ review plan, không review code. Skill phản biện: người đặc tả/thi công không được là người duy nhất ký kiểm thử.

### [RISK] — Điều tồi tệ nhất & ma trận (Xác suất × Tác động)

Điều tồi tệ nhất trong phạm vi paper-only: một "PASS" gate được cấp trên nhánh code sai/không chạy được ở host thật, rồi backtest/paper "đẹp" bị đọc như năng lực thật và dẫn tới quyết định mở live. Rủi ro cụ thể:

| ID | Rủi ro cụ thể (file/hàm → hậu quả) | Xác suất | Tác động |
|---|---|---|---|
| R1 | Hai nhánh core (04_CODE vs V0_2), không ADR → làm lại/ghi đè/PASS nhầm nhánh | Cao | TB–Cao |
| R2 | V0_2 `paper_broker.execute_paper()` `pop` rồi mới `submit`: nếu `submit` ném `PermissionError` thì đề xuất biến mất, không audit. `queue_paper()` chỉ chặn `event_id in self.pending` → sau khi execute, cùng `event_id` queue/execute lần hai được (double fill). `reference_price` lưu trong pending không có TTL/staleness. *(đọc source, chưa chạy)* | TB | TB |
| R3 | V0_2 `risk.activate_kill_switch()` gọi `cancel_all_pending` → `pending.clear()` im lặng, không log (T1.7 chưa nêu việc drop pending). | TB | TB |
| R4 | V0_2 `realized_pnl` là lifetime (docstring tự nhận) và chỉ đổi khi SELL: (a) vị thế long đang lỗ nặng chưa bán → loss limit không bao giờ kích hoạt; (b) sau khi chạm `-max_daily_loss` một lần, `reset_kill_switch()` bị `enforce_loss_limit` ở lần `approve` kế tiếp kích hoạt lại → bot không thể mở lệnh mới nữa trừ khi sửa kế toán. | Cao | TB |
| R5 | `max_position_notional` kiểm theo từng `order.symbol`, không có tổng exposure danh mục → nhiều symbol/profile vượt tổng trần. | TB | TB |
| R6 | 04_CODE `risk.approve` kiểm notional ở `reference_price` nhưng `paper_broker.submit` khớp ở giá đã cộng slippage → notional thực có thể vượt `max_order_notional` đúng bằng `slippage_rate` (V0_2 đã dùng giá khớp: hai nhánh khác hành vi). | Cao | Thấp |
| R7 | `signal_intake` tin cờ `paper_only`/`live_execution` do người gửi tự khai; `test_sell_valid` cho SELL hợp lệ trên SPOT (ngược A3); `_seen` RAM, không giới hạn. Plan xử lý ở M3, nhưng nếu M3 bị rút ngắn vì áp lực tiến độ thì đây là đường vào duy nhất từ bên ngoài. | Thấp (hiện chưa nối) | Cao |
| R8 | Journal: nested journal lặp số entry (Entry 004×2, 005×2, 006×2); root journal có Entry 005/006 khác nội dung; file CFO (04:16) không có entry journal (journal dừng ở Entry 010 của Ka, 03:39). Điều kiện DONE "journal có entry gate" không có khoá định danh duy nhất. | Cao | TB |
| R9 | T0.1 là nút thắt duy nhất của đường găng; nếu NO-HOST kéo dài, áp lực sẽ chuyển thành "PASS-LIMITED" tích luỹ (đã xuất hiện trong ngôn ngữ báo cáo). CFO đề xuất tạm dừng nhưng không có owner/hạn chót ("1–2 phiên"). | Cao | Cao |
| R10 | Probe D1/D2/D5/D6 là "script ad-hoc", không có file nào trong Sandbox → Qw không tái chạy được; P4 lần đầu sai và được viết lại (trung thực, nhưng càng cần lưu script). | Cao | TB |

### [EVIDENCE] — Chứng cứ có độc lập không?

| Tuyên bố | Nguồn | Bậc | Độc lập? |
|---|---|---|---|
| core 6/6 | Cla, container riêng, bản chép từ nội dung đọc qua MCP, không đối chiếu hash | E1 | Không: người chạy = tác giả plan; không phải file trong Sandbox |
| signal intake 27/27 | BX tự báo, Python 3.13.5 local | E1 (báo cáo) | Không: tác giả code tự kiểm; chưa ai chạy lại (Xu và Cla đều ghi chưa chạy). Tôi chỉ đếm tĩnh: 1+1+22 (parametrize)+1+1+1 = 27 ca, khớp số báo — đó không phải bằng chứng chạy. |
| MT5 7/7 | BX | E1 tĩnh (so khớp chuỗi) | Không chứng minh compile |
| SHA-256 Pine khớp | BX | E0 | Chưa ai tính lại độc lập |
| CORE_PAPER_SAFETY_V0_2 | — | Không có evidence | — |
| D1/D2/D5/D6 | Cla probe | E1 | Script không lưu |

Kết luận: toàn bộ bằng chứng hiện có ≤ E1 và hầu hết do chính người viết code/plan tạo ra. Không có cơ sở nào để đồng ý bất kỳ PASS nào. Điểm cộng: các tài liệu đều tự ghi rõ giới hạn, không tuyên bố PASS.

---

## 3. Đề xuất giảm thiểu (điều kiện trước khi tiếp tục)

**Trước khi BX viết code M1 (chặn):**
- **C1 — Hoà giải core.** Xu + Cla lập `CORE_RECONCILIATION.md`: diff từng file 04_CODE ↔ CORE_PAPER_SAFETY_V0_2, quyết định nhánh canonical bằng ADR (đề xuất xem xét V0_2 làm nền vì đã đóng D2/D4/D5, nhưng chỉ chọn sau khi có test), cập nhật `task-graph.md`: T1.1/T1.3/T1.4/T1.5 chuyển PARTIAL kèm phần còn thiếu. Không xoá/di chuyển file khi chưa có yêu cầu rõ của Vinh.
- **C2 — Quyết định host (T0.1) có owner + hạn chót.** Vinh ghi một dòng: host nào, hoặc NO-HOST. Nếu NO-HOST: Vinh quyết định bằng văn bản có cho E1 làm cơ sở mở gate hay không (khuyến nghị: không) và sửa dòng "actual Sandbox environment" trong `ACCEPTANCE_CRITERIA.md` cho khớp.
- **C3 — Hợp nhất nguồn sự thật.** ADR về Entry 005 (MT5Adapter): giữ hay thay; nếu giữ, thêm task `BrokerAdapter` protocol (chỉ interface + implementation paper) vào M1; chọn một journal canonical, đánh số entry duy nhất (thêm hậu tố, không xoá), ghi bổ sung entry cho CFO và CRO.
- **C4 — Sửa Track B trước M3.** Chọn một: (a) gán BX42 cho profile A2 (XAUUSD) với parser/fixture/intake không cần host MT5; hoặc (b) Cla xác nhận Pine phù hợp BTC spot rồi định nghĩa lại nghĩa của SELL. Thêm tiêu chí G3: ít nhất một alert BX42 thật (đã che dữ liệu nhạy cảm) được parse đúng profile, không chỉ fixture tổng hợp.

**Bổ sung vào plan:**
- **C5 — T3.1:** Cla xác nhận nguồn alert có thể ký được hay không; nếu không, thiết kế relay + chỗ giữ khoá + quay vòng, đưa vào sổ rủi ro.
- **C6 — T1.1/T1.2:** loss limit theo equity đánh dấu thị trường (có unrealized) và theo ngày UTC có roll-over; trần tổng exposure danh mục; pending proposal có TTL, idempotency bền, audit mỗi lần drop; thêm ca test hồi quy cho R2–R6.
- **C7 — Evidence:** lưu probe vào `05_TEST/probes/` kèm lệnh + hash; Qw tái chạy độc lập; Ka hoặc CRO ký chéo G1 và G3 (không để người viết đặc tả là người ký duy nhất).
- **C8 — Ceiling:** gán cỡ S/M/L cho từng task, quy ra phiên, và đặt điều kiện dừng/re-plan khi thực tế vượt ceiling (đề xuất ngưỡng do CFO + Vinh chốt trước khi chạy).

**Được phép làm ngay (không rủi ro mới):** T0.4, T0.5, C1–C3, lưu probe scripts, đọc/đối chiếu hai journal. Task code M1 chờ C1.

---

## 4. Trạng thái sau review
- **Verdict CRO:** CONCERN.
- **Work 200:** ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED. G1–G5: NOT PASSED. Live trading: NO-GO.
- Review này là review độc lập dựa trên đọc source; không phải xác minh chạy và không phải release approval.

**Câu hỏi cho người quyết định — Anh Vinh:** Ba quyết định cần anh: (1) execution host hoặc NO-HOST, và có cho E1 mở gate không; (2) nhánh core canonical (04_CODE hay V0_2) sau khi hoà giải; (3) BX42 thuộc profile nào (A2 XAUUSD hay A1 BTC spot). **Anh có chấp nhận rủi ro này không** nếu BX bắt đầu code M1 trước khi C1–C4 xong?

*Ký: Clr — CRO · 2026-10-25*
