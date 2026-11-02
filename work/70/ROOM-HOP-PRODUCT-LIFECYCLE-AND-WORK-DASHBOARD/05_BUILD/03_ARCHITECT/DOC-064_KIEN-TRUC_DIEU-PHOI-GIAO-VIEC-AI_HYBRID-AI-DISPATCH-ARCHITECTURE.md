# DOC-064 — KIẾN TRÚC ĐIỀU PHỐI GIAO VIỆC AI KẾT HỢP
- **STT / Document ID:** DOC-064
- **Priority:** P0
- **Read order:** 64
- **Depends on:** DOC-005; DOC-033; DOC-042; DOC-043; DOC-044; DOC-057; DOC-061; DOC-063
- **Status:** DRAFT — ARCHITECTURE DECISION RECORDED / IMPLEMENTATION NOT AUTHORIZED
- **Version / Updated:** 1.0 / 2026-11-02
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Quyết định
Chọn mô hình **Hybrid AI Dispatch**: ROOM-HOP là control plane quản lý Work/WP, assignment, quyền, trạng thái, tiến độ, audit và evidence; các nền tảng AI giữ nguyên conversation/session và môi trường làm việc hiện hữu. Dispatch đi qua adapter theo khả năng đã xác minh. Ưu tiên tái sử dụng quyền hiện có, không yêu cầu API key hoặc phát sinh API cost mặc định.

Đây là quyết định kiến trúc mục tiêu. Nó không chứng minh bất kỳ adapter/provider nào đã kết nối hoặc có thể gửi tin nhắn vào phiên AI.

## 2. Nguyên tắc bất biến
1. **Conversation continuity:** không buộc AI rời phiên hiện tại nếu nền tảng cho phép tiếp tục phiên đó.
2. **Evidence before status:** trạng thái dispatch, delivery, ACK, execution và completion là các sự kiện khác nhau.
3. **No fake automation:** clipboard/handoff packet không được gọi là API dispatch; ghi Sandbox không đồng nghĩa AI đã nhận.
4. **Least privilege:** quyền cấp theo assignment, Work, repository, branch, path, action và thời hạn; không chia sẻ credential giữa AI.
5. **No API by default:** ưu tiên native connector/quyền sẵn có; API mới phải có business case, ước tính chi phí, bảo mật và phê duyệt của Vinh.
6. **Human authority:** Vinh giữ quyền accept/release và quyết định policy/security/destructive changes.
7. **Provider independence:** domain model không phụ thuộc ChatGPT/Gemini/Qwen cụ thể.
8. **Fail closed:** adapter không rõ identity, target conversation, permission hoặc delivery result thì không tự chuyển sang DELIVERED/ACKNOWLEDGED.
9. **Single source of truth:** Core/Work Registry được chỉ định làm authoritative store sau khi xác minh; Sandbox artifacts là hồ sơ/evidence, không tự trở thành database điều hành.
10. **Independent review:** tác giả không tự cấp kết quả QE độc lập.

## 3. Logical architecture
- **Work Registry / Core:** authoritative Work, WP, assignment references, ownership, policy and version (chỉ khi Core contract/API được xác minh).
- **Dispatch Orchestrator:** kiểm tra READY, dependency, permission, idempotency; tạo dispatch attempt; chọn adapter.
- **AI Registry & Capability Registry:** danh tính khai báo tách khỏi capability đã thử; ghi provider, channel, session binding, supported actions, limits, evidence, verification time, cost class.
- **Adapter Gateway:** interface thống nhất cho Native Connector, Session Handoff, ROOM Meeting Relay và optional API Adapter.
- **Conversation Handoff:** tạo gói lệnh có thể copy/paste vào đúng phiên AI; trả receipt thủ công hoặc qua callback. Không tự động hóa UI nếu chưa có capability được nền tảng hỗ trợ.
- **ACK/Progress Ingest:** nhận ACK/progress/result từ callback, connector, hoặc receipt do người/AI gửi lại.
- **Evidence Registry:** lưu output refs, commit/PR, test logs, hashes, provenance và review evidence theo Core-approved storage contract.
- **Dashboard:** read-only projection; hiển thị chính xác mức độ xác minh.
- **Audit/Event Log:** append-only event history; event delivery có thể at-least-once và consumer phải deduplicate.

## 4. Adapter modes
| Mode | Cách hoạt động | Có thể tự động gửi? | Điều kiện |
|---|---|---|---|
| NATIVE_CONNECTOR | Connector chính thức gửi/nhận qua quyền đã cấp | Có, nếu connector hỗ trợ chính xác hành động | capability test + auth scope + session/target proof |
| SESSION_HANDOFF | ROOM tạo instruction packet; người dùng dán vào conversation hiện hữu; AI trả receipt/result | Không; user-mediated | handoff packet ID và receipt gắn đúng assignment |
| ROOM_MEETING_RELAY | Agent tham gia meeting và nhận/gửi message qua Meeting API | Chỉ trong meeting đã xác minh | identity join + meeting state + message evidence; không đồng nghĩa truy cập conversation riêng |
| API_ADAPTER | API provider chính thức, có thể tạo session mới hoặc tiếp tục session nếu provider hỗ trợ | Có, theo API semantics | Vinh duyệt chi phí; secret manager; privacy/security review |
| UNSUPPORTED | Không có kênh thực thi đã xác minh | Không | BLOCKED; không giả lập |

Adapter không được tự đổi mode sau lỗi theo cách làm mất session continuity hoặc phát sinh phí. Fallback phải được ghi thành mode mới và cần policy cho phép.

## 5. Component responsibilities
- Xu/Orchestrator: phân rã mục tiêu, chọn AI dựa capability, chuẩn bị assignment, theo dõi dependency, tổng hợp; không tự xác nhận ACK thay AI.
- AI Registry: mô tả AI và capability; roster không chứng minh online.
- Dispatch Adapter: chỉ thực hiện giao nhận; không quyết định acceptance.
- AI assignee: ACK, thực hiện trong scope, gửi progress, deliverables và blockers.
- QE reviewer: kiểm tra độc lập; chỉ phát hành review result.
- Core/Registry: kiểm soát authoritative state/authorization và concurrency.
- Vinh: duyệt policy, chi phí API mới, acceptance cuối và release.

## 6. Trust boundaries and security
1. User conversation text, handoff packet, adapter callback và AI output đều là untrusted input cho đến khi xác thực provenance.
2. Không coi AI ID trong body là authenticated principal. Principal phải được ràng buộc bởi connector identity hoặc receipt challenge có kiểm chứng.
3. Không dùng caller-supplied `authorized=true` làm quyền.
4. Không đưa API token, cookie, password hoặc secret vào prompt, Markdown handoff, Sandbox docs hay logs.
5. Callback phải xác minh signature/connector identity, timestamp/nonce, assignment binding và replay window.
6. Mỗi dispatch attempt có idempotency key; duplicate delivery không tạo assignment hoặc transition thứ hai.
7. Permission grant có scope, actor, reason, issued_at, expires_at, revocation và audit.
8. Không cho adapter truy cập dữ liệu ngoài assignment.
9. Revoke/expiry phải ngăn command mới và được re-check trước hành động nhạy cảm.
10. Log phải redacted; lưu tối thiểu dữ liệu conversation, không mirror toàn bộ chat nếu không cần.

## 7. Canonical lifecycle
Assignment business status (tách khỏi Work/WP lifecycle):
- DRAFT → READY → DISPATCHED → ACKNOWLEDGED → IN_PROGRESS → IN_REVIEW → DONE.
- BLOCKED có thể xảy ra ở các trạng thái thực thi; ghi blocker owner, reason, next action.
- REJECTED: AI từ chối hoặc không đủ capability; phải ghi reason.
- EXPIRED: quá hạn ACK/execution theo policy.
- CANCELLED: actor có thẩm quyền hủy; assignment không được tiếp tục.
- DELIVERY_FAILED: adapter báo lỗi giao nhận; không được hiểu là AI từ chối.
Các trạng thái transport riêng: CREATED, SEND_ATTEMPTED, DELIVERED, DELIVERY_UNKNOWN, DELIVERY_FAILED. DELIVERED không phải ACKNOWLEDGED. IN_REVIEW không phải DONE. DONE không tự động làm Work/Gate ACCEPTED/PASS.

## 8. End-to-end flow
1. Xu tạo assignment DRAFT từ DOC-044/Work Package; xác định owner, reviewer, scope, baseline, deliverables, acceptance, dependencies và due policy.
2. Validator kiểm tra đầy đủ contract, role/capability, permission, source baseline, dependency và reviewer independence.
3. Authority chuyển assignment READY; READY là điều kiện cho phép dispatch, không phải quyền code vượt ngoài scope.
4. Orchestrator chọn adapter theo capability evidence còn hiệu lực; ghi adapter mode, target, session reference (không lưu secret) và dispatch attempt.
5. Adapter gửi payload hoặc tạo handoff packet; ghi transport result chính xác.
6. AI trả ACK với assignment_id, dispatch_id, AI ID/identity proof, accepted/rejected, scope understood, ETA/next update. Với session handoff, ACK phải được nhập lại từ phiên AI hoặc receipt có kiểm chứng.
7. Ingest xác minh identity binding, assignment version, expiry, nonce/idempotency; sau đó mới ghi ACKNOWLEDGED.
8. AI gửi progress events, blocker và deliverables. Mọi update gắn assignment_id, sequence/version và provenance.
9. Khi nộp, trạng thái IN_REVIEW; reviewer độc lập kiểm tra acceptance criteria và raw evidence.
10. Nếu đạt, reviewer ghi REVIEW_APPROVED; authority có quyền mới chuyển DONE. Xu không tự nâng Work Gate hoặc Release.
11. Retry dùng cùng idempotency key/payload; payload khác phải key mới và audit. Không dispatch lại mù khi DELIVERY_UNKNOWN.
12. Kết quả được lưu trong authoritative registry sau khi storage contract được Core owner xác nhận; Sandbox giữ handoff/evidence artifacts theo quy định.

## 9. Dashboard requirements
Hiển thị AI declared vs verified; adapter mode; capability evidence age; target session label; transport status; ACK status/time; progress; due/timeout; blocker; result/review; cost class/actual measured cost; evidence refs; sync/freshness. Không hiển thị "Online/Connected" chỉ vì registry có record.

## 10. Rollout constraints
- Phase 0: read-only discovery/capability tests; không gửi message hoặc cấp quyền.
- Phase 1: SESSION_HANDOFF thủ công, một assignment không nhạy cảm, có receipt.
- Phase 2: connector chỉ khi native action và session continuity được chứng minh.
- Phase 3: automated ACK/progress/result ingestion và audit.
- Phase 4: optional API adapter chỉ sau cost approval.
Không triển khai nhiều adapter cùng lúc trước khi contract và acceptance test ổn định.

## 11. Open decisions / blockers
- Core owner và authoritative Work/Assignment/Evidence APIs chưa được xác minh trong scope hiện tại.
- Không có dispatch tool trực tiếp tới các conversation riêng trong MCP 8030 toolset đã kiểm tra.
- Native connector support cho từng AI/session chưa được kiểm chứng.
- Cơ chế signed receipt/challenge cho SESSION_HANDOFF cần chốt implementation.
- Retention/privacy policy và storage provider phải theo Core owner.
- DOC-060 gate namespace vẫn là proposal; DOC-064 không tạo gate mới.

## 12. Acceptance criteria
- Adapter mode được phân biệt rõ; không fake DELIVERED/ACK.
- Conversation session continuity được giữ trong SESSION_HANDOFF.
- READY validation fail-closed.
- Assignment lifecycle và transport lifecycle tách riêng.
- Retry/idempotency/revocation/expiry hoạt động đúng.
- Evidence provenance và reviewer independence được enforce.
- Dashboard chỉ đọc authoritative projection và phân biệt UNKNOWN/STALE.
- API cost approval được kiểm soát.
- Independent QE xác minh các positive/negative cases.
- Không thay đổi Core/Engine/Dashboard hoặc mở BUILD chỉ dựa trên tài liệu này.

**Disposition:** Architecture decision for target design; implementation remains NOT AUTHORIZED pending source contract reconciliation, Core owner, and Work Entry authorization.
