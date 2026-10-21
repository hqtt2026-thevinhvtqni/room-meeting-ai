# Work AI Dashboard Model v1.0
## Mô hình dashboard theo dõi từng Work theo vai trò AI

- Work sở hữu chuẩn: Work 50 — APDS
- Trạng thái: PROPOSED — chờ Vinh duyệt
- Phiên bản: 1.0
- Điều phối: Xu (AI-01)
- Ngày: 2026-10-21 (UTC+07:00)

## 1. Mục tiêu

Mỗi Work có một dashboard riêng, dùng cùng một mô hình dữ liệu và cách hiển thị. Dashboard cho phép Vinh nhìn nhanh: Work đang ở đâu, AI nào chịu trách nhiệm từng phần, đầu ra nào đã có, việc gì bị chặn, ai nghiệm thu và bằng chứng nằm ở đâu.

Dashboard là lớp quan sát/điều phối; không phải nguồn tự tạo sự thật. Nó không được tự chuyển DONE thành PASS, không suy ra PASS từ câu báo cáo, tên tệp hoặc commit đơn lẻ.

## 2. Mô hình ba lớp

1. **HQTT Role Catalog:** danh mục vai trò chuẩn tại `AI_ROLE_CATALOG_v1.0.md`; mỗi Role ID có định nghĩa và phiên bản.
2. **Work Manifest & Assignment:** mỗi Work lưu mục tiêu, phạm vi, deliverables, milestone, dependencies và ma trận AI được phân công.
3. **Dashboard View:** render dữ liệu manifest, nhật ký, trạng thái và evidence; không tự sửa nguồn dữ liệu chỉ vì người dùng đổi bộ lọc/hiển thị.

## 3. Bố cục dashboard

### A. Work Header
- Work ID / tên / owner / branch / trạng thái tổng thể.
- Mục tiêu và phạm vi hiện tại.
- Nguồn dữ liệu được đọc: Sandbox, GitHub hoặc cả hai.
- Thời điểm cập nhật gần nhất và commit/revision đã đọc.
- Đồng bộ: SYNCED / DRIFT / CONFLICT / MCP_UNAVAILABLE / UNKNOWN.

### B. Summary Cards
- Deliverables tổng số / DONE / PASS / BLOCKED / UNVERIFIED.
- Milestone hoàn thành / tổng milestone.
- Việc quá hạn (chỉ nếu có deadline rõ ràng).
- Lỗi mở và rủi ro cao.
- Bằng chứng thiếu hoặc chưa xác minh.

### C. AI Role Board
Mỗi thẻ vai trò hiển thị:
- Role ID + tên vai trò.
- AI ID, tên và provider (nếu đã xác thực); nếu chưa thì NOT_ASSIGNED.
- Trách nhiệm / task được giao.
- Deliverables và tiêu chí nghiệm thu.
- Trạng thái, blockers, dependencies.
- Reviewer/approver được chỉ định.
- Last update, evidence links, revision/commit.
- Nút/đường dẫn xem nhật ký và hồ sơ nhiệm vụ.

### D. Work Pipeline
Hiển thị luồng theo giai đoạn phù hợp: INTAKE → PLAN → ARCHITECTURE → BUILD → TEST → SECURITY/COMPLIANCE → RELEASE → HANDOFF. Work có thể bỏ qua giai đoạn chỉ khi ghi N/A và lý do; các giai đoạn phụ thuộc phải được thể hiện.

### E. Evidence & Decision Log
- Evidence ID, loại bằng chứng, đường dẫn, commit/revision, thời gian, người/AI tạo, reviewer và kết luận.
- Decision ID, nội dung quyết định, người có thẩm quyền, thời điểm và phạm vi hiệu lực.
- Không hiển thị bí mật, token hoặc dữ liệu nhạy cảm không cần thiết.

### F. Sync & Health
- Tình trạng kết nối từng nguồn độc lập.
- Revision/hash cuối cùng đã đọc ở mỗi nguồn.
- Số tệp khác biệt và xung đột.
- Hành động đồng bộ chỉ thực hiện qua workflow được cấp quyền, có diff/preview và log; không tự ghi đè.

## 4. Bộ lọc và drill-down

Bộ lọc: vai trò, AI/provider, giai đoạn, trạng thái, milestone, mức rủi ro, blocker, nguồn dữ liệu. Chọn một thẻ mở hồ sơ nhiệm vụ/đầu ra/bằng chứng tương ứng. Bộ lọc chỉ đổi cách xem, không đổi trạng thái dữ liệu.

## 5. Hợp đồng dữ liệu tối thiểu

### Work
- work_id, name, owner, objective, scope, status, branch
- manifest_revision, source_of_truth_policy, updated_at
- source_health[], sync_status, sync_checked_at

### Assignment
- assignment_id, work_id, role_id, role_catalog_version
- ai_id, provider, assignee, task_ids[], deliverable_ids[]
- reviewer_id, approver_id, authority_scope
- status, blocker_ids[], dependency_ids[]
- updated_at, evidence_ids[], source_revision

### Deliverable
- deliverable_id, title, owner_assignment_id, acceptance_criteria[]
- status, reviewer, evidence_ids[], due_at (optional), revision

### Evidence
- evidence_id, kind, uri_or_path, source, source_revision, content_hash (if available)
- created_by, created_at, reviewed_by, verification_status, notes

### Decision
- decision_id, question, decision, authority, decided_at, scope, evidence_ids

### SyncRecord
- sync_id, source_a, source_b, revisions_before, diff_summary
- conflicts[], approved_by, actions[], verification_after, status, timestamp

## 6. Trạng thái chuẩn

- NOT_ASSIGNED: chưa có người/AI nhận.
- PLANNED: đã phân công, chưa bắt đầu.
- IN_PROGRESS: đang làm.
- BLOCKED: phụ thuộc hoặc điều kiện ngăn tiến độ.
- DONE: đầu ra đã tạo, chưa mặc định nghiệm thu.
- PASS: tiêu chí cụ thể đã kiểm tra và có bằng chứng đạt.
- FAIL: kiểm tra không đạt.
- UNVERIFIED: chưa đủ bằng chứng.
- NOT_APPLICABLE: không áp dụng, có lý do.

Trạng thái đồng bộ riêng: SYNCED, DRIFT, CONFLICT, SOURCE_UNAVAILABLE, UNKNOWN. Không gộp trạng thái đồng bộ vào trạng thái công việc.

## 7. Quy tắc tính tổng quan

- Tổng tiến độ không được lấy trung bình đơn giản trạng thái của các AI.
- Mỗi Work phải xác định deliverables/milestones và trọng số nếu cần tính %; nêu công thức và không tự bịa trọng số.
- Nếu chưa có baseline hoặc dữ liệu đủ, hiển thị UNKNOWN thay vì % giả.
- DONE và PASS là hai trạng thái khác nhau.
- Blocker ở đường găng phải được làm nổi bật; không che bằng điểm tổng quan cao.
- Mọi con số tổng hợp phải drill-down được về các bản ghi nguồn.

## 8. Quyền hạn và an toàn

- Dashboard mặc định read-only.
- Mọi thay đổi phân công/trạng thái nguồn phải qua workflow có quyền, người thực hiện, timestamp và audit log.
- Chỉ người có thẩm quyền mới phê duyệt scope, go/no-go, ngoại lệ bảo mật hoặc release.
- AI không tự cấp thêm quyền, tự duyệt kết quả do mình tạo hoặc sửa bằng chứng để đổi trạng thái.
- Che thông tin bí mật; dùng least privilege (quyền tối thiểu cần thiết).

## 9. Quy tắc GitHub-first khi MCP lỗi

- Nếu MCP không khả dụng nhưng GitHub hoạt động, tiếp tục thay đổi tài liệu trên branch Work; ghi commit, thời điểm, phạm vi bị ảnh hưởng và thao tác còn chờ.
- Dashboard phải hiển thị MCP_UNAVAILABLE riêng; không được suy luận Sandbox offline nếu chưa kiểm tra trực tiếp.
- Khi phục hồi: đọc revision hai phía, tạo diff, phân loại xung đột, yêu cầu phê duyệt khi cần, đồng bộ và đọc lại cả hai phía.
- Không ghi đè hoặc tuyên bố SYNCED nếu thiếu bằng chứng sau đồng bộ.

## 10. Acceptance criteria cho dashboard

1. Mỗi Work có dashboard riêng từ manifest chung.
2. Hiển thị đúng Role ID, AI assignment và trạng thái NOT_ASSIGNED khi thiếu phân công.
3. Có drill-down từ tổng quan → vai trò → nhiệm vụ → deliverable → evidence.
4. Phân biệt DONE/PASS/BLOCKED/UNVERIFIED.
5. Không tạo % tiến độ khi thiếu baseline/công thức.
6. Hiển thị tình trạng nguồn và sync độc lập cho GitHub/Sandbox/MCP.
7. Thay đổi dữ liệu nguồn có audit log; chế độ xem mặc định read-only.
8. Xung đột không tự giải quyết bằng ghi đè.
9. Mỗi tuyên bố PASS liên kết được tiêu chí, kết quả kiểm tra và evidence.
10. Dashboard phản ánh đúng revision/commit mà nó đọc.

## 11. Lộ trình xây dựng

- Phase 1 — Contract: chốt role catalog, Work manifest, assignment/evidence/sync schema.
- Phase 2 — Read-only MVP: một dashboard mẫu cho Work 50, đọc GitHub; hiển thị rõ nguồn và revision.
- Phase 3 — Multi-Work: tái sử dụng cùng component/schema cho các Work khác.
- Phase 4 — Dual-source: thêm Sandbox khi MCP phục hồi; chỉ đọc/so sánh trước.
- Phase 5 — Controlled sync: workflow đồng bộ có diff, conflict handling, approval và verification.
- Phase 6 — E2E acceptance: kiểm tra nguồn dữ liệu thật, quyền hạn, audit log, lỗi kết nối và recovery.

## 12. Giới hạn triển khai hiện tại

Tài liệu mô tả mô hình chuẩn, không tuyên bố đã có dashboard chạy thật. Chưa tạo giao diện ứng dụng, API hoặc runtime trong commit này. Cần review cấu trúc dashboard đang có trước khi quyết định mở rộng hay tái sử dụng.

## 13. Nhật ký

- 2026-10-21 (UTC+07:00) — Xu (AI-01), điều phối Work 50: tạo mô hình dashboard theo từng Work, gắn danh mục vai trò AI, evidence và quy trình GitHub-first/MCP recovery. Trạng thái PROPOSED.
