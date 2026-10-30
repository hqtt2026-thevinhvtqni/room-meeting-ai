# AI Project Participants, Roles & Token Usage
Version: 1.1
Date: 2026-10-30
Scope: Work 70 / 05_BUILD
Status: ACTIVE REGISTER — actual participation and token figures must be evidence-backed.

## 1. Purpose

Maintain one auditable register of every human and AI participant involved in this build:
- identity/provider/model used for each work session;
- assigned title, responsibility, and decision authority;
- task assignment and actual contribution;
- token consumption and, where available, monetary cost;
- evidence source and verification status.

This register is not a claim that every listed AI has already participated. The role roster is the approved working roster; session rows record actual participation only.

## 2. Authority and human ownership

| Participant | Title | Authority / responsibility |
|---|---|---|
| Vinh | Product Owner / Final Decision Authority | Sets product direction, approves material scope and release decisions; final authority |
| Xu (GPT) | AI CEO / Project Orchestrator | Owns end-to-end coordination, planning, delegation, integration decisions and handoff within approved scope |
 
Xu may make routine architecture and implementation decisions within scope. Xu must escalate material product/scope, security, cost, or release decisions to Vinh.

## 3. AI role roster

| AI ID | Participant | Assigned title | Primary responsibility | Participation status |
|---|---|---|---|---|
| AI-01 | Xu — GPT | CEO / Project Orchestrator | End-to-end plan, task allocation, architecture coordination, integration, acceptance recommendation and handoff | Assigned |
| AI-02 | Ka — GPT | CSA / Chief Systems Architect | System architecture challenge, interface/contracts, cross-system consistency and design review | Assigned |
| AI-03 | Cla — GPT | CTO / Code-Debug Lead | Technical leadership, implementation diagnosis, root-cause analysis and technical remediation | Assigned |
| AI-04 | Kha — Gemini | Strategy & Product Architect | Product strategy, requirements challenge, user value and prioritization | Assigned |
| AI-05 | Qw — QA model | QE / Independent QA | Independent test design, verification, defect reporting and evidence review; must not approve own implementation | Assigned |
| AI-06 | Qc — Qwen Coder | Implementation Engineer | Assigned code/UI/backend implementation and Git-based delivery within the authorized branch/scope | Assigned |
| AI-07 | Go — Grok | CFO / Cost & Resource Analyst | Token/cost analysis, resource efficiency and cost reporting | Assigned |
| AI-08 | Co — GPT | Coding Assistant / Integration Support | Supporting implementation, code review and integration tasks delegated by Xu | Assigned |
| AI-09 | Vi — GPT | Coder / Implementation Engineer | Implements assigned code changes under the approved plan and branch; records changed paths and commits | Assigned |
| AI-10 | An — GPT | Tester / Test Engineer | Executes assigned tests, records reproducible results and evidence, and reports defects; does not self-approve implementation | Assigned |
| Support | Vibe — Mistral | External Coding Support | Optional GitHub-based coding support when explicitly assigned | Optional |

Provider/model names must be made more specific in each session record (exact model/version when visible). A role label alone is not proof of a model invocation.

## 4. Responsibility boundaries

1. Xu coordinates and integrates; the assigned implementer owns the code changes they submit.
2. Qw independently verifies; Qw must not mark work PASS solely from an implementer's statement.
3. Ka/Cla/Kha challenge architecture, technical quality and product assumptions within their assigned remit.
4. Go reports usage/cost from provider-reported evidence; estimates must be labelled estimates.
5. Vinh retains final product and release authority.
6. No participant may fabricate token counts, model identity, test results, or completion status.
7. Every AI entering the build must identify its AI ID, exact model/provider if known, role, assigned task and session timestamp in the work log.

## 5. Token and cost accounting rules

Record usage per model invocation or per provider-reported task/session. Do not infer token counts from message length.

Required fields:
- timestamp (UTC or explicit timezone);
- AI ID, provider and exact model/version;
- task/session identifier and work item;
- input tokens, output tokens, cached input tokens (if supplied);
- total tokens (provider-reported, or calculated only when component definitions are compatible);
- monetary cost and currency, if provider reports it;
- source/evidence (usage API, provider dashboard/export, or execution trace);
- verification state: VERIFIED, ESTIMATED, NOT_AVAILABLE, or DISPUTED.

Rules:
- Provider-reported values are preferred and must retain their source.
- If a provider does not expose usage, record NOT_AVAILABLE; never enter zero as a substitute.
- Estimates must be separated from verified totals and must state the estimation method.
- Do not add overlapping aggregates (for example, a session total and its per-call details) into one grand total.
- Keep input/output/cached token categories separate; avoid comparing unlike tokenization or billing definitions as if equivalent.
- Report token totals by AI/model, by task/work item, and by date. Report cost separately from tokens.
- Never expose API keys, credentials, private prompts, or sensitive account data in evidence files.

## 6. Actual participation and token ledger

No token figures are pre-filled because no provider usage evidence has been attached to this register. Add one row per invocation or non-overlapping provider-reported session.

| Timestamp | AI ID | Provider / exact model | Task / work item | Input tokens | Output tokens | Cached tokens | Total tokens | Cost | Evidence reference | Status |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| — | — | — | — | — | — | — | — | — | — | NOT_AVAILABLE |

## 7. Session work log

| Timestamp | AI ID / model | Role in session | Assigned task | Deliverable / changed paths | Verification / reviewer | Outcome |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | NOT_RECORDED |

Each contributor must add a session entry when starting and update it at handoff. Link commits, pull requests, test runs and evidence files where available.

## 8. Reporting summary

At each milestone, publish:
- participants actually active (not merely assigned);
- tasks and deliverables per participant;
- verified input/output/cached/total tokens per model;
- verified cost per provider/model and currency;
- estimated usage in a separate subtotal;
- unavailable or disputed usage data;
- evidence links and reporting period.

A milestone cannot claim complete cost accounting while any material usage remains unreported. State the coverage percentage only when the denominator and evidence source are defined.

## 9. Change control

Changes to authority, role ownership or cost-accounting rules require Xu's documented decision and Vinh's approval where product authority, budget or release policy is affected. Update this file rather than creating competing participant rosters.

---
Maintainer: Xu (AI-01)
Final authority: Vinh (Product Owner)
