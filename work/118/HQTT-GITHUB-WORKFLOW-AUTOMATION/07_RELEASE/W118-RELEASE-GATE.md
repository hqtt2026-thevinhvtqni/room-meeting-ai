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
