# BIÊN BẢN — WORK 117 ROOM MEDIA HUB
- Document: Canonical Work Minutes
- Work ID: 117
- Date: 2026-11-16
- Authority: Vinh
- Coordinator: Xu / AI-01
- Status: PROVISIONAL — USER DIRECTION CONFIRMED; TECHNICAL CONSULTATION PENDING
- Version: 0.1

## 1. Purpose
Establish a Room-wide image/video library for upload, storage, preview, playback, search, classification, Work association, controlled sharing, audit and recovery.

## 2. Confirmed by Product Owner
1. Storage strategy: HYBRID — internal storage and Cloud.
2. Scope: one shared library for the entire ROOM-HOP, not isolated per-Work silos.
3. Xu is authorized to prepare architecture, consultation plan and this provisional minutes record.
4. No implementation is authorized by this direction alone.

## 3. Existing capabilities and overlap discovered
- Work 33 — ROOM Shared File & Evidence Hub (RSFEH): documented content-addressed blobs keyed by SHA-256, SQLite metadata, audit log, Work/evidence links, CLI operations and local/offline storage. Its document records A1–A9 PASS locally, while live Core/MCP integration is BLOCKED. The documented CLI uses a caller-supplied agent string and is not a complete authorization system.
- Work 26 — Multimodal Camera/Voice Platform: proposes bounded artifact references, permission context, Core as authority, media size/type limits, retention and privacy controls. Its architecture explicitly says proposed contracts must not be assumed implemented.
- Work 29 — HQTT-AI Video Studio: produces video artifacts; potential producer/consumer of media assets, not assumed to be the central media repository.
- Work 116 — Resource Library: catalogs discoverable external tools/resources; not the media binary store.

## 4. Provisional architecture direction
- W117 provides the Media Hub product layer: gallery, albums/collections, media metadata, search, previews, Work associations and media workflows.
- Work 33 is the preferred candidate for the canonical file/blob storage abstraction, subject to code and contract review. Extend through an adapter/approved change; do not fork a second raw-file repository.
- Hybrid topology candidate: internal storage as the primary ingest/cache tier, Cloud object storage as encrypted replica/secondary durability tier. The final primary/replica direction, sync semantics and failover policy remain open pending consultation and cost/security review.
- Core :8000 remains the intended authority for identity, authorization and audit decisions. No direct AI-to-filesystem access. Existing Core contracts must be verified before any integration is described as implemented.
- Media bytes must not be placed in GitHub source history. GitHub stores code, schemas, policy and documentation only.
- Cloud provider, local NAS/storage target, API contracts, encryption/key ownership, retention and RPO/RTO remain undecided.

## 5. Consultation requirement
Consultation must be obtained from relevant roles before architecture baseline:
- Cla / AI-03: technical architecture, storage abstraction, integration feasibility and migration implications.
- Ka / AI-02: independent CSA/security/privacy and architecture-contract review.
- Qw / AI-05: independent QE, testability, integrity, recovery and acceptance criteria.
- Go / AI-06: storage cost, bandwidth, capacity growth and operating-cost model.
- Co / AI coder assistant: implementation feasibility and dependency review, only after architecture scope is clear.
No agent response is recorded as received in this version. Notion Custom Agent discovery was blocked by workspace entitlement; no consultation dispatch is claimed.

## 6. Open decisions
1. Internal storage target: workstation, dedicated NAS, server volume, or managed on-prem object store.
2. Cloud provider and region; data residency and contractual terms.
3. Primary/replica direction, replication mode, conflict handling and offline behavior.
4. Core authorization and signed/short-lived media access contract.
5. Metadata DB ownership and whether Work 33's SQLite catalog is retained, migrated or wrapped.
6. Thumbnail/transcoding worker, supported formats/codecs and resource limits.
7. Encryption at rest/in transit, key ownership, malware scanning and content moderation policy.
8. Retention, legal hold, soft-delete, purge approval and backup/restore.
9. Capacity, max file size, concurrent upload/download, throughput and RPO/RTO.
10. Final W117/W33 boundary and migration plan.

## 7. Decisions not made
- No cloud vendor or paid plan selected.
- No storage endpoint, API route, database schema or production secret approved.
- No existing Core/MCP contract assumed.
- No source code or runtime changed.
- No implementation, test PASS, deployment or release authorized.

## 8. Exit criteria before BUILD
- Requirements and measurable acceptance criteria approved.
- Cla, Ka, Qw and Go consultation findings received or explicitly recorded as unavailable with owner/mitigation.
- Work 33 source/code/API state inspected; integration and migration path evidenced.
- Architecture views, data ownership, security/privacy threat model, failure/recovery, cost and operational model reviewed.
- ADRs record alternatives, trade-offs and unresolved risks.
- Independent review complete.
- Vinh explicitly approves architecture gate and implementation scope.


## 9. Product scope confirmation — 2026-11-16
Vinh reconfirmed the shared-scope direction: ROOM MEDIA HUB is a single Room-wide shared library for ROOM-HOP. It is not a set of isolated per-Work storage silos. Individual Works may have filtered views/collections and access scopes, but the canonical media catalog and asset identity are shared. This does not imply public access; authorization remains mandatory.
This confirms product scope only. It does not approve a storage vendor, detailed topology, API, schema, implementation or BUILD.


## 10. Quyết định bổ sung — ZERO COST FIRST / MIGRATION READY (2026-11-16)
- Authority: Vinh / Product Owner.
- Decision: Giai đoạn hiện tại phải ưu tiên phương án lưu trữ có chi phí thực tế bằng 0 đồng. Chấp nhận đây là giải pháp tạm thời; thiết kế phải cho phép thay nhà cung cấp sau này mà không phải thay đổi Media Catalog hoặc định danh Asset.
- Guardrails:
  1. Không đăng ký gói trả phí, không bật dịch vụ có thể tự động tính phí, không thêm phương thức thanh toán và không phát sinh cam kết chi phí nếu chưa có phê duyệt riêng của Vinh.
  2. Chưa cấp quyền tài khoản, chưa xin/nhận OAuth token, chưa tạo kho thật và chưa tải dữ liệu media thật lên nhà cung cấp.
  3. Chỉ khảo sát tài liệu công khai và thực hiện thử nghiệm bằng dữ liệu giả/không nhạy cảm sau khi có phê duyệt phạm vi thử nghiệm.
  4. Mọi giới hạn miễn phí, quota dùng chung, hạn mức API, điều kiện tài khoản và nguy cơ vượt ngưỡng tính phí phải được ghi rõ; không gọi “miễn phí” nếu có đường phát sinh phí chưa được khóa.
- Preliminary provider findings (public documentation; not runtime-tested):
  - TeraBox: quảng bá 1 TB miễn phí; Open Platform yêu cầu đăng ký riêng client_id/client_secret/private_secret; access token 2 ngày, refresh token 30 ngày. API readiness, eligibility, free-tier API use, quota, stability and account restrictions remain UNVERIFIED.
  - Google Drive: tài khoản Google cá nhân có tối đa 15 GB dùng chung giữa Drive, Gmail và Google Photos; do đó không phải 15 GB riêng cho W117.
  - Cloudflare R2: có free tier 10 GB-month Standard, 1 triệu Class A và 10 triệu Class B operations mỗi tháng; phần vượt quota có đơn giá và có thể phát sinh chi phí. Chỉ xem xét nếu có thể khóa rủi ro billing; không mặc định là zero-cost vô điều kiện.
- Current disposition: TeraBox = candidate to investigate first for advertised free capacity, not selected; Google Drive = low-friction fallback/candidate with small shared quota; R2 = bounded free-tier technical candidate only if billing exposure can be prevented. No provider selected.
- Architecture constraint: provider-neutral storage adapter; canonical Asset ID and metadata independent of provider; store provider/object locator separately; checksum verification; export/migration path; avoid proprietary URLs as canonical identity.
- This decision changes cost priority only. It does not approve architecture baseline, BUILD, account authorization, real-data upload, or deployment.
- Status: USER DIRECTION CONFIRMED; PROVIDER SELECTION PENDING; BUILD NOT AUTHORIZED.


## 11. Quyết định điều chỉnh cơ cấu thi công và quản trị hồ sơ — 2026-11-17
- Authority: Vinh / Product Owner.
- Cla / AI-03 (Claude) được tách khỏi vai trò mặc định trực tiếp xây dựng tính năng. Phạm vi Cla: đối soát kỹ thuật/kiến trúc, lập kế hoạch kỹ thuật, rà soát mã nguồn, sửa chữa, debug và phân tích nguyên nhân gốc.
- Đầu mối xây dựng có hai ứng viên: Go / AI-06 (Grok) hoặc Vibe (Mistral). Việc chọn một lead builder còn mở cho đến khi xác minh quyền truy cập, năng lực công cụ và có bằng chứng nhận việc. Không được ghi nhận Go/Vibe đã nhận việc khi chưa có xác nhận.
- Qc (Qwen Coder) đảm nhiệm viết mã UI/Backend theo task được duyệt và quyền truy cập thực tế. Qw (Qween) là QE/QA độc lập, không tự nghiệm thu phần mình xây dựng. Ka giữ vai trò CSA reviewer. Xu điều phối và quản lý hồ sơ; Vinh giữ quyền quyết định cuối cùng.
- Vinh yêu cầu mỗi Work chỉ duy trì đúng bốn hồ sơ quản trị xuyên suốt: (1) một Nhật ký thi công, (2) một Biên bản, (3) một Plan, (4) một Bảng Task. Các tài liệu kỹ thuật khác chỉ là tài liệu hỗ trợ/bằng chứng, không được tạo thành bản kế hoạch hoặc bảng task cạnh tranh.
- Sandbox và GitHub main là hai môi trường song song xây dựng. Bốn hồ sơ chính thức phải dùng cùng nội dung và đường dẫn tương ứng; thay đổi phải được đối soát và đồng bộ có readback, không tự ý tạo nhánh Work riêng.
- Đây là quyết định về cơ cấu và quản trị dự án. Không phải bằng chứng các AI đã được dispatch/đã nhận việc; không phê duyệt kiến trúc cuối cùng, BUILD, chi phí, upload dữ liệu thật, deployment hoặc release.
- Status: ROLE/RECORD GOVERNANCE DIRECTION CONFIRMED; BUILDER SELECTION OPEN; ARCHITECTURE PROVISIONAL; BUILD NOT AUTHORIZED.


## 12. Quyết định lựa chọn Builder chính và vai trò Vibe — 2026-11-17
- Authority: Vinh / Product Owner.
- Go / AI-06 (Grok) được CHỌN làm Builder chính (đầu mối xây dựng) của W117, chịu trách nhiệm đầu mối triển khai và kết quả xây dựng trong phạm vi task được phê duyệt.
- Vibe (Mistral) được CHỌN làm người phản biện kiến trúc độc lập, đồng thời hỗ trợ xây dựng trên GitHub ở các task được giao. Vibe có quyền nêu phản biện, yêu cầu làm rõ rủi ro và đề xuất phương án khác với Go; không mặc định phải đồng ý với thiết kế của Go. Vibe không thay thế trách nhiệm Builder chính của Go.
- Qc (Qwen Coder) là coder triển khai UI/Backend theo task được giao và phạm vi truy cập thực tế.
- Cla (Claude) chỉ đảm nhiệm đối soát kỹ thuật/kiến trúc, lập kế hoạch kỹ thuật, rà soát mã, sửa chữa, debug và phân tích nguyên nhân gốc; không là Builder tính năng mặc định.
- Qw (Qween) kiểm thử độc lập; Ka phản biện CSA/bảo mật; Xu điều phối và quản lý bốn hồ sơ; Vinh giữ quyền phê duyệt cuối cùng.
- Ranh giới thuật ngữ: BUILD là hoạt động xây dựng/hiện thực hóa sản phẩm bằng mã nguồn và cấu hình theo kiến trúc, yêu cầu và task đã được phê duyệt. Builder là vai trò/người chịu trách nhiệm tổ chức và thực hiện hoạt động BUILD. BUILD không đồng nghĩa với một AI cụ thể, không đồng nghĩa với việc mở một Work mới, và không tự động cho phép deploy/release.
- Trạng thái quyền hạn: lựa chọn vai trò Go/Vibe đã được Vinh quyết định; việc dispatch, nhận task, xác minh quyền truy cập GitHub/công cụ và bắt đầu thi công vẫn cần bằng chứng riêng. Quyết định này KHÔNG tự động phê duyệt BUILD, chi phí, upload media thật, deployment hoặc release.
- Status: BUILDER ROLE DECISION CONFIRMED; EXECUTION DISPATCH/ACCESS PENDING; ARCHITECTURE PROVISIONAL; BUILD NOT AUTHORIZED.


## 13. Quyết định ủy quyền BUILD Dashboard riêng cho Work 117 — 2026-11-17
- Authority: Vinh / Product Owner, direct instruction in the current conversation.
- Scope authorized: A dedicated, read-only operational Dashboard for Work 117 only, focused on Work Overview, Task Board, Agent Monitor and Activity & Evidence.
- Go / AI-06 (Grok) is the single accountable primary Builder and integration lead. Qc supports UI/Backend implementation. Cla provides technical assurance/runtime-contract verification. Ka performs independent CSA/security review. Qw performs independent QE. Vibe may challenge architecture and support scoped GitHub tasks after access/acceptance is verified. Xu coordinates and maintains the canonical records.
- Execution instruction: Independent tasks should proceed in parallel and continue to completion without repeatedly asking Vinh for routine confirmation. Escalate only hard blockers, security/privacy risks, irreversible external actions or work outside this scope.
- Data truth: Dashboard reads the canonical W117 Task Board and Journal. It must not fabricate progress, task completion, Agent online state, dispatch, ACK or runtime activity. Unverified states must be displayed as unverified.
- Explicit boundary: This authorization applies ONLY to the W117 Dashboard. It does not authorize the W117 media-hub product implementation (T009–T011), paid services, billing/payment setup, cloud account/token creation, real-media upload, production deployment or release. Those remain separately gated.
- Status: DASHBOARD BUILD AUTHORIZED; AGENT DISPATCH/ACK NOT VERIFIED; IMPLEMENTATION NOT YET EVIDENCED.


## 14. Quyết định điều chỉnh QE/QA toàn HQTT — áp dụng D70-026 (2026-11-21)
- Authority: Vinh / Product Owner; chỉ thị trực tiếp mới nhất.
- Go / AI-06 thay Qw / AI-05 làm QE/QA mặc định duy nhất trên toàn HQTT và mọi Work. Go đồng thời giữ vai trò CFO/Cost Analyst.
- Qw / AI-05 vẫn tồn tại trong stable roster nhưng không còn giữ vai trò QE/QA mặc định. Các nội dung cũ tại Mục 5 và Mục 13 nhắc Qw làm QE/QA được giữ nguyên như lịch sử tại thời điểm ghi nhận; từ thời điểm D70-026 có hiệu lực, Go là đầu mối QE/QA áp dụng cho W117.
- Quy tắc độc lập: Go không tự review/accept deliverable do Go thực hiện; chỉ định reviewer độc lập khác (ví dụ Ka hoặc reviewer đủ điều kiện khác) cho phần có xung đột.
- Ranh giới: vai trò nghiệp vụ không tự chứng minh Go đã nhận task, đăng nhập GitHub, có session hoặc quyền repository/runtime. Dispatch, access và ACK phải có bằng chứng riêng. Không thay đổi scope BUILD, chi phí, upload media, deployment hoặc release.
- Status: ROLE AUTHORITY UPDATED; DISPATCH/ACCESS NOT VERIFIED; BUILD/RELEASE GATES UNCHANGED.
