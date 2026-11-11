# EXECUTION HOST LINES RECONCILIATION — W1111 C03

- Prepared by: Co — Coder under Cla (CTO)
- Date: 2026-11-09 (UTC+7)
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- GitHub refs inspected: `main`, `work/28-mcp-tooling-platform`, `work/w1111-core-execution-authority-v1-2` (PR #48 head branch)
- Sandbox source: Work 13, `EXECUTION-HOST-INFRASTRUCTURE/04_CODE/execution_host/`
- Hash method: GitHub Contents API blob SHA for GitHub; locally computed Git blob SHA-1 (`blob <UTF-8 byte length>\0<content>`) for Sandbox readback. Hashes identify exact file content, not deployed process memory.

## 1. Blob SHA matrix

| File | GitHub main | W28 branch | W13 Sandbox | PR #48 branch | Disposition |
|---|---|---|---|---|---|
| server.py | `45aec57525b5d55bb63544b7bd7fd23062e06151` | `87644127a9a2df638b5677758cfc4d0c883b2985` | `b0d8308121a63332e1f0dcbff15e6f0da9c273e0` | `dd65fcfacfc171e673000ecbeba01d5842a42e8c` | DRIFT × 4 |
| host.py | `977b5bc5072eaf0a3ad054aecd22491483d621b1` | `40c93bb93dc1b6f4d1d002bd51acd8ee60cbef21` | `78a5620364c1e5da1e33033b5f1035509e2d0398` | `a914d36b14bdb5b3207282e7e8a989484421ccdc` | DRIFT × 4 |
| security.py | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | `d96979ac7a5ebd12324a357d3adada2479f93e80` | `4aa20fbc9c5939c49c85222916dc28fb8dd8075b` | GitHub refs MATCH; Sandbox DRIFT |
| w12_adapter.py | MISSING (404) | MISSING (404) | `32b34e4476d2b192c423a8c12f8a55c470769809` | MISSING (404) | GitHub MISSING; Sandbox PRESENT |
| wee_bridge.py | `eec29b8f43d907e06551329f4ed9e350f51352dc` | `2fb528f7748798312ba5aff610c2ea517b2c0b08` | `6597ceb30f15bdfdd4008cc2b027440815901406` | `eec29b8f43d907e06551329f4ed9e350f51352dc` | main = PR; W28/W13 DRIFT |

## 2. Drift descriptions

### server.py
- `main`: HTTP `/health` and `POST /execute`; the inspected handler has no bearer-token/Work allow-list enforcement.
- `work/28-mcp-tooling-platform`: separate hardening line adds bearer-token verification, static Work allow-list, request-size/content-type checks, fail-closed unknown fields and authenticated evidence readback. This is not main or proof of deployment.
- `work/w1111-core-execution-authority-v1-2`: PR #48 Core-grant-aware W13 HTTP boundary; caller-supplied WorkContext/authorized flags are rejected in favor of a grant-bound request and online Core grant validation (per PR source and recorded CI scope).
- W13 Sandbox: older canonical Work13 handler using the W12 adapter; its file hash differs from all three GitHub versions. No runtime import proof ties the current PC PID to this file.
- Main semantic split: transport bearer token/static allow-list (W28) is not equivalent to per-Work Core grant authorization (PR #48).

### host.py
- `main`: nested test result is stored under `result["test"]`, but top-level status/exit code remain those of the primary command; this permits false aggregate PASS.
- W28 branch: includes an initial propagation guard when primary command PASS and nested test not PASS, but it does not fully preserve/propagate all test exit/evidence details and has no distinct stage output directories in the inspected version.
- PR #48 branch: prior code also had only partial nested-status propagation. C02 has now added stage-specific `runtime/command` and `runtime/test` logs, primary status/exit-code preservation, nested FAILED/TIMEOUT/BLOCKED propagation when the primary command passes, and five regression tests. New host blob SHA is `a914d36b14bdb5b3207282e7e8a989484421ccdc`; test blob SHA is recorded in the C02 journal entry.
- W13 Sandbox: different older implementation; exact deployed parity is not established.

### security.py
- GitHub main, W28 branch and PR #48 branch have identical blob SHA, so those three exact GitHub file contents MATCH.
- W13 Sandbox has a different blob SHA. It must be treated as DRIFT until the actual content diff and the intended security-policy ownership are reviewed; no overwrite is authorized by this task.

### w12_adapter.py
- Present in W13 Sandbox only at the inspected canonical path.
- Not found (HTTP 404) at `execution_host/w12_adapter.py` on main, W28 branch or PR #48 branch. This is a path/source gap, not proof the adapter code is absent elsewhere in the repository.
- The W13 Sandbox copy remains the only verified copy at this exact path among the four requested source layers.

### wee_bridge.py
- GitHub main and PR #48 branch match exactly (same blob SHA).
- W28 branch differs; W13 Sandbox differs from all GitHub refs.
- A differing bridge hash means the branch-specific bridge contract must be inspected before any source synchronization; do not assume filename equivalence means behavior parity.

## 3. Canonical-source recommendation (proposal only; no source moved)

1. Treat PR #48 branch as the current **integration candidate** for Core-grant authorization and its updated host aggregate-status fix, subject to Cla review, CI on the exact updated SHA, explicit owner approval and live runtime verification.
2. Keep Work 13 Sandbox as the **current documented W13 source baseline** until a controlled, approved deployment establishes which source is actually active on PC.
3. Do not use W28 branch as a substitute for Core-grant authorization: its bearer-token/static Work allow-list is a different authorization model.
4. Do not label any of the four layers canonical-for-runtime until PID/module/build-hash evidence proves the deployed process loads that exact source.
5. Resolve the missing GitHub `w12_adapter.py` path and review the W13 `security.py`/bridge drift before proposing any convergence commit.

## 4. Evidence and limits

- GitHub source evidence: fetch_file responses for 15 path/ref combinations; exact blob SHAs recorded above.
- W13 Sandbox evidence: sandbox_read_probe status=ok for all five canonical files; Git blob SHA-1 computed from returned UTF-8 file contents.
- Missing path evidence: GitHub fetch_file returned 404 for `execution_host/w12_adapter.py` on all three refs.
- No Git checkout, local `git diff`, pytest, CI dispatch, runtime request, PC operation, file overwrite or merge was performed for this reconciliation.
- C02 code/test writes occurred on the PR #48 branch only; this C03 table records the resulting PR branch host SHA.

**Status:** C03 source hash matrix = COMPLETE for the five requested paths and four requested source layers; semantic review is bounded to inspected source/history; READY FOR CLA REVIEW.
