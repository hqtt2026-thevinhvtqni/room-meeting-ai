# WORK 10 — PROCESS CONTAINMENT PRIMITIVE CI — RUN 40

- Evidence ID: W10-PROCESS-CONTAINMENT-CI-RUN40-20261122
- Name: Co
- Title: AI-07 / End-to-End Architecture & Implementation Lead
- Date-Time: 2026-11-22 05:22 (UTC+07:00)
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`
- Branch: `work/10-computer-agent-mirror`
- Tested commit: `975f534c42acd5e5164430d784be47f96f77c1da`
- Workflow run: [#40](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44956485849)
- Conclusion: SUCCESS — both matrix jobs completed successfully.

## Windows Server 2022

- Runner: `Windows-2022Server-10.0.20348-SP0`, Python 3.12.10.
- Offline/safety/HTTP: 144 checks PASS, 0 FAIL, 0 SKIP.
- Dedicated process containment test: PASS — Windows Job Object contains worker + grandchild; closing the Job Object with KILL_ON_JOB_CLOSE terminates the descendant tree.
- Real Chromium E2E: PASS; state trace PLANNED → RUNNING → VERIFYING → PASS.
- Artifact ID: `14728215548`.
- Artifact ZIP SHA-256: `d75276de58bbf637ba53c347093c151d077044f64f8c08e0a19b78542de64e1e`.
- Offline evidence JSON SHA-256: `17be526337bf069e6c3e28dc4701b36c6da457129fbfd028312005f380031093`.
- Process containment log SHA-256: `044d8bd7da1d869cc9d822f208dbe148e5bf12587941cfea947c9658969b0baf`.
- Real-browser result JSON SHA-256: `e07aa5e266f56c08118f156788a076b4cf9dd377d6eef643b6a9c896e39c18d2`.

## Ubuntu 24.04

- Runner: `Linux-7.0.0-1017-azure-x86_64-with-glibc2.39`, Python 3.12.16.
- Offline/safety/HTTP: 140 checks PASS, 0 FAIL, 1 Windows-only SKIP.
- Dedicated process containment test: PASS — POSIX process group terminates worker + grandchild. This is explicitly a LIMITED profile and is not equivalent to cgroup-v2.
- Real Chromium E2E: PASS.
- Artifact ID: `14728110742`.
- Artifact ZIP SHA-256: `545dd89eb419e9f60609c5c39023df5cddefc0a7c5df8a3876b1d461bdec34fd`.
- Offline evidence JSON SHA-256: `d15667204e4664ad40b952e1144e61692bc8a5f248e3bdc418125b49ac113830`.
- Process containment log SHA-256: `c9c941401bab6a33e47de9cadb40868c4e118bfdbd01c79876085f9505cb8557`.
- Real-browser result JSON SHA-256: `22b87fa5c87b403155117761d33c53331cb5183d0e637b631218bcb5c8241a53`.

## Scope and limitations

- This proves the standalone Windows Job Object primitive can contain and terminate a worker plus its descendant on a hosted Windows Server 2022 runner.
- It does NOT yet prove the Computer Agent HTTP API actually launches each workflow inside that Job Object. The runtime integration is the next implementation task.
- Linux process-group fallback is limited; hardened Linux profile remains BLOCKED pending cgroup-v2 fixture and containment oracle.
- Hosted Windows Server 2022 is not the Owner's physical Windows 10 PC.
- Durable owner fencing, recovery journal, semantic acceptance validator, HTTP abort stack and integrated ROOM-HOP E2E remain open.

## Disposition

**CI PASS — WINDOWS JOB OBJECT PRIMITIVE + LIMITED POSIX PROCESS GROUP.**

P0 process isolation is NOT YET CLOSED because the primitive is not yet wired into the API execution path. Work 10 remains ACTIVE — NOT RELEASED.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
