# Work 103 — Controlled Retrieval Experiment V1 (2026-10-28)

## Status

- Experiment runner: executed on GitHub Actions, Python 3.11 and 3.12.
- Run: [40651626739](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/40651626739)
- Code commit: `43bafd1ba0d9da75f1a867b71981b6952d528833`
- Both matrix jobs: SUCCESS; syntax, unit tests, existing labeled-evaluation gate, experiment sweep, and artifact upload all succeeded.
- Results are archived as Actions artifacts:
  - [Python 3.11 results](https://api.github.com/repos/hqtt2026-thevinhvtqni/room-meeting-ai/actions/artifacts/12799198888/zip)
  - [Python 3.12 results](https://api.github.com/repos/hqtt2026-thevinhvtqni/room-meeting-ai/actions/artifacts/12799609388/zip)
- Experiment is evidence only. It does not change the retrieval production defaults, lock `min_score`, open integration, or assert release readiness.

## Protocol

- Same committed corpus (8 source documents), same labeled set (50 answerable + 15 no-answer queries), same chunking (300/40), and top-k=5 across all variants.
- Swept threshold 0.20–0.70 in 0.05 increments per variant.
- Variants: baseline BM25-lite (K1=1.2, B=0.75); conservative NFKC/whitespace query normalization; BM25 parameter variants (0.8/0.5 and 1.6/0.9); lightweight hybrid (75% BM25 score + 25% unique query-token coverage).
- Latency values below are Python 3.11 runner measurements at top-k=5; tiny eight-document corpus means these are directional only, not production capacity benchmarks.
- The hybrid is lexical coverage blending, not embeddings or semantic retrieval.

## Results at selected thresholds

Metrics are computed on the same dataset. Top-1 is an additional exact expected-source metric; Precision@5/Recall@5/MRR are the evaluator metrics. No-answer accuracy is over 15 questions, so one question changes it by 6.67 percentage points.

| Variant | Threshold | Top-1 | Precision@5 | Recall@5 | MRR | Answered rate | No-answer accuracy | Near-miss leaks | Latency ms/query |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline BM25-lite | 0.35 | 1.00 | 0.86 | 0.97 | 1.00 | 1.00 | 0.8667 (13/15) | 2 | 0.024 |
| Baseline BM25-lite | 0.45 | 1.00 | 0.96 | 0.97 | 1.00 | 1.00 | 0.9333 (14/15) | 1 | 0.024 |
| Query normalization | 0.45 | 1.00 | 0.96 | 0.97 | 1.00 | 1.00 | 0.9333 (14/15) | 1 | 0.025 |
| BM25 K1=0.8, B=0.5 | 0.45 | 0.98 | 0.94 | 0.95 | 0.98 | 0.98 | 0.9333 (14/15) | 1 | 0.024 |
| BM25 K1=1.6, B=0.9 | 0.45 | 1.00 | 0.95 | 0.96 | 1.00 | 1.00 | 0.9333 (14/15) | 1 | 0.024 |
| Hybrid 75/25 | 0.50 | 0.98 | 0.95 | 0.95 | 0.98 | 0.98 | 1.00 (15/15) | 0 | 0.155 |

## Findings

1. **Threshold recalibration is the strongest low-cost baseline candidate.** At 0.45, the existing BM25-lite retains top-1=1.00, Recall@5=0.97, MRR=1.00, and answered_rate=1.00; Precision@5 improves from 0.86 to 0.96 and no-answer accuracy improves from 13/15 to 14/15. The ONT near-miss leak disappears, but the revenue/Hanoi near-miss still leaks.
2. **Conservative query normalization is a no-op** on this set: its metrics match the baseline. Do not promote it as an improvement.
3. **BM25 parameter variants do not dominate the baseline.** K1=0.8/B=0.5 slightly improves Precision@5 at 0.35 (0.87 vs 0.86), but at 0.45 loses some top-1/recall/MRR/answered rate. K1=1.6/B=0.9 at 0.45 remains close but is slightly lower on precision/recall than the baseline.
4. **Hybrid at threshold 0.50 abstains on all 15 no-answer queries**, including all 3 near-miss examples. However it also drops answered_rate and top-1 to 0.98 (one answerable query is lost), and latency rises from ~0.024 to ~0.155 ms/query on this tiny corpus. This is a trade-off, not a clear win.
5. The hard case `doanh thu quý 4 của chi nhánh Hà Nội` remains a leak for baseline and BM25 parameter variants even at threshold 0.45. The hybrid abstains at 0.50, but the experiment does not prove generalization beyond these 3 near-miss examples.

## Decision

- **Candidate for next validation:** run an expanded threshold sweep around 0.40–0.48 with the full set, and independently inspect the one answerable query lost by hybrid at 0.50.
- Keep `min_score=0.35` as the existing experimental operating value until a separate decision is documented. Do not silently change the product default to 0.45.
- Do not promote query normalization or BM25 parameter changes based on this experiment.
- Keep hybrid as a research candidate only; investigate why it abstains correctly on the revenue near-miss and which answerable query it rejects.
- Next meaningful quality step is to add more independently labeled near-miss cases, including missing-location/time/branch facts and lexical-overlap distractors. Three near-miss examples are too few for a robust claim.
- Integration remains **BLOCKED / gate CLOSED**. Release remains **NOT PASS**.
