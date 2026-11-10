# DOC-002 — SỔ ĐĂNG KÝ TÀI LIỆU WORK 112
- Work ID: 112
- Work: ROOM-HOP-INTEGRATION-CONTRACTS-AND-EVIDENCE-ORCHESTRATION
- Version: 1.0
- Status: ACTIVE — DOCUMENT CONTROL BASELINE
- Authority: Vinh
- Owner / Coordinator: Xu / AI-01
- Updated: 2026-11-10 (+07:00)
- Canonical path: 00_ROOT/DOC-002_SO-DANG-KY-TAI-LIEU_WORK-112-DOCUMENT-REGISTER.md

## 1. Quy tắc nguồn chuẩn
- Đây là sổ đăng ký tài liệu duy nhất của Work 112.
- Tài liệu có DOC-ID chỉ có một canonical path; không tạo bản sao làm nguồn chuẩn.
- WORK_MANIFEST.md, INTEGRATION_CHARTER.md và EXECUTION_JOURNAL.md là hồ sơ điều hành gốc, được quản lý trực tiếp tại 00_ROOT và được đăng ký tại đây.
- Mọi thay đổi trạng thái, kiểm tra, thử nghiệm, quyết định và blocker phải được ghi trong EXECUTION_JOURNAL.md.
- Sandbox write acknowledgment không phải bằng chứng GitHub sync; sync chỉ được ghi nhận sau khi fetch đúng branch/path và so sánh nội dung.
- W112 không tạo task register, event bus, evidence store hoặc runtime cạnh tranh với W70 và các Work sở hữu module.

## 2. Document register
| ID | Tài liệu | Canonical path | Status | Ghi chú |
|---|---|---|---|---|
| ROOT-MANIFEST | Work Manifest | 00_ROOT/WORK_MANIFEST.md | ACTIVE | Nguồn định danh, phạm vi, cấu trúc và ranh giới Work |
| ROOT-CHARTER | Integration Charter | 00_ROOT/INTEGRATION_CHARTER.md | ACTIVE | Mục tiêu, WP ban đầu, ownership và acceptance |
| ROOT-JOURNAL | Execution Journal | 00_ROOT/EXECUTION_JOURNAL.md | ACTIVE | Nhật ký append-only nghiệp vụ |
| DOC-001 | Hợp đồng tích hợp liên Work / Cross-Work Integration Contract Baseline | 03_ARCHITECT/DOC-001_HOP-DONG-TICH-HOP-LIEN-WORK_CROSS-WORK-INTEGRATION-CONTRACT-BASELINE.md | DRAFT — NOT APPROVED FOR RUNTIME ENFORCEMENT | Baseline thiết kế; chờ review độc lập và Vinh phê duyệt |
| DOC-002 | Sổ đăng ký tài liệu Work 112 / Work 112 Document Register | 00_ROOT/DOC-002_SO-DANG-KY-TAI-LIEU_WORK-112-DOCUMENT-REGISTER.md | ACTIVE | Sổ đăng ký duy nhất |

## 3. Work 70 compliance
- Lifecycle folders and 05_BUILD child folders follow W70 DOC-001.
- Document naming and controlled change follow W70 DOC-033, DOC-038, DOC-039 and DOC-056.
- Work 112 applies the W70 three-tier task model when its own task register is defined; W70 remains the authority for system-wide lifecycle and governance.
- Dashboard is a read-only projection. It cannot become an alternate task or evidence source.
- No task, phase, assignment or gate is DONE/PASS without attributable ACK, deliverable and evidence.

## 4. Open document-control items
- Physical retirement of legacy root scaffolds: OPEN; preserve until file/link inventory and controlled migration are verified.
- Full Sandbox ↔ GitHub parity for every listed document: NOT VERIFIED as of this revision.
- DOC-001 independent architecture review and approval: PENDING.
- Work 112 product/phase/agent task register: NOT CREATED; must be defined under W70 task model before execution assignments are treated as active.


## Addendum 2026-11-10 — W112 three-tier task model
| ID | Tài liệu | Canonical path | Status | Purpose |
|---|---|---|---|---|
| DOC-003 | Sổ Product Task và Phase Task W112 / W112 Product and Phase Task Register | 04_PLAN/DOC-003_W112_PRODUCT_PHASE_TASK_REGISTER.json | DRAFT_NOT_APPROVED | Nguồn chuẩn duy nhất cho 1 Product Task và 9 Phase Task; trạng thái hiện NOT_ASSESSED |
| SCHEMA-003 | Schema Product/Phase Task W112 | 03_ARCHITECT/DOC-003_W112_PRODUCT_PHASE_TASK_REGISTER.schema.json | CREATED / FORMAL VALIDATION NOT RUN | Kiểm tra cấu trúc DOC-003; không phải nguồn trạng thái |
| DOC-004 | Sổ Agent Task W112 / W112 Agent Task Register | 04_PLAN/DOC-004_W112_AGENT_TASK_REGISTER.json | DRAFT_NOT_APPROVED | Nguồn chuẩn duy nhất cho 6 Agent Task gắn với 6 WP trong Charter |
| SCHEMA-004 | Schema Agent Task W112 | 03_ARCHITECT/DOC-004_W112_AGENT_TASK_REGISTER.schema.json | CREATED / FORMAL VALIDATION NOT RUN | Kiểm tra cấu trúc DOC-004; không phải nguồn trạng thái |

- DOC-003 and DOC-004 implement W70's three-tier model without copying W70 task IDs or duplicating its task state.
- All six Agent Task assignments are PROPOSED_NOT_ACKNOWLEDGED; all Product/Phase tasks are NOT_ASSESSED; product progress remains NOT_CALCULATED.
- A proposed primary/checking agent is a planning reference only. No dispatch, ACK, permission, active execution or Gate PASS is implied.


## Addendum 2026-11-10 — schema-rule conformance status
- DOC-003 against SCHEMA-003: in-session schema-rule conformance subset PASS (zero reported errors).
- DOC-004 against SCHEMA-004: in-session schema-rule conformance subset PASS (zero reported errors).
- JSON parsing and the implemented required/type/property/enum/const/array/range/pattern checks passed on exact Sandbox readback content.
- Formal external JSON Schema validation remains NOT RUN; independent architecture review and Vinh approval remain PENDING. These checks do not approve the task model or authorize dispatch/runtime execution.
