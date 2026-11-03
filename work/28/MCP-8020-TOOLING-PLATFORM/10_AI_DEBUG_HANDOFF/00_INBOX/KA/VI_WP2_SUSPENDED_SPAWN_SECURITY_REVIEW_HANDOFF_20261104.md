# WORK 28 — VI → KA INDEPENDENT SECURITY REVIEW HANDOFF

**Handoff ID:** W28-HO-KA-WP2-20261104-01  
**Execution time:** 2026-11-04 04:09:53 UTC+07:00  
**From:** VI | CODER  
**To:** Ka | REVIEWER  
**Signature:** [KÝ: VI | CODER]  
**Branch:** `work/28-mcp-tooling-platform`

## Review target
- Implementation: `execution_host/process_job.py`, blob `85f4866df7710aa2ad0fe1601ae319c470f1718a`.
- Implementation commit: `2306b2899537ed40b56630d66abf69674c3cda4c`.
- Focused tests: `tests/test_process_job_suspended_spawn.py`, blob `831691a44a56d8634a4b13243d664b21b47f64ae`.
- Windows evidence byte-stability fix: `execution_host/work28_evidence.py`, blob `3d2560024b7f08050b0b0ad07a2ce750e5a92a95`.
- CI run: `41719431129`, three jobs SUCCESS; focused suite Linux 13 passed / 4 native-Windows skips, Windows 17 passed.

## Required independent review
1. Confirm Windows process is created suspended and no target instruction can execute before successful Job Object assignment.
2. Verify Job Object configuration includes kill-on-close and no breakaway semantics; inspect nested Job Object compatibility and inherited child containment assumptions.
3. Inspect every failure path: job create/configure, Popen, process assignment, thread snapshot/enumeration, OpenThread, ResumeThread, abort termination, handle closure and process reaping. Flag any path that can return a running/uncontained process.
4. Review abort cleanup when kill fails or wait times out; determine whether closing the Job Object reliably terminates the process and how unreaped status is surfaced.
5. Review POSIX behavior for regression and confirm OS isolation remains separately NOT_VERIFIED.
6. Verify the outer ExecutionHost.start_service() call path maps JobObjectUnavailable to structured BLOCKED; identify exact caller/route if not.
7. Review race/reentrancy gaps, especially concurrent starts, repeated cleanup, process handle lifetime and service shutdown.
8. Return severity-ranked findings with exact commit, file/line, scenario, remediation and retest criteria. Do not issue PASS based only on CI green status.

## Known open items
- Concurrent/repeated spawn-cleanup tests are not complete.
- Structured error mapping for start_service() remains unverified.
- Native Windows tests passed in CI; this is not a proof of OS sandbox isolation or live Core E2E.

**Requested review state:** INDEPENDENT SECURITY REVIEW REQUIRED.  
**Handoff state:** SENT TO CANONICAL KA INBOX / ACKNOWLEDGEMENT PENDING. GitHub persistence does not prove Ka has opened or accepted this handoff.
