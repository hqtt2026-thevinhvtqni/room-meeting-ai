# SỔ ĐĂNG KÝ TÀI LIỆU / DOCUMENT REGISTER — WORK 0000

- Document ID: DOC-002 | Priority: P0 | Read order: 2
- Depends on: DOC-001 | Status: ACTIVE — STRUCTURED REGISTER
- Version: 1.1 | Updated: 2026-11-03 19:25 +07
- Owner: Work 0000 / Go (Grok) — Sandbox completion batch
- Governing standard: Work 70 DOC-038/039/040/056 (naming, issuance, migration)

## 1. Quy tắc
- Một DOC ID = một canonical path duy nhất.
- Status vocabulary: DRAFT | ACTIVE | SUPERSEDED | ARCHIVED.
- Không xóa dòng cũ; đính chính bằng phiên bản mới hoặc ghi chú.
- Work 70 DOC-055 vẫn là register chuẩn của Work 70; đây là register cục bộ của Work 0000.

## 2. Core governance documents

| DOC ID | Priority | Canonical path | Title | Status |
|--------|----------|----------------|-------|--------|
| DOC-001 | P0 | 00_ROOT/DOC-001_BAN-TUYEN-NGON_WORK-MANIFEST.md | Work Manifest | ACTIVE |
| DOC-002 | P0 | 00_ROOT/DOC-002_SO-DANG-KY-TAI-LIEU_DOCUMENT-REGISTER.md | Document Register | ACTIVE |
| DOC-003 | P0 | 00_ROOT/DOC-003_NHAT-KY-THI-CONG_EXECUTION-LOG.md | Execution Log | ACTIVE |
| DOC-004 | P0 | 00_ROOT/DOC-004_SO-QUYET-DINH_DECISION-LOG.md | Decision Log | ACTIVE |
| DOC-005 | P1 | 00_ROOT/DOC-005_BIEN-BAN_MINUTES-AND-DECISIONS.md | Minutes and Decisions | ACTIVE |

## 3. Discover / Define / Architect / Plan

| DOC ID | Priority | Canonical path | Title | Status |
|--------|----------|----------------|-------|--------|
| DOC-006 | P1 | 01_DISCOVER/DOC-006_BAO-CAO-KHAM-PHA_COMPANY-DISCOVER-BRIEF.md | Company Discover Brief | DRAFT |
| DOC-007 | P1 | 04_PLAN/DOC-007_KE-HOACH_TRIEN-KHAI_COMPANY-GOVERNANCE-ROADMAP.md | Governance Roadmap | DRAFT |
| DOC-012 | P1 | 02_DEFINE/DOC-012_YEU-CAU-QUAN-TRI_COMPANY-GOVERNANCE-REQUIREMENTS.md | Company Governance Requirements | DRAFT |
| DOC-013 | P1 | 03_ARCHITECT/DOC-013_KIEN-TRUC_QUAN-TRI-CONG-TY_COMPANY-GOVERNANCE-ARCHITECTURE.md | Company Governance Architecture | DRAFT |
| DOC-014 | P0 | 01_DISCOVER/DOC-014_KIEM-KE-REPOSITORY-GOC_ORIGINAL-REPOSITORY-INVENTORY.md | Original Repository Inventory | ACTIVE — DISCOVERY SNAPSHOT |
| DOC-015 | P0 | 01_DISCOVER/DOC-015_DOI-CHIEU-QUY-CHUAN-GOC_ORIGINAL-GOVERNANCE-RECONCILIATION.md | Original Governance Reconciliation | ACTIVE — INITIAL |
| DOC-016 | P0 | 01_DISCOVER/DOC-016_SOURCE-FILE-SHA-MANIFEST.md | Source File SHA Manifest | ACTIVE — SNAPSHOT |
| DOC-017 | P0 | 01_DISCOVER/DOC-017_KIEM-TRA-HIEN-TRANG-KY-THUAT_TECHNICAL-BASELINE-REVIEW.md | Technical Baseline Review | ACTIVE — READ-ONLY |
| DOC-018 | P0 | 01_DISCOVER/DOC-018_DANH-MUC-WORK-TOAN-CONG-TY_COMPANY-WORK-PORTFOLIO-REGISTER.md | Company Work Portfolio Register | ACTIVE — INITIAL SNAPSHOT |
| DOC-019 | P1 | 01_DISCOVER/DOC-019_BAO-CAO-DOI-CHIEU-APDS-WORK70-HYBRID-DISPATCH-PORTFOLIO-RECONCILIATION.md | APDS / Work70 / Hybrid Dispatch Reconciliation | ACTIVE — INITIAL |
| DOC-020 | P0 | 01_DISCOVER/DOC-020_BAN-DO-PHU-THUOC_WORK_DEPENDENCY-AND-BOTTLENECK-MAP.md | Dependency & Bottleneck Map | ACTIVE — DISCOVERY BASELINE |
| DOC-021 | P0 | 01_DISCOVER/DOC-021_BAO-CAO-DOI-CHIEU_WORK-ENTRY-GATE-RECONCILIATION.md | Work Entry Gate Reconciliation | ACTIVE |

## 4. Evidence / Build / Dashboard

| DOC ID | Priority | Canonical path | Title | Status |
|--------|----------|----------------|-------|--------|
| DOC-008 | P0 | 06_EVIDENCE/DOC-008_SO-DANG-KY-BANG-CHUNG_EVIDENCE-REGISTER.md | Evidence Register | ACTIVE — STRUCTURED v1.1 |
| DOC-009 | P1 | 05_BUILD/00_ROOT/BUILD_MAPPING_REGISTER.md | Build Mapping Register | ACTIVE |
| DOC-010 | P1 | 05_BUILD/00_ROOT/AI_TEAM_AND_TOKEN_USAGE.md | AI Identity Register & Token Usage | ACTIVE — DECLARED ROSTER / USAGE NOT VERIFIED |
| DOC-011 | P2 | DASHBOARD/README.md | Dashboard Guide | ACTIVE |

## 5. External original asset

| Asset ID | Asset | Canonical source | Relationship | Status |
|----------|-------|------------------|--------------|--------|
| EXT-001 | HQTT AI Platform | `hqtt2026-thevinhvtqni/hqtt-ai-platform` (private, default branch main) | Nền tảng gốc; Work 0000 chỉ index/governance, không thay thế repo | DISCOVERED / PRESERVE |
| — | Compatibility pointer | 01_DISCOVER/EXT-001_REPOSITORY-INVENTORY.md | Trỏ về DOC-014 | ACTIVE — pointer only |

**Lưu ý quan trọng:** Repo là **private**. Public URL trả 404 là hành vi đúng, không phải repo chưa tạo. Baseline commit đã quan sát: `8a2d7aa33ed537e2bc117d3421a454da0e4cd8ab`.

## 6. Quyết định liên quan đến register (tham chiếu nhanh)

| Decision ID | Summary | Status |
|-------------|---------|--------|
| D0000-001 | Work 70 = mandatory lifecycle standard | RECORDED |
| D0000-002 | Work 0000 = company governance plane; Work 70 = operational plane | CONFIRMED |
| D0000-003 | Phân công đề xuất Go/Sandbox – Vibe/GitHub – Xu/Integration | RECORDED (superseded by ACK) |
| D0000-004 | Chờ Go ACK trước khi mở issue | RECORDED |
| D0000-005 | Founder chỉ định Grok = Go; Go ACK | CONFIRMED — ACKNOWLEDGED |

## 7. Trạng thái đợt thi công hiện tại (Go)

| Hạng mục | Trạng thái |
|----------|------------|
| Evidence Register (DOC-008) | **DONE** — structured v1.1 |
| Document Register (DOC-002) | **DONE** — structured v1.1 (this update) |
| Dashboard | CHỜ — sau khi hai register ổn định |
| Recovery proof | CHỜ — phối hợp Vibe + Xu |

| DOC-022 | P0 | 06_EVIDENCE/DOC-022_RECOVERY-PROOF_SANDBOX-BASELINE.md | Recovery Proof — Sandbox Baseline (Phase A) | ACTIVE — PHASE A COMPLETE / PHASE B BLOCKED |

| DOC-023 | P0 | 06_EVIDENCE/DOC-023_READINESS-PACKAGE_GO-TO-XU.md | Readiness Package Go→Xu (SHA inventory + B0 refs) | ACTIVE — ISSUED |

| DOC-024 | P0 | 06_EVIDENCE/DOC-024_READINESS-PACKAGE-CORRIGENDUM.md | Readiness Package Corrigendum (size drift + hash policy) | ACTIVE — ISSUED |


| DOC-025 | P0 | 01_DISCOVER/DOC-025_BAO-CAO-KHAM-SAT_GITHUB-INBOUND-MONITOR-DISCOVERY.md | GitHub Inbound Monitor Discovery Report | ACTIVE — DISCOVERY COMPLETE / DESIGN PROPOSAL ONLY |
