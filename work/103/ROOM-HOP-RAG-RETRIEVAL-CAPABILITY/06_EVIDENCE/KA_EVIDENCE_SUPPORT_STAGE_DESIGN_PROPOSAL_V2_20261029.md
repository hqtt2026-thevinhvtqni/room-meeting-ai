# WORK 103 — Evidence-Support Stage Design Proposal V2 (Contract Completion)

- Author: Ka | CSA / Independent Reviewer (contract completed under Auto-completion authorization from Xu/Vinh, 2026-10-29)
- Date: 2026-10-29 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Supersedes: `KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V1_20261029.md` (V1 remains on branch; nothing in V1 is deleted)
- Decision type: **PROPOSAL FOR REVIEW ONLY — NOT IMPLEMENTED**
- Status: **DESIGN CONTRACT COMPLETE; REVIEW REQUIRED; no release approval**
- Scope: Work 103 retrieval prototype only. No Core :8000, MCP :8020, production corpus, or Dashboard changes.
- Immutables preserved: labels V3, fixture freezes V1/V2, all baseline thresholds, Qw V5.

## 1. What V2 adds over V1

V2 completes the contract gaps identified in the V1 review exchange (Xu + Ka + Vinh, 2026-10-29):

1. A locked disambiguation rule between `EXPLICITLY_UNSPECIFIED` and `INSUFFICIENT_EVIDENCE`.
2. A mandatory, individually-gated test-case suite T1–T7, extending Ka's T1–T5 with target labels, the missing `CONTRADICTED` and `CONFLICTING_EVIDENCE` cases, and a locked target decision for the scope-mismatch case.
3. An independence requirement: the support assessment must not reuse the lexical retrieval score as a support signal.
4. Per-case metric reporting: no aggregate score may hide a failing case.
5. A label-coverage audit requirement: labels V3 carry only `ANSWERABLE`/`NO_ANSWER` and therefore cannot measure five-state decisions; a separate expected-support-decision dataset is required (Gate A), with V3 untouched.

V2 does not implement anything, does not change any gate, and does not claim any metric improvement.

## 2. Locked disambiguation rule (contract-lock)

| State | Mandatory condition | Behavior |
|---|---|---|
| `EXPLICITLY_UNSPECIFIED` | A specific, retrievable source span explicitly states that the requested detail is not specified within that source's scope, AND the query scope is within the source's scope | Answer permitted ONLY as a scope-limited conclusion citing the exact span |
| `INSUFFICIENT_EVIDENCE` | No adequate support, contradiction, or scoped absence statement was established | Abstain; must NOT assert that the information does not exist |

Locked principles:

- Absence of retrieval results is NOT evidence that the document confirms "not specified". (T1 vs T2)
- A statement "this document does not specify X" is NOT evidence that X is unspecified across the whole corpus or system. (T4)
- Retrieval score is NEVER a support signal. High lexical score with non-answering content must still abstain. (T3)

## 3. Mandatory test-case suite T1–T7 (each case gated individually)

| Case | Scenario | Required decision | Required behavior |
|---|---|---|---|
| T1 | Explicit absence statement retrieved; query scope matches source scope (e.g., source states the RX threshold is not specified) | `EXPLICITLY_UNSPECIFIED` | Scope-limited answer permitted, with exact citation of the span |
| T2 | Same query, but the chunk containing the absence statement is NOT retrieved | `INSUFFICIENT_EVIDENCE` | Abstain; no "not specified" claim from an unseen span |
| T3 | Retrieved results are topically related but do not answer the question (schedule confirmation text, no change procedure) | `INSUFFICIENT_EVIDENCE` | Abstain despite non-empty retrieval; the support layer must not reuse the lexical score as a support signal |
| T4 | Scope mismatch: source A states "not specified in document A", query scope exceeds document A | `EXPLICITLY_UNSPECIFIED` ONLY IF the pipeline can emit a scope-limited answer citing document A; otherwise MUST fall back to `INSUFFICIENT_EVIDENCE` (fail-closed) | Never generalize a local absence statement to the corpus |
| T5 | Metadata/provenance invalid: missing source, wrong lines, unverifiable chunk, or verifier exception | `INSUFFICIENT_EVIDENCE` (fail-closed variant) | Never answer; typed reason code; no fabricated provenance |
| T6 | Two approved spans assign different values to the same requested fact | `CONFLICTING_EVIDENCE` | Abstain; must NOT resolve by picking the higher-scored span |
| T7 | An approved span directly negates the query's proposition | `CONTRADICTED` | Abstain from the affirmative answer; report the contradiction with exact citation |

Case T4's target label is now LOCKED (it was undefined in the review exchange): `EXPLICITLY_UNSPECIFIED` is admissible only with a scope-limited answer; otherwise the only permitted outcome is `INSUFFICIENT_EVIDENCE`. Implementations unable to express scope-limited answers must fail closed.

## 4. Independence requirement (T3 dependency, locked)

- The support assessment consumes retrieved candidates as (source_id, chunk_id, line range, text) and must derive its decision from the span content and provenance only.
- The retrieval score may inform candidate ORDER only; it must not appear in, weight, or short-circuit the support decision.
- If the same lexical signal is used for both ranking and support, T3 must fail by construction; such a design failure must surface at review, not at implementation time.

## 5. Per-case measurement (no aggregate hiding)

- Each case T1–T7 is reported as pass/fail individually in Gate B.
- No composite "support score" may replace per-case results; a single failing case blocks implementation approval.
- Gate C additionally reports, separately: answerable false-abstentions, unsupported-answer leaks, supported-answer accuracy, citation-span validity, contradiction handling, latency, per-query traces.
- The existing strict `no_answer_accuracy` floor and all retrieval floors remain in force, unchanged.

## 6. Label-coverage audit (dataset requirement, locked)

- Labels V3 (`work103.adjudicated-labels.v3`) contain only `ANSWERABLE`/`NO_ANSWER`; they cannot adjudicate five-state decisions and must not be edited or version-bumped for this purpose.
- Gate A requires a NEW expected-support-decision dataset, separate from retrieval labels, with per-row: query, expected decision, approved source span(s) with exact lines, rationale, and an independent reviewer.
- Borderline cases (Q008, Q037) require independent adjudication within the new dataset before any release use.
- Coverage requirement: the new dataset must include at least one case for each of the five decisions and for every case T1–T7.

## 7. Gates A–D

Unchanged from V1 (see V1 sections 6): Gate A contract/fixture, Gate B component tests (now mandatory cases T1–T7), Gate C end-to-end fixture evaluation, Gate D architecture integration review. E2E MCP :8020 → Core :8000 remains CLOSED until offline gates pass and a separate integration decision is recorded.

## 8. Non-goals and exclusions

Unchanged from V1: no vector DB, embeddings, external model APIs, or paid dependencies; no changes to `rag_retrieval.py`, `rag_eval.py`, thresholds, fixture, labels V3, or Qw V5; no Core/MCP changes; no merge; no release certification; no claim that this design passes any benchmark.

## 9. Status

- This document completes the design CONTRACT for review. It is NOT implemented, NOT tested, and NOT approved.
- Work 103 remains **ACTIVE / BLOCKED**: corpus-aligned strict no-answer gate still FAIL; E2E still CLOSED.
- Next required step: independent architecture review of this contract (V1 section 8 questions plus the V2 locks in sections 2–6), then Gate A dataset construction.

— Ka | CSA / Independent Reviewer
