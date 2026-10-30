# Hướng dẫn thực thi giai đoạn Vận hành / Operate Execution Playbook
- **STT / Document ID:** DOC-053
- **Priority:** P1
- **Read order:** 53
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
Maintain service health, manage incidents and feed operational learning into the next lifecycle cycle.

## Entry criteria
G8 PASS; named operations owner; runbook, monitoring and support path available.

## Autonomous procedure
1. Establish service health, usage, latency/error, availability and cost indicators where instrumented.
2. Verify alerts, dashboards, logs, backup, restore and access review.
3. Track incidents with severity, timeline, impact, root cause, remediation and lessons.
4. Review user feedback, support demand, reliability and security signals.
5. Manage patching, dependency updates, capacity and lifecycle maintenance.
6. Maintain known-error, risk and improvement backlogs with owners.
7. Conduct periodic operational review and recommend continue, improve, rollback or retire.
8. Feed validated insights into DISCOVER/DEFINE; preserve prior lifecycle history.

## Required outputs
Operations runbook; monitoring/alert evidence; service review; incident records; backup/restore checks; maintenance plan; improvement backlog.

## Exit checks
Operational owner and support path remain active; critical alerts and recovery are tested; risks/incidents are owned; G9 review records next-cycle decisions.

## Do not
Claim monitoring exists without live telemetry, close incidents without evidence, or mark a Work CLOSED while obligations remain open.
