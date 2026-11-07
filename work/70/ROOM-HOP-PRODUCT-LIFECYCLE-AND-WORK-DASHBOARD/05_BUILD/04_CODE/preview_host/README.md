# Work 70 Shared Dashboard Preview Host

Status: prototype package — not yet executed or accepted.

See DOC-089 and DOC-090 for architecture, security boundary and acceptance criteria.

- Python 3 standard library only.
- Registry allowlist controls Work routes.
- GET/HEAD only; no directory listing; no write endpoints.
- Default bind: 127.0.0.1.
- Proposed default port: 8060 (the launcher must check availability).
- Private mobile access must be provided by an approved private HTTPS layer such as Tailscale Serve. Do not expose this host publicly.

Run the safe bootstrap from the repository root. It requires the `main` branch and a clean working tree; `-SyncMain` performs a fast-forward-only update, then Python compile and unit tests. `-Start` starts the local host after tests pass:
`& .\\work\\70\\ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD\\05_BUILD\\04_CODE\\preview_host\\bootstrap_preview_host.ps1 -SyncMain -Start -Port 8060`

Manual server command (after the artifacts are synchronized into their canonical Work directories):
`python work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/05_BUILD/04_CODE/preview_host/server.py --registry work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/05_BUILD/04_CODE/preview_host/preview_registry.json --host 127.0.0.1 --port 8060`

Health check: /healthz (reports Preview Host health only, not Work/Gate status).

Routes:
- /
- /work/70/execution/
- /work/70/product/

The runtime PID/log files are stored under `%LOCALAPPDATA%\\ROOM-HOP\\PreviewHost`, outside the Git working tree. The registry paths are repository-relative. Sandbox files are not automatically mounted into the PC repository; the bootstrap syncs from GitHub main.
