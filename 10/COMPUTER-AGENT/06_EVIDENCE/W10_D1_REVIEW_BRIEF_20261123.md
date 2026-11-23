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
