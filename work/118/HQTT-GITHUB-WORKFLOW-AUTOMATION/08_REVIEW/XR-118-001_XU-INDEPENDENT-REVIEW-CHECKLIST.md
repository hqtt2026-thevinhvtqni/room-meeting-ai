# XR-118-001 — XU INDEPENDENT REVIEW CHECKLIST

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0 — independent security and product-integrity gate
- **Reviewer:** Xu — Independent Reviewer / Architecture Acceptance
- **Build owner:** Ka — Delegated Technical Lead
- **Final product acceptance:** Vinh — Project Owner
- **PR:** https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/67
- **State:** REVIEW REQUESTED — NOT ACCEPTED

## 1. Review authority and limits

Xu reviews the implementation independently and records PASS / BLOCKED / NEEDS CHANGES for each gate. Xu does not need to implement Ka's design. Ka owns remediation. Vinh retains final product acceptance. No review result automatically merges or releases the PR.

## 2. Priority-ordered review gates

| Order | Priority | Review gate | Evidence to inspect | Current state |
|---|---|---|---|---|
| 01 | P0 | Design integrity | TD-118-004 through TD-118-008; Auto E2E architecture and event boundaries | REVIEW |
| 02 | P0 | Actor identity integrity | `.github/w118/role-map.json`; principal-level mapping and deny-by-default behavior | REVIEW |
| 03 | P0 | ACK authorization | Exact syntax, issue binding, active role mapping, no owner-as-executor | REVIEW |
| 04 | P0 | Self-review prevention | Reviewer and PR author resolve to distinct HQTT principals | REVIEW |
| 05 | P0 | Idempotency | Handoff event key, source comment ID, workflow ID + SHA, run attempt marker | REVIEW |
| 06 | P0 | Failure/retry safety | Separate diagnostics workflow, no self-listener, no automatic retry loop | REVIEW |
| 07 | P0 | Controlled fault injection | Owner-only trigger; dedicated test issue; failure scoped to feature branch | REVIEW |
| 08 | P0 | Least privilege | Global contents:read; job-scoped issues/actions write; no secrets or branch-protection change | REVIEW |
| 09 | P0 | Evidence integrity | Exact SHA/run/attempt artifact, RECORDED state, no false acceptance | REVIEW |
| 10 | P0 | Cross-Work boundary | No Work 70 schema/register mutation without Work 70 approval | REVIEW |
| 11 | P0 | Runtime E2E plan | Handoff, ACK deny/allow, duplicate delivery, workflow_run diagnostics after integration | BLOCKED — not deployed |
| 12 | P0 | Release gate | Xu independent disposition followed by Vinh final acceptance; no auto-merge | PENDING |

## 3. Verified CI evidence

- [Run #44748049548](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44748049548): SUCCESS; 36 tests passed; artifact `w118-run-evidence-44748049548-1`, ID `14633817327`.
- The run was a push event. Event-specific jobs were skipped. This evidence does not prove live handoff, ACK, review or diagnostics runtime.
- PR branch is based on main and was 71 commits ahead / 0 behind at the latest comparison.

## 4. Known blockers Xu must not silently waive

1. Xu's GitHub login has not yet been independently confirmed and mapped.
2. No executor identity for Ka/Vi/An is inferred; positive live ACK remains blocked until a real actor identity is verified and mapped.
3. Work 70 Evidence Register integration remains blocked pending Work 70 schema/owner approval.
4. Real GitHub event E2E and workflow_run diagnostics must be executed after the reviewed workflow is integrated into default branch.

## 5. Review result

Xu must record:
- **Design integrity:** PASS / BLOCKED / NEEDS CHANGES
- **Security integrity:** PASS / BLOCKED / NEEDS CHANGES
- **Evidence integrity:** PASS / BLOCKED / NEEDS CHANGES
- **Runtime readiness:** PASS / BLOCKED / NEEDS CHANGES
- **Overall independent disposition:** PASS / BLOCKED / NEEDS CHANGES
- **Findings and required remediation:** numbered list with evidence references
- **Reviewer identity:** verified GitHub login and HQTT principal
- **Date-time:** ISO 8601 with timezone

A Xu design/security PASS permits Vinh to consider a separate non-release integration authorization so runtime E2E can run on the default branch. After integration, Xu must review actual runtime evidence; Vinh then gives final product acceptance. Neither review nor integration alone sets Work 118 to ACCEPTED or RELEASED.


## Additional review checks — event evidence and PR notifier

13. **P0 — ACK state mutation:** verify `w118-acked` is applied only after active actor/role/Issue authorization passes; denied ACK causes no label mutation.
14. **P0 — Event evidence:** handoff, ACK and review artifacts are bound to source event, run/attempt, actor, decision and SHA; state remains RECORDED and no Work 70 register is mutated.
15. **P0 — PR checklist notifier:** `pull_request_target` workflow must not checkout or execute PR head code; it must be same-repository scoped, least-privilege and idempotent per PR head SHA.\n16. **P0 — Independent-review authority separation:** the review workflow must require `can_independently_review`; project-owner `can_accept` authority must not be treated as independent review. Verify same-principal denial and that no unverified Xu login is enabled.\n17. **P0 — Review evidence provenance:** the review artifact must bind the exact trusted policy commit actually checked out, the event SHA, PR head SHA and PR base SHA; do not infer policy provenance from the PR merge ref.


## Runtime execution plan

The post-merge execution sequence is defined in [RT-118-001 — Post-Merge Runtime E2E Runbook](../09_RUNTIME/RT-118-001_POST-MERGE-E2E-RUNBOOK.md). Xu should review the sequence and expected security outcomes before Vinh authorizes main integration. The runbook is PREPARED, not executed; no runtime PASS is implied.


## Staged acceptance boundary

- **Stage A:** Xu reviews design/security and records disposition on PR #67.
- **Stage B:** Vinh may authorize a controlled, non-release main integration solely to execute runtime E2E. The merge does not mean accepted/released.
- **Stage C/D:** Ka executes RT-118-001; Xu independently reviews actual event evidence.
- **Stage E/F:** Vinh records final product acceptance and, separately, release authorization.
