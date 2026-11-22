# WORK 092 — ONE-SHOT EXECUTION ORDER (2026-11-22)

This order records the user's latest end-to-end mission in `pasted_content.txt` and supersedes older wording where it conflicts. Complete the static prototype work in one pass; do not request intermediate ACKs, do not impersonate Nu or Xu, and do not self-accept.

## Goal and scope

Prepare ROOM-HOP Browser V2 as a demonstrable **TEST_ONLY static UI prototype** for independent review. Improve browser chrome, tabs, local navigation controls, Browse/Search/Workflow demos, action timeline, evidence provenance, permissions, responsive layout, and accessibility. This is not a request to build or enable a real browser or Browser Agent Runtime.

Work only in Work 092. Do not modify Work 91, ROOM-HOP Core, Sandbox Runtime, Opera, or other work. Do not merge to `main` or release.

## Binding safety boundaries

1. Runtime stays **BLOCKED**; UI runtime label stays **DISCONNECTED**. All simulated actions/evidence/completion must remain explicitly TEST_ONLY and must not claim a real website, agent, browser action, screenshot artifact, or external verification.
2. Do not build Chromium, open Browser Runtime, connect Opera, call Browser Agent APIs, or contact a website, API, or Internet from the prototype.
3. Do not start any service or run `tests/test_server.py`. Do not probe host/port availability. The optional preview source must bind only `127.0.0.1` and request an OS-assigned ephemeral port (`0`); the product remains usable from `file://`. Do not claim live service isolation because no server is started.
4. Use file-based Chromium UI checks only as UI evidence, never as Browser Runtime/E2E evidence. Android coverage must be named emulation, not physical-device testing.
5. Do not mark Work DONE/ACCEPTED. Xu owns independent acceptance; Vinh owns the final product decision. The current Manus executor is not independent evidence of Nu dispatch/ACK or Xu review.

## T6 / T8 / T17 evidence discipline

The canonical minute table (`BIEN_BAN_W092.md`) contains brief row-level descriptions. A separate detailed original acceptance-spec file for T6/T8/T17 was not found in the current Work 092 tree. Preserve that limitation rather than inventing additional acceptance language. Existing legacy `e2e-result.json` and `v2-e2e-result.json` are historical outputs, not normative criteria or proof for the current source.

- **T6:** test only the truthful local UI activity states (READY/RUNNING/HELD/COMPLETE) while Runtime remains DISCONNECTED. These are not real agent Connected/Working/Done transitions; keep T6 PARTIAL unless Xu determines the TEST_ONLY criterion is satisfied.
- **T8:** verify human-readable actions/descriptions in Browse, Search, and Workflow fixtures; keep each action's simulated provenance clear.
- **T17:** verify local file-based UI makes no HTTP(S)/WebSocket requests and statically confirm no client network API. Optional preview is source-configured loopback/ephemeral only, but since it is not started, process/backend isolation remains NOT RUN.

## Required evidence and handoff

Run JavaScript syntax checks, Node tests, static pytest, the existing file-based browser smoke, and the accessibility/responsive audit when the required local Chromium/Playwright environment is available. Record exact results, commit SHA, Actions run/artifact IDs, screenshots, and remaining NOT RUN/BLOCKED scope in the existing manifest, minutes, acceptance report, build journal, error log, and evidence index. A successful local test or CI run is not independent Xu acceptance.
