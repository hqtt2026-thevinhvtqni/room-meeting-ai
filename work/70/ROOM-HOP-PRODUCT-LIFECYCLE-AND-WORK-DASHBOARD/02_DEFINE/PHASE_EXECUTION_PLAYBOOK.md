# Hướng dẫn thực thi giai đoạn Định nghĩa / Define Execution Playbook
- **STT / Document ID:** DOC-046
- **Priority:** P1
- **Read order:** 46
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
Convert validated discovery into a testable product contract.

## Entry criteria
G1 is PASS, or the authorized owner explicitly permits a limited definition draft while G1 remains unresolved (no phase advancement).

## Autonomous procedure
1. Reconcile discovery findings, user needs, constraints and decisions.
2. Define product vision, measurable outcomes and success metrics with baseline/target/time window where known.
3. Define scope IN/OUT, personas, primary journeys and supported use cases.
4. Write functional and non-functional requirements with unique IDs and priority.
5. Define acceptance criteria that are observable and testable; map each requirement to evidence/test.
6. Record assumptions, dependencies, privacy/security/accessibility/performance constraints.
7. Resolve internal contradictions; create decision requests only for reserved authority.
8. Publish PRODUCT_REQUIREMENTS and update traceability matrix.

## Required outputs
Approved product brief; requirement catalogue; scope boundary; success metrics; acceptance criteria; constraints/dependencies; risk and decision register; requirement-to-test traceability.

## Exit checks
Every in-scope requirement is unambiguous and testable; non-goals are explicit; metrics have definitions; acceptance is measurable; no unresolved critical contradiction. G2 requires product-owner authorization.

## Do not
Invent numeric targets, silently convert assumptions into requirements, or let implementation convenience redefine user outcomes.
