# DOC-122 — Work32 Dedicated PC Self-Hosted Runner Identity Probe

- **Document Number:** DOC-122
- **Priority:** P0 — runner provenance / CI execution integrity
- **Work:** 32 — CI/CD
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- **Status:** READ-ONLY PROBE ADDED — RUN PENDING

## 1. Purpose

Earlier Work32 PR CI used GitHub-hosted Windows for Browser Adapter E2E. The dedicated runner identity step was skipped on pull_request, so those runs did not prove that the user's ROOM-HOP-W32-PC self-hosted runner was online or executing jobs.

## 2. Probe behavior

A separate optional job named Work32 dedicated PC runner identity (read-only) now targets labels self-hosted, Windows, X64 and verifies that the actual runner name is exactly ROOM-HOP-W32-PC.

The job performs only read-only checks:
- runner name, OS, architecture and runner temp path;
- Python and Git executable path/version;
- listener presence and owning process name/PID on ports 8010, 8020, 8030, 8031 and 8787.

It does not checkout source, modify files, start/stop processes, access credentials, invoke sandbox_read(), or execute protected commands. For pull_request events, the Work32 release_gate now requires this probe to succeed. A queued probe keeps the release gate pending; a wrong runner identity fails the gate. On push events the probe may be skipped unless the dedicated self-hosted Windows Browser Adapter lane is enabled by the repository variable.

## 3. Expected outcomes

- If the runner is online with matching labels and identity, the job completes and records the actual PC toolchain/listener snapshot.
- If the runner is offline or labels are absent, the job remains queued; this is evidence that the Windows service being Running locally is not sufficient proof of GitHub runner connectivity.
- If a different self-hosted Windows X64 runner claims the job, the exact-name check fails.

## 4. Acceptance boundary

The probe does not provision or enable Execution Host :8031. It does not prove Core/Host authority configuration, protected execution, or production readiness. Those remain separate gates.

**Current status:** Probe added to the PR workflow; exact execution result pending. PROTECTED EXECUTION DENIED; Work32 ACTIVE — NOT RELEASED.

## BIÊN BẢN
- **Name:** Ka
- **Title:** CSA / Work32 Execution Owner
- **Date-Time:** 2026-11-12 00:25 Asia/Ho_Chi_Minh
- Recorded a read-only exact-identity check for the dedicated Work32 PC runner.

## NHẬT KÝ
- **W32-LOG-20261112-115**
- Added a separate self-hosted runner identity probe without changing the existing release gate.
## 5. Run #390 observation and correction

- Run #390 scheduled the probe on the exact runner ROOM-HOP-W32-PC; GitHub log identifies runner version 2.338.2, group Default and machine ADMIN-PC. The runner successfully claimed the job, proving it is connected and matches the self-hosted Windows X64 labels.
- The first step failed before executing PowerShell statements because the machine's Execution Policy blocked GitHub's temporary .ps1 script. This is a shell-launch policy issue, not a runner registration or label issue.
- Corrective workflow change: both probe steps now invoke PowerShell with -NoProfile -ExecutionPolicy Bypass -File {0}. This applies only to the job process; it does not modify machine/user ExecutionPolicy.
- Run #390 remains a failed historical probe. A new run is required to prove the corrected probe.
- The pull_request release_gate now depends on the probe; it cannot PASS while the probe is queued or failed.