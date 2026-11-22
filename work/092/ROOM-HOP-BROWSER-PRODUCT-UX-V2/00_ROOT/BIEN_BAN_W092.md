# BIÊN BẢN WORK 092 — ROOM-HOP BROWSER PRODUCT UX V2

- **Ngày cập nhật:** 2026-11-22 (Asia/Ho_Chi_Minh)
- **Executor:** Manus executor trong phiên hiện tại; không đại diện Nu/Xu độc lập.
- **Kết luận:** **PARTIAL — NOT ACCEPTED**; Runtime **BLOCKED**.
- **Phạm vi hiện hành:** static HTML/CSS/JavaScript UI, mọi hành vi TEST_ONLY và runtime DISCONNECTED.

## Kết quả rà soát hiện tại

Chạy trên bản làm việc Work 092 trong Manus Sandbox bằng Chromium hệ thống qua `file://`; không khởi chạy HTTP preview/server, không probe host/port, không truy cập site/API/Internet. Kết quả: Node 18/18; static pytest 12/12; Playwright UI smoke 33/33; accessibility/responsive audit 70/70; 0 HTTP(S)/WebSocket request. Đây là UI fixture evidence, không phải Browser Runtime/E2E. Chi tiết máy chạy, check-by-check và giới hạn nằm trong `02_EVIDENCE/test-results/accessibility-audit.json` và `browser-ui-smoke.json`.

## T1–T17 acceptance matrix

| ID | Trạng thái | Evidence boundary |
|---|---|---|
| T1 | PASS — file UI | Trang tĩnh tải từ `file://`; không khởi chạy server. |
| T2 | PASS — emulation | UI render ở desktop, tablet, Android-like mobile emulation; screenshots ghi rõ UI-only. |
| T3 | PASS — mock UI | Nhập URL, Back, Forward, Reload chỉ đổi local fixture state. |
| T4 | PASS — mock UI | Mở/chọn/đóng tab; tablist chỉ chứa tabs; focus được phục hồi; tab cuối không đóng được. |
| T5 | PASS — UI + Node | Task parser, blank-input error, 3 scenario tests. |
| T6 | PARTIAL | READY/RUNNING/HELD/COMPLETE được kiểm tra cho script TEST_ONLY; không có agent Connected/Working/Done thật và không suy diễn tương đương. Chi tiết acceptance gốc sâu hơn không có trong hồ sơ hiện hành. |
| T7 | PASS — UI fixture | Browse 3 bước, Search 6 bước, Workflow 8 bước theo thứ tự; mọi action là simulated. |
| T8 | PASS — copy/UI | Mỗi bước trong ba kịch bản có action label và mô tả người đọc được; provenance nói rõ TEST_ONLY. Screen-reader thực tế chưa chạy. |
| T9 | PASS — UI fixture | Evidence có nhãn mô phỏng, timestamp/source và không có artifact thật. |
| T10 | PASS — demo only | TEST_ONLY DEMO COMPLETE chỉ xuất hiện sau script; không xác minh tác vụ đời thực. |
| T11 | PASS — UI | Hold/Resume khóa hoặc mở script cục bộ; không chuyển quyền cho agent. |
| T12 | PASS — UI + Node | Quyền cờ TEST_ONLY, mặc định không bật, gate theo scenario, reset thu hồi cờ. |
| T13 | PASS — Chromium | Viewport 1920×1080 CSS px, không tràn ngang; ảnh toàn trang 1920×1971. |
| T14 | PASS — emulation | Android-like Playwright emulation 390×844 CSS px, touch hoạt động, không tràn ngang; không phải thiết bị Android vật lý. |
| T15 | PASS — UI fixture | Browse/Search/Agent Workflow đều chạy hết số action mong đợi trong demo cục bộ. |
| T16 | PASS — UI | Reset xóa grants/history; reload mock view đi Loading về DISCONNECTED/Ready. |
| T17 | PARTIAL | `file://` smoke/audit ghi nhận 0 HTTP(S)/WebSocket request; mã client không có fetch/XHR/WebSocket. Preview source loopback/ephemeral; service/backend isolation NOT RUN vì không khởi chạy/probe. |

## Accessibility / responsive evidence

70/70 kiểm tra tự động PASS; tên/label được kiểm tra bằng heuristic mã nguồn/DOM, tablist chỉ chứa role=tab, keyboard arrows/Home/End và focus restoration hoạt động, state/ARIA/validation được kiểm tra, reduced-motion spinner giới hạn 0.00001s. Các cặp màu chữ/nền được lấy từ computed style với ngưỡng 4.5:1; mọi cặp đã kiểm tra đạt, cặp thấp nhất 4.71:1. Desktop 1920×1080, tablet 768×1024 và Android-like emulation 390×844 đều không tràn ngang. Đây không phải chứng nhận WCAG đầy đủ; screen-reader/assistive technology và Android vật lý **NOT RUN**.

## Port / preview

`server.py` đã chuyển từ bind rộng/cổng cố định sang `127.0.0.1` và port `0` để OS chỉ định ephemeral port nếu người có quyền chủ động chạy thủ công. Không có server được khởi chạy, không probe host/port, không chiếm cổng hoạt động. HTTP health route, preview runtime và backend isolation **NOT RUN**. Hướng dẫn hiện hành ưu tiên mở `index.html` bằng `file://`.

## GitHub / executor / quyết định

Trước các thay đổi hiện tại, branch `work092/one-shot-20261122` có head `72b50a902a504b12a50270faa909b0bf08c9ae7a`; CI đã xác minh trước đó tại source SHA `12f74b03e8397c5e366f932d40280cfc28e1d168`, run `44997247247`, artifact `14743304960`. CI đó không kiểm tra source mới. CI cho commit source/test mới **chưa chạy tại thời điểm cập nhật bản phút này**; sẽ chỉ ghi PASS sau khi có run/sha/artifact thật. Không merge `main`.

Các hồ sơ historical `e2e-result.json`/`v2-e2e-result.json` từng ghi `agent_state: Done`, `PASS`, hoặc URL `127.0.0.1:8787`; chúng không được dùng làm bằng chứng hiện hành cho TEST_ONLY/disconnected UI hoặc preview isolation.

**Quyết định:** Work 092 vẫn **PARTIAL — NOT ACCEPTED**. T6 và T17 còn một phần chưa được chứng minh; direct Work Sandbox execution, server isolation, screen-reader/physical Android testing, Browser Runtime, Nu independent dispatch/ACK và Xu independent review đều **NOT RUN/BLOCKED**. Xu kiểm tra độc lập; Vinh quyết định cuối cùng.
