
# EXECUTION HOST SOURCE TRACE — WORK 1111

Ngày: 2026-11-08  
Repository: hqtt2026-thevinhvtqni/room-meeting-ai  
Default branch: main  
Phạm vi: source inspection only; no runtime invocation, no code mutation.

## 1. Repository and identity anchors
- GitHub repository metadata: public; default branch main.
- Latest commit returned first by GitHub commit search (committer-date descending): dc87d852920514357f082b9615c050733699e847 — docs(work70): verify dashboard assignment journal readback. This is a search result, not a PC/runtime attestation.
- agents/xu.yaml on main: blob 225b9ec95c3274fc18796fc0bfe0df8f42b835a9; id=xu.

## 2. Main branch source evidence

| File | Blob SHA | Source finding |
|---|---|---|
| execution_host/server.py | 45aec57525b5d55bb63544b7bd7fd23062e06151 | HTTP /health and POST /execute; no token/Work allow-list check visible in this handler |
| execution_host/host.py | 977b5bc5072eaf0a3ad054aecd22491483d621b1 | subprocess execution, timeout cleanup, stdout/stderr and FINAL_RESULT evidence |
| execution_host/security.py | 4aa20fbc9c5939c49c85222916dc28fb8dd8075b | executable allow-list, command validation, workspace/evidence containment, safe environment |
| execution_host/models.py | 2488b7c95cf3784fc26eaf677044fe5ab0866420 | WorkContext carries authorized boolean, execution workspace and evidence root |
| execution_host/identity.py | 517dbb36bbdbfa3b606a6dec98c82612e12eeefa | runtime instance/build hash/start time/PID/platform/bind address |
| execution_host/wee_bridge.py | eec29b8f43d907e06551329f4ed9e350f51352dc | HTTP bridge defaults to 127.0.0.1:8031 |
| tests/test_execution_host.py | 183cba2959db9d9fb00751055efdeddd09c14a64 | 10 tests cover core process/evidence/security/service behaviors |

## 3. Separate hardening branch

Branch work/28-mcp-tooling-platform exists. Its execution_host/server.py blob is 87644127a9a2df638b5677758cfc4d0c883b2985. It adds:
- X-Room-Hop-Execution-Auth bearer-token verification.
- Static authorized Work allow-list.
- 256 KiB body cap, JSON content-type validation and fail-closed unknown body keys.
- Authenticated evidence readback.

This is NOT main. No evidence in this inspection proves this branch was merged, deployed, or running on PC.

## 4. Cross-Work architecture findings already recorded in W70 DOC-061

- Shared bearer token proves token possession, not distinct AI/principal identity.
- Work allow-list is static deployment configuration, not dynamic per-assignment/role/action authorization.
- Core grant fetch can fall back to a local registry when Core grant fetch fails.
- snapshot_only defaults false; ordinary command mode remains possible unless explicitly configured otherwise.
- Actual Windows service, startup config, firewall/proxy and deployed source/build hash are NOT VERIFIED.
- The reviewed execution_host.execute_work() attaches nested test result but returns top-level status from the primary command. A failing test command may not propagate to top-level status. Existing inspected test inventory does not exercise run_test=True with failing test.
- W70 DOC-061 already contains the fuller audit and corrected historical disposition. W1111 records this trace as a pointer, not a competing duplicate audit.

## 5. Correct state

- Source implementation :8031: PRESENT on GitHub main.
- Hardened handler: PRESENT on separate branch only in this comparison.
- MCP 8030 process/pytest tool: NOT EXPOSED in current capability list.
- Live :8031 listener, deployed branch/SHA/build hash, auth configuration, Core grant source and network perimeter: NOT VERIFIED.
- W1111 execution authorization: NOT CONFIGURED / NOT VERIFIED; no execution attempted.
- No code/test/runtime mutation performed.

## 6. Next verification sequence
1. Inspect the canonical Work 13/Execution Host handoff and exact source synchronization records.
2. Compare main and hardening branch by path/blob SHA; do not cherry-pick or overwrite.
3. Locate the approved PC startup/service configuration and attest actual PID, bind address, runtime build hash and source revision using read-only evidence.
4. Verify Core grant origin, auth token provisioning, Work allow-list, snapshot mode and network boundary without exposing secrets.
5. Add/verify regression coverage for nested test failure propagation and strict response identity binding before any runtime use.
6. Only then consider a bounded harmless execution probe; capture request ID, exact source SHA, health identity, exit code, stdout/stderr, evidence readback and cleanup. Do not execute until authorization and isolation contract are verified.

## 7. Work 13 canonical PC handoff / historical attestation

Read in Work 13 Sandbox:
- PC_INTEGRATION_HANDOFF.md: canonical package entrypoint is python -m execution_host.server; default bind 127.0.0.1:8031; /health and /execute; intended evidence includes FINAL_RESULT.json, runtime stdout/stderr and runtime identity.
- WEE_8031_BRIDGE_STATUS.md: bridge source/contract WRITTEN; compile/pytest in current Room-Hop session NOT RUN; live HTTP :8031 NOT RUN from this session.
- W13_CANONICAL_PC_RUNTIME_ATTESTATION_BLOCKER_LOG.md (2026-10-08): historical PID 5188, Python 3.12, listener 127.0.0.1:8031, /health PASS; instance_id w13-686df0ff197e4d478fbe68f8e03c44a8; build_hash f7adcf88fe3db910b0f4572c370ab4274805dc193367247db3e8ad8d8f877098; Windows 10. POST /execute was inconclusive/not run due client-side PowerShell parameter issue and PSReadLine rendering crash.
- W13_CANONICAL_PC_RUNTIME_DECISION_LOG.md keeps canonical PC runtime attestation BLOCKED and explicitly says not to repeat already-PASS /health or repeat architecture audit absent new evidence.
- Work 13 stored server.py is pre-hardening W12ExecutionAdapter implementation. Do not infer that current PC runs this file or the separate Work 28 hardened branch.

Disposition: historical health PASS only; current PC runtime and build NOT VERIFIED; valid /execute evidence absent. No live request was sent by W1111.
