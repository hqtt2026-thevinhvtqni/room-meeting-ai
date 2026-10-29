# WORK 103 — Evidence-Support Stage Design Proposal V1

- Author: Ka | CSA / Independent Reviewer
- Date: 2026-10-29 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Decision type: **PROPOSAL FOR REVIEW ONLY — NOT IMPLEMENTED**
- Status: **DESIGN REVIEW REQUIRED; no release approval**
- Inputs: Manifest V4 benchmark fixture, Ka adjudicated labels V3 (immutable), corpus-aligned failure report, and no-answer leak analysis supplied from the working tree.
- Scope: Work 103 retrieval prototype only. No Core :8000, MCP :8020, production corpus, or Dashboard changes.

## 1. Problem statement

The fixed corpus-aligned benchmark reproduces these results at `min_score=0.35`: Hit@5=0.950, Precision@5=0.880, Recall@5=0.950, MRR=0.9375, answered rate=0.975, and strict no-answer accuracy=0.300 against a floor of 0.800. Threshold sweeps do not satisfy both answerable retrieval and abstention floors.

The leak analysis identifies lexical collisions between answerable and no-answer queries over shared sources. Q008, Q035, and Q010 remain leaks at threshold 0.45; raising the threshold harms answerable queries. This proposal therefore closes threshold-only tuning as the primary remediation path. It does not claim the source itself proves absence merely because a lexical match was returned.

## 2. Proposed separation of responsibilities

1. **Candidate retrieval (existing prototype):** return ranked chunks with stable source ID, chunk ID, exact line range, score, and index snapshot. Retrieval score indicates relevance only; it must not imply answer support.
2. **Evidence-support assessment (new, separately gated stage):** assess whether the retrieved spans entail an answer to the exact query, contradict it, explicitly document that the requested detail is unspecified, or fail to establish any of these.
3. **Answer/abstention policy:** allow an answer only when support is sufficient and the evidence is traceable. Otherwise abstain with a typed reason. A high lexical score alone is never sufficient.
4. **Citation serialization:** citations must refer only to exact retrieved spans that passed the support assessment. Never fabricate source IDs, line ranges, or quotations.

The support assessment must be a separate module/interface with independent tests. It must not silently alter the ranker, labels, corpus, or current strict benchmark metric.

## 3. Proposed result contract (draft)

```json
{
  "query_id": "Q008",
  "decision": "INSUFFICIENT_EVIDENCE",
  "answer_permitted": false,
  "reason_code": "PROCESS_NOT_ESTABLISHED",
  "evidence": [
    {
      "source_id": "00_CORPUS/sales.md",
      "chunk_id": "stable-chunk-id",
      "start_line": 1,
      "end_line": 2,
      "relation": "RELATED_BUT_NOT_SUPPORTING"
    }
  ],
  "unsupported_subquestions": ["What is the process for changing a delivery schedule?"],
  "index_snapshot": "fixture-pinned-id",
  "support_policy_version": "evidence-support-v1"
}
```

This is an illustrative contract, not an observed output. Exact field names and allowed values require architecture review before implementation.

Required decisions:
- `SUPPORTED`: direct, traceable evidence answers the requested proposition.
- `CONTRADICTED`: traceable evidence explicitly conflicts with the requested proposition.
- `EXPLICITLY_UNSPECIFIED`: source text explicitly establishes that the requested detail is not specified, with the scope of that statement clear.
- `INSUFFICIENT_EVIDENCE`: no adequate support, contradiction, or scoped absence evidence was established.
- `CONFLICTING_EVIDENCE`: approved spans materially disagree; abstain pending resolution.

Do not equate `INSUFFICIENT_EVIDENCE` with proof that information does not exist. Do not equate topical relevance with support.

## 4. Required safeguards

- **Closed evidence set:** the stage may inspect only the pinned, approved fixture/source snapshot; no web search, external memory, or unapproved documents.
- **Exact provenance:** preserve source ID, chunk ID, start/end lines, corpus hash, index snapshot and policy version through the decision.
- **Question decomposition:** assess each material sub-question separately; an answer is permitted only when all material claims are supported.
- **Negation and scope:** distinguish “this source does not mention X” from “X does not exist”; do not generalize a local absence statement to the entire corpus.
- **No-answer handling:** a non-empty retrieval may still correctly lead to abstention. A retrieved span counts as absence evidence only if it explicitly and appropriately scopes the missing-detail statement.
- **Fail closed:** missing spans, malformed provenance, conflicting evidence, unsupported claims, or verifier exceptions produce abstention, never an optimistic answer.
- **No silent label changes:** labels V3 remain immutable. Any adjudication change requires a new version, rationale, reviewer and hashes.
- **No metric substitution:** retain strict `no_answer_accuracy` and all existing floors. Report any support-aware metric separately until independently approved.

## 5. Review cases from the current fixture

| Case | Known risk | Required behavior |
|---|---|---|
| Q008 — delivery schedule change process | `sales.md` mentions confirming a delivery schedule but does not establish a change procedure | Abstain with `INSUFFICIENT_EVIDENCE`, unless a precise approved span explicitly answers the procedure |
| Q010 — storage location of schedules | lexical collision with sales source content | Do not infer a storage location from schedule-related text |
| Q035 — whether “Customer A” has an order | customer/order vocabulary overlap | Do not infer a real order or customer record from generic sales process text |
| Q004 — RX power threshold | a source may explicitly say a threshold is unspecified | Use `EXPLICITLY_UNSPECIFIED` only if the exact span and scope warrant it |
| Q044 — default retrieval score | topical/technical overlap may be mistaken for a numeric configuration value | Do not manufacture a default; cite only explicit configuration evidence |
| Q025 / Q032 | near-threshold vocabulary collisions | Preserve abstention when support is absent; do not expand the absence mapping merely to improve a metric |
| Q037 — AI caller output | possible multi-source evidence / label ambiguity | Keep V3 unchanged; adjudicate only in a new version before using it as a release case |

Q008's grounded-absence classification is explicitly **borderline**. This proposal does not certify it as a correct absence example.

## 6. Validation plan before implementation approval

### Gate A — contract and fixture
- Freeze the input fixture and source hashes used for this experiment.
- Add an explicit expected-support-decision dataset separate from retrieval labels. Each row must include query, expected decision, approved source span(s), rationale, and reviewer.
- Have an independent reviewer adjudicate borderline cases, especially Q008 and Q037. Do not count the original blind-label process as verified.

### Gate B — component tests
- Supported paraphrase with exact citation.
- Related but non-answering source must abstain.
- Explicitly unspecified value with correct scope.
- Negation, contradiction, multiple sub-questions and conflicting spans.
- Empty retrieval, missing source, invalid line range, corrupted provenance, and verifier exception all fail closed.
- Reordering candidates or changing irrelevant chunks must not invent support.

### Gate C — end-to-end fixture evaluation
- Run retrieval and support assessment separately and together on the same immutable fixture.
- Preserve all existing retrieval floors and strict no-answer gate.
- Report answerable false-abstentions, unsupported-answer leaks, supported-answer accuracy, citation-span validity, contradiction handling, latency, and per-query traces.
- No threshold or label changes during comparison. No release PASS unless every pre-approved floor is met in reproducible CI.

### Gate D — architecture integration review
- Review the module contract before connecting it to Core.
- If later approved, Core owns application semantics and canonical-data access; MCP :8020 remains an adapter/delegator and must not read storage directly.
- No live MCP :8020 → Core :8000 → retrieval → source-readback test is authorized by this proposal. E2E remains CLOSED until the offline gate passes and a separate integration decision is recorded.

## 7. Non-goals and explicit exclusions

- No vector database, embedding model, external model API, or paid dependency in this proposal.
- No changes to `rag_retrieval.py`, `rag_eval.py`, baseline thresholds, fixture, labels V3, or Qw V5.
- No Core/MCP changes, no production corpus approval, no merge, no release certification.
- No claim that this design alone will pass the benchmark. It requires implementation, independent review and reproducible evidence.

## 8. Decision requested from architecture/review

Review only these questions:
1. Is the five-state decision vocabulary sufficient and unambiguous?
2. What is the minimum accepted evidence unit: exact line span, claim/span pair, or both?
3. Which component owns the support assessment, and what contract crosses the Core boundary?
4. What independent adjudication process and thresholds are required for the support dataset?
5. What release floors should apply to unsupported-answer leakage and citation validity without weakening existing gates?

Until those questions are reviewed, status remains **PROPOSAL ONLY / BLOCKED FOR IMPLEMENTATION**.

— Ka | CSA / Independent Reviewer
