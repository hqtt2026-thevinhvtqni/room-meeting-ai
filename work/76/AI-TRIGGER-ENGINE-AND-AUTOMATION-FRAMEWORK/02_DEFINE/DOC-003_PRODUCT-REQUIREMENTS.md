# DOC-003 — PRODUCT REQUIREMENTS / YÊU CẦU SẢN PHẨM

## Functional requirements
FR-01 Registry: tạo, đọc, sửa phiên bản, pause, resume, disable Trigger; lưu owner, Work/WP scope, loại, timezone, điều kiện, action, policy reference.
FR-02 Scheduler: chạy one-shot và recurring; lưu next_run; xử lý timezone và lịch chạy bị bỏ lỡ.
FR-03 Event intake: nhận webhook/event; xác thực nguồn, schema, timestamp, signature và replay window.
FR-04 Condition engine: hỗ trợ typed operands/operators, AND/OR/NOT, threshold, time window; không dùng eval tùy ý.
FR-05 Dispatch: tạo nhiệm vụ có assignment_id, correlation_id, target identity, scope, expiry và idempotency key.
FR-06 Safety: kiểm tra principal, permission, approval, cooldown, dedupe, rate limit và kill switch.
FR-07 Observability: ghi received/evaluated/suppressed/queued/dispatched/acknowledged/succeeded/failed/expired.
FR-08 Dashboard: read-only view cho Registry, executions, blockers, evidence, freshness và source mode.
FR-09 Replay: chỉ replay trong chế độ kiểm soát; mặc định dry-run, không phát sinh side effect.
FR-10 Multi-tenant: cô lập dữ liệu theo Work và policy scope.

## Non-functional requirements
NFR-01 Security: authentication, authorization, signature validation, secret redaction, least privilege.
NFR-02 Reliability: at-least-once intake có idempotent processing; không tuyên bố exactly-once nếu chưa chứng minh.
NFR-03 Audit: append-only/tamper-evident record, correlation across intake/evaluation/dispatch.
NFR-04 Resilience: bounded retry, exponential backoff, dead-letter queue và operator recovery.
NFR-05 Performance: SLO/throughput/latency phải được đo và phê duyệt sau discovery; chưa đặt số giả.
NFR-06 Maintainability: versioned schema, migration strategy, contract tests.
NFR-07 Privacy: không lưu prompt/private conversation hoặc secret ngoài nhu cầu được duyệt.

## Acceptance baseline
- Mọi Trigger có owner, scope, version, source, condition, action, policy, status.
- Mọi execution truy được event → evaluation → authorization → dispatch → ACK/outcome.
- Không chạy action khi policy DENY, evidence thiếu hoặc audit unavailable.
- Duplicate event không tạo duplicate side effect.
- Pause/disable/kill switch có hiệu lực được kiểm thử.
- Dashboard không ghi dữ liệu và hiển thị UNKNOWN khi source không xác minh.
- Independent QE review và Vinh acceptance trước release.

## Open decisions
Event broker, database, scheduler technology, Core API contract, dispatch transport, retention, SLO and approval matrix remain TBD.
