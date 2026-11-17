# WORK 28 — VI → AN INDEPENDENT QA HANDOFF
**Handoff ID:** W28-HO-AN-WP2-RECOVERY-20261118-PR61
**Execution time:** 2026-11-18 05:11:16 UTC+07:00
**From:** Vi | CODER
**To:** An | Independent QA / TESTER
**Work:** 28 — MCP Tooling Platform / WP2
**PR:** https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/61
**Branch:** `auto/work28-vi-wp2-recovery-20261118`
**Base SHA:** `8301a7f8fb6a91689482710a9006e2cdbab709c4`
**Current reviewed head at handoff:** `8ad00128de931adf2a3beacc647056dfb4a4663c`

## Scope for independent verification
Vi has implemented a recovery slice for the HIGH findings in Ka's review dated 2026-11-15:
1. Stop cleanup retains the service registry handle until process-tree cleanup is verified; failed cleanup remains BLOCKED and retryable.
2. A stale service leader is cleaned and its process group/Job Object drained before replacement; an uncertain cleanup prevents a new spawn.
3. Same-name service start/stop/status transitions are serialized under a registry lock.
4. A dead leader with remaining or unknown process membership is not reported STOPPED.
5. `JobObjectUnavailable.process_reaped` and abort notes are preserved in execute-command evidence; an uncertain suspended-process abort is not converted to `no_process / process_reaped=true`.

## Required tests
- Run `tests/test_wp2_service_mapping_and_race.py` on Linux and native Windows.
- Run `tests/test_process_job.py`, `tests/test_process_job_suspended_spawn.py`, `tests/test_execution_host.py` and the full Work 28 workflow.
- Verify same-name concurrent starts create exactly one registry entry/process.
- Verify stop cleanup failure preserves the handle and retry can later clear it.
- Verify stale leader + surviving child blocks replacement.
- Verify cleanup exception and unknown member count stay BLOCKED.
- Verify spawn abort with `process_reaped=false` remains false in FINAL_RESULT evidence and does not contain `no_process`.
- Repeat the concurrent same-name test at least 3 times if practical; inspect raw job logs and exact SHA.

## Evidence rules
Record exact tested commit SHA, OS/runner identity, command, pass/fail/skip counts, exit code, raw logs/artifact links and uncovered cases. Do not infer PASS from source readback or PR mergeability. Native Windows-only tests must execute on Windows, not merely skip on Linux.

## Boundaries
Do not touch the quarantined historical MCP :8020 listener, Core :8000, deployed Runtime or Execution Host :8031. Do not merge PR #61 or open the Execution Gate. Review/test only the exact PR head SHA and report findings independently.

**STATUS:** HANDOFF STAGED / AN ACKNOWLEDGEMENT AND INDEPENDENT TEST RESULT NOT YET OBSERVED.
**Signature:** [KÝ: VI | CODER]
