# Work 70 Shared Dashboard Preview Host

Status: prototype package — not yet executed or accepted.

See DOC-089 and DOC-090 for architecture, security boundary and acceptance criteria.

- Python 3 standard library only.
- Registry allowlist controls Work routes.
- GET/HEAD only; no directory listing; no write endpoints.
- Default bind: 127.0.0.1.
- Proposed default port: 8060 (the launcher must check availability).
- Private mobile access must be provided by an approved private HTTPS layer such as Tailscale Serve. Do not expose this host publicly.

Run from the repository root after the Sandbox artifacts have been synchronized into their canonical Work directories:
`python work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/05_BUILD/04_CODE/preview_host/server.py --registry work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/05_BUILD/04_CODE/preview_host/preview_registry.json --host 127.0.0.1 --port 8060`

Health check: /healthz (reports Preview Host health only, not Work/Gate status).

Routes:
- /
- /work/70/execution/
- /work/70/product/

The registry paths are repository-relative and must be reconciled with the actual checkout before running. The current Sandbox paths are not automatically mounted into the user's PC repository.
