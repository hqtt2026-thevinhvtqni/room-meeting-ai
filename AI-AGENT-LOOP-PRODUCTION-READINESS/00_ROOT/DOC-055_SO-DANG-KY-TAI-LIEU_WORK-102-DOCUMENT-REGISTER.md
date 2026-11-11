# DOCUMENT REGISTER — WORK 102
- Document ID: DOC-055 | Priority: P0 | Read order: 9 | Version: 1.4
- Status: ACTIVE — SINGLE CANONICAL REGISTER | Owner: Xu / AI-01 | Authority: Vinh
Rule: one controlled document = one DOC-ID + one canonical path. Legacy artifacts are preserved and classified; they are not duplicate canonicals.

| DOC-ID | Priority | Read order | Canonical path | Purpose | Status |
|---|---|---:|---|---|---|
| DOC-001 | P0 | 1 | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | Identity, authority, scope | ACTIVE |
| DOC-034 | P0 | 2 | 00_ROOT/DOC-034_BIEN-BAN_CHUAN-HOA-WORK-102-MINUTES.md | Standardization decision record | RECORDED |
| DOC-003 | P0 | 3 | 00_ROOT/DOC-003_CAU-TRUC-KHO-VA-DONG-BO_REPOSITORY-LAYOUT-AND-SYNC.md | Layout and sync | ACTIVE |
| DOC-004 | P0 | 4 | 00_ROOT/DOC-004_MA-TRAN-CONG-VONG-DOI_LIFECYCLE-GATE-MATRIX.md | Lifecycle gates | ACTIVE |
| DOC-005 | P0 | 5 | 00_ROOT/DOC-005_MAY-TRANG-THAI_WORK-STATE-MACHINE.md | Work state machine | ACTIVE |
| DOC-006 | P0 | 6 | 00_ROOT/DOC-006_SO-QUYET-DINH_DECISION-LOG.md | Decisions | ACTIVE |
| DOC-033 | P0 | 7 | 00_ROOT/DOC-033_TIEU-CHUAN-TAI-LIEU-VA-LUU-TRU_WORK-DOCUMENTATION-AND-STORAGE-STANDARD.md | Storage standard | ACTIVE |
| DOC-035 | P0 | 8 | 00_ROOT/DOC-035_NHAT-KY-THI-CONG_WORK-EXECUTION-LOG.md | Canonical journal | ACTIVE |
| DOC-055 | P0 | 9 | 00_ROOT/DOC-055_SO-DANG-KY-TAI-LIEU_WORK-102-DOCUMENT-REGISTER.md | Single register | ACTIVE |
| DOC-007 | P1 | 10 | 01_DISCOVER/DOC-007_BAO-CAO-KHAM-PHA_DISCOVERY-BRIEF.md | Discovery brief | BASELINE |
| DOC-008 | P1 | 11 | 02_DEFINE/DOC-008_YEU-CAU-SAN-PHAM_PRODUCT-REQUIREMENTS.md | Requirements | BASELINE |
| DOC-009 | P1 | 12 | 03_ARCHITECT/DOC-009_KIEN-TRUC_AGENT-LOOP-ARCHITECTURE.md | Architecture synthesis | BASELINE |
| DOC-011 | P1 | 13 | 04_PLAN/DOC-011_KE-HOACH_IMPLEMENTATION-ROADMAP.md | Plan and milestones | ACTIVE |
| DOC-014 | P1 | 14 | EVIDENCE/DOC-014_SO-DANG-KY-BANG-CHUNG_EVIDENCE-REGISTER.md | Sole cross-phase evidence register | ACTIVE — 61 HISTORICAL FILES COPIED/READ-BACK; LEGACY RETIREMENT OPEN |
| DOC-015 | P1 | 15 | 06_VERIFY/DOC-015_KE-HOACH-KIEM-CHUNG_VERIFICATION-PLAN.md | Verification plan | ACTIVE |
| DOC-016 | P0 | 16 | 07_ACCEPT/DOC-016_CHECKLIST-NGHIEM-THU-PC_PC-ACCEPTANCE-CHECKLIST.md | Current safe PC acceptance plan | DRAFT |
| DOC-036 | P1 | 17 | 05_BUILD/00_ROOT/DOC-036_SO-DO-ANH-XA_BUILD-MAPPING-REGISTER.md | Source and legacy mapping | ACTIVE |
| DOC-037 | P1 | 18 | 05_BUILD/00_ROOT/DOC-037_DANH-MUC-ARTIFACT-LEGACY_LEGACY-ARTIFACT-PATH-INVENTORY.md | Path inventory for legacy reconciliation | ACTIVE — PATH ONLY |

## Legacy / technical artifact classification
- 00_ROOT/WORK_MANIFEST.md remains an unconverted legacy manifest; DOC-001 is canonical. Convert the old path to a compatibility pointer only after preserving exact original content and checking inbound links.
- 01_PLAN/PLAN_WORK102_v1.0.md is the legacy source for DOC-011; preserve pending controlled reconciliation.
- 03_ARCHITECTURE/* are legacy architecture source inputs for DOC-009; preserve.
- 04_CODE/* are source candidates; canonical Git ref NOT VERIFIED.
- 05_TEST/* are test source candidates; preserve.
- Former top-level 06_EVIDENCE/* are legacy historical evidence and supporting artifacts; preserve in place pending individual content/hash/link audit and controlled migration to EVIDENCE/ or 06_VERIFY/ according to artifact class. No new canonical records there.
- 06_VERIFY/* owns verification plans, procedures and test definitions; DOC-015 is canonical.
- 05_BUILD/06_EVIDENCE/* is temporary build-stage staging only.
- 07_RELEASE/* are PC acceptance/handoff materials; not release proof.
- 01_ORIGINAL/* and 02_EXTENSION/* are legacy staging areas mapped to 05_BUILD equivalents.
- 07_ENVIRONMENT/* is legacy environment/test tooling mapped to 05_BUILD/05_TEST staging; inspect scripts before execution.
- root 10_AI_DEBUG_HANDOFF/* is legacy; canonical intake is 05_BUILD/10_AI_DEBUG_HANDOFF.
- sibling 06_EVIDENCE/WORK_102_ENGINEERING_JOURNAL_20261015.md is a legacy journal; preserve and cross-reference. Canonical Work journal is DOC-035.
- README.md, transcript.md, source, tests, scripts, schemas, run bundles and __pycache__ are technical/generated artifacts; do not assign fake DOC IDs.
- DASHBOARD/README.md and 09_DASHBOARD_PREVIEW/README.md are status/readme artifacts, not implemented dashboard products.
DOC-037 is a path-level inventory only; it does not certify content, file type, hashes or canonical source. The register is an initial controlled-document index, not a claim that every legacy artifact has been reconciled.

## Section 6 normalization addendum — 2026-11-07
The Work 70 v1.2 canonical layout is now reflected in the register: DOC-014 is owned by top-level EVIDENCE/; DOC-015 remains under 06_VERIFY/; 05_BUILD/06_EVIDENCE/ is staging only; former top-level 06_EVIDENCE/ is legacy-only. Existing raw files remain preserved. File-level migration of the 72 legacy path entries remains OPEN and requires per-artifact classification, integrity checks, inbound-link review and independent QE.


## 2026-11-08 — Bắt buộc đồng bộ cấu trúc theo Work 70 v1.3 (Xu / AI-01)

**Nguồn chuẩn:** Work 70 DOC-001 v1.5, DOC-003 v1.2 và DOC-056 mục 8 đã được cập nhật trong Sandbox Work 70.

**Quy tắc áp dụng cho Work 102:** root lifecycle phải theo đúng thứ tự `00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD`. EVIDENCE là thư mục không đánh số. Chỉ 06_VERIFY mang số 06 ở Work root. Bên trong 05_BUILD, numbering được tính độc lập theo cấp cha; không được để hai thư mục cùng cấp dùng chung số.

**Sai lệch phát hiện từ Sandbox inventory hiện tại:**
- Root đồng thời có 06_EVIDENCE và 06_VERIFY.
- Root đồng thời có 07_ACCEPT, 07_ENVIRONMENT và 07_RELEASE.
- Root đồng thời có 08_DASHBOARD và 08_RELEASE.
- Root đồng thời có 09_DASHBOARD_PREVIEW và 09_OPERATE.
- Các khu vực kỹ thuật 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 04_PLAN, 05_TEST và 10_AI_DEBUG_HANDOFF đang nằm lẫn ở Work root, không đồng nhất với ranh giới 05_BUILD của Work 70.
- Đã tồn tại EVIDENCE/DOC-014 làm đích sổ bằng chứng mới; 06_EVIDENCE chứa lịch sử/bằng chứng cũ. Không xóa hoặc ghi đè dữ liệu lịch sử.

**Quyết định quy hoạch:**
1. Chuẩn root Work 102 phải trùng Work 70; không phát minh một lifecycle riêng.
2. EVIDENCE/ là đích canonical duy nhất cho cross-phase evidence; DOC-014 tại EVIDENCE/ được giữ làm sổ canonical tạm thời, chờ cập nhật DOC-055 và inbound links.
3. 06_EVIDENCE/ được phân loại LEGACY, cấm tạo file mới; chỉ retire sau khi từng file được inventory, copy/migrate, đối chiếu nội dung/hash, sửa inbound links và readback.
4. 07_ENVIRONMENT và các khu kỹ thuật phải được phân loại và chuyển về đúng khu 05_BUILD hoặc phase owner; không tự suy đoán đích cho đến khi lập mapping file-level.
5. 08_DASHBOARD và 09_DASHBOARD_PREVIEW phải được đối chiếu với DASHBOARD canonical theo Work 70; không duy trì hai dashboard root ngang cấp.
6. Giữ nguyên mọi file nguồn/bằng chứng; không xóa thư mục lịch sử khi chưa có bản sao xác minh và rollback.

**Giới hạn thực thi được xác nhận:** Sandbox 8030 hiện chỉ cung cấp list/read/write/append/delete-file; không có thao tác directory move/rename/copy. Vì vậy phần quy hoạch và kiểm soát văn bản được ghi nhận, nhưng di chuyển vật lý file/thư mục chưa thể thực hiện an toàn bằng các action hiện có. Không tuyên bố filesystem normalized. Cần thực hiện batch migration bằng cơ chế file-level có kiểm chứng, sau đó chạy duplicate-number, link-integrity, DOC register parity và readback.

**Trạng thái:** GOVERNING RULE ALIGNED = RECORDED; WORK 102 FILESYSTEM RESTRUCTURE = BLOCKED (NO SAFE MOVE/COPY API); SOURCE FILES PRESERVED; ACCEPTANCE/RELEASE = NOT APPROVED.


## 2026-11-08 — Re-baseline to Work 70 Standard v1.3 (binding)

Work 70 source documents checked in Sandbox: DOC-001 v1.5, DOC-003 v1.2 and DOC-056 section 8. This addendum supersedes any earlier Work 102 wording that calls the former root `06_EVIDENCE/` a canonical evidence area or describes the root tree as already normalized.

**Canonical Work-root set:** `00_ROOT`, `01_DISCOVER`, `02_DEFINE`, `03_ARCHITECT`, `04_PLAN`, `05_BUILD`, `06_VERIFY`, `EVIDENCE`, `07_ACCEPT`, `08_RELEASE`, `09_OPERATE`, `DASHBOARD`. Exactly one numbered root phase uses `06`: `06_VERIFY`. `EVIDENCE/` is deliberately unnumbered and is the sole cross-phase evidence home. `05_BUILD/06_EVIDENCE/` is nested temporary build staging only.

**Mục 6 — ownership:** `06_VERIFY/` owns verification plans, procedures, test definitions and verification conclusions. `EVIDENCE/` owns the cross-phase evidence register and preserved evidence artifacts. The two areas have distinct purposes; no root-level `06_EVIDENCE/` may be treated as a second canonical evidence store.

**Historical evidence consolidation:** 61 leaf files from former root `06_EVIDENCE/` were copied with their relative paths into `EVIDENCE/LEGACY_EVIDENCE_ARCHIVE/`. Each destination was read back and compared with its source content: 61/61 exact matches. Originals remain in the old path as rollback copies; no original was deleted. DOC-014 was updated to reference the archived copies and remains the sole evidence register.

**Physical retirement is not yet complete:** old root `06_EVIDENCE/` and other legacy root folders remain present pending inbound-link sweep, file/hash reconciliation and a safe retirement operation. Sandbox currently exposes file operations but no directory move/rename. Therefore lifecycle tree normalization remains PARTIAL / NOT PASS. Do not claim the root directory numbering check passes while these legacy folders remain.

**Legacy root mapping (content review required before any further move):** `01_ORIGINAL` → `05_BUILD/01_ORIGINAL`; `02_EXTENSION` → `05_BUILD/02_EXTENSION`; `03_ARCHITECTURE` → `05_BUILD/03_ARCHITECTURE` or approved architecture record in `03_ARCHITECT`; `04_CODE` → `05_BUILD/04_CODE`; `05_TEST` → `05_BUILD/05_TEST` and relevant procedures in `06_VERIFY`; `07_ENVIRONMENT` → `05_BUILD/05_TEST/environment`; `07_RELEASE` → `07_ACCEPT`, `08_RELEASE` or `05_BUILD/07_RELEASE` according to artifact class; `08_DASHBOARD` and `09_DASHBOARD_PREVIEW` → canonical `DASHBOARD/` with preview explicitly `PREVIEW_ONLY`; root `10_AI_DEBUG_HANDOFF` → `05_BUILD/10_AI_DEBUG_HANDOFF`. Preserve originals until each artifact has a verified mapping and rollback.

**No technical status change:** source authority, PC/runtime acceptance, technical gates A–E, independent QE, acceptance and release remain NOT VERIFIED / NOT ACCEPTED / NOT RELEASED. No source/runtime tests were run as part of this document and evidence consolidation pass.


## 2026-11-12 — Consolidation records (Work 51 + Work 52 → Work 102)
| Document ID | Canonical path | Purpose | Status |
|---|---|---|---|
| DOC-012 | `03_ARCHITECT/DOC-012_WORK51_WORK52_WORK102_CONSOLIDATED_ARCHITECTURE.md` | Consolidated architecture, source attribution, ownership boundaries, contract mapping rules and acceptance gates | RECORDED / READ-BACK OK |
| DOC-013 | `04_PLAN/DOC-013_WORK102_CONSOLIDATION_IMPLEMENTATION_PLAN.md` | Controlled implementation work packages WP0–WP7 | RECORDED / READ-BACK OK |

Decision W102-DEC-008 is appended to DOC-006; execution record W102-LOG-20261112-02 is appended to DOC-035. Both were read back and marker-verified. No source code or test files were changed.

| DOC-064 | P1 | 19 | 05_BUILD/00_ROOT/DOC-064_WP0_PROVENANCE-REGISTER_WORK51_WORK52_WORK102.md | WP0 inventory, GitHub branch refs and candidate provenance for W51/W52/W102 | ACTIVE — WP0 PARTIAL; read-back verified |

| DOC-065 | P1 | 20 | 05_BUILD/03_ARCHITECTURE/DOC-065_WP1_CONTRACT-COMPATIBILITY-MAPPING_DRAFT.md | Draft field mapping W51 WorkContract / W52 A2A task-event / W102 Agent Loop to Core-owned contract | DRAFT — Core mapping NOT VERIFIED; not approved |
