# WORK 103 — GATE C SEED: EVIDENCE-SUPPORT CORPUS DIAGNOSTIC (REPORT-ONLY, FULL 50-QUERY COVERAGE)

- **Producer:** Vibe (GLM 5.3 via Vibe Work agent), 2026-11-09, under the full build authority granted by Vinh in the Work 103 coordination conversation (2026-11-08: "giao toàn quyền cho vibe xây dựng tiếp, chủ động khi cần phối hợp thì báo").
- **Scope:** Sandbox prototype diagnostic only. No Core :8000, MCP :8020, dashboard or runtime integration; labels V3, fixture freezes, baseline thresholds, Qw V5, rag_retrieval.py and rag_eval.py untouched; no existing gate weakened, reordered or removed.
- **Status:** REPORT-ONLY diagnostic (Gate C seed). All fact-spec decisions are AUTHORED and PENDING INDEPENDENT ADJUDICATION (Ka, DEBT-ES-02). No gate or release claim is made from these numbers.

## 1. Artifacts

| Artifact | Path | Role |
|---|---|---|
| Corpus eval harness | `04_CODE/rag_evidence_support_corpus_eval.py` | Runs the real retrieval pipeline (RetrievalIndex, BM25-lite) at the fixture operating point (top_k=5, min_score=0.35, chunking 300/40), feeds retrieved spans to `assess_support`, reports five-state decision + diagnostic category per query. Report-only: exit 0 on outcomes, exit 1 only on validation errors. |
| Fact specs V1 | `05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json` | 22 rows (12 answerable + 10 no-answer), authored 2026-11-08, adjudication-scoped set. |
| Fact specs V2 | `05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V2.json` | 50 rows — FULL coverage of EVAL_SET_CORPUS_V4_V3.json (40 answerable + 10 no-answer). V1 rows carried unchanged; 28 answerable rows added; no V1 row modified. |
| Unit tests | `05_TEST/test_rag_evidence_support_corpus_eval.py` | Spec/fixture validation, taxonomy, end-to-end mini pipeline, CLI exit-code discipline. |
| CI step | `.github/workflows/work-103-rag-ci.yml` | "Evidence-support corpus diagnostic" step runs the harness on BOTH V1 and V2 before the baseline and independent gates; per-row GitHub annotations limited to non-MATCH rows (GitHub caps annotations). |

## 2. Method (honesty note)

The build environment executes TypeScript, not Python. Before writing the Python, the full two-stage pipeline (line chunking, BM25-lite scoring with QUERY_STOPWORDS/QUERY_EXPANSIONS, and the five-state `assess_support` precedence chain) was ported to TypeScript and executed over all 50 queries. The simulation predicted exactly: 49 MATCH, 0 NO_ANSWER_LEAK, 0 FALSE_ABSTENTION, 1 CONTRADICTION_MISSED (Q040, zero retrieved candidates). CI then reproduced the identical summary (see section 4). CI is the binding verification.

## 3. Findings (CI-verified, run 42559810631, head e66d3716)

- **V2 summary:** `specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0`
- **V1 summary:** `specs=22 match=21 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0`
- **The headline result:** with the evidence-support stage behind unchanged lexical retrieval, ALL 10 adjudicated no-answer queries now resolve without a single affirmative leak (Q004/Q008 via scoped absence statements -> EXPLICITLY_UNSPECIFIED; Q010/Q025/Q032/Q035/Q044 fail closed on retrieved-but-unmatched spans -> INSUFFICIENT_EVIDENCE/NO_ADEQUATE_SUPPORT; Q016/Q030/Q046 retrieve nothing at the operating threshold -> NO_CANDIDATES). This is the seeded remediation path for the failing independent gate (no_answer_accuracy=0.300 vs floor 0.8), which itself remains UNCHANGED and still fails.
- **Answerable side undamaged:** 39/40 answerable queries reach their authored ideal decision (36 SUPPORTED + 3 CONTRADICTED via negation spans). No false abstentions.
- **Q040 CONTRADICTION_MISSED is a retrieval miss, not a support-stage defect:** lexical retrieval returns ZERO candidates for Q040 at min_score 0.35, so the negating span ("Retrieval không cấp quyền thực thi lệnh") is never seen by the support stage. Recorded against the retrieval-side debt family (DEBT-ES-06); the support stage can only contradict what retrieval surfaces.
- **Citation-source divergence (candidate Gate C metric):** Q037/Q045 match spans in `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md` while the fixture's expected source is `00_CORPUS/architecture.md` (duplicate-content corpus). The harness scores decisions only; citation-source alignment is NOT yet measured and is recorded as a candidate Gate C addition (DEBT-ES-08).
- **Taxonomy fix found by CI:** `CONFLICTING_EVIDENCE` on an answerable query is a distinct ideal-mismatch (evidence found, values conflict), NOT an abstention. `ABSTAIN_FAMILY` was corrected to (EXPLICITLY_UNSPECIFIED, INSUFFICIENT_EVIDENCE); run #92 failed on exactly this expectation before the fix.

## 4. CI execution history

- Commit `910316f4` (2026-11-09 02:34 UTC): initial harness + V1 specs (22 rows) + tests + CI step.
- Commit `bdbcffcb`: mini-fixture leak-test fix (leak pattern must match text actually retrieved by the no-answer query).
- Commit `01042798`: annotation-echo for unit-test failures; **run 42467375198-era pattern repeated: run #92 (42552053676) FAILED** — one unit test exposed the CONFLICTING_EVIDENCE/ABSTAIN_FAMILY taxonomy bug.
- Commit `d9635f4a`: taxonomy fix + fact specs V2 (full 50-query coverage) + CI runs both spec sets. **Run 42559743132:** py_compile, ALL FOUR unit suites, Gate B decision-set step, corpus diagnostic (V1+V2), EVAL_V2 baseline and grounded-abstention diagnostic PASS on Python 3.11 AND 3.12; the Manifest V4 + Ka V3 independent gate still FAILS (no_answer_accuracy=0.300 vs 0.8) — preserved unchanged. GitHub's annotation cap (~10 notices/check-run) hid the V2 summary.
- Commit `e66d3716`: per-row annotations limited to non-MATCH rows so both summaries surface. **Run 42559810631:** all suites PASS; both summaries visible (section 3); independent gate FAIL unchanged.

## 5. Debts recorded for Xu / Ka (Vibe authored the specs and must NOT self-adjudicate)

- **DEBT-ES-07 (Ka):** independent adjudication of all 50 rows of `EVIDENCE_SUPPORT_FACT_SPECS_V2.json` (supersedes the 22-row scope of DEBT-ES-02 for corpus diagnostics); freeze with SHA-256 per the B5 protocol. The 49/50 MATCH result is build evidence only, NOT adjudication.
- **DEBT-ES-08 (Xu):** candidate Gate C metric — citation-source alignment, needed because the corpus contains duplicate-content sources (Q037/Q045 divergence). Fold into the Gate C design after DEBT-ES-02/07.
- **DEBT-ES-06 (Ka/Qw, extended):** Q040 joins Q008/Q035/Q010 as the concrete retrieval-side leak/miss list at the operating point (Q040: zero candidates above min_score 0.35). QUERY_EXPANSIONS overfit risk unchanged.
- **DEBT-ES-03 (Xu, unchanged):** Gate C design remains BLOCKED until Ka's adjudication of the decision set and fact specs.

## 6. Next

Ka: DEBT-ES-01/02/07. Xu: DEBT-ES-03/04/05/08 and DOC-055/057 registration of the V2 dataset. Vibe: available for further build under Vinh's standing authorization; no further self-serving adjudication.

## 7. v2 metrics update — citation-source alignment + relaxed-threshold retrieval probe (CI run #96, head c14939a4)

- **Harness upgrade (commit `c14939a4eab69a6995fc6289cabc30042eab2014`):** the corpus-eval harness now measures, for answerable rows with fixture-declared expected sources, (a) `citation_aligned` — whether any cited source matches the expected source — and (b) a relaxed-threshold retrieval probe (RELAXED_PROBE_TOP_K=10) reporting `relaxed_best`, the best relaxed score of the expected-source span, quantifying how far the operating threshold sits from surfacing it. REPORT-ONLY: no gate, threshold, fixture or eval change.
- **CI-verified V2 summary (run #96, head c14939a4):** `specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0 citation_misaligned=2 expected_source_missed=2`
- **CI-verified V1 summary:** `specs=22 match=21 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0 citation_misaligned=0 expected_source_missed=1`
- **citation_misaligned=2 (Q037/Q045):** both SUPPORTED rows match spans in `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md` while the fixture's expected source is `00_CORPUS/architecture.md` (duplicate-content corpus). Q037 top1 score 1.0 (expected-source relaxed best 0.353077); Q045 top1 0.725207. Candidate Gate C metric (DEBT-ES-08).
- **expected_source_missed=2 (Q037/Q040):** Q040 (ideal CONTRADICTED, reason NO_CANDIDATES, expected `00_CORPUS/security.md`) has zero candidates at the operating point; the expected-source span's relaxed best is 0.19145 — well below min_score 0.35 — confirming Q040 as a retrieval-side miss (DEBT-ES-06), not a support-stage defect.
- **Unit tests:** all four suites (including the corpus-eval suite) PASS on the CI matrix; the only check error is the preserved independent-gate failure (no_answer_accuracy=0.300 vs floor 0.8), unchanged.
- **Adjudication status:** all v2-metric fields (expected sources, citation alignment, relaxed probe values) are AUTHORED_PENDING_INDEPENDENT_ADJUDICATION (Ka, DEBT-ES-07 scope extension; Xu, DEBT-ES-08). No gate or release claim is made from these numbers.
- **Verification note:** annotations were read from the GitHub commit-checks page of head c14939a4; the anonymous api.github.com quota was exhausted from the build environment's shared IP, so the numeric Actions run ID of run #96 could not be recorded this session — workflow run number (#96) plus commit SHA are the binding references.
