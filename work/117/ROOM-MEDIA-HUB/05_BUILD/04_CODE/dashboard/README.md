# W117 Operational Dashboard

**Status:** WORKING PREVIEW + E2E PASS (Go / AI-06); audit-fix pass + snapshot refresh (Vibe, 2026-11-17)  
**Authorization:** Dashboard BUILD only (Vinh, 2026-11-17). **Product BUILD is NOT authorized.**

## What this is
A dedicated, **read-only** operational Dashboard for Work 117 only.

| View | Content |
|------|---------|
| Work Overview | Status cards + strict scope boundary |
| Task Board | Dashboard tasks (10) + Product tasks (13, reference) |
| Agent Monitor | Role, status, evidence provenance — no invented online state |
| Activity & Evidence | Timeline derived from canonical Journal |

## Source of truth
Parsed data inputs:
- `00_ROOT/TASK_BOARD.md`
- `00_ROOT/NHAT_KY_THI_CONG.md`

Informational provenance only (not parsed into the snapshot):
- `00_ROOT/BIEN_BAN.md`

Data is loaded from `data/snapshot.json` (generated from the canonical files above). All KPI card values are derived from the task arrays in the snapshot, not hand-written. All data-driven strings are HTML-escaped before rendering.

**Rules enforced**
- No fabricated progress metrics
- No invented Agent online/session status
- Unverified states displayed as `DISPATCH/ACK NOT VERIFIED`
- Clear provenance on every view

## Run (real local server)

```bash
cd 05_BUILD/04_CODE/dashboard

# 1) Integrity self-test
python tests/test_snapshot.py

# 2) Full automated E2E suite (recommended)
python tests/test_e2e.py

# 3) Start server (default port 8170)
python run.py

# Optional custom port
python run.py --port 9000
```

Then open: **http://127.0.0.1:8170/**

`run.py` validates the snapshot before serving. Press Ctrl+C to stop.

## Automated E2E
- Suite: `tests/test_e2e.py`
- Last full run: **43/43 PASS** (2026-11-17, builder self-test, pre-relocation path)
- Note: suite counts were updated to 10 dashboard tasks after W117-DASH-010 was added; a fresh run from the canonical path is recorded as a pending debt until executed in a Python environment.
- Evidence: `EVIDENCE/DASHBOARD_E2E_TEST_20261117.md`, `EVIDENCE/DASHBOARD_AUDIT_FIX_20261117_VIBE.md`
- Coverage: snapshot integrity, static assets, HTML markers, JS contract, HTTP server (/, snapshot, assets, 404, auth boundary)

## Project layout
```
dashboard/
├── index.html              # Shell
├── run.py                  # Local HTTP server + integrity gate
├── README.md
├── data/
│   └── snapshot.json       # Canonical data snapshot
├── assets/
│   ├── dashboard.css
│   └── dashboard.js        # Loads snapshot via fetch
└── tests/
    ├── test_snapshot.py    # Count + authorization boundary tests
    └── test_e2e.py         # Full automated E2E suite
```

## Out of scope (hard boundary)
- ROOM MEDIA HUB product implementation (T009–T011)
- Paid services, cloud accounts, real media upload
- Production deployment / release

## Owner
Go / AI-06 — Primary Builder & integration lead

