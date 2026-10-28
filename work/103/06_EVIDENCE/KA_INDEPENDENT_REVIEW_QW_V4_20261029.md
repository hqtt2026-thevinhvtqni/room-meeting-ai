# WORK 103 — KA INDEPENDENT REVIEW OF QW V4 / MANIFEST v2.0
**Date-time:** 2026-10-29 (UTC+07:00)
**Reviewer:** Ka | CSA / Independent Reviewer
**Scope:** Work Sandbox evidence only; no production-corpus approval implied.
**Decision:** STRUCTURE PASS; LABEL ADJUDICATION BLOCKED; FREEZE NOT VERIFIED; RAG E2E NOT PASS.

## 1. Evidence directly inspected
Read through ROOM-HOP MCP Sandbox:
- `00_CORPUS/CORPUS_MANIFEST_v2.0.md`
- all five `00_CORPUS/*.md` fixture files
- `03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md`
- `06_EVIDENCE/QW_BLIND_LABELS_50_QUERIES_V4_20261029.md`
- `05_TEST/test_rag_retrieval.py`
- `04_CODE/rag_retrieval.py`
- `06_EVIDENCE/BLIND_LABELING_GATE_STATUS_20261028.md`

V4 has 50 rows Q001–Q050, unique IDs, seven columns including the new `category_stratum`, and no score/rank/retrieval-output fields. Manifest v2.0 explicitly calls the corpus a Benchmark Fixture Corpus rather than a production canonical corpus. These are positive structural improvements.

## 2. Row-level adjudication findings
### BLOCKER — Q050 is still not supported by the cited evidence
Query: “Tệp 00_CORPUS/security.md có chứa mật khẩu quản trị của hệ thống không?”
Label: ANSWERABLE; source: `00_CORPUS/security.md`.
The source says the system must not store or return an admin password, and says credentials must not be indexed. These are policy constraints; they do not prove that the file itself contains no password. The current rationale incorrectly treats a prohibition as evidence of actual file contents. Recommended fix: rewrite the query to ask whether policy prohibits storing/returning admin passwords, or label the file-content question NO_ANSWER unless a verified content inspection/source statement establishes absence. Do not use “absence of evidence” to convert a policy prohibition into a factual claim about file contents.

### Provenance / authority still incomplete
Manifest v2.0 improves disclosure but does not yet provide independently traceable provenance:
- Upstream Source/Derivation entries are descriptive pointers (e.g. synthetic unit-test fixtures, Work 89/22 scope); no upstream commit/blob hash, source artifact snapshot, or exact derivation evidence is recorded.
- “Approver / Scope” values such as “Work 103 Scope” and “Work 103 Architecture” identify a scope, not a named approver or approval evidence.
- Byte Size and SHA-256 remain Pending for all manifest rows.
- `00_CORPUS` files are authored benchmark fixtures. They may support a controlled fixture benchmark, but they must not be represented as validated production knowledge. The architecture document explicitly says Workspace/Sandbox is for build artifacts and evidence, not a canonical production corpus.

This does not prevent describing the corpus honestly as a fixture set, but it prevents claims that provenance/approval and freeze have been fully satisfied.

### Label-rule / dataset-quality note
The manifest's “Absence of Evidence” rule is too broad as currently phrased if interpreted to mean that a policy forbidding a thing proves the thing is absent from a particular file or system. Keep the distinction:
- policy question (“Is indexing credentials prohibited?”) -> ANSWERABLE from the policy;
- state/content question (“Does this file contain a password?”) -> only ANSWERABLE with evidence about that file's actual contents; otherwise NO_ANSWER.
Q050 must be corrected or adjudicated under this distinction before the label set can be accepted.

### Other rows
- Q015: supported by `00_CORPUS/architecture.md` which explicitly says MCP does not access storage directly and all operations go through Core.
- Q026: supported by the architecture fixture's explicit `sufficient_evidence` / `abstention_reason` contract.
- Q028/Q041/Q042/Q043: supported by the architecture fixture's source-path, chunk-number, start-line and end-line metadata statements.
- Q036: the cited architecture source explicitly documents approved source registry -> ingestion adapter -> normalized docs/source metadata -> chunks -> retrieval index -> Core-owned retrieval service -> MCP -> authorized AI caller. Manifest includes that source path. Its hash/size still pending.
- Q040: reasonably supported as a policy-level negative (retrieval grants no execution authority); avoid phrasing this as proof of runtime enforcement.
- Q047–Q049: structurally valid governance/process questions, but the cited evidence.md is itself a Work 103 fixture. External role/approval authority is not independently evidenced by that fixture alone.
- Q011–Q014 port claims: these appear in the authored architecture fixture, but remain fixture claims until reconciled against approved upstream architecture/runtime evidence.

## 3. Blindness and freeze
V4 contains no retrieval scores, ranks or outputs. That is a structural observation only; it does not prove Qw never viewed retrieval output while annotating. No independent blind-process attestation from Xu is present in the inspected gate record. No SHA-256/byte-size table has been populated and no valid freeze declaration is evidenced. Ka cannot substitute for Xu's process attestation or sign a freeze on Xu's behalf.

## 4. Implementation / acceptance boundary
`04_CODE/rag_retrieval.py` explicitly calls itself an isolated Sandbox prototype not wired into Core/MCP. Unit tests use synthetic `docs/network.md` and `docs/sales.md` fixtures, not the V4 corpus as an end-to-end system. Therefore the V4 review does not establish benchmark execution, Core/MCP integration, or RAG E2E PASS.

## 5. Required actions
1. Qw: correct Q050 (prefer a policy question or supply verifiable evidence of the file's actual contents); preserve V4 unchanged and create V5 only if changing the row.
2. Qw / source owner: attach traceable upstream source references (commit/blob or immutable source snapshot) for each fixture; identify actual approver or mark approval explicitly “not granted / fixture only.”
3. Xu: verify blind-process attestation; compute and record actual byte sizes and SHA-256 hashes for every manifest item and the final label artifact; freeze only the exact hashes reviewed.
4. Ka: after Q050 resolution and a verifiable freeze record, adjudicate the final immutable version and sign the per-row decision log.
5. Implementation owner: run the separate acceptance/E2E plan against the intended approved source scope. Do not infer E2E PASS from this labeling review.

## 6. Gate decision
- V4 structure: PASS.
- Fixture corpus classification: PASS (classification is appropriately cautious).
- Row-level adjudication: BLOCKED pending Q050 correction and provenance evidence.
- Xu blind-process attestation and freeze/hash: NOT VERIFIED.
- Retrieval benchmark: NOT VERIFIED.
- Live MCP :8020 -> Core :8000 -> retrieval -> source readback: NOT PASS.
- Work 103: ACTIVE / BLOCKED.

**Signature:** Ka | CSA / Independent Reviewer
