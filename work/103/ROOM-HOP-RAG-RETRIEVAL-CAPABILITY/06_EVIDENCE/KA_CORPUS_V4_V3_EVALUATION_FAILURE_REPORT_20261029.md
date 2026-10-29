# WORK 103 — Manifest V4 / Ka V3 Evaluation Failure Report

- Reviewer: Ka (CSA / Independent Reviewer)
- Date-time: 2026-10-29 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Evaluation commit: `5c85f5fac442074a300569bb33e283792db0441a`
- CI run: [GitHub Actions #41](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40798293268)
- Decision: **FAIL baseline / Work 103 remains ACTIVE-BLOCKED**.

## 1. Fixture and execution provenance

The new evaluation fixture is `05_TEST/EVAL_SET_CORPUS_V4_V3.json`. GitHub readback confirms:
- 6 embedded source documents: five domain/policy files and the architecture document.
- 40 ANSWERABLE queries and 10 NO_ANSWER queries derived from `KA_ADJUDICATED_LABELS_50_QUERIES_V3_20261029.json`.
- Canonical adjudicated-label dataset SHA-256: `4a1e11221f623030fc95632fa39b386eb7612e5ead244693b1d7c171d7089fa5`.
- The eval harness now accepts `--eval-set`; CI runs this fixture as a separate gate without replacing the existing synthetic benchmark.

GitHub Actions #41 ran on Python 3.11 and 3.12. Syntax compile and both unit-test groups passed; the old synthetic `EVAL_SET.json` gate passed. The new corpus-aligned gate failed on both Python versions. The controlled experiment step was skipped because the gate exits non-zero.

## 2. Operating threshold 0.35 — measured result

| Metric | Actual | Baseline | Result |
|---|---:|---:|---|
| Hit@5 | 0.775 | 0.900 | FAIL |
| Precision@5 | 0.754 | 0.800 | FAIL |
| Recall@5 | 0.775 | 0.900 | FAIL |
| MRR | 0.775 | 0.900 | FAIL |
| Answered rate | 0.800 | 0.900 | FAIL |
| No-answer accuracy | 0.500 | 0.800 | FAIL |

The evaluator reported 9 answerable-query misses, including false abstentions, and 5 no-answer leaks (3 easy, 2 near-miss).

## 3. Threshold trade-off — no valid operating point found

| min_score | Hit@5 | Precision@5 | Recall@5 | MRR | Answered rate | No-answer accuracy |
|---:|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.900 | 0.798 | 0.900 | 0.887 | 0.925 | 0.400 |
| 0.35 | 0.775 | 0.754 | 0.775 | 0.775 | 0.800 | 0.500 |
| 0.45 | 0.600 | 0.579 | 0.600 | 0.600 | 0.600 | 0.800 |

No tested threshold satisfies all six baseline floors. Lowering the threshold improves retrieval coverage but substantially worsens no-answer accuracy; raising it improves abstention but causes unacceptable false abstentions. **Do not change baseline thresholds or tune the fixture just to make CI green.**

## 4. Failure examples to investigate

### Answerable misses / false abstentions
- Q027 — “Điều gì xảy ra nếu top_k được đặt là 0 hoặc số âm?” Expected `00_CORPUS/architecture.md`.
- Q036 — “Luồng dữ liệu RAG bắt đầu từ đâu và đi qua những thành phần nào?” Expected `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`.
- Q037 — “AI caller nhận được gì từ RAG retrieval?” Expected `00_CORPUS/architecture.md`.
- Q040 — “Có thể sử dụng RAG để tự động xóa tệp trên ổ đĩa không?” Expected `00_CORPUS/security.md`.
- Q041–Q043 — chunk metadata and line-range questions, expected `00_CORPUS/architecture.md`.
- Q045 — `rag_get_context` fields, expected `00_CORPUS/architecture.md`.
- Q047 — responsibility for independent blind-label review, expected `00_CORPUS/evidence.md`.

These misses suggest the lexical retrieval baseline struggles with Vietnamese phrasing, technical identifiers, negation/implicit safety questions, and chunk-level score thresholds. Each query must be inspected against retrieved chunks and exact source spans before changing ranking behavior.

### No-answer leaks
- Q008 — process for changing a cement delivery schedule.
- Q010 — where delivery schedules are stored.
- Q035 — whether “Customer A” has an order.
- Q004 — a concrete normal RX power threshold.
- A technical near-miss asking the default minimum score.

The first three share terms with the sales corpus but request details that are explicitly absent. The last two share terms with sources that discuss the subject without supplying the requested value. A lexical overlap score alone does not reliably distinguish topic overlap from answer support.

## 5. Required remediation plan

1. Preserve this failing run as baseline evidence.
2. Add per-query diagnostic output: expected source, retrieved source IDs/chunk IDs/scores, and abstention reason; do not expose private or unrestricted filesystem content.
3. Review each miss/leak against the immutable V3 labels and exact source spans. If a label is wrong, issue a new adjudication version; never edit Qw V5 or silently rewrite V3.
4. Test candidate retrieval changes on this same frozen fixture and compare all six metrics plus the exact error list. Keep the synthetic benchmark as a separate regression suite.
5. Accept a new threshold only if all gates pass on the fixed fixture and the result is reproduced in CI. If no threshold satisfies both answerability and abstention, consider an evidence-support/answerability stage as a separately scoped extension; do not call it a lexical retrieval PASS.
6. Keep live MCP :8020 → Core :8000 → retrieval → source-readback gate closed until an actual end-to-end run is captured.

## Decision

**Corpus-aligned retrieval baseline: FAIL.** Unit tests and the legacy synthetic benchmark pass, but neither result overrides this failure. Work 103 stays **ACTIVE / BLOCKED**. No production corpus approval, blind-process certification, final freeze, or live RAG E2E PASS is granted.

— Ka | CSA / Independent Reviewer
