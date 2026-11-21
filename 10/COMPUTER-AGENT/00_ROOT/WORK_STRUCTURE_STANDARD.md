# ROOM-HOP — Work Structure Standard v1.0
Date: 2026-10-28
Owner: Xu — AI-01 / CEO coordinator
Status: STANDARD PROPOSED FOR ADOPTION; Work 10 implementation below is active.

## Required areas in every Work

1. `08_DASHBOARD/` — operational dashboard source. It must display live/API-backed state when connected and clearly show OFFLINE/BLOCKED when not connected. Never hard-code a success state.
2. `09_DASHBOARD_PREVIEW/` — a quick visual preview that opens independently and lets reviewers inspect the dashboard layout and work status without starting the runtime. Label sample/mock data clearly; do not present preview data as live evidence.
3. `10_AI_DEBUG_HANDOFF/` — shared handoff area for AI-generated debugging packages. A debugging AI (e.g. Cla CTO) deposits the complete report, patch/diff, reproduction tests, logs, and supporting evidence here. Other AIs review and validate from this area before proposing or applying a patch.

## AI Debug Handoff lifecycle

- `00_INBOX/<AI>/<timestamp-or-run-id>/`: immutable incoming package; preserve original files and folder structure.
- `01_REVIEW/`: independent code/spec review and risk classification.
- `02_PATCH_CANDIDATES/`: reviewed candidate patch only; never silently overwrite canonical source.
- `03_VALIDATION/`: original-vs-patched tests, regression results, logs and hashes.
- `04_DECISIONS/`: decision record, approvals, blocked items and handoff.
- Keep source of truth separate. Depositing a patch is not authorization to apply it.
- Do not overwrite LOCKED contracts. Any proposed behavior change requires an explicit versioned review.
- No AI may claim PASS without executable evidence. Preserve FAIL/BLOCKED honestly.
- No commit/push/merge/release unless separately authorized by the project’s governance rules.
- Never place Core :8000 inside Sandbox.

## Work 10 paths

- Operational dashboard: `COMPUTER-AGENT/08_DASHBOARD/`
- Dashboard preview: `COMPUTER-AGENT/09_DASHBOARD_PREVIEW/`
- AI debugging handoff: `COMPUTER-AGENT/10_AI_DEBUG_HANDOFF/`
- Existing `preview/` at Sandbox root is preserved as the generic Work preview tool; it is not a substitute for the Work-specific dashboard preview.
