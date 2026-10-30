# Hướng dẫn thực thi giai đoạn Kiểm chứng / Verify Execution Playbook
- **STT / Document ID:** DOC-050
- **Priority:** P1
- **Read order:** 50
- **Depends on:** DOC-042; DOC-004; DOC-005
- **Status:** ACTIVE / EXECUTION PLAYBOOK
- **Version / Updated:** 1.1 / 2026-10-30


# PHASE EXECUTION PLAYBOOK — WORK 70
Status: ACTIVE — operating standard
Owner: Xu / AI-01 (lifecycle coordinator)
Authority: Vinh retains product decisions, acceptance and release authority.
Rule: Execute the whole phase autonomously where permissions and evidence allow. Never fabricate evidence or promote a gate without authorized evaluation.

## Universal execution protocol
1. READ: inspect current manifest, prior phase outputs, decisions, dependencies and evidence.
2. TRACE: map every input to its canonical source and version; identify owner and authority.
3. ANALYZE: distinguish facts, assumptions, unknowns, risks and conflicts.
4. DECIDE: make reversible in-scope decisions; record material decisions. Escalate only decisions reserved to Vinh or another named authority.
5. BUILD: produce the phase's canonical artifacts in this directory; update registers and cross-references.
6. VERIFY: check completeness, consistency, schema/format, traceability and acceptance criteria.
7. HANDOFF: publish outputs, evidence, blockers, next-phase readiness and audit log.

## Execution rules
- Do not pause for routine step-by-step approval.
- Do not overwrite conflicting canonical records silently; preserve history and log superseding decisions.
- Unknown, missing, stale or contradictory information remains UNKNOWN/BLOCKED; never infer PASS.
- Work completion and phase completion are separate. Phase DONE requires its exit gate.
- Use the smallest sufficient change. Do not expand scope into other Works.
- Every output records owner, version/date, source references and status.
- Stop only for missing authority, destructive/irreversible action, security/privacy risk, external dependency, or decision explicitly reserved to Vinh.


## Objective
Independently establish whether the integrated product meets its requirements and is safe to accept.

## Entry criteria
G5 PASS; candidate version/commit and build evidence are immutable and identifiable.

## Autonomous procedure
1. Build a requirement-to-test/evidence matrix; identify uncovered requirements.
2. Verify environment, version, configuration, test data and reproducible commands.
3. Execute functional, integration, contract, regression, failure, security and performance tests as applicable.
4. Test negative paths, unauthorized actions, stale/unknown data, retries, partial failures and recovery.
5. Inspect logs and artifacts; capture exact outputs, timestamps and environment.
6. Classify defects by severity, impact, reproducibility and owner; retest fixes.
7. Compare actual results against acceptance criteria; record limitations and residual risks.
8. Produce an independent verification report and recommendation.

## Required outputs
Test plan/results; traceability matrix; reproducible evidence; defect register; security/failure findings; coverage gaps; residual-risk statement; verification recommendation.

## Exit checks
All critical requirements have evidence; critical/high defects are dispositioned under policy; tests are reproducible; independent QE signs the result. G6 is evaluated by QE plus owner.

## Do not
Allow the implementer to be sole verifier, infer test success from code review, or hide skipped/unavailable tests.
