# RT-118-001 — POST-MERGE RUNTIME E2E RUNBOOK

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0 — release-blocking runtime verification
- **Executor:** Ka — Delegated Technical Lead
- **Independent acceptance:** Xu
- **Final product acceptance:** Vinh
- **State:** PREPARED — NOT EXECUTED

## 1. Preconditions

1. Xu has completed independent design/security review of PR #67 and recorded disposition.
2. Vinh has explicitly authorized a controlled, non-release main integration for runtime verification only. Final product acceptance remains pending until after runtime evidence review.
3. PR #67 is merged by the authorized process; no direct push or force-push to main.
4. Default branch contains the orchestrator, diagnostics listener, PR checklist notifier, role map and event evidence helper.
5. The existing `w118-handoff` label is present. The current Work 118 Issue #65 has this label.
6. No executor identity is added until its GitHub login and HQTT principal are verified.
7. Work 70 Evidence Register integration remains disabled until Work 70 owner/schema approval.

## 2. Test sequence

| Order | Test | Action | Expected evidence | Gate |
|---|---|---|---|---|
| 01 | PR checklist notifier | Create same-repository test PR with `W118` in title/body | One checklist comment with marker PR number + head SHA | PASS/BLOCKED |
| 02 | Handoff event | Create `[W118 E2E TEST] handoff` Issue and apply `w118-handoff` | One handoff comment; `w118-handoff-evidence` artifact | PASS/BLOCKED |
| 03 | Owner cannot execute | Vinh comments `ACKED-ka <issue-number>` | `ACK UNVERIFIED`; no `w118-acked` label; ACK_DENIED artifact | PASS/BLOCKED |
| 04 | Executor ACK positive | Only after a real executor login is verified and mapped, that actor comments `ACKED-<mapped-role> <issue-number>` | `w118-acked` label; ACK_VERIFIED comment; ACK_AUTHORIZED artifact | BLOCKED until identity verified |
| 05 | Controlled diagnostics dispatch | Vinh comments exactly `W118-TEST-DIAGNOSTICS` on the dedicated test Issue with `w118-handoff` label | Owner authorization passes; workflow_dispatch starts only on `work/118-auto-e2e-v2` | PASS/BLOCKED |
| 06 | Controlled failure | Dispatch run executes fault-injection job | Run fails with deliberate exit 17 on isolated branch; no main code change | PASS/BLOCKED |
| 07 | Diagnostics issue creation | Observe `W118 Failure Diagnostics` workflow_run | Exactly one `w118-blocked` issue keyed by workflow ID + SHA; exact run URL/ID/attempt/branch/SHA | PASS/BLOCKED |
| 08 | Diagnostics duplicate delivery | Rerun the failed upstream run/attempt | Same diagnostic issue reused; one update marker per run attempt; no duplicate Issue | PASS/BLOCKED |
| 09 | Review event | Xu submits an approved review after Xu login is verified/mapped and PR author is a different principal | REVIEW_AUTHORIZED artifact/comment; no merge or release | PASS/BLOCKED |
| 10 | Evidence boundary | Inspect all event artifacts and Work 70 register | Artifacts remain RECORDED; no Work 70 write | PASS/BLOCKED |

## 3. Expected security behavior

- Vinh's owner accounts cannot ACK execution roles.
- A reviewer account mapped to the same principal as the PR author is denied.
- Unmapped reviewer/actor is denied.
- Unmapped PR author prevents a claim of reviewer independence.
- Only the dedicated controlled-test permission can dispatch fault injection.
- Fault injection cannot run on main.
- The diagnostics workflow does not listen to itself.
- No automatic retry, auto-merge or auto-release occurs.

## 4. Cleanup without evidence loss

After the runtime tests:
1. Keep all GitHub Actions runs and uploaded artifacts.
2. Add a final comment to the controlled diagnostic Issue stating that it was a planned fault-injection test.
3. Close the test Issue and controlled diagnostic Issue with a reason; do not delete them.
4. Close the temporary test PR after capturing its checklist comment and CI evidence.
5. Append all URLs, run IDs, artifact IDs, SHA values and PASS/BLOCKED outcomes to the Work journal.

## 5. Acceptance exit

Runtime E2E is not complete until tests 01–03 and 05–10 have actual GitHub event evidence. Test 04 remains a separately tracked blocker until a real executor identity is verified. Xu records independent design/security review before integration and independently reviews runtime evidence after tests. Vinh records final product acceptance after runtime review and makes a separate release decision. Main integration alone does not change ACTIVE — NOT RELEASED.
