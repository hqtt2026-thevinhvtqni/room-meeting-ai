# ROOM-HOP Browser Product UX V2 — TEST_ONLY UI

## Mục tiêu và ranh giới

Đây là static HTML/CSS/JavaScript UI fixture. Runtime luôn **DISCONNECTED**; giao diện và các kịch bản đều **TEST_ONLY**. Không có Browser Agent, Chromium điều khiển, website, Internet, Core/MCP hay external API. Task chỉ chọn kịch bản cục bộ đã chuẩn bị; quyền là cờ UI, không phải browser/security permission. Các activity/evidence đều mô phỏng; screenshot action không tạo ảnh/tệp và completion không xác minh tác vụ ngoài đời.

## Hành vi UI

- Browser tabs, mock navigation/address bar, TEST_ONLY task input, local permission gate, hold/resume, reset, timeline/evidence provenance.
- Tab/panel semantics, keyboard navigation bằng ArrowLeft/ArrowRight/Home/End, focus management cho mở/đóng tab, focus-visible styling, reduced-motion rule và responsive breakpoints.
- Mọi màn hình phải thể hiện rõ DISCONNECTED/TEST_ONLY; không hiển thị trạng thái đã kết nối hoặc kết quả website thật.

## Mở giao diện

Mở `index.html` trực tiếp bằng trình duyệt (`file://`). Không cần và không nên chạy `server.py`/`start.sh` để tái lập các kiểm tra UI-only dưới đây. Không nhập địa chỉ fixture được hiển thị như một URL website thật.

## Kiểm tra tái lập an toàn

Chạy tại thư mục `01_SOURCE/room-hop-browser-v1-prototype/`:

```bash
node --check app.js && node --check workflow.js
node --test tests/workflow.test.js
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py
```

Chỉ chạy `tests/test_static_contract.py` trong phạm vi UI-only: `tests/test_server.py` tạo `ThreadingHTTPServer` loopback/ephemeral trong fixture và không thuộc lệnh kiểm chứng này.

**Optional file-based browser smoke** cần Python Playwright và Chromium khả dụng tại `/usr/bin/chromium`:

```bash
python3 tests/browser_smoke.py
```

Script mở `index.html` bằng `file://`, kiểm tra 27 tương tác/ARIA/focus/state/permission/reset/responsive cases và ghi nhận HTTP(S) requests. Nó không tạo ảnh, không kết nối network/runtime và không phải Browser Agent E2E. Trong Cloud Sandbox, Chromium được chạy headless với `--no-sandbox`; không suy rộng cấu hình này sang môi trường production.

## Kết quả mới nhất (2026-11-22)

**Cloud Sandbox mirror / same-hash local file UI checks:**

- `node --check app.js && node --check workflow.js`: PASS (2 files).
- Node built-in tests: **18/18 passed**.
- Static-only pytest: **10/10 passed**.
- Playwright + system Chromium, `file://` UI smoke: **27/27 passed**; no HTTP(S) requests; không có screenshot file.
- Environment: Python 3.12.3, pytest 8.4.2, Node 22.23.4, Playwright Python 1.64.1, Chromium 156.0.8078.73.

**GitHub Actions CI for the same canonical source/test hashes:** branch `work092/one-shot-20261122`, commit `76549220114b4d20cff78e525343837b7e6c9f4c`, run [`44996828261`](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44996828261) **SUCCESS**. Actions ran static pytest **10/10** and Node **18/18** and uploaded JUnit artifact `work092-ui-only-pytest-report` (ID `14744740180`). CI did not run Playwright or Browser Runtime. The older run `44982525770` at SHA `dcd75f0...` applies to an earlier source snapshot only.

These results do not establish direct Work Sandbox execution: it remains **NOT RUN**. Structured verification report and source hashes: `02_EVIDENCE/test-results/ui-only-verification-2026-11-22.json`; current Actions details: `02_EVIDENCE/test-results/github-actions-status.json`. Work 092 remains **PARTIAL — NOT ACCEPTED**; T6/T8/T17, full accessibility/contrast audit, independent Xu review and runtime integration remain open/block.
