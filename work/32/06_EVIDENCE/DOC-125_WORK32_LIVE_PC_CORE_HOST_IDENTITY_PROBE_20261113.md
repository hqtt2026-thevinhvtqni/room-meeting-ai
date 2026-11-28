# DOC-125 — Work32 Live PC Core / Host Identity Probe Result

- **Document Number:** DOC-125
- **Priority:** P0 — live runtime authority and process identity
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 10:25 Asia/Ho_Chi_Minh
- **Branch:** work/32-main-integration-authority-20261112
- **PR:** #52 — Core-owned Execution Authority
- **Exact source head tested:** 17ba50ab2e8736e2636e323741ce735c107fe197
- **Workflow:** Run #416 / 43357544278
- **Status:** HOSTED CI PASS; LIVE PC CORE/HOST IDENTITY BLOCKED

## 1. Exact-head hosted CI

Run #416 completed the hosted/source lanes successfully on exact PR head `17ba50ab2e8736e2636e323741ce735c107fe197`:

- Python 3.12 unit tests: **250 passed**.
- Product Auto E2E: **122 passed**.
- Hosted Windows Browser Adapter E2E: **10 passed**; preflight, browser-context cleanup and adapter cleanup PASS.
- Work32 tooling/workflow mirror: PASS.
- Immutable product artifact: checksum verification, dependency check, compile check and artifact-level E2E **1 passed**.

The separate dedicated PC runner probe and Work32 release acceptance gate failed. Hosted CI success does not override the live runtime result.

## 2. Dedicated PC runner identity

The read-only probe ran on the intended machine:

- Runner: `ROOM-HOP-W32-PC`.
- OS / architecture: Windows / X64.
- Runner identity: PASS.
- Python: `NOT_FOUND` in the runner service environment.
- Git: `2.55.0.windows.3`.

## 3. Live Core result — BLOCKED

- Core listener: `127.0.0.1:8000`.
- Observed PID: `12272`, process name `python.exe`.
- Process owner/module: UNKNOWN / UNRESOLVED; expected entrypoint match false.
- Invalid service identity request to the expected Execution Authority status route returned **HTTP 404**.
- The required authentication-denial response is HTTP 401 or 403.

HTTP 404 is not evidence that invalid credentials were denied by the Core Authority service. It indicates that the live listener did not expose the expected route at probe time. The running process entrypoint remains unverified.

## 4. Live Execution Host result — BLOCKED

- Host listener: `127.0.0.1:8031`.
- Observed PID: `16720`, process name `python.exe`.
- Process owner/module: UNKNOWN / UNRESOLVED; expected entrypoint match false.
- Health endpoint: HTTP 200.
- `status`: PASS.
- `service`: execution-host.
- `provider_type`: missing/blank.
- `authority`: missing/blank.
- `grant_cache`: missing/blank.

The current source contract expects `provider_type=CORE_AUTHORIZED_PYTEST`, `authority=CORE_ONLINE`, and `grant_cache=false`. The live health response does not attest these values. HTTP 200 alone is insufficient to accept the Host identity.

## 5. Interpretation

The source branch contains:
- the Core authority router mounted by `room_hop_mcp/core_http_main.py`;
- the Host health identity emitted by the current `GrantedExecutionHost.identity()`.

The live listeners do not expose those expected contracts. The legacy `room_hop_mcp/adapter/http_server.py` source does not mount the Execution Authority router, but the live process module could not be read; therefore the exact deployed entrypoint/version is **not proven**.

The evidence supports a runtime/source mismatch or stale service configuration as the working hypothesis. It does not prove which process command or configuration is currently active.

## 6. Required next acceptance action

When the PC runtime can be safely inspected under Vinh's control:

1. Identify the actual process command line and owner for ports 8000 and 8031.
2. Compare the running Core and Host entrypoints with the approved Work32 branch/source SHA.
3. Inspect the Core mount/configuration and Host health identity without exposing credentials.
4. Apply a controlled service update/restart only after the exact service configuration and owner are verified.
5. Re-run the read-only negative Core probe and Host health identity probe.
6. Require HTTP 401/403 from Core and the complete Host identity fields before considering the live runtime gate PASS.

No service restart, process termination, configuration change, credential provisioning or protected command was performed by Ka.

## 7. Acceptance disposition

- Source completion validation: PASS.
- Unit / Product Auto E2E / hosted Windows Browser Adapter / tooling / immutable artifact: PASS.
- Dedicated PC runner identity: PASS.
- Live Core Authority route: BLOCKED — HTTP 404.
- Live Host identity: BLOCKED — required identity fields missing.
- Runner Python availability: BLOCKED / NOT FOUND in service PATH.
- Independent security review: PENDING.
- Main integration, merge, CD, staging, production and release: NOT AUTHORIZED / NOT RUN.

**Conclusion:** The current PC runtime does not attest the Core-owned Execution Authority and Host identity contracts. Do not classify this as a test-only issue or convert the health HTTP 200 into PASS. **PROTECTED EXECUTION DENIED; WORK32 ACTIVE — NOT RELEASED.**

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-13 10:25 Asia/Ho_Chi_Minh
- **Decision:** Keep the live Core/Host runtime gate BLOCKED until process provenance, Core denial semantics and Host identity are verified on the PC.

## NHẬT KÝ

- **W32-LOG-20261113-118**
- Recorded the final Run #416 PC probe results and the required controlled runtime reconciliation.
