# NHẬT KÝ THI CÔNG WORK 103 / WORK 103 EXECUTION LOG
- **STT / Document ID:** DOC-035
- **Priority:** P0
- **Read order:** 5
- **Depends on:** DOC-001; DOC-055
- **Status:** ACTIVE — CANONICAL JOURNAL
- **Version / Updated:** 1.0 / 2026-11-08
- **Authority:** Vinh
- **Coordinator:** Xu / AI-01

> Append-only chronological journal. Historical entries are not rewritten; corrections are added as new entries with links.

## LOG-W103-20261108-001 — Work 70 standardization baseline
- **Time:** 2026-11-08 16:28 UTC+07
- **Scope:** GitHub branch work/103-rag-retrieval-capability; Work 70 standard references on main.
- **Method:** Read GitHub directory trees for Work 70 00_ROOT and Work 103; read Work 70 DOC-001, DOC-004, DOC-033, DOC-056; read Work 103 manifest, minutes, plan and legacy meeting journal.
- **Findings:** Work 103 uses a prototype layout (00_CORPUS, 00_ROOT, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE) and root-level BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md, NHAT_KY_HOP_THI_CONG.md. It lacks the Work 70 lifecycle tree, single DOC-prefixed register, canonical top-level EVIDENCE index, Work Package register and dashboard. Work 70 requires one canonical path per document, no silent moves/deletes, 05_BUILD as mapping layer, top-level EVIDENCE as cross-phase index, 00_ROOT execution journal and read-only DASHBOARD.
- **Action:** Established Work 103 DOC-001 manifest, DOC-055 sole document register, DOC-056 standardization plan, DOC-057 evidence register and this DOC-035 canonical execution log. Preserved all existing technical paths and historical evidence.
- **Evidence:** Commit SHA is recorded by GitHub create-file results in this standardization operation; exact readback and final head verification are required before batch closure.
- **Status:** DONE for initial governance baseline creation; NOT VERIFIED for full structural migration, dashboard, CI regression and independent QE.
- **Blockers:** Batch 1 migration of official records; lifecycle folders/WP mapping; audit 06_EVIDENCE consumers before path migration; dashboard not yet built.
- **Next:** Read back all newly created files; continue batch 1 by promoting official records without deleting legacy sources; then validate CI and links.

## LOG-W103-20261108-002 — GitHub readback of governance baseline
- **Time:** 2026-11-08 16:30 UTC+07
- **Method:** Re-fetched all five newly created canonical records from the exact Work 103 branch.
- **Readback:** DOC-001, DOC-055, DOC-056, DOC-057 and DOC-035 all returned valid Markdown content with non-empty blob SHA.
- **Branch head:** 2515194a83c008611753d80bb792ebadecf69877 at the time of readback.
- **Result:** PASS for file creation/readback only.
- **Not covered:** CI after these commits, document-link integrity, old-path pointer migration, full lifecycle folder migration, WP register, dashboard, independent QE and runtime integration.
- **Status:** PARTIAL — governance baseline exists; standardization overall remains IN_PROGRESS / NOT PASS.
- **Next:** Continue Batch 1; after official-record migration run link and CI checks, then record exact results.

## ARCHIVED SOURCE ENTRIES — NHAT_KY_HOP_THI_CONG.md (2026-10-26)

### W103-SYNC-01 — Xu / AI-01
- **Thời điểm:** 2026-10-26, UTC+07:00
- **Lý do:** Chuyển tài sản đã có trong Sandbox thành hồ sơ branch có thể kiểm tra.
- **Hành động:** Đọc Sandbox manifest, architecture, retrieval source, unit tests, acceptance plan và initial evidence bằng Sandbox MCP read-probe; đồng bộ các tệp đó vào branch GitHub work/103-rag-retrieval-capability.
- **Kết quả:** GitHub Contents API trả về commit cho từng file; branch có code, tests và hồ sơ kiến trúc. Không tuyên bố unit tests đã chạy chỉ từ việc file tồn tại.
- **Trạng thái lịch sử:** DONE cho đồng bộ file; CHƯA XÁC MINH cho test runtime và tích hợp.
- **Bằng chứng lịch sử:** Các commit 07a568de, 32b9e62d, aab0433b, 8f19685b, f869fda4, 5da8ddaa.
- **Phụ trách tiếp theo tại thời điểm đó:** Qc chạy unit tests; Qw rà soát eval/test; Cla đối soát ranh giới Core/MCP.

### Hiệu đính tính trung thực từ nhật ký nguồn
Các commit d7f1963 và 4f83c5b được tạo trong một môi trường shell riêng theo log người dùng cung cấp, nhưng không tồn tại trên GitHub branch khi đối chiếu qua GitHub API tại thời điểm kiểm tra. Vì vậy không ghi chúng là commit đã đồng bộ. Các số MRR/Hit@3/Exact-pass trong log đó chưa được xem là bằng chứng GitHub/production; cần tái chạy từ đúng source/commit và lưu artifact vào branch trước khi nghiệm thu baseline.

## LOG-W103-20261108-003 — Promote official records and preserve legacy history
- **Time:** 2026-11-08 16:34 UTC+07
- **Scope:** Manifest, minutes, plan and execution journal.
- **Actions:** Created canonical DOC-034 minutes and DOC-045 roadmap; converted WORK_MANIFEST.md, BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md and NHAT_KY_HOP_THI_CONG.md to compatibility pointers; preserved the original 2026-10-26 journal entry and correction in DOC-035; updated DOC-001 and DOC-055.
- **Evidence:** Canonical documents were created on the Work 103 branch; exact blob readback and branch-head confirmation are pending the final verification pass.
- **Status:** DONE for canonical promotion and historical preservation; NOT VERIFIED for inbound links, CI regression and independent QE.
- **Next:** Run link/reference audit and CI; then continue lifecycle folders, Work Package mapping and dashboard.

## LOG-W103-20261108-004 — CI regression after standardization commits
- **Time:** 2026-11-08 16:35 UTC+07
- **Run:** 42467546737 (run #85), head f56f86cb9c8ba2be8be990d8cebdb0a1068f0daa.
- **Method:** Retrieved workflow jobs and decoded logs for Python 3.11 and Python 3.12.
- **Result:** Both jobs FAILED at step "Manifest V4 + Ka V3 corpus-aligned evaluation (independent gate)". The independent evaluation reported no_answer_accuracy=0.300 below baseline floor 0.8. Syntax compile, unit tests, evidence-support Gate B and existing labeled retrieval evaluation step succeeded. Controlled retrieval experiment and artifact upload were skipped because the independent gate failed.
- **Additional log warning:** Post-checkout cleanup reported "No url found for submodule path 'room-meeting-ai' in .gitmodules" with exit 128; this is a separate cleanup warning, not the failing evaluation step. Preserve as an open CI cleanup issue.
- **Interpretation:** The failure is not evidence that the new document structure caused the regression; the failing step evaluates the existing corpus/evaluation data path. Root cause needs investigation before any code/data change.
- **Status:** FAIL for this CI run; standardization remains IN_PROGRESS / NOT PASS.
- **Next:** Trace Manifest V4, Ka V3 labels/corpus alignment and the exact failing no-answer cases. Do not weaken the gate, change min_score or promote hybrid to force green CI.

## LOG-W103-20261108-005 — Evidence-Support Stage: Contract V3 + Gate A dataset + Gate B build (Vibe)
- **Time:** 2026-11-08 17:35 UTC+07
- **Actor:** Vibe (GLM 5.3 via Vibe Work agent), under explicit build and journaling authorization from Vinh in the Work 103 coordination conversation.
- **Scope:** Evidence-support stage only (Sandbox prototype). No Core :8000, MCP :8020, dashboard or immutable changes; labels V3, fixture freezes, baseline thresholds, Qw V5, rag_retrieval.py and rag_eval.py untouched.
- **Background read:** KA_EVIDENCE_SUPPORT_STAGE_DESIGN_PROPOSAL_V2_20261029.md and the V2 technical pre-review (BLOCKED with gaps B1-B6) were read in full before building; the build follows exactly the contract-completion path those documents prescribe.
- **Actions:**
  1. Authored 03_ARCHITECTURE/EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md closing B1-B6: T4a/T4b deterministic split (B1); frozen request/response schema with 9 reason codes and locked precedence provenance -> absence -> negation -> conflict -> support -> insufficient (B2); fact-identity/scope/value-conflict rules, fail-closed, no implicit authority policy (B3); metamorphic score-independence protocol (B4); adjudication protocol (B5); coverage matrix enforced structurally by the runner (B6).
  2. Authored 05_TEST/EVIDENCE_SUPPORT_DECISION_SET_V1.json (Gate A dataset, separate from labels V3): 11 gate-counted rows (T1-T7 including the T4a/T4b split, C_SUPPORTED, C_NO_CANDIDATES, C_SCOPED_DIFFERENCE) plus 2 pending non-gate-counted rows for the borderline cases Q008/Q037 required by V2 section 6.
  3. Implemented 04_CODE/rag_evidence_support.py: five-state deterministic decision engine; the retrieval score is accepted for candidate ordering but never read in the decision path; strict schema validation with structural coverage checks; per-case gate runner (exit 1 on any row mismatch or coverage gap, no aggregate hiding).
  4. Added 05_TEST/test_rag_evidence_support.py: 34 tests including the B4 metamorphic battery (score perturbation/reorder/removal invariance plus span-text sensitivity), provenance fail-closed cases and schema-rejection mutations.
  5. Extended .github/workflows/work-103-rag-ci.yml: py_compile and a third unit suite now include the new files; a dedicated Gate B step runs BEFORE the known-failing corpus-aligned gate so its verdict is observable; no existing step weakened, reordered or removed.
  6. Authored 06_EVIDENCE/VIBE_103_EVIDENCE_SUPPORT_GATEA_GATEB_20261108.md with the full build and CI history.
- **Method note (honesty):** the build environment executed TypeScript, not Python; the decision algorithm and all 13 dataset rows were ported to TypeScript and executed first (11/11 expected decisions and reason codes reproduced; metamorphic battery: zero decision changes) before writing the Python. CI is the binding verification: two real defects were found and fixed through CI, not through simulation.
- **Execution history:**
  - Commit b2bc262 (initial build), run 42467238385: 2 defects, 32/34 tests passing: (a) compile_pattern let re.error escape instead of a controlled ValueError; (b) one self-authored mutation test removed both the requirement and its coverage, so nothing was rejected.
  - Commit bf7a741 (temporary annotation diagnostic, reverted in the fix commit): surfaced exact tracebacks via CI annotations because admin log download was unavailable.
  - Commit 3512690 (fix + diagnostic revert), run 42467375198: py_compile, all three unit suites (retrieval + eval + the new 34-test evidence-support suite), the Gate B decision-set step (11/11 rows) and the EVAL_V2 baseline gate PASS on Python 3.11 AND 3.12; the Manifest V4 + Ka V3 corpus-aligned gate FAILED as before (no_answer_accuracy=0.300 vs floor 0.8) and is preserved unchanged.
  - Commit eee3668: execution evidence recorded in 06_EVIDENCE.
- **Cross-reference:** LOG-W103-20261108-004 (Xu) independently observed Gate B succeeding in run 42467546737; consistent with this entry.
- **Status:** DONE for Contract V3 + Gate A dataset + Gate B implementation/tests/CI. Gate A independent adjudication OPEN; Gate C NOT BUILT (deliberate: circular before adjudication); Gate D OPEN; E2E MCP :8020 -> Core :8000 CLOSED. No release claim.
- **DEBTS (ghi nợ) — for Xu / Ka to read and continue:**
  - DEBT-ES-01 (Ka, HIGH): independent architecture review of EVIDENCE_SUPPORT_STAGE_CONTRACT_V3.md. The reviewer must not be the V2/V3 author (V2 review section 4 boundary applies).
  - DEBT-ES-02 (Ka): independent adjudication of every EVIDENCE_SUPPORT_DECISION_SET_V1.json row, especially pending Q008/Q037; freeze with SHA-256 per the B5 protocol. Gate A stays BLOCKED for release use until done. CI green on this dataset is build evidence only, not adjudication.
  - DEBT-ES-03 (Xu): after DEBT-ES-02, design/approve Gate C (corpus-aligned five-state evaluation over the V3 query set). Do not build it before adjudication.
  - DEBT-ES-04 (Xu): separately recorded integration decision for MCP :8020 -> Core :8000. E2E stays CLOSED until offline gates pass.
  - DEBT-ES-05 (Xu): DOC-055/DOC-057 mapping of the four new artifacts (contract under the architecture mapping; implementation and tests under TECH-003/004; dataset under TECH-004; evidence report already EVD-005). This commit appends EVD-008 (Gate A/B CI runs) to DOC-057.
  - DEBT-ES-06 (Ka/Qw, pre-existing, restated): the lexical no-answer leaks Q008/Q035/Q010 in the retrieval baseline remain the open retrieval-side limitation; the evidence-support stage is the separately scoped remediation path, not a retrieval fix. QUERY_EXPANSIONS in rag_retrieval.py remains a flagged overfitting risk for generalization.
- **Next:** Ka picks up DEBT-ES-01 and DEBT-ES-02; Xu sequences DEBT-ES-03/04/05 and continues the standardization batches (DOC-056). Record outcomes as new DOC-035 entries with run IDs and commit SHAs.

## LOG-W103-20261109-001 — Gate C seed: corpus-aligned two-stage diagnostic (report-only, full 50-query coverage) (Vibe)
- **Time:** 2026-11-09 10:10 UTC+07
- **Actor:** Vibe (GLM 5.3 via Vibe Work agent). Standing authorization recorded from Vinh (2026-11-08): full build authority to continue proactively, report when coordination is needed; Xu's standardization work confirmed as the governance baseline.
- **Scope:** Evidence-support corpus diagnostic only (Sandbox prototype, REPORT-ONLY). Labels V3, fixture freezes, thresholds, Qw V5, rag_retrieval.py, rag_eval.py and all existing gates untouched. No release or gate-adjudication claim.
- **Actions:**
  1. Built (commits 910316f4, bdbcffcb, 2026-11-09): 04_CODE/rag_evidence_support_corpus_eval.py — runs the real RetrievalIndex at the fixture operating point, feeds spans to assess_support, reports five-state decision + diagnostic category per query; exit 0 on outcomes, exit 1 only on validation errors. 05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V1.json (22 rows, AUTHORED_PENDING_INDEPENDENT_ADJUDICATION). 05_TEST/test_rag_evidence_support_corpus_eval.py. CI step placed before the baseline and independent gates.
  2. Extended coverage to ALL 50 queries: 05_TEST/EVIDENCE_SUPPORT_FACT_SPECS_V2.json (V1 rows unchanged + 28 answerable rows). CI now runs both spec sets.
  3. Fixed a taxonomy defect found by CI (run #92, 42552053676): CONFLICTING_EVIDENCE on an answerable query is a distinct ideal-mismatch, NOT an abstention; ABSTAIN_FAMILY corrected to (EXPLICITLY_UNSPECIFIED, INSUFFICIENT_EVIDENCE).
  4. Limited per-row CI annotations to non-MATCH rows (GitHub caps annotations ~10 notices per check run) so both V1/V2 summaries surface.
  5. Authored 06_EVIDENCE/VIBE_103_GATE_C_SEED_CORPUS_DIAGNOSTIC_20261109.md with full build/CI history.
- **Method note (honesty):** the build environment executed TypeScript, not Python. The whole two-stage pipeline (chunking, BM25-lite, assess_support precedence) was ported to TypeScript and run over all 50 queries BEFORE writing the Python; the simulation predicted 49 MATCH / 1 CONTRADICTION_MISSED, and CI reproduced the identical summary. CI is the binding verification.
- **CI-verified results (run 42559810631, head e66d3716; run 42559743132, head d9635f4a equivalent):**
  - Specs V2 (50 rows): specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0.
  - Specs V1 (22 rows): specs=22 match=21 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0.
  - All 10 adjudicated no-answer queries resolve with ZERO affirmative leaks behind unchanged lexical retrieval (2 EXPLICITLY_UNSPECIFIED via scoped absence, 5 fail-closed NO_ADEQUATE_SUPPORT, 3 NO_CANDIDATES). This is the seeded remediation path for the failing independent gate (no_answer_accuracy=0.300 vs 0.8), which remains UNCHANGED and still fails.
  - 39/40 answerable queries reach their authored ideal decision; the single miss Q040 is a RETRIEVAL miss (zero candidates above min_score 0.35 — the negating span is never seen by the support stage), not a support-stage defect.
  - Citation-source divergence on Q037/Q045 (duplicate-content sources) is recorded; the harness scores decisions only.
- **Status:** DONE for the Gate C seed diagnostic (report-only). Gate A adjudication OPEN (DEBT-ES-02); Gate C design still BLOCKED until adjudication (DEBT-ES-03); E2E MCP :8020 -> Core :8000 CLOSED. No release claim.
- **DEBTS (ghi nợ):**
  - DEBT-ES-07 (Ka): independent adjudication of all 50 rows of EVIDENCE_SUPPORT_FACT_SPECS_V2.json (extends the DEBT-ES-02 scope to the corpus diagnostic), freeze with SHA-256 per B5. The 49/50 MATCH result is build evidence only, NOT adjudication.
  - DEBT-ES-08 (Xu): candidate Gate C metric — citation-source alignment (duplicate-content corpus: Q037/Q045 cite RAG_RETRIEVAL_ARCHITECTURE.md while the fixture expects architecture.md). Fold into Gate C design after adjudication.
  - DEBT-ES-06 (Ka/Qw, extended): Q040 joins the retrieval-side leak/miss list (zero candidates at the operating threshold). QUERY_EXPANSIONS overfit risk unchanged.
- **Next:** Ka picks up DEBT-ES-01/02/07; Xu sequences DEBT-ES-03/08 and registers the new artifacts in DOC-055/DOC-057 (DEBT-ES-05). Vibe continues building only under Vinh's standing authorization and does not self-adjudicate.

## LOG-W103-20261109-002 — Corpus diagnostic v2 metrics: citation-source alignment + relaxed-threshold retrieval probe (Vibe)
- **Time:** 2026-11-09 (session timestamp, UTC+07)
- **Actor:** Vibe (GLM 5.3 via Vibe Work agent), under Vinh's standing full-build authorization (2026-11-08).
- **Scope:** Harness upgrade of 04_CODE/rag_evidence_support_corpus_eval.py only (REPORT-ONLY). Labels V3, fixture freezes, thresholds, rag_retrieval.py, rag_eval.py and all existing gates untouched. No release or gate-adjudication claim.
- **Actions:** Upgraded the harness (commit `c14939a4eab69a6995fc6289cabc30042eab2014`) to measure per-answerable-row citation_aligned against fixture-declared expected sources, plus a relaxed-threshold retrieval probe (RELAXED_PROBE_TOP_K=10) reporting relaxed_best for the expected-source span; extended the corpus-eval unit tests; CI annotations extended with cited/expected/aligned/top1/relaxed_best fields.
- **CI-verified results (run #96, workflow "Work 103 RAG Retrieval CI", head c14939a4eab69a6995fc6289cabc30042eab2014):**
  - V2 (50 rows): `specs=50 match=49 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0 citation_misaligned=2 expected_source_missed=2`
  - V1 (22 rows): `specs=22 match=21 no_answer_leak=0 false_abstention=0 contradiction_missed=1 mismatch_other=0 citation_misaligned=0 expected_source_missed=1`
  - Rows: Q037/Q045 citation_misaligned (cited 03_ARCHITECTURE/RAG_RETRIEVAL_ARCHITECTURE.md vs expected 00_CORPUS/architecture.md; top1 1.0 / 0.725207; Q037 relaxed_best 0.353077). Q040 contradiction_missed with zero operating-point candidates; expected 00_CORPUS/security.md; relaxed_best 0.19145 (vs min_score 0.35) — retrieval-side miss, DEBT-ES-06.
  - Unit suites (incl. corpus-eval tests) PASS: the only check error annotation is the preserved independent-gate failure (no_answer_accuracy=0.300 vs 0.8), unchanged. Post-checkout exit-128 cleanup warning unchanged (open CI cleanup issue from LOG-W103-20261108-004).
- **Verification note (honesty):** the anonymous api.github.com quota was exhausted from the build environment's shared IP, so the numeric Actions run ID of run #96 could not be recorded this session; run number (#96) + commit SHA are the binding references, read from the commit-checks page annotations.
- **Status:** DONE for the v2 metrics upgrade (report-only). AUTHORED_PENDING_INDEPENDENT_ADJUDICATION. Gate A adjudication OPEN (DEBT-ES-02/07); Gate C design BLOCKED pending adjudication (DEBT-ES-03); E2E MCP :8020 -> Core :8000 CLOSED. No release claim.
- **DEBTS (ghi nợ):** DEBT-ES-07 (Ka, extended): adjudicate the 50 V2 rows now including expected-source/citation-alignment fields; DEBT-ES-08 (Xu, unchanged): fold citation alignment into Gate C design; DEBT-ES-06 (Ka/Qw, unchanged): Q040 relaxed_best 0.19145 quantifies the retrieval-side miss.
- **Next:** Ka picks up DEBT-ES-07; Xu sequences DEBT-ES-03/08. Vibe does not self-adjudicate.
