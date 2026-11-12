# DOC-002 — DISCOVER BRIEF / BÁO CÁO KHÁM PHÁ

## Problem statement
ROOM-HOP cần một cơ chế kích hoạt AI thống nhất. Các nhu cầu hiện có gồm lịch định kỳ, sự kiện từ hệ thống/GitHub, điều kiện ngưỡng, lệnh thủ công và sự kiện vòng đời Work. Nếu mỗi Work tự tạo scheduler hoặc trigger riêng, sẽ phát sinh trùng lặp, thiếu audit, không nhất quán về quyền và khó quan sát.

## User and system outcomes
- Người quản trị khai báo Trigger một lần, theo dõi được trạng thái và lịch sử.
- AI chỉ nhận nhiệm vụ sau khi sự kiện hợp lệ, điều kiện đúng và policy cho phép.
- Có thể tạm dừng, vô hiệu hóa, mô phỏng và truy vết từng lần chạy.
- Dashboard cho thấy trigger nào đã đăng ký, điều kiện nào được đánh giá, kết quả dispatch/ACK và bằng chứng.

## Trigger taxonomy
- TIME: kích hoạt theo lịch.
- EVENT: kích hoạt bởi sự kiện đã xác thực.
- CONDITION: kích hoạt khi biểu thức đạt điều kiện.
- MANUAL: kích hoạt theo lệnh đã xác thực.
- COMPOSITE: kết hợp nhiều nguồn/điều kiện, chỉ triển khai sau khi semantics được chốt.

## Discovery questions
1. Event sources nào là authoritative và có webhook/polling contract?
2. Core identity, Work/WP authorization và audit API nào sẽ được dùng?
3. AI dispatch transport nào có thật, hỗ trợ receipt/ACK ra sao?
4. Trigger cần độ trễ, throughput, retention và availability mục tiêu nào?
5. Những action nào bắt buộc human approval?
6. Quy tắc timezone, daylight-saving, retry, dedupe và replay?
7. Trigger configuration versioning và rollback được quản lý thế nào?

## Constraints
- Không giả định private-session dispatch đã tồn tại.
- Không tự suy diễn AI ID từ display name.
- Không tin payload từ bên ngoài nếu chưa xác thực chữ ký/nguồn.
- Không để event payload chứa prompt injection điều khiển policy hoặc cấp quyền.
- Không chạy protected action nếu authorization/audit không sẵn sàng.

## Discovery status
DRAFT / evidence collection pending. Danh sách câu hỏi trên chưa được xem là đã giải quyết.


## Evidence-backed discovery findings — 2026-11-13 (bounded; not approved)

The following findings answer parts of the discovery questions but do not close the underlying architecture decisions.

| Discovery question | Current evidence-backed finding | Status / remaining work |
|---|---|---|
| 1. Authoritative event sources and webhook/polling contract? | No authoritative event-source registry, webhook signature/key-rotation contract, polling owner or replay store was located in the bounded indexed default-branch search of room-meeting-ai. | OPEN / NOT LOCATED. Xu must identify source owners and exact repository/ref/API contracts. |
| 2. Core identity, Work/WP authorization and audit API? | W70 DOC-063 is a draft design reference requiring server-trusted principal, assignment, scope, gate, expiry/revocation and commit-time revalidation. The inspected W70 source-trace record did not find Work/WP authorization or Evidence Registry routes in the inspected Core router. HQTT AI Platform API design mentions token-based authentication conceptually, but its inspected backend router only exposes health/ping. | OPEN / NOT VERIFIED. Core owner must identify actual API, route, schema, deployed enforcement and audit persistence. |
| 3. AI dispatch transport and receipt/ACK? | HQTT AI Platform Task_Dispatch and AI_Workflow describe operating-process handoff, not a machine transport. The inspected HQTT backend has no task/dispatch/ACK route. W76 has no verified target identity resolver or receiver-issued ACK schema. | WP-76-07 BLOCKED. Require real provider, authenticated target identity, receipt/ACK contract and raw end-to-end evidence. |
| 4. Latency, throughput, retention and availability targets? | No approved SLO or measured baseline was found in the inspected W76 records. | OPEN. Do not invent numerical SLO; obtain product/operations owner decision and measure before release. |
| 5. Actions requiring human approval? | DOC-003 FR-06 and DOC-004 require policy/approval checks, but an approved action-classification and approval matrix has not been evidenced. | OPEN. Xu proposes classification; Vinh approves policy. |
| 6. Timezone, DST, retry, dedupe and replay rules? | DOC-004 proposes explicit UTC event timestamps, typed time windows, idempotency and dry-run replay; DOC-006 contains corresponding test design. No authoritative scheduler, broker or persistence mechanism has been selected. | PARTIALLY SPECIFIED / NOT IMPLEMENTED. ADR must define scheduler semantics, clock basis, DST, missed-run and retry/DLQ policy. |
| 7. Trigger versioning and rollback? | DOC-004 proposes one ACTIVE version per trigger ID, atomic activation/retirement, expected-version concurrency and audit continuity. No durable registry/persistence implementation is verified. | DESIGN PROPOSAL ONLY. Requires storage/transaction ADR and regression evidence. |

### Discovery disposition
- Discovery questions are now classified as OPEN, PARTIALLY SPECIFIED or BLOCKED with explicit evidence boundaries; none is promoted to APPROVED merely because a design proposal exists.
- DOC-004 sections H/H.3 hold the detailed cross-Work dependency map and exact source paths/blob SHAs.
- DOC-006 holds the FR/NFR-to-verification traceability matrix; all new test IDs are specifications, not executed tests.
- Lifecycle remains 01_DISCOVER; G0/G1 NOT VERIFIED; Co WE-G4/G5 BLOCKED; WP-76-07 BLOCKED; runtime implementation and CI evidence NOT_AVAILABLE; NOT RELEASED.
