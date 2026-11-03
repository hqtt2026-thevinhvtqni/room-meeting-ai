# WORK 28 — VI → AN INDEPENDENT QA HANDOFF

**Handoff ID:** W28-HO-AN-WP2-20261104-01  
**Execution time:** 2026-11-04 04:09:53 UTC+07:00  
**From:** VI | CODER  
**To:** An | TESTER  
**Signature:** [KÝ: VI | CODER]  
**Branch:** `work/28-mcp-tooling-platform`

## 1. Exact canonical artifacts

| Artifact | Branch path | Blob SHA / commit |
|---|---|---|
| Suspended-spawn implementation | `execution_host/process_job.py` | blob `85f4866df7710aa2ad0fe1601ae319c470f1718a`; source commit `2306b2899537ed40b56630d66abf69674c3cda4c` |
| Focused 17-test suite | `tests/test_process_job_suspended_spawn.py` | blob `831691a44a56d8634a4b13243d664b21b47f64ae`; test commit `25a6d96cbf8d7b2c08ef0d907417d9cc5ce640b6` |
| CI workflow with explicit pytest invocation and Windows exit-code checks | `.github/workflows/work28-mcp-tooling.yml` | blob `a0980124a4eb9e66b5f87ee56de126c4d4cf243e`; workflow guard commit `2987b1b49bd8b6a6549769307d64dd5e2f7468e0` |
| Windows evidence byte-stability fix | `execution_host/work28_evidence.py` | blob `3d2560024b7f08050b0b0ad07a2ce750e5a92a95`; commit `f60091bbd3ab92368d786d517f0eaed370723472` |

The WP2 implementation uses Job Object creation/configuration before spawning; Windows process creation with CREATE_SUSPENDED; assignment to the Job Object; then resume. Failure paths abort the suspended process and raise `JobObjectUnavailable`. Both `spawn_managed()` and `spawn_managed_service()` use the shared spawn path. POSIX uses a new session/process group. OS isolation remains NOT_VERIFIED.

## 2. CI evidence to reproduce independently

**GitHub Actions run:** `41719431129`  
**Tested branch commit:** `f60091bbd3ab92368d786d517f0eaed370723472`  
**Run URL:** https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/41719431129

| Job | Job ID | Result | Focused suite result |
|---|---:|---|---|
| execution-host-lifecycle-linux | 126207966906 | SUCCESS | 13 passed, 4 skipped (native-Windows-only) |
| execution-host-lifecycle-windows | 126207966141 | SUCCESS | 17 passed |
| unit-regression-tests | 126207966714 | SUCCESS | configured Work 28 unit/regression suite completed successfully |

Windows log additionally confirms the two previously failing evidence-seal tests and the readback HTTP tests pass after the newline-stable byte-write fix. Before that fix, the Windows workflow had been masking intermediate Python failures; the workflow now exits on every nonzero Python command. Please inspect raw job logs, not just the green summary.

## 3. Independent QA requests

1. Re-read the exact canonical source and test blobs above; do not rely on this description as proof.
2. Independently reproduce the 17-test suite on native Windows and Linux. Confirm all four native Windows tests actually execute on Windows and are skipped only on Linux.
3. Inspect process ordering and failure cleanup: Job Object creation/configuration failure; Popen failure after Job creation; assignment failure; thread enumeration/snapshot failure; OpenThread failure; ResumeThread failure; abort kill failure; process reaping and handle closure.
4. Add adversarial concurrent/repeated spawn-cleanup race tests. Include parallel service starts and execution jobs, and assert no child can execute before containment.
5. Trace `ExecutionHost.start_service()` through the outer API and verify `JobObjectUnavailable` is translated to a structured BLOCKED result rather than an uncaught error. Do not weaken fail-closed behavior to achieve this.
6. Check regression behavior for existing process cleanup, timeout, cancellation and POSIX session-group containment.
7. Report exact commit, runner OS, command, raw output/log link, pass/fail/skip counts, uncovered cases and severity-ranked findings.

## 4. Known limitations / acceptance boundary

- Concurrent/repeated spawn-cleanup race coverage is not complete.
- Outer API mapping for `start_service()` still needs proof.
- Four native Windows tests were skipped on Linux as intended; Windows job is the evidence that they executed.
- No OS sandbox isolation claim; `ISOLATION_STATUS=NOT_VERIFIED`.
- No live Core authorization E2E, deployment or release acceptance is claimed.

**Requested QA state:** INDEPENDENT VERIFICATION REQUIRED.  
**Handoff state:** SENT TO CANONICAL AN INBOX / ACKNOWLEDGEMENT PENDING. GitHub persistence does not prove An has opened or accepted this handoff.
