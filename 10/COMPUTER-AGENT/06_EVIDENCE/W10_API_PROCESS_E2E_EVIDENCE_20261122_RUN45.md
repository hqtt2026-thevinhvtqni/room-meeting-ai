# WORK 10 — INTEGRATED API + PROCESS CONTAINMENT + REAL BROWSER E2E — RUN 45

- Evidence ID: W10-API-PROCESS-E2E-RUN45-20261122
- Name: Co
- Title: AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:40 (UTC+07:00)
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/10-computer-agent-mirror`
- Tested commit: `bba3c18fab5b81f02177d002b91eeee0b9db87d5`
- GitHub Actions: [Run #45](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44957836070)
- Conclusion: SUCCESS — both Windows Server 2022 and Ubuntu 24.04 matrix jobs succeeded.

## 1. Windows Server 2022

- Runner: `Windows-2022Server-10.0.20348-SP0`, Python 3.12.10.
- Offline contract: 60 PASS.
- Safety negative suite: 45 PASS.
- HTTP API: 37 PASS.
- Process containment + owner lease: 2 PASS.
- Total: **144 PASS / 0 FAIL / 0 SKIP**.
- Integrated real Chromium E2E through HTTP API: **PASS**.
- API response: HTTP 200; state trace PLANNED → RUNNING → VERIFYING → PASS; 13 action steps; 15 evidence entries.
- Process containment: `windows-job-object-kill-on-close-v1`; assurance `OS_JOB_OBJECT_ATOMIC_JOB_LIST`; Job Object active processes after cleanup = 0; forced cleanup = false.
- Screenshot: `06_EVIDENCE/real-browser-e2e.png`, 21,662 bytes.
- Artifact ID: `14728032174`.
- Artifact ZIP SHA-256: `666d826ce49a3080cd4e1af53c05dde9b4aaa34f23725ae72363acc0f9844619`.
- Offline evidence JSON SHA-256: `3184594ffd1ddaa09eb8c98f1f6c5a7a73399dd8a98f3d114e01e6633f959e37`.
- E2E result JSON SHA-256: `08e444318884f50a970fb42f56407120c63a4577afab2806be10929e717e84c3`.
- Screenshot SHA-256: `80bbaa48bf4f5293d80fa91517087233479a35cb2b499d0245c66822018e924f`.

## 2. Ubuntu 24.04

- Runner: `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`, Python 3.12.16.
- Offline contract: 60 PASS.
- Safety negative suite: 41 PASS / 1 Windows-only SKIP.
- HTTP API: 37 PASS.
- Process containment + owner lease: 2 PASS.
- Total: **140 PASS / 0 FAIL / 1 SKIP**.
- Integrated real Chromium E2E through HTTP API: **PASS**.
- API response: HTTP 200; state trace PLANNED → RUNNING → VERIFYING → PASS; 13 action steps; 15 evidence entries.
- Process containment: `posix-process-group-limited-v1`; assurance `LIMITED_NOT_CGROUP_V2`; process group empty verified; forced cleanup = false.
- Screenshot: `06_EVIDENCE/real-browser-e2e.png`, 28,465 bytes.
- Artifact ID: `14728212970`.
- Artifact ZIP SHA-256: `a54a3a160cca570fba5461407d8279d0f0cf885fc4509ad1621fd7e6f3a34f6d`.
- Offline evidence JSON SHA-256: `9f431d3c230c4cff0fbc4da05e7d9c5b78df847652f61f90c2b565ceaf0eac32`.
- E2E result JSON SHA-256: `46122cb094dd79bca6fb53ab864af46a87463bc68bf5222f2d7102742052a14a`.
- Screenshot SHA-256: `e02d255d636b709227030091e9bfa63e752edf3f92b7657920623bebf7c67db0`.

## 3. What this run now proves

1. HTTP authentication, exact Origin allow-list, body validation and execution admission work with the process supervisor.
2. A normal workflow executes in an isolated worker and returns PASS only after post-condition verification.
3. The Windows worker is created atomically inside a named Job Object via `PROC_THREAD_ATTRIBUTE_JOB_LIST`; its real Chromium/browser descendants are included in the Job Object lifecycle.
4. Parent verifies the containment is empty before releasing the request lease.
5. Timeout regression returns BLOCKED, terminates the contained worker tree, verifies empty containment and permits the next request only after cleanup.
6. Host owner lease and monotonically increasing owner generation are exercised by HTTP tests.
7. Real Chromium E2E is executed through the HTTP API and ProcessSupervisor, not by constructing AgentRuntime directly in the test process.

## 4. Remaining acceptance boundaries

- Windows evidence is from hosted Windows Server 2022, **not the Owner's physical Windows 10 PC**. Local PowerShell startup, ACL, user profile, Chrome profile and ROOM-HOP PC bridge remain to be verified on the target PC.
- Linux process-group mode is explicitly limited and test-only. Hardened Linux production profile remains BLOCKED pending cgroup-v2 implementation and fixture.
- Work 10's file-system and PowerShell capability contract/API are not yet implemented; current canonical Action Contract remains browser-oriented and LOCKED.
- V8 acceptance-manifest semantic validator and its negative suite remain open.
- Integrated ROOM-HOP Dashboard / PC Bridge acceptance remains open.
- Source parity and final Sandbox↔GitHub inventory must be reconciled after the remaining implementation.

## 5. Disposition

**CROSS-PLATFORM API + PROCESS SUPERVISOR + REAL CHROMIUM E2E: PASS (RUN 45).**

This is a major implementation milestone, not final Work 10 release acceptance. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
