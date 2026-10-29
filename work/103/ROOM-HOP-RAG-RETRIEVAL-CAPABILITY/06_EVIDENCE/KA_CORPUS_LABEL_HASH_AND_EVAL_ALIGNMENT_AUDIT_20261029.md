# WORK 103 — KA Corpus/Label Hash Verification and Remaining Gate Audit
- Reviewer: Ka (CSA / Independent Reviewer)
- Date-time: 2026-10-29 (UTC+07:00)
- Branch: `work/103-rag-retrieval-capability`
- Scope: Work 103 only.
- Decision: **ACTIVE / BLOCKED**. Hashes for the six declared logical-text sources and canonical label dataset are verified from GitHub readback. Corpus freeze, blind-process provenance, evaluation-set alignment, and live E2E remain open.

## 1. GitHub readback and source hashes

The five domain/policy fixture files are present under `00_CORPUS/`; the sixth source is the architecture document at `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`. All six are present under the Work 103 root `work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/`.

| Source | SHA-256 over UTF-8/LF logical text | Match to Manifest V4 |
|---|---|---|
| `00_CORPUS/network.md` | `f7c0b4c2c9f88a39ac5bea73d99d8e2593b6c634273b668ed5f8e2ae19a55089` | MATCH |
| `00_CORPUS/sales.md` | `a25b613d6d30be1b6f283d74ace9ccbee41a608bae75c5758fc019366b0f2fbc` | MATCH |
| `00_CORPUS/architecture.md` | `5910ffb71f423a908f471f9ad093cea5e1c550c8e6353b61335d2e1a1a7ad530` | MATCH |
| `00_CORPUS/security.md` | `56c166ebc8699696ac0f4c470409101444aaa62ac9872c905d85f52afc14d71f` | MATCH |
| `00_CORPUS/evidence.md` | `f0b03afc3b3504139ef1d3b60441d054c0b5e6e674d86d65dca47322fd624538` | MATCH |
| `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md` | `ef51fa32722cfcb11c630e3f39c83ac1ee25036e1201ac856a4d586f86adb27e` | MATCH |

Hash scope: Ka fetched the published files through GitHub's raw-content endpoint, confirmed LF line endings (no CRLF), re-encoded the returned UTF-8 text, and computed SHA-256. All six source hashes and UTF-8 byte lengths match Manifest V4. This verifies the published GitHub branch's raw text representation; it does not verify the original Sandbox's stored bytes or prove a byte-identical local Sandbox/GitHub checkout. The manifest's own SHA-256 over the published UTF-8/LF bytes is `52a843c800cbc503c8f429f6e21b8b0fe55d293b87e535f7272bd22cd3f4a666`; V5 label text SHA-256 is `48d100372bb3e4b88f541dee750e62f82f9642ee2fd0e481553ef43cfaa281f2`.

## 2. Canonical adjudicated label artifact

Created the first canonical representation and then completed row-by-row source adjudication in:
`06_EVIDENCE/KA_ADJUDICATED_LABELS_50_QUERIES_V2_20261029.json`

- Parsed/reviewed row count: 50/50.
- Per-row canonical SHA-256 fields: 50/50 independently recomputed and matched on GitHub readback.
- Canonical dataset SHA-256 (compact JSON serialization of adjudicated rows, including source SHA and Ka review fields, excluding per-row hash fields): `579c61bda1df8b643795f58da733f8fc3c2b4132438588da1f7e32a7c1c404d3`.
- Recomputed dataset hash on GitHub readback: same value.
- Three adjudications against the explicit answerability rule: Q009 `NO_ANSWER` -> `ANSWERABLE` (sales employee is named); Q016 `NO_ANSWER` -> `ANSWERABLE` (architecture says ChromaDB is an extension gate and lists prerequisites, so immediate addition is not supported); Q046 `NO_ANSWER` -> `ANSWERABLE` (the corpus answers that immediate configuration is not available and requires the extension gate, though it provides no configuration recipe). Qw V5 remains unchanged.

This verifies the canonical JSON representation and records Ka's row-by-row source review. It does not prove that the annotation process was blind or authorize freezing the dataset.

## 3. Critical evaluation alignment finding

The 50-query adjudication corpus (Manifest V4) is not the same corpus as `05_TEST/EVAL_SET.json` on the Work 103 branch:
- Manifest V4 enumerates six source documents: five fixture policy/domain files plus the RAG architecture document.
- `EVAL_SET.json` is version 2 and embeds eight different synthetic documents with its own 14 labeled plus 5 no-answer query baseline, according to the acceptance plan.

Therefore, the reported retrieval metrics for EVAL_SET v2 must not be presented as measured performance on the 50-query Manifest V4 corpus. The two datasets have different sources and different purposes. Before any release-quality retrieval score is accepted, define the evaluation corpus/snapshot explicitly and run the evaluation against that exact snapshot and its matching labels. Do not silently replace EVAL_SET or conflate its metrics with the 50-query adjudication set.

## 4. Remaining gates / actions

1. **Raw-byte integrity:** still not verified; available read APIs return decoded text and size metadata.
2. **Blinding provenance:** still not verified; no independent process attestation proves Qw did not view retrieval outputs.
3. **Adjudication:** Ka has completed a source-based review of all 50 rows and recorded three corrections in V2. The blind-process provenance remains unverified, so the set is adjudicated but not certified as a blind evaluation.
4. **Evaluation alignment:** choose and freeze one explicit source snapshot for the benchmark, bind labels and metrics to it, and rerun metrics against that exact dataset.
5. **Runtime integration:** `rag_retrieval.py` describes itself as an isolated Sandbox prototype, not wired into Core/MCP. The acceptance plan still has the live integration and negative E2E checklist unchecked.
6. **Testing:** this review verified source hashes and label hashes from GitHub readback; it did not execute Python tests or live MCP/Core E2E in this session. Existing test/CI claims are not newly re-run by this report.

## Decision
**Work 103 remains ACTIVE / BLOCKED.** GitHub sync and logical-text hash consistency for the six Manifest V4 sources are verified. Do not declare corpus FROZEN, final blind-label PASS, retrieval evaluation PASS on the 50-query set, or RAG E2E PASS until the remaining gates have their own evidence.

— Ka | CSA / Independent Reviewer
