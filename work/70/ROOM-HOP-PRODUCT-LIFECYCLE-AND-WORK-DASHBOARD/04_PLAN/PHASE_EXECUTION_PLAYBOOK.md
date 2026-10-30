# Hướng dẫn thực thi giai đoạn Kế hoạch / Plan Execution Playbook
- **STT / Document ID:** DOC-048
- **Priority:** P1
- **Read order:** 48
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
Turn the approved design into executable, measurable work packages and a controlled delivery sequence.

## Entry criteria
G3 PASS or authorized planning-only activity.

## Autonomous procedure
1. Decompose outcomes and architecture into WPs small enough to own, review and verify.
2. Assign accountable owner, independent reviewer, priority and deliverable for each WP.
3. Record dependencies, sequencing, critical path, external inputs and resource constraints.
4. Define acceptance criteria, test strategy, evidence requirements and rollback for each WP.
5. Estimate effort/risk only where evidence supports it; label uncertain estimates.
6. Establish milestones, change control, decision deadlines and escalation path.
7. Validate no circular dependencies, orphan WPs, duplicate ownership or untestable outputs.
8. Publish roadmap, WP register and dependency map.

## Required outputs
Roadmap; WP register; dependency graph; milestone plan; responsibility matrix; test/evidence plan; risk and contingency plan; BUILD entry checklist.

## Exit checks
Every deliverable has one owner and reviewer, dependencies are explicit, acceptance/evidence is defined, and scope/capacity are credible. G4 authorizes BUILD.

## Do not
Start BUILD merely because a plan exists; do not mark a WP DONE without verified acceptance evidence.
