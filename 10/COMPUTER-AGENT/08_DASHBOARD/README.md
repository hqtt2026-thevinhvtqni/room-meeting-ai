# WORK 10 — OPERATIONAL LIVE DASHBOARD

`08_DASHBOARD/index.html` is the operational control UI for the Work 10 Agent API. It reads live health from `GET /health` and displays each workflow result/evidence from the response to `POST /agent/execute`. It does not read preview JSON, invent PASS, or provide task history: the current API has no persistent history endpoint.

## What the page verifies

- API responds with `status: ok` and `service: computer-agent`.
- API reports `work_id: 10`; another Work is rejected by the UI.
- Current execution lease and the effective destructive-action flag are shown from the API's health response.
- A workflow can be submitted only after a recent successful Work 10 health check, when the API is not busy, the operator supplies the bearer token, fills the task/actions/post-condition, and checks the explicit real-execution confirmation.
- Result status, state trace, checks, action evidence, final observation and raw JSON come from the Agent API response. A new run clears the previous in-tab result. Nothing is saved to localStorage/sessionStorage.
- The token stays in page memory and is sent only in the Authorization header. Do not place it in the URL, prompt, evidence, shell history, or source.

## Start locally (Windows PowerShell)

Use the Work 10 root as the current directory and two PowerShell terminals.

**Terminal A — Agent API**

```powershell
$token = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:COMPUTER_AGENT_API_TOKEN = $token
Set-Clipboard -Value $token
$env:COMPUTER_AGENT_ALLOWED_ORIGINS = "http://127.0.0.1:3000"
$env:COMPUTER_AGENT_WORK_ID = "10"
python .\04_CODE\agent_api.py
```

Keep this terminal open; the API binds to loopback by default. The generated token is local to this shell session.

**Terminal B — serve the Dashboard**

```powershell
python -m http.server 3000 --bind 127.0.0.1 --directory .\08_DASHBOARD
```

Open exactly `http://127.0.0.1:3000` (not `file://`, not a public hostname). Wait until the header shows `CONNECTED · W10`; verify the Work ID, version, lease, and policy. Paste the clipboard token into the password field only when ready to run.

## Running a real workflow

1. Use an approved target and actions supported by `03_ARCHITECTURE/ACTION_CONTRACT.md`; do not paste secrets into task/action/verification fields.
2. Enter a meaningful post-condition in the Verification JSON. The UI requires at least one check and will not accept a bare observation as a user-defined acceptance test.
3. Review the target, action list, destructive-action policy, and expected post-condition. Then check the explicit confirmation and press **Execute workflow** once.
4. Review the HTTP status, runtime status, trace, each evidence row, final observation, and raw response. `PASS` is only the result returned by the Agent API for that submitted workflow; it does not certify Work release or other gates.
5. If a request times out, the UI marks its result uncertain and does not auto-retry. Check API health and the browser/target state before deciding whether to retry.
6. Stop both servers when finished. Clear the form to remove the token and payload from the tab's memory.

The API's own `COMPUTER_AGENT_ALLOWED_ORIGINS`, path/domain policy, action timeout, workflow timeout, and destructive-action setting remain authoritative. A UI checkbox does not grant permissions. Do not expose the loopback API via port forwarding, reverse proxy, or a public network.

## Testing and evidence boundary

Run the static dashboard contract check with:

```powershell
python .\05_TEST\test_dashboard_contract.py
```

This checks source-level UI invariants and JavaScript syntax only. It is **not** a live browser/API integration test. P4 remains NOT VERIFIED until the operational page is opened in a supported browser against the exact Work 10 API revision and live health + an approved end-to-end workflow are observed with retained evidence. The Sandbox's real-browser/CI evidence for other revisions does not certify this Dashboard change, Windows behavior, or the user's PC.

`09_DASHBOARD_PREVIEW/` and root `preview/` are layout/demo previews. Their JSON is sample data and must never be presented as current runtime state.
