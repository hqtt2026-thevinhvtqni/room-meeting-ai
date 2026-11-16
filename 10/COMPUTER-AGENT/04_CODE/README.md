# 04_CODE — COMPUTER AGENT V1

This is the Work 10 implementation built from the locked contracts.

## Module boundary
- `agent_api.py` — HTTP API, request validation, authentication and CORS boundary.
- `agent_runtime.py` — action execution + workflow verification loop.
- `execution_coordinator.py` — process-wide exclusive execution lease.
- `browser_adapter.py` — Playwright browser control boundary.
- `models.py` — typed action/result contracts.

## Local secure startup (PowerShell)

Run from the `COMPUTER-AGENT` directory. Keep the token in the local process environment; never commit it or put it in a URL.

```powershell
$env:COMPUTER_AGENT_TOKEN = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:COMPUTER_AGENT_ALLOWED_ORIGINS = "http://127.0.0.1:3000"
$env:COMPUTER_AGENT_PORT = "8787"
python 04_CODE/agent_api.py
```

The token is generated locally and is not printed to the console. Copy it from the current PowerShell session only if you need to paste it into the Dashboard password field. Do not send it to ROOM-HOP chat, GitHub, logs, or screenshots.

If the token or Origin allow-list is absent, `POST /agent/execute` fails closed. Browser requests must come from an exact allowed Origin and include `Authorization: Bearer <token>`. Non-browser clients may omit Origin but must still provide the token.

## Dashboard
Serve `08_DASHBOARD` from the configured Origin, for example with a local static server on port 3000. Do not open `index.html` directly with `file://`; the browser Origin would be `null` and is not trusted by default.

The Dashboard accepts a task, explicit Actions JSON, a non-empty Verification JSON block, and a session-only Bearer token. The token is not written to local storage or source.

## HTTP safeguards
- 1 MiB request-body default and 100-action default limit.
- JSON-only POST requests with bounded request schema.
- Constant-time Bearer token comparison; missing server token fails closed.
- Exact Origin allow-list; no wildcard CORS.
- Preflight limited to POST and Authorization/Content-Type.
- One process-wide execution lease; a concurrent request receives BLOCKED/409 before an adapter is constructed.
- Adapter shutdown completes before the API returns PASS; shutdown failure returns FAIL/500.

The process-wide lease is per service process. Multi-process deployments require an external shared lease and are not accepted by this implementation yet.
