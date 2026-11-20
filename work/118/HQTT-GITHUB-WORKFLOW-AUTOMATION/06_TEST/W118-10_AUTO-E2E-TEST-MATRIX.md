# W118-10 — AUTO E2E TEST MATRIX

- **Work:** W118
- **Priority:** P0
- **Test owner:** Ka builds the harness; Xu independently reviews; Vinh gives final acceptance.
- **State:** PARTIAL — contract tests run on feature branch; real event tests pending deployment.

| ID | Scenario | Expected result | Current state |
|---|---|---|---|
| T10-01 | Parse orchestrator and diagnostics workflow YAML | Both parse and required event contracts exist | PASS — initial CI |
| T10-02 | Explicitly mapped executor ACKs its own role | Authorized only when active login and role match | PASS — unit fixture |
| T10-03 | Owner login attempts execution ACK | Denied; owner is acceptance-only | PASS — unit test |
| T10-04 | Unknown login attempts ACK | Denied; no state transition | PASS — unit test |
| T10-05 | ACK references another Issue | Denied | PASS — parser/contract test; CLI event test pending |
| T10-06 | Duplicate ACK event | One result comment per source comment ID | IMPLEMENTED; runtime pending |
| T10-07 | Duplicate handoff label event | One handoff comment per issue/label event ID | IMPLEMENTED; runtime pending |
| T10-08 | PR author approves own PR | Rejected as independent acceptance | PASS — unit test |
| T10-09 | Unmapped reviewer approves PR | Not counted as W118 acceptance | PASS — unit test |
| T10-10 | Same workflow and SHA fail more than once | Reuse one open diagnostic issue | PASS — unit test; runtime pending |
| T10-11 | Different workflow or SHA fails | Distinct idempotency key | PASS — unit test |
| T10-12 | Same run is retried | Attempt-specific update marker; no automatic retry | PASS — unit test |
| T10-13 | Controlled W118 validation failure | Diagnostics workflow observes failure and creates/updates issue | PENDING — diagnostics workflow must be on default branch |
| T10-14 | W300 or W70 natural failure after listener deployment | W118 diagnostics captures exact run URL and SHA | PENDING — wait for eligible real event |
| T10-15 | Evidence artifact retrieval | Artifact contains run ID, attempt, SHA, event and outcome | PASS — artifact exists for run 44745874397 |
| T10-16 | Work 70 Evidence Register write | Only after Work 70 schema approval | BLOCKED — no schema mutation authorized |
| T10-17 | Xu acceptance reviewer identity | Xu mapped to verified GitHub login and accepted review recorded | BLOCKED — identity not yet confirmed |

## 1. Evidence rules

A test is PASS only when its expected result is supported by a test output, GitHub event, job result, artifact or API readback. A skipped job is not a pass. Historical failures predating the listener do not prove diagnostics runtime. A controlled failure is labeled as fault-injection evidence and is not represented as a natural production incident.

## 2. Final test bundle

The final acceptance bundle must contain:
- Branch and PR URL, commit SHAs and diff.
- CI run URLs and job-level conclusions.
- Unit/contract test output.
- Handoff and ACK source events plus bot responses.
- Unauthorized denial evidence.
- Diagnostics issue URL and duplicate-delivery proof.
- Downloadable evidence artifact and its SHA.
- Xu review and Vinh acceptance record.


## CI evidence update — 2026-11-20

- **Run:** [44746386416](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44746386416)
- **Commit:** `326f4d1fc312d991b601075990a96dd7969fde11`
- **Job:** `validate` — SUCCESS.
- **Test output:** `Ran 26 tests in 0.071s`; `OK`.
- **Artifact:** `w118-run-evidence-44746386416-1`, artifact ID `14632693408`, not expired at inspection.
- **Scope:** unit/contract and YAML/event/permission contract tests. The event jobs were skipped because this was a push event; no real handoff, ACK or diagnostics event is claimed by this run.


## Verification update — 2026-11-20 (30 tests)

- **Run:** [44746898664](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44746898664)
- **Commit:** `c49323b0241f0adc5b7827d58ce45916d628c832`
- **Job:** `validate` — SUCCESS.
- **Test output:** `Ran 30 tests in 0.103s`; `OK`.
- **Artifact:** `w118-run-evidence-44746898664-1`, artifact ID `14633311975`, not expired at inspection.
- **Added coverage:** owner-gated controlled diagnostics trigger, branch-scoped fault injection, unauthorized trigger denial and handoff re-application idempotency contract.
- **Event scope:** push run; event-specific jobs were skipped. This run does not claim live handoff, ACK or diagnostics runtime.

| ID | Scenario | Current state |
|---|---|---|
| T10-18 | Controlled diagnostics test trigger authorization | PASS — unit/contract coverage; live dispatch pending default-branch deployment |


## Review identity security cases — 2026-11-20

- Same principal, different GitHub logins: DENY.
- Reviewer mapped, PR author unmapped: DENY (independence not verifiable).
- Reviewer and PR author mapped to distinct principals: ALLOW only if reviewer has active acceptance permission.
- These cases are now part of the feature-branch unit test suite; runtime review event evidence remains pending.


## Principal-level review CI evidence — 2026-11-20

- **Run:** [44747589539](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44747589539)
- **Commit:** `999691e8863b40f77602d15f2e12a1ec85985a58`
- **Result:** validate SUCCESS; `Ran 32 tests in 0.064s`; `OK`.
- **Artifact:** `w118-run-evidence-44747589539-1`, ID `14634211524`, not expired at inspection.
- **New security assertions:** same HQTT principal via two GitHub logins is denied; unmapped PR author is denied; different mapped principal is accepted only with active acceptance permission.


## Latest validation — 2026-11-20

- Run [44747797589](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44747797589) SUCCESS.
- Commit: `52ee35920156b4966a7b4d60b214ed3c80001b76`.
- Test output: `Ran 32 tests in 0.106s`; `OK`.
- Artifact: `w118-run-evidence-44747797589-1`, ID `14634046784`, not expired at inspection.
- Event-specific jobs were skipped on the push event; this remains contract/unit evidence, not live GitHub event E2E.


## Event evidence / PR checklist coverage — 2026-11-20

- Added `event_evidence.py` tests: event/run binding, immutable RECORDED state, Work 70 boundary and invalid input rejection.
- Added contract checks: ACK label is applied only inside the authorized branch; handoff/ACK/review jobs upload event artifacts; PR checklist uses safe `pull_request_target` with no checkout; path filters include the checklist workflow.
- The PR checklist write attempt in ordinary pull_request context failed because the GitHub token was read-only. The design was corrected to a dedicated base-context workflow; no token permission escalation was made.
- Latest verified count before this amendment: 43 tests PASS in Run #44748809778; next CI run validates the path-filter test and final documentation.


## Latest event-contract verification — 2026-11-20

- **Run:** [44748965030](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44748965030)
- **Result:** SUCCESS; `Ran 44 tests in 0.175s`; `OK`.
- **Artifact:** `w118-run-evidence-44748965030-1`, ID `14634556693`, not expired at inspection.
- **New coverage:** OPERATION event evidence builder; immutable RECORDED state; ACK label applied only after authorization; safe `pull_request_target` checklist; same-repository scope; no PR code checkout; workflow path filter coverage.
- **Known event failure and correction:** ordinary pull_request token could not add comments (`Resource not accessible by integration`). The write action was removed from that context and moved to the base-context notifier; no broader token permission was requested.
- **Runtime limitation:** handoff, ACK, review and workflow_run diagnostics events remain pending default-branch integration.


## Provenance and diagnostics coverage update — 2026-11-20

- Added contract test that CI run evidence binds source commit, tested commit/ref, repository, actor, run URL and PR identity.
- Added diagnostics subscription for `W118 PR Review Checklist`; contract test confirms the listener covers W118, PR checklist, W300 and Work 70 and does not self-listen.


## Latest verified contract run — 2026-11-20

- **Run:** [44749396083](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44749396083)
- **Result:** SUCCESS; `Ran 45 tests in 0.229s`; `OK`.
- **Artifact:** `w118-run-evidence-44749396083-1`, ID `14635085374`, not expired at inspection.
- **Coverage:** CI source/tested revision provenance; diagnostics subscription includes PR checklist; all prior role, idempotency, ACK label, event artifact and safe PR notifier contracts.
- **Runtime boundary:** event-specific jobs were skipped on the push run; no live event E2E PASS is claimed.
