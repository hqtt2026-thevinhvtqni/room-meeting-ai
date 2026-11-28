# DOC-062 — BROWSER ADAPTER :8787 GATE RECHECK AND RUN #18 EXACT-SHA EVIDENCE

- **Document Number:** DOC-062
- **Priority order:** P0 — Resolve remaining browser-adapter E2E blocker without fabricating a PASS
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Date-Time:** 2026-11-04 13:45:29 Asia/Ho_Chi_Minh
- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** work/32-ci-cd-python-ci-v2
- **Exact HEAD SHA:** 450c0b2409c0d19c68931cb0331652bac6f3b5df
- **Workflow:** .github/workflows/ci-validation.yml
- **GitHub Actions run:** #18 / 41787301060
- **Run URL:** https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41787301060

## 1. Latest exact-SHA CI verification

Run #18 completed with conclusion SUCCESS on exact HEAD SHA `450c0b2409c0d19c68931cb0331652bac6f3b5df`. All four jobs and all steps completed successfully.

| Job | Result | Evidence |
|---|---|---|
| Python 3.12 compile + bounded unit | SUCCESS | 167 passed |
| Work 32 tooling | SUCCESS | 20 unittest cases, OK |
| Product Auto E2E | SUCCESS | 45 passed, 1 Starlette/httpx deprecation warning |
| Immutable product artifact | SUCCESS | 1 passed; archive checksum verified |

Artifacts (not expired at verification time):
- Tooling: ID `13301911411`, SHA-256 `524f2ff6573f55b101028d2c803447e6274a6dc1ca23c2349048cc25c331d517`.
- E2E: ID `13301867192`, SHA-256 `f25d4e1f8b0edf3736e415bf576ee3ba140e69184f2c346d268ff5976c21e155`.
- Unit: ID `13301751797`, SHA-256 `1e02459701c01b22a8be0614bbba67b6b1b1a08fd18813e451a70255bcba0be3`.
- Immutable product candidate: ID `13301487100`, SHA-256 `9666fdbad0265f9f49ace8568ccc4ace7bfaa8a72ef805499ceef96258e8b58e`.

## 2. Browser adapter source and endpoint contract

Read the exact branch source:
- `tests/test_browser_agent_adapter_e2e.py`, blob `acdc0f0970e32261a5871cbe3983c27656e653ab`.
- `room_hop_mcp/browser_agent_adapter/adapter.py`, blob `0ced9207c1897b9a7b572b7fefa44fec2dd92b76`.

Confirmed behavior:
1. The E2E test POSTs to `http://127.0.0.1:8787/browser/execute_workflow`.
2. It requires a live Playwright/Chromium adapter and checks real navigation, DOM inspection, extraction, wait and screenshot.
3. The adapter requires `ROOMHOP_MCP_URL` for ROOM-HOP MCP handoff.
4. The adapter selects `ROOMHOP_MEETING_ID` when configured; otherwise it falls back to the first active meeting. The test asserts the exact meeting ID `MEETING-MCP-LIFECYCLE-001`, so deterministic execution requires that environment variable to identify this meeting.
5. The test also asserts submission status PASS and transcript read-back true.

Vinh reports that port 8787 is open. This is recorded as user-provided operational context, not as a Ka-observed health-check result. The test binds its target to loopback `127.0.0.1`; a GitHub-hosted runner's loopback is the runner itself, not the user's PC. The current connected ROOM-HOP MCP tools expose Sandbox/meeting operations but no PC terminal, SSH, port-forward or remote command execution. Attempts to resolve the local endpoint from the current execution plane did not produce a health response. Therefore Ka cannot truthfully claim to have executed this test against the user's PC service in this session.

## 3. Coverage disposition

Run #18 coverage report explicitly returned:
- `unaccounted_test_files=2`
- `missing_whitelisted_files=0`
- `NOT RUN BY CI: tests/test_browser_agent_adapter_e2e.py`
- `NOT RUN BY CI: tests/test_f4_resource_limits.py`

No tests were removed, skipped or weakened. `CHECK_STRICT=1` remains disabled and strict coverage remains NOT AUTHORIZED.

## 4. Next executable closure conditions

- Browser adapter E2E: execute the existing test from the same PC/runtime where `127.0.0.1:8787` is listening, with `ROOMHOP_MCP_URL` set and `ROOMHOP_MEETING_ID=MEETING-MCP-LIFECYCLE-001`; retain stdout, adapter evidence JSON/screenshot, ROOM-HOP transcript read-back and exact source SHA. If hosted CI execution is required, a registered self-hosted runner on that PC (or an approved reachable endpoint with authenticated routing) must be evidenced; do not point a GitHub-hosted runner at its own loopback and call it the PC service.
- F4: remains a separate unresolved policy/implementation task. Its test source explicitly marks several assertions as expected to fail until byte-limit, MCP schema and repeated-request policy are implemented. No F4 implementation or policy was inferred from the browser port being open.
- Strict coverage, main merge, CD/staging, deployment, release and production changes remain outside this execution.

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 13:45:29 Asia/Ho_Chi_Minh
- **Record:** Re-read Xu ADR-003, Work 32 gate/evidence records, exact branch workflow, browser E2E test and Browser Agent Adapter implementation; inspected exact-SHA run #18 jobs/logs/artifacts and coverage report. Recorded Vinh's port-open statement without converting it into an independently observed health PASS.

## NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 13:45:29 Asia/Ho_Chi_Minh
- **Priority:** P0
- **Action:** Reconciled the latest branch HEAD and run #18; confirmed the Browser Adapter test's loopback target, MCP environment requirements and fixed meeting assertion; determined the current control plane has no PC-local execution/port-forward facility.
- **Result:** Run #18 PASS, 4/4 jobs; browser-adapter test remains NOT RUN by hosted CI; F4 remains unresolved. User-reported port-open state is acknowledged but not independently health-checked from this execution plane.
- **Disposition:** Track A hosted CI = PASS on exact SHA; Browser Adapter E2E = READY FOR SAME-HOST EXECUTION / NOT VERIFIED; F4 = BLOCKED pending policy/implementation; strict coverage = NOT AUTHORIZED; Track B = BLOCKED per Xu ADR-003; CD = BLOCKED; Work 32 = ACTIVE — NOT RELEASED.


## Addendum — ROOM-HOP meeting prerequisite readback (2026-11-04 13:47 Asia/Ho_Chi_Minh)

A live ROOM-HOP MCP `list_meetings` read returned `MEETING-MCP-LIFECYCLE-001` with status `active`. The exact meeting asserted by the browser E2E test therefore exists and is active. Other active meetings also exist (including `MEETING-2026-009`), so the adapter must be started with `ROOMHOP_MEETING_ID=MEETING-MCP-LIFECYCLE-001`; otherwise its fallback to the first active meeting is nondeterministic relative to the test's fixed assertion. This closes the meeting-existence prerequisite only; it does not prove the :8787 endpoint health or browser workflow execution.


## Addendum — Browser Adapter execution deferred by user availability (2026-11-04 14:02 Asia/Ho_Chi_Minh)

Vinh confirmed he is not currently at the PC. The same-host test against `127.0.0.1:8787` is therefore formally **DEFERRED — WAITING FOR PC ACCESS**. This is not a product defect, not a failed test, and not a PASS. The exact test, adapter endpoint, active meeting ID and required environment variables have been recorded in this document. Resume when the PC/runtime is available; no user-side command is required now.
