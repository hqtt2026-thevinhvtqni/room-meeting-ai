# W118-13..17 — Core/GitHub Adapter Test Matrix

- **Architecture:** TD-118-012 v1.2
- **Status:** CONTRACT TEST PLAN — exact-head CI evidence linked below
- **Rule:** Tests prove adapter behavior only; they do not prove Core/W102/W14 runtime availability.

## 1. Core Task projection adapter

| ID | Scenario | Expected |
|---|---|---|
| C01 | Explicit Core-owner field map | Normalize approved snapshot |
| C02 | Missing required field mapping | Reject; no guessed Core schema |
| C03 | Missing nested field path | Reject |
| C04 | Duplicate/invalid acceptance check | Reject |
| C05 | Issue ID null/positive | Accept only valid values |
| C06 | Issue projection | Stable Core Task marker, source revision and authority boundary |
| C07 | Read-only behavior | No Task state, Assignment state, event ID or sequence mutation |

## 2. GitHub Issue mirror

| ID | Scenario | Expected |
|---|---|---|
| I01 | First Core Task mirror | Create one Issue and exact readback |
| I02 | Repeated mirror | Idempotent; no duplicate |
| I03 | New Core source revision | Update same Issue and readback |
| I04 | PR contains same marker | Exclude PR; create/find Issue only |
| I05 | Pagination limit reached | Fail closed; no possible duplicate create |
| I06 | Missing Core lock lease | Reject before API call |
| I07 | Non-Core Task object | Reject |
| I08 | Issue mirror permissions | No Assignee, Issue state, merge or release mutation |

## 3. Source binding

| ID | Scenario | Expected |
|---|---|---|
| S01 | Task-scoped branch + matching trailers | PASS binding |
| S02 | Missing/duplicate Work/Task/Issue trailer | Reject |
| S03 | Work/Task/Issue mismatch | Reject |
| S04 | after/head_commit/commit SHA mismatch | Reject |
| S05 | Force push or branch deletion | Reject |
| S06 | Aggregate legacy branch | UNBOUND_LEGACY_BRANCH; no Task inference |

## 4. Stateless GitHub webhook verifier

| ID | Scenario | Expected |
|---|---|---|
| W01 | Valid HMAC-SHA256 | Verified transient envelope |
| W02 | Invalid signature / missing header | Reject |
| W03 | Short secret / malformed digest | Reject |
| W04 | Non-UUID delivery ID | Reject |
| W05 | Wrong repository / unallowlisted event | Reject |
| W06 | Invalid JSON / oversized body | Reject |
| W07 | Timestamp without timezone | Reject |
| W08 | Persistence boundary | No inbox, queue, event ID or sequence |

## 5. Stateless GitHub event adapter

| ID | Scenario | Expected |
|---|---|---|
| E01 | Task-scoped push exact binding | EVIDENCE_LINKED intent |
| E02 | Aggregate branch push | UNBOUND; no event intent |
| E03 | Work/Task/Issue mismatch | Reject |
| E04 | Push without Core Issue link | BLOCKED |
| E05 | CI with matching Core source binding | CI evidence intent |
| E06 | CI arrives before Core push evidence | DEFERRED; no local queue |
| E07 | Unapproved workflow name | Reject |
| E08 | CI failure | Evidence only; no Task/Assignment state |
| E09 | Issue closed/reopened | Observation only; Core decides |
| E10 | Unlinked Issue event | UNHANDLED |
| E11 | Unverified delivery envelope | Reject |
| E12 | Core event intent | No event_id/seq; Core assigns and persists |

## 6. GitHub Actions workflow contract

| ID | Scenario | Expected |
|---|---|---|
| G01 | Handoff label | Request captured; no Assignment |
| G02 | ACKED comment | Claim captured; no identity verification or ACK state |
| G03 | PR review submitted | Observation captured; no acceptance/merge/release |
| G04 | Permissions | Least privilege, no contents write or bypass |
| G05 | Action pinning | Third-party actions SHA pinned |
| G06 | Failure evidence | Artifacts identify exact event/run/commit |

## 7. Runtime integration — NOT RUN

| ID | Integration | Required owner / dependency |
|---|---|---|
| R01 | Core Task snapshot API + approved field map | Core :8000 owner |
| R02 | Core per-Task lock lease | Core :8000 owner |
| R03 | Core Event Intent ingress and dedup | Core :8000 owner |
| R04 | Agent identity/Assignment/ACK | W102 + W01/W02/W22 + Core |
| R05 | Execution/branch/commit/push | W14 (absorbed W12/W13 modules) |
| R06 | CI adapter and callback | W14 integrated path + GitHub Actions |
| R07 | Work 70 projection parity | W70 owner/schema ACK |
| R08 | Full Plan-to-Close E2E | All owners + Vinh acceptance |

## 8. Exact CI evidence

Update only after inspecting the exact branch-head run and its artifact. Contract CI PASS must never be reported as runtime E2E or product acceptance.


## Exact-head CI result

- SHA `5f02a9eafbf68eb0bcfca2942733882dab9cc5bf`
- Push run #44882420198 SUCCESS — 94 tests PASS / 0.209s
- PR run #44882422288 SUCCESS
- Artifact ID 14697683781; SHA-256 `a2703f70b4a250197b14a84bb5408cef18f2917266f542c7850a54c70e098abc`
- Runtime integration tests R01–R08 remain NOT RUN because Core/W102/W14/W70 ports/approvals are unavailable.


## Ownership correction — 2026-11-22

R05/R06 runtime owner is W14. W12/W13 are absorbed internal components, not standalone owners. W14 canonical source/API/runtime parity remains NOT VERIFIED; runtime integration cases remain BLOCKED.


## 8. Current exact-head contract verification — 2026-11-22

- **Tested source SHA:** `dbdd71d6758abfdf614a59dce2fe5f081cb6a454`.
- **GitHub Actions:** PR run #44951313523 SUCCESS; 95 tests PASS / 0.208s.
- **Artifact:** ID 14724769218; SHA-256 `2758b161a6e47427c48b966b4bcd5d3bbe1135e7c7b0398316eb87e249372e42`.
- Added regression guard: W14 is sole integrated execution owner; W12/W13 are absorbed internal foundations; W70 DOC-093 remains DRAFT_NOT_APPROVED.
- **Runtime tests R01–R08:** NOT RUN / BLOCKED. W14 source/runtime parity, Core API/event port, W102 principal/Assignment and W70 approved schema/owner ACK are unavailable or unverified.
- Contract CI PASS is not runtime E2E, independent review, product acceptance or release.
