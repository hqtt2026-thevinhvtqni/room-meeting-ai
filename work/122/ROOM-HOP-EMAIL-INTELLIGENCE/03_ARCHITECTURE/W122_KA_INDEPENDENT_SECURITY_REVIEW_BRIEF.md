# W122 — YÊU CẦU REVIEW ĐỘC LẬP CHO KA / SECURITY & AUTHORITY
- Work: 122 — ROOM-HOP EMAIL INTELLIGENCE
- Assignee: Ka / AI-02
- Role: Independent architecture/security reviewer.
- Status: REVIEW REQUEST — findings pending.
- Scope: Review current W122 Biên bản, Kế hoạch, architecture intake and W22/W52 reference contracts. Read-only; do not implement or modify canonical W122 records.

## Review focus
1. Threat model for inbound email as untrusted content, including prompt injection in body, quoted thread, signatures, HTML, links, calendar content and attachments.
2. OAuth/token security: least privilege, vault reference model, refresh/revocation, tenant/mailbox isolation, redaction and audit.
3. Authorization boundaries: owner, mailbox identity, agent identity, per-mailbox policy, approval authority and send-time revalidation.
4. High-risk categories that must always require human approval; evaluate whether the current list is complete.
5. Cross-mailbox leakage, spoofing/compromised senders, malicious attachment/link handling, recipient confusion and hallucinated commitments.
6. Send safety: draft hash, recipient-set binding, approval expiry/staleness, idempotency/outbox, timeout ambiguity and provider receipt semantics.
7. Webhook/polling security: signature/authentication, replay, duplicate, out-of-order events, subscription renewal and cursor reconciliation.
8. Audit integrity, retention, privacy/data minimization, deletion and incident response.
9. Dashboard must not be an authority; UI approval must call an authorized backend command.
10. W52 reuse boundary: current W52 candidate is no-tool/read-only and cannot be assumed to provide email execution or approval. Identify safe reusable principles only.

## Required output
- Findings ranked CRITICAL/HIGH/MEDIUM/LOW with evidence references.
- Missing controls and concrete mitigations.
- Explicit FACT / INFERENCE / UNKNOWN.
- Review of default-DENY policy and proposed policy state machine.
- Security acceptance criteria and negative tests.
- Any disagreement with W122 proposal, with rationale.
- Do not mark PASS for untested controls; no implementation or real email operations.


## Review package — 2026-11-27
Primary artifact for this review:
- `03_ARCHITECTURE/W122_THREAT_MODEL_AND_SECURITY_CONTROLS_DRAFT.md`
- Document code SEC-W122-001, version 0.1-DRAFT.
- Scope: 20 STRIDE-oriented threat entries (TM-01–TM-20), eight trust boundaries, policy invariants, proposed controls, residual risks, release security gates and negative-test mapping to W122-T001–T024.
- Status: draft only; not independently reviewed; no security tests executed.

Specific issue requiring explicit challenge:
- R2 must remain Gmail read-only, with no Gmail drafts and no send.
- W122-local draft records are distinct from Gmail-native Drafts.
- Gmail-native draft management requires separate scope review; Gmail compose is restricted and can include send capability. A hidden UI Send button is not a security boundary.
- Assess whether local drafts are the correct R3 default and specify the additional conditions if Gmail-native drafts are ever proposed.

Please return a review artifact with:
1. Exact document/version reviewed and SHA-256 if available.
2. TM-01–TM-20 disposition (accept / revise / reject) and rationale.
3. Missing threats, severity changes and residual-risk acceptance requirements.
4. Specific review of cross-tenant isolation, prompt-injection containment, OAuth scopes, attachment/SSRF safety, approval binding, send ambiguity, audit and retention.
5. Required test additions or corrections mapped to W122-T001–T024.
6. Verdict: PASS / PASS WITH CONDITIONS / FAIL / BLOCKED, with evidence and limitations.

Dispatch/receipt remains NOT VERIFIED. This brief is prepared for handoff only; it does not assert that Ka has received or accepted the assignment.
