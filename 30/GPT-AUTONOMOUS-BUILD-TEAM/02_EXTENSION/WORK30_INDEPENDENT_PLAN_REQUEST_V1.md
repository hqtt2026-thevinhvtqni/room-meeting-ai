# WORK 30 — INDEPENDENT PLAN REQUEST V1
Document ID: W30-PLAN-REQ-001
Status: PLAN REQUEST ISSUED TO CHANNELS / INDIVIDUAL RECEIPT NOT VERIFIED
Owner: Vinh (product decision) | Coordinator: Xu (Planner)
Work ID: 30 — GPT-AUTONOMOUS-BUILD-TEAM
Date: 2026-10-17 (UTC+07:00; exact issuance time not independently sourced)

## 1. Purpose
Develop an evidence-backed, end-to-end autonomous build workflow for ROOM-HOP Work 30. The product must accept an approved task/Plan, inspect relevant Work context and runtime safely, execute the permitted build/test loop through the ROOM-HOP boundary, capture reproducible evidence, handle defects, and produce a truthful handoff. The goal is a working integrated flow, not merely phase descriptions or mock success.

## 2. Current known context — treat as leads to verify, not unquestionable truth
The Sandbox inventory shows a Python implementation under:
- 04_CODE/work30_e2e/ (cli.py, contract.py, engine.py, path_safety.py, policy.py, roomhop.py, router.py, state.py)
- 04_CODE/handoff_validator.py
- 04_CODE/tests/ (contract, engine, CLI E2E, validator, path safety, pilot, policy router, state)
Evidence inventory includes W30_AUTO_001 and W30_AUTO_002 attempt/final-result artifacts, MCP probe, identity gate, unit-test output, and An/Ka/Vi/Xu reports.
Previous reported risks include Sandbox readback returning empty/unusable responses, task/identity dispatch and ACK not proven consistently, and the need to distinguish a successful file write from actual recipient receipt. Validate these claims against current evidence and report what is confirmed versus unknown.

## 3. Product objective
Propose a complete design and implementation path that demonstrates this flow:
1. Read the approved Plan, task contract, acceptance criteria, and relevant Work evidence before changing code.
2. Validate task identity, scope, allowed actions, workspace/path boundaries, and execution policy (fail closed on uncertainty).
3. Discover/check runtime prerequisites and ROOM-HOP Core/MCP/Workspace integration without bypassing Core/MCP boundaries.
4. Execute the approved task through the intended ROOM-HOP path; do not claim real execution if only a mock/stub was used.
5. Capture task ID, actor identity, timestamps, exact commands/actions, exit status, logs, changed files, test results, and artifact references.
6. Detect failures and create actionable defect records with reproduction, expected/actual result, evidence, severity, and owner.
7. Route repairs to Vi with a bounded retry policy; Nu owns full-flow re-execution after repair. Stop after two unsuccessful repair attempts on the same defect and escalate for root-cause/Plan decision.
8. Run independent tests by An, independent adversarial challenge by Cla near completion, then independent review by Ka.
9. Produce a handoff with DONE/PASS/DECISION/BLOCKED statuses, open risks, evidence, and explicit NOT VERIFIED where evidence is missing.
10. Demonstrate one real end-to-end pilot on the supported runtime. Clearly separate unit tests, mocked tests, integration tests, and real E2E evidence.

## 4. Fixed team and decision rules
- Vinh: approves the consolidated Plan before implementation; approves material scope/architecture changes and any risk acceptance.
- Xu: Planner/coordinator; collects independent proposals, reconciles disagreements, creates one consolidated Plan, tracks evidence and handoff. Xu must not fabricate consensus or receipts.
- Planning channel A — Sandbox: Claude (Cla) and Grok (Go) each prepare an independent proposal.
- Planning channel B — GitHub: Qwen (Qe) and Vibe each prepare an independent proposal.
- Nu: autonomous end-to-end coder/executor after Plan approval.
- Vi: repair coder for evidence-backed defects.
- An: independent tester.
- Cla: also performs the late-stage independent challenge gate after An and before Ka. Keep Cla's planning proposal separate from its later challenge role.
- Ka: independent final reviewer; must form its own judgement.
- No implementation before Vinh approves the consolidated Plan. No unsupported PASS. Missing evidence = BLOCKED/NOT VERIFIED.
- All tasks and reports require real identity, task ID, timestamp, provenance, and evidence. A file write is not an ACK.

## 5. Planning assignment — all four proposals must be independent
Each planner must work from this same brief and inspect the available Work files/evidence in its assigned channel. Do not read or coordinate with the other three proposals before submitting your own.
- Claude (Cla) and Grok (Go): Sandbox channel. Submit separately to:
  GPT-AUTONOMOUS-BUILD-TEAM/02_EXTENSION/PLAN_PROPOSALS/CLAUDE_PLAN_PROPOSAL.md
  GPT-AUTONOMOUS-BUILD-TEAM/02_EXTENSION/PLAN_PROPOSALS/GROK_PLAN_PROPOSAL.md
- Qwen (Qe) and Vibe: GitHub channel. Submit separately to:
  docs/work30/plan-proposals/QWEN_PLAN_PROPOSAL.md
  docs/work30/plan-proposals/VIBE_PLAN_PROPOSAL.md
Do not overwrite another planner's proposal. If directory/file creation is unavailable, report the exact blocker and return the complete proposal in the designated channel instead.

## 6. Required proposal format
A. Executive summary and target user outcome.
B. Evidence inventory: path/ref, what it proves, what it does not prove, timestamp/revision, confidence.
C. Current-state trace: existing modules, flow, dependencies, runtime boundaries, verified gaps.
D. Proposed target architecture and data/control flow.
E. End-to-end acceptance criteria written as observable pass/fail conditions.
F. Work breakdown in dependency order, each item with owner (Nu/Vi/An/Cla/Ka/Xu), inputs, outputs, tests, and evidence artifact.
G. Security/safety analysis: identity and permission checks, path/workspace isolation, command policy, secrets, fail-closed cases, auditability.
H. Test strategy: unit, contract, integration, failure-injection, regression, and real E2E; explain which tests are mocked.
I. Defect routing and two-attempt escalation policy.
J. Risks, trade-offs, alternatives, unknowns, and decisions needed from Vinh.
K. Concrete definition of DONE, PASS, BLOCKED, and NOT VERIFIED.
L. First pilot: exact proposed scenario, prerequisites, execution steps, expected outputs, rollback/recovery, and evidence collection.
M. Recommendation with rationale; include dissent or rejected options rather than hiding them.

## 7. Independence and quality rules
- Same brief, independent reasoning; no copying/merging other proposals before submission.
- Cite exact paths, commit IDs, task IDs, logs, test output or runtime artifacts. Never invent evidence.
- Label every claim VERIFIED, INFERRED, or UNKNOWN.
- Distinguish code that exists from code that has run; distinguish mock from real provider/runtime.
- Do not edit product implementation during this planning round.
- Xu synthesizes only after the four proposals are collected or their non-delivery is evidenced. Xu must preserve disagreements and gaps.
- The consolidated Plan is submitted to Vinh for approval. Build phase remains blocked until approval.

## 8. Receipt and completion protocol
Each planner must return an identity-bound ACK with this document ID, their identity, channel, timestamp, and intended output path before/alongside the proposal. A receipt is verified only by a direct system response or verifiable message/task record. An absent ACK or proposal is PENDING/BLOCKED, not presumed delivered.
