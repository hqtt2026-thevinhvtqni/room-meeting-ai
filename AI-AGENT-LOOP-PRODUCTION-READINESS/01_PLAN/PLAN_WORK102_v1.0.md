# Work 102 Plan — Agent Loop Production Readiness

**Version:** 1.0  
**Status:** ACTIVE — NOT PASS — NOT RELEASED  
**Authority:** Vinh, Project Owner  
**Coordinator:** Xu  
**Build owner:** Co  
**Independent reviewer:** Ka  
**Operational journal:** ../06_EVIDENCE/WORK_102_ENGINEERING_JOURNAL_20261015.md

## 1. Goal

Make the bounded Agent Loop safe and verifiable at production integration boundaries, reusing canonical ROOM Core and Execution Host contracts rather than inventing a second orchestration system.

## 2. Decisions and guardrails

1. Evidence First. No PASS without source-bound and runtime-appropriate evidence.
2. Workflow: READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.
3. Vinh approved a repair budget of at most **2 repair rounds** and **3 test runs per related defect cycle** (baseline, after repair 1, after repair 2). At the limit without acceptance, mark BLOCKED and name the exact missing prerequisite.
4. No separate Tester/An assignment for Work 102. Co runs available checks; Ka reviews independently; Xu coordinates and adjudicates.
5. Stop immediately for authorization/security boundary violations, cross-work data loss, checkpoint corruption, or unauthorized side effects.
6. No Core-in-Sandbox, Core 2, parallel dispatcher/queue, or replacement Execution Host.
7. The engineering journal is the only operational source of truth for AI actions in the session. All actual outcomes, ACKs, evidence, blockers, and next actions belong there.

## 3. Workstreams

### A — Stabilize local Agent Loop recovery and budget behavior
- Compare current source hashes to the V2 patch manifest, file by file.
- Review the full diff against the current contract; V2 supersedes V1.
- Preserve final-step retryable failure behavior: BUDGET_EXHAUSTED, with no extra executor call after the step limit.
- Address only evidenced defects: rejected resume must not overwrite the target checkpoint; cost test fixture must explicitly specify estimated_cost=1.0 without weakening runtime accounting; checkpoint-store failures must use a stable safe reason.
- If hashes drift, do not blindly apply the patch; reconcile only the necessary hunks and record why.
- Run collection and full suite against the exact candidate only when an authorized execution environment is available. Capture command, versions, source hashes, raw stdout/stderr, JUnit, exit code, and source-bound evidence bundle.
- If execution is unavailable, record ENV_BLOCKED / PENDING EVIDENCE and continue static review.

### B — Independent review
- Ka reviews exact source hashes, complete V2 diff, regression coverage, checkpoint preservation, retry/cost semantics, error classification, and evidence binding.
- Record severity, evidence, open findings, and re-review result in the operational journal.

### C — Gate A canonical integration mapping
- Identify the authoritative Core task/event/dispatch owner and exact schema/API.
- Verify task IDs, authenticated receiver identity, inbox delivery, correlated ACK/result, persistence, idempotency, lease/fencing, dependency wake-up, recovery, and deployed runtime identity.
- Map Work 30 dispatch acceptance and Work 52 A2A contracts to the existing canonical owner.
- Inspect Work 14 Execution Host timeout/cancel/evidence boundaries.
- Classify findings as SOURCE-VERIFIED, RUNTIME-VERIFIED, HISTORICAL-ONLY, or NOT-FOUND/NOT-VERIFIED. Do not treat NOT-VERIFIED as repository-wide MISSING.
- No local test result alone can close Gate A.

## 4. Acceptance criteria

Work 102 cannot be marked PASS or released until all applicable criteria are supported by evidence:

- [ ] Current source and test hashes are recorded and candidate-bound.
- [ ] Resume rejection and checkpoint preservation regressions pass on the exact adopted candidate.
- [ ] Cost charging and retry/step-budget semantics pass without weakened limits.
- [ ] Checkpoint-store failures return controlled FAILED results with stable safe reason codes.
- [ ] Full suite results include raw output, JUnit, versions, exit code, and exact source hashes.
- [ ] Ka's independent review is recorded and all blocking findings are resolved or explicitly accepted by the authorized owner.
- [ ] Canonical Core task authority and dispatch/ACK/result correlation are verified.
- [ ] Persistence, idempotency, leases/fencing, recovery, and Execution Host integration are verified at the correct boundary.
- [ ] Required runtime/E2E checks are performed; no fake adapter or demo is represented as production evidence.
- [ ] Final handoff lists exact evidence, residual risks, and release decision.

## 5. Status at creation

Patch V2 is a proposed candidate; Co adoption, current source hash match, and Ka review are not yet verified. The reported 62/62 result is isolated candidate evidence only, not canonical Core/Host/PC/provider E2E. Gate A remains PARTIAL / BLOCKED. Work 102 remains ACTIVE / NOT PASS / NOT RELEASED.

## 6. Execution protocol

Do not declare work dispatched or received until the authoritative system returns direct evidence. Do not silently exceed the repair/test budget. Do not merge, release, or change canonical main source as part of this plan.
