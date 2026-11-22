# WORK 10 — ROOT-BOUNDARY + ACCEPTANCE-RUNNER CI — RUN 230

- Document ID: W10-ROOT-BOUNDARY-ACCEPTANCE-RUNNER-CI-20261122-RUN230
- Run ID: `44967028038`; Run #230
- Exact tested commit: `eac6db5ed228cea64d030839f07232c7a492a995`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44967028038
- Conclusion: SUCCESS — Ubuntu 24.04 and Windows Server 2022 jobs both passed.

## Ubuntu 24.04
- Job ID: `137038249362`
- Total: **229 PASS / 0 FAIL / 2 expected SKIP**
- Windows launcher/acceptance contract: **22 PASS**
- HTTP API: 52 PASS
- Dashboard static: 17 PASS
- Dashboard live E2E: 7 PASS
- V8 validator: 16 PASS
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14731619080`; size 43,178 bytes
- ZIP SHA-256: `b3b12e9c4908d28ea398ec5a457de6a0a2adf3d85245ab2eb9a793681db755b1`

## Windows Server 2022
- Job ID: `137038249610`
- Total: **235 PASS / 0 FAIL / 0 SKIP**
- Windows launcher/acceptance contract: **22 PASS**
- PowerShell AST syntax: START, STOP and RUN_WORK10_ACCEPTANCE scripts all PASS.
- Local launcher smoke: PASS — API :8787 + Dashboard :3010, Work ID 10 health, HTTP 200, verified STOP.
- HTTP API: 52 PASS
- Dashboard static: 17 PASS
- Dashboard live E2E: 7 PASS
- V8 validator: 16 PASS
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14730864925`; size 37,127 bytes
- ZIP SHA-256: `d9f1490f990f21fc827d8f97f6295f1d91ac57d2d76a4e94fc99e2f4b2b9fd2e`

## Root-boundary controls verified by the 22-check contract

- Default read root is the Work 10 directory.
- Additional roots must exist; drive roots and network-share roots are rejected.
- Writable and PowerShell roots must be descendants of an allowed read root.
- Separate `-EnableWrite` and `-EnablePowerShell` switches are required.
- Session record stores configured roots and enabled flags, not the bearer token.
- Static Dashboard process does not inherit the API bearer token.
- Startup failure removes its session record and clears secret variables.
- STOP refuses to terminate while execution is active and verifies PID command line + start time.

## Acceptance runner boundary

- Windows CI parses `RUN_WORK10_ACCEPTANCE.ps1` successfully but does not execute it because it intentionally requires a Windows 10 client, while GitHub uses Windows Server 2022.
- The acceptance runner is intended for Owner's physical Windows 10 PC. It runs launcher smoke, full test suite, real Chromium E2E, hashes source/contracts/schemas and writes timestamped JSON/logs.
- The report keeps release gate OPEN and records only presence of the production HMAC environment variable; actual production key/pin/signature validation is NOT RUN.

## Disposition

- Root-boundary and local launcher contract: PASS.
- Windows PowerShell AST + local start/stop smoke: PASS.
- Full hosted regression: Windows 235 PASS; Ubuntu 229 PASS + 2 expected SKIP.
- Physical Windows 10 acceptance remains NOT RUN.
- Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
