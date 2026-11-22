# ROOM-HOP Browser Product UX V2 — TEST_ONLY UI

## Goal and boundary

This is a static HTML/CSS/JavaScript UI fixture. Runtime always remains **DISCONNECTED**; all scenarios/actions are **TEST_ONLY**. There is no Browser Agent, controlled Chromium Runtime, external website, Internet/API, Core/MCP, or real screenshot artifact. Task text selects a local prepared scenario; permission flags are UI-only test gates, not browser/security grants. Completion means the fixture script finished, not a real-world task.

## UI behavior

- Browser tabs, local mock address/navigation/reload, TEST_ONLY task input, scenario selector, action timeline, evidence provenance, permission gates, hold/resume/reset.
- The browser tablist contains only `role=tab` buttons. Close current tab is an accessible external tablist control; active-tab selection/focus is restored after close. Secondary tabs use roving tabindex and keyboard navigation.
- Keyboard focus, error announcements/`aria-invalid`, ARIA states, reduced motion and responsive breakpoints are tested.
- Browser, agent panel, page status, evidence and completion labels keep the disconnected/test-only boundary visible.

## Opening the prototype

Open `index.html` directly with `file://`. No server is required and `server.py`/`start.sh` should not be run for these checks. The optional server, if a user deliberately starts it, binds to `127.0.0.1` and asks the OS for an ephemeral port (`0`); it is not part of the normal verification path. Do not use a stale fixed-port URL from historical test outputs.

## Reproducible checks

From this directory:

```bash
node --check app.js && node --check workflow.js
node --test tests/workflow.test.js
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py
python3 tests/browser_smoke.py
python3 tests/accessibility_audit.py
```

`browser_smoke.py` and `accessibility_audit.py` require Python Playwright and system Chromium at `/usr/bin/chromium`. Both use `file://`, not an HTTP preview or Runtime. `browser_smoke.py` writes `02_EVIDENCE/test-results/browser-ui-smoke.json`. `accessibility_audit.py` writes `02_EVIDENCE/test-results/accessibility-audit.json` and current UI-only screenshot captures under `02_EVIDENCE/screenshots/`.

## Results — 2026-11-22

Latest local Work 092 branch-checkout run in the Manus Sandbox:

- JavaScript syntax: PASS (2 files).
- Node built-in tests: **18/18 PASS**.
- Static-only pytest: **12/12 PASS**.
- File-based Chromium UI smoke: **33/33 PASS**; address entry, Back/Forward/Reload, tablist/close/focus, task/permission gate, scenario completion, reset, responsive sizes; zero external HTTP(S) requests.
- Accessibility/responsive audit: **70/70 PASS**; label-source heuristic, tab/secondary-tab semantics, focus/ARIA/error/status states, reduced motion, contrast sample set ≥4.5:1, Browse/Search/Workflow actions, desktop/tablet/mobile-emulation layouts; zero HTTP(S)/WebSocket requests.
- CSS viewports: desktop 1920×1080, tablet 768×1024, Android-like Playwright emulation/touch 390×844; all without horizontal overflow. Emulation is not a physical Android device.

GitHub Actions historically passed at SHA `12f74b03e8397c5e366f932d40280cfc28e1d168` (run `44997247247`, artifact `14743304960`), but that predates this source revision. Current source CI is pending after push. Actions runs static pytest and Node only; it does not run Playwright, `tests/test_server.py` or Browser Runtime. Direct Work Sandbox execution, physical Android, assistive-technology review and Xu acceptance remain NOT RUN; Runtime remains BLOCKED. Work 092 is **PARTIAL — NOT ACCEPTED**.
