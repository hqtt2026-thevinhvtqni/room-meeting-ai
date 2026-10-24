# Work 200 — Construction Journal
**Date:** 2026-10-24  
**Actor:** Xu / ROOM-HOP MCP member identity `xu`  
**Role:** AI coordinator and initial project setup

## Entry 001 — Create Work
- **Action:** Called ROOM-HOP MCP 8030 `sandbox_create_work`.
- **Result:** PASS — service returned `status=ok`, `work_id=200`, `work_name=CRYPTO-TRADING-BOT`, `identity_id=xu`, authorization `ALLOW: xu is a registered ROOM HOP member`.
- **Evidence:** Work creation response; Sandbox listing showed the standard project structure and `00_ROOT/WORK_MANIFEST.md`.
- **Boundary:** Created in Sandbox only; no GitHub changes or source merges performed.

## Entry 002 — Initial project framing
- **Action:** Prepare manifest, project brief, initial architecture, and acceptance criteria.
- **Scope:** Backtesting and paper trading first; live trading excluded from initial milestone.
- **Verification status:** Project creation verified. Document-write verification and code/test execution are pending; do not call implementation DONE.


## Entry 003 — Initial safe trading core
- **Action:** Wrote initial Python package and tests through MCP 8030.
- **Files:** domain models, OHLCV validation, moving-average crossover strategy, risk manager, paper-only broker, pyproject, and pytest tests.
- **Safety boundary:** no exchange connector, live order submission, withdrawal, or API credentials included.
- **Tool evidence:** each of the 9 file writes returned `status=ok`.
- **Verification:** test files were written but have not been executed; MCP 8030 tools available in this session do not expose a code-execution command. Status remains ACTIVE / P0-P1 IN PROGRESS, not PASS.


## Entry 004 — Dashboard prototype
- **Action:** Added responsive static dashboard through MCP 8030.
- **Artifacts:** `04_CODE/dashboard/index.html`, `04_CODE/dashboard/README.md`, `02_EXTENSION/DASHBOARD_SCOPE_AND_INTEGRATION_PLAN.md`.
- **Features:** portfolio KPI cards, mock equity curve with 1D/1W/1M tabs, risk-limit visualization, demo-only stop control, watchlist, sample paper trades, and system-readiness indicators.
- **Safety:** all values are explicitly labelled mock/demo; no exchange API, live order execution, credentials, or backend integration.
- **Write evidence:** all 3 MCP write operations returned `status=ok`.
- **Verification:** file listing confirms dashboard artifacts exist. Browser rendering and interaction tests have not been run; no visual QA PASS claimed.
- **Next:** connect read-only API after the backend contract is implemented, then run browser tests and verify stale/error states.

## Entry 004 — BX42MR V4.2.8 reference intake
- User authorized supplemental work in Work 200 Sandbox.
- Inspected ZIP with Pine v6 source and V4.2.7->V4.2.8 patch; SHA256 source `2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a`.
- Saved canonical Pine and patch to user's Library `/Work200-BaoXtra-V428/`.
- Registered integration plan, import record and checklist under `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/`.
- Complete Pine source transfer via MCP was blocked; deleted incomplete copy rather than retain invalid source. No Pine/pytest test run, no trading enabled.


## Entry 005 — Xu đánh giá hiện trạng Work 200 từ snapshot MCP
- **Ngày:** 2026-10-24.
- **Người đánh giá:** Xu — AI-01 / điều phối.
- **Nguồn:** `sandbox_list` và `sandbox_read_probe` qua MCP 8030; đây là kiểm tra file/source, không phải chạy chương trình.
- **Trạng thái tổng thể:** ACTIVE / PARTIAL IMPLEMENTATION / NOT VERIFIED. Không tuyên bố PASS.

### Những gì đã xác nhận có trong Sandbox
- Python core: `models.py`, `data_validation.py`, `strategy.py`, `risk.py`, `paper_broker.py`.
- Dashboard prototype: `04_CODE/dashboard/index.html` và README; chưa có bằng chứng kết nối backend hoặc chạy browser QA.
- BX42 reference extension có source Pine, hướng dẫn, import record, checklist và `WORK200_BX428_INTEGRATION_PLAN.md`.
- `signal_intake.py` và `test_signal_intake.py` đã xuất hiện trong snapshot. Signal intake chỉ xác thực và trả `REVIEW_ONLY`, không đặt lệnh; có allow-list mặc định BTCUSDT / OKX / SPOT / 15m, kiểm tra thời gian và thứ tự SL/TP; dedup chỉ trong bộ nhớ.
- `IMPLEMENTATION_STATUS_20261024.md` vẫn ghi pytest NOT RUN.

### Phát hiện cần BX xử lý
1. **Chưa có MT5 Adapter:** trong danh sách file hiện tại chưa thấy module kết nối MT5, terminal health check, symbol metadata, order lifecycle hoặc position reconciliation. Không tuyên bố MT5-ready.
2. **Mâu thuẫn cấu hình/định hướng:** `signal_intake.py` mặc định BTCUSDT / OKX / SPOT / 15m, trong khi plan BX42 đề xuất test hình ảnh ban đầu XAUUSD M15 với HTF D1/H4/H1 và strategy Pine; đây là các sản phẩm/nguồn dữ liệu khác nhau. Cần tách profile cấu hình, không trộn kết quả XAUUSD CFD với BTC spot.
3. **Dedup chưa bền vững:** `_seen` nằm trong memory, mất khi process restart; không đủ chống replay trong production. Giữ ở review/paper scope và bổ sung persistence/idempotency test trước khi tích hợp execution.
4. **Risk Engine chưa đủ để làm live gate:** hiện kiểm tra notional và daily loss cơ bản; chưa thấy kiểm tra tick/lot step, min/max volume, SL/TP theo symbol, spread guard, stale tick, trạng thái terminal, trạng thái vị thế thật và reconciliation. Hiện chỉ phù hợp làm nền paper, chưa cho live.
5. **Kiểm thử chưa xác minh:** source test hiện có không chứng minh test pass; phải chạy pytest trong môi trường xác định và ghi command, exit code, số pass/fail/blocked. Nếu không có execution environment thì ghi BLOCKED.
6. **Strategy integration chưa chứng minh:** intake trả `REVIEW_ONLY`; chưa thấy pipeline nối tín hiệu BX42 -> data integrity -> risk approval -> paper fill. Không tự nâng trạng thái thành order accepted/filled.
7. **Dashboard còn demo:** cần backend contract và test trạng thái disconnected/stale/error; nút stop UI-only không được mô tả như kill switch thực.
8. **Bàn giao theo nhật ký:** BX đọc entry này, tiếp tục triển khai đúng phạm vi, ghi từng thay đổi và bằng chứng; không bật live trading, không thêm credential, không ghi PASS nếu chưa có test evidence.

### Quyết định nghiệm thu tại snapshot này
- **PASS:** xác nhận các file nêu trên tồn tại và đọc được qua MCP 8030.
- **BLOCKED / NOT RUN:** pytest, browser QA, backtest, MT5 terminal integration, strategy parity, paper end-to-end.
- **NO-GO:** giao dịch tiền thật.
- **Điều kiện bước kế:** chốt profile thị trường/adapter, xây contract adapter và pipeline paper-only, chạy test có bằng chứng, cập nhật implementation status và nhật ký.

## Entry 005 — BX42MR V4.2.8 source integrity and signal intake
- Imported complete 1758-line Pine source under 02_EXTENSION/BaoXtra_BX42MR_V4_2_8; read-back SHA-256 equals ZIP original: 2cb18bd304a6951c2ffc7fea70a6510bfa5f4b07cc1b985b793201369e27bf3a.
- Installed crypto_bot/signal_intake.py and test_signal_intake.py. Local Python 3.13.5 / pytest 9.0.2: 27/27 tests passed, no compile errors.
- Added alert format contract (BX421, BX42_MR), updated acceptance checklist, and saved verification report.
- Evidence file: 06_EVIDENCE/BX428_INTEGRATION_VERIFICATION_20261024.md.
- Unverified: Pine compilation/backtest, original Python core tests, persistent/authenticated adapter, paper end-to-end risk/portfolio execution.
- Live execution remains forbidden. Local tests do not imply a full project PASS.


## Entry 006 — Tiến độ kiểm tra lại Work 200
- **Thời điểm:** 2026-10-24 09:27 ICT (Asia/Ho_Chi_Minh).
- **Người kiểm tra:** Xu — AI-01.
- **Phương pháp:** đọc lại danh sách file và evidence qua MCP 8030; không chạy code trong lần kiểm tra này.
- **Tiến triển mới so với snapshot trước:** đã xuất hiện `ALERT_COMPATIBILITY_CONTRACT_V01.md` và `BX428_INTEGRATION_VERIFICATION_20261024.md`; Pine source 1758 dòng được ghi nhận đã copy đủ và SHA-256 khớp bản ZIP gốc; report ghi signal-intake tests 27 passed trên Python 3.13.5 / pytest 9.0.2 ở local container.
- **Phạm vi bằng chứng:** 27 tests chỉ dành cho `test_signal_intake.py` / module `REVIEW_ONLY`; không đại diện cho toàn bộ Work 200. Original `test_core.py` chưa chạy; Pine chưa compile/backtest trên TradingView; chưa có adapter xác thực/persistence, paper end-to-end, dashboard backend integration hay MT5 adapter.
- **Quan sát source:** intake hiện từ chối chuỗi alert BX421/BX42_MR dạng pipe; contract nêu rõ cần parser review-only riêng, authenticated transport, event ID bền vững và không tự biến BACKTEST/PAPER/SL_UPDATE thành lệnh BUY/SELL.
- **Trạng thái:** PARTIAL PROGRESS / NOT RELEASED. PASS giới hạn: nguồn Pine checksum match theo evidence record và module signal intake 27/27 test local theo verification report. Xu chưa tự chạy lại các test trong lần kiểm tra này.
- **Còn thiếu ưu tiên:** contract parser tương thích alert BX42 review-only; cấu hình tách BTC spot khỏi XAUUSD CFD; persistent idempotency; tích hợp risk->paper; MT5 adapter; dashboard API; chạy toàn bộ core tests/backtest; lưu evidence lệnh chạy và exit code.
- **An toàn:** NO-GO giao dịch tiền thật; không có bằng chứng MT5-ready.

## Entry 006 — MT5/MQL5 Swing Semi-Auto v0.1 source handoff
- Added 517-line MQL5 EA, .set config, VI/EN README, static pytest source checks under `02_EXTENSION/BaoXtra_BX42MR_V4_2_8/MT5_PORT_V0_1/`.
- Verified all five text files against their respective Library originals, including final newlines.
- MQL5 SHA256: `94ac4f83904df5d7ffee1f81921660d2e5f481fc262dd45b0541d3c18a966356`.
- Local Python pytest contract suite: 7/7 PASS; package ZIP integrity PASS.
- Added separate parity matrix and integration status. Evidence: `06_EVIDENCE/BX428_MT5_SOURCE_VERIFY_20261024.md`.
- MetaEditor compile and Strategy Tester NOT RUN; MT5 Trade iPhone cannot execute .mq5. Terminal PC/VPS needed; optional mobile push only.
- Entire module is REVIEW ONLY and cannot place orders. No broker execution or live mode approved.

## Entry 007 — Full MT5 parity scope and acceptance plan
- Audited canonical Pine (1758 lines) vs MT5 V0.1 (517 lines); confirmed distinct Legacy SMC and RSI Momentum engines and default engine RSI Momentum.
- Extracted 179 input declarations into 14 groups, persisted 2 TSV manifests in MT5_FULL_PORT_V1.
- Authored modular architecture, 20-row feature parity matrix, test/acceptance gates and mode-separated implementation sequence.
- Verified local static tests: MT5 V0.1 source checks 7/7 PASS; Python signal intake 27/27 PASS. Both remain static/local evidence, not MT5 MetaEditor compiled output.
- Source parity of future full MQL5 port: NOT IMPLEMENTED. MetaEditor/Strategy Tester and demo execution: NOT RUN. LIVE disabled.


## Entry 008 — Biên bản đánh giá và giao Cla lập plan tiếp tục
- **Thời điểm:** 2026-10-25 ICT.
- **Người ghi:** Xu — AI-01 / điều phối HQTT.
- **Yêu cầu của Vinh:** ghi nhận biên bản và nhật ký; Vinh sẽ nhờ Cla lập plan theo đánh giá/định hướng của Xu rồi triển khai tiếp.
- **Đánh giá:** Work 200 vẫn ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED. Đã rà soát tài liệu/source qua MCP 8030; đây không phải lần chạy toàn bộ chương trình.
- **Phát hiện chính:** alert BX42 pipe chưa tương thích parser; dedup chỉ ở memory; profile BTCUSDT/OKX/SPOT cần tách khỏi BX42/XAUUSD; paper pipeline end-to-end chưa xác minh; dashboard còn demo; MT5 v0.1 chưa compile/replay trên terminal và full parity chưa triển khai.
- **Bằng chứng giới hạn:** 27/27 signal-intake tests và 7/7 MT5 source-contract tests được ghi nhận chạy ở local container; không đại diện cho toàn Work 200 hoặc xác nhận test trong Sandbox.
- **Giao Cla (AI-03 / CTO Code-Debug):** lập plan tiếp tục trong phạm vi Work 200, phân task/phụ thuộc/owner, điều kiện cần, tiêu chí nghiệm thu đủ và evidence bắt buộc. Ưu tiên tách profile, parser review-only, paper-only pipeline, test trong môi trường được ủy quyền, backtest và track MT5 theo gate riêng.
- **Giao BX:** triển khai theo plan được xác lập; ghi lệnh, môi trường, exit code, kết quả và giới hạn vào evidence/journal.
- **QA:** Qw xác minh độc lập khi artifact và evidence sẵn sàng; không suy ra PASS từ file tồn tại.
- **An toàn:** NO-GO giao dịch tiền thật; không credential, không live orders; không fake PASS.
- **Biên bản chi tiết:** 06_EVIDENCE/WORK200_MINUTES_20261025_01.md.
- **Trạng thái bước kế:** READY FOR CLA PLANNING; chưa phải release approval hay DONE.


## Entry 009 — Cla (AI-03 / CTO Code-Debug) lập PLAN v2.0 và đánh giá độc lập
- **Thời điểm:** 2026-10-25 ICT. **Người ghi:** Cla.
- **Phương pháp:** đọc nguyên văn tài liệu và source lõi qua MCP 8030; dựng lại các module lõi trong container của Cla (Python 3.12.3) và chạy `pytest` cho `test_core.py` cùng 7 probe có mục tiêu. Đây là evidence E1, không phải chạy trong Sandbox và không thay thế T0.2.
- **Kết quả đo:** `test_core.py` = 6 passed. Probe xác nhận D1 (trần vị thế/lỗ ngày vô hiệu khi dùng tham số mặc định), D2 (SELL giảm vị thế bị chặn), D5 (strategy có state ẩn), D6 (không phát hiện khoảng trống/trộn timeframe). Chưa chạy lại `test_signal_intake.py` (27/27 là số do BX báo).
- **Artifact:** `00_ROOT/PLAN_WORK200_v2.0.md`, `00_ROOT/references/task-graph.md`, `06_EVIDENCE/CLA_ASSESSMENT_20261025.md`. Không sửa file nào có sẵn; không xoá file nào.
- **Định hướng:** Track A (lõi: Portfolio, Risk v2, backtest) → B (bridge BX42) → C (API + dashboard); Track D (MT5) khoá cho đến khi G3 PASS và có host MetaEditor. Giả định A1–A6 áp dụng mặc định, có thể ghi đè.
- **Bàn giao:** Xu chốt T0.1 (execution host hoặc NO-HOST) và T0.4. BX bắt đầu T1.3, T1.4, T1.7 (không phụ thuộc) và chờ đặc tả S1/S2 của Cla cho T1.6, T1.1, T1.2. Qw QA độc lập theo cột `[QA]`.
- **Trạng thái:** ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED. Chưa có PASS nào cho Work 200. NO-GO giao dịch tiền thật. Plan ở trạng thái PROPOSED, chờ duyệt.


## Entry 010 — Ka CSA review độc lập và bổ sung Plan Work 200 v2.0
- **Thời điểm:** 2026-10-25 03:39 ICT (Asia/Ho_Chi_Minh).
- **Người ghi:** Ka — CSA / Independent Reviewer.
- **Phương pháp:** đọc qua ROOM-HOP MCP 8030: plan v2.0, task graph, assessment của Cla, biên bản Xu, implementation status và journal; kiểm tra danh sách Sandbox/Work metadata. Đây là review tài liệu/source, không chạy code.
- **Kết luận:** ACCEPT WITH CONDITIONS FOR PLANNING; không phải implementation PASS hoặc release approval.
- **Bổ sung:** K0 execution host/NO-HOST + baseline; K1 chốt profile/giả định; K2 Portfolio/Risk/Ledger/idempotency/audit và E2E failure-path; K3 backtest chống look-ahead và tái lập; K4 dashboard/MT5 giữ gate riêng; K5 evidence path, task graph và sai lệch metadata/cấu trúc Sandbox.
- **Phát hiện quản trị:** `sandbox_list_works` trả `work_name=06_EVIDENCE` cho Work 200; tồn tại cả `06_EVIDENCE/` ở root Sandbox và `CRYPTO-TRADING-BOT/06_EVIDENCE/`. Yêu cầu T0.5 inventory/đề xuất canonical path; không tự xóa hoặc di chuyển.
- **Artifact:** `CRYPTO-TRADING-BOT/06_EVIDENCE/KA_CSA_REVIEW_PLAN_WORK200_V2_20261025.md`.
- **Trạng thái:** Work 200 ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED; G1–G5 chưa PASS theo evidence hiện có; E2/E3 chưa được Ka xác minh trong host được ủy quyền; live trading NO-GO.
- **Bàn giao điều phối:** Xu xử lý M0 và quyết định host/profile; Cla tiếp tục cung cấp S1/S2 và review gate; BX thực hiện task theo dependency; Qw ký E3 khi đủ artifact/evidence. Vinh giữ quyền phê duyệt cuối cùng.


## Entry 011 — Clr (CRO) critical review độc lập Work 200 + PLAN v2.0
- **Thời điểm:** 2026-10-25 ICT. **Người ghi:** Clr — CRO (phản biện độc lập, không phải người thi công).
- **Phương pháp:** đọc qua MCP 8030 (plan v2.0, task-graph, manifest, acceptance criteria, source 04_CODE, source `02_EXTENSION/CORE_PAPER_SAFETY_V0_2`, hai file test, journal nested + journal root, assessment của Cla/Ka/Go, biên bản Xu). Không chạy code, không tạo chứng cứ. Bậc evidence: E0. Chưa đọc: dashboard `index.html`, Pine, MQL5, TSV, alert contract, BX428 verification.
- **Verdict:** CONCERN. Chưa cho BX code T1.1/T1.2/T1.4/T1.5 trước khi xử lý C1–C4. Không phải REJECT, không phải release approval.
- **Phát hiện chính:** (1) tồn tại nhánh core thứ hai `CORE_PAPER_SAFETY_V0_2` đã phủ một phần D1/D2/D4/D5/D6 nhưng plan/task-graph ghi NOT STARTED, không có test, không có entry journal; (2) plan không có task BrokerAdapter/MT5Adapter, mâu thuẫn Entry 005 (DECISION) trong journal root, không có ADR; journal root khác nội dung journal nested, không phải bản sao; (3) Track B: BX42 test ban đầu trên XAUUSD nhưng profile A1 là BTC spot và T3.4 từ chối alert XAUUSD; (4) chuẩn nghiệm thu "actual Sandbox environment" bị thay bằng "host ủy quyền" khi chưa có phê duyệt của Vinh; (5) lỗi thiết kế ở V0_2 (đọc source, chưa chạy): `execute_paper` pop trước submit, `event_id` dùng lại được sau execute, `realized_pnl` lifetime và bỏ qua lỗ chưa chốt, reset kill switch bị kích hoạt lại ngay; (6) mọi bằng chứng ≤ E1 và không độc lập; probe của Cla không lưu script.
- **Điều kiện:** C1 hoà giải hai nhánh core bằng ADR + cập nhật task-graph; C2 chốt T0.1 (host/NO-HOST) có owner + hạn và sửa tiêu chí nghiệm thu; C3 hợp nhất journal, ADR về MT5Adapter; C4 sửa Track B (profile cho BX42, tiêu chí G3 có alert thật). Bổ sung: C5 xác nhận khả năng ký HMAC của nguồn alert, C6 loss limit theo equity/ngày UTC + TTL pending + trần exposure danh mục, C7 lưu probe script + Ka/CRO ký chéo G1/G3, C8 gán cỡ S/M/L và điều kiện dừng ceiling.
- **Quản trị ghi nhận:** journal nested lặp số entry (004, 005, 006 mỗi số hai lần); Entry này đánh số 011 theo thứ tự cuối của nested journal; `CFO_ASSESSMENT_AND_FINANCIAL_PLAN_20261025.md` (Go) chưa có entry journal riêng.
- **Artifact:** `CRYPTO-TRADING-BOT/06_EVIDENCE/CRITICAL_REVIEW_CRO_WORK200_20261025.md`.
- **Trạng thái:** Work 200 ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED; G1–G5 NOT PASSED; live trading NO-GO.
- **Chờ quyết định của Vinh:** (1) execution host hoặc NO-HOST, và có cho E1 mở gate không; (2) nhánh core canonical (04_CODE hay V0_2); (3) BX42 thuộc profile A2 XAUUSD hay A1 BTC spot. Anh có chấp nhận rủi ro này nếu BX bắt đầu code M1 trước khi C1–C4 xong?


## Entry 009 — Xu hợp nhất kế hoạch chính thức Work 200 cho Coder
- **Ngày:** 2026-10-25 ICT.
- **Người lập:** Xu — AI-01 / điều phối HQTT.
- **Mục tiêu:** hợp nhất vòng đóng góp trước đó thành một master implementation plan duy nhất để Cla/BX dùng làm nguồn triển khai chung.
- **Artifact:** `00_ROOT/PLAN_WORK200_MASTER_v1.0.md`.
- **Ghi nhận:** hợp nhất baseline hiện trạng, kiến trúc, profile tách biệt, hợp đồng tín hiệu BX42, risk/paper boundary, work packages WP0-WP8, phụ thuộc, owner, acceptance gates, evidence requirements, thứ tự coder queue và non-goals.
- **Ưu tiên đầu:** Cla đóng băng task map/schema/profile và xác định execution host được ủy quyền; BX kiểm tra/chạy core tests có bằng chứng; tiếp theo parser BX42 review-only + persistent idempotency; sau đó paper-only end-to-end pipeline.
- **Các track tiếp theo:** backtest/reporting; dashboard read-only; Pine parity; MT5 compile/replay/parity theo gate riêng.
- **An toàn:** live trading vẫn NO-GO; không credentials; không tuyên bố test PASS khi chưa chạy trong môi trường có bằng chứng.
- **Trạng thái:** MASTER PLAN SAVED / READY FOR CODER TASKING. Chưa có implementation/test/release PASS nào được suy ra từ việc lưu plan.


## Entry 010 — Đồng bộ Work 200 lên GitHub
- **Ngày:** 2026-10-25 ICT.
- **Người thực hiện:** Xu — AI-01 / điều phối HQTT.
- **Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`.
- **Branch:** `work/200-crypto-trading-bot` (tạo từ `main`; chưa merge vào main).
- **Thư mục chuẩn:** `WORK-200-CRYPTO-TRADING-BOT/`, theo quy ước thư mục Work đã kiểm tra trên các branch Work khác.
- **Đã đồng bộ từ Sandbox MCP 8030 sang GitHub:** `README.md`, `PLAN_WORK200_MASTER_v1.0.md`, `WORK200_MINUTES_20261025_01.md`, `WORK_JOURNAL_20261024.md`.
- **Commit SHA cho các lần ghi file:** README `14e9bd7d6123946c51cff89627a8626cc4a21ec3`; master plan `89cb280e4716606bf3df47ccb57f474d772c84f3`; minutes `1023840e509e183e81ba664e984c1272d0f89b94`; journal initial sync `cf18878a2b8447ec2153b1517a815b71d2eed863`.
- **Quy tắc đồng bộ hai chiều:** khi một artifact đổi ở Sandbox hoặc GitHub, AI phụ trách phải đối chiếu revision trước, đồng bộ bản mới sang nơi còn lại, đọc lại hai bản và ghi hash/commit/evidence vào journal. README nêu rõ hiện chưa cài daemon/webhook đồng bộ tự động; không được tuyên bố auto-sync.
- **Giới hạn:** thao tác này đồng bộ tài liệu/biên bản/nhật ký; chưa đồng bộ toàn bộ mã nguồn Work 200 từ Sandbox sang GitHub, chưa mở PR và chưa merge main.
- **Trạng thái:** BRANCH CREATED / DOCUMENTS PUBLISHED; cần read-back verification trước khi kết luận sync PASS.


## Entry 011 — Read-back verification GitHub ↔ Sandbox
- **Ngày:** 2026-10-25 ICT.
- **Người xác minh:** Xu — AI-01.
- **Kết quả:** PASS cho đồng bộ tài liệu trong phạm vi đã nêu.
- **Bằng chứng:** đọc lại trực tiếp từ Sandbox MCP 8030 và GitHub branch `work/200-crypto-trading-bot`; nội dung khớp chính xác từng ký tự cho master plan, minutes và journal sau cập nhật.
- **GitHub paths:** `WORK-200-CRYPTO-TRADING-BOT/PLAN_WORK200_MASTER_v1.0.md`, `WORK-200-CRYPTO-TRADING-BOT/WORK200_MINUTES_20261025_01.md`, `WORK-200-CRYPTO-TRADING-BOT/WORK_JOURNAL_20261024.md`.
- **Giới hạn:** README đồng bộ quy trình cũng đã tạo trên branch; chưa có daemon/webhook tự động. Chưa đồng bộ toàn bộ code/source Work 200; chưa merge branch vào main.
- **Commit gần nhất trước entry này:** journal `63b5d82bbd0d4e96f056db662c1d2cf1fffac309`.
- **Trạng thái tổng:** DOCUMENT SYNC VERIFIED; FULL WORK SOURCE SYNC NOT CLAIMED; BRANCH NOT MERGED.


## Entry 012 — Đồng bộ cây Work 200 lên thư mục chuẩn GitHub
- **Ngày:** 2026-10-25 ICT.
- **Người ghi:** Xu — AI-01.
- **GitHub:** `WORK-200-CRYPTO-TRADING-BOT/` trên branch `work/200-crypto-trading-bot`.
- **Phạm vi đã chép:** các file text/source có thể đọc qua MCP trong cây `CRYPTO-TRADING-BOT/`, gồm plan gốc và master plan, brief, architecture, BX42 Pine và tài liệu, MT5 v0.1/full-port specification, Python core, dashboard, tests, acceptance criteria, các đánh giá của Cla/CFO/CRO/Ka, evidence và journal.
- **Cách tổ chức:** giữ cấu trúc thư mục tương ứng `00_ROOT` … `07_RELEASE` bên trong thư mục Work trên GitHub; giữ thêm các file lối vào cấp Work (README, master plan, minutes, journal) để điều hướng nhanh.
- **Loại trừ có chủ đích:** `desktop.ini` là metadata Windows không cần quản lý trong repo; file `.gdoc` là shortcut Google Docs, không phải nội dung tài liệu gốc nên không giả lập thành file nội dung. Chưa xác minh/đồng bộ các artifact ngoài danh sách MCP có thể đọc.
- **Trạng thái:** source/document tree snapshot published on work branch. Branch chưa merge vào main. Chưa có đồng bộ tự động nền; cập nhật tiếp tục theo quy trình agent-driven/manual đã ghi trong README.
- **Lưu ý:** thao tác đồng bộ không có nghĩa các code/test đã chạy hoặc Work 200 đã PASS; trạng thái vẫn ACTIVE / PARTIAL / NOT RELEASED.
