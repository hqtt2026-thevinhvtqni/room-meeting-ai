# ERROR LOG — Work 092

## 2026-10-06 — V2

- V1 đã được redesign theo Browser-first hierarchy; các phần developer/test được chuyển xuống secondary Demo/Test Mode và Developer/Architecture View.
- V2 E2E phát hiện Agent Workflow đếm cả metadata `Workflow complete` trong Evidence (`8/6`). Đã sửa để chỉ tính 6 evidence keys chuẩn; clean-state retest PASS `6/6`.
- Không ghi nhận lỗi known sau vòng clean-state retest V2.

## 2026-11-22 — Regression fixes found by final mirror testing

9. **Favicon 404:** initial Chromium run on the local read-back mirror found a missing favicon request. Added `data:,` favicon and static pytest assertion; final E2E had no console/page/network errors.
10. **Tab close was inert:** the × was decorative and `aria-hidden`. Added semantic close button, focus style, switching/removal logic and guard against closing the final tab; static pytest and Playwright checks pass on mirror.
11. **Verification boundary:** pytest 12/12, Node 14/14, JS syntax and Chromium E2E 11/11 passed on Cloud Sandbox mirror only. Not direct Work Sandbox or GitHub Actions. CI remains pending until a real run is verified.


## 2026-11-22 — One-shot TEST_ONLY re-audit

15. **Preview bind/port risk corrected in source:** optional `server.py` now binds only `127.0.0.1` and asks the OS for port `0`; no service was started and no host/port probe was performed. The health route and backend/process isolation remain NOT RUN.
16. **ARIA tablist structure tightened:** a per-tab close button inside the tablist left a non-tab interactive child in the tablist subtree. The UI now uses direct role=tab children and one accessible Close current tab button outside the tablist; tests verify focus restoration and final-tab guard.
17. **Contrast palette improved:** muted text colors were adjusted after a preliminary contrast review. The current automated computed-color sample set passes 4.5:1 AA text threshold; minimum observed 4.71:1. This is not a full WCAG or assistive-technology certification.
18. **Legacy E2E outputs superseded for current acceptance:** historical JSON files still contain mock `agent_state: Done`/`PASS` labels and a fixed-port URL. Preserve them as archival data, but do not use them to establish current agent state, T6 acceptance, or T17 service isolation.
19. **Current tests:** Node 18/18, static pytest 12/12, local file UI smoke 33/33, accessibility/responsive audit 70/70; zero HTTP(S)/WebSocket requests. Browser Runtime, server fixture, physical Android and screen-reader tests were not run.
