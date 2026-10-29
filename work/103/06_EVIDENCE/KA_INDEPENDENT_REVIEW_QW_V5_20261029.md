# WORK 103 — KA INDEPENDENT REVIEW: QW V5 / CORPUS MANIFEST v3.0
**Date-time:** 2026-10-29 (UTC+07:00)
**Reviewer:** Ka | CSA / Independent Reviewer
**Decision:** STRUCTURE PASS; HASH/MANIFEST VERIFICATION FAIL; BLIND-PROCESS FREEZE BLOCKED; RAG E2E NOT PASS.

## Evidence inspected
Read directly through ROOM-HOP MCP Sandbox: manifest v3.0, all six manifest files, V5 labels, request/scope, Work manifest, retrieval prototype, unit tests, and gate status.

## Structural validation — PASS
- Exactly 50 rows, unique Q001–Q050.
- Seven columns: query_id, query_text, label, expected_source_id, category_stratum, evidence_span_rationale, ambiguity_flag.
- No score, rank, or retrieval-output fields.
- Q050 is now a valid policy-level ANSWERABLE question: security.md explicitly says the system must not store or return an administrator password.
- Q015, Q026, Q028, Q036, Q041–Q043 and Q047–Q049 have plausible source-level support in the referenced fixtures, subject to corpus identity and provenance gates.

## P0 — Manifest byte sizes do NOT verify
Manifest declarations versus current MCP-reported file sizes:

| File | Manifest bytes | MCP-reported bytes | Result |
|---|---:|---:|---|
| 00_CORPUS/network.md | 720 | 728 | MISMATCH |
| 00_CORPUS/sales.md | 651 | 658 | MISMATCH |
| 00_CORPUS/architecture.md | 1367 | 1384 | MISMATCH |
| 00_CORPUS/security.md | 1070 | 1082 | MISMATCH |
| 00_CORPUS/evidence.md | 1127 | 1138 | MISMATCH |
| 03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md | 2606 | 2649 | MISMATCH |

SHA-256 values were not independently recomputed in this review. The manifest's “verified” claim is therefore unsubstantiated. Do not mark the corpus FROZEN. Qw must calculate hashes/sizes from exact bytes using a documented method, create a new manifest version (preserve v3.0), and have an independent verifier reproduce the results. If MCP size_bytes represents another encoding/representation, document the acquisition and hashing method and demonstrate matching results.

## Provenance — approval claims still insufficient
“Approver / Scope Evidence” mostly links scope/architecture documents, not a distinct approval record identifying approving authority, decision, date, and approved artifact version/hash. A source document used to derive a fixture is derivation evidence, not independent approval. Keep the classification as Benchmark Fixture Corpus; do not call it production-canonical or upstream-approved.

## Blindness / freeze — BLOCKED
- No independently verifiable Xu attestation proves labels were created without viewing retrieval outputs.
- Omitting score/rank/output fields proves artifact shape only, not process blindness.
- No verified freeze record/hash for the exact V5 and corpus snapshot was found.
- Since corpus fixtures and rationales were authored together in this workflow, describe it as benchmark-fixture annotation unless the independent blind process is evidenced.

## Row-level notes
- Q050: policy question supported; ANSWERABLE accepted against the fixture.
- Q040: supports a policy/authority boundary; it does not prove runtime enforcement or prove that no external tool could delete files. Keep rationale policy-level.
- Q004/Q008–Q010/Q016/Q025/Q030/Q032/Q035/Q044/Q046: NO_ANSWER plausible relative to this fixture snapshot, not the wider production system.
- Q027 is supported by the fixture and prototype (top_k <= 0 raises ValueError), not integrated runtime evidence.
- V5 is not an evaluation result; no benchmark metrics or live E2E execution were performed in this review.

## Required actions
1. Qw: create a new manifest version with reproducible hashes/sizes; preserve v3.0. Add actual approval evidence or mark approval NOT PROVIDED / derivation only.
2. Xu: independently verify exact file bytes/hashes and document the blind-process attestation, if verifiable. Do not declare FROZEN until hashes match.
3. Ka: repeat source/hash checks and complete row-level adjudication after corrected snapshot is available.
4. Implementation owner: separately run acceptance and live MCP :8020 -> Core :8000 -> retrieval -> source readback. Current `rag_retrieval.py` says it is not wired into Core/MCP; E2E remains NOT PASS.

**Gate:** ACTIVE / BLOCKED.
**Signature:** Ka | CSA / Independent Reviewer
