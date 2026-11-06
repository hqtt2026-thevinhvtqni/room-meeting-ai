# DOC-001 — WORK MANIFEST / TUYÊN NGÔN WORK 76

- Document ID: DOC-001 | Priority: P0 | Read order: 1
- Work ID: 76
- Work Name: AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK
- Product: ROOM-HOP AI Trigger Engine
- Version: 0.1.0-draft | Updated: 2026-11-06
- Status: ACTIVE / DISCOVER BASELINE — G0/G1 NOT YET VERIFIED
- Product Owner / Final Authority: Vinh
- Lifecycle Orchestrator: Xu (runtime identity: xu)
- Reference standard: Work 70 — ROOM-HOP Product Lifecycle & Work Dashboard
- Sandbox: Work 76 via MCP 8030
- GitHub: hqtt2026-thevinhvtqni/room-meeting-ai / main / work/76/AI-TRIGGER-ENGINE-AND-AUTOMATION-FRAMEWORK/

## Mission
Xây dựng nền tảng dùng chung để đăng ký, tiếp nhận, đánh giá điều kiện, kích hoạt và giao nhiệm vụ cho AI Agent trong ROOM-HOP. Trigger không phải chỉ là một dòng lệnh; đây là một đối tượng có cấu hình, điều kiện, quyền hạn, lịch sử, kiểm soát lặp và bằng chứng.

## Scope
1. Time triggers: lịch một lần, định kỳ, timezone-aware.
2. Event triggers: webhook, GitHub events, system/device events, Work lifecycle events.
3. Condition triggers: biểu thức có kiểu dữ liệu, ngưỡng, AND/OR, cửa sổ thời gian.
4. Manual/command triggers: lệnh có xác thực và phạm vi.
5. Trigger registry, event intake, condition evaluator, scheduler, dispatcher, execution log, dashboard.
6. Dry-run, simulation, replay có kiểm soát, pause/disable, cooldown, deduplication, retry policy và dead-letter handling.
7. Multi-Work, multi-Agent; phân quyền theo principal, Work, action và resource.

## Out of scope for initial release
- Không tự cấp quyền cho AI khi Trigger kích hoạt.
- Không tự động thực hiện hành động nguy hiểm (xóa dữ liệu, thay đổi mạng, cấp quyền, release, thanh toán) nếu chưa có approval policy riêng.
- Không coi webhook/event payload là instruction đáng tin cậy.
- Không tự ý gửi lệnh vào private ChatGPT conversations hoặc khẳng định đã dispatch tới phiên AI khi chưa có transport/ACK evidence.
- Không thay thế Core làm nguồn chân lý về identity, authorization, lifecycle và audit.

## Canonical Work layout
00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 06_EVIDENCE, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD.
05_BUILD is an engineering mapping/execution area, not an alternate canonical source root.

## Lifecycle baseline
Current phase: 01_DISCOVER.
G0/G1: NOT VERIFIED. Later phases are preparation only and do not imply predecessor gates passed.
Release status: NOT RELEASED.
Dashboard: read-only projection; status source is local snapshot until Core integration is verified.

## Authority and invariants
1. Vinh is final authority.
2. Xu coordinates end-to-end within approved scope.
3. Work 70 is the lifecycle, gate, documentation, evidence and dashboard reference.
4. Trigger definition and execution permission are separate.
5. Every trigger execution has a correlation ID and durable audit trail.
6. No evidence, no PASS. Unknown is not PASS.
7. Dashboard is read-only and cannot mutate Trigger or Work state.
8. Fail closed for protected actions when identity, policy, evidence or audit dependencies are unavailable.

## Initial delivery objectives
- DOC-003 architecture and trigger contract.
- DOC-004 implementation and rollout plan.
- DOC-005 test/verification plan.
- Dashboard baseline and Work Package register.
- Build implementation only after discovery, requirements and architecture gates are reviewed.

## Status vocabulary
DRAFT / PLANNED / READY / ACTIVE / IN_PROGRESS / IN_REVIEW / PASS / FAIL / BLOCKED / DONE / NOT_STARTED / NOT_READY / NOT_VERIFIED.
