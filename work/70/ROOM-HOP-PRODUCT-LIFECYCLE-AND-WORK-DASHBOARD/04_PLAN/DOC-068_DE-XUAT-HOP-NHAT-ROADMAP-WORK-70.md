# DOC-068 — ĐỀ XUẤT HỢP NHẤT ROADMAP VÀ ĐÍCH BÀN GIAO WORK 70
- Document ID: DOC-068
- Version: 1.0
- Date: 2026-11-02
- Owner: Xu / AI-01
- Authority: Vinh
- Status: DRAFT / SOURCE RECONCILIATION COMPLETE / PRODUCT OWNER DECISION REQUIRED / G4 NOT READY
- Depends on: DOC-001, DOC-004, DOC-005, DOC-006, DOC-011, DOC-043, DOC-044, DOC-054, DOC-055, DOC-057, DOC-061, DOC-062, DOC-064, DOC-065, DOC-066, DOC-067, WORK70_SINGLE_DELIVERY_MANDATE.md

## 1. Kết luận điều hành
Đã đọc và đối chiếu nội dung DOC-011, DOC-062, DOC-064, DOC-065, DOC-066, DOC-067 và WORK70_SINGLE_DELIVERY_MANDATE.md trực tiếp từ Sandbox.

Kết luận:
1. DOC-011 là roadmap hiện hành, gồm 6 WP, trạng thái ACTIVE, version 1.2 ngày 2026-10-30.
2. DOC-062 là đề xuất chuẩn hóa 6 WP, ghi rõ PRODUCT OWNER APPROVAL PENDING và G4 NOT READY. DOC-062 đề nghị giữ nguyên 6 WP ID của DOC-011, không biến Build Register candidate thành nguồn chuẩn.
3. WORK70_SINGLE_DELIVERY_MANDATE.md đặt đích bàn giao ở 8 package, nhưng tự ghi PROPOSED DELIVERY BASELINE, NOT GATE PASS, NOT BUILD AUTHORIZATION.
4. DOC-064/065 là kiến trúc và hợp đồng Hybrid AI Dispatch dạng proposal; không chứng minh adapter, Core API hoặc private-session dispatch đã hoạt động.
5. DOC-066 ghi rõ implementation NOT AUTHORIZED / tests NOT RUN; xác nhận MCP 8030 không có công cụ dispatch trực tiếp đến private AI conversations.
6. DOC-067 xác nhận Qw đã ACK WP70-QA và chuẩn bị xong; execution BLOCKED, các test QA-01..QA-08 NOT RUN.
7. Do đó, không có căn cứ thay thế DOC-011 bằng một baseline 8 WP hoặc mở BUILD. Đề xuất giữ 6 WP làm mã kế hoạch chuẩn; tổ chức 8 package của mandate thành các sub-deliverables dưới 6 WP, sau khi Product Owner chấp thuận phạm vi mở rộng.

## 2. Đối chiếu nguồn và thẩm quyền
| Tài liệu | Nội dung xác minh | Thẩm quyền/trạng thái |
|---|---|---|
| DOC-011 | 6 WP, ACTIVE, 1.2 / 2026-10-30 | Roadmap hiện hành |
| DOC-062 | Giữ 6 WP ID; Build Register là candidate; G4 NOT READY | DRAFT, chờ Vinh duyệt |
| WORK70_SINGLE_DELIVERY_MANDATE | 8 package, tiêu chí DONE tổng thể | Đích bàn giao đề xuất; không cấp quyền |
| DOC-064 | Hybrid AI Dispatch architecture | DRAFT; implementation not authorized |
| DOC-065 | Dispatch/ACK/Progress/Result/Review contract | DRAFT; chưa map Core routes |
| DOC-066 | 7 track, Phase 0-6, HD-001..HD-030; tests not run | PLANNED; implementation not authorized |
| DOC-067 | QE plan QA-01..QA-08; Qw ACK; execution blocked | Preparation complete; not test PASS |
| DOC-001 | Phase pointer 01_DISCOVER; G0/G1 NOT_READY | Manifest authority |

## 3. Phương án hợp nhất đề xuất
Giữ 6 WP ID hiện hành để tránh tạo hai hệ thống mã WP cạnh tranh. Phân rã 8 package đích thành 8 sub-deliverables, ánh xạ như sau:

| Sub-deliverable | Nội dung | WP cha DOC-011 | Ghi chú |
|---|---|---|---|
| SD-01 Governance baseline | Manifest, lifecycle, gate, state, registers, canonical ownership | WP-70-01 | Kế thừa mục tiêu hiện tại |
| SD-02 Lifecycle Engine | RESOLVE→BIND→VALIDATE→PREPARE→EXECUTE→TEST→EVIDENCE→FINALIZE; fail-closed, idempotency | WP-70-01 | Mở rộng phạm vi; cần phê duyệt |
| SD-03 Planning/mapping | Work-level plan, mapping, canonical WP source/schema | WP-70-02 | Kế thừa mục tiêu hiện tại |
| SD-04 Hybrid AI Dispatch | Assignment, handoff, delivery, ACK, progress, result, review | WP-70-02 | Phạm vi mới; phụ thuộc Core authority |
| SD-05 Core authority/contracts | Core registry/services, routes, auth, audit, Work scope | WP-70-04 | Giữ trạng thái BLOCKED đến khi Core owner/source được xác minh |
| SD-06 Dashboard | Core-backed read-only UI, freshness/error states, browser E2E | WP-70-03 | Kế thừa mục tiêu hiện tại |
| SD-07 Evidence/export | Durable evidence, integrity, provenance, export | WP-70-05 | DESIGN ONLY đến khi Core/storage contract được duyệt |
| SD-08 QE/acceptance/release/operations | Independent QE, security, integration, acceptance, rollback, operations | WP-70-06 | Bao gồm acceptance/release/operate đầu-cuối |

### Dependency bắt buộc
- SD-01/SD-03: chỉ đọc, reconcile và thiết kế có thể tiếp tục trong phạm vi hiện có.
- SD-05 (Core authority) phải xác minh trước khi SD-02/SD-04/SD-06/SD-07 tích hợp vào authoritative state.
- SD-02/SD-04/SD-06/SD-07 chỉ triển khai thay đổi khi Work Entry authorization và contract tương ứng hợp lệ.
- SD-08 kiểm thử độc lập sau khi có implementation và môi trường được phép.
- Không dùng Sandbox JSON hoặc Dashboard snapshot làm authoritative Core.

## 4. Điều chỉnh vai trò — đề xuất, chưa phải assignment/ACK mới
- Xu: coordination, WP baseline, integration, evidence reconciliation.
- Ka: architecture/security review DOC-061/064/065 và contract delta.
- Vi + Core owner được chỉ định: Core source/API/auth/persistence discovery; không đoán route.
- Co: Lifecycle Engine domain/controller sau contract approval và Work Entry.
- Vi: Dashboard read-only sau Core contract.
- Qw: independent QE; DOC-067 ghi ACK nhưng execution vẫn blocked.
- An: runtime/UI test support; cần xác minh ACK riêng.
- Vinh: phê duyệt thay đổi phạm vi/canonical baseline, gate authority, acceptance/release.
Không suy diễn ACK của Ka/Vi/An từ artefact hoặc tên owner trong tài liệu.

## 5. Quyết định đề nghị Product Owner
D-068-01 (proposed):
- Giữ DOC-011 six-WP IDs làm cấu trúc mã kế hoạch chuẩn.
- Chấp thuận 8 sub-deliverables SD-01..SD-08 làm phân rã phạm vi của WORK70_SINGLE_DELIVERY_MANDATE, gắn vào 6 WP cha theo bảng tại mục 3.
- Cho phép Xu cập nhật DOC-011 version mới, DOC-055 và DOC-006 sau khi quyết định được Vinh chấp thuận.
- Quyết định này KHÔNG mở G4/BUILD; G0/G1 và các gate liên quan vẫn phải đạt bằng evidence.
- DOC-062 được giữ là đề xuất reconciliation hiện có và sẽ được cập nhật trạng thái theo quyết định; không nâng Build Register candidate thành canonical registry tự động.

## 6. Hành động được phép tiếp tục ngay
1. Read-only source tracing để xác định Core owner, repo, routes, auth middleware, persistence, execution entrypoint.
2. Đối chiếu DOC-061 với source evidence và lập danh sách contract gaps.
3. Kiểm tra isolated spike/domain code hiện có; phân biệt unit test với controller/runtime E2E.
4. Chuẩn bị handoff packets cho Ka/Vi/Co/An/Qw; ghi MANUAL_HANDOFF_REQUIRED nếu không có dispatch channel trực tiếp.
5. Hoàn thiện test fixtures/schema validation không sửa authoritative source và không mở quyền thực thi.
6. Sửa tài liệu/register sau khi có quyết định của Vinh; không tự đổi canonical baseline.

## 7. Blockers và trạng thái trung thực
- G0/G1: NOT_READY theo Manifest.
- G4/BUILD: NOT READY / NOT PASS.
- Core owner/API/Auth/persistence: NOT VERIFIED.
- Hybrid dispatch: contract proposal; no private-session dispatch evidence.
- Lifecycle Engine: có isolated spike/domain artifacts trong Sandbox; chưa chứng minh integrated controller execution.
- QE: preparation complete; execution blocked; QA-01..QA-08 NOT RUN.
- Tests HD-001..HD-030: kế hoạch test, không phải kết quả test.
- GitHub sync/branch/commit: chưa được chứng minh trong lần đối chiếu này.
- Release: NOT RELEASED.

## 8. Quy tắc cập nhật sau quyết định
Khi Vinh chấp thuận D-068-01:
1. Cập nhật DOC-006 với decision ID và phạm vi chấp thuận.
2. Cập nhật DOC-011 version mới, giữ 6 WP ID và thêm SD-01..SD-08/dependencies/owners/acceptance.
3. Cập nhật DOC-055 register; không di chuyển DOC-064/065 nếu chưa có controlled migration plan.
4. Đồng bộ DOC-062/DOC-066 và mandate, loại bỏ nội dung trùng/khác trạng thái.
5. Chỉ chuyển assignment sang READY khi DOC-044/DOC-057 đủ source, scope, permission, dependency, reviewer, ACK và evidence plan.
6. G4 chỉ được đánh giá bởi gate evaluator có thẩm quyền dựa trên bằng chứng; tài liệu này không cấp phép BUILD.

---
Prepared by Xu / AI-01. Source content read from Work 70 Sandbox on 2026-11-02.

## 9. Bổ sung bằng chứng Core source — 2026-11-02
- GitHub repository: hqtt2026-thevinhvtqni/room-meeting-ai; default branch: main.
- Main HEAD được xác minh: bb700982f5e01f6eda0d258c2af1f1b3351e8867 (commit 2026-11-01T20:05:06Z).
- Đọc trực tiếp `room_hop_mcp/adapter/http_server.py` trên main; blob SHA: 54cb3ecbce2e6b13083f31c14f0c1f0738f1457d.
- Router đang đăng ký `GET /identities`, các route `/meetings`, `/meetings/{meeting_id}`, `/meetings/{meeting_id}/transcript`, `POST /meetings/{meeting_id}/paste`, và lifecycle meeting `POST /meetings`, `/open`, `/join`, `/start`, `/close`.
- Không thấy Work-scoped Work/WP/Assignment/Evidence routes trong router này. Đây là kết luận giới hạn ở router/file/revision đã đọc, không phải khẳng định toàn repository không có route khác.
- Search GitHub cho thấy `DASHBOARD_CORE_READ_CONTRACT.md` ghi các route Work là endpoint đề xuất, không khẳng định tồn tại.
- Hệ quả: WP-70-04/SD-05 tiếp tục BLOCKED; không được dùng các route đề xuất làm API thật. Cần xác định Core owner và kiểm tra router/service khác trước khi kết luận toàn hệ thống.

## 10. Bổ sung kiểm tra GitHub branch — 2026-11-02
- Repository: `hqtt2026-thevinhvtqni/room-meeting-ai`.
- Compare `main...work/70/05-build`: status `diverged`, ahead_by=42, behind_by=399, merge base `fc6a19888765d174aea9aea839620338ac9f71e8`.
- Compare response liệt kê 14 file Work 70 được thêm trên branch, đều là hồ sơ/tài liệu/schema/mapping; không có file source Core/Engine/Dashboard được thay đổi trong danh sách compare này.
- Không merge, rebase hoặc cherry-pick. Chênh lệch 42/399 làm cho thao tác hợp nhất mù có rủi ro cao.
- Main HEAD tại lần kiểm tra: `bb700982f5e01f6eda0d258c2af1f1b3351e8867`. Các commit DOC-068, DOC-055, DOC-035 sau đó được tạo trên main theo chuỗi riêng; không thay đổi branch work/70/05-build.
- Hệ quả: GitHub branch sync của DOC-068/055/035 hiện có thể xác minh trên main; không có bằng chứng branch work/70/05-build đã nhận các tài liệu mới hoặc source implementation. Cần lập controlled sync plan riêng, không merge/rebase tự động.

## 11. Bổ sung quét HTTP route trên main — 2026-11-02
- GitHub code search trên main cho `@app.get`, `@app.post`, `FastAPI(` và `create_http_app` trả về các adapter files: `room_hop_mcp/adapter/http_server.py`, `room_hop_mcp/adapter/browser_server.py`, `room_hop_mcp/browser_agent_adapter/adapter.py`.
- Đã đọc `room_hop_mcp/adapter/browser_server.py`, blob SHA `1b9dfe4b9d3f62e08a324ff146a9a50bb63e1313`; chỉ thấy các route Meeting list/get/transcript/paste.
- Đã đọc `room_hop_mcp/browser_agent_adapter/adapter.py`, blob SHA `0ced9207c1897b9a7b572b7fefa44fec2dd92b76`; đây là browser workflow adapter, không phải Work/WP/Assignment registry API.
- Search `APIRouter`, `include_router`, `WorkRegistry`, `EvidenceRegistry` không trả kết quả trong phạm vi GitHub code search hiện tại.
- Kết luận giới hạn: các HTTP adapter files được tìm thấy trên main hiện không cung cấp Work-scoped lifecycle APIs. Cần kiểm tra thêm service/runtime composition và xác định Core owner; không tuyên bố toàn repository không có implementation nếu chưa quét toàn bộ.
