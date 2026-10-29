# WORK 103 — Manifest V4 / Ka V3 Evaluation Failure Report

- Reviewer: Ka (CSA / Independent Reviewer)
- Date-time: 2026-10-29 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- CI baseline run: [GitHub Actions #41](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40798293268)
- Latest diagnostic run: [GitHub Actions #43](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40798530306)
- Decision: **FAIL baseline / Work 103 remains ACTIVE-BLOCKED**.

## 1. Fixture and provenance

`05_TEST/EVAL_SET_CORPUS_V4_V3.json` contains six source documents, 40 ANSWERABLE queries, and 10 NO_ANSWER queries derived from `06_EVIDENCE/KA_ADJUDICATED_LABELS_50_QUERIES_V3_20261029.json`. Canonical label dataset SHA-256: `4a1e11221f623030fc95632fa39b386eb7612e5ead244693b1d7c171d7089fa5`.

The evaluation harness accepts `--eval-set`; CI runs the corpus-aligned fixture as a separate gate without replacing the existing synthetic benchmark. Run #41 and #43 both show Python 3.11/3.12 syntax compilation and unit tests PASS, the old synthetic benchmark PASS, and the new corpus-aligned gate FAIL.

## 2. Operating threshold 0.35

| Metric | Actual | Baseline | Result |
|---|---:|---:|---|
| Hit@5 | 0.775 | 0.900 | FAIL |
| Precision@5 | 0.754 | 0.800 | FAIL |
| Recall@5 | 0.775 | 0.900 | FAIL |
| MRR | 0.775 | 0.900 | FAIL |
| Answered rate | 0.800 | 0.900 | FAIL |
| No-answer accuracy | 0.500 | 0.800 | FAIL |

The evaluator reports nine answerable-query misses/false abstentions and five no-answer leaks (three easy, two near-miss).

## 3. Threshold trade-off

| min_score | Hit@5 | Precision@5 | Recall@5 | MRR | Answered rate | No-answer accuracy |
|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.900 | 0.798 | 0.900 | 0.887 | 0.925 | 0.400 |
| 0.35 | 0.775 | 0.754 | 0.775 | 0.775 | 0.800 | 0.500 |
| 0.45 | 0.600 | 0.579 | 0.600 | 0.600 | 0.600 | 0.800 |

No tested threshold satisfies all six floors. Lower thresholds improve retrieval coverage but worsen no-answer accuracy; higher thresholds improve abstention but cause unacceptable false abstentions. Do not change baselines or tune the fixture just to make CI green.

## 4. Representative failures

Answerable misses include:
- Q027: top_k zero/negative handling; expected `00_CORPUS/architecture.md`.
- Q036: RAG data flow; expected `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`.
- Q037: AI caller output; expected `00_CORPUS/architecture.md`.
- Q040: whether RAG can delete files; expected `00_CORPUS/security.md`.
- Q041–Q043: chunk metadata and line ranges; expected `00_CORPUS/architecture.md`.
- Q045: `rag_get_context` fields; expected `00_CORPUS/architecture.md`.
- Q047: responsibility for independent blind-label review; expected `00_CORPUS/evidence.md`.

No-answer leaks include:
- Q008: process for changing a cement delivery schedule.
- Q010: where delivery schedules are stored.
- Q035: whether “Customer A” has an order.
- Q004: concrete normal RX power threshold.
- A near-miss asking the default minimum retrieval score.

The failures indicate that lexical overlap alone struggles with Vietnamese phrasing, technical identifiers, implicit/negative safety questions, and distinguishing topic overlap from evidence that answers the question. Inspect exact retrieved chunk IDs and scores before changing ranking behavior.

## 5. Remediation

1. Preserve the failing run as baseline evidence.
2. Capture per-query diagnostics (expected source, retrieved source/chunk IDs, line ranges, scores and abstention reason) without including full document text in CI logs.
3. Review every miss/leak against the immutable V3 labels and source spans. If a label is wrong, issue a new adjudication version; do not edit Qw V5 or silently rewrite V3.
4. Test retrieval changes on the same fixture and compare all six metrics plus the error list. Keep the synthetic benchmark separate.
5. Accept a threshold only if all gates pass on the fixed fixture and CI reproduces the result. If lexical retrieval cannot meet both answerability and abstention requirements, propose a separately scoped evidence-support stage rather than claiming lexical retrieval PASS.
6. Keep live MCP :8020 → Core :8000 → retrieval → source-readback CLOSED until an actual end-to-end run is captured.

## Diagnostic instrumentation

Per-query miss and no-answer diagnostics have been added to `04_CODE/rag_eval.py`; the current workflow invocation uses `--diagnostics`. Run #43 was created from the preceding code commit, so its logs did not include that later workflow argument. A subsequent run must verify that diagnostics are present. Instrumentation does not change ranking, labels, thresholds, or verdicts.

## Decision

**Corpus-aligned retrieval baseline: FAIL.** Unit tests and the legacy synthetic benchmark pass, but neither overrides this failure. Work 103 stays **ACTIVE / BLOCKED**. No production corpus approval, blind-process certification, final freeze, or live RAG E2E PASS is granted.

— Ka | CSA / Independent Reviewer


## Follow-up experiment — query normalization and weighted aliases

- Changes tested: query-only Vietnamese/English grammatical stopword filtering and a small weighted bilingual alias map for terms such as “luồng dữ liệu” / “data flow”, “xóa tệp” / “execute commands”, and line-range metadata.
- CI: [run #49](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40799030826), both Python versions pass unit tests but the corpus-aligned gate still fails.
- At the existing operating threshold 0.35: Hit@5=0.950, Precision@5=0.880, Recall@5=0.950, MRR=0.9375, answered rate=0.975. These five metrics now meet their floors, but strict no-answer accuracy is only 0.300 and fails.
- Sweep trade-off: at 0.45, no-answer accuracy rises only to 0.700 while Hit@5=0.875, Recall@5=0.875, MRR=0.863 and answered rate=0.900 fall below floors. No tested threshold passes the full gate.
- This is an experiment, not a PASS. Do not merge the retrieval prototype into Core based on answerable-query scores alone.

### Label-review candidate (not silently changed)

Q037 asks what the AI caller receives from RAG retrieval. The RAG architecture source explicitly describes an authorized AI caller receiving a grounded answer with citations/abstention, while V3 currently lists only `00_CORPUS/architecture.md` as the expected source. Ka flags this as a candidate for multi-source adjudication, but V3 remains immutable pending a separately versioned label decision.

### Interpretation caution

The strict no-answer metric counts every non-empty retrieval as a leak. For Q004 (RX threshold), Q008 (delivery-schedule change process), and Q044 (default score), the retrieved topic source also explicitly says the requested detail is not specified. That source can support a grounded abstention rather than an unsupported answer. Preserve the strict metric for comparability, but add a separately named grounded-abstention metric before using this benchmark for a release decision; do not silently redefine the existing metric.


## Grounded-abstention diagnostic added

A report-only script, `05_TEST/grounded_abstention_eval.py`, now compares strict empty-retrieval accuracy with a separately named grounded-abstention measure. It credits retrieval only when all returned sources are explicitly annotated as evidence that the requested detail is unspecified. It does not modify labels, ranking, the existing `no_answer_accuracy` gate, or baseline thresholds. CI runs this diagnostic before the strict corpus-aligned gate and prints the result for review.


## Supplemental grounded-abstention run — CI #54

- [GitHub Actions run #54](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40799292123) executed the report-only grounded-abstention analysis before the strict gate.
- At threshold 0.35: strict empty-retrieval accuracy = 0.300; grounded no-answer accuracy = 0.600.
- At threshold 0.45–0.60: grounded no-answer accuracy = 0.800, but the answerable-query sweep is below baseline (at 0.45: Hit@5=0.875, Recall@5=0.875, MRR=0.863, answered rate=0.900).
- Thus, even the supplemental interpretation does not yield a threshold that satisfies both answer retrieval and no-answer behavior. The strict gate remains unchanged and fails. The diagnostic mapping is an explicit reviewer interpretation and must be independently reviewed before being used for any release gate.
- Run #54: unit tests PASS on Python 3.11/3.12; corpus-aligned strict gate FAIL on both.


## Follow-up: per-query no-answer leak analysis

The reproduced seven-leak analysis is recorded in [KA_NO_ANSWER_LEAK_ANALYSIS_20261029.md](KA_NO_ANSWER_LEAK_ANALYSIS_20261029.md). The main conclusion is that threshold-only tuning has no tested setting satisfying both answerable retrieval and strict no-answer floors. Q008 remains a borderline grounded-absence case and must not be credited without independent exact-span review.

The separately scoped response is documented in [KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V1_20261029.md](KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V1_20261029.md). It is proposal-only; no implementation or architecture approval is granted. Fixture, retrieval/evaluator code, thresholds, and labels V3 remain unchanged.
