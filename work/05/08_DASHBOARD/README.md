# Operational Dashboard — Work 05

## Purpose
Reserved for an operational dashboard backed by actual runtime/API state.

## Evidence and status rules
- Display live status only when the underlying runtime/API result and observation time are available.
- Never hard-code PASS, infer health from file presence, or treat preview/mock data as live state.
- If no operational dashboard is implemented, show NOT IMPLEMENTED / BLOCKED with the exact missing dependency.
- Keep implementation and evidence in existing project-specific locations; this README does not claim a dashboard implementation.

## Boundary
The separate demo zone is `09_DASHBOARD_PREVIEW/`; preview data must be visibly marked `PREVIEW_ONLY`.
