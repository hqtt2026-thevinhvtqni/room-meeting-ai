# NU BUILD JOURNAL — WORK 092

## 2026-11-22 — One-shot execution and final mirror retest

- Current executor followed the user's ONE-SHOT instruction without pausing for intermediate ACK/approval. Existing NU_ACK is explicitly not proof of an independently dispatched Nu agent.
- Reviewed Work 092 source/evidence through MCP, applied T5/T9/T12 changes, and added task/evidence/permission tests.
- Initial Playwright Chromium run exposed a favicon 404. Added a local data URI favicon and regression assertion; final E2E has zero console/page errors.
- Review found tab close (×) was decorative. Added an accessible close button and logic, prevented closing the final tab, and added static/E2E regression coverage.
- Final tests on Cloud Sandbox mirror reconstructed from MCP read-back: pytest 12/12; Node 14/14; JS syntax checks pass; Playwright+system Chromium 11/11.
- E2E covered tab open/switch/close, URL/Back/Forward/Reload, control handoff, empty task, Search/Browse/Workflow, permissions, evidence provenance, XSS-safe rendering, desktop/mobile overflow and no external page requests/errors.
- Screenshot dimensions: desktop viewport 1920×1080, full page 1920×1833; mobile viewport 390×844, full page 390×2857, scrollWidth=clientWidth=390.
- Distinction: test/browser evidence is mirror-only, not direct Work Sandbox or GitHub Actions. GitHub Actions remains pending until verified run URL/SHA/conclusion/artifact.
- Final disposition at this journal entry: PARTIAL — NOT ACCEPTED; Xu retains acceptance authority.
