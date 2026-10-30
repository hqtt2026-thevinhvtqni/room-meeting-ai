# QUY TRÌNH LẬP KẾ HOẠCH / PLAN PROCESS
- **STT / Document ID:** DOC-045
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 45
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-008; DOC-009; DOC-011; DOC-012; DOC-033; DOC-038; DOC-044
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-045 quy định cách thực hiện 04_PLAN (Lập kế hoạch): chuyển requirements và architecture baseline đã được G2/G3 chấp thuận thành kế hoạch thực thi có thể giao việc, theo dõi, kiểm soát thay đổi và kiểm chứng.

PLAN trả lời: cần tạo những kết quả nào, theo Work Package (WP — gói công việc) nào, thứ tự/phụ thuộc ra sao, ai chịu trách nhiệm, reviewer nào độc lập, nguồn lực/ước lượng nào có căn cứ, milestone và tiêu chí hoàn thành là gì, rủi ro nào có thể ảnh hưởng và khi nào được phép bắt đầu BUILD.

PLAN không thay đổi product requirements hoặc architecture baseline. Nếu phát hiện cần thay đổi outcome/scope/acceptance, quay lại DEFINE; nếu thay đổi HOW/architecture, mở ADR/ACR theo DOC-044. Không dùng kế hoạch để hợp thức hóa quyết định chưa được phê duyệt.

04_PLAN là nơi duy nhất sở hữu kế hoạch WP cấp Work. 05_BUILD chỉ ánh xạ WP sang vùng kỹ thuật, artifact nguồn chuẩn và bằng chứng thực thi; không tạo một kế hoạch WP độc lập cạnh tranh với 04_PLAN.

## 2. Điều kiện đầu vào

### 2.1 Entry criteria
- G2 DEFINE → ARCHITECT đã PASS.
- G3 ARCHITECT → PLAN đã PASS.
- DOC-008 approved requirements baseline và DOC-009/architecture baseline version được xác định.
- Có architecture handoff, contracts, verification expectations, risks, dependencies, assumptions và known limitations.
- Các quyết định còn mở có owner, due/trigger và ảnh hưởng tới kế hoạch được đánh dấu.
- Product Owner xác nhận mục tiêu, giới hạn và các trade-off lập kế hoạch trọng yếu.

Nếu G2/G3 chưa PASS, chỉ lập draft/scenario để chuẩn bị; không phát hành execution baseline và không mở BUILD chính thức.

### 2.2 Nguyên tắc
1. **Outcome-led:** WP phải tạo ra outcome/deliverable truy được về requirement và architecture.
2. **Single source:** WP cấp Work chỉ được quản lý tại 04_PLAN; 05_BUILD là mapping/execution.
3. **Small and verifiable:** WP đủ nhỏ để có owner, reviewer, dependency, output và điều kiện đóng rõ.
4. **Evidence-based estimates:** estimate nêu giả định, dữ liệu tham chiếu, range/confidence; không tạo độ chính xác giả.
5. **Dependency-aware:** dependency và critical path được biểu diễn rõ; không lập lịch khi prerequisite chưa đáp ứng.
6. **Risk-adjusted:** ưu tiên theo giá trị, rủi ro, uncertainty, dependency và cost of delay.
7. **Definition of Ready/Done:** không giao thực thi khi thiếu đầu vào; không đóng WP khi thiếu evidence.
8. **Independent verification:** implementer không tự xác nhận độc lập output của mình.
9. **Change control:** mọi thay đổi baseline có impact analysis và authority.
10. **No fake progress:** trạng thái kế hoạch không phải trạng thái thực thi; planned ≠ started ≠ completed.

## 3. Đầu vào

- DOC-008 approved requirements baseline, traceability và acceptance criteria.
- Architecture baseline, ADRs, contracts, deployment/security/operations design và G3 decision.
- Verification strategy, quality attribute scenarios và evidence requirements.
- Work constraints: time, cost, capacity, skills, tools, procurement, environment và compliance.
- Dependency map, risk register, assumptions, unresolved decisions và external commitments.
- Existing Work roadmap, mapping register và source ownership rules.
- Product Owner priorities, milestone constraints và release/acceptance target nếu đã được phê duyệt.

Mỗi estimate, deadline, resource commitment hoặc dependency phải ghi nguồn và độ tin cậy. Không suy ra availability/capacity của một cá nhân hoặc AI từ roster.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Chốt ưu tiên, scope, ngân sách/nguồn lực, deadline và trade-off trọng yếu; duyệt plan baseline |
| Plan Coordinator (Xu / AI-01) | Phân rã, điều phối dependency, duy trì roadmap/WP register, risk và change control |
| Work Package Owner | Chịu trách nhiệm đầu ra, estimate, tiến độ, evidence và escalation của WP |
| Implementer | Thực hiện task theo scope/contract, ghi log và artifact/evidence |
| Independent Reviewer / QE | Xác minh output và tiêu chí Done độc lập với implementer |
| Architect | Giải đáp design intent, quản lý ADR/ACR và đánh giá thay đổi kiến trúc |
| Operations/Security/Data Owner | Xác nhận prerequisite chuyên môn, readiness và operational/security controls |

Một người có thể kiêm vai trò trong WP nhỏ nếu được chấp thuận, nhưng không được mô tả self-review là independent review. AI agent chỉ được giao việc trong phạm vi tool/permission thực tế; roster không phải bằng chứng đã thực thi.

## 5. Quy trình lập kế hoạch — P01 đến P10

### P01 — Xác nhận baseline và phạm vi
- Kiểm tra G2/G3 decision, requirements baseline, architecture baseline và version.
- Đối chiếu In Scope/Out of Scope, constraints, acceptance và known limitations.
- Liệt kê unresolved decisions có thể chặn hoặc làm đổi kế hoạch.
- Nếu baseline mâu thuẫn, dừng lập execution baseline và trả đúng phase/authority.
**Đầu ra:** Planning Intake & Baseline Map.

### P02 — Xác định deliverables và decomposition
- Chuyển outcomes/requirements/architecture elements thành deliverables có thể nghiệm thu.
- Phân rã theo vertical value slice hoặc dependency hợp lý; tránh chia theo vai trò thuần túy nếu tạo handoff thừa.
- Xác định WP boundaries, interfaces, inputs/outputs và ownership.
- Không tạo WP chỉ để phản ánh một folder; folder không phải deliverable.
**Đầu ra:** Deliverable Breakdown & WP Candidate List.

### P03 — Định nghĩa Work Package
Mỗi WP tối thiểu có:
- WP ID ổn định, title, objective/outcome và rationale.
- Requirement/architecture/ADR trace links.
- Scope, exclusions, assumptions và constraints.
- Deliverables/artifacts, canonical source repository/path và version policy.
- Owner, implementers, independent reviewer và decision authority.
- Dependencies, prerequisites và interface/hand-off.
- Priority, risk/complexity, estimate range/confidence và estimate basis.
- Planned start/end hoặc milestone; không điền ngày cam kết khi chưa có cơ sở.
- Definition of Ready (DoR), Definition of Done (DoD) và verification/evidence requirements.
- Status, blocker, change history và last updated.
**Đầu ra:** Work Package Register.

### P04 — Phân tích dependency và sequencing
- Ghi predecessor/successor, dependency type, owner và exit condition.
- Phân biệt hard dependency, soft dependency, external dependency và parallelizable work.
- Xác định critical path, integration points, long-lead items và sequencing constraints.
- Xử lý dependency chưa xác nhận bằng risk/contingency, không giả định đã sẵn sàng.
**Đầu ra:** Dependency Graph & Milestone Sequence.

### P05 — Ước lượng và năng lực
- Ước lượng effort/duration/cost/resource theo range và confidence.
- Ghi assumptions, historical basis, uncertainty và exclusions.
- Kiểm tra skill/tool/environment availability, review capacity và integration overhead.
- Dùng spike/prototype để giảm uncertainty khi cần; spike có timebox và learning objective.
- Nếu chưa có dữ liệu, ghi UNKNOWN/TBD và cách lấy dữ liệu.
**Đầu ra:** Estimate & Capacity Plan.

### P06 — Ưu tiên, milestone và delivery strategy
- Ưu tiên theo outcome/value, risk reduction, dependency, urgency và cost of delay.
- Xác định milestone, sequencing, integration cadence, demo/review points và contingency.
- Xác định incremental delivery, feature flags, migration windows hoặc rollout stages khi liên quan.
- Không ép deadline/commitment ngoài thẩm quyền hoặc năng lực đã xác minh.
**Đầu ra:** Prioritized Roadmap & Milestone Plan.

### P07 — Risk, quality và verification planning
- Gắn risk với WP, dependency, owner, likelihood/impact, mitigation, contingency và trigger.
- Phân bổ verification: unit, integration, contract, system, security, performance, failure/recovery, browser/E2E, regression và operational checks khi phù hợp.
- Xác định evidence artifact, location, producer, verifier, environment và retention.
- Đảm bảo independent review có capacity và không bị dồn về cuối.
**Đầu ra:** WP Risk Register & Verification/Evidence Allocation.

### P08 — Build Mapping và source ownership
- Ánh xạ từng WP tới 05_BUILD child areas, canonical source repo/path, branch/ref và artifact owner.
- Ghi rõ mapping là pointer/coordination; bản copy tạm thời phải có source/version/hash và expiry/cleanup condition.
- Không để 05_BUILD trở thành source root hoặc WP plan thứ hai.
- Xác định integration branch/PR strategy và artifact promotion path.
**Đầu ra:** 05_BUILD Mapping Updates và Source Ownership Map.

### P09 — Plan quality review và baseline
- Kiểm tra traceability, completeness, dependency cycles, ownership gaps, estimate confidence, resource feasibility và review capacity.
- Kiểm tra WP không trùng, không bỏ sót deliverable bắt buộc và không có hidden scope.
- Xác nhận DoR/DoD, evidence plan và acceptance linkage.
- Reviewer ghi findings; sửa version có lịch sử.
- Product Owner phê duyệt baseline, priorities, constraints và commitments.
**Đầu ra:** DOC-011 Implementation Roadmap / WP Plan — READY FOR G4 REVIEW.

### P10 — G4 review và handoff sang BUILD
- Đối chiếu G4 criteria theo DOC-004.
- Ghi decision, authority, baseline version, scope, milestone và accepted risks.
- Chỉ sau G4 PASS mới cho phép mở execution WP/BUILD theo quyền.
- Giao WP có DoR đạt, owner, reviewer, source mapping và verification plan.
**Đầu ra:** G4 Gate Review Record và Build Authorization/Handoff Package nếu PASS.

## 6. Work Package lifecycle

Trạng thái WP chuẩn:
- **DRAFT:** đang phân rã, chưa đủ điều kiện review.
- **PROPOSED:** đủ thông tin cơ bản, chờ review/ưu tiên.
- **READY:** DoR đạt và có quyền bắt đầu theo gate.
- **IN_PROGRESS:** thực thi đã bắt đầu, có execution record.
- **BLOCKED:** có blocker cụ thể, owner và điều kiện gỡ.
- **IN_REVIEW:** deliverable đã nộp, đang chờ review/verification.
- **DONE:** DoD đạt, reviewer/evidence được ghi nhận.
- **CANCELLED:** bị dừng có authority và lý do.
- **SUPERSEDED:** được thay bằng WP/baseline mới; giữ trace lịch sử.

Không được chuyển DRAFT/PROPOSED trực tiếp thành DONE. DONE không tự động đồng nghĩa phase gate PASS hoặc product acceptance.

## 7. Definition of Ready và Definition of Done

### DoR — điều kiện sẵn sàng
- Objective/scope/exclusions rõ.
- Requirement/architecture trace links tồn tại.
- Inputs/prerequisites/dependencies đã sẵn sàng hoặc có quyết định chấp nhận.
- Owner, implementer, reviewer và authority được chỉ định.
- Deliverables và canonical source path rõ.
- Estimate/assumptions/risks đủ để quyết định.
- Acceptance/DoD, verification method và evidence location xác định.
- Quyền, môi trường, tool và dữ liệu thử nghiệm sẵn sàng.

### DoD — điều kiện hoàn thành
- Deliverable được cập nhật tại canonical source.
- Scope/acceptance của WP được đáp ứng.
- Tests/reviews cần thiết đã chạy; kết quả và môi trường được ghi.
- Evidence có ID, URI/path, hash/version, producer, timestamp và verifier khi áp dụng.
- Findings/defects được đóng hoặc có disposition/waiver hợp lệ.
- Documentation, mapping, changelog và handoff được cập nhật.
- Reviewer xác nhận; WP Owner không tự tạo independent PASS.
- Không còn blocker ẩn; residual risk được ghi.

## 8. G4 — Gate PLAN → BUILD

Điều kiện tối thiểu:
- [ ] G2 và G3 PASS; approved requirements/architecture baseline được xác định.
- [ ] Deliverables và WP decomposition truy được về outcomes/requirements/architecture.
- [ ] WP Register đầy đủ ID, objective, scope, owner, reviewer, dependencies và outputs.
- [ ] Mỗi WP có DoR/DoD, verification method và evidence requirements.
- [ ] Dependency graph không có cycle chưa xử lý; critical path và external dependencies rõ.
- [ ] Estimates có basis/range/confidence; capacity/skills/tools/environment được xác minh hoặc risk được chấp thuận.
- [ ] Milestones, priority, sequencing và contingency có cơ sở.
- [ ] Risks, assumptions, open decisions và mitigation có owner.
- [ ] 05_BUILD mapping trỏ đúng canonical source; không có source-of-truth ambiguity.
- [ ] Verification/QE/review capacity được phân bổ.
- [ ] Independent plan review hoàn tất; findings có disposition.
- [ ] Product Owner/authorized authority phê duyệt plan baseline và G4.

Trạng thái:
- **PASS:** mọi điều kiện bắt buộc đạt và authority decision có evidence.
- **NOT READY:** kế hoạch thiếu chi tiết có thể hoàn thiện.
- **NEEDS RESEARCH:** estimate/dependency/technical feasibility chưa có dữ liệu.
- **BLOCKED:** thiếu authority, nguồn lực, prerequisite hoặc external dependency.
- **WAIVED:** chỉ theo DOC-004, có rationale, scope, residual risk, owner và expiry/review date; không mặc định tương đương PASS.

G4 PASS cho phép bắt đầu các WP đã READY trong phạm vi được duyệt; không phải blanket authorization để bỏ qua DoR hoặc security/release controls.

## 9. Change control

Mọi thay đổi plan baseline dùng Plan Change Request (PCR):
- PCR ID, requester, date, rationale và evidence.
- WP/deliverable/dependency/milestone/estimate/owner bị ảnh hưởng.
- Impact tới requirements, architecture, security, verification, cost, capacity, schedule và acceptance.
- Options, risk, recommendation, reviewer và authority decision.
- Baseline version mới, migration/communication và audit history.

Thay đổi product outcome/scope/acceptance quay lại DEFINE. Thay đổi HOW/architecture theo DOC-044. Điều chỉnh sequencing/estimate trong quyền ủy quyền có thể được Plan Coordinator ghi nhận; thay đổi commitment/priority trọng yếu cần Product Owner.

## 10. Handoff sang 05_BUILD

Gói bàn giao:
- Approved requirements và architecture baseline references.
- G4 decision và approved DOC-011 plan version.
- WP Register, owners/reviewers, priority và status.
- DoR/DoD, deliverables và acceptance.
- Dependency graph, milestone, estimate/capacity và risk.
- 05_BUILD mapping: WP → build area → canonical repo/path → branch/ref → artifact.
- Verification/evidence allocation và QE/review schedule.
- Security/privacy/operational constraints.
- Open decisions, blockers, assumptions và escalation path.

05_BUILD ghi nhận thực thi và mapping; mọi thay đổi source được thực hiện ở canonical repository đã khai báo. Evidence cross-phase được đăng ký ở top-level 06_EVIDENCE. Kế hoạch WP gốc vẫn ở 04_PLAN.

## 11. Checklist thực hiện

- [ ] P01 baseline/scope/G2/G3.
- [ ] P02 deliverables/decomposition.
- [ ] P03 WP Register.
- [ ] P04 dependency/sequencing.
- [ ] P05 estimate/capacity.
- [ ] P06 priorities/milestones.
- [ ] P07 risk/verification/evidence.
- [ ] P08 05_BUILD mapping/source ownership.
- [ ] P09 plan review/baseline.
- [ ] P10 G4 decision/handoff.
- [ ] Update Document Register, Decision Log, Evidence Register and Work Execution Log as applicable.

## 12. Hướng dẫn AI tham gia PLAN

1. Đọc DOC-001, DOC-002, DOC-004, DOC-005, DOC-008, DOC-009, DOC-011, DOC-012, DOC-033, DOC-044 và hồ sơ liên quan.
2. Xác nhận G2/G3 trước khi phát hành execution plan.
3. Không suy ra owner availability, deadline, cost hoặc tool access từ roster.
4. Mỗi WP có deliverable, trace, owner, reviewer, dependency, DoR/DoD và evidence.
5. Không đặt WP plan trong 05_BUILD; chỉ mapping.
6. Estimate phải có basis/range/confidence; ghi TBD nếu thiếu dữ liệu.
7. Tách planned progress khỏi actual execution evidence.
8. Không tự phê duyệt priority/commitment/trade-off ngoài quyền.
9. Không fake PASS; status phải khớp bằng chứng.
10. Nếu thiếu điều kiện, báo blocker, evidence đã kiểm tra, bottleneck và điều kiện cần.

## 13. Ví dụ minh họa (giả định)

Một WP “Implement Work-scoped Core Read API” có thể cần contract được duyệt, authorization model, schema, owner Core, independent reviewer, test cases 401/403/404, Work isolation, stale/network failure và audit evidence. Nếu Core owner hoặc API contract chưa sẵn sàng, WP ở PROPOSED/BLOCKED với prerequisite cụ thể; không tự gán IN_PROGRESS/DONE. Đây là ví dụ phương pháp, không phải trạng thái thực tế của Work 70.

## 14. Kiểm soát và thay đổi

DOC-045 là chuẩn quy trình. Vinh quyết định ưu tiên, scope, chi phí/nguồn lực, deadline và G4. Xu điều phối và duy trì plan; không tự phê duyệt baseline hoặc commitment ngoài quyền được giao.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành P01–P10, WP lifecycle, DoR/DoD, dependency/estimate/risk planning, G4 và handoff standard. |
