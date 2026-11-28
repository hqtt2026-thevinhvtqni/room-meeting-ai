# Room UI Browser E2E — Work 05

Status: CONTRACT CREATED; EXECUTION BLOCKED.

The Playwright contract must run against the existing ROOM-HOP Room UI, never a newly created frontend. Required runtime inputs are `W05_ROOM_UI_BASE_URL`, `W05_ROOM_ID`, and an optional controlled `W05_CONNECTION_ID`. Coverage includes NOT_CONNECTED, controlled OAuth start, callback return and sanitized CONNECTED state, ERROR/REAUTH_REQUIRED/DISCONNECTED actionability, browser storage/URL secret audit, and disconnect request boundary.

Execution is eligible only after the canonical Room route, authenticated browser session, backend connection routes, OAuth callback route, and approved test account are supplied. A passing contract against a fake page is OFFLINE UI TEST, not REAL GOOGLE. No token, authorization code, private key, or client secret may be placed in test environment values.

The local suite files are `room_ui_oauth.spec.ts` and `ROOM_UI_BROWSER_E2E_README.md` under `/home/ubuntu/w05_e2e_work001`.
