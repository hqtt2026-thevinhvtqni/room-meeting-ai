# W118 RELEASE GATE — XU REVIEW / VINH ACCEPTANCE

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Priority:** P0 — release governance
- **State:** NOT RELEASED

## 1. Required gates

| Gate | Owner | Required evidence | State |
|---|---|---|---|
| Build complete | Ka | Source, branch, CI and 52/52 unit-contract tests | PASS — contract build; runtime E2E remains pending |
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


## Current gate evidence — 2026-11-20

- PR #67 is OPEN, mergeable, not merged; branch synchronized with Main (0 behind).
- Latest CI [#44758608904](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44758608904) SUCCESS, 52 unit/contract tests PASS; artifact `14638958067`.
- T10-19 through T10-25 regression gates PASS.
- Xu independent review remains PENDING; Vinh Stage B non-release integration authorization remains PENDING.
- Runtime handoff, positive/negative ACK, review, controlled fault injection and workflow_run diagnostics have not been executed; all were SKIPPED on PR synchronize.
- Therefore the product is **not READY FOR FINAL ACCEPTANCE**, **not ACCEPTED**, and **not RELEASED**.


## Current active-candidate overlay — 2026-11-24 05:43 +07:00 (Entry 070)

- Current active review candidate is **PR #68**: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/68.
- Exact branch/PR HEAD at readback: `e5d7c989bf8fa73637283f2d75f8003861669ee7`; PR #68 OPEN / UNMERGED against `main`.
- PR #67 in the earlier Stage A/B and historical snapshots is superseded/historical; do not treat it as the current integration candidate. Preserve the staged gates: Xu design/security review, explicit Vinh non-release integration authorization, runtime execution/review, Vinh final acceptance, separate release authorization.
- Xu review PENDING; Vinh integration authorization NOT GRANTED; final acceptance NOT ACCEPTED; release NOT AUTHORIZED.


## Authoritative current release-gate overlay — Entry 073 (2026-11-24 06:11 +07:00)

> This P0 overlay supersedes the historical PR #67 references and older snapshots above for current routing/status. It does not change the staged authority requirements.

- **Active candidate:** [PR #68](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/68), branch `work/118-auto-e2e-v2-clean`, base `main`, exact HEAD `3345175799a984f9586b483896431069c0f1b043`, OPEN / not draft / UNMERGED.
- **Exact-head CI:** [Run #1069 / ID `45285944558`](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/45285944558), validate SUCCESS, **102 contract/unit tests in 0.296s**; artifact ID `14872425816`, SHA-256 `3bc79b82305ebe3f343693c4a2e5c2ae42023da9d86c2ca1452ec77139ca2a7b`, unexpired at metadata readback. Source-binding and handoff/ACK/review-observation capture jobs SKIPPED. This is not runtime E2E.
- **Stage A — Xu design/security review:** PENDING; review packet in [XR-118-001](../08_REVIEW/XR-118-001_XU-INDEPENDENT-REVIEW-CHECKLIST.md). Xu GitHub login/principal mapping is not verified.
- **Stage B — Vinh non-release integration authorization:** NOT GRANTED. No merge before explicit owner decision.
- **Stage C — Ka runtime E2E:** NOT RUN; dependent on approved Core/W102/W14/W33/W70 contracts and Vinh Stage B authorization.
- **Stage D — Xu runtime evidence review:** PENDING / cannot occur before real runtime evidence exists.
- **Stage E — Vinh final product acceptance:** NOT ACCEPTED.
- **Stage F — separate Vinh release authorization:** NOT AUTHORIZED / NOT RELEASED.

### Mandatory external gates (not waivable by W118)

Core Task/Event read/dispatch/persistence and authenticated Task-scoped Issue-mirror lease; W102 verified principal, Assignment and recipient-bound ACK; W14 canonical protected execution path and Work Authority/HostPort; W33 authenticated evidence ingress; W70 approved Evidence Register schema/owner ACK and read-only projection must be proven by their owning Work. No W118-local replacement authority or duplicate Host/queue/dispatcher is permitted.

### Review findings routed to Xu

Entries 065, 067, 068, 069 and 071 remain open static review findings. Implementation/workflow freeze remains until Xu records disposition. No remediation is inferred or silently accepted. Full details and requested review outputs are in XR-118-001 and journal Entries 065–073.

### Governance / BIÊN BẢN

- PR #68 remains OPEN / UNMERGED; no rebase, force-push, PR close, Main integration, release, external Work/Sandbox mutation or security/permission/secret change.
- **Name:** Ka / AI-02. **Title:** CSA / W118 Delegated Build Owner. **Date-Time:** 2026-11-24 06:11 +07:00.
- **Result:** Release gate reconciled to current PR #68 and exact-head CI. ACTIVE — BLOCKED — NOT ACCEPTED — NOT RELEASED.
### Final revision-binding addendum — handover packet consolidation

- HEAD `3345175799a984f9586b483896431069c0f1b043` / Run #1069 above are pre-consolidation evidence only.
- The final packet is consolidated in the documentation-only commit immediately following parent `1a27bcb67f7544bc8dc7296264126d9b6559eb14`. Xu's review must bind to the live PR #68 head SHA and matching exact-head CI as read at review start. No earlier CI result is transferable to a later SHA.
- Staged gates remain unchanged: Xu review → separate Vinh non-release integration authorization → runtime E2E → Xu runtime evidence review → Vinh final acceptance → separate Vinh release authorization.
