# WORK 10 — PC HOST CAPABILITIES + API PROCESS CONTAINMENT — RUN 49

- Evidence ID: W10-HOST-CAPABILITIES-RUN49-20261122
- Name: Co
- Title: AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:52 (UTC+07:00)
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Branch: work/10-computer-agent-mirror
- Tested commit: c11319e26bc6578baaf71e664152c259ee0c1e37
- GitHub Actions: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44958804750
- Conclusion: SUCCESS — Windows Server 2022 and Ubuntu 24.04 jobs both succeeded.

## 1. Windows Server 2022

- Offline contract: 60 PASS.
- Safety negative suite: 45 PASS.
- HTTP API: 49 PASS.
- Process containment / owner lease: 2 PASS.
- Host operations: 14 PASS.
- Total: **170 PASS / 0 FAIL / 0 SKIP**.
- Real Chromium API E2E: PASS; 13 actions, 15 evidence entries; final state PASS.
- Process assurance: OS_JOB_OBJECT_ATOMIC_JOB_LIST; containment empty verified; forced cleanup false.
- Host operations:
  - list_directory: PASS.
  - read_file + SHA-256: PASS.
  - write_file + read-back; implicit overwrite denied; explicit overwrite accepted: PASS.
  - path traversal outside allowlisted root: BLOCKED.
  - run_pytest: PASS.
  - run_powershell_script: PASS using allowlisted .ps1; outside-root script: BLOCKED.
  - generic shell operation: BLOCKED/not exposed.
- Artifact ID: 14728826352.
- Artifact ZIP SHA-256: 28612379a95de8247cfc5a4c7a9c6c1690b62ad873e6c8fac309ecd136260249.
- Offline evidence JSON SHA-256: e67f264fad9748305e002ed5cda51b30a8bfc5d7ca1afd3b82b74bc88cc51e26.
- E2E result JSON SHA-256: 995b26499e53ffccd310d4209c41ccb9d734d91c45dc89a867dee44fbd6ad6af.
- Screenshot SHA-256: 80bbaa48bf4f5293d80fa91517087233479a35cb2b499d0245c66822018e924f.

## 2. Ubuntu 24.04

- Offline contract: 60 PASS.
- Safety negative suite: 41 PASS / 1 Windows-only SKIP.
- HTTP API: 49 PASS.
- Process containment / owner lease: 2 PASS.
- Host operations: 12 PASS / 1 PowerShell-only SKIP.
- Total: **164 PASS / 0 FAIL / 2 SKIP**.
- Real Chromium API E2E: PASS; 13 actions, 15 evidence entries; final state PASS.
- Process assurance: LIMITED_NOT_CGROUP_V2; process group empty verified; forced cleanup false.
- Host operations:
  - list_directory/read_file/write_file: PASS.
  - traversal rejection: PASS.
  - run_pytest: PASS.
  - PowerShell correctly BLOCKED on non-Windows.
  - generic shell operation: BLOCKED/not exposed.
- Artifact ID: 14728158260.
- Artifact ZIP SHA-256: 53f88be0f1e151318fd3f7760578a0498536fa6db267eda0e5999bf5d666ea1b.
- Offline evidence JSON SHA-256: d3f9cf05d4c425266eeeb61c2842766ba277d66824a8a029ed7be6e2ca39713a.
- E2E result JSON SHA-256: 2389febe37f543cb6dfec53e6828ef9439fb1cdca685919c9d80a44db7bd35d5.
- Screenshot SHA-256: e02d255d636b709227030091e9bfa63e752edf3f92b7657920623bebf7c67db0.

## 3. What is proven

1. File-system list/read/write host capabilities operate through the authenticated host API and ProcessSupervisor.
2. Path traversal and symlink escapes are rejected; writes require an explicit writable-root configuration, explicit overwrite, and exact read-back/hash.
3. Pytest runs through a fixed Python module command, with allowlisted paths, generated empty config, disabled ambient plugin autoload and conftest discovery confined to the selected cwd.
4. PowerShell runs only on Windows, only for existing .ps1 files under explicit PowerShell roots, using -NoProfile -NonInteractive -File. No inline PowerShell or generic shell endpoint exists.
5. Pytest and PowerShell child processes inherit the same OS containment as the worker; parent verifies the containment empty.
6. Browser and host capability APIs share the same bearer authentication, Origin policy, body-size boundary, execution lease and parent deadline.

## 4. Remaining acceptance boundaries

- Hosted Windows Server 2022 is not the Owner's physical Windows 10 PC. Local install/startup, user account ACL, actual repository root, Chrome profile, PowerShell profile and local process-tree evidence remain NOT RUN.
- Linux is a LIMITED process-group test profile, not cgroup-v2.
- V8 semantic acceptance-manifest validator and trusted-runner attestation remain OPEN.
- Integrated ROOM-HOP PC Bridge / Dashboard E2E remains OPEN.
- Full Sandbox↔GitHub source parity and final exact-hash inventory remain to be rechecked.
- Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
