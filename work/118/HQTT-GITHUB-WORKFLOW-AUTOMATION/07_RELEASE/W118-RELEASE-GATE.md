# W118 RELEASE GATE — XU REVIEW / VINH ACCEPTANCE

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0 — release governance
- **State:** NOT RELEASED

## 1. Required gates

| Gate | Owner | Required evidence | State |
|---|---|---|---|
| Build complete | Ka | Source, tests, branch and CI | IN PROGRESS |
| Independent technical review | Xu | Review of design, security, diff and runtime evidence | PENDING |
| Final product acceptance | Vinh | Xu review disposition + acceptance matrix + limitations | PENDING |
| Main integration | Ka, after acceptance | Reviewed PR, CI green, explicit no-conflict check | BLOCKED |
| Post-merge E2E | Ka | Real events on main and retrievable artifacts | PENDING |
| Release decision | Vinh | Final acceptance record | PENDING |

## 2. Non-negotiable rules

- Ka may decide and implement the Auto E2E system under the owner's delegation.
- Ka cannot self-accept the product.
- Xu and Vinh are the only acceptance authorities for this Work.
- No self-review, no automatic retry loop, no automatic merge and no automatic release.
- A successful CI run is not a product acceptance.
- Unknown GitHub identities remain unauthorized until explicitly verified and mapped.
- No change to Work 70 schema, repository secrets, branch protection or organization permissions without the responsible owner approval.

## 3. Final state vocabulary

- `BUILDING`: implementation in progress.
- `VERIFYING`: runtime and negative-path tests in progress.
- `READY FOR XU REVIEW`: implementation and evidence bundle complete.
- `XU REVIEWED`: Xu has recorded an independent disposition.
- `ACCEPTED`: Vinh has recorded final acceptance.
- `RELEASED`: only after acceptance and controlled main integration.

The Work must remain `ACTIVE — NOT RELEASED` until the final gate is met.


## Amendment — staged review, integration and final acceptance (2026-11-20)

The runtime diagnostics listener must exist on the default branch to receive real `workflow_run` events. Therefore the prior single-step wording "final acceptance before main integration" is refined into two separate gates. Integration is not release.

| Stage | Owner | Decision / evidence | State |
|---|---|---|---|
| A. Design/security review | Xu | Independent review of PR #67, role policy, permissions, idempotency and event architecture | PENDING |
| B. Non-release integration authorization | Vinh | Explicit authorization to merge for runtime verification only; Work remains ACTIVE — NOT RELEASED | PENDING |
| C. Runtime E2E execution | Ka | Execute RT-118-001 on main; retain artifacts and diagnostic Issues; remediate by follow-up PRs | PENDING |
| D. Runtime evidence review | Xu | Independently verify real handoff/ACK/diagnostics events and all negative-path evidence | PENDING |
| E. Final product acceptance | Vinh | Accept or reject the complete evidence bundle and residual blockers | PENDING |
| F. Release | Vinh | Separate explicit release decision after acceptance | PENDING |

**Non-release integration constraints:** no auto-merge; PR #67 remains manually merged only after stages A and B; merge does not mark Work ACCEPTED or RELEASED; no secrets, branch protection or Work 70 schema changes; runtime failures are remediated through reviewed follow-up PRs; Work status remains ACTIVE — NOT RELEASED until stage E/F.

This staged gate avoids the circular dependency where the workflow_run listener cannot be runtime-tested until it is on the default branch, while preserving Xu's and Vinh's acceptance authority.
