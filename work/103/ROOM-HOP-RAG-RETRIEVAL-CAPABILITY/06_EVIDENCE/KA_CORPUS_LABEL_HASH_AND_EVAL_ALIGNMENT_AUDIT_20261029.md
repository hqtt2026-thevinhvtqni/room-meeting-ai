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

The authoritative refined row-by-row adjudication is:
`06_EVIDENCE/KA_ADJUDICATED_LABELS_50_QUERIES_V3_20261029.json`

- Parsed/reviewed row count: 50/50.
- Per-row canonical SHA-256 fields: 50/50 independently recomputed and matched on GitHub readback.
- Canonical dataset SHA-256: `4a1e11221f623030fc95632fa39b386eb7612e5ead244693b1d7c171d7089fa5`; recomputation on readback matches.
- Final adjudication: Q009 changes from `NO_ANSWER` to `ANSWERABLE` because `sales.md` explicitly names the sales employee as responsible for both confirmations. Q016 and Q046 remain `NO_ANSWER`: the architecture source gives ChromaDB extension-gate criteria but no implementation/configuration procedure answering these how-to queries.
- V2 is retained as historical/provisional; V3 supersedes it. Qw V5 remains unchanged.

This verifies the canonical V3 JSON representation and records Ka's row-by-row source review. It does not prove that the original annotation process was blind.

## 3. Critical evaluation alignment finding

The 50-query adjudication corpus (Manifest V4) is not the same corpus as `05_TEST/EVAL_SET.json` on the Work 103 branch:
- Manifest V4 enumerates six source documents: five fixture policy/domain files plus the RAG architecture document.
- `EVAL_SET.json` is version 2 and embeds eight synthetic documents with 50 labeled queries and 15 no-answer queries. The earlier plan's “14 labeled + 5 no-answer” statement is stale for this v2 file.

Therefore, the reported retrieval metrics for EVAL_SET v2 must not be presented as measured performance on the 50-query Manifest V4 corpus. The two datasets have different sources and different purposes. Before any release-quality retrieval score is accepted, define the evaluation corpus/snapshot explicitly and run the evaluation against that exact snapshot and its matching labels. Do not silently replace EVAL_SET or conflate its metrics with the 50-query adjudication set.

## 4. Remaining gates / actions

1. **Raw-byte integrity:** published GitHub raw-content bytes are verified against the six declared source hashes (UTF-8/LF). Original Sandbox stored bytes are still not independently verified.
2. **Blinding provenance:** still not verified; no independent process attestation proves Qw did not view retrieval outputs.
3. **Adjudication:** Ka has completed a source-based review of all 50 rows; V3 records one final correction (Q009) and preserves Q016/Q046 as NO_ANSWER. The blind-process provenance remains unverified, so the set is adjudicated but not certified as a blind evaluation.
4. **Evaluation alignment:** choose and freeze one explicit source snapshot for the benchmark, bind labels and metrics to it, and rerun metrics against that exact dataset.
5. **Runtime integration:** `rag_retrieval.py` describes itself as an isolated Sandbox prototype, not wired into Core/MCP. The acceptance plan still has the live integration and negative E2E checklist unchecked.
6. **CI / baseline:** Ka did not execute Python tests directly. GitHub Actions run #32 completed successfully on Python 3.11 and 3.12; retrieval unit tests and the labeled evaluation gate passed. The metrics apply only to EVAL_SET v2 (8 embedded documents, 50 labeled queries and 15 no-answer queries), not to the six-source Manifest V4 corpus or the newly adjudicated 50-query dataset. No live MCP/Core E2E was executed.

## Decision
**Work 103 remains ACTIVE / BLOCKED.** GitHub sync and logical-text hash consistency for the six Manifest V4 sources are verified. Do not declare corpus FROZEN, final blind-label PASS, retrieval evaluation PASS on the 50-query set, or RAG E2E PASS until the remaining gates have their own evidence.

— Ka | CSA / Independent Reviewer
