# Hướng dẫn thực thi giai đoạn Khám phá / Discover Execution Playbook
- **STT / Document ID:** DOC-045
- **Priority:** P1
- **Read order:** 45
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
Establish an evidence-backed understanding of the user problem and opportunity before selecting a solution.

## Entry criteria
Work identity and owner exist; G0 is satisfied or its missing items are explicitly listed.

## Autonomous procedure
1. Read intake, prior decisions, support incidents, user requests and relevant operational evidence.
2. Identify user groups, affected workflows, context, frequency, severity and current workaround.
3. Separate observed facts, user statements, third-party evidence, assumptions and unknowns.
4. Map root causes and constraints; do not jump to a preferred implementation.
5. Define opportunity, desired outcomes, non-goals and discovery questions.
6. Record source/provenance for each material claim and confidence/limitations.
7. Produce/update DISCOVER_BRIEF and discovery evidence index.

## Required outputs
Problem statement; user/context map; evidence and source register; assumptions/unknowns; opportunity statement; non-goals; discovery risks; recommendation to proceed, investigate further or stop.

## Exit checks
Problem is specific and evidenced; target users and context are clear; assumptions are visible; opportunity and non-goals are bounded; unresolved questions have owners. G1 evaluation is independent/authorized.

## Do not
Treat a solution idea as proof of a problem, invent customer research, or mark G1 PASS from a completed brief alone.
