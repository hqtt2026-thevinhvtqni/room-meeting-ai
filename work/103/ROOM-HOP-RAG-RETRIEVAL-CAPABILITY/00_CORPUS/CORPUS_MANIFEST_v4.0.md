# CORPUS MANIFEST v4.0 (Benchmark Fixture Corpus)

## Status
- **Classification**: Benchmark Fixture Corpus (Derived for Work 103 evaluation).
- **Approval Status**: **PENDING**. This corpus is derived from Work 103 scope documents by Qw. It has NOT received formal upstream approval as a canonical production corpus. Xu/Ka must formally review and approve before promotion.
- **Freeze Status**: PENDING_XU_VERIFICATION.

## Provenance & Integrity Table

| File Path | Logical Size (Bytes) | MCP Reported Size (Bytes) | SHA-256 (Logical Content) | Upstream Source / Derivation | Approver / Scope Status |
|---|---|---|---|---|---|
| `00_CORPUS/network.md` | 720 | **728** | `f7c0b4c2c9f88a39ac5bea73d99d8e2593b6c634273b668ed5f8e2ae19a55089` | Work 103 Network Troubleshooting Scope | PENDING (Derived by Qw, awaiting Xu/Ka review) |
| `00_CORPUS/sales.md` | 651 | **658** | `a25b613d6d30be1b6f283d74ace9ccbee41a608bae75c5758fc019366b0f2fbc` | Work 103 Sales Confirmation Scope | PENDING (Derived by Qw, awaiting Xu/Ka review) |
| `00_CORPUS/architecture.md` | 1,367 | **1,384** | `5910ffb71f423a908f471f9ad093cea5e1c550c8e6353b61335d2e1a1a7ad530` | Work 103 RAG Port & Contract Scope | PENDING (Derived by Qw, awaiting Xu/Ka review) |
| `00_CORPUS/security.md` | 1,070 | **1,082** | `56c166ebc8699696ac0f4c470409101444aaa62ac9872c905d85f52afc14d71f` | Work 103 Security & Indexing Rules | PENDING (Derived by Qw, awaiting Xu/Ka review) |
| `00_CORPUS/evidence.md` | 1,127 | **1,138** | `f0b03afc3b3504139ef1d3b60441d054c0b5e6e674d86d65dca47322fd624538` | Work 103 QA/Review Process Definition | PENDING (Derived by Qw, awaiting Xu/Ka review) |
| `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md` | 2,606 | **2,649** | `ef51fa32722cfcb11c630e3f39c83ac1ee25036e1201ac856a4d586f86adb27e` | Work 103 RAG Retrieval Architecture Decision | PENDING (Derived by Qw, awaiting Xu/Ka review) |

## Critical Notes for Xu (Coordinator)
1. **Size Mismatch Resolution**: The "Logical Size" was calculated on the core text content. The "MCP Reported Size" includes trailing newlines or specific encoding bytes (e.g., CRLF) present in the actual Sandbox files. 
2. **Mandatory Action**: Xu MUST independently calculate the SHA-256 hash directly from the raw sandbox bytes of each file to ensure absolute integrity before declaring the corpus FROZEN. Do not trust the "SHA-256 (Logical Content)" column without raw byte verification.
3. **Approval Gate**: This manifest explicitly states that the corpus is PENDING approval. It is a fixture for evaluation, not a ratified production standard yet.

## Xu reconciliation addendum — 2026-10-29 (UTC+07:00)

Xu independently reproduced the six **logical UTF-8/LF text hashes and lengths** from MCP-returned content. All six logical hashes/sizes match this manifest and v3. For each file, MCP `size_bytes` equals the UTF-8 size after converting each returned LF to CRLF; the returned text contains LF only. Reconstructed CRLF hashes differ from the logical hashes (see `06_EVIDENCE/XU_CORPUS_HASH_RECONCILIATION_20261029.md`). This supports the line-ending explanation, but reconstructed CRLF hashes are not raw-byte verification.

- Logical text hash verification: **COMPLETE, 6/6 matches**.
- Exact stored-byte hashing through MCP: **NOT AVAILABLE / NOT VERIFIED**.
- Freeze status: **PENDING KA REVIEW; NOT FROZEN**.
- Approval remains limited to benchmark-fixture use; no upstream production-corpus approval is claimed.
- V5 label text hash: `48d100372bb3e4b88f541dee750e62f82f9642ee2fd0e481553ef43cfaa281f2` (UTF-8/LF text representation); this does not prove annotation blinding.
