# WORK 28 — ACCEPTANCE DEPENDENCY MATRIX (PR #74 / AD-W28-20261123-002)

**Evidence ID:** EV-W28-20261123-001  
**Priority:** P0 — release-blocking dependency matrix  
**Read order:** 32  
**Work:** 28 — MCP-8020-TOOLING-PLATFORM  
**Branch:** ka/work28-security-hardening-20261123  
**Date-Time:** 2026-11-23 15:04 +07:00  
**Author:** Ka — owner-delegated BUILD OWNER / CSA  
**Status:** EVIDENCE MAP — NOT AN APPROVAL / NOT A TEST RESULT

## 1. Purpose

Map PR #74 architecture baseline gates G0–G7 to the current Work28 candidate evidence and unresolved owner-owned dependencies. This is a source/documentation map, not a claim that external Work components have passed.

## 2. Gate matrix

| PR #74 gate | Owner / boundary | Required acceptance evidence | Current bounded evidence | Status |
|---|---|---|---|---|
| G0 — Source provenance | Core, W14, W52, W70 | Canonical repos/branches/HEADs, file hashes, release mapping and deployed process/build identity | Main Core entrypoint/adapter mismatch recorded; W14 release branch is 6 ahead / 1,793 behind Main and lacks expected manifest/boundary paths; W52 branch is 4 ahead / 1,759 behind Main and contains only four W52 docs; W70 DOC-061 remains draft | **BLOCKED** |
| G1 — Identity | Core + W52 | Enrolled service and Agent principals, protected credential, revocation and runtime attestation | Work28 V1.2 candidate has service credential hash tests; no live Agent principal, recipient runtime attestation, credential rotation or deployed identity proof | **BLOCKED** |
| G2 — W52 dispatch / ACK | W52 | Authenticated assignment dispatch, recipient ACK/NACK, durable outbox, idempotency, cursor and recovery | PR #74 defines ownership; inspected W52 GitHub branch has no orchestration implementation; Sandbox-only candidates not independently read or proven live | **BLOCKED** |
| G3 — Core authority | Core :8000 | Gate-aware scoped grant issue/validate/revoke; append-only ledger; restart/readback; source and assignment binding | Main inspected app does not mount grant routes; Work28 V1.2 authority is candidate-only; PR #48 is open/unmerged and has a recorded source-hash binding defect; DOC-W28-078 is subordinate candidate only | **BLOCKED** |
| G4 — W14 Host | W14 | Online grant + ACK validation before side effect; W14 HostPort; containment-before-spawn; isolation, timeout, cancellation, descendant cleanup and run record | Main Host POST /execute trusts caller WorkContext; inspected W14 bridge is one-shot HTTP, not persistent bidirectional RpcPort; W14 canonical source/deployment not pinned | **BLOCKED** |
| G5 — Provider | W14; W10 locked | Approved provider contract/capability negotiation and harmless read-only test behind W14 | W10 remains LOCKED / NO CHANGE; no provider invocation authorized or tested | **NOT AUTHORIZED / BLOCKED** |
| G6 — Projection | W092 / W113 | Actual Core events rendered with source timestamps, actor, IDs, reason and evidence refs; stale/unknown states | No live authoritative execution events exist in this Work28 candidate; projections not connected/proven | **NOT VERIFIED** |
| G7 — Independent E2E | W28 + owner Works + independent QE | Non-production Agent lifecycle observed end-to-end; negative/recovery tests; immutable evidence and readback | PR #76 CI #438 proves configured candidate unit/regression + Linux/Windows lifecycle only; no live Core/W52/W14/provider/PC/E2E; independent QE is not assigned in current owner-delegated phase | **BLOCKED** |

## 3. Work28 candidate-local evidence (do not overstate)

| Area | Evidence | What it proves | What it does not prove |
|---|---|---|---|
| PR #76 fail-closed security slice | CI run #438 / 45102972232; merge candidate 3d43ee511ad5ea69e4464079bfbf3c4e5ce3f074; 5/5 jobs SUCCESS | Configured Work28 tests, Linux/Windows lifecycle suites, immutable artifact and auto gate report for exact merge candidate | Live Core authority, W52 ACK, W14 HostPort, W70 policy, deployed process, protected evidence readback |
| Core transport hardening | HTTPS-only remote URL, no redirects; raw CI logs in #429/#438 | Candidate client transport behavior under configured tests | Correct canonical Core route, deployed TLS identity, live grant validation |
| HTTP snapshot containment | Candidate returns 503 if online Core validator absent; no snapshot side effect | Protected snapshot HTTP path remains blocked without online authority | Functional authorized execution |
| DOC-W28-078 | Candidate contract and source addenda A1/A2 plus W14/W70/W52 trace | Wire-level proposal and bounded source findings | Approved route/schema, external owner contract, implementation, runtime |
| Journal | JRN-W28-071..083 on candidate branch | Append-only Work activity/evidence trail on PR branch | Canonical branch integration or product acceptance |

## 4. Blocking dependency order

1. **G0 first:** pin Core :8000 source/composition, W14 canonical source/HostPort owner mapping, W52 source/interface, W70 approved policy contract.
2. **G1 + G2:** establish service/Agent identity and recipient-authenticated ACK; ACK must be durable and precede any possible W14 side effect.
3. **G3:** implement the approved Core extension inside Core :8000, not a second Core or standalone authority process; prove grant binding, revocation, policy freshness, durable event sequence and readback.
4. **G4:** W14-owned adapter validates Core grant + ACK binding online, establishes containment before spawn and implements HostPort lifecycle/close semantics.
5. **G5 + G6:** provider remains behind W14; W092/W113 read actual Core events only.
6. **G7:** independent negative/recovery E2E with immutable artifacts, process/build identity and protected evidence readback.

No gate may be skipped or inferred from another gate's PASS.

## 5. Safe candidate work allowed while blocked

- Continue PR #76 candidate hardening and regression coverage that does not invent external routes or trust caller WorkContext.
- Convert DOC-W28-078 into non-authoritative schema fixtures and local negative tests, clearly marked candidate, after checking no owner schema conflict.
- Review candidate store concurrency/hash-chain behavior; do not deploy or label it Core's authoritative ledger.
- Maintain exact CI artifact/hash/journal readback.
- Do not modify Main, Core :8000, W14, W52, W70, W10, W092 or W113 source/runtime; do not call historical MCP :8020; do not run PC tests until Vinh reports PC ready.

## 6. Acceptance conclusion

**Work 28 is ACTIVE — INTEGRATION BLOCKED — NOT RELEASED. Execution Gate CLOSED.**

The candidate PR #76 CI result is valid within its configured test scope. All PR #74 G0–G7 integration gates remain BLOCKED or NOT VERIFIED as shown above. No merge, deployment, provider execution, live E2E or acceptance is claimed.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]
