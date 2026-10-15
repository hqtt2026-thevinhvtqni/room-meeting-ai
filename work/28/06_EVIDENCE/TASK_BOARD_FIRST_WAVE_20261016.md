# WORK 28 — TASK BOARD / FIRST EXECUTION WAVE
Date: 2026-10-16 (+07)
Scope: Work 28 only. Work 13 stays locked and untouched.

## Task 1 — Xu (P0, start immediately)
GitHub issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/8
- Read current branch README, workflow, technical journal, gap decision and capability audit.
- Produce a source/test/evidence matrix and identify the exact canonical test command and latest branch CI status.
- Verify one read-only call and raw registry only if the supported PC :8020 path is available; otherwise record exact BLOCKED evidence.
- Fix the first confirmed Work 28-only defect and add regression tests. Do not wait for other reviewers before doing independent work.

## Task 2 — Go (P0, parallel)
GitHub issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/9
- Independently reproduce tests at the current Work 28 revision.
- Return SHA, command, exit code, passed/failed/skipped counts, logs, mock-vs-live classification and smallest defect list.
- Do not touch Work 13 or weaken assertions.

## Task 3 — Cla (P0, parallel)
GitHub issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/10
- Review identity/Core auth, path containment, caller-supplied identity, limits, secrets, mutation/readback and evidence trust.
- Return file/function-specific findings, severity, reproducible evidence and minimal Work 28-only fixes.
- Do not modify Work 13 or weaken tests.

## Task 4 — Ka CSA (P1, after/alongside initial evidence)
GitHub issue: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/issues/11
- Build gate matrix with evidence URL/run ID, commit SHA and PASS/FAIL/BLOCKED for each gate.
- Verify latest branch CI and submodule cleanup warning; give evidence-based release verdict.
- No merge/release/lock while mandatory gates remain unverified.

## Observed facts at task creation
- Work 28 README says current status ACTIVE / NOT LOCKED and live MCP → Core → runtime E2E remains blocked/unverified.
- Workflow `.github/workflows/work28-mcp-tooling.yml` runs `python -m unittest discover -s 05_TEST -v` from `work/28/MCP-8020-TOOLING-PLATFORM`, with `PYTHONPATH=04_CODE`.
- Prior journal records CI run 38769093143 with 56 tests OK and a post-job submodule cleanup warning; this is historical unit/regression evidence, not live E2E.
- Tool-gap decision prioritizes verifying canonical API/source before adding `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, `capability_discover`.
- Live PC MCP :8020 `tools/list`, authenticated identity/Core authorization, and canonical execution E2E are not verified in the inspected evidence.
- The user's report of 26 targeted tests PASS/exit 0 is retained as user-supplied evidence; this session has not independently opened its log file or verified the checkout SHA.

## Dispatch caveat
GitHub issues were created as durable task specifications. They are not proof Go, Cla or Ka received/accepted the tasks or started execution; their GitHub assignees were not guessed. Xu proceeds with the work that can be performed directly and records any access limitation.
