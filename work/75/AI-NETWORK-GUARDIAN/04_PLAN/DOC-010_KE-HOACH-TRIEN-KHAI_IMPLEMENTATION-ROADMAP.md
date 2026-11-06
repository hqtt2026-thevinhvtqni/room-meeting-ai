# DOC-010 — Kế hoạch triển khai / Implementation Roadmap

Status: ACTIVE / DESIGN BASELINE. Work is not released.

| WP | Work package | Owner proposal | Reviewer | Status |
|---|---|---|---|---|
| WP75-01 | Work progress dashboard and product baseline | Xu / AI-01 | Qw / AI-05 | ACTIVE |
| WP75-02 | Router and office LAN discovery | Xu + Vinh | Ka / AI-02 | BLOCKED — router/topology inputs missing |
| WP75-03 | Read-only collector and router adapter | Cla / AI-03 | Ka / AI-02 | PLANNED |
| WP75-04 | Deterministic network conflict detection | Vi (capability to verify) | Qw / AI-05 | PLANNED |
| WP75-05 | Evidence-grounded local AI diagnosis | Xu + local AI engineer TBD | Ka / AI-02 | PLANNED |
| WP75-06 | Mobile/PC integration, security, QA and release | Qw + An | Vinh | PLANNED |

## Delivery sequence
1. Confirm product scope, user roles and router/LAN discovery.
2. Finalize architecture and data contracts.
3. Build PC dashboard baseline and shared backend.
4. Implement read-only collector and deterministic detection.
5. Add mobile client and notification workflow.
6. Integrate AI evidence-grounded diagnosis.
7. Run security, functional, mobile/desktop and failure-mode tests.
8. Owner acceptance, release gate and operational handoff.

## Known blockers
- B75-01: router vendor/model/firmware and LAN topology unknown.
- B75-02: canonical Git/Sandbox synchronization and full parity not yet proven.
- B75-03: Sandbox scaffold has legacy top-level folders that differ from Work 70 canonical structure; cleanup not performed.
- B75-04: Dashboard browser E2E and formal schema validation not yet evidenced.

No WP may be marked DONE/PASS without linked evidence and independent verification.
