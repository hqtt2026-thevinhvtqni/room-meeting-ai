# DOC-008 — Kiến trúc hệ thống / System Architecture

## Logical architecture
1. **Mobile Client:** monitoring, notifications, incident review and AI assistant.
2. **PC Web Client:** full operations dashboard and administration.
3. **Shared Backend/API:** authentication, authorization, inventory, incidents, telemetry, audit and configuration policy.
4. **Network Collector:** local service that passively collects router/LAN observations through supported read-only interfaces.
5. **Detection Engine:** deterministic rules for duplicate IP, conflicting leases, unknown devices and connectivity anomalies.
6. **AI Assistant:** evidence-grounded diagnosis, natural-language explanation and recommended checks.
7. **Storage:** local database for inventory, telemetry summaries, incidents, decisions and audit events.

## Data flow
Router/LAN → read-only collector → normalized observations → storage/event pipeline → deterministic detection → incident/evidence → AI explanation → PC/Mobile clients.

## Trust boundaries
- Collector credentials are least-privilege and read-only.
- Clients never connect directly to router management interfaces.
- Backend enforces user and device authorization.
- AI receives only scoped, sanitized evidence and cannot invoke network mutation tools.
- All sensitive access and approved actions are audited.

## Deployment
- Initial deployment inside the office LAN on a local PC/server.
- PC access through a secured local web interface.
- Mobile access over trusted LAN/VPN; do not expose router or backend administration ports directly to the public internet.
- Remote access, TLS/certificate strategy, backup and recovery require explicit design before production.

## Open architecture decisions
- Router vendor/model/firmware and supported read-only API/protocol.
- LAN topology, subnet/VLAN and DHCP authority.
- Local server/PC operating environment and availability requirements.
- Mobile delivery choice (PWA vs native app) after UX and notification requirements are validated.
- Database and AI runtime selection after hardware/data constraints are known.

## Safety
Initial release is passive/read-only. Any future write capability requires a separate threat model, approval workflow, rollback plan and explicit owner authorization.
