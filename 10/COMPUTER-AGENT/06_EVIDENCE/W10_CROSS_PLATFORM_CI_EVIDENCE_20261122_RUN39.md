# WORK 10 — CROSS-PLATFORM CI EVIDENCE — RUN 39

- Evidence ID: W10-CROSS-PLATFORM-CI-RUN39-20261122
- Name: Co
- Title: AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:22 (UTC+07:00)
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/10-computer-agent-mirror`
- Tested commit: `d4c75478a2f5ce62b483d079d6049096d03ffdaa`
- Workflow run: [#39](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44956259543)
- Conclusion: SUCCESS — both matrix jobs completed successfully.

## 1. Windows Server 2022

- Runner: `Windows-2022Server-10.0.20348-SP0`
- Python: `3.12.10`
- Offline contract suite: 60 passed / 0 failed.
- Safety policy suite: 45 passed / 0 failed.
- HTTP API suite: 39 passed / 0 failed.
- Total offline checks: 144 passed / 0 failed / 0 skipped.
- Real Chromium E2E: PASS.
- Workflow artifact ID: `14727394221`
- Artifact ZIP SHA-256: `4d40f0dd3de4bc05bdc860b6192327cfed63594912b636bb4168240c086915c9`
- Offline evidence JSON SHA-256: `80f5c893e832c15d3bfde41c0b4ca72ae9aa89c4130b9f6c98f4905893f677d5`
- Real-browser result JSON SHA-256: `af7cb8b56311eb13d17d288a3bb8ebfe7f3ff9faaeb12b78171acbf4ab132444`
- Screenshot PNG SHA-256: `80bbaa48bf4f5293d80fa91517087233479a35cb2b499d0245c66822018e924f`
- Real-browser result: status PASS; state trace PLANNED → RUNNING → VERIFYING → PASS; 13 action steps; 14 evidence entries.

## 2. Ubuntu 24.04

- Runner: `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`
- Python: `3.12.16`
- Offline contract suite: 60 passed / 0 failed.
- Safety policy suite: 41 passed / 0 failed / 1 Windows-only skip.
- HTTP API suite: 39 passed / 0 failed.
- Total offline checks: 140 passed / 0 failed / 1 skipped.
- Real Chromium E2E: PASS.
- Workflow artifact ID: `14728010540`
- Artifact ZIP SHA-256: `0c47e7717268263a671d60d047d5f984f1d1c2fe77af1f59e8dc4a8e4cb965fd`
- Offline evidence JSON SHA-256: `85e25699ffc3c1dd91a0312449bbcae19ee1ddf9547b68964403f6aaec8fbac2`
- Real-browser result JSON SHA-256: `a0e2e84204e54522f4bb08237bd7171fa95c6916790a56a750d06bb1642efacd`
- Screenshot PNG SHA-256: `e02d255d636b709227030091e9bfa63e752edf3f92b7657920623bebf7c67db0`
- Real-browser result: status PASS; state trace PLANNED → RUNNING → VERIFYING → PASS; 13 action steps; 14 evidence entries.

## 3. Interpretation and limitations

- This run verifies the exact tested GitHub branch commit on hosted Windows Server 2022 and Ubuntu 24.04 runners.
- Windows Server 2022 Job Object/process-tree containment was NOT tested by this run; the process-supervisor implementation and its dedicated tests were added after this commit and require a later run.
- The Ubuntu process group is not equivalent to Linux cgroup-v2 containment.
- The hosted Windows runner is not the Owner's physical Windows 10 PC. No claim is made about local PC PowerShell, Chrome profile, filesystem ACLs or ROOM-HOP local bridge integration.
- The run's offline-test evidence was generated before the real-browser step, so its `host_chromium_e2e` field says NOT RUN even though the separate real-browser result artifact is PASS. The workflow/evidence ordering is being corrected in the next revision.
- P0 process isolation, durable owner fencing, semantic acceptance validator and integrated ROOM-HOP E2E remain open.

## 4. Disposition

**CI PASS — LINUX + WINDOWS**

This is a cross-platform contract/API/browser baseline only. It does not close P0 or authorize release. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
