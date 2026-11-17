# EVIDENCE — W117 Dashboard audit-fix pass + snapshot refresh (Vibe, 2026-11-17)

- **Work:** 117 — ROOM-MEDIA-HUB (Dashboard scope only)
- **Actor:** Vibe (supporting GitHub Builder, per TASK_BOARD role allocation; self-ACK recorded in Journal)
- **Trigger:** Xu's independent audit (Journal 2026-11-17, ACTION REQUIRED) + Vinh's standing instruction to record debts and keep building.
- **Commit:** single commit to `main` containing all files listed below.

## Files changed
| File | Change |
|---|---|
| `05_BUILD/04_CODE/dashboard/data/snapshot.json` | Refreshed to 2026-11-17T11:42:00+07:00; DASH-001..004 → DONE (implementation); DASH-009 IN_PROGRESS; DASH-010 added; Xu → "COORDINATOR — RUNTIME NOT VERIFIED"; Vibe ACK recorded; timeline extended with 6 new canonical Journal events; sources corrected (BIEN_BAN = informational only) |
| `05_BUILD/04_CODE/dashboard/assets/dashboard.js` | `esc()` HTML-escaping on all data-driven innerHTML insertions; KPI values derived from task arrays instead of hard-coded counts; client-side count check 9 → 10 |
| `05_BUILD/04_CODE/dashboard/assets/dashboard.css` | Added `:focus-visible` keyboard-focus styles |
| `05_BUILD/04_CODE/dashboard/tests/test_snapshot.py` | dashboard_tasks count check 9 → 10 |
| `05_BUILD/04_CODE/dashboard/tests/test_e2e.py` | dashboard_tasks count check 9 → 10 |
| `05_BUILD/04_CODE/dashboard/README.md` | Data-source alignment (parsed vs informational); status/notes updated |
| `00_ROOT/TASK_BOARD.md` | Last-updated line; W117-DASH-010 row; recorded-ACK note |
| `00_ROOT/WORK_MANIFEST.md` | Status line separates authorized Dashboard build from NOT AUTHORIZED product build |
| `00_ROOT/NHAT_KY_THI_CONG.md` | Appended Vibe entry 2026-11-17 11:42 +07 (this pass + debts) |
| `EVIDENCE/DASHBOARD_AUDIT_FIX_20261117_VIBE.md` | This file |

## Verification performed
- Snapshot integrity re-check (equivalent assertions to `tests/test_snapshot.py`): PASS — counts dashboard=10, product=13; dashboard_build=AUTHORIZED; product_build=NOT AUTHORIZED; T009/T010/T011/T013 all "NOT AUTHORIZED"; Go ACK present; Xu runtime-not-verified marker present; timeline ≥ 3.
- HTML/JS contract markers preserved for `tests/test_e2e.py`: view-overview/tasks/agents/timeline, dashboard.js/css references, load-error, provenance, fetch + no-store, statusClass, renderOverview/renderAgents/renderTimeline.

## Debts recorded (Journal, same timestamp)
- DEBT-W117-DASH-A: re-run both Python test suites from canonical path after this commit (previous 43/43 PASS predates relocation and this change).
- DEBT-W117-DASH-B: independent QE (Qw) DISPATCH UNCONFIRMED.
- DEBT-W117-DASH-C: independent technical (Cla) and CSA (Ka) reviews DISPATCH UNCONFIRMED.
- DEBT-W117-DASH-D: real-browser visual/a11y verification outstanding.

## Boundary
Dashboard scope only. Product BUILD remains NOT AUTHORIZED. No secrets, media binaries, cloud resources or deployment involved.
