# WORK 10 — HOST E2E & LOCAL WINDOWS OPERATOR RUNBOOK

- Version: 1.0
- Date: 2026-11-22 (UTC+07:00)
- Purpose: local acceptance of Work 10 browser API + PC host capabilities on the Owner's Windows 10 PC.
- Status: PROCEDURE PREPARED; NOT EXECUTED ON OWNER PC.

## 1. Preconditions

1. Use a trusted local checkout of `hqtt2026-thevinhvtqni/room-meeting-ai` on branch `work/10-computer-agent-mirror`.
2. Confirm the checkout commit with `git rev-parse HEAD`; record it with every test run.
3. Use a dedicated, low-privilege Windows account where possible. Do not run arbitrary untrusted pytest tests or PowerShell scripts: approved code executes with the agent service account's permissions.
4. Install Python 3.12 and ensure Chrome/Chromium is available for Playwright.
5. Open PowerShell in `10\COMPUTER-AGENT`.

## 2. Install and offline regression

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
python -m playwright install chromium
python -m compileall -q .\04_CODE .\05_TEST
python .\05_TEST\run_all_tests.py
```

Expected on Windows: every suite exits 0; the current CI baseline is 189 PASS / 0 FAIL / 0 SKIP before the Dashboard static contract suite was added. After the Dashboard suite addition, use the latest passing CI count as the baseline. Do not accept an overall PASS if any suite is missing, skipped unexpectedly or failed.

## 3. Configure local Agent API (Terminal A)

Generate a local bearer token and keep it only in this PowerShell session:

```powershell
$token = python -c "import secrets; print(secrets.token_urlsafe(32))"
$env:COMPUTER_AGENT_API_TOKEN = $token
Set-Clipboard -Value $token
$env:COMPUTER_AGENT_ALLOWED_ORIGINS = "http://127.0.0.1:3010"
$env:COMPUTER_AGENT_WORK_ID = "10"
$env:COMPUTER_AGENT_HOST_ALLOWED_ROOTS = (Get-Location).Path
$env:COMPUTER_AGENT_HOST_WRITABLE_ROOTS = ""
$env:COMPUTER_AGENT_HOST_POWERSHELL_ROOTS = ""
python .\04_CODE\agent_api.py
```

Defaults are read-only for file writes and PowerShell. Keep the API bound to loopback; do not use port forwarding, a public hostname, reverse proxy or external network exposure.

## 4. Configure optional write and PowerShell roots

Only if the Owner explicitly wants these capabilities enabled, configure narrow directories containing only approved files/scripts. Do not point them at the whole drive or user profile.

Example (replace with a dedicated Work 10 scratch folder):

```powershell
$approvedRoot = "D:\ROOM-HOP-CLEAN\room-meeting-ai\10\COMPUTER-AGENT\06_EVIDENCE\operator-scratch"
New-Item -ItemType Directory -Force $approvedRoot | Out-Null
$env:COMPUTER_AGENT_HOST_WRITABLE_ROOTS = $approvedRoot
$env:COMPUTER_AGENT_HOST_POWERSHELL_ROOTS = $approvedRoot
```

The path allow-list is an API boundary, not an OS sandbox for code inside a pytest test or approved PowerShell script. Keep the service account low privilege and the roots trusted. If write or PowerShell is not needed, leave the variables empty.

## 5. Serve Dashboard (Terminal B)

```powershell
python -m http.server 3010 --bind 127.0.0.1 --directory .\08_DASHBOARD
```

Open exactly `http://127.0.0.1:3010`. Wait for live health to identify service `computer-agent`, Work ID `10`, version and execution lease. Paste the bearer token into the in-memory password field only. Do not save it in browser storage, URL, task payload or evidence.

## 6. Validate host API operations

All POST calls require both:
- `Authorization: Bearer <token>`
- `Origin: http://127.0.0.1:3010`
- `Content-Type: application/json`

Example PowerShell request for a read-only directory listing:

```powershell
$headers = @{
  Authorization = "Bearer $token"
  Origin = "http://127.0.0.1:3010"
}
$body = @{
  operation = "list_directory"
  arguments = @{ path = "." }
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8787/agent/host/execute" -Headers $headers -ContentType "application/json" -Body $body
```

Test these in order:
1. `list_directory` and `read_file` within the configured root.
2. `run_pytest` using only a trusted, explicitly allowlisted test path.
3. `write_file` only after an explicit writable root is configured; require explicit `overwrite=true` to replace an existing file and verify returned read-back SHA-256.
4. `run_powershell_script` only with a pre-existing approved `.ps1` under the explicit PowerShell root; no inline command is accepted.
5. `validate_acceptance_manifest` only after production trust configuration in section 8 is complete.

Unknown operations, path traversal, symlink escape, unauthorized origin/token, missing root configuration and unsupported OS operations must be BLOCKED/REJECTED.

## 7. Browser E2E

```powershell
python .\05_TEST\e2e_real_browser.py
```

Retain `06_EVIDENCE/real-browser-e2e-result.json` and `real-browser-e2e.png`. Verify state trace PLANNED → RUNNING → VERIFYING → PASS, final observation, checks, action evidence, ProcessSupervisor profile and containment-empty proof. A screenshot alone is not sufficient.

## 8. Production V8 validator trust configuration

CI uses a test-only HMAC key. It must never be reused for production. Generate a new secret on the Owner's PC and keep it out of source, shell history, chat, screenshots and evidence:

```powershell
$env:COMPUTER_AGENT_VALIDATOR_HMAC_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:COMPUTER_AGENT_VALIDATOR_KEY_ID = "W10-OWNER-PC-2026-01"
$env:COMPUTER_AGENT_VALIDATOR_SHA256 = (Get-FileHash .\04_CODE\acceptance_validator.py -Algorithm SHA256).Hash.ToLower()
$env:COMPUTER_AGENT_VALIDATOR_SCHEMA_SHA256 = (Get-FileHash .\06_EVIDENCE\W10_P0_ACCEPTANCE_MANIFEST_V8.schema.json -Algorithm SHA256).Hash.ToLower()
$env:COMPUTER_AGENT_VALIDATOR_POLICY_SHA256 = (Get-FileHash .\06_EVIDENCE\W10_P0_CATEGORY_OUTCOME_POLICY_V8.json -Algorithm SHA256).Hash.ToLower()
$env:COMPUTER_AGENT_SOURCE_COMMIT = (git rev-parse HEAD).Trim()
```

The HMAC key is a secret. Environment variables are visible to sufficiently privileged local processes; use a dedicated low-privilege account and follow the Owner's local secret-handling policy. The current implementation fails closed if any pin/key is missing or mismatched. Do not copy the CI test key.

## 9. Capture evidence

Record:
- exact Git commit and SHA-256 of the source/schema/policy;
- Windows edition/build, architecture, Python and Playwright versions;
- API health response with secrets redacted;
- each host operation request/response with bearer token removed;
- full suite output and per-suite logs;
- real-browser E2E JSON and screenshot;
- process run journal and containment evidence;
- V8 attestation and its signature verification result (never include HMAC key);
- exact root allow-lists and whether write/PowerShell were enabled.

Store evidence under Work 10 `06_EVIDENCE`; do not hand-edit test output.

## 10. Acceptance boundary / known limitations

- This runbook has NOT been executed on the Owner's physical Windows 10 PC in the current session.
- Hosted Windows Server 2022 CI is useful evidence but does not replace local Windows 10 startup, ACL, Chrome profile, PowerShell and repository-root tests.
- Linux process-group containment remains LIMITED_NOT_CGROUP_V2; no hardened Linux production claim.
- PC host allow-lists are not a sandbox for arbitrary test/script code; only trusted tests/scripts may be enabled.
- ROOM-HOP Dashboard / PC Bridge integrated E2E remains a separate acceptance gate.
- No merge to main or release without Owner's separate approval.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**


## Current CI baseline update — 2026-11-22

After adding the Dashboard static contract suite, Run #69 is the current hosted regression baseline:
- Windows Server 2022: 206 PASS / 0 FAIL / 0 SKIP.
- Ubuntu 24.04: 200 PASS / 0 FAIL / 2 expected SKIP.
- Dashboard static contract: 17 PASS on each OS.
- V8 validator: 16 PASS on each OS.

See `06_EVIDENCE/W10_CROSS_PLATFORM_CI_EVIDENCE_20261122_RUN69.md`. This is hosted CI, not Owner PC acceptance.


## Shared Dashboard ingress boundary — 2026-11-22

Port `3000` is reserved for the single shared ROOM-HOP Dashboard ingress owned by W113. This Work 10 Dashboard is a standalone local development/acceptance UI and therefore serves on loopback port `3010` during isolated testing. Work 10 must not start a competing listener on port 3000. Production Work 10 Dashboard access must be mounted/registered by W113 under its approved Work route; the route path and embedding contract are not guessed here. The Agent API remains loopback-only and its exact Origin allow-list must be configured for the approved host origin before any integration. W113 integration is NOT VERIFIED.


## Current live Dashboard/API smoke baseline — Run #135

The full suite now includes `dashboard_live_e2e` (7 checks). Run #135:
- Windows Server 2022: 213 PASS / 0 FAIL / 0 SKIP.
- Ubuntu 24.04: 207 PASS / 0 FAIL / 2 expected SKIP.
- Dashboard static contract: 17 PASS per OS.
- Dashboard live health/API/consent smoke: 7 PASS per OS.
- Real Chromium API/runtime E2E: PASS per OS.

See `06_EVIDENCE/W10_LIVE_DASHBOARD_API_EVIDENCE_20261122_RUN135.md`. Hosted CI does not replace Owner PC acceptance.


## Local launcher / shutdown scripts — 2026-11-22

- `START_WORK10_LOCAL.ps1`: validates Python 3.12 and loopback ports 8787/3010, keeps writes and PowerShell roots disabled, generates a per-session bearer token, starts the Agent API and standalone Dashboard on loopback, checks health/Work ID 10, records process IDs without storing the token, copies the token to clipboard and opens the Dashboard. It never binds port 3000.
- `STOP_WORK10_LOCAL.ps1`: refuses to stop while an execution is active; validates process command line and start time against the session record before stopping only the two Work 10 processes.
- Run `./05_TEST/START_WORK10_LOCAL.ps1` after dependencies are installed, or add `-InstallDependencies` to install requirements and Chromium. Stop with `./05_TEST/STOP_WORK10_LOCAL.ps1`.
- The launcher does not configure production V8 HMAC trust, enable writes or enable PowerShell. Those remain explicit operator actions.
- `test_windows_launcher_contract.py` has 10 static safety assertions; GitHub Windows CI also parses both PowerShell files with the PowerShell AST parser.
