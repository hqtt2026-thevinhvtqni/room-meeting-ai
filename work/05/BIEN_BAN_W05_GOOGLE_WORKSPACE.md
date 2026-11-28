# BIÊN BẢN WORK 05 — GOOGLE WORKSPACE / DOCS / DRIVE

> RECOVERY VERSION — 2026-09-29
> Nguồn: nội dung trao đổi Work 05 đã có trong phiên làm việc và nội dung phục hồi do CEO Vinh cung cấp.
> Trạng thái: RECOVERED / RECONSTRUCTED. Không coi phần phục hồi là bản gốc nguyên byte.

## 0. RECOVERY NOTE

Ngày 2026-09-29, trong quá trình ghi Section 16 Vibe Mitra, Xu đã dùng sandbox_write với chỉ nội dung mới. sandbox_write có semantics ghi đè toàn bộ file, nên nội dung cũ của biên bản bị thay thế. Đây là lỗi thao tác của Xu.

Chỉ thị phục hồi của CEO Vinh: có thể ghi thẳng toàn bộ nội dung trao đổi vào biên bản, không cần trắc lọc. Vì vậy tài liệu này ưu tiên bảo toàn thông tin và lịch sử trao đổi thay vì chỉ giữ bản tổng hợp cuối.

Nguyên tắc sau sự cố: READ CURRENT → PRESERVE CURRENT → APPEND/RECONSTRUCT → WRITE FULL CONTENT → READ BACK → VERIFY. Không dùng sandbox_write với chỉ phần mới.

## 1. MỤC TIÊU WORK 05

Work 05 — Google Docs / Google Drive nhằm nghiên cứu và xây phương án toàn trình cho phép nhiều AI agents và con người cùng tạo, đọc, ghi, cập nhật biên bản trên Google Docs/Drive; phải có đồng bộ, xử lý ghi đồng thời, versioning, logging và evidence kiểm thử.

Chỉ đạo của Vinh: các AI tự xây phương án toàn trình độc lập trước; Xu không được khóa kiến trúc từ đầu. Sau khi thu đủ proposal mới tổng hợp và kiểm chứng bằng evidence.

## 2. CÁC PHƯƠNG ÁN ĐỘC LẬP ĐÃ THU

### Go/Grok
- Backend/service layer giữa AI và Google APIs.
- Google Cloud Project; Docs API + Drive API.
- Service Account hoặc OAuth/domain-wide delegation; Shared Drive hoặc My Drive.
- AI → Backend → lock → Google APIs → response/log → AI.
- Revision control với requiredRevisionId và targetRevisionId; lock + revision; retry; quota/error handling.
- Create/copy template/move/update/batchUpdate; read bằng documents.get; export PDF/DOCX.
- Đề xuất test concurrent, conflict, retry, latency, no data loss.
- Khi đưa vào ROOM-HOP phải map qua kiến trúc hiện hữu: AI → MCP 8020 → Core 8000 → Google Workspace Adapter; không tạo Core 2.

### Claude / Cla
- Shared Google Docs/Drive minutes cho nhiều AI.
- Optimistic locking, content-aware merge/OT-like approach, backend Service Account + AI tokens.
- Versioning, checksum, atomic writes, hybrid polling/event, retry.
- Python/Flask; Dev → Staging → Production; unit/integration/load tests.
- Cần kiểm chứng các tuyên bố về auto-resolve, OT và latency/quota trước khi triển khai.

### Manus
- E2E middle layer cho multi-AI + Google Docs/Drive.
- Shared Drive/ACL/OAuth/service account/DWD.
- changes.list, changes.watch, webhook, reconciliation.
- requiredRevisionId/targetRevisionId.
- API/connector, data model, command, idempotency, audit log, versioning, logging, quota, retry, DLQ.
- One meeting = one Google Doc; structured sections: metadata, participants, agenda, decisions, action items, unresolved/disagreements, update history.
- Queue partition/distributed lock theo document_id; revision bảo vệ khỏi external edits; stale revision → reread/rebase/new patch/CONFLICT, không blind retry.
- Sync cursor + dedup + periodic reconciliation; có thể mở rộng Workspace Events/PubSub.
- Metadata DB: meetings, commands, outbox, sync_cursors, audit_events, locks, oauth_accounts.
- Audit append-only; API POST/GET meeting, commands, sync, webhook, permissions.
- Test auth, create/move/ACL, read/revision/parser, concurrent requiredRevision, target revision append, human edit sync, watch renewal, 429/503/DLQ/idempotency, revoke permission, log redaction.

### Kha / Gemini
- Multi-AI / Users → API Gateway/Backend Connector → Service Layer → Google Drive & Docs API.
- JWT/OAuth2, RBAC, rate limiting, circuit breaker.
- Redis distributed lock + Google revision + DB.
- Drive copy_file rồi Docs batchUpdate; replaceAllText; insertText/deleteContentRange.
- SA/DWD; logging agent/user/action/file/status/execution time.
- Native Google revision + application document_versions.
- 429 exponential backoff + jitter; timeout queue; 409 conflict.
- Test create/read/concurrent update/429/token expiry.
- Khi tổng hợp phải map vào Core/MCP hiện hữu và giữ độc lập proposal.

## 3. CHỈ ĐẠO MỚI — AI TỰ XÂY TOÀN TRÌNH

Work 05 không được Xu pre-lock architecture. Mỗi AI phải tự nghiên cứu và đề xuất toàn trình: Google Docs/Drive API, create/manage docs, minutes storage/read/write/update, multi-AI access, auth/authz, sync, API/backend/connector, data flow, logging, versioning, errors, deployment, tests và evidence.

Mục tiêu: independent proposals → collect → Vinh/Xu synthesize → final architecture → implementation.

## 4. DEEPSEEK — PHƯƠNG ÁN ĐỘC LẬP

DeepSeek đề xuất mô hình Collaborative Minutes với Work05 Backend/Connector ở giữa và Google Docs làm nơi lưu nội dung. Nguyên tắc: evidence-first; write dựa trên revision thực tế; fail-safe conflict; idempotent retry.

Auth: Service Account là phương án chính; OAuth2 cho UI/admin; Secret Manager; AI không giữ Google credentials. Data model: Work05/Minutes, Templates, metadata/index. Một meeting = một Google Doc; có headings/named ranges như RANGE_DECISIONS và RANGE_ACTION_ITEMS.

REST: create/read/full update/section update/append/revisions/search/lock. Safe write: acquire lock → documents.get revision+structure → AI PATCH → batchUpdate → requiredRevisionId → mismatch thì reread/replan → audit → release.

requiredRevisionId cho vùng nhạy cảm như Decisions/Action Items; targetRevisionId cho append/merge phù hợp. Create: documents.create → Drive files.update để đưa vào folder → batchUpdate template.

Sync: Drive changes.watch, renew channel, notification không chứa full change nên cần polling/reconciliation bổ sung. Logging/audit gồm timestamp, agent, action, document, revision before/after, section, status, latency.

Stack đề xuất: FastAPI, google-api-python-client/google-auth, Redis, PostgreSQL hoặc Cloud Logging, Secret Manager, Cloud Run. Test create/read/update/append, concurrent conflict, revision mismatch, target revision, 429, lock expiry, webhook.

Điểm đóng góp đáng giữ: safe write + revision/index + fail-safe conflict. Cảnh báo: không biến Google Docs thành Core 2 vì ROOM-HOP đã có Core :8000 là single truth.

## 5. MÊ / META — PHƯƠNG ÁN ĐỘC LẬP

Mục tiêu: N AI agents + humans cùng create/read/write/update minutes, sync, không mất dữ liệu, versioning/logging/evidence.

Mê đề xuất mỗi minutes = Google Doc + metadata JSON sidecar; giữ cấu trúc 7 Work05 folders.

Architecture: AI Agents → WORK05 Backend Service FastAPI → Google Workspace Connector → Drive API v3 + Docs API v1.

Middleware xử lý queue, lock, retry, versioning. Docs structured content; batchUpdate InsertText/ReplaceAllText; không export TXT để ghi.

Auth: Service Account + DWD là primary; OAuth2 User Consent cho user/admin; AI không giữ Google credentials.

REST: POST /v1/bienban; GET /v1/bienban/{id}; POST append; PUT section; POST/DELETE lock.

Append flow: AI ai_id/content → Redis lock → current version/structure → batchUpdate → log/update metadata/release lock.

Ba cơ chế concurrency: Redis distributed lock; expected_version; append-only default cho AI. PUT overwrite chỉ dành cho lead/Xu/Vinh. Conflict trả VERSION_CONFLICT/409 và yêu cầu GET lại.

Sync: polling khoảng 10 giây + revisions.list; webhook chưa dùng ở PoC. Logging Cloud Logging + JSON evidence; Google revisions + snapshot mỗi 10 versions.

Test: create/read checksum; 5 concurrent append; concurrent PUT cùng expected_version; auth; manual Docs edit detection.

Điểm cần kiểm chứng: Redis lock không thay thế Google revision; expected_version không nhất thiết bằng Google revision; polling 10s là tham số vận hành chứ chưa phải chuẩn đã chứng minh; JSON sidecar có nguy cơ tạo second truth.

## 6. VIBE MITRA — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

Vibe Mitra báo cáo đã nghiên cứu evidence về Google Docs API, Drive API, versioning, sync, auth, quota và năng lực connector Google Drive; đã đối chiếu cấu trúc Drive hiện tại của team.

Đã thấy trên Drive của Vinh: folder 05 / GOOGLE-WORKSPACE-DOCS-DRIVE với 7 sub-folder 00_ROOT, 01_ORIGINAL, 02_EXTENSION, 03_ARCHITECTURE, 04_CODE, 05_TEST, 06_EVIDENCE, 07_RELEASE; cùng BIEN_BAN_W05_GOOGLE_WORKSPACE.md/.txt.

Vibe xác định biên bản đã có là tài sản gốc và đề xuất xây connector bao quanh, không đè biên bản.

### 6.1 Mục tiêu
Xây hệ thống cho phép N AI agents + con người cùng tạo/đọc/ghi/cập nhật biên bản trên Google Docs/Drive; đảm bảo đồng bộ, không mất dữ liệu khi ghi đồng thời, versioning, logging và evidence.

### 6.2 Kiến trúc 3 lớp
AI Agents Layer → WORK05 Backend Service — Python FastAPI → Google Workspace Connector Layer → Google Drive API v3 + Google Docs API v1.

Lý do không cho AI gọi trực tiếp Google API: cần lớp trung gian cho queue, lock, retry và versioning.

### 6.3 Data Model
Giữ cấu trúc Work05/7 folders. Mỗi biên bản có doc_id, drive_file, bien_ban_id, title, owner, created_by_ai, status, version, checksum, last_sync. Nội dung Doc chuẩn hóa bằng Heading 1/2/3; bảng dùng Table trong Docs API.

### 6.4 Google API
Tạo/lưu trữ dùng Drive API; đọc dùng documents.get; ghi/cập nhật dùng documents.batchUpdate với InsertTextRequest/ReplaceAllTextRequest; versioning tham khảo Drive revisions.list/revisions.get. Không dùng export TXT để ghi vì mất cấu trúc bảng/format.

### 6.5 Authentication
Vibe đề xuất Service Account + Domain-wide Delegation cho team; OAuth2 User Consent cho end user. AI không cần trực tiếp giữ Google credentials.

### 6.6 Connector/API
Work05Connector gồm create_bien_ban, read_bien_ban, append_section, update_section, list_bien_ban, lock_doc. REST gồm POST /v1/bienban, GET /v1/bienban/{id}, POST /append, PUT /section, POST/DELETE lock.

### 6.7 Data Flow
AI POST append → backend kiểm tra lock → lấy current_version → documents.get lấy endIndex → batchUpdate chèn vào cuối → log → tăng version → release lock.

Google → system → AI: Vibe chọn polling và revisions.list thay vì webhook trong PoC.

### 6.8 Đồng bộ/Concurrent Update
Ba cơ chế: Redis distributed lock với SET doc:{id}:lock ... NX EX; optimistic concurrency bằng expected_version; append-only default cho AI. PUT overwrite dành cho lead/Xu/Vinh.

Conflict trả VERSION_CONFLICT/409, current_version và your_version, yêu cầu AI GET lại.

### 6.9 Logging/Versioning/Error
Mỗi batchUpdate ghi Cloud Logging và evidence JSON trong 06_EVIDENCE. Dùng Drive revisions; snapshot JSON mỗi 10 versions. 403 rateLimitExceeded → exponential backoff; 404 notFound → document bị xóa; 409 → conflict; chuẩn hóa error response.

### 6.10 Triển khai
B1 chuẩn bị Service Account và quyền folder 05. B2 mở rộng sandbox_service.py thành Work05Connector, deploy FastAPI Cloud Run. B3 migration hai file biên bản sang Docs thật. B4 multi-AI test harness cho 5 AI append trong 30 giây.

### 6.11 Test/Evidence
test_create_read: create → read → checksum; test_concurrent_append: 5 threads cùng append; test_conflict: hai AI PUT cùng expected_version; test_auth: quyền đúng/sai; test_offline_edit: người sửa Docs web và backend phát hiện revision tăng.

### 6.12 Risks
Race condition khi Redis chết; index drift; quota; Shared Drive vs My Drive. Vibe đề xuất kiểm tra documents.get ngay trước batchUpdate và không cache index quá lâu.

### 6.13 Các quyết định Vibe đưa ra để Vinh/Xu xem xét
1. Service Account hay OAuth user — Vibe nghiêng SA.
2. Append-only hay edit tự do — Vibe nghiêng append-only cho AI, lead được overwrite.
3. Google Doc thuần hay Doc + JSON sidecar — Vibe nghiêng cả hai.
4. Giữ 7 folder hiện tại — Vibe nghiêng giữ nguyên vì đã có evidence.

### 6.14 Nội dung trao đổi về Vibe
Vibe đã nghiên cứu evidence về Google Docs/Drive API, requiredRevisionId, Changes API, oplog JSONL, build-vs-buy connector, failure point E4 khi human edit trong lúc AI append, 3 implementation options, 7 PoC experiments và khoảng 25 sources. Một hướng được nêu là thử open-source MCP server piotr-agier/google-drive-mcp với optimistic locking ifRevisionId/team-mode, sau đó thay bằng custom backend nếu cần policy sâu hơn. Đây là proposal cần kiểm chứng, không phải quyết định cuối.

## 7. CÁC ĐIỂM SO SÁNH ĐƯỢC GHI NHẬN TRONG TRAO ĐỔI

Mê thiên về implementation-oriented: FastAPI, connector, Redis lock, expected_version, append-only, polling và concurrent test harness.

DeepSeek thiên về safe write/revision/index, requiredRevisionId, fail-safe conflict, idempotency, audit, sync cursor và reconciliation.

Go/Grok thiên về Google API/revision/lock/quota/operation.

Claude tập trung optimistic locking, merge/conflict và consistency.

Manus tập trung vòng đời E2E: command, idempotency, audit, sync, recovery, DLQ và reconciliation.

Nguyên tắc của Work 05: không xếp hạng AI, không chọn winner. Mỗi proposal là một nguồn đóng góp độc lập; chỉ sau khi thu đủ mới tổng hợp và chạy evidence.

## 8. GHI NHẬN TRAO ĐỔI CỦA XU VỚI CEO VINH

Vinh yêu cầu AI tự xây toàn trình, Xu tổng hợp từ các AI thay vì tự thiết kế trước. Xu đã đồng ý rằng giá trị của Work05 nằm ở việc nhiều AI tự xây các phương án khác nhau rồi dùng evidence để tổng hợp.

Vinh nhắc rằng Xu là CEO/Quản lý tổng hợp phải giữ biên bản và bằng chứng. Xu thừa nhận việc dùng sandbox_write sai khiến mất nội dung là FAIL về thao tác tài liệu, FAIL về kiểm soát trước khi ghi và FAIL về vai trò tổng hợp.

Xu đã chốt nguyên tắc phục hồi: không tự bịa phần mất; tìm bản gốc/backup; nếu không có thì đánh dấu RECOVERY GAP hoặc RECONSTRUCTED thay vì gọi là bản gốc.

CEO Vinh sau đó cung cấp toàn bộ nội dung trao đổi và cho phép ghi thẳng toàn bộ nội dung trao đổi vào biên bản, không cần trắc lọc.

## 9. TRẠNG THÁI HIỆN TẠI

DONE: đã nhận nguồn phục hồi do CEO Vinh cung cấp.
DONE: đã đọc WORK_MANIFEST.md của Work 05; manifest xác nhận Work ID 05, Work Name GOOGLE-WORKSPACE-DOCS-DRIVE, Status ACTIVE, Created 2026-09-28.
RECOVERED: các proposal và trao đổi hiện có trong context được đưa vào biên bản này.
RECONSTRUCTED: một số section cũ được phục hồi từ nội dung trao đổi/context thay vì bản file nguyên gốc.
RECOVERY GAP: chưa có bằng chứng file-level để khẳng định từng ký tự của Sections 1–13 trùng bản trước sự cố.
NOT FINAL: chưa có kiến trúc cuối cùng; chưa có winner/ranking giữa các AI.

## 10. QUY TẮC CẬP NHẬT BIÊN BẢN SAU SỰ CỐ

1. Đọc file hiện tại trước.
2. Không dùng sandbox_write với chỉ phần mới.
3. Nếu sandbox_write bắt buộc dùng, phải gửi toàn bộ nội dung file đã giữ nguyên + phần mới.
4. Sau write phải sandbox_read lại.
5. Kiểm tra section count, heading cuối, và nội dung trước/sau.
6. Nếu có bất kỳ nghi ngờ nào: STOP, không ghi tiếp.

## 11. CHỈ THỊ CỦA CEO

Work 05 tiếp tục theo hướng: thu thập phương án độc lập → giữ nguyên evidence → tổng hợp → kiểm chứng → mới chốt kiến trúc và triển khai.

Không để sự cố biên bản làm thay đổi nguyên tắc: ưu tiên sự thật hơn sự hào hứng; evidence trước, suy đoán sau.

## 12. COPILOT — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

Nguồn: nội dung do Copilot cung cấp ngày 2026-09-29. Đây là proposal độc lập, ghi nguyên nội dung kỹ thuật chính vào biên bản để Xu tổng hợp sau; chưa coi là kiến trúc cuối cùng.

### 12.1 Kiến trúc tổng thể
- Google Docs API và Google Drive API làm nền tảng.
- Backend Connector: service trung gian Node.js/Express hoặc Python/FastAPI để AI giao tiếp với Google API.
- Authentication/Authorization: OAuth 2.0 với scope `https://www.googleapis.com/auth/documents` và `https://www.googleapis.com/auth/drive.file`.
- Data Flow: AI → Backend → Google Docs/Drive → Backend → AI.
- Concurrency Control: Google Docs batch updates + Drive revisions.
- Logging & Versioning: backend log + Drive revision history.

### 12.2 Quy trình toàn trình
1. Tạo Google Doc: AI yêu cầu tạo biên bản → Backend gọi `documents.create` → lưu Doc ID vào DB.
2. Lưu trữ: biên bản lưu trên Google Drive; metadata Doc ID, người tạo, timestamp lưu trong DB backend.
3. Đọc: Backend gọi `documents.get`, trả về JSON structured text + styles.
4. Ghi/cập nhật: Backend gọi `documents.batchUpdate`; hỗ trợ append text, replace text, insert table, format.
5. Nhiều AI cùng truy cập: mỗi AI có token riêng; Drive permissions share Doc với email/service account; dùng revision ID để phát hiện xung đột.
6. Authentication: OAuth 2.0 flow AI → Backend → Google Auth → Token; refresh token duy trì session.
7. Đồng bộ: mỗi update kèm revision ID; mismatch → backend merge hoặc báo conflict; Copilot nêu CRDT (Conflict-free Replicated Data Type — cấu trúc dữ liệu có thể hợp nhất không xung đột) như một khả năng cho text merge.
8. API/backend/connector:
   - `POST /docs/create`
   - `GET /docs/{id}`
   - `POST /docs/{id}/update`
   - `GET /docs/{id}/history`
   - `POST /docs/{id}/share`
9. Data Flow: AI gửi JSON → Backend xử lý → Google API → response → Backend chuẩn hóa → AI.
10. Logging/Versioning/Error Handling: log request/response; Drive revision history để rollback; retry exponential backoff.
11. Triển khai: Backend trên Kubernetes/Docker; OAuth credentials lưu trong Vault; CI/CD pipeline.
12. Test/Evidence: unit test backend API; integration test Google Docs API; evidence tạo Doc, update, đọc lại, kiểm tra revision.

### 12.3 Rủi ro và điểm cần quyết định
- Token hết hạn → refresh.
- Conflict khi nhiều AI update đồng thời.
- Google API quota limit.
- Chọn DB backend: Postgres vs MongoDB.
- Chọn merge strategy: last-write-wins vs CRDT.
- Chọn logging: local hoặc cloud logging/ELK.

### 12.4 Nhận xét để Xu giữ khi tổng hợp
Proposal của Copilot đã đi từ kiến trúc → flow → API → dữ liệu → auth → concurrency → logging/versioning → deployment → test → risks/decisions. Các điểm cần kiểm chứng trước khi đưa vào kiến trúc ROOM-HOP cuối cùng gồm: semantics và khả năng áp dụng thực tế của revision ID cho từng loại update; cách merge khi revision mismatch; phạm vi phù hợp của `drive.file`; OAuth/token model khi AI hoạt động qua MCP/Core; Kubernetes/Vault có thực sự cần thiết ở PoC hay không; và CRDT có cần thiết cho structured Google Docs minutes hay chỉ nên dùng fail-safe conflict + reread/replan.

### 12.5 Nguyên tắc giữ proposal
Không xếp hạng Copilot với các AI khác tại bước này. Copilot được giữ như một nguồn thiết kế độc lập để đối chiếu với Go/Grok, Claude, Manus, Kha/Gemini, DeepSeek, Mê/Meta và Vibe Mitra trong bước synthesis/evidence sau.


## 13. OUTLITE — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

Nguồn: nội dung do CEO Vinh cung cấp trong phiên ngày 2026-09-29, được yêu cầu ghi biên bản với nhãn **OUtlite / OUTLITE**. Nội dung proposal này có mức độ trùng lặp cao với Section 12 (Copilot); tại bước thu thập chưa coi đây là hai kiến trúc khác nhau nếu chưa xác nhận nguồn/định danh. Không xếp hạng.

### 13.1 Kiến trúc tổng thể
- Google Docs API và Google Drive API làm nền tảng.
- Backend Connector: service trung gian Node.js/Express hoặc Python/FastAPI để AI giao tiếp với Google API.
- Authentication/Authorization: OAuth 2.0 với scope `https://www.googleapis.com/auth/documents` và `https://www.googleapis.com/auth/drive.file`.
- Data Flow: AI → Backend → Google Docs/Drive → Backend → AI.
- Concurrency Control: Google Docs batch updates + Drive revisions.
- Logging & Versioning: backend log + Drive revision history.

### 13.2 Quy trình toàn trình
1. Tạo Google Doc: AI gửi yêu cầu tạo biên bản → Backend gọi `documents.create` → lưu Doc ID vào DB.
2. Lưu trữ: biên bản lưu trực tiếp trên Google Drive; metadata gồm Doc ID, người tạo, timestamp lưu trong DB backend.
3. Đọc: AI yêu cầu đọc → Backend gọi `documents.get`; trả về JSON gồm structured text + styles.
4. Ghi/cập nhật: Backend gọi `documents.batchUpdate`; hỗ trợ append text, replace text, insert table, format.
5. Nhiều AI cùng truy cập: mỗi AI có token riêng; Drive permissions share Doc với email/service account; dùng revision ID để phát hiện xung đột.
6. Authentication: OAuth 2.0 flow AI → Backend → Google Auth → Token; refresh token để duy trì session.
7. Đồng bộ: mỗi update kèm revision ID; mismatch → backend merge hoặc báo conflict; có thể dùng CRDT (Conflict-free Replicated Data Type — cấu trúc dữ liệu có thể hợp nhất không xung đột) để merge text.
8. API/backend/connector:
   - `POST /docs/create`
   - `GET /docs/{id}`
   - `POST /docs/{id}/update`
   - `GET /docs/{id}/history`
   - `POST /docs/{id}/share`
9. Data Flow: AI gửi request JSON → Backend xử lý → Google API → response → Backend chuẩn hóa → AI.
10. Logging/Versioning/Error Handling: log mỗi request/response; Drive revision history để rollback; retry với exponential backoff.
11. Triển khai: Backend chạy trên Kubernetes/Docker; Secrets OAuth credentials lưu trong Vault; CI/CD pipeline.
12. Test/Evidence: unit test cho API backend; integration test với Google Docs API; evidence tạo Doc, update, đọc lại, kiểm tra revision.

### 13.3 Rủi ro và điểm cần quyết định
- Token hết hạn → cần refresh.
- Conflict khi nhiều AI update cùng lúc.
- API quota limit.
- Chọn DB backend: Postgres vs MongoDB.
- Chọn merge strategy: last-write-wins vs CRDT.
- Chọn logging: local hay cloud logging/ELK.

### 13.4 Ghi chú của Work 05
Proposal OUTLITE được giữ như nguồn độc lập theo chỉ đạo “AI tự xây toàn trình → Xu tổng hợp”. Tuy nhiên, vì nội dung hiện tại trùng cao với Section 12 Copilot, Xu không tự tách thành một “phương án thắng” hoặc tạo khác biệt giả. Việc xác định đây là cùng nguồn hay hai nguồn độc lập sẽ được giữ ở trạng thái cần xác nhận nếu sau này cần thống kê số lượng AI/proposal.

### 13.5 Trạng thái
RECEIVED — đã nhận đầy đủ nội dung proposal trong phiên.
RECORDED — đã ghi vào biên bản Work 05.
NOT FINAL — chưa kiểm chứng semantics của revision/concurrency, scope OAuth, CRDT, deployment stack hoặc mapping cuối vào Core/MCP ROOM-HOP.


## 13. OUTLITE — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

Nguồn: proposal do CEO Vinh cung cấp và yêu cầu ghi biên bản với nhãn OUTLITE. Nội dung có mức độ trùng lặp cao với Section 12 (Copilot), nên chưa coi là một kiến trúc khác biệt nếu chưa xác nhận định danh nguồn.

### 13.1 Kiến trúc
Google Docs API + Google Drive API; Backend Connector bằng Node.js/Express hoặc Python/FastAPI; OAuth 2.0 với scopes documents và drive.file; luồng AI → Backend → Google Docs/Drive → Backend → AI; batchUpdate + Drive revisions; backend logging/versioning.

### 13.2 Flow toàn trình
Tạo Doc bằng documents.create và lưu Doc ID vào DB; lưu biên bản trên Drive và metadata trong DB; đọc bằng documents.get; cập nhật bằng documents.batchUpdate với append/replace/insert table/format; nhiều AI dùng token và Drive permissions; refresh token cho OAuth; revision mismatch thì merge hoặc báo conflict; CRDT được nêu như khả năng merge text.

### 13.3 API
POST /docs/create; GET /docs/{id}; POST /docs/{id}/update; GET /docs/{id}/history; POST /docs/{id}/share.

### 13.4 Logging / Versioning / Error
Log request/response; Drive revision history để rollback; retry exponential backoff.

### 13.5 Deployment
Backend chạy Kubernetes/Docker; OAuth credentials lưu trong Vault; CI/CD pipeline.

### 13.6 Test / Evidence
Unit test backend API; integration test Google Docs API; evidence create Doc, update, read-back và kiểm tra revision.

### 13.7 Risks / Decisions
Token expiry; concurrent conflict; API quota; chọn Postgres hoặc MongoDB; last-write-wins hoặc CRDT; local/cloud logging hoặc ELK.

### 13.8 Trạng thái ghi nhận
RECEIVED → RECORDED. Chưa final. Các điểm revision/concurrency, OAuth scope/token model, CRDT và deployment stack vẫn phải được evidence kiểm chứng trước khi đưa vào kiến trúc ROOM-HOP cuối cùng.


## 14. KA / CSA — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

**Nguồn:** Ka / CSA — 2026-09-29.  
**Trạng thái:** PROPOSAL INDEPENDENT / NOT FINAL. Chưa triển khai, chưa xếp hạng.

### 14.1 Mục tiêu

Xây lớp Document Collaboration Boundary dựa trên Google Docs / Google Drive cho phép AI và con người tạo, đọc, append, update biên bản; hỗ trợ multi-AI access, authentication/authorization, concurrent update, sync, versioning, audit, logging, error handling, deployment và evidence.

### 14.2 Kiến trúc

```
AI Members
   |
ROOM-HOP Core
   |
WORK 05 Document Service
   |-- Document Registry
   |-- Access Policy
   |-- Write Queue
   |-- Conflict Manager
   |-- Sync Worker
   |-- Audit Logger
   |
   +-- Google Docs Connector
   +-- Google Drive Connector
             |
       Google Workspace
```

AI không gọi Google API trực tiếp. Core không phụ thuộc trực tiếp Google API. Document Service là boundary.

### 14.3 Document Registry

Registry giữ mapping Work/Meeting → Drive location → Google Doc ID. Metadata tối thiểu: work_id, meeting_id, document_id, drive_id, folder_id, document_type, status, last_known_revision, schema_version.

Không tìm document bằng filename mỗi lần.

### 14.4 Canonical Document và Audit Store

Tách:

- **Canonical Document:** Google Doc, phục vụ đọc/cộng tác/trình bày.
- **Audit Store:** backend lưu operation_id, actor, operation, payload hash, base/result revision, status, timestamp, request_id và lỗi/retry.

Google revision history không phải audit log duy nhất.

### 14.5 Create / Read / Write

Create:

```
POST /v1/work-documents
 -> verify Work/actor/policy
 -> documents.create
 -> Drive placement
 -> Registry
```

Read:

```
GET /v1/work-documents/{work_id}
 -> registry
 -> documents.get
 -> normalize
```

Write không expose raw Google Docs Request cho AI. Operation vocabulary: APPEND, INSERT, REPLACE/section update.

API đề xuất:

```
POST  /v1/work-documents
GET   /v1/work-documents/{work_id}
POST  /v1/work-documents/{work_id}/entries
PATCH /v1/work-documents/{work_id}/sections/{section_id}
GET   /v1/work-documents/{work_id}/history
POST  /v1/work-documents/{work_id}/sync
GET   /v1/work-documents/{work_id}/status
GET   /v1/work-documents/{work_id}/operations/{operation_id}
```

### 14.6 Authentication / Authorization

Hai hướng credential:

1. OAuth user authorization.
2. Service Account / Shared Drive.

Credential chỉ tồn tại ở backend/connector boundary.

Có hai lớp authorization:

```
ROOM-HOP Policy
+
Google Drive ACL
```

Google ACL không thay semantic authorization của ROOM-HOP.

### 14.7 Concurrent Update

Không dùng Last Writer Wins mặc định.

```
AI-01 ---+
AI-02 ---+--> Write Queue --> Conflict Manager --> Google Docs
AI-03 ---+
```

Khi read được revision R100, write giữ base_revision=R100. Operation nhạy cảm dùng Google Docs WriteControl.requiredRevisionId.

Nếu document đã R101:

```
REVISION_CONFLICT
 -> read current
 -> re-evaluate/replan
 -> retry nếu policy cho phép
```

Không blind overwrite.

targetRevisionId chỉ dùng khi operation đã chứng minh merge-safe, ví dụ một số append. Replace/semantic-sensitive update dùng requiredRevisionId.

### 14.8 Idempotency

Mỗi operation có idempotency_key. Retry sau timeout phải kiểm tra operation đã commit chưa để tránh duplicate append.

```
retry != duplicate
```

### 14.9 Versioning

Tách:

1. Google revisionId — concurrency control.
2. Work 05 operation sequence — audit identity.
3. schema_version — data-model compatibility.

Không dùng Google revisionId làm business version vĩnh viễn.

### 14.10 Sync

Pull:

```
AI/Core -> Document Service -> documents.get
```

Push/sync:

```
Google Drive change signal
 -> Sync Worker
 -> read change feed/current state
 -> Document Service
 -> ROOM-HOP event
```

Notification chỉ là tín hiệu có thay đổi, không phải canonical content. Cần reconciliation định kỳ.

### 14.11 Data Flow

AI → Google:

```
AI
 -> ROOM-HOP Core
 -> authorization
 -> Document Service
 -> registry
 -> idempotency
 -> revision read
 -> Write Queue
 -> Conflict Manager
 -> Google Docs Connector
 -> batchUpdate
 -> Audit Store
 -> Core
 -> AI
```

Google → AI:

```
Google Docs/Drive
 -> change/pull
 -> Sync Worker
 -> Document Service
 -> state/audit
 -> ROOM-HOP event
 -> AI
```

### 14.12 Error Handling

Chuẩn hóa AUTH_ERROR, FORBIDDEN, NOT_FOUND, RATE_LIMIT, TIMEOUT, NETWORK_ERROR, GOOGLE_API_ERROR, REVISION_CONFLICT, INVALID_OPERATION, DUPLICATE_OPERATION, SYNC_ERROR, INTERNAL_ERROR.

Retry có kiểm soát cho transient failures/rate limit/timeout; không retry mù với forbidden, invalid operation, not found hoặc revision conflict. Có exponential backoff + jitter và retry limit.

### 14.13 Logging / Security

Mỗi request có request_id, operation_id, work_id, document_id, actor_id.

Event: REQUEST_RECEIVED, AUTHORIZED, DOCUMENT_RESOLVED, REVISION_READ, WRITE_STARTED, WRITE_COMMITTED, WRITE_CONFLICT, RETRY, SYNC_STARTED, SYNC_COMPLETED, ERROR.

Không commit client secret, private key, refresh/access token vào Git. Production credential phải ở secure secret storage.

### 14.14 Connector Contract

Core chỉ biết interface:

```python
class DocumentConnector:
    def create_document(...)
    def get_document(...)
    def append(...)
    def update_section(...)
    def sync(...)
    def get_status(...)
```

GoogleDocsConnector implement interface. Có thể thay bằng Local/Notion/Microsoft Graph connector mà không đổi semantic Core.

### 14.15 Test / Evidence

Tối thiểu:

- T01 Authentication: valid/invalid/expired credential.
- T02 Create: Doc tồn tại + registry document_id.
- T03 Read: exact read-back.
- T04 Append: A/B tồn tại đúng.
- T05 Authorization: unauthorized actor bị reject.
- T06 Idempotency: cùng operation không duplicate.
- T07 Concurrent write: cùng base revision không silent overwrite.
- T08 External edit: stale revision gây conflict hoặc merge theo policy đã chứng minh.
- T09 Sync: human edit được phát hiện.
- T10 Recovery: timeout/retry không duplicate.

Evidence liên quan phải có operation_id, actor, base/result revision, Google result, final content và audit events.

Evidence ladder:

```
E0 Design
E1 Google API
E2 ROOM-HOP integration
E3 Concurrency
E4 Audit/recovery/sync
E5 Real multi-AI
```

### 14.16 MVP

MVP-01: OAuth + create/get/append + registry.  
MVP-02: WriteControl + revision conflict + idempotency.  
MVP-03: multi-AI + audit + queue.  
MVP-04: Drive changes/watch + sync + reconciliation.  
MVP-05: Shared Drive + production security + monitoring + recovery.

### 14.17 Rủi ro

Concurrent write; retry duplicate; credential leak; Google quota; human direct edit; revision history không đủ làm audit; service-account ownership/storage; Google ACL khác ROOM policy; missed/delayed notification; document size/performance; connector/API change.

### 14.18 DECISIONS cần Vinh/Xu chốt

- DEC-KA-01: Google Doc là canonical human-readable minutes hay mirror?
- DEC-KA-02: My Drive hay Shared Drive?
- DEC-KA-03: OAuth, Service Account hay hybrid?
- DEC-KA-04: Audit Store ở đâu?
- DEC-KA-05: Có single-writer queue theo document không?
- DEC-KA-06: requiredRevisionId hay targetRevisionId theo operation type?
- DEC-KA-07: AI chỉ append hay được update section?
- DEC-KA-08: Human có được edit trực tiếp Google Doc?
- DEC-KA-09: Human edit gây conflict thì policy nào?
- DEC-KA-10: Có local/offline mirror không?

### 14.19 Kết luận proposal

Ka đề xuất xem Work 05 là **Document Collaboration Boundary**, không đơn thuần là “Google Docs connector”, gồm:

```
Identity
Authorization
Document Persistence
Concurrent Collaboration
Evidence / Audit
```

Google Docs/Drive cung cấp document/collaboration/storage/ACL/change capabilities; ROOM-HOP vẫn giữ semantic authority.

Kiến trúc proposal:

```
ROOM-HOP
   -> Document Service
      -> Google Adapter
         -> Google Docs / Drive
```

**FINAL STATUS:** READY FOR ARCHITECTURE REVIEW  
**IMPLEMENTATION:** NOT STARTED  
**CREDENTIALS:** NOT USED  
**SEMANTIC CONTRACT:** NOT FINAL  
**RANKING:** NONE  
**NEXT:** Vinh/Xu tổng hợp proposal + evidence, sau đó mới chốt architecture và implementation.

## 15. LA DOLA — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

**Nguồn:** La Dola — nội dung proposal được Vinh cung cấp ngày 2026-09-29.
**Trạng thái:** RECEIVED / RECORDED / NOT FINAL. Đây là phương án độc lập để Xu/Vinh tổng hợp sau; không xếp hạng và không coi là kiến trúc cuối.

### 15.1 Tổng quan & mục tiêu
Xây dựng hệ thống trung gian quản lý Biên bản công việc trên Google Docs/Drive, cho phép nhiều AI cùng truy cập, đọc, ghi, cập nhật đồng bộ, an toàn và có theo dõi lịch sử.

Yêu cầu cốt lõi: tạo/quản lý tài liệu trên Google Docs; lưu trữ, đọc, ghi và cập nhật có kiểm soát; nhiều AI truy cập song song không mất dữ liệu; xác thực/phân quyền; xử lý cập nhật đồng thời; logging/versioning/error handling; triển khai và kiểm chứng.

### 15.2 Kiến trúc
AI/Agent → REST API/JSON → Backend trung gian → Google Docs API v1 + Google Drive API v3 → Google Workspace.
Backend phụ trách xác thực, phân quyền, đồng bộ, xử lý xung đột, log và lưu phiên bản. Auth dùng OAuth 2.0 hoặc Service Account. Google Docs dùng documents.get và batchUpdate; Drive dùng files.create, permissions, revisions.

### 15.3 Authentication / Authorization
La Dola đề xuất Service Account là chính, OAuth 2.0 Web là dự phòng nếu cần gắn hành động với người dùng thật.
Scopes được nêu: https://www.googleapis.com/auth/documents; https://www.googleapis.com/auth/drive.file; https://www.googleapis.com/auth/drive.metadata.readonly. Proposal không dùng drive toàn quyền.
Thiết lập gồm Google Cloud Project, bật Docs API/Drive API, tạo Service Account, đặt credential qua biến môi trường và chia sẻ thư mục gốc cho Service Account với quyền phù hợp.

### 15.4 Tạo & quản lý biên bản
Cấu trúc Drive đề xuất: WORK-05/GIAO_NHAN, WORK-05/MAU và LOG_HOAT_DONG.
Mẫu biên bản gồm mã, ngày, người tạo, trạng thái SOẠN/CHÍNH THỨC/KHOÁ, nội dung checklist và bảng thay đổi theo thời gian/AI/nội dung.
Luồng tạo: documents.create → nhận documentId → batchUpdate ghi nội dung ban đầu → Drive API đặt quyền.

### 15.5 Đọc / ghi / cập nhật
Đọc bằng documents.get, lấy body.content và revision metadata rồi chuẩn hóa text/Markdown cho AI.
Ghi/cập nhật bằng documents.batchUpdate với writeControl.requiredRevisionId. Nếu revision khớp thì commit; nếu không khớp thì conflict → tải lại → hợp nhất → thử lại có giới hạn.
Proposal nêu queue và rate limiting theo tài liệu. Hai AI ghi cùng vị trí sẽ bị conflict; nhiều AI đọc đồng thời không xung đột. Polling 5–10 giây hoặc Drive webhook được đề xuất để phát hiện thay đổi.

### 15.6 Data Flow
AI → Backend xác thực → kiểm tra quyền → lấy document + revisionId → chuyển yêu cầu AI thành Docs requests → batchUpdate + WriteControl → log + revision mới → thông báo AI khác tùy chọn.
Google → AI: documents.get → chuẩn hóa text/Markdown → thêm metadata phiên bản/thời gian sửa/người sửa cuối → trả AI.
Đồng bộ hai chiều dùng polling revisionId hoặc Drive webhook; backend có thể chủ động báo cho AI đang chờ sau khi ghi thành công.

### 15.7 Logging / Versioning / Error Handling
Hai lớp log/version: Google Drive revision history và system log gồm timestamp, ai_id, document_id, action, revision_before, revision_after, summary.
401: refresh token và retry giới hạn; 403: báo cấu hình/quyền, không retry; 404: kiểm tra document; 409: read/merge/retry tối đa 3 vòng; 429: chờ Retry-After rồi retry; 5xx: exponential backoff 1s → 2s → 4s.
Đảm bảo không mất dữ liệu bằng queue trước khi gọi API, không xóa log cũ, log bất biến cho từng cập nhật và đề xuất xuất bản sao cuối ngày.

### 15.8 Triển khai
Proposal nêu Node.js 20+ / Python 3.11+ / Go 1.22+, mức 1 vCPU/512 MB, mạng tới *.googleapis.com và các biến môi trường credential path, Work05 folder ID, MAX_RETRY, timeout, sync interval.
Giai đoạn: kết nối cơ bản → đọc/ghi → optimistic locking → multi-AI/phân quyền → đồng bộ/thông báo → monitoring/tối ưu.

### 15.9 API trung gian
POST /api/v1/docs/create — tạo biên bản.
GET /api/v1/docs/:id — đọc nội dung + metadata.
PATCH /api/v1/docs/:id — cập nhật có kiểm soát phiên bản.
GET /api/v1/docs/:id/history — lịch sử.
POST /api/v1/docs/:id/share — chia sẻ quyền.
GET /api/v1/docs/:id/wait — chờ thông báo thay đổi.

### 15.10 Kiểm thử / Evidence
T-01 tạo biên bản và xác nhận trên Drive; T-02 đọc và so sánh nội dung 100%; T-03 cập nhật tuần tự AI1 → AI2 → AI3; T-04 hai AI ghi cùng lúc và kiểm tra không mất dữ liệu; T-05 AI không có quyền ghi bị 403; T-06 mạng lỗi giữa chừng rồi phục hồi; T-07 xem/khôi phục lịch sử; T-08 nhiều request đọc đồng thời; T-09 vượt rate limit; T-10 kiểm tra log truy vết.

### 15.11 Rủi ro & điểm cần quyết định
Rủi ro: ghi đè nếu không kiểm soát revision; Google API quota; lộ Service Account key; không có realtime WebSocket trực tiếp từ Docs API; quá nhiều version; mất kết nối khiến request bị kẹt.
Đề xuất để Xu/Vinh xem xét: Service Account cho luồng AI tự động; log hệ thống và trong biên bản; một tài liệu/ngày; đồng bộ 5–10 giây; conflict cùng vị trí giữ cả hai và sắp xếp theo mã AI; người tổng hợp/Vinh có quyền khóa biên bản.

### 15.12 Kết luận proposal
La Dola xác định nền tảng là Google Docs API v1 + Drive API v3 với lớp trung gian kiểm soát. Trọng tâm là Service Account, optimistic locking bằng revisionId, backend queue, retry/error handling, log hai lớp và kiểm thử concurrent write.

**Implementation:** NOT STARTED.
**Credentials:** NOT USED.
**Architecture:** chưa chốt.
**Ranking:** NONE.
Semantics như merge conflict, revision history, ownership/storage của Service Account, scope quyền và mapping vào Core/MCP ROOM-HOP vẫn cần evidence kiểm chứng trước khi chốt kiến trúc.

## 16. QE / QWEN — PHƯƠNG ÁN TOÀN TRÌNH ĐỘC LẬP

**Nguồn:** Qe/Qwen — nội dung proposal được Vinh cung cấp ngày 2026-09-29.  
**Trạng thái:** RECEIVED / RECORDED / NOT FINAL. Đây là phương án độc lập để Xu/Vinh tổng hợp; không xếp hạng và không coi là kiến trúc cuối.

### 16.1 Tổng quan kiến trúc
Phương án đề xuất một **Connector Service (Middleware)** thay vì cho AI gọi trực tiếp Google API. Các thành phần:
- AI Agents: tạo yêu cầu Create/Read/Append.
- Message Queue (Redis/RabbitMQ): điều phối và xếp hàng yêu cầu ghi.
- Google Connector Service: Node.js/Python, gọi Google API, quản lý lock, retry và parse.
- Google Drive / Docs API: tầng lưu trữ vật lý.
- Shadow Database (PostgreSQL/MongoDB): metadata và bản sao JSON của biên bản để AI truy vấn nhanh.

### 16.2 Authentication & Authorization
Qe/Qwen đề xuất **Google Workspace Service Account + Shared Drive**, không dùng My Drive cá nhân.
- Service Account trên GCP; có thể dùng Domain-Wide Delegation nếu cần act on behalf of user, hoặc cấp quyền trực tiếp cho SA trên Shared Drive.
- Shared Drive đề xuất tên `AI_Knowledge_Base`; SA là Content Manager; AI/Human là Contributors.
- Scopes được đề xuất: `https://www.googleapis.com/auth/drive` và `https://www.googleapis.com/auth/documents`.
- Secret `credentials.json` phải nằm trong GCP Secret Manager / AWS Secrets Manager, không commit code.

### 16.3 Data Flow — Write/Append
Điểm Qe/Qwen xác định là khó nhất: Google Docs API không hỗ trợ CRDT; ghi đồng thời vào giữa văn bản có thể làm index lệch.
Chiến lược đề xuất: **Append-Only + Distributed Lock**:
1. AI gửi yêu cầu vào Queue.
2. Connector xin Redis Distributed Lock theo `document_id`.
3. Connector gọi `documents.get` lấy `endIndex`.
4. Connector gọi `documents.batchUpdate` với `insertText` tại `endIndex`.
5. Release Lock.

### 16.4 Data Flow — Read
1. AI yêu cầu đọc `doc_id`.
2. Connector kiểm tra Shadow DB; nếu cache chưa quá 5 phút thì trả về.
3. Nếu cần, gọi `documents.get`.
4. Parse `body.content` thành JSON chuẩn hóa.
5. Lưu Shadow DB và trả kết quả cho AI.

### 16.5 Create / Read / Update
**Create:** Drive `files.create` với mimeType Google Document, đặt parent là folder trong Shared Drive; sau đó Docs `batchUpdate` để chèn Header chuẩn từ Template JSON.

**Read:** Docs `documents.get`; parse `body.content`, `paragraph`, `textRun`; phân loại section theo `namedStyles` như Heading 1/Heading 2.

**Update:** Docs `batchUpdate` với `insertText` tại `END_INDEX`. Không dùng `updateParagraphStyle` hoặc chèn giữa văn bản trừ trường hợp đặc biệt và có lock chặt.

### 16.6 Logging / Versioning / Error Handling
Qe/Qwen đề xuất tận dụng **Drive API Revisions** và lưu `revision_id` mới nhất trong Shadow DB.
Structured JSON log gồm timestamp, agent_id, operation, doc_id, status, index_used, latency_ms.

Xử lý lỗi:
- 429: exponential backoff, giới hạn cứng proposal là tối đa 1 request/second/document.
- 400 Invalid Index: gọi lại `documents.get` lấy index mới và retry 1 lần.
- 403: alert Admin và pause queue.

### 16.7 Deployment
Connector Service đóng gói Docker.
Infrastructure: GKE/Kubernetes hoặc Cloud Run.
Monitoring: Prometheus/Grafana, theo dõi request Google API/phút, latency Docs API và lock timeout.

### 16.8 Test & Evidence
- Unit test parser với Docs có bảng, ảnh, heading lồng nhau.
- Integration concurrency: 5 AI agents đồng thời append 100 dòng vào cùng một Google Doc; kỳ vọng không mất dữ liệu, không Invalid Index; thứ tự theo Queue hoặc thời gian.
- Evidence: Queue history, Connector logs, nội dung cuối Google Doc.
- Load test: document 50 trang; nếu latency > 2 giây thì kích hoạt Shadow DB cache.

### 16.9 Reality Check / Risks
**Rủi ro 1 — Docs lớn/chậm:** Qe/Qwen cho rằng Docs API có thể chậm với file lớn; đề xuất Shadow DB và AI truy vấn DB, worker đồng bộ DB → Google Docs.

**Rủi ro 2 — Human sửa trực tiếp:** endIndex có thể thay đổi. Hai hướng:
- A: AI-Drafts riêng, sau đó Apps Script/Connector merge vào Final_Minutes.
- B: chấp nhận rủi ro, Redis lock ngắn hạn và fetch lại endIndex ngay trước insert.

**Rủi ro 3 — Rate limit:** nhiều AI đồng thời có thể gặp 429; đề xuất batching các yêu cầu ghi trong khoảng 1 giây thành một `batchUpdate` chứa nhiều `insertText`.

### 16.10 Điểm cần Vinh/Xu quyết định
1. **Mô hình lưu trữ:**
   - Option 1: Google Docs là Master/Source of Truth; Shadow DB là cache.
   - Option 2: Database là Master; Google Docs là View/Export.
   - Qe/Qwen **đề xuất Option 2 — DB-as-Master, Docs-as-View** vì AI cần dữ liệu có cấu trúc; Docs phù hợp báo cáo cho Human.
2. Có cần Shared Drive riêng cho từng Project/Department để tách quyền hay không?

### 16.11 Kết luận proposal
Qe/Qwen tập trung giải bài toán **Concurrency và Data Integrity** bằng **Distributed Lock + Append-Only**, đồng thời đề xuất DB-as-Master và Google Docs-as-View để tối ưu truy vấn AI và giảm phụ thuộc vào hiệu năng Docs API.

**Implementation:** NOT STARTED.  
**Credentials:** NOT USED.  
**Architecture:** chưa chốt.  
**Ranking:** NONE.  
**Điểm cần evidence:** hiệu năng thực tế, semantics của endIndex/Invalid Index trong các kịch bản concurrent, tính phù hợp của Drive Revisions cho versioning/audit, và tác động của human direct edit cần được kiểm chứng trước khi chốt.
