# Initial Evidence Log — Work 32

Date: 2026-10-19 (Asia/Ho_Chi_Minh). Executor: Xu (AI-01), coordinator.
Updated: 2026-11-04 (Vibe agent; Phase B runs #1–#4, repair loop, handoff proposal).
Updated: 2026-11-05 (Vibe agent; G7 approval, mcp pin, run #5–#7 verdicts + product-drift finding).

## Phase A — Survey evidence
- Reviewed available ROOM-HOP architecture context and repository metadata read-only.
- Created Work 32 Sandbox through MCP :8020 and wrote design/acceptance documentation.
- Created GitHub branch `work/32-ci-cd-room-hop-python-no-docker` from the then-current main head `cc3100c835ad87ac9670a2ba38dc2c2dfae63755`.
- No PC changes, live-service changes or deployment.

## Mirror verification (completed 2026-11-04)
- Mirror verified via GitHub content read-back: all 11 documented files readable and match the README manifest.
- GitHub head of Work branch at verification: `8098d1a7d00d68858442b7fac72ba70a1a0a46f8`.
- Current main head rechecked: `d7266eb9bfedfc534fc87d56548e47841bb583b9` (differs from branch base — merge/backport must be re-planned before integration).
- Prior blocker (sandbox_read returns empty object): worked around by reading mirror content directly from GitHub.

## Survey findings (baseline)
- requirements.txt (as surveyed): pyyaml>=6.0, pytest>=7.0, python-dotenv>=1.0.0, groq>=0.11.0 (main branch carries the same incomplete file).
- pytest.ini: pythonpath=. ; norecursedirs excludes tests/legacy.
- No .github/workflows existed on the Work branch before Phase B.

## Phase B — Minimal CI pilot (authorized by Vinh on 2026-11-04)
Workflow: `.github/workflows/work32-ci-pilot.yml` — Work-branch-only; permissions contents:read + issues:write; no Docker, no secrets, no deploy. G3/G5 files (live-service/e2e) excluded from G2 by design.

### Run history (evidence-first dispositions)
| Run | Commit | G1 | G2 | G6 | Disposition |
|---|---|---|---|---|---|
| [#1](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786211574) | 39e6191 | PASS | FAIL (scope too broad) | artifacts only | Repair 1/3: G2 scoped to unit tests only |
| [#2](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786558557) | d54626e | PASS | FAIL | FAIL (issue lookup) | Repair 2/3: deterministic evidence lookup |
| [#3](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41786658982) | fd93d3e | PASS | FAIL (exit 2, collection errors) | PASS → issue #39 | G4 finding 1: undeclared deps |
| [#4](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41787560785) | 750c08d | PASS | FAIL (exit 1; 10 failed) | PASS → issue #39 | G4 finding 2: mcp 2.x API break |
| #5, #6 | be6e7c3 / 2374ce5 (docs-only pushes) | PASS | FAIL (same 10 mcp tests; 178 passed) | PASS → issue #39 | No code change; expected repeat |
| [#7](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41941796297) | 95495b9 | PASS | **FAIL (exit 1; 3 failed, 185 passed)** | PASS → issue #39 | mcp pin effective (10→3); remaining = product-drift finding (below) |

### G4 finding 1 (fixed 2026-11-04): undeclared dependencies
- Code imports `requests`, `mcp`, `fastapi`, `uvicorn` — none declared. Fixed via requirements.txt.

### G4 finding 2 (fixed 2026-11-05): mcp SDK major-version incompatibility
- `mcp>=1.0` resolved to 2.x (removed `@server.list_tools()`); pinned to `mcp>=1.14,<2.0` after G7 approval.
- Effect: 10 failing tests → 3 failing tests (185 passed).

### Product-drift finding (run #7 — G5 scope, OPEN — requires Coder under approval, NOT a CI defect)
1. `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression`: `room_hop_mcp/adapter/server.py` registers only 4 tools (`add_paste_to_meeting`, `get_meeting`, `get_transcript`, `list_meetings`); the frozen contract ("6 tools KHÔNG đổi, KHÔNG thêm add_message") requires also `join_meeting` and `start_meeting`.
2. `tests/test_f4_resource_limits.py` (2 tests): `add_paste` inputSchema is `{'type': 'string'}` without `maxLength`; F4 policy contract requires `maxLength == 1048576`.
- These are product/test-contract mismatches in the source under test — outside the CI pilot's repair scope. Candidate paths: (a) Coder restores the 2 missing tool registrations + `maxLength` in server.py after Vinh's approval; or (b) Reviewer/QE confirms whether main head `d7266eb…` already carries the fix (branch divergence from base `cc3100c…` is a plausible cause and must be checked first).


### Main-head reconciliation check (2026-11-05, after run #7 — per Vinh's instruction)
- Read `room_hop_mcp/adapter/server.py` and the failing tests on main head `d7266eb9bfedfc534fc87d56548e47841bb583b9`.
- **Main does NOT carry a fix**: main's server.py also registers only 4 tools (list_meetings, get_meeting, get_transcript, add_paste_to_meeting) and its add_paste schema has no maxLength.
- **Finding A — the 2 F4 failures are INTENTIONAL design markers**: `tests/test_f4_resource_limits.py` states in its header that some tests SHOULD FAIL until F4 resource limits are implemented; the failing pair (`test_add_paste_schema_declares_maximum_length`, `test_add_paste_schema_limit_matches_f4_policy`) is exactly that documented "expected FAIL" evidence. They are not regressions and arguably should not gate G2 as hard FAILs (candidate: deselect/mark as design markers in the G2 scope, or implement F4 maxLength to turn them green).
- **Finding B — test T8 is genuine contract drift**: `tests/test_message_v1.py::test_t8_existing_mcp_tools_no_regression` asserts the frozen 6-tool contract (incl. `join_meeting`, `start_meeting`), but server.py (both branch and main) exposes only 4. `MeetingService` has join/start methods; the MCP adapter simply does not register them. Fix path: register the 2 missing tools in `room_hop_mcp/adapter/server.py` (Coder scope, after Vinh's approval), or amend the frozen contract (Reviewer + Vinh decision; test comment says "KHÔNG đổi").
- Gate impact: G2 could reach PASS-with-evidence by (1) registering the 2 tools, and (2) either implementing the F4 maxLength (per policy MAX_TEXT_BYTES = 1048576) or scoping the 2 design-marker tests out of the hard gate.

### G7 decision record
- 2026-11-05: Vinh instructed "triển khai tiếp w32" → recorded as approval to apply the proposed mcp pin from this session and verify via CI (executed, run #7).

### Evidence channels
- Canonical tracking issue: [#39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39) — auto-posted per-run summary + log tail.
- Issue #38 closed as duplicate. Artifacts retained 14 days per run; CI job-log API download requires repo admin.


### Product-fix execution (2026-11-05, per Vinh: "Hoàn thiện đi làm")
- Commit `c37040c463325916e99e3dc791a20fe35cc206e6`: `room_hop_mcp/adapter/server.py` now registers the frozen 6-tool contract (`join_meeting`, `start_meeting` added; MeetingService already implemented both) and declares `maxLength: 1048576` on `add_paste` `text` (F4 policy), closing both Finding A and Finding B.
- **Run [#10](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41944927224) — SUCCESS: G1 PASS, G2 PASS with 188 passed / 0 failed (2.94s). Evidence in issue #39.**
- Final gate state: G0 PASS · G1 PASS · G2 PASS (188/188, executed evidence) · G6 PASS · G7 PASS (Vinh, 2026-11-05). G3/G5 BLOCKED by design (Phase C). CD/deployment NOT RUN (out of scope this phase).

## NOT DONE — remaining items for Xu (handoff 2026-11-05)
1. **G3 integration gate** — MCP → Core → runtime contract tests need isolated fixtures (live-service prerequisites unavailable to this session; Phase C requires separate approval).
2. **G5 E2E gate** — excluded files (`test_e2e.py`, `test_integration.py`, `test_http_lifecycle.py`, `test_http_recording.py`, `test_browser_agent_adapter_e2e.py`, `test_wee_8031_bridge.py`, `test_work13_wee_integration.py`, `test_execution_host.py`) remain unexecuted in CI (BLOCKED by design).
3. **Main-head reconciliation** — Work branch is based on `cc3100c…`; main is at `d7266eb…`. Merge/rebase plan, plus porting the requirements.txt dependency fix and the 6-tool/maxLength fix to main, is undecided (main's own suite would still fail the same 3 tests without them).
4. **Merge/PR** — no pull request opened; no merge performed (guardrail: no AI auto-merge; requires Reviewer + Vinh).
5. **CD/release** — Phase D not authorized; no deployment, rollback plan, or release notes produced.
6. **sandbox_read MCP endpoint** — still returns empty content (worked around via GitHub read-back; fix belongs to the Work 24/28/30 tooling track).

### Gate status (after run #7)
- G0, G1, G6: PASS with evidence. G7: PASS (Vinh, 2026-11-05).
- G2: FAIL — remaining 3 failures are product-drift (see finding above); CI-side work complete.
- G3/G5: BLOCKED by design (Phase C).
- Next: Vinh decides product-repair path (Coder scope) or main-head reconciliation first.

## PR handoff record (2026-11-05)
- Draft PR [#40](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/40) opened: `work/32-ci-cd-room-hop-python-no-docker` → `main`. Draft on purpose — no AI auto-merge; Reviewer checks diff/risks (noting branch base `cc3100c…` vs main `d7266eb…`), Vinh decides integration.
- Main's own CI workflows (if configured on PRs to main) will also run on this PR; treat their results as additional evidence, not a substitute for review.
- Phase B acceptance item "Verify PR behavior and disclose skipped gates" satisfied: PR opened, skipped gates disclosed in the PR body (G3/G5 NOT RUN by design; CD NOT RUN).
- Remaining NOT-DONE list unchanged — see "NOT DONE — remaining items for Xu" above.

### Phase C step 1 — G3/G5 isolated exploration (2026-11-05, per Vinh: "Tiếp đi")
- Commit `c6dc8a787732ca530528bad841b9415ab76bc7d5`: added `g3-g5-exploration` job (continue-on-error) to `work32-ci-pilot.yml` — runs each of the 8 previously-excluded integration/e2e test files in isolation on the hosted runner, uploads per-file logs as artifacts (`work32-g35-evidence-<run_id>`), and posts per-file dispositions to issue #39. Evidence-only; no hard gate; no live-PC changes.
- Runs #11 (5d7fbff) and #12 (9625400) — doc-only commits under the pre-Phase-C workflow: SUCCESS (G0–G2 re-verified green; evidence in issue #39).
- **Run #13 (G3/G5 exploration, commit c6dc8a7) — job success. Per-file dispositions (isolated runner, evidence-only):**
  | Test file | Verdict |
  |---|---|
  | tests/test_e2e.py | **PASS** (exit 0, 1 passed) |
  | tests/test_integration.py | **PASS** (exit 0, 5 passed) |
  | tests/test_http_lifecycle.py | **PASS** (exit 0, 7 passed) |
  | tests/test_http_recording.py | **PASS** (exit 0, 4 passed) |
  | tests/test_browser_agent_adapter_e2e.py | **FAIL** (exit 2, collection error: connection refused to 127.0.0.1:8787 /browser/execute_workflow — requires live browser-agent service) |
  | tests/test_wee_8031_bridge.py | **PASS** (exit 0) |
  | tests/test_work13_wee_integration.py | **FAIL** (exit 1 — requires live WEE service/fixtures) |
  | tests/test_execution_host.py | **PASS** (exit 0) |
- **Interpretation (for Xu)**: 6 of 8 excluded files PASS in a plain isolated runner — safe candidates to fold into the CI (G2/G3) scope. The 2 FAILs are live-service dependencies (browser-agent :8787, WEE), NOT CI defects; keep them excluded or wire up service stubs/fixtures (Phase C scope decision for Xu + Vinh).
- **Anomaly — ci-pilot job of run #13**: no "Run #13 (G0–G2)" evidence comment appeared on issue #39 after extended monitoring (the G3/G5 comment posted normally; runs #11/#12 ci-pilot comments are present). ci-pilot verdict for run #13 = **NOT CONFIRMED** (missing evidence comment; job log needs admin to inspect). Note: the G0–G2 code path is unchanged since run #10 (only the workflow file changed), so a G2 regression is unlikely — but per evidence-first doctrine this is recorded as unconfirmed, not assumed PASS. Xu should inspect run #13's ci-pilot job log; if the comment step failed (e.g. secondary rate limit from the concurrent `gh issue comment`), add retry/backoff to both comment steps.
- Gate impact: G3/G5 now have exploration-level executed evidence. Promoting any file into a hard gate still requires Xu/Vinh decision (Phase C scope).


## Execution journal — 2026-11-06 (Asia/Ho_Chi_Minh)
Coordinator: Xu (AI-01). Requested by Vinh: record the current test evidence and continue Work 32 with Ka (AI-02 / CSA reviewer).

### READ / TRACE — current GitHub baseline
- Work branch: `work/32-ci-cd-room-hop-python-no-docker`.
- Branch HEAD verified: `d93402a4c0c6a6875e73c0240f168fb4be73cfb4`.
- PR [#40](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/40) remains OPEN + DRAFT, base `main` at `d7266eb9bfedfc534fc87d56548e47841bb583b9`; not merged. No merge/deploy performed.
- Canonical CI evidence tracker: [Issue #39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/39).

### Latest verified CI evidence
- Push run [#14](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41979573352), commit `d93402a4c0c6a6875e73c0240f168fb4be73cfb4`: workflow conclusion SUCCESS. Both jobs succeeded: G0–G2 and G3/G5 isolated exploration. This is a workflow/job status, not a claim that every explored test passed.
- PR validation run [#18](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/42169429080), commit `edde8ee0b2fa4a0ae7e944adc69db4d249ada641` (PR event): G0–G2 PASS, **190 passed / 0 failed**. Treat this as PR validation evidence; it does not change the Work branch HEAD recorded above.
- Latest per-file G3/G5 exploration published to Issue #39 (run #18): **6/8 files PASS; 2/8 FAIL**. PASS: `test_e2e.py`, `test_integration.py`, `test_http_lifecycle.py`, `test_http_recording.py`, `test_wee_8031_bridge.py`, `test_execution_host.py`. FAIL: `test_browser_agent_adapter_e2e.py` (connection refused at `127.0.0.1:8787/browser/execute_workflow`); `test_work13_wee_integration.py` (real WEE host reports `BLOCKED`, while test expects `PASS`). These remain exploration-only; do not label G3/G5 fully PASS.
- Two Starlette deprecation warnings were emitted by HTTP lifecycle/recording tests; non-fatal in the observed run.
- A cleanup log previously exposed `fatal: No url found for submodule path 'room-meeting-ai' in .gitmodules`; the job still concluded SUCCESS. Treat this as a separate cleanup/configuration defect to investigate, not as a passing cleanup check.

### DECISION / current gate posture
- G0–G2: PASS with executed CI evidence (latest PR run #18: 190/190).
- G3/G5: PARTIAL EXPLORATION EVIDENCE (6/8 pass; 2 service-dependent failures). Not accepted as fully passing gates.
- G6: artifacts/evidence publication succeeded in observed runs.
- G7: prior Vinh approval remains recorded; no new approval inferred for merge or deployment.
- PR #40: OPEN + DRAFT; human review and Vinh integration decision remain required.
- CD/deployment: NOT RUN.

### Ka handoff — AI-02 / CSA review (next execution)
Objective: turn the exploration evidence into a safe, reviewable Phase C plan without weakening tests or claiming unsupported PASS.

1. **Baseline and divergence review:** compare Work branch `d93402a` with current `main` `d7266eb`; identify changed files, merge-base, conflicts and any main-only changes. Deliver a file-level risk matrix and a recommended integration sequence. Do not rebase, force-push, merge or alter main.
2. **G3/G5 classification:** review the eight test files and classify each as hermetic (self-contained), fixture-backed, or live-service dependent. Recommend which of the six passing files can be promoted into a deterministic CI gate, with exact commands and dependencies. Do not delete or skip failing tests to obtain green.
3. **Service contract plan:** specify the minimum isolated service/fixture contract for Browser Agent `:8787/browser/execute_workflow` and Work13/WEE. Identify owners, required startup/health checks, teardown, and what constitutes real evidence. Do not replace live integration with a fake PASS.
4. **Submodule cleanup diagnosis:** trace the `.gitmodules` warning to its source and propose a minimal safe repair with a regression check.
5. **Acceptance handoff:** produce a review report listing evidence, unresolved risks, test matrix, recommended owners (Cla/Vi for code changes; An/Qw for verification), and explicit human decision points. Keep PR #40 DRAFT until the review is complete and Vinh decides integration.

### Xu coordination guardrails
- Ka is assigned review/architecture/acceptance planning as CSA; implementation changes require a separate scoped coder task and review.
- No edits to production code, no merge, no CD/deployment, no secrets, no Docker, and no use of ROOM-HOP :8020.
- Next evidence must be linked from Issue #39 and this log. A green workflow alone is not sufficient; report per-gate and per-file outcomes.
- Status at journal close: **ACTIVE — REVIEW/HANDOFF IN PROGRESS — NOT RELEASED**.
