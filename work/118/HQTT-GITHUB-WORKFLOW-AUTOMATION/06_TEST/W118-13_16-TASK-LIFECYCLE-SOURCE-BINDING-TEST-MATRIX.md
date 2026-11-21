# W118-13 / W118-16 — TEST MATRIX: TASK LIFECYCLE & SOURCE BINDING

- **Architecture:** TD-118-012
- **Implementation:** W118-13/16 build note
- **Test code:** `tests/w118/test_task_lifecycle.py`, `tests/w118/test_source_binding.py`, `tests/w118/test_workflow_contract.py`
- **Status:** CONTRACT TESTS PASS AT TESTED SHA — RUNTIME E2E PENDING

## 1. W118-13 — Task Contract / Lifecycle

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T13-01 | Create valid Task | DRAFT, version 1, creation event recorded | PASS |
| T13-02 | Invalid acceptance criteria | Reject Task creation | PASS |
| T13-03 | Non-owner creates Task | DENY | PASS |
| T13-04 | Actor identity unverified | DENY / fail closed | PASS |
| T13-05 | Executor attempts READY | DENY | PASS |
| T13-06 | Full lifecycle with separate Owner, Orchestrator, Executor, Verifier | Each transition follows allowed graph | PASS |
| T13-07 | ACK by non-assigned principal | DENY | PASS |
| T13-08 | ACK references wrong dispatch ID | DENY | PASS |
| T13-09 | Agent attempts ACCEPTED | DENY | PASS |
| T13-10 | VERIFIED without evidence refs | Reject | PASS |
| T13-11 | CLOSED without successful Issue readback | Reject | PASS |
| T13-12 | Stale expected version | VersionConflict; no state mutation | PASS |
| T13-13 | Duplicate idempotency key + same operation | Replay/no duplicate event | PASS |
| T13-14 | Same idempotency key + different operation | IdempotencyConflict | PASS |
| T13-15 | Non-owner principal attempts Owner transition | DENY | PASS |
| T13-16 | Transition details attempt to overwrite protected Task identity | Reject | PASS |
| T13-17 | Event history order | Append-only ordered event sequence | PASS |

## 2. W118-16 — GitHub Push Source Binding

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T16-01 | Parse canonical Task branch | Extract Work ID and Task ID | PASS |
| T16-02 | Existing aggregate branch | UNBOUND_LEGACY_BRANCH; no guessed Task | PASS |
| T16-03 | Valid push payload | BOUND with repository, Work, Task, Issue and exact head SHA | PASS |
| T16-04 | Wrong repository | Reject | PASS |
| T16-05 | Work ID / Task ID prefix mismatch | Reject | PASS |
| T16-06 | Missing commit trailers | Reject | PASS |
| T16-07 | Duplicate Issue trailer | Reject | PASS |
| T16-08 | Commit Task ID mismatch | Reject | PASS |
| T16-09 | Mixed Issue IDs in one push | Reject | PASS |
| T16-10 | head_commit SHA differs from push after | Reject | PASS |
| T16-11 | Force push | Reject | PASS |
| T16-12 | Push after SHA absent from commits list | Reject | PASS |
| T16-13 | Branch deletion | Reject | PASS |
| T16-14 | Empty commits list | Reject | PASS |
| T16-15 | Workflow invokes source validator on push | Contract check | PASS |
| T16-16 | Workflow records source-binding status in CI evidence | Contract check | PASS |
| T16-17 | Workflow artifact includes run and optional source-binding evidence | Contract check | PASS |

## 3. Exact CI evidence

- Tested code/workflow SHA: `5e131e108a7195ca1ff5ae96b3fadb119e4bc31b`.
- Push run: [#44877054701](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877054701) — SUCCESS; 86 tests PASS / 0.332s.
- PR run: [#44877057892](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44877057892) — validate SUCCESS.
- Artifact ID: `14696186741`; SHA-256: `9dae6385ae1e68572305ee6314bf1edf046361fc9993301cc85367603c56531a`.
- Push on current aggregate branch returned `UNBOUND_LEGACY_BRANCH`, which is the intended fail-closed result; no Task state was changed.
- Event-specific handoff, ACK, acceptance-review and controlled-failure jobs were SKIPPED.

## 4. Not covered / runtime gates

- Real task-scoped branch creation and push event.
- Authenticated webhook delivery to Sandbox and duplicate/out-of-order delivery.
- Real Agent Registry principal, capability match, dispatch, positive/negative ACK, heartbeat and reassignment.
- GitHub Issue create/update/readback from Sandbox.
- CI PASS/FAIL callback updating the correct Task.
- Work 70 Evidence Register and Dashboard projection.
- Full lifecycle runtime E2E and product acceptance.

**Disposition:** contract PASS at tested SHA; no claim of live runtime E2E or W118 product acceptance.


## 5. Task Register and Task/Assignment separation update

| Test ID | Scenario | Expected result | Current evidence |
|---|---|---|---|
| T13-18 | New Task creation | Task status PLANNED; Assignment status UNASSIGNED | PASS |
| T13-19 | Task READY transition | Only Owner/Orchestrator can change Task status | PASS |
| T13-20 | Assignment PROPOSED/DISPATCHED/ACKNOWLEDGED | Separate Assignment state changes; Task status remains READY | PASS |
| T13-21 | Executor ACK | Exact assigned principal and dispatch ID required | PASS |
| T13-22 | Agent-assigned Task IN_PROGRESS | Requires Assignment ACKNOWLEDGED/IN_PROGRESS | PASS |
| T13-23 | Assignment ACCEPTED | Requires independent verifier evidence | PASS |
| T13-24 | Task DONE | Requires Assignment ACCEPTED and Owner acceptance evidence | PASS |
| T13-25 | Issue link | Separate readback event; does not change Task status | PASS |
| T13-26 | External push/CI observation | Appends evidence; Task and Assignment status unchanged | PASS |

**Latest combined contract CI:** exact branch-head SHA `45b2cda82a99589afe33f2838656c5bbae8069f5`; push run [#44879719166](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44879719166) SUCCESS; 127 tests PASS / 0.257s; artifact ID 14697318273; SHA-256 `de06cfb5787728c7fb214fb80c485f6efe33e2738ad9376db0ea66748b8f2514`.


| T13-27 | OWNER_DIRECTED_SESSION | Task may enter IN_PROGRESS with explicit Owner directive reference while Assignment remains UNASSIGNED | PASS |
| T13-28 | OWNER_DIRECTED_SESSION without directive reference | Reject; do not fabricate Agent identity or ACK | PASS |

**Owner-directed execution CI:** tested SHA `4bd94d43251f26e88200d6e0f1ef9c19354bc426`; push run #44880193690 SUCCESS; 130 tests PASS / 0.512s; artifact ID 14697279628; SHA-256 `0eeb2d5cdf89a31c9d8e2346c04f1083c4d1d9699154f572cb70b73c94e56807`.


**Latest owner-directed execution test:** SHA `108595c61f2d2ad9097dda1eed3252f7cfbec7e0`; run #44880271750 SUCCESS; 130 tests PASS / 0.402s; artifact ID 14697951120; SHA-256 `8e33daf7a33c3a7131acad64f3d56f04be9a0e519f72e2aeb2f389aa6d864138`.
