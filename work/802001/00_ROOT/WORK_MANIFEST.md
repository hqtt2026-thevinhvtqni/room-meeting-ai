# WORK MANIFEST — WORK 802001

- Work ID: 802001
- Work Name: AGENT WORK SUPERVISION & GUIDANCE — THEO DÕI, NHẮC NHỞ VÀ HƯỚNG DẪN AGENT
- Product: Nghiệp vụ theo dõi và hướng dẫn Agent trong quá trình thực hiện Work/assignment
- Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu / AI-01
- Governing standard: Work 70 — DOC-001, DOC-004, DOC-005, DOC-033, DOC-035, DOC-057
- Status: ACTIVE — BUSINESS STANDARDIZATION / TECHNICAL DESIGN NOT APPROVED
- Scope revision: 2026-11-17 v1.2 — governance reference correction

## Purpose
Theo dõi Agent từ lúc nhận việc đến khi hoàn tất; hướng dẫn trước khi làm; theo dõi checkpoint; phát hiện sai/lệch/chậm/blocked/thiếu evidence; nhắc nhở; hướng dẫn sửa; kiểm tra lại; escalation và ghi nhật ký.

## Canonical lifecycle structure
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD — theo Work 70.

## Canonical records
- Biên bản: 00_ROOT/BIEN_BAN.md
- Kế hoạch: 04_PLAN/IMPLEMENTATION_ROADMAP.md
- Kiến trúc nghiệp vụ: 03_ARCHITECT/AGENT_OPERATIONAL_GATE_ARCHITECTURE.md
- Nhật ký thi công: 00_ROOT/NHAT_KY_THI_CONG.md
- Document Register: 00_ROOT/DOCUMENT_REGISTER.md
- Evidence Register: EVIDENCE/EVIDENCE_REGISTER.md
- Dashboard contract: DASHBOARD/README.md

## Boundary
Work 70 remains governing lifecycle standard. W802001 defines assignment-level Agent supervision and guidance. Gate/deny enforcement is one possible control, not the entire product. Legacy E2E auto-wake evidence remains preserved and is not proof of supervision functionality.

## Truth status
Business scope documented. Runtime monitoring, automated reminders, Agent correction loop and enforcement are NOT VERIFIED / NOT IMPLEMENTED unless separately evidenced. Legacy folders remain pending inventory/migration; no deletion authorized.
