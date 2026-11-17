# HỒ SƠ PHẢN BIỆN ĐỘC LẬP — WORK 502 MÊ
- Document ID: W502-ARCH-CONSULT-001
- Date: 2026-11-18
- Target: W502-ARCH-001 Architecture Proposal v0.1
- Status: PREPARED — DISPATCH/ACK NOT VERIFIED; NO REVIEW CLAIMED

## Context and fixed decisions
AutoGPT Platform is the selected candidate engine; self-host preferred; Work 502 is separate; ROOM-HOP Core retains identity/authorization; Work 501 owns model/provider routing; six functional roles plus one Manager; single-model and multi-model configurations supported; zero-cost first; no silent paid fallback; no BUILD authorization.

## Common challenge questions
1. Is AutoGPT Platform the correct project/component, or is AutoGPT Classic being confused with Platform?
2. Which capabilities overlap Work 14, 15, 16, 30, 50, 501 and ROOM-HOP Core? What must be reused rather than rebuilt?
3. Can AutoGPT be safely subordinated to ROOM-HOP Core without duplicate identity, permissions, session or task authority?
4. What is the minimum adapter/API/MCP boundary? What data is canonical in ROOM-HOP versus AutoGPT runtime?
5. Can one model serve all six roles? When does multi-model materially improve outcomes and what is the cost/privacy impact?
6. What are the actual hardware, Docker, database, queue, memory and operational requirements for self-host?
7. What is the exact Platform license at the candidate release and what use/distribution restrictions apply?
8. What prompt-injection, SSRF, shell, filesystem, secret, network egress and supply-chain threats remain?
9. How should concurrency, file locks, bounded retries, cancellation, crash recovery and idempotency work?
10. What objective evidence is required before a task, product, QA result or deployment may be marked DONE/PASS?
11. Which parts should be rejected or deferred to avoid building a second platform inside ROOM-HOP?

## Reviewer assignments
- Cla / AI-03: technical architecture, AutoGPT internals, adapter, queue, state, concurrency and failure recovery. No code.
- Ka / AI-02: security, authorization boundary, secrets, egress, sandbox, prompt injection and license risk. No code.
- Qw / AI-05: QA independence, acceptance criteria, test matrix, evidence integrity and retry limits. No code.
- Vibe: adversarial challenge; try to falsify the proposal and identify simpler alternatives. No implementation.
- Go / AI-06: local infrastructure, hardware/resource and zero-cost feasibility. No installation/download/account/billing.
- Qc: source/API/MCP/block feasibility and implementation boundary. No code.
- Kha: provider/model and Work 501/23 overlap, model selection and free-tier terms. No keys/live paid calls.
- Work 14/15/16/30/50 owners: report existing capabilities and source contracts that MÊ can reuse.

## Required response format
Verdict ACCEPT / ACCEPT WITH CONDITIONS / REVISE / REJECT; numbered findings with severity and source evidence; overlap/reuse; cost/privacy/security impact; proposed corrections; unresolved questions; BUILD blockers; objective exit criteria; reviewer identity/model/version/timestamp/source context. Unverified identity/source means UNVERIFIED and cannot count as independent review.

## Dispatch register
| Reviewer | Scope | Dispatch | ACK | Review |
|---|---|---|---|---|
| Cla / AI-03 | Technical | NOT SENT | NOT VERIFIED | PENDING |
| Ka / AI-02 | Security | NOT SENT | NOT VERIFIED | PENDING |
| Qw / AI-05 | QE | NOT SENT | NOT VERIFIED | PENDING |
| Vibe | Adversarial | NOT SENT | NOT VERIFIED | PENDING |
| Go / AI-06 | Feasibility/cost | NOT SENT | NOT VERIFIED | PENDING |
| Qc | Adapter feasibility | NOT SENT | NOT VERIFIED | PENDING |
| Kha | Model/provider | NOT SENT | NOT VERIFIED | PENDING |
| Work owners | Reuse/source contracts | NOT SENT | NOT VERIFIED | PENDING |

## Reconciliation
Xu records only actual reviewer responses in canonical minutes, task board and journal. Conflicts remain OPEN until resolved by evidence or Vinh decision. No reviewer is treated as having accepted this design merely because a brief was prepared. No BUILD before reconciled design and explicit Vinh approval.