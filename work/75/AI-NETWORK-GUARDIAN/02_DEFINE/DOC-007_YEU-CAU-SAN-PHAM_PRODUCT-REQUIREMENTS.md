# DOC-007 — Yêu cầu sản phẩm / Product Requirements

## Vision
A secure, local-first network infrastructure management product for office LANs, accessible from Mobile and PC, with AI-assisted operations.

## User roles
- Network administrator: full authorized management and review.
- Operator: monitoring, triage and approved operational actions.
- Viewer: read-only visibility.
- AI assistant: scoped analysis and recommendations; never an implicit human identity.

## Platform requirements
### PC Dashboard
- Network overview: router health, LAN status, devices, IP/MAC inventory and incidents.
- Topology view and device relationship visualization.
- Incident queue, severity, evidence, timeline and acknowledgement.
- AI explanation panel with source observations, confidence and recommended checks.
- User/role management, audit trail and system health.
- Configuration views; writes disabled in initial release.

### Mobile App
- Sign-in and role-aware access.
- Network health summary and device status.
- Push/in-app incident alerts.
- Incident details, evidence and timeline.
- AI-assisted explanation and recommended next steps.
- Secure acknowledgement and notes, subject to role permissions.

## Shared capabilities
- One backend API and canonical data model for both clients.
- Device inventory, router adapter, event ingestion and incident lifecycle.
- Data provenance, timestamps, freshness, confidence and audit history.
- Local-first deployment and secure authentication/authorization.
- AI retrieval grounded only in observed network data and approved documentation.

## Initial scope
- Start with one office router and the connected LAN.
- Passive discovery and read-only collection.
- Detect duplicate/conflicting IP observations, unknown devices and connectivity anomalies where evidence supports it.
- AI summarizes evidence and proposes checks.
- Human approval required for any network-impacting operation.

## Non-goals for initial release
- Automatic router configuration or firmware changes.
- Automatic blocking/quarantine of devices.
- Cloud dependency as a requirement for core monitoring.
- AI-generated unsupported certainty.

## Acceptance gates
- Mobile and PC use the same backend and identity/authorization model.
- Read-only router access demonstrated with evidence.
- Detection rules tested against known positive and negative cases.
- AI output cites observed evidence and can abstain.
- Audit records and security controls verified.
- No production/release claim before QA and owner acceptance.
