# KẾ HOẠCH W122 — ROOM-HOP EMAIL INTELLIGENCE
Status: PROPOSED — DISCOVER FIRST; BUILD NOT AUTHORIZED
Owner: Vinh | Coordinator: Xu | Standard: Work 70 | Date: 2026-11-25

## Outcome
Secure provider-neutral ROOM-HOP Mail Center for multiple mailboxes: monitor, classify, summarize, identify action-required messages, draft replies, and send only under explicitly approved per-mailbox policies.

## Work packages
| WP | Scope | Owner / contributors | Exit evidence |
|---|---|---|---|
| 122-01 | Intake, scope, source inventory | Xu; Ka review | Manifest, requirements baseline |
| 122-02 | Gmail/Google discovery | Kha (initial only), Xu | OAuth scopes, Gmail API/Watch lifecycle, quotas |
| 122-03 | Outlook/M365 and IMAP discovery | Xu/Cla | Provider capability comparison |
| 122-04 | ROOM-HOP integration trace | Xu/Cla; Ka review | Verified Core/Gateway/Event/Runtime contracts |
| 122-05 | Security, threat model, privacy, retention | Ka; Go review | Threat model, data flow, permission matrix |
| 122-06 | Provider-neutral architecture & ADR | Xu; Ka/Cla/Go | One approved minutes + ADR |
| 122-07 | Implementation plan and cost model | Xu/Cla/Go | Build breakdown, estimates, cost controls |
| 122-08 | Connectors, sync, intelligence | Cla/Manus/Vibe/Co/Vi as assigned | Source diff, tests, journal |
| 122-09 | Mail Center dashboard/notifications | Assigned after architecture | Live data contract, UI tests |
| 122-10 | Send control/policy enforcement | Assigned after security gate | Deny/allow, approval, idempotency, audit tests |
| 122-11 | Independent verification | Go unless conflict; independent reviewer | QE report, evidence read-back |
| 122-12 | Release/operations handoff | Xu + delivery team | Runbook, rollback, monitoring, revoke |

## Gates
G0 Intake: scope, owner, dependencies, W120/W121 non-interference.
G1 Discover: provider APIs, ROOM-HOP contracts, security/data requirements.
G2 Architecture: contracts, threat model, policy state machine, ADR reviewed/approved.
G3 Build authorization: explicit gate; no implementation before it.
G4 Verification: synthetic/test tenant; real outbound send separately authorized.
G5 Acceptance: independent QE, Owner acceptance, evidence complete.
G6 Release/Operate: staged read-only → draft-only → bounded auto-send.

## Controls
Read-only discovery first. No OAuth consent, app registration, credential change, paid service or external send without required approval. Least privilege, encrypted token storage, redaction, audit, revocation. Defend prompt injection and malicious attachments. Outbound sends require send-time policy check, recipient validation, idempotency and provider receipt. High-risk categories always require human approval. One canonical minutes, plan and journal.

## Initial staffing
Xu coordinator/architect; Ka security reviewer; Cla CTO integration/debug; Kha initial Gmail discovery only; Go CFO + default QE/QA + scoped coding support with conflict separation; Vibe GitHub-only/no numeric ID; Manus AI-18 autonomous builder after runtime identity/permission verification; Qw HQTT reviewer; Qc/Vi/Co by official roster.

## Immediate next actions
1. Verify Work 122 registration and W120/W121 unchanged.
2. Inspect W70 intake requirements and W52 communication contracts.
3. Prepare provider brief for Kha and security brief for Ka.
4. Trace actual ROOM-HOP source/runtime contracts; do not assume candidate ports are implemented.
5. Reconcile reviewer findings into one official minutes revision before architecture/build.
