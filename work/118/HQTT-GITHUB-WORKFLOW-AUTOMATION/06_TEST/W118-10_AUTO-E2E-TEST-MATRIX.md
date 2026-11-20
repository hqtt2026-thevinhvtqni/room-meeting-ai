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
