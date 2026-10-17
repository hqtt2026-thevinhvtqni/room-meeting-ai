# Work 30 — GPT Autonomous Build Team

Work 30 is maintained as a numbered Work at the repository root, parallel to the ROOM-HOP Sandbox Work ID `30`.

- **Sandbox source:** Work ID `30`, name `GPT-AUTONOMOUS-BUILD-TEAM`
- **GitHub mirror:** `30/GPT-AUTONOMOUS-BUILD-TEAM/`
- **Canonical repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`
- **Current phase:** independent planning; implementation remains gated on Vinh's approval of the consolidated Plan.

## Sync integrity

This directory establishes the numbered Work location and publishes the currently verified Work 30 governance documents. It is **not yet a complete byte-for-byte Sandbox mirror**: the ROOM-HOP Sandbox read endpoint returned empty responses for source-file readback during this operation, so code/evidence files have not been represented as if they were copied. Do not treat this structural mirror as E2E verification.

## Governance documents

- [Team model decision](02_EXTENSION/WORK30_TEAM_MODEL_DECISION_V1.md)
- [Independent planning request](02_EXTENSION/WORK30_INDEPENDENT_PLAN_REQUEST_V1.md)
- [Multi-AI planning loop](02_EXTENSION/WORK30_MULTI_AI_PLAN_LOOP_V2.md)
- [Nu/Vi coder model](02_EXTENSION/WORK30_CODER_MODEL_NU_VI_V2.md)
- [Cla independent challenge gate](02_EXTENSION/WORK30_CLA_INDEPENDENT_CHALLENGE_GATE_V1.md)

## Required synchronization protocol

1. Read and trace the Sandbox source before copying.
2. Preserve relative paths under `GPT-AUTONOMOUS-BUILD-TEAM/`.
3. Exclude generated caches (`__pycache__`, `*.pyc`) and machine-specific `desktop.ini`.
4. Verify every copied file by readback/hash; report missing files as BLOCKED, never PASS.
5. Keep Sandbox and GitHub evidence aligned; log actor, role, timestamp, commit, and verification result.

See `02_EXTENSION/MIRROR_SYNC_STATUS.md` for the current status.
