# Hướng dẫn thực thi giai đoạn Phát hành / Release Execution Playbook
- **STT / Document ID:** DOC-052
- **Priority:** P1
- **Read order:** 52
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
Deploy the accepted version safely, reproducibly and with a tested recovery path.

## Entry criteria
G7 PASS; explicit release authorization; immutable artifact/version; deployment owner and target environment identified.

## Autonomous procedure
1. Confirm release scope, artifact integrity, compatibility and dependency versions.
2. Review secrets/configuration, access controls, data migrations and change window.
3. Prepare release notes, deployment steps, health checks, backup and rollback plan.
4. Validate target environment and operational readiness.
5. Deploy only through authorized mechanism; capture actor, timestamp, artifact digest and logs.
6. Run smoke/health/security checks and compare with release criteria.
7. If checks fail, stop rollout and execute authorized rollback; preserve incident evidence.
8. Publish release record and update dashboard projection from authoritative state.

## Required outputs
Release approval; versioned package/digest; release notes; deployment log; smoke-test evidence; rollback/backup evidence; post-release status.

## Exit checks
Deployment matches accepted artifact; health checks pass; rollback is available; release owner signs G8.

## Do not
Deploy unaccepted code, expose credentials, claim success without target-environment evidence, or silently continue after failed health checks.
