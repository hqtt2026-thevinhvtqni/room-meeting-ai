# Hướng dẫn thực thi giai đoạn Thi công / Build Execution Playbook
- **STT / Document ID:** DOC-049
- **Priority:** P1
- **Read order:** 49
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
Implement approved work packages against canonical source locations while preserving traceability and least privilege.

## Entry criteria
G4 PASS; WP state READY; source repository/path, branch, permissions, dependencies and acceptance criteria are declared.

## Autonomous procedure
1. Read the WP, architecture contracts, source manifest and current repository state before editing.
2. Create/continue only the authorized branch and worktree; preserve unrelated changes.
3. Implement the smallest complete change; keep source of truth in the declared repository, not Sandbox.
4. Add/update automated tests, migration notes, configuration examples and documentation as required.
5. Record changed files, commits/PRs, tool/runtime versions, commands and execution outputs.
6. Run focused tests, then relevant regression/static/security checks; distinguish NOT_RUN from PASS.
7. Request independent review; resolve findings and retain review evidence.
8. Update BUILD_MAPPING_REGISTER and WP status only from verified facts.
9. Package artifacts for VERIFY; do not self-approve the phase gate.

## Required outputs
Source/PR/commit references; mapping register; test logs; review findings; known defects; build provenance; evidence links; handoff notes.

## Exit checks
All planned implementation is integrated at the declared source; tests are reproducible; no unresolved critical defect; provenance is complete; G5 is independently evaluated.

## Do not
Claim code exists from a plan, push/merge without permission, store secrets, or treat a green unit test as product acceptance.
