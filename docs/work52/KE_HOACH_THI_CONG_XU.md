# KE_HOACH_THI_CONG_XU.md — Work 52

## Mục tiêu
Thiết kế và kiểm chứng nền tảng A2A/điều phối AI trung lập nhà cung cấp cho ROOM-HOP, tái sử dụng kiến trúc hiện hữu và có bằng chứng E2E.

| Gate | Công việc | Phụ trách | Bằng chứng cần có | Trạng thái |
|---|---|---|---|---|
| G0 | Đọc governance và kiểm kê repo, Work 10/11/12/14/16/21/28/30/31/51; xác định trùng lặp | Xu điều phối; coder sau discovery | File/path/commit inventory, dependency map | IN PROGRESS |
| G1 | Đặc tả A2A contract, lifecycle, events, errors, cancellation, retries, timeout, correlation IDs | Xu thiết kế; reviewer độc lập | Versioned schema, decision record | NOT STARTED |
| G2 | Lập bảng khả năng runtime/adapter: Codex, Qwen và provider khác | Adapter owner sau G0 | Probe logs; supported/unsupported matrix | NOT STARTED |
| G3 | Thiết kế security: identity, authentication/authorization, least privilege, isolation, secret handling, audit | Security reviewer | Threat model, permission matrix, negative tests | NOT STARTED |
| G4 | Xây prototype trong Sandbox sau khi G0-G3 được duyệt | Coder được phân công | Source, repeatable tests, logs | NOT STARTED |
| G5 | Kiểm thử E2E đa runtime, lỗi mạng, timeout, cancellation, retry, denied tool, tester handoff | Tester độc lập | Test report và raw evidence | NOT STARTED |
| G6 | Handoff: tài liệu, giới hạn, vận hành, rollback, các mục BLOCKED | Xu điều phối + team | Handoff checklist, nhật ký | NOT STARTED |

## Contract tối thiểu
- task_id, correlation_id, work_id, requested_by, assigned_agent, role, capability_requirements
- input, output_schema, constraints, workspace_scope, tool_permissions
- Lifecycle: QUEUED, ACCEPTED, RUNNING, WAITING_APPROVAL, SUCCEEDED, FAILED, CANCELLED, TIMED_OUT
- Events có timestamp, sequence/cursor, producer identity và provenance
- Error taxonomy, retry policy, idempotency, cancellation semantics
- Evidence references, test outcomes, handoff result; không cho model tự gán PASS khi thiếu kiểm chứng
- Versioning/compatibility, provider capability discovery, observability

## Quy tắc
- Không viết production code trước G0 và khi chưa xác định ranh giới thành phần.
- Không hỏi lại thông tin đã có trong hồ sơ; khi bị chặn, thu thập bằng chứng và tiếp tục phần không bị chặn.
- Không giả định mọi AI hỗ trợ cùng giao thức hoặc mọi máy có thể truy cập cùng endpoint.
- Mọi thay đổi Sandbox cần read-after-write/test evidence.
- Không tự merge/push GitHub.
- Nhật ký dùng UTC+07:00.
