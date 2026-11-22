# WORK 10 — WINDOWS OVERSIZED-REQUEST TEST REMEDIATION — RUNS 169 / 175

- Document ID: W10-HTTP-OVERSIZE-TEST-REMEDIATION-20261122-01
- Date-Time: 2026-11-22 06:48 (UTC+07:00)
- Implementer: Co | AI-07 / End-to-End Architecture & Implementation Lead

## 1. Failure observed — Run #169

- Run ID: `44965200063`; tested commit `2815ffbd56118aa065aaa5aca39e0a88bfd089d5`.
- Ubuntu 24.04: SUCCESS.
- Windows Server 2022: FAILURE in HTTP API test after 20 assertions.
- Exact exception: `ConnectionAbortedError: [WinError 10053] An established connection was aborted by the software in your host machine` while the test sent a 1 MiB + 10 byte JSON body.
- The API checks Content-Length and returns 413 before reading the body. On Windows, urllib could still be transmitting the oversized body while the server rejected/closed the connection, causing the client-side socket abort. This was a test transport race, not an API acceptance or adapter execution failure.

## 2. Test correction

Updated `05_TEST/test_http.py`:
- Added an explicit `http.client.HTTPConnection` helper that sends the authenticated request headers with a Content-Length greater than 1 MiB but does not transmit the oversized body.
- The API must reject the declared length with HTTP 413 and `request_body_too_large` before body read/adapter start.
- This directly tests the server's early Content-Length boundary without relying on platform-specific behavior while uploading a large body.

No API runtime behavior was relaxed; the 1 MiB limit and 413 rejection remain unchanged.

## 3. Follow-up CI — Run #175

- Run ID: `44965429403`
- Exact tested commit: `740798d7053061f5c8d0908d4882f8aed13f1a4b`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44965429403
- Both OS jobs SUCCESS.
- Windows Server 2022: 225 PASS / 0 FAIL / 0 SKIP.
- Ubuntu 24.04: 219 PASS / 0 FAIL / 2 expected SKIP.
- HTTP API suite: 52 PASS on both OSes, including oversized Content-Length -> 413.
- Windows PowerShell syntax and local launcher smoke: PASS.
- Dashboard static: 17 PASS; Dashboard live smoke: 7 PASS; V8 validator: 16 PASS; real Chromium API/runtime E2E: PASS.
- Artifacts: Windows ID `14731307568`, SHA-256 `bb0c7e67f8b4ec424dcfbba2c5bdad96ef45df0a975e643a5890b53f789162c8`; Linux ID `14731007308`, SHA-256 `3a882a65330209066fd73fa523bb3570c8ab4cd965e4d2501a3250473d101245`.

## 4. Disposition

- Run #169 Windows test transport failure: diagnosed.
- Oversized request API limit: unchanged; HTTP 413 verified.
- Run #175 cross-platform regression: PASS.
- No source API security weakening; only test request construction changed.
- Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
