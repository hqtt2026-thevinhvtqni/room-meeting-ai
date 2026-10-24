# KA CSA — INDEPENDENT REVIEW & SUPPLEMENT TO PLAN WORK 200 v2.0
**Ngày/giờ:** 2026-10-25 03:39 ICT (Asia/Ho_Chi_Minh)
**Người đánh giá:** Ka — CSA / Independent Reviewer
**Phạm vi:** Work 200 — CRYPTO-TRADING-BOT; đọc qua ROOM-HOP MCP 8030.
**Căn cứ đã đọc:** `00_ROOT/PLAN_WORK200_v2.0.md`, `00_ROOT/references/task-graph.md`, `06_EVIDENCE/CLA_ASSESSMENT_20261025.md`, `06_EVIDENCE/WORK200_MINUTES_20261025_01.md`, `06_EVIDENCE/IMPLEMENTATION_STATUS_20261024.md`, `06_EVIDENCE/WORK_JOURNAL_20261024.md`, cùng kết quả `sandbox_list` và `sandbox_list_works`.

## 1. Kết luận review kế hoạch CTO
**Kết luận: ACCEPT WITH CONDITIONS FOR PLANNING; NOT AN IMPLEMENTATION PASS; NOT RELEASE APPROVAL.**

Plan v2.0 của Cla có cấu trúc và định hướng hợp lý: Evidence E0–E3; tách Track A lõi paper → B BX42 → C API/dashboard; Track D MT5 bị khóa; có phụ thuộc, owner, tiêu chí nghiệm thu, risk register và cấm live trading. Các phát hiện D1–D11 được ánh xạ thành task cụ thể.

Ka đồng ý dùng v2.0 làm bản kế hoạch triển khai tiếp theo sau khi Xu/Vinh xác nhận các quyết định quản trị nêu dưới đây. Không có căn cứ để đánh dấu bất kỳ task/gate nào PASS chỉ từ lần đọc tài liệu này.

## 2. Bổ sung bắt buộc vào cách điều hành

### K0 — Execution host và baseline là P0
- Xu + Cla phải ghi rõ host kiểm thử được ủy quyền hoặc ghi **NO-HOST** vào evidence policy/journal.
- Khi NO-HOST, mọi task yêu cầu E2/E3 phải ghi BLOCKED, có owner và điều kiện gỡ; vẫn có thể làm source review và task không cần chạy code nhưng không được đổi chuẩn evidence.
- Baseline phải bao gồm cả core và signal intake; con số 6/6 (bản chép trong container Cla) và 27/27 (BX báo chạy local) là bằng chứng giới hạn, không gộp thành PASS toàn bộ.

### K1 — Chốt profile trước khi ghép luồng
- Giữ tách biệt `P-BTC-SPOT-OKX-15M` và `P-XAU-CFD-MT5`; không dùng chung config, dữ liệu, phí, tick/lot rules hoặc báo cáo.
- A1–A6 hiện trong plan là **giả định vận hành đề xuất**, không phải quyết định đã được Vinh ký. Xu cần ghi rõ chấp thuận/ghi đè; đặc biệt profile thị trường, spot long-only và quy tắc khớp lệnh backtest.
- Không kết nối BX42 alert thành order. Các loại PAPER/BACKTEST/SL_UPDATE phải giữ semantics riêng và REVIEW_ONLY cho đến khi hợp đồng được test.

### K2 — Không ghép pipeline trước khi sửa chặn rủi ro
- Portfolio/Ledger phải là nguồn trạng thái chuẩn cho Risk v2; không cho caller tự cung cấp trạng thái vị thế/PnL mặc định để bỏ qua limits.
- SELL chỉ được giảm/đóng vị thế spot hiện có; khi HALTED vẫn chỉ cho phép lệnh giảm exposure theo policy được test.
- Event log phải ghi được risk decision, paper fill, kill-switch transitions và lý do; idempotency phải sống qua restart.
- E2E tối thiểu phải kiểm tra đường chấp nhận và đường từ chối: invalid/stale data, vượt limit, duplicate/replay, kill switch, profile sai, parser alert không hợp lệ. Mỗi case phải có expected events và đối chiếu ledger.

### K3 — Backtest phải chứng minh tính trung thực, không chỉ tạo báo cáo
- Synthetic fixtures tất định là baseline hợp lệ; dữ liệu thị trường thật là tùy chọn, không được bịa hoặc thay thế khi thiếu.
- Bắt buộc kiểm tra look-ahead bằng test biến đổi dữ liệu tương lai và negative control strategy gian lận.
- Phí/slippage/spread, next-bar open, SL-before-TP trong cùng nến và train/validation/test boundaries phải được thể hiện trong test/report.
- Báo cáo phải có data/config hash và chạy lặp lại cho kết quả byte-for-byte theo tiêu chí plan.

### K4 — Dashboard và MT5 giữ gate riêng
- Dashboard không hiển thị mock như dữ liệu thật; phải hiển thị mode, source, as_of/freshness và unavailable/stale/error.
- Nút Stop UI không được gọi là kill switch thật nếu backend chưa xác nhận chuyển trạng thái.
- MT5 v0.1 7/7 source-contract tests không chứng minh MQL5 compile hoặc Strategy Tester. Full port W2–W10 giữ BLOCKED đến khi G3 PASS và có host MetaEditor/terminal demo được ủy quyền.

### K5 — Quản trị evidence và cấu trúc Sandbox
- `sandbox_list_works` đang hiển thị Work 200 với `work_name=06_EVIDENCE`, trong khi nội dung manifest/plan xác định CRYPTO-TRADING-BOT; đồng thời tồn tại thư mục `06_EVIDENCE/` ở root Sandbox và `CRYPTO-TRADING-BOT/06_EVIDENCE/`. Cần T0.5 lập inventory và đề xuất canonical path, không tự xóa/di chuyển.
- Task graph và plan phải đồng bộ sau mỗi thay đổi trạng thái. Mọi PASS cần evidence path, command, environment, exit code, test counts, input/code hash và giới hạn xác minh.
- Work 200 qua MCP 8030 hiện chứng minh được thao tác liệt kê/đọc/ghi Sandbox; chưa có tool chạy code trong phiên này. Không được suy ra MCP file access = execution capability.

## 3. Trình tự đề nghị để Xu điều phối
1. **M0 trước:** T0.1 execution host/NO-HOST; T0.3 profile decision; T0.4 đồng bộ trạng thái plan v1.0; T0.5 inventory cấu trúc. T0.2 baseline chạy khi có host.
2. **Song song có kiểm soát:** BX chỉ bắt đầu T1.3, T1.4, T1.7 như plan cho phép; Cla cung cấp S1/S2 trước các task phụ thuộc InstrumentSpec/Risk v2. Không mở rộng sang dashboard/MT5 để né đường găng.
3. **G1:** chỉ review sau khi T1.1–T1.8 đủ evidence; yêu cầu Qw ký E3 cho gate theo plan.
4. **G2/G3:** backtest chống look-ahead và bridge BX42 được kiểm riêng; không để PASS một track bù cho track còn thiếu.
5. **G4/G5 và MT5:** chỉ sau các phụ thuộc tương ứng; thiếu browser/MetaEditor host thì ghi BLOCKED với điều kiện gỡ.

## 4. Trạng thái sau review
- **Plan CTO:** ACCEPT WITH CONDITIONS FOR PLANNING.
- **Work 200:** ACTIVE / PARTIAL IMPLEMENTATION / NOT RELEASED.
- **Code/tests E2/E3:** chưa được Ka xác minh trong host được ủy quyền.
- **G1–G5:** NOT PASSED theo evidence hiện có.
- **Live trading:** NO-GO; không credential, không live orders.
- **Quyền quyết định:** Xu điều phối; Vinh giữ quyền phê duyệt cuối cùng. Ka là CSA reviewer độc lập, không tự phê duyệt release.

**Ký tên:** Ka — CSA / Independent Reviewer
**Thời điểm:** 2026-10-25 03:39 ICT
