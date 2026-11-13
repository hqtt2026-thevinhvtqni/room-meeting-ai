# KẾ HOẠCH CHUẨN HÓA WORK 103 THEO WORK 70
- **STT / Document ID:** DOC-056
- **Priority:** P0
- **Read order:** 3
- **Depends on:** DOC-001; DOC-055
- **Status:** ACTIVE — BATCH 0 COMPLETE / BATCH 1 IN PROGRESS / BATCH 5 IN PROGRESS
- **Version / Updated:** 1.1 / 2026-11-09
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Governing standard
Work 103 adopts Work 70 lifecycle, gate matrix, Work Package model, document naming/storage rules, one-register rule, canonical evidence path, read-only dashboard contract and evidence-backed journal process. Work-specific RAG technical gates remain subordinate to G0–G9.

## 2. READ → TRACE → ANALYZE
Initial GitHub inventory was read from branch work/103-rag-retrieval-capability. Existing top-level layout contains 00_CORPUS, 00_ROOT, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE and three root-level legacy records. This is a technically useful prototype layout but not aligned with Work 70 lifecycle ownership.

Existing CI, imports and tests may depend on 04_CODE, 05_TEST and 06_EVIDENCE. Folder movement is not cosmetic: first map workflow references, imports, relative paths, evidence links and source consumers. No source or evidence files are moved/deleted in Batch 0.

## 3. Migration batches
| Batch | Scope | Actions | Exit evidence | Status |
|---|---|---|---|---|
| 0 | Read/trace and governance baseline | Inventory current tree; establish DOC-001, sole DOC-055 register, this plan and canonical EVIDENCE index; preserve legacy paths | Exact GitHub readback and commit SHA | DONE |
| 1 | 00_ROOT and official records | Promoted manifest, minutes, plan and execution journal to DOC-prefixed canonical paths; converted four old paths to compatibility pointers; registered records | Content/history preservation confirmed; inbound-link audit and CI regression still pending | IN_PROGRESS |
| 2 | Lifecycle folders | Classify corpus originals, reference docs, architecture, requirements, plans, tests and acceptance evidence into 01_DISCOVER–07_ACCEPT; preserve code/test paths through mappings | Full old→new path map; no broken imports/CI | NOT_STARTED |
| 3 | 05_BUILD engineering map | Create Work Package register and mapping records for source, tests, CI and evidence; define exact canonical source repo/path/branch/commit | WP completeness and source mapping validation | NOT_STARTED |
| 4 | EVIDENCE migration | Audit all links, workflow paths and consumers of 06_EVIDENCE; migrate canonical index to EVIDENCE/ without duplicate independent copies; retain compatibility pointers | Link checker, workflow pass, hash/readback | NOT_STARTED |
| 5 | DASHBOARD | Build read-only Work Execution dashboard and Product dashboard where applicable; derive data from canonical Manifest/Register/WP/Gates/Evidence; no mock values | Schema validation, live source readback, browser verification | IN_PROGRESS — DOC-058 created 2026-11-09; exit evidence NOT yet complete |
| 6 | VERIFY / ACCEPT / RELEASE readiness | Independent QE validates structure, registers, links, lifecycle gates, dashboard and CI | Signed verification evidence and gate decision | NOT_STARTED |

## 4. Non-destructive migration rules
1. Never bulk rename, delete, reset, clean or overwrite source/evidence as a first step.
2. Preserve all current CI paths and imports until dependency tracing proves a safe migration.
3. Every old path maps to one canonical path or is explicitly marked retained legacy.
4. Never duplicate an official record as two independently editable sources.
5. Retain historical evidence and failed runs; do not rewrite them as success.
6. Do not move or relabel historical decisions. Supersede with a new decision record if required.
7. All edits are committed on work/103-rag-retrieval-capability; do not merge to main or alter other Works as part of this task.
8. Exact GitHub readback is required after each batch. CI success proves only the workflow checks actually executed, not dashboard, integration or release readiness.

## 5. Current decisions retained
- Experimental operating min_score remains 0.35; 0.45 remains candidate only.
- Hybrid retrieval is not selected.
- Blind candidate pool V1 remains unlabeled until independent annotation and adjudication are complete.
- Integration remains BLOCKED; Release remains NOT PASS.
- Do not report new-set metrics until labels are frozen and hashed.

## 6. Acceptance criteria for standardization
- One canonical Manifest and one Document Register.
- Four official records have one canonical owner each: minutes, plan, architecture/model (when needed), execution journal.
- Lifecycle folder ownership follows Work 70.
- 05_BUILD contains mappings/coordination, not duplicate canonical source or official records.
- Cross-phase evidence has one canonical EVIDENCE index.
- All controlled docs follow DOC-ID and filename conventions; technical exceptions are registered.
- Work Packages, gate criteria and evidence traceability are inspectable.
- Dashboard is read-only and source-backed.
- No source/test/CI regression; exact CI and readback evidence recorded.
- Independent QE completes before declaring standardization PASS.


## Batch 1 progress note — 2026-11-08
Canonical DOC-034 minutes and DOC-045 plan were created from the legacy records. DOC-035 now preserves the earlier 2026-10-26 journal entry and its integrity correction. WORK_MANIFEST.md, BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md and NHAT_KY_HOP_THI_CONG.md are now compatibility pointers. This promotion does not close Batch 1: link integrity and CI regression remain unverified.

## CI regression note — 2026-11-08
The first CI run after the governance/official-record commits is run 42467546737 (head f56f86cb9c8ba2be8be990d8cebdb0a1068f0daa). Both Python 3.11 and 3.12 jobs failed at the independent Manifest V4 + Ka V3 corpus-aligned evaluation gate: no_answer_accuracy=0.300 against the required floor 0.8. Unit tests, syntax, Gate B and existing labeled retrieval evaluation step succeeded. This is recorded as EVD-007 and DOC-035 LOG-W103-20261108-004. Do not attribute the failure to document migration without evidence; investigate the dataset/gate separately. Batch 1 remains open pending link audit and a passing CI run or documented disposition.

## Batch 5 progress note — 2026-11-09
DASHBOARD/DOC-058_DASHBOARD_WORK-103-EXECUTION.md created (producer: Vibe, under Vinh's standing full-build authorization). Read-only projection: every displayed value cites canonical sources (DOC-001/DOC-055/DOC-057/DOC-035 evidence IDs and CI run references); no mock values; dashboard status explicitly states that no gate PASS is claimed. Registered in DOC-055 as DOC-058 / DASH-001 (CREATED / NOT_VERIFIED). Batch 5 exit evidence — schema validation, live source readback and browser verification — is NOT yet complete; the batch remains IN_PROGRESS. Verification note: this commit is docs-only; no CI behaviour change is claimed.

### Batch 5 verification progress — 2026-11-09 (Vibe, LOG-W103-20261109-006)
Schema validation and live source projection checks of DOC-058 against DOC-001/DOC-055/DOC-056/DOC-057/DOC-035 at head c4fc5010f540badb793a0bde06d24cf37e226e2d: PASS (details in DOC-035 LOG-W103-20261109-006). CI at that head: unit suites PASS on Python 3.11/3.12; independent gate FAIL 0.300 vs 0.8 preserved; diagnostic summaries identical to run #96. Browser verification of DOC-058 remains outstanding — Batch 5 stays IN_PROGRESS / NOT VERIFIED until it is done and DEBT-ES-05 closure is confirmed by Xu.


## Batch 2 progress note — 2026-11-09 (Vibe, LOG-W103-20261109-007)
Batch 2 chuyển NOT_STARTED → IN_PROGRESS: path & dependency map hoàn tất trong DOC-059 (CI consumers C1..C9, code-internal dependencies, 6 ràng buộc di chuyển, ánh xạ old→new đề xuất). KHÔNG có file nào được di chuyển trong bước prep này; việc di chuyển phải là một commit duy nhất đồng bộ CI theo DOC-059 §3, kèm readback + CI disposition. Lưu ý dữ liệu: source_id trong fixture là định danh logic, không đụng khi di chuyển thư mục.


## Batch 2 progress note — 2026-11-09 (Vibe, LOG-W103-20261109-008)
Lifecycle skeleton (01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 06_VERIFY, 07_ACCEPT, 08_RELEASE, 09_OPERATE) tạo xong với README classification index tham chiếu DOC-059. Phân loại: 00_CORPUS = originals + curated fixture (cần phân loại trước khi di chuyển); 02_EXTENSION = reference; 03_ARCHITECTURE → 03_ARCHITECT (deferred, source_id logic); 05_TEST/04_CODE = declared legacy source layout (giữ nguyên); 06_EVIDENCE → EVIDENCE (Batch 4, CI write target). Full old→new path map = DOC-059; no broken imports/CI (không có di chuyển vật lý). Batch 2: mapping/classification DONE, physical moves DEFERRED — batch IN_PROGRESS cho tới khi di chuyển hoặc có disposition văn bản.

## Batch 3 progress note — 2026-11-09 (Vibe, LOG-W103-20261109-008)
05_BUILD/DOC-060 WP register tạo xong: WP-103-01..08 với owner/reviewer/dependencies/deliverables/acceptance criteria/status/evidence theo DOC-001 §6. 05_BUILD chỉ chứa mapping/coordination. Batch 3 exit evidence (WP completeness + source mapping validation): register complete; source mapping validation = DOC-059 §1/§2; chờ Xu xác nhận trước khi đóng batch.
