# WORK 10 — LIVE DASHBOARD / API SMOKE EVIDENCE — RUN 135

- Document ID: W10-LIVE-DASHBOARD-API-EVIDENCE-20261122-RUN135
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44963956538`; Run #135
- Exact tested commit: `a3d935066ffa2dbada32bdd7cf1c94599e6463cf`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44963956538
- Conclusion: SUCCESS — Ubuntu 24.04 and Windows Server 2022 jobs both passed.

## New Dashboard live E2E suite

`05_TEST/test_dashboard_live_e2e.py` starts the local Agent API on loopback port 8787 and Work 10 standalone Dashboard on loopback port 3010, then uses Playwright to verify:
1. local Agent API health identifies Work ID 10;
2. Dashboard fetches live health cross-origin and shows CONNECTED;
3. Dashboard renders Work ID 10;
4. Execute remains disabled before explicit consent;
5. Execute enables only after health + token + explicit consent;
6. Clear removes the in-memory bearer token;
7. Clear resets consent and disables Execute.

This smoke test does not click Execute and does not run a real workflow. The separate real Chromium E2E suite verifies the API/runtime browser workflow. Port 3000 remains reserved for W113's shared Dashboard ingress.

## Ubuntu 24.04
- Job ID: `137028669195`
- Contract: 60 PASS
- Safety: 41 PASS / 2 expected Windows-only SKIP
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 12 PASS
- V8 acceptance validator: 16 PASS
- Dashboard static contract: 17 PASS
- Dashboard live E2E: **7 PASS**
- Total: **207 PASS / 0 FAIL / 2 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14730642888`; size 41,951 bytes
- ZIP SHA-256: `197f37dd1beaab4589a85a2c7f7b76c6b98b3e40a4bbc73f6835648a17c1284d`

## Windows Server 2022
- Job ID: `137028669326`
- Contract: 60 PASS
- Safety: 45 PASS
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 14 PASS
- V8 acceptance validator: 16 PASS
- Dashboard static contract: 17 PASS
- Dashboard live E2E: **7 PASS**
- Total: **213 PASS / 0 FAIL / 0 SKIP**
- Real Chromium E2E: PASS
- Artifact ID: `14730518600`; size 35,819 bytes
- ZIP SHA-256: `ec8703ec46cd80026bc46ee0df56b700fc0528d922a6c8ae861ef4f64d86a5e1`

## Scope and limitations

- Run #135 proves the live Dashboard-to-local-Agent-API health and consent gating on hosted Windows Server 2022 and Ubuntu 24.04.
- The test does not execute a browser workflow from the Dashboard button; real API/browser workflow is separately tested by `e2e_real_browser.py`.
- Hosted Windows Server 2022 is not the Owner's physical Windows 10 PC.
- Production HMAC key/pins, Linux cgroup-v2 and ROOM-HOP W24/W112/W14/W113 integration remain open.

## Disposition

- Dashboard static contract: 17 PASS on each OS.
- Dashboard live health/API/consent smoke: 7 PASS on each OS.
- Full hosted regression: Ubuntu 207 PASS / 0 FAIL / 2 SKIP; Windows 213 PASS / 0 FAIL / 0 SKIP.
- Work 10: ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
