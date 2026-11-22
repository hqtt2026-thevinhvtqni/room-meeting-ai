# STATIC SITE DELIVERY — WORK 092

Work 092 is static HTML/CSS/JavaScript. The normal and tested path is opening `01_SOURCE/room-hop-browser-v1-prototype/index.html` directly with `file://`; no server is required.

The optional Python preview server is opt-in only. If manually started, it binds `127.0.0.1` and asks the OS for port `0` (ephemeral), then prints the selected URL. It does not bind `0.0.0.0` or a fixed service port. This review did **not** start the server, probe any host/port, or test its health route/backend isolation. Do not treat the old fixed-port URL in historical files as current guidance.

No real Browser Agent, controlled Chromium Runtime, external API, website request, or Internet access is part of the prototype. Scenario actions and evidence are local TEST_ONLY fixtures.

## Current verification — 2026-11-22

Run from `01_SOURCE/room-hop-browser-v1-prototype/`:

```bash
node --check app.js && node --check workflow.js
node --test tests/workflow.test.js
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/test_static_contract.py
python3 tests/browser_smoke.py
python3 tests/accessibility_audit.py
```

Observed results in the current Manus Sandbox branch checkout:

- Node syntax: PASS (2 files); Node tests **18/18**.
- Static pytest: **12/12**.
- Playwright/system Chromium `file://` browser smoke: **33/33**; 0 external HTTP(S) requests.
- Accessibility/responsive audit: **70/70**; 0 HTTP(S)/WebSocket requests; computed contrast samples all at least 4.5:1.
- Desktop 1920×1080, tablet 768×1024, Android-like emulation 390×844 CSS px: no horizontal overflow. Android is emulation, not physical-device evidence.

The scripts store current results in `02_EVIDENCE/test-results/browser-ui-smoke.json` and `accessibility-audit.json`, and UI-only screenshots in `02_EVIDENCE/screenshots/`. None is Browser Runtime/E2E evidence. GitHub Actions only runs static pytest and Node tests; current-source Actions verification is pending until a real run is confirmed. Direct Work Sandbox execution, server fixtures, Runtime and Xu acceptance remain NOT RUN/BLOCKED.
