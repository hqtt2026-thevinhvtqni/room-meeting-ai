# W05 REAL GOOGLE PHASE — VINH GATE REQUEST

STATUS: NEEDS_VINH / BLOCKED_BY_INFRASTRUCTURE
OWNER / AGENT: Manus Orchestrator
TIMESTAMP: 2026-10-05T06:21:30+07:00
INPUT: Existing W05_REAL_WORK_001 mock checkpoint, prior decisions, Real Google Phase v1.0.
ACTION: Enumerate unresolved authority decisions without guessing approval or requesting secrets in chat.
RESULT: The following gates remain unresolved. Recommended options are technical recommendations only, not approvals.

## G1 — Workspace ownership
- Decision ID: G1 / D4
- Question: Should durable production documents live in a dedicated Shared Drive, and who owns/administers it?
- Recommended option: dedicated Shared Drive with explicit Core-held drive ID and organization/group membership.
- Alternatives: My Drive for user-owned drafts; another approved team corpus.
- Evidence: Google documents team ownership and Shared Drive membership/access semantics; prior synthesis recommends Shared Drive for durable artifacts.
- Technical consequence: adapter must use Shared Drive parameters and targeted corpus searches.
- Security consequence: membership/inherited access becomes the primary boundary.
- Operational consequence: requires Workspace admin/Manager provisioning, retention, and offboarding policy.
- If undecided: no production target may be selected; real mutations remain blocked.
- Exact decision required from Vinh: approve/reject Shared Drive, identify authoritative owner/admin, and approve membership/access model.

## G2 — Credentials
- Decision ID: G2 / D3
- Question: OAuth, Service Account, or Hybrid?
- Recommended option: Hybrid under Core policy: least-privilege OAuth for user-owned/user-attributed flows; narrowly allowlisted service account only for approved unattended shared resources.
- Alternatives: OAuth-only; service-account-only.
- Evidence: Google documents OAuth for user consent and service accounts for app-owned/shared resources or explicitly delegated access.
- Technical consequence: Core owns credential selection and adapter egress; Runner/MCP hold no tokens or keys.
- Security consequence: refresh tokens/private keys require secure storage, rotation, redaction, and default deny.
- Operational consequence: OAuth consent/offboarding and service-account lifecycle must be managed.
- If undecided: no credentials may be configured or used.
- Exact decision required from Vinh: approve model, resource/tenant policy, secret-storage standard, and operational owner.

## G3 — OAuth scopes
- Decision ID: G3
- Question: What is the minimum approved scope set?
- Recommended option: start with the narrowest per-file scope compatible with the approved flow; expand only with documented need.
- Alternatives: broader Drive metadata/content scopes if the approved use case proves necessary.
- Evidence: Google recommends least privilege; broad/restricted scopes can trigger verification/security obligations.
- Technical consequence: capability set may be limited; adapter must surface scope failures safely.
- Security consequence: narrower blast radius and lower data exposure.
- Operational consequence: scope review/consent/verification may be required.
- If undecided: readiness cannot pass and no API call should occur.
- Exact decision required from Vinh: approve exact scopes and the justification for each.

## G4 — Domain-wide delegation
- Decision ID: G4 / D3
- Question: Is domain-wide delegation required?
- Recommended option: NO by default; use only if a concrete approved workflow cannot use user OAuth or direct resource sharing.
- Alternatives: approved DWD with enumerated scopes and delegated subjects.
- Evidence: Google requires Workspace administrator authorization for DWD; it is not inferred from Cloud IAM.
- Technical consequence: without DWD, unattended cross-user access is unavailable.
- Security consequence: DWD increases blast radius and requires strict allowlists/audit.
- Operational consequence: Workspace admin must authorize, review, and revoke it.
- If undecided: do not enable it; real cross-user execution is blocked.
- Exact decision required from Vinh: approve/reject DWD, subjects, scopes, admin owner, and review cadence.

## G5 — Human-edit intake
- Decision ID: G5 / D1/D7/D8
- Question: How do human Docs edits become known to Core?
- Recommended option: Drive Changes/watch as notification/reconciliation trigger; Core retrieves authoritative state, classifies drift/conflict, and accepts or rejects through policy.
- Alternatives: periodic polling only; explicit structured intake workflow.
- Evidence: notifications do not contain full change details; changes.list/reconciliation is required; auto-bidirectional merge is not assumed.
- Technical consequence: Core owns cursor, reconciliation, and conflict classification.
- Security consequence: human edits are untrusted external input until validated.
- Operational consequence: freshness, missed notifications, and reconciliation ownership need an SLA.
- If undecided: human-edit behavior remains reject/drift-detect only; no automatic import.
- Exact decision required from Vinh: approve intake mechanism and whether any human edits may update Core.

## G6 — Full update
- Decision ID: G6 / D5
- Question: Is full-document replacement allowed?
- Recommended option: NO by default; controlled sections and append-only event areas only.
- Alternatives: explicitly gated full update for first generation, migration, rebuild, or recovery.
- Evidence: prior synthesis identifies full replacement as destructive and recommends revision checks, snapshot/diff, idempotency, and explicit authorization.
- Technical consequence: adapter implements bounded section operations, not arbitrary overwrite.
- Security consequence: reduces accidental loss of human/unmanaged content.
- Operational consequence: rebuilds require change control and rollback evidence.
- If undecided: full update remains disabled.
- Exact decision required from Vinh: approve/reject full update and enumerate allowed reasons/rollback controls.

## G7 — Conflict policy
- Decision ID: G7 / D8
- Question: What happens on stale or semantically conflicting writes?
- Recommended option: reject stale destructive write → re-read → bounded re-plan; auto-merge only for an explicit low-risk allow-list.
- Alternatives: strict reject only; approved targetRevisionId merge for selected operations.
- Evidence: Docs requiredRevisionId provides fail-closed behavior; targetRevisionId delegates merge semantics to Google; prior synthesis rejects generic untested merge.
- Technical consequence: Core stores observed revision, operation fingerprint, retry count, and conflict status.
- Security consequence: prevents silent data loss and semantic corruption.
- Operational consequence: conflicts may require human review and bounded retry handling.
- If undecided: reject stale destructive writes and do not auto-merge.
- Exact decision required from Vinh: approve policy and auto-merge allow-list.

## G8 — Webhook / freshness SLA
- Decision ID: G8 / D7
- Question: What reconciliation freshness is required?
- Recommended option: safe periodic reconciliation until an SLA and secure HTTPS webhook ownership are approved.
- Alternatives: watch + changes.list with approved renewal/monitoring; polling-only.
- Evidence: watch is a hint, channels expire, and changes.list retrieves authoritative state.
- Technical consequence: cursor-draining and reconciliation jobs are required.
- Security consequence: webhook endpoint/authentication/replay controls must be approved.
- Operational consequence: worker, renewal, monitoring, and incident response are required.
- If undecided: no webhook; use only local/mock or future bounded polling design.
- Exact decision required from Vinh: approve freshness target, webhook ownership/security, and reconciliation interval.

## G9 — Migration
- Decision ID: G9 / D4/D2
- Question: Must existing Google documents be migrated?
- Recommended option: NO migration in this phase unless an explicit corpus and owner-approved plan exists.
- Alternatives: controlled inventory, dry run, ACL comparison, staged migration.
- Evidence: prior run has no selected corpus or migration authority; migration can alter effective access.
- Technical consequence: adapter targets only an explicit test resource when readiness passes.
- Security consequence: prevents unintended access/ownership changes.
- Operational consequence: avoids unbounded data movement and rollback complexity.
- If undecided: no migration and no unknown-document mutation.
- Exact decision required from Vinh: approve/reject migration scope, owner, ACL review, and rollback.

## G10 — Backup / retention
- Decision ID: G10 / D2/D5
- Question: What backup frequency, retention, and restore expectation apply?
- Recommended option: Core audit plus versioned export/recovery artifact, with frequency/retention set by owner before production.
- Alternatives: provider-native retention only; scheduled exports with defined retention.
- Evidence: Core must remain authoritative for audit; JSON/export sidecars are not a second authority.
- Technical consequence: backup/restore tooling and restore verification are needed.
- Security consequence: backups need access controls, encryption, and secret/data classification.
- Operational consequence: storage cost, retention jobs, and restore drills are required.
- If undecided: no production retention claim; mock evidence only.
- Exact decision required from Vinh: approve RPO/RTO, frequency, retention, restore owner, and deletion/hold policy.

## G11 — Production deployment
- Decision ID: G11 / D1–D8
- Question: Is this phase local proof, development deployment, or production deployment?
- Recommended option: local proof until credentials, runtimes, scopes, target, and gates are approved.
- Alternatives: development deployment in isolated test project/corpus; production deployment after release gate.
- Evidence: readiness checks show no auth and ports :8000/:8020 unavailable.
- Technical consequence: current phase can only produce readiness and adapter-level plans; no live integration.
- Security consequence: avoids unapproved external egress and mutation.
- Operational consequence: live deployment requires service ownership, monitoring, rollback, and incident response.
- If undecided: status remains BLOCKED_BY_INFRASTRUCTURE/PARTIAL.
- Exact decision required from Vinh: approve phase environment and accountable operator.

## GATE SUMMARY
G1–G11: NEEDS_VINH or BLOCKED_BY_INFRASTRUCTURE. No approval is inferred. No secret is requested or exposed. Independent work continues only where safe: readiness documentation, adapter contract planning, and mock evidence preservation.

EVIDENCE: prior 08_DECISION.md, 09_BUILD.md, 10_TEST.md, 11_QE.md, 12_FIX.md, 14_FINAL.md; official Google documentation listed in 04_RESEARCH.md.
NEXT: Complete REAL_GOOGLE_READINESS.md and await explicit authority/infra before real execution.
