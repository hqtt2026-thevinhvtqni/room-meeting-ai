# WORK 10 — FINAL LOCAL LAUNCHER / HTTP REGRESSION — RUN 180

- Document ID: W10-LOCAL-LAUNCHER-HTTP-CI-EVIDENCE-20261122-RUN180
- Workflow: Work 10 Cross-Platform Verification
- Run ID: `44965583364`; Run #180
- Exact tested commit: `1d64e841b10bf1a68bc3dba2484ff0bcfbd7d415`
- Branch: `work/10-computer-agent-mirror`
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44965583364
- Conclusion: SUCCESS — Ubuntu 24.04 and Windows Server 2022 jobs both passed.

## Windows Server 2022
- Job ID: `137033738113`
- PowerShell AST parser: START and STOP scripts PASS.
- Local launcher smoke: PASS — API loopback :8787 + Dashboard :3010 start; health Work ID 10; Dashboard HTTP 200; STOP verifies process command line/start time and stops only session processes.
- Contract: 60 PASS
- Safety: 45 PASS
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 14 PASS
- V8 validator: 16 PASS
- Dashboard static: 17 PASS
- Dashboard live E2E: 7 PASS
- Windows launcher contract: **13 PASS**
- Total: **226 PASS / 0 FAIL / 0 SKIP**
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14731581984`; size 36,850 bytes
- ZIP SHA-256: `4c99a7cf5a3ea33b6666223403dd7bd17fc43bc8c2e56b505f6914df85894ddb`

## Ubuntu 24.04
- Job ID: `137033737895`
- Contract: 60 PASS
- Safety: 41 PASS / 2 expected Windows-only SKIP
- HTTP API: 52 PASS
- Process containment: 2 PASS
- Host operations: 12 PASS
- V8 validator: 16 PASS
- Dashboard static: 17 PASS
- Dashboard live E2E: 7 PASS
- Windows launcher contract: **13 PASS**
- Total: **220 PASS / 0 FAIL / 2 expected SKIP**
- Real Chromium API/runtime E2E: PASS
- Artifact ID: `14731102249`; size 42,941 bytes
- ZIP SHA-256: `abfeb8ee4927b33866342e7f60852d126015586403b0754c7cead832a7d76dd4`

## Final fixes included in this run

1. **Windows oversized HTTP body test:** Run #169 had a Windows WinError 10053 because urllib could still be sending a 1 MiB+ body when the server rejected its Content-Length. The test now sends the oversized Content-Length header without uploading the body; API runtime still rejects >1 MiB with HTTP 413. Run #175 passed this fix; Run #180 revalidates it.
2. **Launcher token isolation:** Agent API receives the per-session bearer token in its child-process environment; the static Dashboard server starts only after the parent clears that environment variable, so it does not inherit the API token.
3. **Launcher failure cleanup:** if startup fails, the script stops processes it started, clears token variables and removes the session record.
4. **Launcher safety contract:** 13 static assertions pass on both OS runners.
5. **Windows start/stop:** PowerShell AST parse + noninteractive launcher smoke pass on Windows Server 2022.

## Limitations

- The Windows runner is Windows Server 2022, not the Owner's physical Windows 10 PC.
- CI uses `-NoClipboard -NoOpenBrowser`; interactive clipboard copy and default-browser launch require physical PC acceptance.
- Production V8 HMAC key/pins are not provisioned.
- Linux containment remains LIMITED_NOT_CGROUP_V2.
- W24/W112/W14/W113 runtime integration and F-15 timeout mapping remain open.
- No main merge, deployment or release occurred.

**Disposition:** Latest hosted cross-platform baseline PASS — Windows 226 PASS, Ubuntu 220 PASS + 2 expected SKIP. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
