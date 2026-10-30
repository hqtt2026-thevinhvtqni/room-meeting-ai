# Hướng dẫn thực thi giai đoạn Nghiệm thu / Accept Execution Playbook
- **STT / Document ID:** DOC-051
- **Priority:** P1
- **Read order:** 51
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
Obtain a formal, accountable decision that the identified product version is acceptable.

## Entry criteria
G6 PASS or an explicitly documented exception submitted to the authorized acceptance authority.

## Autonomous procedure
1. Assemble exact candidate version, scope, requirements, verification report and evidence index.
2. Summarize passed criteria, failed/waived criteria, open defects and residual risks.
3. Confirm evidence links resolve and match the candidate version/hash.
4. Check operational, support, privacy, security and user-readiness obligations.
5. Prepare a concise decision brief: ACCEPT, REJECT or PENDING, with consequences.
6. Route to the named acceptance authority; record decision, actor, timestamp, rationale and conditions.
7. If rejected/pending, convert findings into owned follow-up WPs without erasing history.

## Required outputs
Acceptance package; evidence index; defect/waiver disposition; signed/authorized acceptance record; conditions and follow-up actions.

## Exit checks
Only an authorized human/role can accept. G7 requires ACCEPTED status and all mandatory evidence; Xu cannot substitute its own recommendation for Vinh's reserved authority.

## Do not
Treat silence as approval, accept a different build than the one verified, or bury exceptions in meeting notes.
