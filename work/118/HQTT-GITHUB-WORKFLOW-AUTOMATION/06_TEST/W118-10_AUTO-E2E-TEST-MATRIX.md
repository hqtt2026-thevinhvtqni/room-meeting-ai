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
| T10-17 | Xu acceptance reviewer identity | Xu mapped to verified GitHub login and accepted review recorded | BLOCKED — identity not yet confirmed |\n| T10-19 | Review policy provenance | pull_request_review authorization loads role map and verifier only from trusted default branch; no PR-controlled checkout credentials | PASS — regression test in Run #44755364888; 46 tests total |\n| T10-20 | ACK Work-scope authorization | ACK event is processed only when source Issue has `w118-handoff` label and is not a PR | PASS — regression test in Run #44755648230; 47 tests total |\n| T10-21 | Independent review authority | Only an explicitly mapped independent reviewer can record review authority; project-owner final acceptance is not interchangeable | PASS — unit tests in Run #44755930029; 47 tests total |\n| T10-22 | Role-map schema completeness | Role map rejects entries missing the independent-review permission field | PASS — schema 1.1 regression in Run #44756198541; 48 tests total |\n| T10-23 | Review evidence provenance | Review OPERATION artifact binds exact trusted policy commit, PR head SHA, PR base SHA and event SHA | PASS — regression test in Run #44756410351; 49 tests total |\n| T10-24 | Direct fault-injection authorization | Direct workflow_dispatch is authorized against trusted default-branch role map before failure injection | PASS — regression test in Run #44757234204; 50 tests total |\n| T10-25 | Diagnostic issue idempotency across closure | A closed diagnostic Issue with the same workflow_id + commit SHA is reopened/updated instead of creating a duplicate | PASS — unit + workflow contract tests in Run #44758004387; 52 tests total |

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


## Runtime execution package

Post-merge event execution order and expected outcomes are specified in [RT-118-001](../09_RUNTIME/RT-118-001_POST-MERGE-E2E-RUNBOOK.md). This runbook is prepared only; no issue/comment/diagnostics runtime result is marked PASS before its actual GitHub event evidence exists.


## Latest branch validation — 2026-11-20

- Run [#44749959595](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44749959595): SUCCESS; `Ran 45 tests in 0.138s`; `OK`.
- Artifact `w118-run-evidence-44749959595-1`, ID `14635085964`, not expired at inspection.
- PR #67 head `6824976dc133790d47aedcf0e5a385e875b2f198`; branch 116 ahead / 0 behind main.
- This is contract/unit CI only. Handoff, ACK, review and workflow_run runtime jobs were skipped on push; runtime E2E remains pending.
\n\n## P0 review-policy provenance regression evidence — 2026-11-20\n\n- **Run:** [44755364888](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755364888) — validate SUCCESS.\n- **Test output:** `Ran 46 tests in 0.234s`; `OK`.\n- **Tested commit:** `a5c4c52ef660c60e98c480f5bc63bfaf26e81d1e`.\n- **Regression:** `test_review_authorization_checks_out_trusted_default_branch` PASS.\n- **Artifact:** `w118-run-evidence-44755364888-1`, ID `14636718273`, SHA-256 `c5b8d9a860c111079304579d74213ff516fe1016952bd74756aac4719b670689`, unexpired at readback.\n- **Scope:** PR synchronize validation; handoff, ACK, acceptance-review and controlled-failure event jobs were SKIPPED. This is unit/contract proof only, not runtime event E2E.\n\n\n## ACK Work-scope regression evidence — 2026-11-20\n\n- **Run:** [44755648230](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755648230) — validate SUCCESS.\n- **Test output:** `Ran 47 tests in 0.319s`; `OK`.\n- **Tested commit:** `6db3296e663b27008d9269cd191ac2edea990b6f`.\n- **Regression:** `test_ack_verification_is_scoped_to_w118_handoff_issues` PASS.\n- **Artifact:** `w118-run-evidence-44755648230-1`, ID `14637735820`, SHA-256 `c4ec772682b4a967d903ded718af9ed806f3c37af614394d486e7b746ecbd79c`, unexpired at readback.\n- **Scope:** PR synchronize validation; event-specific handoff/ACK/review/controlled-failure jobs were SKIPPED. No runtime event E2E is claimed.\n\n\n## Independent-review authority separation evidence — 2026-11-20\n\n- **Run:** [44755930029](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44755930029) — validate SUCCESS.\n- **Test output:** `Ran 47 tests in 0.229s`; `OK`.\n- **Tested commit:** `021e5c9555c623150fec96f68367417cf2d26e73`.\n- **Coverage:** owner accounts retain `can_accept=true` but have `can_independently_review=false`; an independent reviewer fixture is allowed only when explicitly mapped and active; same-principal cross-account review and unmapped PR author are denied.\n- **Artifact:** `w118-run-evidence-44755930029-1`, ID `14637227755`, SHA-256 `5975be66447fd1d3512a88d809d04536cb4906665a2d31eec491e46a2f77af87`, unexpired at readback.\n- **Scope:** PR synchronize validation; event-specific jobs were SKIPPED. No runtime review event or positive live ACK is claimed.\n\n\n## Role-map schema 1.1 verification — 2026-11-20\n\n- **Run:** [44756198541](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44756198541) — validate SUCCESS.\n- **Test output:** `Ran 48 tests in 0.321s`; `OK`.\n- **Tested commit:** `898742306f00bb8d09fa7b60f4119dcf6e579a8b`.\n- **Schema:** role map version bumped to `1.1`; loader requires the independent-review permission field; T10-22 verifies missing-field rejection.\n- **Artifact:** `w118-run-evidence-44756198541-1`, ID `14638126091`, SHA-256 `681be1785735281a936d774f0de422c973fc9dc48871c53262d10c26dfe1fabf`, unexpired at readback.\n- **Scope:** PR synchronize validation; event-specific jobs were SKIPPED. No runtime event E2E is claimed.\n\n\n## Review evidence provenance regression — 2026-11-20\n\n- **Run:** [44756410351](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44756410351) — validate SUCCESS.\n- **Test output:** `Ran 49 tests in 0.207s`; `OK`.\n- **Tested commit:** `bd4613d50d2ce9f5e417840a513332b1022c94ad`.\n- **Regression:** T10-23 asserts that review evidence source_commit is the checked-out trusted policy SHA and that event, PR head and PR base SHAs are separately bound.\n- **Artifact:** `w118-run-evidence-44756410351-1`, ID `14638351674`, SHA-256 `c13688e45484886f302aac1046464587c821a098488259f447442409b0b51a9a`, unexpired at readback.\n- **Scope:** PR synchronize validation; event-specific jobs remain SKIPPED. No live review event E2E is claimed.\n\n\n## Direct fault-injection authorization regression — 2026-11-20\n\n- **Run:** [44757234204](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44757234204) — validate SUCCESS.\n- **Test output:** `Ran 50 tests in 0.201s`; `OK`.\n- **Tested commit:** `d7241386f491840172e840c79dada7fea61f2576`.\n- **Regression:** T10-24 asserts direct workflow_dispatch actor is checked against trusted default-branch authorization before the deliberate failure step can run.\n- **Artifact:** `w118-run-evidence-44757234204-1`, ID `14638571210`, SHA-256 `0dd1c6dc177ea53d6f64e231b7367e36dbce348b374b36c73c69abf8df4274a8`, unexpired at readback.\n- **Scope:** PR synchronize validation; direct controlled-failure and other event jobs were SKIPPED. This proves the guard contract, not live actor propagation.\n\n\n## Diagnostics closed-Issue idempotency regression — 2026-11-20\n\n- **Run:** [44758004387](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44758004387) — validate SUCCESS.\n- **Test output:** `Ran 52 tests in 0.394s`; `OK`.\n- **Tested commit:** `a8051d66755830690fa96940f44b048ba8e1fd0f`.\n- **Coverage:** closed issue key reuse unit test PASS; workflow contract verifies `--state all` and `gh issue reopen`.\n- **Artifact:** `w118-run-evidence-44758004387-1`, ID `14640485869`, SHA-256 `b029bddc43da57df2b0199b1dde40987fbe096ed82dda23f2f4571fa5f2ec949`, unexpired at readback.\n- **Intermediate failure:** Run #44757920850 failed because the first contract assertion incorrectly expected the helper name in the shell workflow; assertion was corrected to verify actual CLI arguments. Final run above is PASS.\n- **Scope:** PR synchronize validation; diagnostics workflow_run job itself was not executed.\n