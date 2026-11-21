# WORK 10 — P0 ACCEPTANCE INTEGRITY AMENDMENT V7

- Document ID: W10-P0-ACCEPTANCE-INTEGRITY-AMENDMENT-20261119-07
- Work: 10 — COMPUTER-AGENT | Sandbox Work ID: 10
- Name: Ka | Title: Delivery / Technical Coordinator
- Date-Time: 2026-11-19 13:50 (UTC+07:00)
- Priority: P0
- Status: DESIGN REVISION — STATIC ONLY — NOT IMPLEMENTED
- Supersedes: none; supplements Amendment v6 without overwriting it.
- Inputs: AN independent review result v6; Amendment v6; Schema v6; Crash Matrix v6; Work Manifest; Sync Policy v1.2; Work Structure Standard; three LOCKED contracts.

## 1. Authority and boundaries

This is a design/evidence amendment only. It does not authorize P0 implementation, source/test/runtime/configuration changes, host tests, GitHub writes, or release. Amendment v6, Schema v6, Matrix v6 and An's review remain immutable historical evidence.

Read-only contracts remain LOCKED:
- ACTION_CONTRACT.md
- WORKFLOW_CONTRACT.md
- SAFETY_POLICY.md

No host fixture, OS primitive, transport stack, runtime behavior, or executable PASS is asserted. The revised schema has been serialized as JSON and parsed as JSON in the authoring environment only; no JSON Schema validator has been run.

## 2. Finding dispositions

| An finding | V7 action | Current disposition |
|---|---|---|
| AN-V6-F01 — PASS omits state/oracle evidence | V7 schema requires the full expected and observed state tuple; PASS requires non-empty structured oracle evidence, safe terminal state, a consistency-check record and at least one hashed PRESENT artifact. | DESIGN REMEDIATION PROPOSED; validator proof BLOCKED; finding remains OPEN pending An review. |
| AN-V6-F02 — SUPPORTED profile lacks immutable fixture identity | V7 schema conditionally requires non-null SHA-256, host_build, architecture and fixture_manifest_ref for SUPPORTED profiles; PASS requires SUPPORTED. | DESIGN REMEDIATION PROPOSED; actual host fixture absent; finding remains OPEN/BLOCKED pending An review and real fixture. |
| AN-V6-F03 — expected/observed/verdict inconsistency | V7 adds a mandatory PASS consistency-check record. Because JSON Schema cannot compare arbitrary sibling values for equality, a separate semantic validator MUST compare expected vs observed outcome and all applicable state fields; PASS requires validator_result=PASS and both match flags true. | PARTIAL DESIGN REMEDIATION; semantic validator and negative test execution NOT RUN; finding remains OPEN pending An review. |
| AN-V6-F04 — matrix not executable | Keep v6 matrix as DESIGN ONLY; add negative schema/semantic validation case catalogue in this amendment. Host/transport fixture and executable harness remain absent. | PARTIAL / BLOCKED; not closed. |

No finding is closed by Ka. Only An may provide independent re-review disposition; runtime/host claims additionally require executable evidence.

## 3. V7 schema contract

Companion file: 06_EVIDENCE/W10_P0_ACCEPTANCE_MANIFEST_V7.schema.json

V7 changes:
1. expected and observed both require outcome, admission, gate, process_state, containment_state, lease_state and owner_state.
2. observed.oracle_evidence is required as structured records containing oracle_id, source, result and artifact_ref.
3. SUPPORTED conditionally requires non-null fixture SHA-256, exact host_build, architecture and fixture_manifest_ref.
4. PASS requires profile support_status=SUPPORTED; admission=CLOSED; gate=CLOSED; containment_state=EMPTY; process_state=ABSENT or EXITED; non-empty oracle evidence; a consistency_check with both match flags true and validator_result=PASS; and at least one PRESENT artifact with a valid SHA-256.
5. Every PRESENT artifact requires a valid SHA-256. Every NA artifact requires a non-empty na_reason.
6. UNSUPPORTED profiles cannot produce PASS.
7. Test IDs and review revision are V7-scoped.

Important limitation: schema validation alone cannot prove that evidence is genuine, that expected equals observed, that a hash refers to the actual fixture, or that an oracle was obtained from the authoritative OS/transport source. These require semantic validator checks plus independently retained artifacts. A caller-authored consistency_check is not itself proof.

## 4. Required semantic validator rules

The validator MUST reject a record unless:
- expected.outcome equals observed.outcome;
- each expected state field applicable to the test category equals its observed counterpart;
- every oracle artifact_ref resolves to a PRESENT artifact whose bytes hash to the recorded SHA-256;
- the fixture_manifest_ref resolves to the exact fixture bytes whose SHA-256 equals profile.fixture_sha256;
- the fixture host_build and architecture equal the observed host inventory, not caller-supplied labels alone;
- category-specific oracle IDs and sources match an allow-listed oracle map for that test category and OS;
- PASS has no UNKNOWN state, no missing oracle, no unresolved task, and no pending cleanup;
- verdict PASS is consistent with the test's expected terminal outcome. For example, a test may have expected/observed outcome TERMINATED and verdict PASS when the termination acceptance assertions all pass. Verdict PASS does not mean observed.outcome must literally be PASS.

The validator itself must emit its version/hash, input manifest hash, result, per-rule results, and timestamp. Validator PASS is necessary but not sufficient for runtime acceptance; independent review and source/host provenance remain separate gates.

## 5. Negative validation catalogue — required before re-review

The following are test specifications, not executed tests:

| Case ID | Mutation | Required result |
|---|---|---|
| W10-V7-SCHEMA-01 | Remove observed.process_state | REJECT |
| W10-V7-SCHEMA-02 | Remove observed.containment_state | REJECT |
| W10-V7-SCHEMA-03 | Remove observed.lease_state or owner_state | REJECT |
| W10-V7-SCHEMA-04 | PASS with missing/empty oracle_evidence | REJECT |
| W10-V7-SCHEMA-05 | SUPPORTED with null/missing fixture_sha256 | REJECT |
| W10-V7-SCHEMA-06 | SUPPORTED with null/missing host_build | REJECT |
| W10-V7-SCHEMA-07 | SUPPORTED with null/missing architecture | REJECT |
| W10-V7-SCHEMA-08 | PASS with missing consistency_check or validator_result != PASS | REJECT |
| W10-V7-SCHEMA-09 | PASS without any PRESENT artifact carrying valid SHA-256 | REJECT |
| W10-V7-SEM-01 | verdict PASS while expected.outcome != observed.outcome | REJECT |
| W10-V7-SEM-02 | verdict PASS while any applicable expected/observed state differs | REJECT |
| W10-V7-SEM-03 | PASS whose fixture hash does not match fixture bytes/host inventory | REJECT |
| W10-V7-SEM-04 | PASS whose oracle artifact is absent, NA, hash-mismatched or from an unapproved source | REJECT |
| W10-V7-SEM-05 | PASS while any required state is UNKNOWN or cleanup remains pending | REJECT |
| W10-V7-SEM-06 | UNSUPPORTED profile with verdict PASS | REJECT |

Execution status for every case above: NOT RUN. No result may be recorded PASS until a real validator and its test suite execute against the exact V7 schema hash.

## 6. F04 acceptance-matrix boundary

The 21-row v6 crash matrix remains DESIGN ONLY. Its unique IDs and written oracles do not establish executable acceptance. Before F04 can move beyond PARTIAL/BLOCKED, each row needs:
- one test-owned deterministic injection fixture and documented reset procedure;
- pinned OS/transport profile and immutable fixture hash;
- exact injection-point confirmation;
- authoritative process/containment/gate/lease/owner oracle capture;
- expected-vs-observed semantic comparison;
- retained logs/artifacts and reproducible runner command;
- independent re-run or witness review.

Windows Job Object and Linux cgroup v2 evidence remain separate. HTTP abort rows require peer-socket and server-side closure evidence; client timeout/cancellation alone is insufficient. No host fixture is currently supplied.

## 7. Gate and next actions

- AN-V6-F01: OPEN — V7 schema design proposed; validator not run.
- AN-V6-F02: OPEN / BLOCKED — schema tightened; actual immutable host fixture absent.
- AN-V6-F03: OPEN / PARTIAL — semantic validator specification added; implementation/tests not run.
- AN-V6-F04: PARTIAL / BLOCKED — executable fixtures and host evidence absent.
- P0 implementation: BLOCKED / NOT AUTHORIZED.
- Release: NOT AUTHORIZED.
- Work 10: ACTIVE — NOT RELEASED.
- Three contracts: LOCKED / READ-ONLY.
- Source/test/runtime/config: NOT MODIFIED.
- Host/runtime tests: NOT RUN.
- JSON Schema validator: NOT RUN.
- GitHub parity: NOT VERIFIED.

Next sequence:
1. An independently re-reviews V7 schema and this amendment; no self-closure by Ka.
2. After An's design review, a separate authorized validation task may implement/run schema and semantic negative tests; this does not authorize P0 runtime implementation.
3. Obtain actual Windows/Linux fixture inventories and transport fixture before claiming SUPPORTED.
4. Keep F04 blocked until executable crash/transport harness and host evidence exist.
5. Preserve F-15 as OWNER DECISION REQUIRED; no TaskResult/Workflow timeout mapping is inferred.

KÝ: Ka | Delivery / Technical Coordinator
