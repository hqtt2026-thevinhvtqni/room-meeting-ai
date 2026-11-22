# NU ACCEPTANCE REPORT — WORK 092

**Ngày:** 2026-11-22 Asia/Ho_Chi_Minh
**Executor:** Manus executor trong phiên hiện tại; không đại diện Nu hoặc Xu độc lập.
**Disposition:** **PARTIAL — NOT ACCEPTED**. Runtime remains **BLOCKED**. Xu retains independent acceptance; Vinh retains final product decision.

## 1. Executive summary

Đã hoàn thiện các sửa chữa trong phạm vi static Browser UI: TEST_ONLY/disconnected labels được giữ nguyên; tablist được chỉnh để chỉ có role=tab children, close-current-tab ở ngoài tablist và phục hồi focus; contrast màu được cải thiện; optional server đổi sang loopback + OS-ephemeral port. Kết quả hiện có: Node 18/18, pytest 12/12, `file://` smoke 33/33, accessibility/responsive audit 70/70, 0 HTTP(S)/WebSocket requests.

Đây là prototype acceptance evidence, không phải Browser Runtime, real-agent, real website, E2E service hoặc Xu acceptance.

## 2. Work status

- **Product:** static TEST_ONLY UI, runtime DISCONNECTED.
- **Overall:** PARTIAL — NOT ACCEPTED; no merge, no release.
- **Direct Work Sandbox/MCP test execution:** NOT RUN; kiểm thử được chạy trên Work 092 branch clone trong Manus Sandbox. Không khởi chạy server/service.
- **Nu independent dispatch/ACK:** NOT ESTABLISHED. Không giả danh Nu.
- **Xu independent review:** NOT RUN; không tự nghiệm thu thay Xu.

## 3. T6/T8/T17 acceptance matrix

| Criterion | Result | Evidence and limit |
|---|---|---|
| **T6 — agent-state transitions** | **PARTIAL** | UI fixture READY/RUNNING/HELD/COMPLETE và reset được kiểm tra; runtime giữ DISCONNECTED. Không có agent Connected/Working/Done thật. Hệ thống hiện hành không chứa tài liệu gốc chi tiết hơn ngoài row-level matrix; không suy diễn rằng các trạng thái fixture tương đương agent thật. |
| **T8 — human-readable actions** | **PASS — TEST_ONLY UI** | Browse 3, Search 6, Workflow 8 hành động có label/mô tả người đọc được, trạng thái SIMULATED/TEST_ONLY và timeline. Không chứng minh hành động website thật; assistive-technology review chưa chạy. |
| **T17 — isolation boundaries** | **PARTIAL** | Browser `file://` smoke/audit quan sát 0 HTTP(S)/WebSocket request; static contract kiểm tra không khai báo fetch/XHR/WebSocket client. Preview source bind `127.0.0.1`, port `0`; server không được khởi chạy, host/port không được probe, nên backend/process isolation NOT RUN. |

## 4. Accessibility audit

- Automated DOM/ARIA/name-source heuristic, direct tablist children semantics, roving tabindex, arrow-key navigation, focus outline, focus restoration after closing active tab, named controls, `aria-describedby`, `aria-selected`, `aria-pressed`, `aria-expanded`, `aria-busy`, progress values and error announcement: PASS trong các trường hợp đã kiểm tra.
- Error message: visible, `role=alert`/assertive live region, input `aria-invalid=true`, focus trở lại trường task. Loading/Ready/Error/Disconnected: được kiểm tra. Reduced-motion spinner duration 0.00001s: PASS.
- Mẫu cặp màu computed foreground/background kiểm tra ở ngưỡng 4.5:1: tất cả PASS; mức thấp nhất 4.71:1.
- Giới hạn: đây không phải WCAG conformance certification; screen-reader/assistive technology, keyboard-only manual exploratory review trên thiết bị thật **NOT RUN**.

## 5. Desktop / tablet / mobile test results

Playwright + system Chromium chạy local `file://`; viewport được đặt bằng browser/emulation, không chỉ dựa vào CSS static inspection.

| Target | Result | Screenshot evidence |
|---|---|---|
| Desktop 1920×1080 CSS px | PASS; horizontal overflow absent; full-page capture 1920×1971 | `screenshots/ui-only-desktop-1920x1080.png` |
| Tablet 768×1024 CSS px | PASS; horizontal overflow absent; full-page capture 768×2274 | `screenshots/ui-only-tablet-768x1024.png` |
| Android-like emulation 390×844 CSS px | PASS; touch toggle and no horizontal overflow; full-page capture 390×2770 CSS px | `screenshots/ui-only-android-emulation-390x844.png` |

Android result là Playwright device emulation với touch; **không phải thiết bị Android vật lý** (physical-device test NOT RUN).

## 6. Port and preview safety

`server.py` hiện dùng `PREVIEW_HOST="127.0.0.1"`, `PREVIEW_PORT=0`, OS-assigned ephemeral port nếu được chạy thủ công. Không có preview URL cố định hoặc bind `0.0.0.0`. Server không được khởi chạy; `tests/test_server.py`, health route và process/backend isolation NOT RUN. Không có host/port probe hoặc cổng nào bị chiếm. `file://` là phương pháp tái lập kiểm thử hiện hành.

## 7. Test results

- `node --check app.js && node --check workflow.js`: PASS.
- `node --test tests/workflow.test.js`: **18/18 PASS**.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py`: **12/12 PASS**.
- `python3 tests/browser_smoke.py`: **33/33 PASS**, file-based Chromium UI smoke; zero HTTP(S) request.
- `python3 tests/accessibility_audit.py`: **70/70 PASS**, gồm computed contrast sample, keyboard, ARIA/state, three scenarios, desktop/tablet/mobile emulation; zero HTTP(S)/WebSocket request.
- `git diff --check`: PASS.
- `tests/test_server.py`, Browser Runtime, true external-browser E2E, HTTP preview/server isolation: **NOT RUN**.

## 8. GitHub commit / branch / CI

Branch đích: `work092/one-shot-20261122`; không merge `main`. CI gần nhất trước source update là run `44997247247`, SUCCESS tại SHA `12f74b03e8397c5e366f932d40280cfc28e1d168`, artifact ID `14743304960`. **Không được dùng run cũ này để chứng minh source hiện tại.** CI cho commit mới đang chờ push/run verification; SHA/run/artifact mới sẽ chỉ ghi sau khi đọc kết quả thật.

Workflow hiện chỉ chạy static pytest + Node; không chạy Playwright, `test_server.py` hay Runtime.

## 9. Evidence index

- `02_EVIDENCE/test-results/accessibility-audit.json` — 70 checks, full results and limits.
- `02_EVIDENCE/test-results/browser-ui-smoke.json` — file-based smoke results and checks.
- `02_EVIDENCE/screenshots/README.md` — inventory and provenance.
- `02_EVIDENCE/screenshots/ui-only-desktop-1920x1080.png`
- `02_EVIDENCE/screenshots/ui-only-tablet-768x1024.png`
- `02_EVIDENCE/screenshots/ui-only-android-emulation-390x844.png`
- `00_ROOT/BIEN_BAN_W092.md` — current T1–T17 matrix.
- `02_EVIDENCE/NU_BUILD_JOURNAL.md` — commands, results and chronology.

Legacy `e2e-result.json` and `v2-e2e-result.json` are archival only: they contain historical mock/agent claims and a fixed-port URL; they are not evidence for the current TEST_ONLY build or service isolation.

## 10. Remaining blockers

T6 remains PARTIAL because actual agent lifecycle transitions are not exercised and no detailed criterion source authorizes equating fixture states to real agent states. T17 remains PARTIAL because server/backend/process isolation was deliberately not run. Direct Work Sandbox execution, physical Android, screen-reader/assistive technology, live Browser Runtime, Nu independent dispatch/ACK, Xu independent review, and current-source GitHub Actions verification are **NOT RUN or BLOCKED** until their separate evidence exists.

## 11. Recommendation

Hand to Xu for independent source/evidence review as **ready for review, not accepted** after current commit and CI evidence are synchronized. Keep Runtime BLOCKED. Xu must decide whether T6's TEST_ONLY-only state model satisfies the prototype criterion; Vinh makes the final product/operation decision. Do not mark DONE/ACCEPTED based on this executor's report.
