# Work 103 — Labeled Set Quality Audit (50 queries, 2026-10-28)

Per Xu task 02: verify that PASS reflects real quality, not just green tests.
Method: full per-query execution over EVAL_SET v2 at min_score = 0.35,
top_k = 5, chunking 300/40 (logic-equivalent verified run; CI confirms gate).

## Label distribution (expected references per source)
- bien-ban-hop-tuan-ont: 9   nhiem-vu-tuan-42: 9
- quy-trinh-xu-ly-su-co: 8    ke-hoach-giao-hang: 6
- bao-cao-doanh-thu: 6        ky-luat-hop: 6
- bao-mat-thong-tin: 6        quy-dinh-cong-tac: 6
All 50 expected references point to committed documents (schema-validated;
duplicate/unknown refs are rejected by tests).

## Answerable queries (50)
- TOP-1 CORRECT: 50/50 — the expected source ranks first for every query.
- ALL EXPECTED IN TOP-5: 47/50 — three multi-expectation queries rank one
  expected source below the top-5 window.
- PRECISION@5 = 0.86: 16/50 queries return related-but-unexpected documents
  alongside the expected one. Examples (top-1 always correct):
  - "hạn chót xử lý sự cố ngày nào" -> expected ONT minutes; also returns
    quy-trinh-su-co (top-2, score 0.369 vs 0.683). Plausible related doc,
    acceptable for evidence context, but shows top-5 window carries noise.
  - "tiếp nhận ticket từ khách hàng" -> also returns ke-hoach-giao-hang
    (shares "khách hàng").
- Verdict: ranking quality is real; precision loss comes from legitimately
  related documents sharing vocabulary — a candidate for improvement
  (query normalization / scoring variants) in task 03.

## No-answer queries (15)
- EASY: 12/12 correctly abstain (all far from corpus vocabulary).
- NEAR-MISS: 1/3 abstains ("đặt vé máy bay đi Đà Nẵng du lịch"), 2/3 LEAK:
  1. "tín hiệu quang ONT khu C mạnh bao nhiêu dBm" -> bien-ban-hop-tuan-ont,
     score 0.355 — BARELY above the 0.35 threshold. This leak is
     threshold-sensitive: a slightly higher threshold (0.40) abstains it.
  2. "doanh thu quý 4 của chi nhánh Hà Nội" -> bao-cao-doanh-thu, score 0.512.
     Vocabulary overlap ("doanh thu", "quý", "chi nhánh") but the answer
     (Hanoi branch Q4 revenue) does not exist. Threshold-robust leak.
- Verdict: no_answer_accuracy = 13/15 = 86.7% is the honest current state.
  Leak #2 is the true unsolved case; leak #1 may be partially addressed by
  threshold recalibration — but recalibration must be re-swept against the
  full set, not tuned for one query (see task 03 protocol).

## Conclusions
1. PASS reflects genuine ranking quality (50/50 top-1, no false abstention).
2. Two concrete weaknesses are identified and quantified, not hidden:
   precision@5 = 0.86 (related-doc noise) and near-miss abstention 1/3.
3. These numbers are the BASELINE for the controlled improvement experiment
   (task 03). Any proposed variant must beat them on the SAME labeled set
   with no-answer behavior and latency reported.
