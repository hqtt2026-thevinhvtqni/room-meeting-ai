# W122 — GÓI QUYẾT ĐỊNH KIẾN TRÚC G2 / ARCHITECTURE DECISION PACK

- Work: 122 — ROOM-HOP EMAIL INTELLIGENCE
- Document class: Architecture decision proposal / decision pack
- Revision: 0.1 — DRAFT FOR OWNER REVIEW
- Prepared by: Xu / AI-01
- Decision authority: Vinh / Product Owner
- Status: NOT APPROVED — no G2 closure, no G3 build authorization
- Basis: W122 Biên bản, Kế hoạch, architecture intake sections 1–19, W05 reuse boundary, W52/W11/W12 evidence trace, Gmail API public documentation research previously recorded in W122 discovery artifacts.

## 1. Purpose and decision rule
This pack converts the current architecture proposal into explicit decisions that Vinh can accept, reject or amend. Recommendations are not decisions. No item becomes APPROVED until the Owner records an explicit decision in the canonical Biên bản/decision record. G2 approval does not itself authorize production mailbox access or external sending; G3 remains a separate gate.

## 2. Proposed baseline decisions

| ID | Decision topic | Xu recommendation for G2 | Alternatives / trade-off | Status |
|---|---|---|---|---|
| ADR-W122-01 | First provider | Gmail API first, provider-neutral adapter boundary; defer other providers | Multi-provider first increases scope and verification burden | PROPOSED |
| ADR-W122-02 | First demo account | One explicitly owner-designated mailbox, owner-controlled OAuth consent; no admin-wide delegation | Multi-mailbox onboarding first increases identity and consent complexity | PROPOSED |
| ADR-W122-03 | Initial permission | Read-only pilot; request the narrowest scope that supports the approved feature. Metadata-only cannot support body summarization/search query; body analysis requires Gmail read-only permission and its restricted-scope obligations | Metadata-only is safer but feature-limited; read-only body access enables intelligence but raises verification/security burden | PROPOSED |
| ADR-W122-04 | Draft and send | R2 is Gmail read-only with no Gmail drafts. Consider W122-local drafts first. Gmail-native draft management requires separate scope review because Gmail compose is restricted and can include send capability; do not request it in R2. Any later send requires a separate Owner decision, explicit approval and narrow policy | Treating Gmail compose as harmless draft-only permission can expand blast radius because it may enable sending | PROPOSED |
| ADR-W122-05 | Identity and tenancy | Every mailbox is a separately authorized resource bound to owner, tenant, provider subject and connection ID. Never infer mailbox identity from email address alone | Single global account identity is simpler but unsafe for shared/multiple mailboxes | PROPOSED |
| ADR-W122-06 | Sync authority | Durable per-mailbox history cursor is authoritative; Pub/Sub/watch is a wake-up signal only; periodic reconciliation is mandatory | Poll-only is simpler but less timely; push-only risks missed notifications | PROPOSED |
| ADR-W122-07 | Data minimization | Store normalized metadata and derived intelligence by default; raw body/attachments retention off unless a specific feature and retention period are approved | Full raw archive improves context/search but increases privacy, breach and deletion burden | PROPOSED |
| ADR-W122-08 | Untrusted content | Treat body, quoted thread, HTML, headers, links, calendar content and attachments as untrusted input; no embedded instruction may grant tools, change policy or authorize send | Trusting known senders is insufficient against compromised accounts and spoofing | PROPOSED |
| ADR-W122-09 | Automation policy | Default DENY for external side effects. Auto-classification and notification may run within authorized read scope; draft generation cannot send. Sensitive/high-impact/ambiguous messages always require human review | Wider auto-send saves time but increases financial, legal, privacy and reputation risk | PROPOSED |
| ADR-W122-10 | Approval binding | Any future send approval must bind mailbox, exact sender identity, exact recipient set, immutable content hash, policy version, approver and expiry; any change invalidates approval | Approval bound only to a thread or draft ID can be replayed or altered | PROPOSED |
| ADR-W122-11 | Send reliability | Future send path requires durable outbox, idempotency key and UNKNOWN/reconciliation state for ambiguous timeout; never blindly retry uncertain sends | Simple retry is easier but can duplicate external messages | PROPOSED |
| ADR-W122-12 | ROOM-HOP integration | Integrate only through versioned, owner-approved Core identity/authority/audit and W52 dispatch contracts plus W14 Host contract. Do not call guessed ports/routes or create parallel identity/event stores | Direct service calls or local shadow registries may appear faster but break authority and audit boundaries | PROPOSED |
| ADR-W122-13 | UI authority | Dashboard/Mail Center is render-only for state; every action is authorized server-side and revalidated at execution time | Client-side role/policy checks are not a security boundary | PROPOSED |
| ADR-W122-14 | Model and AI provider | Keep model adapter replaceable; model output is untrusted suggestion, never authority. No vendor commitment until privacy, data processing, quality and cost are evaluated | Hard-coding one model simplifies early build but creates lock-in and policy coupling | PROPOSED |
| ADR-W122-15 | Cost and external services | No paid cloud, Pub/Sub, vault, model or monitoring commitment until monthly budget and owner approval are recorded | Early managed services may accelerate delivery but create recurring cost and data-processing exposure | PROPOSED |

## 3. Proposed release boundary
- R0 — Architecture and synthetic design: current phase; no provider credentials or mailbox access.
- R1 — Synthetic core: fake provider, fake identities, test fixtures; no real external side effects.
- R2 — Gmail read-only pilot: only after G2/G3 approval, OAuth app/consent and restricted-scope obligations are cleared; one owner-designated test mailbox; no drafts or sends.
- R3 — W122-local draft-only first: store drafts inside W122 under approved retention/access controls; do not create Gmail-native drafts or request Gmail compose scope by default. Any Gmail-native draft capability requires a separate scope/security/Owner decision because compose can include send capability.
- R4 — Controlled send: separate Owner authorization, allow-list and template policy, independent security/QE PASS, immutable approval and reconciliation. Not included in current authorization.
- R5 — Anh Đức handover: only after tenant onboarding, roles, revoke/backup, support and acceptance evidence.

## 4. G2 acceptance conditions
G2 must not close until all of the following are evidenced:
1. Owner has accepted/rejected each proposed decision or explicitly deferred it with an owner and due condition.
2. Data classification, retention, deletion, attachment and residency decisions are explicit.
3. Gmail OAuth scope plan and Google restricted-scope verification implications are understood and accepted.
4. Core identity/tenant/mailbox authorization/audit contract is available and approved.
5. W52 dispatch and event contract is approved and runtime identity verification is defined.
6. W14 Host execution boundary and deployment ownership are evidenced.
7. Threat model, send-state machine, audit model and synthetic acceptance plan have independent Ka/QE findings.
8. Cost ceiling and external-service approval boundary are recorded.
9. Canonical Biên bản is updated only after Owner decisions; no approval is inferred from this proposal.

## 5. Outstanding review inputs
- Kha: Gmail/Google capability, OAuth scope, Pub/Sub/watch, quotas, Workspace/delegation and W05 reuse discovery report. Brief exists; W122 dispatch/receipt and findings NOT VERIFIED.
- Ka: independent threat model, authorization, send approval, webhook/cursor, privacy and negative-test review. Brief exists; W122 dispatch/receipt and findings NOT VERIFIED.
- Go: cost envelope and QE execution capacity; no cost commitment or test execution evidenced.
- Cla: integration feasibility after G2 only; no implementation request yet.
- Nu/Manus: autonomous build assignment only after runtime identity, authorization, audit and G3 scope are verified; no assignment/ACK claimed.
- Vibe/Qc: GitHub-only code work after G3; no assignment.
- Qw: QE role must be verified from official roster/authority, not inferred from display name.

## 6. Open owner decisions (not answered by this pack)
- Is the first release limited to a single personal Gmail mailbox, or should tenant/shared mailbox support be included in R1?
- What is the maximum retention period for normalized metadata, derived summaries, body content and attachments?
- Are attachments excluded from R1 entirely, or may safe document types be indexed later?
- Which notification destination is authorized, and what information may appear in notification previews?
- What is the monthly cost ceiling and who approves paid infrastructure?
- Which exact low-risk categories, if any, may eventually qualify for auto-send? Default remains none.
- What onboarding and support responsibilities are required for anh Đức's handover?

## 7. Explicit non-approvals
This pack does not:
- approve G2 or close discovery;
- authorize code implementation, OAuth registration/consent or mailbox connection;
- authorize real email read, draft, send, archive, label, delete or forwarding operations;
- approve Pub/Sub, a paid service, model provider or data-retention period;
- verify Kha/Ka have received or accepted their W122 briefs;
- certify production Core/Gateway/Event Listener/Agent Runtime/W14 integration.

**Current gate:** G2 NOT APPROVED. G3 BUILD NOT AUTHORIZED. REAL SEND NOT AUTHORIZED.
