# WORK 30 — CROSS-VENDOR MULTI-AI PLAN LOOP V2

- Decision: W30-DEC-004
- Recorded by: Xu — Plan Synthesizer / Điều phối tổng hợp
- Timestamp: 2026-10-17 21:36 UTC+07:00
- Status: DECISION RECORDED; proposal delivery and acknowledgements NOT YET VERIFIED

## 1. Purpose
Work 30's PLAN step gathers independent implementation proposals from AI systems across vendors through two separate evidence sources. Xu does not author the initial plan and does not seed the other AIs with a preferred solution. Xu consolidates the received proposals into one coherent Plan for Vinh's decision.

## 2. Two proposal channels
### Channel A — ROOM-HOP Sandbox
- Claude (Cla): independently analyze the same brief and submit a proposal/evidence in the Work 30 Sandbox.
- Grok (Go): independently analyze the same brief and submit a proposal/evidence in the Work 30 Sandbox.

### Channel B — GitHub
- Qwen (Qe): independently analyze the same brief and submit a proposal/evidence to the designated Work 30 GitHub location.
- Vibe: independently analyze the same brief and submit a proposal/evidence to the designated Work 30 GitHub location.

The GitHub repository identified for this Work is `hqtt2026-thevinhvtqni/room-meeting-ai`. The coordination document is stored at `docs/WORK30_MULTI_AI_PLAN_LOOP_V2.md`. This file defines the protocol; it is not itself proof that Qe or Vibe received the brief or submitted a proposal.

## 3. Common brief and independent proposals
All four AIs receive the same objective, scope, constraints, and output template. Each must produce its proposal independently before reviewing other AI proposals. Each proposal must include:
1. Understanding of the objective and scope.
2. Proposed architecture/approach and rationale.
3. Ordered implementation steps and dependencies.
4. Expected artifacts/deliverables.
5. Risks, assumptions, unknowns, and alternatives.
6. Acceptance criteria and how each criterion will be verified.
7. Evidence location/link and actual execution status.
8. Items requiring Vinh's decision.

## 4. Xu's Plan synthesis responsibilities
Xu must:
- Collect the four proposals from both channels and confirm provenance (AI identity, channel, timestamp, source path/URL).
- Compare overlap, contradictions, unique strengths, costs, dependencies, and risks.
- Build one integrated Plan without hiding disagreements or claiming consensus where none exists.
- Mark each Plan item as evidence-backed, proposed, or unresolved.
- Identify missing proposals explicitly; no silent substitution for an absent AI.
- Present the unified Plan to Vinh for approval. Do not start implementation until approval is recorded.

## 5. Unified Plan output
Required columns:
| ID | Deliverable | Source proposal(s) | Integrated decision | Steps/dependencies | Acceptance criteria | Evidence | Risks/open questions | Vinh decision |
|---|---|---|---|---|---|---|---|---|
| P-01 | Pending four independent proposals | Cla / Go / Qe / Vibe | Not yet decided | Pending | Measurable criteria required | Must link source evidence | Record unknowns | PENDING |

## 6. Execution after Plan approval
Once Vinh approves:
- The designated implementer(s) execute only the approved Plan.
- Test and review roles are assigned explicitly in the approved Plan; do not assume that proposal authors automatically become testers/reviewers.
- Results must be evidence-backed. Failed tests, blockers, and deviations must remain visible.
- Xu tracks Plan status and consolidates evidence, but does not fabricate implementation, test results, or acknowledgements.

## 7. Receipt and evidence rules
- A successful file write/commit proves only that the storage operation succeeded.
- It does not prove an AI received or read the brief.
- Receipt requires a response tied to the expected AI identity and task/brief identifier.
- Proposal completion requires a source artifact and its contents to be inspected.
- If a channel cannot provide verifiable delivery or readback, mark that channel BLOCKED and do not claim the four-AI loop is operational.

## 8. Current state
The protocol is recorded in Sandbox and GitHub. Actual dispatch to Claude, Grok, Qwen, and Vibe, and receipt of four independent proposals, remain PENDING/NOT VERIFIED. Work 30 must not mark PLAN complete until proposal artifacts from both channels are collected and inspected.

[Signed: XU — PLAN SYNTHESIZER]
