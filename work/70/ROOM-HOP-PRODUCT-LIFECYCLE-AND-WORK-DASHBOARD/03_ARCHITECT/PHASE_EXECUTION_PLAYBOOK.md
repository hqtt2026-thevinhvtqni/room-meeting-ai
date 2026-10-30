# Hướng dẫn thực thi giai đoạn Kiến trúc / Architect Execution Playbook
- **STT / Document ID:** DOC-047
- **Priority:** P1
- **Read order:** 47
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
Design a secure, operable and testable system that satisfies the approved requirements.

## Entry criteria
G2 PASS or an explicitly authorized architecture exploration with no BUILD authorization.

## Autonomous procedure
1. Map requirements to components and assign one owner per responsibility.
2. Define system boundaries, trust boundaries, deployment topology and dependencies.
3. Specify data model, source of truth, lifecycle/state transitions and retention.
4. Specify APIs/events: schemas, authentication, authorization, idempotency, versioning, pagination and errors.
5. Design failure modes: timeout, retry, partial write, stale cache, unavailable dependency, recovery and rollback.
6. Threat-model sensitive data, credentials, prompt/tool injection, privilege escalation and audit gaps.
7. Compare alternatives and record architecture decisions with rationale and consequences.
8. Define observability, SLOs where known, operational ownership and test seams.
9. Verify architecture-to-requirement traceability and update canonical diagrams/contracts.

## Required outputs
Architecture overview; component and data-flow diagrams; interface contracts; data/security model; threat/risk register; ADRs; failure/recovery design; deployment/operations outline; architecture verification checklist.

## Exit checks
Every critical requirement maps to a design; interfaces and authority boundaries are explicit; security and failure behavior are designed; unresolved risks have owners; architecture authority approves G3.

## Do not
Present logical services as implemented APIs, assume undocumented Core endpoints, or begin irreversible implementation against unverified contracts.
