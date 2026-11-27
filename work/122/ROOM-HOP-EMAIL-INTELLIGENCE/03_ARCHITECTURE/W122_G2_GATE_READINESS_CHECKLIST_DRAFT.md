# W122 — G2 Gate Readiness Checklist
**ID:** G2-CHECK-W122-001 | **Version:** 0.1-DRAFT | **Date:** 2026-11-27
**Prepared by:** Xu / AI-01 | **Decision authority:** Vinh
**Status:** EVIDENCE REVIEW — G2 NOT APPROVED
**Related:** G2 Decision Pack; ODR-W122-001; SEC-W122-001; AUTH-STATE-W122-001; T001–T024

> This checklist assesses documentary readiness only. A document existing is not equivalent to an approved contract, independent review, runtime proof or gate PASS.

## 1. Gate evidence matrix
| ID | G2 requirement | Evidence currently present | Assessment | Missing evidence / closure condition |
|---|---|---|---|---|
| G2-01 | Canonical product scope and release boundaries | Architecture intake sections 1–19; G2 decision pack | PARTIAL | Owner accepts scope, first release, and explicit exclusions in canonical Biên bản |
| G2-02 | Owner decisions recorded | ODR-W122-001 has 12 OPEN decisions | BLOCKED | Explicit ACCEPT/REJECT/DEFER per required decision, rationale and Biên bản reference |
| G2-03 | Gmail OAuth scope and Google obligations | Gmail discovery notes; metadata/read-only/compose distinction | PARTIAL | Kha independent findings, exact scopes/API operations, consent/verification assessment and Owner acceptance |
| G2-04 | Mailbox identity and tenant isolation contract | W05 reuse boundary; proposed W122 authorization matrix | BLOCKED | Approved Core identity/tenant/mailbox ownership and delegation contract plus enforcement evidence |
| G2-05 | Audit and credential lifecycle | W05 generic patterns; proposed controls | BLOCKED | Approved credential vault and tamper-evident audit interfaces, ownership and durability guarantees |
| G2-06 | W52 task/event dispatch contract | W52 draft A2A contract and interface inspection | BLOCKED | Approved versioned dispatch/event contract and verified runtime identity/receipt/idempotency/retry/audit |
| G2-07 | W14 Host execution boundary | W12 boundary docs; W14 integration ownership identified | BLOCKED | Approved W14 Host contract, deployed adapter and execution evidence |
| G2-08 | Threat model independent review | SEC-W122-001 draft and Ka brief | BLOCKED | Verifiable Ka receipt and independent written verdict with threat dispositions |
| G2-09 | Authorization/state machine review | AUTH-STATE-W122-001 draft | PARTIAL | Ka review, owner decision and mapping to approved Core enforcement |
| G2-10 | Synthetic acceptance plan | T001–T024 plan authored | PARTIAL | Fixtures, implementation, test environment, independent QE identity and actual results; not a prerequisite to decide every architecture point but required before build/release gates as scoped |
| G2-11 | Cost ceiling and service commitments | ODR-10 OPEN; no paid commitment | BLOCKED | Owner-defined budget ceiling and service/data-processing approvals |
| G2-12 | Privacy, retention, attachments and notification policy | Threat model and ODR-05–07 OPEN | BLOCKED | Explicit retention/deletion/residency, attachment and notification decisions |
| G2-13 | Provider/model data processing | ODR-11 OPEN; replaceable model adapter proposal | BLOCKED | Approved provider terms, data flow and model-processing policy |
| G2-14 | Canonical approval record | G2 pack and decision register are drafts | BLOCKED | Owner-approved canonical Biên bản amendment referencing accepted decisions and evidence |
| G2-15 | Build authorization boundary | G2/G3 explicitly not approved | PASS (control) | Maintain G3 denied until G2 closed and separate G3 authorization is recorded |

## 2. Current readiness summary
- Documentary design artifacts: PRESENT.
- Owner decisions: 12 OPEN.
- Kha Gmail discovery review/receipt: NOT VERIFIED.
- Ka security review/receipt: NOT VERIFIED.
- Approved Core identity/authorization/audit contracts: NOT EVIDENCED.
- Approved W52 dispatch/event and W14 Host contracts: NOT EVIDENCED.
- Synthetic fixtures/code/tests: NOT CREATED / NOT IMPLEMENTED / NOT RUN.
- Independent QE: NOT RUN.
- G2: NOT READY / NOT APPROVED.
- G3 BUILD: NOT AUTHORIZED.
- Gmail OAuth/mailbox: NOT CONNECTED / NOT VERIFIED.
- Gmail-native draft and real send: NOT AUTHORIZED.

## 3. Critical path to G2
1. Obtain and verify Kha's independent Gmail/Google discovery findings and exact scope recommendation.
2. Obtain and verify Ka's independent threat-model and authorization review.
3. Resolve Owner decisions ODR-01–ODR-12 (some may be explicitly deferred with owner and due condition).
4. Obtain approved Core identity, mailbox ownership, authorization and audit contracts.
5. Obtain approved W52 dispatch/event and W14 Host contracts with runtime evidence.
6. Resolve data handling, retention, attachment, model and cost boundaries.
7. Update canonical Biên bản only from explicit Owner decisions; then conduct a final evidence trace and gate review.
8. Keep G3 separate: no code/build until separate G3 authorization.

## 4. How to interpret status
- PASS means evidence is present and meets the stated criterion; it is not inferred from a draft.
- PARTIAL means a design or partial source exists but acceptance evidence is missing.
- BLOCKED means a required decision, approved contract, independent review or operational evidence is absent.
- NOT RUN is not PASS.
- This checklist is a Xu assessment, not independent QE/security approval.

## 5. Immediate safe next action
Continue documentary closure and independent-review preparation. Do not request OAuth, read the demo mailbox, create Gmail drafts, send mail, enable paid services, or implement code under this checklist. The previously nominated demo mailbox remains only a future test target after explicit connection and gate approvals.
