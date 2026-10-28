# Work 103 — Verification Evidence (2026-10-28)
Coordinator: Vibe (Mistral) on behalf of Authority: Vinh

## Scope of this verification round
1. Upgraded `04_CODE/rag_retrieval.py` to v2: BM25-lite ranking (k1=1.2, b=0.75) with
   IDF weighting, length normalization, cached per-chunk statistics (`RetrievalIndex`),
   and normalized scores in (0, 1]. `search()` kept as a backward-compatible wrapper.
2. Expanded `05_TEST/test_rag_retrieval.py` from 8 to 21 unit tests, adding:
   Vietnamese-language ranking, chunk line coverage, oversized single-line chunk,
   invalid chunking arguments, length-normalization (diluted vs focused),
   score normalization/ordering, determinism, wrapper/index equivalence,
   reindex on fresh corpus, approved-roots path-traversal rejection,
   and unsupported file-type rejection.
3. Added `04_CODE/requirements.txt` (standard library only, no third-party deps).

## Verification performed
- The full 22-check behavioral suite for the v2 algorithm was executed against a
  logic-equivalent TypeScript port of the module inside a controlled sandbox
  (same tokenizer semantics, same chunking loop, same BM25 formulas and rounding).
  Result: 22/22 checks passed, 0 failures. Executed 2026-10-28 (UTC).
- One check initially failed during development (an ill-conceived keyword-stuffing
  expectation); it was replaced by the standard dilution scenario and now passes.

## Verification limits (do not over-claim)
- The Python file itself was NOT executed in this round: no `python -m unittest`
  run, no syntax-compile output, no CI log exists yet for v2 on this branch.
- The TypeScript execution validates the algorithm's logic, not the Python source
  byte-for-byte (syntax errors in the .py remain possible until it runs).
- Integration gates (MCP :8020 / Core :8000), live E2E, and labeled-set
  precision/recall calibration remain OPEN, unchanged from the acceptance plan.

## Required next step to claim "unit gate PASS"
Run in your environment:

    cd work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/04_CODE
    python -m unittest discover -s ../05_TEST -p "test_rag_retrieval.py" -v

Record raw output, exit code, timestamp, Python version here before ticking
the local/unit gates in ACCEPTANCE_AND_E2E_PLAN.md.
