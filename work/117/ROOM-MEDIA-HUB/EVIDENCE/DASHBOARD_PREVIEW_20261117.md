# EVIDENCE — W117 Dashboard Working Preview

- Date: 2026-11-17
- Builder: Go / AI-06
- Scope: W117 Operational Dashboard only (product BUILD not authorized)

## Deliverables

| Path | Description |
|------|-------------|
| `05_BUILD/04_CODE/dashboard/index.html` | App shell |
| `05_BUILD/04_CODE/dashboard/assets/dashboard.css` | Styles |
| `05_BUILD/04_CODE/dashboard/assets/dashboard.js` | Client logic (loads snapshot) |
| `05_BUILD/04_CODE/dashboard/data/snapshot.json` | Canonical data snapshot |
| `05_BUILD/04_CODE/dashboard/run.py` | Local HTTP server + integrity gate |
| `05_BUILD/04_CODE/dashboard/tests/test_snapshot.py` | Self-test (counts + auth boundary) |
| `05_BUILD/04_CODE/dashboard/README.md` | Run instructions |

## How to run
```bash
cd 05_BUILD/04_CODE/dashboard
python tests/test_snapshot.py   # expect PASS
python run.py                   # http://127.0.0.1:8170/
```

## Integrity rules verified by test
- dashboard_tasks count == 9
- product_tasks count == 13
- meta.authorization.dashboard_build == AUTHORIZED
- meta.authorization.product_build == NOT AUTHORIZED
- Go agent present with ACK/IN_PROGRESS status
- Product tasks T009/T010/T011/T013 remain NOT AUTHORIZED

## Known limitations
- Snapshot, not live sync with Sandbox files
- Independent reviews (Cla / Ka / Qw) still DISPATCH UNCONFIRMED
- No accessibility audit yet
- No browser E2E automation yet

## Boundary confirmation
This evidence covers **Dashboard only**. It does not authorize or implement ROOM MEDIA HUB product features, paid services, cloud accounts, real media, or production deployment.
