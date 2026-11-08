# WORK MANIFEST — WORK 103
- **STT / Document ID:** DOC-001
- **Priority:** P0
- **Read order:** 1
- **Depends on:** NONE
- **Status:** ACTIVE
- **Version / Updated:** 1.0 / 2026-11-08
- Work ID: 103
- Work Name: ROOM-HOP-RAG-RETRIEVAL-CAPABILITY
- Product: Evidence-grounded RAG retrieval capability for ROOM-HOP
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu (AI-01)
- Canonical repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Canonical working branch: work/103-rag-retrieval-capability
- Source-of-truth policy: GitHub branch + immutable commit for versioned source and records; Sandbox is execution/working environment, not an independent source of truth.
- Standard baseline: Work 70 lifecycle, gate, Work Package, evidence, document, naming, register and dashboard standards.

## 1. Purpose and scope
Build an evidence-grounded Retrieval-Augmented Generation (RAG) capability for ROOM-HOP, reusable by Work 91 Harness and other authorized Core capabilities. Work 103 owns retrieval capability and its acceptance evidence; it does not own Core identity/authorization or Work 28 MCP platform.

## 2. Architecture boundaries
- Core :8000 remains the single source of truth.
- Work 28 owns MCP platform/tool contracts. Work 103 consumes only approved contracts.
- Dashboard :3000 is read-only/render-only.
- No second Core, no direct AI-to-filesystem/database access, no independent production RAG port.
- Begin with source-aware lexical retrieval and metadata. Embeddings/vector database require measured evaluation benefit and a recorded decision.
- Retrieved content is untrusted input; embedded instructions must never be executed. Insufficient evidence requires abstention.
- Historical architecture statements mentioning MCP :8020 are legacy references only, not instructions to activate or depend on that endpoint. Confirm the current approved integration contract before G4.

## 3. Canonical top-level structure
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD.

## 4. Canonical ownership
- 00_ROOT: Manifest, sole Document Register, Decision Log, minutes and Work-wide chronological execution journal.
- 01_DISCOVER: original inputs, problem/context discovery and findings.
- 02_DEFINE: requirements, scope, success metrics and acceptance criteria.
- 03_ARCHITECT: approved RAG architecture, data flow, trust boundaries, schemas and interfaces.
- 04_PLAN: master implementation roadmap, Work Packages, owners and dependencies.
- 05_BUILD: engineering mapping/coordination only; not canonical source-code or official-record storage.
- 06_VERIFY: verification strategy, test procedures and checklists.
- EVIDENCE: single cross-phase evidence index and verified evidence references.
- 07_ACCEPT: acceptance decision and record.
- 08_RELEASE: release manifest and approval.
- 09_OPERATE: operational procedures, monitoring and incident records.
- DASHBOARD: read-only projection of canonical Work records.
- Canonical code/tests remain in explicitly declared source mappings. Current implementation is physically under 04_CODE and tests under 05_TEST as a legacy source layout pending controlled migration. No source move in this batch.

## 5. Canonical Work records
- Minutes: 00_ROOT/DOC-034_BIEN-BAN_HOP-WORK-103-MINUTES.md (canonical; BIEN_BAN.md is a compatibility pointer).
- Plan: 04_PLAN/DOC-045_KE-HOACH-THI-CONG_WORK-103-ROADMAP.md (canonical; KE_HOACH_THI_CONG_XU.md is a compatibility pointer).
- Architecture/model: 03_ARCHITECT/ (existing architecture content to be classified and registered).
- Execution journal: 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-103-EXECUTION-LOG.md.
- Evidence: EVIDENCE/ (cross-phase register); existing 06_EVIDENCE/ is legacy compatibility location until link/CI migration is verified.

## 6. Work packages and gates
Work Packages are registered at Work level in 04_PLAN. Every WP must have owner, reviewer, dependencies, deliverables, acceptance criteria, status and evidence links.
Apply lifecycle gates G0–G9 from Work 70. Work-specific technical gates G1–G5 remain subordinate acceptance criteria; they do not replace lifecycle gates.
No evidence, no PASS. Unknown, stale, contradictory or unverified evidence is NOT_READY/BLOCKED, never PASS.

## 7. Current verified baseline (2026-11-08)
- GitHub branch contains RAG source, tests, architecture, corpus, evaluation sets and historical evidence.
- CI run 40668733280 for head 5f91f3ea2143dafaa5af958dc2bb431399e93621 was confirmed SUCCESS by user; EVAL_V2 and both unit suites green at that head.
- Blind candidate pool V1 contains 50 unlabeled questions; it is not a frozen labeled evaluation set.
- Existing experiment evidence is historical and uses the previous labeled set. It is not evidence from the blind pool.
- min_score 0.35 remains experimental operating value; 0.45 is candidate only; hybrid is not selected.
- Integration gate: BLOCKED. Release: NOT PASS.
- Independent label freeze and new-set evaluation are not complete.
- Dashboard: NOT IMPLEMENTED/NOT VERIFIED in this Work baseline.

## 8. Migration invariants
- One DOC-ID, one canonical path, one Document Register.
- Controlled documents use Vietnamese-first, English-second ASCII filenames with DOC-NNN prefix. Technical/runtime filenames are registered exceptions.
- Do not silently delete, rename, move or overwrite legacy files. Inventory and map first; preserve CI paths and inbound links; migrate in controlled batches.
- Top-level EVIDENCE/ is canonical. Existing 06_EVIDENCE/ remains legacy until a complete reference audit and validation.
- Dashboard is read-only and derives from canonical records; no mock status data.
- Every action, test, command, result, evidence reference, PASS/FAIL/BLOCKED and next step must be written to the canonical execution journal.
- Dashboard progress never substitutes for gate decisions.

## 9. Read order
DOC-001 Manifest → DOC-055 Document Register → DOC-056 Standardization/Migration Plan → current lifecycle phase records → DOC-035 Execution Journal → relevant evidence and source mappings.
