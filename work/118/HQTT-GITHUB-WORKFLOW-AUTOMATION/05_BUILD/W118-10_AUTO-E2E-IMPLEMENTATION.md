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
| W118-10-05 | Idempotent handoff event | IMPLEMENTED | Marker keyed by issue and label event ID; runtime pending after deployment |
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
