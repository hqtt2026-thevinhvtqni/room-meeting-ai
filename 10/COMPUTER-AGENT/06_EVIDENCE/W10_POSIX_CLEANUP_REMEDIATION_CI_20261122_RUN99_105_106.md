# WORK 10 — POSIX PROCESS-GROUP CLEANUP HARDENING — RUNS 99 / 105 / 106

- Document ID: W10-POSIX-CLEANUP-REMEDIATION-20261122-01
- Date-Time: 2026-11-22 06:37 (UTC+07:00)
- Implementer: Co | AI-07 / End-to-End Architecture & Implementation Lead
- Scope: Linux limited process-group cleanup reliability; Windows Job Object code unchanged.

## 1. Failure observed — Run #99

- Run ID: `44963052277`; tested commit: `d9be51ed64cff959a16bfba73b21fbf4530e4147`.
- Windows Server 2022: SUCCESS.
- Ubuntu 24.04: FAILURE in `process_containment` (1 PASS / 1 FAIL); other suites and real Chromium E2E passed.
- Exact failure: `POSIX process group kills worker and descendant (limited profile): AssertionError: process group did not become empty`.
- Root cause from the test/log path: after SIGTERM/SIGKILL, the process-group existence probe ran immediately after the worker leader exited. An orphaned descendant could still be present as a zombie awaiting init reaping; the implementation returned false without polling the bounded cleanup window. This was correctly fail-closed, but the check was too eager to declare cleanup unresolved.

## 2. Remediation

Updated `04_CODE/process_supervisor.py`:
- retains SIGTERM first;
- gives the group a short bounded grace period;
- sends SIGKILL to the group even when the leader has already exited;
- polls process-group identity until the configured deadline;
- returns PASS only when the process group no longer exists; permission/timeout/uncertain state remains BLOCKED/false.

Updated `05_TEST/test_process_containment.py`:
- POSIX descendant cleanup now repeats the worker + grandchild lifecycle three times per suite invocation to expose orphan/zombie timing races.
- It still treats inability to prove the group empty as failure.
- POSIX process-group profile remains explicitly limited; this is not cgroup-v2.

## 3. Follow-up CI

### Run #105 — implementation patch
- ID: `44963236229`
- Tested commit: `e46189f532f0d3405ac9fc8a57cf3cc27f3ccf06`
- Ubuntu 24.04: 200 PASS / 0 FAIL / 2 SKIP.
- Windows Server 2022: 206 PASS / 0 FAIL / 0 SKIP.
- Real Chromium E2E: PASS on both.
- Artifacts: Linux ID `14730532236`, SHA-256 `b8aba944a7773687564d6b62f8f24cdb14eeaf25a8b5e4d0d5fadd637ecc98bf`; Windows ID `14730203465`, SHA-256 `6ca40bf27dc57b7e35a369a0ddad3fcf941f26f3afe56764df749a6937862da0`.
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44963236229

### Run #106 — repeated descendant stress test
- ID: `44963255436`
- Tested commit: `12992e1d36dddb6443afd9eee1a756d7c04f5437`
- Ubuntu 24.04: 200 PASS / 0 FAIL / 2 SKIP.
- Windows Server 2022: 206 PASS / 0 FAIL / 0 SKIP.
- Real Chromium E2E: PASS on both.
- The POSIX test executed three worker/grandchild cleanup cycles; suite passed.
- Artifacts: Linux ID `14729499872`, SHA-256 `5009ab7adb92adf03556932b62b43a9bf0506aaafd7ccb15b3c9701803b0169c`; Windows ID `14730148883`, SHA-256 `045169804bfdc1d7f0b925a61dec4568256dcac95ecdf031d8835dc9e54e2fde`.
- URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44963255436

## 4. Disposition

- Run #99 failure: diagnosed and remediated.
- POSIX process-group cleanup polling: cross-platform CI PASS in #105.
- Three-cycle POSIX descendant stress: cross-platform CI PASS in #106.
- Linux containment remains `LIMITED_NOT_CGROUP_V2`; no hardened Linux production claim.
- Windows Job Object tests remain PASS; this patch did not change Windows containment.
- Physical Windows 10 and Linux cgroup-v2 production acceptance remain separate gates.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
