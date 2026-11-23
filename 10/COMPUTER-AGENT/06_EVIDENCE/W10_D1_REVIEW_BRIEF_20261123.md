# W10 D1 — Desktop Adapter Contract & Threat Model Review Brief
- Brief ID: W10-D1-REVIEW-BRIEF-20261123
- Status: READY FOR TECHNICAL CONSULTATION — NOT APPROVED FOR IMPLEMENTATION
- Owner: Vinh
- Coordinator: Xu
- Date: 2026-11-23

## Objective
Review the draft Desktop Adapter Capability Contract and Threat Model before implementation. Keep the Browser Adapter and three LOCKED contracts unchanged.

## Proposed baseline
- W10 remains the only governed Computer Agent boundary.
- Browser Adapter = Playwright/Chromium; proposed Desktop Adapter = native OS accessibility APIs.
- agent-desktop is a candidate backend only.
- W10 Runtime + policy + ProcessSupervisor contain all operations.
- W24/W112/W14/W113 ownership boundaries remain intact.
- v0.1 allow-list: capabilities, scoped observe, resolve, click, type, select, toggle, focus (under review), bounded wait, close W10-owned session.
- Deny by default: shell, clipboard, arbitrary shortcuts/coordinates, app/process/system administration, credentials, file transfer and external/irreversible actions.
- Every state-changing operation requires a fresh observation and post-condition verification; no silent coordinate fallback.

## Review questions
1. Is the trust boundary and ownership split complete and non-duplicative?
2. Are the operation allow-list and deny-list safe and technically implementable?
3. Are observation-bound refs, TTL and one-action/one-fresh-observation rules sufficient?
4. Should focus be removed from v0.1, and must the pilot use a dedicated Windows user session?
5. Are privacy, redaction, retention and evidence requirements implementable?
6. Are T01–T15 threats and minimum acceptance criteria complete?
7. What concrete tests or failure modes are missing?
8. Should W10 invoke candidate via a narrow CLI/library wrapper or internal MCP stdio, and why?
9. What are the blockers and measurable entry/exit criteria for a Windows pilot?

## Required response format
- Verdict: APPROVE / APPROVE WITH CHANGES / REJECT / BLOCKED
- Findings: issue → evidence/reason → severity
- Required changes: exact clause/section
- Missing tests: test → expected safe outcome
- Residual risks
- Entry conditions for D2
- No code, installation, runtime action or permission changes during this review.

## Participants requested
Ka (architecture/security review), Cla (technical implementation feasibility), Qw (quality/negative-test review), Nu (independent end-to-end risk review). Xu consolidates feedback into one canonical Biên bản and one Nhật ký. No agent is authorized to install or implement.

## Xu pre-review findings to reviewers — revision request (2026-11-23)

Please review the original D1 package together with the proposed addenda in the capability contract and threat model. This remains a design-only consultation.

### Required reviewer decisions
1. Ka — architecture/security: Validate authorization binding/replay/revocation, destructive semantic classification, trust boundaries, privacy/retention, threat coverage and whether W24/W112 canonical contracts can carry the required grant context without duplication.
2. Cla — implementation feasibility: Validate Windows accessibility provider support, immutable backend pin/provenance, ProcessSupervisor process-tree/session-handle containment, cancellation/cleanup, and precise operation/result semantics. Identify impossible or underspecified requirements.
3. Qw — QE/negative testing: Produce a traceability matrix from each threat/control to test ID, fixture, expected result, evidence artifact and pass/fail/block rule. Include all mandatory negative cases listed in the threat-model addendum.
4. Nu — independent end-to-end risk review: Challenge human-session safety, prompt injection, semantic misclassification, privacy leaks, uncertain side effects, recovery and operational failure modes across the full lifecycle.

### Review response format
For each finding: ACCEPT / REVISE / REJECT / BLOCKED; severity; exact document section; rationale/evidence; proposed replacement wording; test implication; unresolved dependency. Explicitly state what was actually inspected or tested. Do not claim runtime/security validation from document inspection.

### Consultation state
No reviewer has been dispatched or has responded through a verified channel as of this revision. This brief is prepared for forwarding only. It does not constitute ACK, approval, implementation authorization or D1 PASS.
