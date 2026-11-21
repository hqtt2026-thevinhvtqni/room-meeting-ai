# 04_CODE — COMPUTER AGENT V1

This is a new implementation built from the Work 10 specification.

Do not treat 01_ORIGINAL/index.html as the implementation source.

Initial module boundary:
- agent_api.py — HTTP API contract
- agent_runtime.py — action execution + verification loop
- browser_adapter.py — browser control boundary
- models.py — typed request/result contracts

Implementation must remain observable and testable.


## HTTP transport and execution-lease boundary (v1.3.0)

The local API is loopback-only by default and requires both:
- `COMPUTER_AGENT_API_TOKEN`: operator-managed bearer secret; never place it in source, URL, logs, or committed files.
- `COMPUTER_AGENT_ALLOWED_ORIGINS`: comma-separated exact browser origins. Default: `http://127.0.0.1:3010`.

`POST /agent/execute` rejects missing/invalid bearer credentials (401), non-allowlisted or missing Origin (403), and non-JSON content (415). Preflight is limited to POST with Authorization and Content-Type. Request bodies are capped at 1 MiB; chunked Transfer-Encoding is rejected; verification schema is validated before adapter construction. `/health` is read-only and unauthenticated but still rejects an explicitly supplied unapproved Origin. Do not expose the API beyond loopback without a separately reviewed transport design.

Dashboard must be served from an exact allowlisted HTTP origin (not opened as `file://`). The operator enters the token into the password field; the page keeps it in memory only and sends it in the Authorization header.


## Local operator startup (PowerShell) — standalone dev port 3010

Use two separate PowerShell terminals. Run from the Work 10 source directory.

**Terminal A — API**
1. Generate a local secret and keep it in this shell:
   $token = python -c "import secrets; print(secrets.token_urlsafe(32))"
   $env:COMPUTER_AGENT_API_TOKEN = $token
   Set-Clipboard -Value $token
2. Set the exact Dashboard origin:
   $env:COMPUTER_AGENT_ALLOWED_ORIGINS = "http://127.0.0.1:3010"
3. Start the API:
   python .\04_CODE\agent_api.py

**Terminal B — Dashboard**
1. Serve 08_DASHBOARD from the Work 10 root:
   python -m http.server 3010 --bind 127.0.0.1 --directory .\08_DASHBOARD
2. Open http://127.0.0.1:3010 and paste the clipboard token into the password field.

Do not print the token into logs, add it to .env files committed to Git, place it in a URL, or paste it into ROOM-HOP chat/evidence. Stop both local servers when finished. These startup steps are documentation only and have NOT been executed in this session.


## Timeout / execution lease
The API admits one workflow at a time process-wide. If an adapter call times out while its worker is still alive, the Runtime reports BLOCKED and exposes the timed-out worker to the HTTP host. The host keeps the execution lease and defers adapter.close() until that worker exits; later execute requests receive 409 execution_busy and do not construct another adapter. If the worker never exits, the lease remains held (fail-closed); restart is an operator recovery action after investigating the stuck process. This is not cancellation: the worker may still finish its side effect. Playwright thread-affinity and host behavior must be tested before acceptance.


## Adapter thread ownership
Runtime now lazily creates one dedicated daemon adapter-owner thread per execution. Adapter start, every action, final observation, and adapter close are serialized on that same thread to respect Playwright Sync API thread affinity. A timeout does not cancel the in-flight call; the API retains its process-wide lease and queues close only after that call completes. The HTTP fake-adapter regression records thread IDs for start/action/deferred-close. This architecture is statically present but has NOT been run with Playwright/Chromium; host verification remains mandatory.


## Current process and PC-host architecture — 2026-11-22

The earlier thread-owned adapter notes above are historical and are superseded by the isolated worker architecture now implemented and tested:

- `agent_api.py` performs authentication, exact-Origin validation, request validation and admission, then delegates each request to `ProcessSupervisor`.
- `execution_worker.py` owns the browser or host-operation lifecycle in a separate child process. The parent validates the correlated JSON response and does not release the execution lease until containment is confirmed empty.
- Windows uses a Job Object with kill-on-close and atomic process assignment before the worker start gate is released. Hosted Windows Server 2022 E2E verifies worker + descendant cleanup.
- Linux currently uses a limited process-group profile. This is not cgroup-v2 and is not approved as hardened production containment.
- `host_operations.py` exposes only allowlisted `list_directory`, `read_file`, `write_file`, `run_pytest`, `run_powershell_script` and `validate_acceptance_manifest`. It has no generic shell or inline PowerShell command. Write roots and PowerShell roots are empty unless explicitly configured.
- `acceptance_validator.py` implements V8 schema + semantic validation, category policy, source/runner pins, artifact/fixture hashes and HMAC attestation. Missing or mismatched production trust configuration returns BLOCKED.
- `POST /agent/host/execute` is separate from the LOCKED browser Action Contract. See `03_ARCHITECTURE/PC_HOST_CAPABILITY_CONTRACT.md`.

## Verification boundary

Cross-platform GitHub Actions Run #53 tested commit `29daa718509b1c3906527a8cd9358104061e3b85`: Ubuntu 24.04 183 PASS / 0 FAIL / 2 SKIP; Windows Server 2022 189 PASS / 0 FAIL / 0 SKIP. Both ran real Chromium E2E and the V8 validator suite (16 PASS each). This does not certify the Owner's physical Windows 10 PC, production HMAC key provisioning, Linux cgroup-v2, or integrated ROOM-HOP Dashboard / PC Bridge.

## Local operator setup

Use the operator runbook in `05_TEST/HOST_E2E_RUNBOOK.md` and the PC Host Capability Contract. Keep the API bound to loopback, set an operator-managed bearer token, configure exact Dashboard origins and explicit filesystem roots. Keep writable and PowerShell roots disabled unless the operator intentionally enables them. Do not put API tokens or production HMAC keys in source control, URLs, browser storage, screenshots or evidence logs.


## Shared Dashboard ingress boundary — 2026-11-22

Port `3000` is reserved for the single shared ROOM-HOP Dashboard ingress owned by W113. This Work 10 Dashboard is a standalone local development/acceptance UI and therefore serves on loopback port `3010` during isolated testing. Work 10 must not start a competing listener on port 3000. Production Work 10 Dashboard access must be mounted/registered by W113 under its approved Work route; the route path and embedding contract are not guessed here. The Agent API remains loopback-only and its exact Origin allow-list must be configured for the approved host origin before any integration. W113 integration is NOT VERIFIED.
