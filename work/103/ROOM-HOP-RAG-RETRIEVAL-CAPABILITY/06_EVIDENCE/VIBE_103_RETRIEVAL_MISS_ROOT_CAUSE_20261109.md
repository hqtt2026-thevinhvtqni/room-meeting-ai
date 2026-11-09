# VIBE 103 — Retrieval-Miss Root-Cause Analysis (Diagnostic v3, report-only)
- **Producer:** Vibe (GLM 5.3 via Vibe Work agent), 2026-11-09 (UTC+07), under Vinh's standing full-build authorization (2026-11-08).
- **Status:** REPORT-ONLY, AUTHORED_PENDING_INDEPENDENT_ADJUDICATION. No code, threshold, label, fixture or gate was changed by this analysis. Nothing here is a release or gate-adjudication claim.
- **Purpose:** Decompose the retrieval-side misses quantified by diagnostic v2 (CI run #96, head c14939a4eab69a6995fc6289cabc30042eab2014) into their causes, and hand Ka/Qw (DEBT-ES-06) and Xu (DEBT-ES-08) counterfactual evidence for remediation decisions.

## 1. Method and port validation
The build environment executes TypeScript, not Python. The exact production pipeline (chunking max_chars=300/overlap=40 line-aligned; BM25-lite k1=1.2 b=0.75; QUERY_STOPWORDS; QUERY_EXPANSIONS at 0.75 weight; score = raw / sum(query-term IDFs), capped at 1.0) was ported to TypeScript and run over the EVAL_SET_CORPUS_V4_V3 fixture corpus (42 chunks across 6 sources).

Port validation anchors — the port reproduces the CI-verified numbers exactly:
| Anchor | CI (run #96) | TS port |
|---|---|---|
| Q040 relaxed_best (security.md negating span) | 0.191450 | 0.191450 |
| Q037 relaxed_best (expected architecture.md span) | 0.353077 | 0.353077 |
| Independent gate no_answer_accuracy | 0.300 (3/10) | 3/10 retrieval abstentions |
| Q008 lexical leak score (sales.md) | ~0.990 (Ka leak analysis) | 0.990402 |

CI remains the binding verification for any future change; this document is analysis material only.

## 2. Finding F1 — Q040 is a threshold miss, not a ranking miss
The negating span ("Retrieval không cấp quyền thực thi lệnh cho hệ thống", security.md chunk 3/4, overlapping) is the RANK-1 candidate for Q040 at the relaxed threshold (0.191450 / 0.187447). Ranking is correct; the operating min_score 0.35 rejects it. Two multiplicative penalties:

1. **Zero-df query terms inflate the IDF denominator.** Of Q040's 12 query terms, 6 appear in NO corpus chunk (sử, tự, xóa, đĩa, động, ổ) yet still contribute their IDF to the denominator: idfSum 40.0287 vs 13.3026 for matched terms only — a ~3.0x score penalty on every chunk.
2. **Vocabulary mismatch bridged only by a 0.75-weight expansion alias.** The query says "xóa tệp" (delete files); the span says "thực thi lệnh" (execute commands). The only lexical bridge is the hand-authored QUERY_EXPANSIONS entry xóa tệp → (thực, thi, lệnh, execute, commands) at 0.75 weight. Without that alias the span would score ~0.

## 3. Finding F2 — counterfactual matrix over all 50 queries (why the threshold cannot simply be "fixed")
Four normalization/threshold variants were simulated over the full 50-query fixture. Denominator changes scale all chunks of a query uniformly, so RANKING is unchanged; only threshold crossings move.

| Variant | Answerable expected-source pass (≥0.35, in top-5) | No-answer retrieval abstentions (0 candidates ≥0.35) |
|---|---|---|
| current (CI-verified behaviour) | 38/40 (Q037 rank>5; Q040 0.191<0.35) | 3/10 (Q016, Q030, Q046) |
| exclude zero-df terms from denominator | 39/40 (Q040 recovered at 0.564) | **0/10 — ALL no-answer queries leak, including Q030 adversarial gibberish at 0.794** |
| expansion alias weight 0.75→1.0 | 38/40 (Q040 0.243, still <0.35) | 3/10 (unchanged) |
| both | 39/40 | **0/10** |

Interpretation (material for DEBT-ES-06): any normalization that recovers Q040 re-opens the entire no-answer leak surface at the retrieval level. The honest remediation options for Ka/Qw are corpus-side (an explicit security policy sentence containing the deletion vocabulary, so the span matches on original query terms) or a re-calibrated per-class threshold — but each must be re-evaluated against the full fixture, and this matrix shows the tradeoff explicitly. The two-stage architecture (retrieval + evidence-support stage) already answers all 10 no-answer queries safely behind unchanged lexical retrieval (CI: no_answer_leak=0, false_abstention=0 in V2, run #96), which remains the seeded remediation path for the failing independent gate.

## 4. Finding F3 — Q037 is a ranking problem; insensitive to any threshold/normalization fix
Q037's expected span (architecture.md chunk 7, "trả về/lý do từ chối" family) scores 0.353077 — ABOVE the 0.35 threshold — but ranks 7th: the top-5 is crowded by the duplicate-content source 03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md (chunks #4/#5 at 1.0, containing the identical "authorized AI caller → grounded answer with citations/abstention" data-flow text) and evidence.md governance chunks (0.54/0.48). Because denominator variants scale uniformly per query, no variant changes top-5 membership. The citation misalignment on Q037/Q045 therefore belongs to DEBT-ES-08 (citation-source alignment metric / duplicate-content corpus policy), not DEBT-ES-06.

## 5. Finding F4 — Q045 duplicate-content ranking detail
RAG_RETRIEVAL_ARCHITECTURE.md#11 (0.725207) outranks architecture.md#4 (0.604044) on semantically identical rag_get_context contract text, because the smaller/cleaner chunk in the duplicate source has higher term density under BM25 length normalization. Decision remains SUPPORTED either way (scored decisions only); the divergence is purely the citation-source field.

## 6. Finding F5 — retrieval-level leak profile at the operating point
7/10 no-answer queries return at least one candidate ≥0.35 (Q004 0.412, Q008 0.990, Q010 0.636, Q025 0.367, Q032 0.434, Q035 0.736, Q044 0.429); 3/10 abstain (Q016, Q030, Q046) — exactly the independent gate's 0.300. The Q008 leak (0.990402) exceeds nearly every answerable query's score: score magnitude alone cannot separate no-answer from answerable at the lexical level, which is the quantified justification for the two-stage design (Gate B evidence-support discipline) rather than any single-threshold retrieval fix.

## 7. Recommendations handed to owners (Vibe does not self-adjudicate)
- **Ka/Qw (DEBT-ES-06):** Q040 remediation should be corpus-side (explicit policy span matching deletion vocabulary) or a per-class calibrated threshold; F2's matrix is the evidence that a global normalization change is not viable without re-opening all 10 no-answer leaks. QUERY_EXPANSIONS overfit risk is now concretely visible: Q040 is retrieved ONLY through a hand-authored alias.
- **Xu (DEBT-ES-08):** F3/F4 show citation misalignment is a duplicate-content ranking property, measurable now; fold into Gate C design after adjudication.
- **No action taken on rag_retrieval.py, thresholds, labels, fixtures or gates by this analysis.**
