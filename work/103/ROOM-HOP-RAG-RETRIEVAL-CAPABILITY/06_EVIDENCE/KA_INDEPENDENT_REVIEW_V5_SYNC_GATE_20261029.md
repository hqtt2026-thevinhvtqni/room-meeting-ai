# WORK 103 — KA Independent Review of Corpus Manifest V4 and Labels V5
- Reviewer: Ka (CSA / Independent Reviewer)
- Date: 2026-10-29 (UTC+07:00)
- Scope: Work 103 only; review of Sandbox artifacts and sync verification on branch `work/103-rag-retrieval-capability`.
- Status: BLOCKED — do not freeze or claim RAG E2E PASS.

## GitHub sync evidence
The following files were created on the Work 103 branch from the current Work 103 Sandbox content:
- `00_CORPUS/CORPUS_MANIFEST_v4.0.md` — blob SHA `5832e9a51b2531637473c59e7f70ef371ed24872`.
- `06_EVIDENCE/QW_BLIND_LABELS_50_QUERIES_V5_20261029.md` — blob SHA `cc5c8d39725bac8d51237adcbd9ee96a0d094db8`.
The paths are under `work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/`. GitHub readback succeeded for both. The compare endpoint reports the branch is 30 commits ahead and 10 behind main; this review does not merge or rebase branches.

## Findings
1. Manifest V4 explicitly says approval is PENDING and freeze is PENDING_XU_VERIFICATION. It reports logical UTF-8/LF hashes, not independently verified raw stored-byte hashes. The reconciliation document itself says raw-byte verification is NOT VERIFIED. Ka does not certify raw-byte integrity from decoded text alone.
2. Labels V5 contains 50 query rows Q001–Q050 and no retrieval scores/ranks in the artifact. However, it still cites Manifest v3.0 in the labeling rules and corpus reference, not v4.0.
3. V5 does not include the claimed per-row `label_canonical_sha256` fields. No canonical dataset hash/freeze attestation was verified in this review.
4. Q050 is supported by the current security fixture: the fixture explicitly prohibits storing or returning system administrator passwords. Q015 and Q027 also match the architecture fixture's stated MCP/Core boundary and positive top_k rule. These spot checks do not constitute full adjudication of all 50 labels.
5. The blind-process claim remains unverified. File structure and absence of score columns do not prove Qw did not view retrieval outputs before labeling.
6. The source fixture paths referenced by the manifest were not all found on GitHub at the expected nested paths during this pass. Do not treat GitHub's manifest/label sync as proof that the complete corpus snapshot is synced.

## Required before opening the evaluation gate
- Align V5's corpus/version references with the exact frozen manifest and snapshot.
- Produce a canonical hash for the complete labels dataset using a documented deterministic serialization; verify it independently.
- Verify the actual corpus source files and their hashes from a reproducible byte-level source, or explicitly standardize and document the UTF-8/LF logical-text hash convention.
- Obtain an explicit freeze attestation and a truthful blind-process attestation with provenance.
- Ka must finish row-by-row adjudication after the snapshot and annotation provenance are stable.
- Separately demonstrate live MCP :8020 -> Core :8000 -> retrieval -> source readback before any RAG E2E PASS.

## Decision
**Work 103 remains ACTIVE / BLOCKED.** The two artifacts are now present on the Work 103 GitHub branch, but the freeze, complete-corpus sync, blind-process provenance, final adjudication, and live E2E acceptance gates remain open.

— Ka | CSA / Independent Reviewer
