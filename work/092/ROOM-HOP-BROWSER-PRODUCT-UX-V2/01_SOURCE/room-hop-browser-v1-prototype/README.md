# ROOM-HOP Browser Product UX V2 — TEST_ONLY UI

## Goal and boundary

This is a static HTML/CSS/JavaScript UI fixture. Runtime always remains **DISCONNECTED**; all scenarios/actions are **TEST_ONLY**. There is no Browser Agent, controlled Chromium Runtime, external website, Internet/API, Core/MCP, or real screenshot artifact. Task text selects a local prepared scenario; permission flags are UI-only test gates, not browser/security grants. Completion means the fixture script finished, not a real-world task.

## UI behavior

- Browser tabs, local mock address/navigation/reload, TEST_ONLY task input, scenario selector, action timeline, evidence provenance, permission gates, hold/resume/reset.
- Browser tablist contains only `role=tab` buttons. Close current tab is an accessible external tablist control; active-tab focus is restored after close. Secondary tabs use roving tabindex and keyboard navigation.
- Keyboard focus, error announcements/`aria-invalid`, ARIA states, reduced motion and responsive breakpoints are tested.
- Browser, agent panel, page status, evidence and completion labels keep the disconnected/test-only boundary visible.

## Opening the prototype

Open `index.html` directly with `file://`. No server is required and `server.py`/`start.sh` were not run for these checks. The optional server, if deliberately started by an authorized operator, binds to `127.0.0.1` and asks the OS for an ephemeral port (`0`). Do not use stale fixed-port URLs in historical outputs.

## Reproducible checks

From this directory:

```bash
node --check app.js && node --check workflow.js
node --test tests/workflow.test.js
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py
python3 tests/browser_smoke.py
python3 tests/accessibility_audit.py
```

`browser_smoke.py` and `accessibility_audit.py` require Python Playwright and system Chromium at `/usr/bin/chromium`. Both use `file://`, not an HTTP preview or Runtime. Smoke writes `02_EVIDENCE/test-results/browser-ui-smoke.json`; audit writes `accessibility-audit.json` and UI-only screenshots under `02_EVIDENCE/screenshots/`.

## Results — 2026-11-22

At source/test SHA `3de70ffb9d0883bb94d227428601dddcaf70d2e2`: JavaScript syntax 2 files PASS; Node tests **18/18**; static pytest **12/12**; file-based Chromium UI smoke **33/33**; accessibility/responsive audit **70/70**; 0 HTTP(S)/WebSocket requests, console errors or page errors. CSS viewports: desktop 1920×1080, tablet 768×1024, Android-like Playwright emulation/touch 390×844; all have no horizontal overflow. Android emulation is not a physical Android device. Contrast samples all met 4.5:1; lowest observed was 4.71:1.

GitHub Actions [run 45000773196](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/45000773196) completed SUCCESS at the same source SHA. JUnit artifact ID **14745910744** was downloaded and parsed: pytest 12 tests, 0 failures/errors/skips; job log confirms Node **18/18**. Actions runs static pytest and Node only; it does not run Playwright, `tests/test_server.py` or Browser Runtime. A later docs-only commit does not inherit this source CI result. Direct Work Sandbox execution, physical Android, assistive-technology review, server isolation and Xu acceptance remain NOT RUN; Runtime remains BLOCKED. Work 092 is **PARTIAL — NOT ACCEPTED**.
