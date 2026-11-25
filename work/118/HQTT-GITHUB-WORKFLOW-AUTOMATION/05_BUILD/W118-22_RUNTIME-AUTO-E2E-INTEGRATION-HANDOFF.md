# W118-22 — HỒ SƠ ĐIỀU PHỐI TÍCH HỢP RUNTIME AUTO E2E
**Mã tài liệu:** W118-22  
**Phiên bản:** 1.1 — DRAFT / OWNER HANDOFF + SOURCE RECONCILIATION  
**Ngày:** 2026-11-26  
**Phạm vi:** W118, nhánh `work/118-auto-e2e-v2-clean`  
**Mục tiêu:** Chuyển W118 từ kiểm tra contract tĩnh sang tích hợp có thẩm quyền và kiểm chứng một luồng Runtime Auto E2E thực.

## 1. Quyết định điều phối
W118 không tiếp tục mở rộng validator hoặc tăng số lượng unit test để thay thế tiến độ tích hợp. Công việc kế tiếp là nhận các hợp đồng giao tiếp đã được chủ sở hữu phê duyệt, nối đúng adapter tại ranh giới Work, sau đó chạy một luồng thật có cùng correlation ID xuyên suốt năm chặng.

W118 là bên điều phối và tích hợp. W118 **không sở hữu** API, schema, quyền Core, chính sách cấp grant, runtime host, ingestion hoặc Evidence Registry của các Work khác. Không tự suy diễn endpoint, payload, token, principal hay trạng thái phê duyệt.

## 2. Luồng đích và điều kiện chứng minh

| Thứ tự | Chặng | Chủ sở hữu | Bằng chứng tối thiểu cần đọc/nhận | Trạng thái hiện tại |
|---|---|---|---|---|
| 1 | Core tạo Task/Execution Grant có thẩm quyền | Core / W01 / W02 / W22 theo phân quyền hiện hành | Contract V1.2 đã duyệt; Task snapshot; actor/principal đã xác thực; grant ID, phạm vi Work/source, hạn dùng, audience và cách xác minh | BLOCKED — chưa có contract/receipt được xác minh |
| 2 | W102 nhận Assignment và ACK đúng recipient | W102 + Core | Assignment ID gắn Task; recipient/AI identity đã xác thực; ACK receipt; correlation ID; trạng thái authoritative từ Core | BLOCKED — chưa chứng minh Assignment/ACK live |
| 3 | W14 thực thi dưới Core Authority | W14 | Contract grant validation; Work/source binding từ nguồn tin cậy; execution ID; kết quả và provenance; từ chối request không có grant hợp lệ | BLOCKED — source trace cho thấy request context có trường authorized do caller gửi; chưa thấy xác minh grant Core trong đường thực thi đã khảo sát |
| 4 | W33 tiếp nhận evidence đã xác thực | W33 | Ingestion interface/CLI/API được chủ sở hữu xác nhận; receipt ID; digest; correlation ID; xác minh nguồn gửi và idempotency | BLOCKED — production ingress chưa được xác minh |
| 5 | W70 đọc lại Evidence Registry chuẩn | W70 | Schema/version được duyệt; cách ghi/đọc chuẩn; evidence record ID; read-back khớp digest, nguồn, Task và correlation ID | BLOCKED — schema/owner contract chưa được xác minh |

**Định nghĩa E2E PASS:** một lần chạy mới, không dùng fixture/fake/mock, có cùng correlation ID; mỗi chặng có receipt gắn với chặng trước; Core authority được xác minh; W14 từ chối khi grant không hợp lệ; W33 có ingestion receipt; W70 trả về record đã lưu với digest và provenance khớp. CI xanh hoặc verifier tĩnh không thay thế tiêu chí này.

## 3. Phân định việc W118 tự làm và việc phải chờ chủ sở hữu

### 3.1 W118 tự chịu trách nhiệm
- Giữ correlation ID xuyên suốt các adapter và log.
- Chuyển đổi dữ liệu chỉ theo schema/contract đã duyệt; giữ nguyên source revision và digest.
- Lưu receipt bất biến, chống ghi đè; phát hiện thiếu chặng, sai thứ tự, sai nguồn hoặc sai digest.
- Bổ sung adapter và kiểm thử contract sau khi có fixture chính thức do owner cung cấp.
- Chạy E2E trên runtime được cấp quyền; lưu command, thời gian, môi trường, run ID, receipt và kết quả vào nhật ký.
- Tách rõ CI contract, static validation, sandbox simulation và live runtime evidence.

### 3.2 Không được tự làm thay owner
- Không tạo hoặc giả lập Core Task, Assignment, authenticated principal hay Execution Grant.
- Không tự cấp quyền, tạo token/secret, đổi permission, branch protection hoặc cấu hình production ingress.
- Không coi `authorized: true`, identity header, role-map, fixture hoặc membership là bằng chứng Core authorization.
- Không sửa hợp đồng W14/W33/W70 theo phỏng đoán.
- Không gọi endpoint thực thi hoặc gửi payload mutation khi chưa có contract được duyệt, principal hợp lệ và runtime target được xác minh.
- Không đánh dấu PASS chỉ vì unit tests/CI hoặc chữ ký envelope hợp lệ.

## 4. Phiếu yêu cầu đầu vào theo chủ sở hữu

### A. Core / W01 / W02 / W22 — Core Authority contract
**Cần bàn giao:**
1. Tên và phiên bản tài liệu/schema V1.2 chính thức; trạng thái APPROVED và người phê duyệt.
2. Contract chính xác để đọc Task snapshot và yêu cầu/kiểm tra Execution Grant; endpoint/transport chỉ ghi theo tài liệu được duyệt.
3. Cách xác thực principal; issuer/audience; claim/permission; thời hạn; thu hồi; ràng buộc Work ID, Task ID, repository, source SHA và operation.
4. Receipt hoặc response mẫu đã loại bỏ secret, kèm negative case: thiếu grant, hết hạn, sai Work, sai SHA, sai audience, revoked.
5. Cách kiểm tra lease/fencing/idempotency nếu Core yêu cầu.

**Không chấp nhận thay thế:** header danh tính tự khai, token giả, boolean authorized, fixture hoặc contract PROPOSED.

### B. W102 — Assignment / ACK
**Cần bàn giao:**
1. API/adapter contract chính thức cho Task → Assignment → recipient ACK.
2. Nguồn xác thực recipient và quy tắc ánh xạ AI ID ↔ principal đã được Core công nhận.
3. Assignment ID, ACK receipt schema, trạng thái authoritative, idempotency key và cách truy vấn read-back.
4. Một mẫu success và các mẫu reject/duplicate/expired đã loại bỏ thông tin nhạy cảm.

**Điều kiện tích hợp:** W118 chỉ gửi/đọc qua adapter được owner chỉ định; không tự tạo Assignment bằng GitHub Issue/comment.

### C. W14 — Protected Execution Host
**Cần bàn giao:**
1. Commit/source revision và phiên bản runtime host được xác nhận là baseline.
2. Contract thực thi chính thức và cách W14 xác minh Core-issued grant ở server side.
3. Cách W14 tự lấy WorkContext/root/source snapshot tin cậy; không nhận root hoặc quyền do caller tự khai.
4. Bằng chứng test từ chối request không grant, grant sai Work/SHA, grant hết hạn/thu hồi.
5. Runtime target, phương thức khởi động/health check, người vận hành và điều kiện PC access nếu cần.

**Finding cần owner xử lý:** source đã khảo sát cho thấy POST /execute dựng WorkContext từ JSON body và kiểm tra boolean authorized cùng workspace containment; chưa thấy Core grant validation. Đây là finding source-level, chưa phải kết luận exploit runtime. W14 owner cần xác nhận/fix trước khi W118 gửi lệnh thực thi.

### D. W33 — Authenticated Evidence Ingestion
**Cần bàn giao:**
1. Interface chính thức (CLI/API/library), phiên bản và lệnh mẫu an toàn.
2. Cơ chế xác thực caller và quyền ghi theo Work/Task.
3. Receipt schema gồm tối thiểu receipt ID, correlation ID, source identity/revision, digest, timestamp, outcome.
4. Quy tắc content-addressed storage, idempotency, duplicate và cách đọc lại receipt.
5. Runtime/host requirements; nếu là CLI cục bộ thì chỉ rõ binary/environment và đường dẫn dữ liệu được phép.

**Không suy diễn:** việc W33 có blob store + SQLite catalog không tự chứng minh có production HTTP ingress hoặc endpoint dùng được từ W118.

### E. W70 — Evidence Registry
**Cần bàn giao:**
1. Tên schema và version hiện hành đã APPROVED; người/đơn vị sở hữu.
2. Contract append/read-back chính thức; nguồn dữ liệu chuẩn và quyền ghi/đọc.
3. Mapping receipt W33 sang Evidence Registry record; correlation, Work/Task, source SHA, digest, provenance.
4. Quy tắc append-only, deduplication, verification status và cách truy vấn record.
5. Một record mẫu đã loại bỏ dữ liệu nhạy cảm và kết quả read-back.

**Không chấp nhận thay thế:** DOC-093 hoặc schema đang DRAFT/PROPOSED, file projection/dashboard, hoặc một bản JSON tự tạo trong W118.

## 5. Ma trận trạng thái và tiêu chí đóng blocker

| Blocker | Phân loại | Chủ sở hữu hành động | Điều kiện chuyển trạng thái |
|---|---|---|---|
| Core contract + principal + grant | EXTERNAL OWNER BLOCKER | Core/W01/W02/W22 | Nhận contract APPROVED + mẫu receipt/negative cases + verifier trust model |
| W102 Assignment/ACK | EXTERNAL OWNER BLOCKER | W102/Core | Nhận contract APPROVED + authenticated recipient + ACK read-back |
| W14 grant enforcement | EXTERNAL OWNER BLOCKER | W14/Core | Owner xác nhận implementation; negative tests chứng minh reject; runtime host attested |
| W33 authenticated ingress | EXTERNAL OWNER BLOCKER | W33 | Nhận interface chính thức + auth + ingestion receipt/read-back |
| W70 Registry contract | EXTERNAL OWNER BLOCKER | W70 | Nhận schema APPROVED + append/read-back contract |
| W118 adapter mapping | W118 OWNED — WAITING INPUT | W118 | Chỉ triển khai sau khi có contract/fixtures owner-approved |
| PC/runtime availability | ENVIRONMENT BLOCKER | Runtime/PC operator | Host attestation, process/port/health evidence và quyền vận hành được xác minh |
| Full E2E correlation | INTEGRATION GATE | W118 + tất cả owners | Một run thật qua đủ 5 chặng, receipt liên kết và read-back khớp |

## 6. Thứ tự triển khai sau khi nhận đủ đầu vào
1. **Contract intake:** lưu nguyên văn schema/contract đã duyệt, version, commit/source và người phê duyệt; chạy schema conformance offline.
2. **Security boundary:** W14 owner chứng minh server-side grant validation và trusted WorkContext; không gửi execute request trước bước này.
3. **Assignment path:** nối Core Task → W102 Assignment/ACK; xác minh read-back từ Core.
4. **Execution path:** nối W14 bằng grant hợp lệ, source snapshot pinning và execution receipt.
5. **Evidence path:** nối W33 ingestion và nhận receipt đã xác thực.
6. **Registry path:** append/read-back từ W70 theo schema chuẩn.
7. **E2E:** chạy một correlation ID end-to-end; sau đó chạy negative tests riêng; lưu mọi evidence vào journal.
8. **Handoff:** báo cáo DONE/PASS/BLOCKED theo từng gate; không suy rộng kết quả một chặng thành PASS toàn luồng.

## 7. Ranh giới môi trường
- Build MCP/Sandbox 8030 hiện được dùng để quản lý/đọc/ghi hồ sơ; không coi đây là process execution host.
- Không dùng Meeting MCP 8020.
- W14 Execution Host :8031 là runtime target đã được kiến trúc xác định, nhưng trạng thái listener/live health phải được kiểm chứng tại môi trường thực; không tuyên bố đang chạy khi chưa có bằng chứng.
- Không tự chuyển W12/W13 thành một execution host mới; W14 là owner execution path theo kiến trúc đã truy vết.
- Nếu bước nào cần PC, phải ghi rõ command, expected output và evidence cần thu; chỉ báo anh Vinh khi thực sự cần thao tác trên PC.

## 8. Kết luận hiện tại
**W118-22 = CREATED / DRAFT / OWNER HANDOFF READY.**  
**Runtime Auto E2E = BLOCKED / NOT RUN.**  
Đây là hồ sơ điều phối yêu cầu hợp đồng và bằng chứng từ owner, không phải contract mới, không phải approval, không phải runtime pass và không thay đổi quyền của bất kỳ Work nào.

**Người điều phối:** Xu / AI-01 — theo ủy quyền của Vinh.  
**Giới hạn:** không merge, không release, không thay đổi quyền/secrets, không mutation runtime trong bước lập hồ sơ này.


## 9. Fresh source reconciliation — 2026-11-26 (UTC+07)

### 9.1 Core Execution Authority V1.2 — approved scope, candidate implementation, not deployed
- **Owner decision:** W1111 `APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md` on branch `work/w1111-core-execution-authority-v1-2`, blob `2ae990bfab4c1e2dcb2782cd79f332fdae655742`, reconciles Vinh's prior 2026-10-25 approval of DR-1..DR-4: enrolled service identity, short-lived grant, Core append-only durable store, and additive mount within Core. Gate 1 is recorded APPROVED; Gate 2 OPEN/AUTHORIZED. Gates 3–5 remain NOT OPEN. This is an existing owner decision; W118 must not ask Vinh to approve DR-1..DR-4 again.
- **Candidate PR:** [PR #48](https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/48), `feat(core): implement Work-scoped Execution Authority V1.2`, remains OPEN / DRAFT / UNMERGED; GitHub metadata reports mergeable=false. Current compare at this audit: main...branch `work/w1111-core-execution-authority-v1-2` = DIVERGED, 157 ahead / 999 behind, merge base `82a490ad16c72e77ca3c9c8d9f83feabcb6f4e54`. Do not merge, rebase, cherry-pick or deploy from this branch under W118 authority.
- **Branch source evidence:** `room_hop_mcp/adapter/http_server.py` blob `48e05c0f5d8121e35ba9bea01ebd8f338529073c` imports `ExecutionAuthority`, loads configuration fail-closed and mounts the five execution-grant routes through `mount_execution_authority_routes`. `room_hop_mcp/adapter/execution_authority_http.py` blob `8cb21fadf6bf2318f4884d368b77f2abf796b807` defines issue/status/validate/run/revoke routes. `core/execution_authority.py` blob `163b126178b67c6e0a3f68ba33eaf7b9e6d91503` contains credential digest registry, Work policy and append-only hash-chain store. `execution_host/server.py` blob `dd65fcfacfc171e673000ecbeba01d5842a42e8c` validates bearer grant online, checks purpose, timeout and source snapshot, and records run via Core. These are branch source observations only.
- **Important composition correction:** the branch's `core_http_main.py` delegates to `create_http_app`; the actual additive route mount is in the branch's `http_server.py`. Main currently lacks the corresponding authority adapter/mount in the inspected entrypoint/router. Do not describe V1.2 as available on main or on the live Core :8000.
- **CI claim scope:** PR description records 33 passing tests and exact branch CI run `42732254869` on branch revision `9bbeed63dfbdcc6a00b8bdb31c3db1b00b812197`. This is historical branch CI evidence as recorded in the PR description; this audit did not rerun it and it does not prove current main, PC deployment or live Core/Host runtime.
- **W118 disposition:** REUSE CANDIDATE / NOT INTEGRATED. The candidate does not establish W102 Assignment/recipient-authenticated ACK binding, W33 ingestion, W70 Evidence Registry read-back or a deployed W14 runtime. Any reuse must follow W14 ownership and W1111's existing gate/branch controls.

### 9.2 W14 — protected execution ownership and adoption
- W118 current STATUS defines W14 as the sole product/delivery owner for integrated Work Authority, ExecutionHostBridge, GitHub Gateway and CI path; W12/W13 are absorbed internal foundations, not independent W118 owners.
- PR #48 contains Core/Host/W12/W13 implementation candidates, but no evidence in this readback establishes that W14 has adopted the exact branch/source revision as its canonical current build, or that its runtime is deployed.
- **Disposition:** W14 ADOPTION / SOURCE-LINEAGE / RUNTIME ATTESTATION REQUIRED. W118 will not fork or duplicate Execution Host.

### 9.3 W102 — Assignment and authenticated ACK
- W17 current source reconciliation records W70 Assignment templates and W112 cross-Work contract as draft references only; authoritative Assignment API/service, durable state, recipient-authenticated ACK ingestion/verifier, transaction/audit/read-back and runtime remain NOT VERIFIED.
- W112 DOC-001 remains DRAFT / NOT APPROVED FOR RUNTIME ENFORCEMENT. W70 DOC-044 is an assignment template, not a runtime Assignment API.
- **Disposition:** BLOCKED — no verified Core Task → W102 Assignment → recipient-bound ACK round-trip. No GitHub Issue or self-reported ACK may substitute.

### 9.4 W33 — authenticated evidence ingestion
- W17 current branch/source reconciliation records branch `work/33/ROOM-SHARED-FILE-EVIDENCE-HUB` as DIVERGED (16 ahead / 1503 behind at its recorded check), documentation-only delta; expected source paths `03_ARCHITECT/ARCHITECTURE.md` and `04_CODE/src/rsfeh/{store.py,cli.py}` were NOT_FOUND in that branch readback.
- The available W117/W17 audit describes W33 as local SHA-256 blob + SQLite catalog and CLI-first, with caller-supplied agent attribution rather than authentication; no HTTP ingress or Core/MCP authenticated write path is verified. Historical W33 17/17 and A1–A9/A11 PASS claims remain NOT VERIFIED in the latest W17 reconciliation; A10 Core/MCP integration remains BLOCKED.
- **Disposition:** BLOCKED — no canonical, current, authenticated ingestion interface and receipt contract available to W118. Do not reconstruct W33 source or invoke an assumed CLI/API under W118.

### 9.5 W70 — authoritative Evidence Registry
- W70 DOC-061 (main blob `a54dc2202e56cfb9737395fd523a5488ab35b0f3`) is DRAFT / contract approval pending / implementation not verified; it explicitly treats Core Work/Evidence APIs as proposals until an owner-approved runtime contract exists.
- W70 DOC-071 (main blob `12f11320dc9da89b27de21313b698224d74519ce`) is source trace complete but states Core owner NOT IDENTIFIED, Work/WP/Assignment persistence and Work Evidence Registry NOT FOUND IN INSPECTED SCOPE / NOT VERIFIED.
- W70 DOC-093/DOC-094 are draft/proposal task registers, not an approved Evidence Registry API/schema. Dashboard projection is read-only and cannot replace canonical persistence.
- **Disposition:** BLOCKED — no owner-approved schema plus append/read-back route or service contract verified.

### 9.6 Consolidated decision and next executable path
1. Preserve PR #48 as an upstream candidate; do not import its large divergent history into W118.
2. Obtain W14 owner confirmation of the canonical source/revision that adopts Core grant validation, and a deployment attestation for :8031. This is not a request to re-approve DR-1..DR-4.
3. Resolve the current Core runtime integration path: the approved V1.2 implementation exists on PR #48, but main's inspected route mount is absent and live :8000 is not verified. W118 cannot bypass this by calling a speculative route.
4. Obtain the W102 Assignment/ACK contract and W33 authenticated ingestion receipt interface from their canonical owners; W118 adapters remain read-only/contract-only until then.
5. Obtain W70 approved Evidence Registry schema and read-after-write contract; do not use draft task registers or Dashboard projections as a substitute.
6. Only after 2–5 are evidenced, run one non-sensitive, task-scoped E2E with one correlation ID and preserve all receipts.

**Updated gate matrix:** Core V1.2 design/DR-1..DR-4 APPROVED; branch implementation candidate PRESENT; main route mount NOT PRESENT IN INSPECTED SOURCE; live Core NOT VERIFIED. W102 Assignment/ACK BLOCKED. W14 adoption/runtime NOT VERIFIED. W33 authenticated ingestion BLOCKED. W70 Evidence Registry read-back BLOCKED. Full Runtime Auto E2E BLOCKED / NOT RUN.

**No owner-level question to Vinh is raised at this point:** prior V1.2 approval is already recorded. The next dependencies are technical owner handoffs and exact runtime/source evidence, not a new DR-1..DR-4 decision.
