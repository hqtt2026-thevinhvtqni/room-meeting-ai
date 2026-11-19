# GAP REGISTER — WORK 17

- Work ID: 17 · Owner: Vinh · Điều phối: Xu / AI-01
- Ngày cập nhật: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Nguồn phát hiện: WORK_17_AUDIT_JOURNAL.md Entry 001–005; quét GitHub main kỳ 2026-11-19.

## Định mức ưu tiên
- P0: chặn trực tiếp khả năng chạy được luồng AI end-to-end; phải xử lý trước G3.
- P1: gây sai lệch bằng chứng/kết luận nếu không xử lý trước G4–G6.
- P2: chất lượng, hiệu suất, dọn dẹp; xử lý sau G6.

## Danh mục gap

| ID | Gap | Mảng năng lực | Ưu tiên | Evidence hiện tại | Tiêu chí nghiệm thu | Trạng thái |
|----|-----|---------------|---------|-------------------|---------------------|------------|
| GAP-01 | Dispatch/ACK tới AI member chưa được chứng minh; tool surface 8030 không có private-session dispatch; source adapters được kiểm tra là browser/execution/Git/CI/Meeting artifact, không phải AI provider transport | Dispatch & acknowledgment | P0 | Journal Entries 002, 016–021; WORK_17_GAP01_DISPATCH_ACK_SOURCE_RECONCILIATION.md §8–9; WORK_17_GAP01_TECHNICAL_OPTIONS_AND_HANDOFF_PROTOCOL.md (proposal only) | Một dispatch thật có trace ID khớp provider delivery receipt + ACK accountable, đạt cấp E3 | OPEN |
| GAP-02 | Token/cost telemetry NOT_AVAILABLE cho toàn bộ AI member | Observability & cost | P0 | Journal Entry 002 | Bảng usage (member, model, session) từ nguồn metering, cấp E2 | OPEN |
| GAP-03 | Chuỗi execution/browser chưa E2E verified | Execution | P0 | Journal Entry 002 (tham chiếu DOC-018) | Một tác vụ browser thật: session record + artifact hash, cấp E3 | OPEN |
| GAP-04 | Core owner/API/auth/persistence chưa xác minh; Core execution-grant routes chưa được chứng minh mount vào entrypoint; authoritative Work persistence/owner chưa xác minh | Core authority & orchestration | P0 | Journal Entry 002 + WORK_17_CORE_AUTHORITY_SOURCE_TRACE.md (2026-11-19) | Trace request thật qua Core, grant fail-closed, owner được chỉ định, Work persistence/audit và Host online validation; E3 | OPEN |
| GAP-05 | Xung đột mapping AI-06/AI-07/AI-08 trong DOC-010 | Identity & authorization | P1 | Journal Entry 002 | Quyết định của Vinh + cập nhật DOC-010 v1.2, ghi Decision Log | OPEN |
| GAP-06 | Chênh lệch danh mục: Sandbox 71 Work vs DOC-018 snapshot 56 Work (+15 chưa phân loại) | Portfolio reconciliation | P1 | Journal Entry 002 | Mỗi Work chênh lệch được phân loại: mới hợp lệ / legacy / trùng / anomaly | OPEN |
| GAP-07 | GitHub main chỉ mirror 17 workfolder; 54 Work còn lại không có bản canonical trên GitHub | Evidence & governance | P1 | WORK_17_PORTFOLIO_RECONCILIATION.md kỳ 2026-11-19 | MVSR tăng từ 17/71 lên ≥ 70/71 hoặc ghi rõ ngoại lệ có lý do | OPEN |
| GAP-08 | Journal self-reference commit SHA (Entry 004/005) | Evidence & governance | P2 | Journal Entry 005 | Chuyển sang SYNC_RECORD.md; dừng ghi SHA HEAD vào thân journal | OPEN |
| GAP-09 | Roster DOC-010 v1.1: runtime identity phần lớn NOT VERIFIED; participation khai báo chưa chứng minh | Identity & session | P1 | Journal Entry 002 | Mỗi member được gắn trạng thái theo bộ tiêu chí evidence (E0–E4), không theo khai báo | OPEN |
| GAP-11 | Execution Host nhận WorkContext từ caller và dựa vào boolean `authorized`; chưa thấy service authentication/Core grant online validation trong HTTP Host path; command surface rộng hơn pytest-only contract | Security & execution authority | P0 | WORK_17_CORE_AUTHORITY_SOURCE_TRACE.md; source blobs execution_host/server.py, models.py, security.py, host.py, wee_bridge.py | Host ingress xác thực service identity; Core grant bind Work/purpose/source/policy/expiry; online validate + revoke; pytest-only enforcement; negative integration tests + independent QE; E3 | OPEN |
| GAP-10 | Một số Work tham chiếu kiến trúc cũ cần kiểm soát (legacy references) | Nguồn chuẩn (canonical) | P2 | Journal Entry 002 | Danh sách tham chiếu legacy + đề xuất lỗi thời hóa theo Work 70 | OPEN |

## Quy tắc vận hành register
1. Không đóng gap nào chỉ bằng cách viết thêm tài liệu mô tả; cần bằng chứng đúng cấp.
2. Mỗi gap P0 phải có: owner được chỉ, Work phụ thuộc, mốc dự kiến trước Gate tương ứng.
3. Việc sửa Work thành phần để xử lý gap phải đi qua Gate G7 (sau quyết định của Vinh) và hội ý Work 70.


**GAP-01 addendum — Entry 022 (2026-11-19):** Core is jointly built by Vinh and Xu; no external Core maintainer search is required. Runtime API/router, Assignment persistence and live authorization binding remain NOT VERIFIED. W52 Sandbox contains candidate Codex App Server + Qwen ACP adapters only; both are read-only/no-tool and advertise task.stream_events. Live Codex/Qwen, CorePort/AuthorityPort/W14 HostPort bindings, provider receipt and authenticated ACK remain BLOCKED/NOT VERIFIED. W52 candidate is reusable source, not proven live dispatch. Evidence: Journal Entry 022; W52 WORK_MANIFEST.md, adapter-interface.md, capability-matrix.md, room_a2a/adapters.py, contracts.py, XU_STATIC_REVIEW_R2_20261029.md. Status remains OPEN / P0.


**GAP-01 addendum — Entry 023:** W52 HostPort requires bidirectional long-lived RpcPort; inspected W14 HTTP surface exposes only GET /health and POST /execute with one-shot command/ExecutionResult. W14 adapters inspected are Browser/GitHub/CI, not Codex/Qwen provider transport. No direct W52→W14 HostPort binding proven. W14 RuntimeIdentity is host identity, not AI recipient identity. Caller-supplied WorkContext.authorized is not online Core grant proof (tracked separately by GAP-11). Evidence: Journal Entry 023 and W14 manifest/source paths listed there. GAP-01 remains OPEN / P0.

GAP-01 addendum — Entry 024: Intended chain W70 Assignment/control plane → Core identity/authority/state → W52 provider orchestration → W14 execution/transport → W33 durable evidence → W70 projection is DESIGN ONLY, not live integrated proof. Core HTTP app inspected mounts identity + Meeting routes, not Assignment/Dispatch/Evidence; Agent Registry defers permissions/authority. W70 DOC-044 is template and DOC-095 design baseline, not runtime API. W33 is offline CLI-first store, no HTTP v1; --agent is caller-supplied metadata; A10 integration BLOCKED. Evidence: Journal Entry 024. GAP-01 OPEN/P0, E2/E3 NOT PROVEN.

GAP-01 addendum — Entry 025: Reuse W112 DOC-001 v1.0 as cross-Work contract candidate; it is DRAFT / NOT APPROVED FOR RUNTIME ENFORCEMENT. DOC-001 already defines assignment ACK, event correlation/idempotency, evidence provenance, and MOCK/SNAPSHOT/SANDBOX/LIVE separation. W112 index (dated 2026-11-09) records W52 NOT SYNCED, W33 branch-mapped, W14 partial release-branch sync, W37 investigation workspace; refresh exact canonical repo/branch/commit before integration. Core builder boundary per Vinh: Vinh + Xu. No parallel contract/engine; GAP-01 OPEN/P0, E2/E3 NOT PROVEN.


GAP-01 addendum — Entry 028 (2026-11-19): Positive Core source finding: core/connectors.py contains synchronous OpenAI and Anthropic Meeting-turn connectors behind AgentConnector; however run_meeting_v2.py inspected main path uses build_mock_connectors(), and inspected tests do not prove successful provider HTTP invocation. DiscussionEngine is Meeting participant round-robin, not W70 Work Assignment dispatch. AgentRegistry defers permissions/authority; identity_resolution is registry classification, not provider recipient authentication. AgentResponse does not preserve provider receipt/request ID or assignment/dispatch/attempt/correlation-bound ACK. Reuse candidate exists at provider-call primitive level, but E2 provider delivery receipt and E3 Assignment→Dispatch→Delivery→accountable ACK remain NOT PROVEN. GAP-01 OPEN/P0; Work17 READ/TRACE ONLY; protected execution DENY / NOT RELEASED. Evidence: Journal Entry 028; source blobs core/connectors.py 809c4d2fca01e6fcdaf26b91bf34b1af26dfd15a, core/discussion.py aa722f95235f613c288ba212074527ed2ce01ebc, run_meeting_v2.py 3506137f465c38995fd10472dc2e982f17e23a01, tests/test_connectors.py 356d7580ddef49faf074f9519fbfffc71f7a4a81, tests/test_discussion.py 8028b93be998c122d57cf129d0a3ff12c5734da5.


GAP-01 addendum — Entry 029 (2026-11-19): Core HTTP entrypoint room_hop_mcp/core_http_main.py build_app() constructs MeetingManager/MeetingService and returns create_http_app(service); inspected entrypoint does not import/construct AgentConnector or run_discussion. Inspected room_hop_mcp/adapter/http_server.py exposes only identity + Meeting routes; no Work Assignment/dispatch/provider/receipt/ACK/evidence route. Entrypoint docstring mentions additive Work execution-authority mount but inspected composition/adapter do not show that mount; bounded documentation/source discrepancy only. Therefore Core connector source exists (Entry 028), but connector-to-HTTP runtime wiring and Work dispatch route remain NOT PROVEN. GAP-01 OPEN/P0; E2/E3 NOT PROVEN; READ/TRACE ONLY; protected execution DENY / NOT RELEASED. Evidence: Journal Entry 029; core_http_main.py blob 8dd6bb5ea500026d932ca52eb6079c980d722ab0; http_server.py blob 54cb3ecbce2e6b13083f31c14f0c1f0738f1457d.
