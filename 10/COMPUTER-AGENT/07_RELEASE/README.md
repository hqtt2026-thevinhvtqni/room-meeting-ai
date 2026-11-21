# 07_RELEASE — WORK 10 HANDOVER / RELEASE GATE

Work 10 is **ACTIVE — NOT RELEASED**. This folder contains handover documentation, not a production release.

## Current owner handover

- Current handover package: `W10_HANDOVER_PACKAGE_20261122.md`
- Status: prepared for Owner acceptance; physical Windows 10 validation, production V8 key provisioning, Linux cgroup-v2 and ROOM-HOP integration remain open.
- Historical handover: `WORK10_HANDOVER_TO_OWNER_20261117.md` is preserved as a dated historical snapshot and is superseded by the 2026-11-22 package for current implementation status.

## Release prerequisites

1. Complete the physical Windows 10 local acceptance procedure in `05_TEST/HOST_E2E_RUNBOOK.md`.
2. Provision production V8 validator HMAC key and exact validator/schema/policy pins; verify a signed attestation locally.
3. Decide and disposition Linux cgroup-v2 production containment.
4. Complete ROOM-HOP Dashboard / PC Bridge integrated E2E or record an explicit Owner-approved limitation.
5. Finish Sandbox↔GitHub inventory reconciliation and exact readback.
6. Owner reviews evidence, open risks and handover package, then issues a separate written acceptance/release decision.

No main merge, deployment, tag or production release is authorized by the handover package alone.
