# W118-10 — AUTO E2E IMPLEMENTATION

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0 — product execution and evidence integrity
- **Implementation branch:** `work/118-auto-e2e-v2`
- **Base:** `main` at `41e8397600505d94434b5830e7aea1a012db77a2`
- **Owner authorization:** Vinh, 2026-11-20 — Ka authorized to decide and build Auto E2E through acceptance; Xu and Vinh retain acceptance authority.
- **State:** BUILD IN PROGRESS — NOT RELEASED

## 1. Target architecture

1. GitHub is canonical for Issues, PRs, commits, workflow runs and review events.
2. GitHub Actions is the event ingress and least-privilege execution layer.
3. W118 role map is the authorization policy input; unknown actors and roles are denied.
4. The Work 118 evidence artifact is an immutable per-run record. It remains RECORDED and does not claim Work 70 register verification.
5. A separate diagnostics workflow observes failed upstream runs. It does not listen to itself, preventing a diagnostics self-loop.
6. No automatic retry, auto-merge or release action is permitted.

## 2. Implementation register

| ID | Component | Result | Evidence / limitation |
|---|---|---|---|
| W118-10-01 | Feature branch from canonical main | DONE | Branch created from main SHA above |
| W118-10-02 | Fail-closed role map | DONE | Two owner logins mapped to acceptance only; no executor identities guessed |
| W118-10-03 | ACK authorization engine | DONE | Exact token, role and issue binding; deny by default |
| W118-10-04 | Independent review authorization | DONE | Self-review and unmapped reviewer denied |
| W118-10-05 | Idempotent handoff event | IMPLEMENTED | Marker keyed by issue number + label ID + issue.updated_at; runtime pending after deployment |
| W118-10-06 | Idempotent ACK result | IMPLEMENTED | Marker keyed by source comment ID; runtime pending after deployment |
| W118-10-07 | CI failure diagnostics | IMPLEMENTED | Separate workflow; key = workflow ID + commit SHA; runtime pending after deployment |
| W118-10-08 | CI evidence artifact | IMPLEMENTED | Run ID, attempt, SHA, event and test outcome; RECORDED only |
| W118-10-09 | Automated contract tests | RUNNING | GitHub Actions on feature branch |
| W118-10-10 | Real GitHub event E2E | PENDING | Requires Xu review and controlled deployment to main |
| W118-10-11 | Failure-path E2E | PENDING | Controlled failure injection on feature branch, then diagnostics listener verification |
| W118-10-12 | Work 70 Evidence Register write | BLOCKED | Requires Work 70 owner approval of compatible schema; W118 will not mutate Work 70 |
| W118-10-13 | Xu acceptance identity mapping | BLOCKED | Xu's GitHub login must be confirmed by Xu; no identity is inferred |

## 3. Security boundaries

- Global workflow permission is `contents: read`; issue mutation permission is job-scoped.
- Owner accounts have acceptance permission only; they cannot ACK execution roles.
- No executor login is enabled until the identity and role are verified.
- ACK syntax must match exactly `ACKED-<role> <issue-number>`.
- Handoff, ACK and diagnostics mutations have stable idempotency markers.
- Diagnostics issues do not assign an actor automatically.
- CI artifacts are evidence, not acceptance.
- No token, secret, branch protection or organization permission is changed by this implementation.

## 4. Acceptance exit conditions

- All contract/unit tests pass.
- Handoff event, authorized/unauthorized ACK, duplicate event and review gates are tested against real GitHub events.
- Controlled upstream failure creates exactly one diagnostic issue per workflow/commit and updates it idempotently.
- Evidence artifact is retrievable and bound to exact run/SHA.
- Work 70 register integration is either approved and tested by Work 70 or explicitly excluded from this release.
- Xu completes independent review; Vinh gives final acceptance.
- No auto-merge. Merge/release occurs only after the human acceptance gates are satisfied.


## Verification update — 2026-11-20

Latest completed full contract run before this documentation update: [Run 44746386416](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44746386416), commit `326f4d1fc312d991b601075990a96dd7969fde11`, job `validate` SUCCESS, `26 tests / OK`. Artifact `w118-run-evidence-44746386416-1` (ID `14632693408`) was present and unexpired. Event jobs were skipped on the push event; runtime E2E is still pending.


## Controlled failure test harness

A controlled test dispatcher is now implemented in the orchestrator workflow. It requires an exact `W118-TEST-DIAGNOSTICS` comment on a dedicated issue titled `[W118 E2E TEST]...`, the existing `w118-handoff` label, and an active principal with `can_trigger_controlled_test=true`. Only the two owner-confirmed accounts currently satisfy this permission. The dispatcher starts `workflow_dispatch` on the isolated W118 feature branch with `failure_injection=controlled`; the failure job is hard-scoped to that branch. After the diagnostics listener is integrated into default branch, the resulting failed run can exercise the real `workflow_run` listener without deliberately breaking main or production workflows.

This dispatcher is implemented and contract-tested; the actual dispatch and diagnostics issue creation remain PENDING until controlled deployment is accepted.


## Review independence hardening — 2026-11-20

A final code review found that login-only self-review detection would allow two GitHub accounts mapped to the same HQTT principal to review each other. The implementation now resolves both reviewer and PR author through the role map and denies review when they map to the same principal. An unmapped PR author also fails closed because independence cannot be proven. Tests cover same-principal cross-account denial, unknown-author denial and a mapped different-principal positive case.


## Principal-level review verification — 2026-11-20

- **Fix:** same-principal cross-account review is denied; unmapped PR author denies an independence claim; distinct mapped principal with active acceptance permission is allowed.
- **CI:** [Run #44747589539](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44747589539) SUCCESS; 32 tests passed; artifact ID `14634211524` exists and was unexpired at readback.
- **Scope:** unit/contract proof only. Runtime pull_request_review event evidence and Xu identity mapping remain pending.


## Event-level automation update — 2026-11-20

- Authorized ACK applies the `w118-acked` label after authorization succeeds; denied/unmapped actors do not change issue state.
- Handoff, ACK and review event jobs write separate OPERATION evidence artifacts using `event_evidence.py`, all state RECORDED.
- PR review checklist is posted by a dedicated `pull_request_target` workflow. It does not checkout or execute PR code, only accepts same-repository PRs, and has job-scoped `issues:write` with `contents:read`.
- The initial pull_request-context comment attempt failed with `Resource not accessible by integration`; it was removed and replaced with the base-context notifier. This is recorded as a permission-boundary correction, not hidden.


## Event automation verification — 2026-11-20

- CI [Run #44748965030](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44748965030) SUCCESS; 44 tests passed; artifact ID `14634556693`.
- Handoff/ACK/review event evidence artifacts are implemented. ACK state label `w118-acked` is applied only on authorized actor/role/issue binding.
- PR checklist notifier moved to `pull_request_target` after actual PR-context token write was denied. It uses no checkout and runs no PR code, restricted to same-repository PRs.
- PR #67 remains Draft; event jobs were skipped on the push validation run and are not yet runtime verified.


## Provenance and diagnostics subscription update — 2026-11-20

- CI run artifact distinguishes PR source SHA from the exact tested SHA and records repository, actor, branch/ref, workflow ref, run URL, PR number and base SHA.
- Failure diagnostics now subscribes to the separate `W118 PR Review Checklist` workflow as well as W118, W300 and Work 70. It remains non-self-listening.
\n\n## P0 review-policy provenance hardening — 2026-11-20\n\nA source audit found that the `pull_request_review` job used an unqualified `actions/checkout`. On that event, the default ref can resolve to the PR merge ref, allowing PR-controlled role-map or authorization code to influence the acceptance decision. The review job now explicitly checks out `${{ github.event.repository.default_branch }}` and sets `persist-credentials: false`. A regression contract test asserts both controls. The change is committed on `work/118-auto-e2e-v2`; Run [#44755364888](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755364888) completed SUCCESS with 46 tests PASS, including the new regression. Artifact ID `14636718273`. Event-specific jobs were skipped on this PR synchronize run. This is a P0 contract-level remediation, not a runtime E2E PASS.\n\n\n## P0 ACK Work-scope guard — 2026-11-20\n\nA source audit found that the ACK workflow accepted any repository Issue carrying an `ACKED-` comment, provided the actor/role mapping passed. It did not require the Issue to be a Work 118 handoff. The ACK job now also requires the source Issue to carry `w118-handoff` and not be a pull request. Regression test T10-20 asserts this event boundary. This prevents a future mapped executor from accidentally or deliberately applying W118 ACK state to unrelated repository Issues. Code and test are committed; CI verification is pending.\n\n\n## P0 independent-review authority separation — 2026-11-20\n\nThe review policy previously reused `can_accept` for the independent reviewer event. That conflated Vinh's final project-owner acceptance authority with Xu's independent review authority. The policy now has a separate required boolean `can_independently_review`; the review authorizer checks only that permission. Vinh's two owner logins retain `can_accept: true` and explicitly have `can_independently_review: false`. Xu's login remains unmapped until Xu independently confirms it. The review helper was renamed to `authorize_independent_review`, and tests cover a positive mapped independent-review fixture, owner denial, same-principal cross-account denial and unmapped PR-author denial. Run [#44755930029](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755930029) validates 47 tests PASS; event-specific jobs were skipped, so runtime review remains pending.\n\n\n## Role-map schema 1.1 and strict permission validation — 2026-11-20\n\nThe new `can_independently_review` permission is now a required field under role-map schema `1.1`. The loader fails closed when the field is missing or not boolean. Run [#44756198541](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44756198541) completed SUCCESS with 48 tests PASS, including the missing-field rejection case. Artifact ID `14638126091`. Event-specific jobs remained skipped; runtime review remains pending.\n