# QUY TRÌNH THIẾT KẾ KIẾN TRÚC / ARCHITECT PROCESS
- **STT / Document ID:** DOC-044
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 44
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-008; DOC-009; DOC-010; DOC-033; DOC-038; DOC-043
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-044 quy định cách thực hiện 03_ARCHITECT (Thiết kế kiến trúc): chuyển requirements baseline đã được G2 chấp thuận thành kiến trúc có thể triển khai, kiểm chứng, vận hành và quản trị thay đổi.

ARCHITECT trả lời HOW: hệ thống được chia thành những ranh giới nào, thành phần nào chịu trách nhiệm gì, dữ liệu thuộc ai, các thành phần giao tiếp ra sao, bảo mật và lỗi được xử lý thế nào, kiến trúc được triển khai và kiểm chứng bằng cách nào.

ARCHITECT không tự thay đổi WHAT/WHY đã được DEFINE phê duyệt. Nếu phát hiện requirement thiếu, mâu thuẫn, không khả thi hoặc trade-off làm thay đổi outcome/scope/acceptance, phải tạo finding/change request và trả về DEFINE để đúng authority quyết định. Không âm thầm hạ yêu cầu để làm kiến trúc dễ hơn.

DOC-044 là quy trình. DOC-009 là hồ sơ kiến trúc nền tảng và mô hình vòng đời Work; DOC-010 là hợp đồng đọc Dashboard–Core. Hai hồ sơ đó không bị thay thế bởi DOC-044.

## 2. Điều kiện đầu vào

### 2.1 Entry criteria
- G2 DEFINE → ARCHITECT đã PASS theo DOC-004 bởi Product Owner/authority.
- DOC-008 Product Requirements có version baseline được duyệt và decision record tương ứng.
- Có scope, actors, use cases, acceptance criteria, quality attributes, constraints, dependencies và traceability.
- Các rủi ro/unknown/open decisions còn lại có owner, cách xử lý và điều kiện chấp nhận rõ.
- Có quyền truy cập tài liệu, mã nguồn, API/schema và chuyên gia cần thiết để xác minh hiện trạng khi kiến trúc phụ thuộc vào chúng.

Nếu G2 chưa PASS, chỉ được chuẩn bị phân tích/kiến trúc nháp. Không được tuyên bố phase ARCHITECT chính thức đã mở, không đóng G3 và không phát hành architecture baseline đã duyệt.

### 2.2 Nguyên tắc
1. **Requirements first:** mọi quyết định kiến trúc phải truy về requirement, constraint hoặc rủi ro có căn cứ.
2. **Evidence over assumption:** phân biệt IMPLEMENTED/OBSERVED, DOCUMENTED, PROPOSED, ASSUMED và UNKNOWN.
3. **Fit-for-purpose:** chỉ tạo view/model cần thiết để giải quyết stakeholder concern và rủi ro; không vẽ cho đủ bộ.
4. **Explicit boundaries:** xác định rõ ownership, trust boundary, source of truth và quyền ghi.
5. **Secure and resilient by design:** security, privacy, failure, recovery và observability được xét từ đầu.
6. **Verifiable architecture:** quality attributes phải có scenario, ngưỡng/tiêu chí và phương pháp kiểm chứng.
7. **Reversible decisions:** ghi alternatives, consequences, assumptions và khả năng đảo ngược trong ADR.
8. **No authority inflation:** AI/architect đề xuất; Product Owner quyết định trade-off sản phẩm, scope, chi phí và G3.
9. **No fake implementation:** bản vẽ, hợp đồng hoặc endpoint đề xuất không phải bằng chứng code/runtime đã tồn tại.
10. **Change with traceability:** mọi thay đổi kiến trúc đánh giá tác động hai chiều tới requirements, plans, code, tests và evidence.

## 3. Đầu vào bắt buộc

- DOC-008 approved requirements baseline và G2 decision.
- DOC-007 Discover Brief cùng các evidence/risk/assumption liên quan khi cần.
- Use cases, workflows, system boundary và acceptance criteria.
- NFR/quality attribute scenarios, security/privacy/data/integration/operations requirements.
- Existing architecture, source code, API contracts, schemas, deployment topology và operational constraints đã xác minh.
- Dependency, vendor/platform constraints, legal/compliance obligations.
- Risk register, open questions, decision log và known limitations.
- DOC-009/DOC-010 và các architecture records liên quan nếu phạm vi có liên quan.

Mỗi nguồn hiện trạng phải ghi repository/path, branch/ref hoặc version, thời điểm đọc, phạm vi đã xem và giới hạn kiểm tra. Nếu chưa truy cập được source/runtime, ghi UNKNOWN/NOT VERIFIED; không suy từ tên file hoặc tài liệu đề xuất thành hiện trạng.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Chốt trade-off sản phẩm, scope, chi phí/rủi ro trọng yếu và G3 |
| Architect / Architecture Lead | Chịu trách nhiệm tính nhất quán, các view, interface, ADR và traceability |
| Lifecycle Orchestrator (Xu / AI-01) | Điều phối toàn trình, kiểm tra đầu vào/đầu ra, hồ sơ và gate pack; không tự phê duyệt G3 |
| Domain/Product Analyst | Giải thích requirements, workflows, business rules và xác nhận tác động |
| Security/Privacy Reviewer | Rà soát threat model, trust boundary, quyền, dữ liệu và control |
| Platform/Operations Engineer | Rà soát deployment, reliability, observability, backup/recovery và vận hành |
| Implementer / Technical Owner | Đánh giá feasibility, implementation implications và estimate có căn cứ |
| Independent Reviewer / QE | Rà soát độc lập tính đầy đủ, nhất quán, khả kiểm chứng và evidence |

Người thiết kế không được tự nhận là reviewer độc lập cho cùng artifact. Danh sách AI tham gia không chứng minh đã thực hiện review; cần ghi người, phạm vi, thời điểm và kết quả thực tế.

## 5. Quy trình thực hiện — A01 đến A10

### A01 — Xác nhận baseline và kiến trúc hiện trạng
- Kiểm tra G2 decision, DOC-008 version, scope và acceptance baseline.
- Đọc DOC-009, DOC-010 và architecture records có liên quan.
- Kiểm tra source/API/schema/runtime cần thiết; ghi chính xác branch/ref, path, thời điểm và phạm vi.
- Phân loại nội dung: IMPLEMENTED/OBSERVED, DOCUMENTED, PROPOSED, ASSUMED, UNKNOWN hoặc CONFLICTED.
- Xác định tài liệu cũ, duplicate, drift và các mâu thuẫn.
**Đầu ra:** Architecture Intake & As-Is Evidence Map.

### A02 — Xác định architecture drivers và quality scenarios
- Liệt kê stakeholder concerns, functional drivers, constraints và rủi ro.
- Chuyển NFR thành quality attribute scenarios: source/actor, stimulus, condition, expected response, measurable response measure.
- Xác định các ưu tiên có xung đột như security vs usability, consistency vs availability, latency vs cost.
- Nêu trade-off và quyết định cần Product Owner.
**Đầu ra:** Architecture Drivers & Quality Attribute Scenario Register.

### A03 — Thiết kế system context và boundaries
- Xác định system-of-interest, actors, external systems, dependencies và trust boundaries.
- Mô tả responsibility, ownership, protocol/data exchange ở mức phù hợp.
- Chỉ rõ những gì thuộc hệ thống, bên ngoài hệ thống, adapter hoặc human authority.
- Không để một thành phần vừa là nguồn dữ liệu chuẩn vừa là projection nếu chưa có quyết định rõ.
**Đầu ra:** System Context View, Boundary & Ownership Map.

### A04 — Thiết kế logical/component/service architecture
- Phân rã thành phần theo trách nhiệm, cohesion, coupling và bounded context khi phù hợp.
- Với mỗi thành phần ghi purpose, owner, inputs/outputs, state, permission, failure behavior và dependencies.
- Chỉ định source of truth cho identity, authorization, lifecycle state, decisions, evidence metadata và artifact bytes.
- Xác định sync/async, transaction boundary, idempotency và consistency model khi liên quan.
- Phân biệt logical service với service/API đã triển khai thực tế.
**Đầu ra:** Component/Service View, Responsibility Matrix, State & Ownership Model.

### A05 — Thiết kế interface, API, event và data contracts
- Mỗi interface ghi producer/consumer, operation, schema/version, validation, authN/authZ, error semantics, timeout/retry, pagination, idempotency và compatibility.
- Với event ghi event identity, ordering, delivery semantics, replay, deduplication và retention khi phù hợp.
- Với data ghi schema, classification, ownership, lifecycle, provenance, retention/deletion, consistency và migration.
- Xác định contract tests và backward/forward compatibility.
- Endpoint/schema chỉ được gọi là IMPLEMENTED sau khi đối chiếu mã nguồn hoặc runtime và có bằng chứng kiểm chứng.
**Đầu ra:** API/Event/Data Contract Set và Contract Verification Plan.

### A06 — Security, privacy và threat model
- Xác định assets, actors, entry points, trust boundaries và threat scenarios.
- Phân tích authentication, authorization, least privilege, tenant/Work isolation, secret handling, audit và abuse cases.
- Xác định data classification, minimization, retention, deletion, export và privacy controls.
- Xem xét injection, confused deputy, privilege escalation, replay, data leakage, supply-chain và untrusted tool output khi liên quan.
- Mỗi threat có likelihood/impact hoặc phương pháp xếp hạng, control, residual risk, owner và verification evidence.
- High-risk residual risk phải escalated đúng authority; không tự waiver.
**Đầu ra:** Threat Model, Security/Privacy Control Matrix và Residual Risk Register.

### A07 — Failure modes, resilience và operability
- Xác định failure mode cho từng dependency và boundary: unavailable, timeout, partial write, duplicate, stale, corrupt, unauthorized, overload.
- Định nghĩa fail-open/fail-closed theo rủi ro; không dùng một chính sách chung cho mọi tình huống.
- Thiết kế retry/backoff, timeout, circuit breaking, idempotency, reconciliation, rollback và recovery khi phù hợp.
- Xác định logging, metrics, tracing, alert, audit, health/readiness và support ownership.
- Xác định backup/restore, RPO/RTO hoặc ghi TBD có owner/kế hoạch đo nếu chưa chốt.
**Đầu ra:** Failure & Recovery Model, Observability/Ops Design và Verification Scenarios.

### A08 — Deployment, runtime và technology decisions
- Mô tả environment, trust zones, network flows, deployment units, scaling, configuration và secrets.
- Ghi resource assumptions, capacity, availability, backup, upgrade/rollback và environment parity.
- Chọn công nghệ dựa trên requirements, constraints, operational capability, security, lifecycle, cost và alternatives.
- Không chọn framework/vendor chỉ vì quen thuộc hoặc vì AI đề xuất.
- Tách rõ technology already in use, selected but not implemented và candidate.
**Đầu ra:** Deployment/Runtime View, Technology Decision Set và Operational Constraints.

### A09 — ADR, traceability và architecture quality review
Mỗi Architecture Decision Record (ADR — hồ sơ quyết định kiến trúc) tối thiểu có:
- ADR ID, title, status, date, owner và decision authority.
- Context/problem và requirement/constraint/risk links.
- Options considered, including “do nothing”.
- Decision và rationale; evidence và counter-evidence.
- Consequences, trade-offs, security/ops/cost impact.
- Reversibility, migration/rollback strategy và revisit trigger.
- Reviewers, approval reference và superseded ADR nếu có.

Rà soát traceability:
requirements → architecture elements/contracts → quality scenarios → verification methods/evidence.
Đồng thời truy ngược architecture element tới requirement/driver; thành phần không có lý do phải được giải trình hoặc loại khỏi baseline.

**Đầu ra:** ADR Register, Architecture Traceability Matrix, Review Findings và candidate baseline.

### A10 — G3 review và handoff sang PLAN
- Kiểm tra toàn bộ G3 criteria tại mục 9.
- Phân loại finding: BLOCKER, MAJOR, MINOR, OBSERVATION; gán owner và due/exit condition.
- Independent reviewer ghi kết quả, không tự phê duyệt thay Product Owner.
- Product Owner quyết định PASS, NOT READY, BLOCKED hoặc WAIVED theo DOC-004.
- Chỉ khi G3 PASS mới phát hành architecture baseline làm đầu vào chính thức cho 04_PLAN.
**Đầu ra:** G3 Gate Review Record và Architecture Baseline/Handoff Package nếu được duyệt.

## 6. Bộ hồ sơ kiến trúc tối thiểu

Tạo theo mức độ liên quan, không bắt buộc vẽ tất cả nếu không có giá trị:
- System Context Diagram.
- Container/Component Diagram hoặc logical service view.
- Deployment/Runtime Diagram.
- Data Flow/Trust Boundary Diagram.
- Sequence/State Diagram cho workflow hoặc state transition trọng yếu.
- API/Event/Data Contracts và version policy.
- Data ownership/source-of-truth model.
- Threat model và security/privacy control matrix.
- Failure/recovery và observability/operations design.
- Quality attribute scenarios và verification mapping.
- ADR Register và Architecture Traceability Matrix.
- Risk, assumption, dependency, open decision và known limitation register.

Mỗi diagram/model phải có title, ID/version, scope, legend, owner, date, source/assumptions và liên kết requirements/ADR. Diagram là mô hình giải thích; không thay thế source code, runtime test hoặc security evidence.

## 7. Quy tắc chất lượng kiến trúc

Một architecture baseline tốt phải:
- Đáp ứng approved requirements hoặc ghi rõ gap/decision cần trả lại DEFINE.
- Có boundaries, responsibilities, ownership và source of truth rõ.
- Không có write path trái phép hoặc quyền authority bị mở rộng ngoài chủ đích.
- Có contract đủ rõ để implementer và verifier độc lập hiểu giống nhau.
- Bao phủ quality attributes, security/privacy, failure/recovery và operations theo risk.
- Có traceability hai chiều và ADR cho quyết định trọng yếu.
- Có thể kiểm chứng bằng test, inspection, analysis hoặc operational evidence xác định trước.
- Nêu rõ assumptions, limitations, residual risks và phần chưa xác minh.
- Không mô tả proposal như implementation hoặc runtime truth.

## 8. Quản lý thay đổi kiến trúc

Mọi thay đổi sau khi G3 PASS phải có Architecture Change Request (ACR):
- ACR ID, requester, ngày, lý do và evidence.
- Requirements, architecture views, interfaces, data, ADRs bị ảnh hưởng.
- Impact tới security/privacy, reliability, operations, cost, schedule, migration và compatibility.
- Alternatives, risk, recommendation và reviewers.
- Authority decision, version mới và kế hoạch verification.
Thay đổi làm đổi product outcome, scope, requirement hoặc acceptance phải quay lại DEFINE/G2. Thay đổi thuần HOW trong phạm vi baseline có thể xử lý bằng ADR/ACR theo quyền được ủy quyền. Không sửa lặng lẽ baseline đã duyệt.

## 9. G3 — Gate ARCHITECT → PLAN

Điều kiện tối thiểu:
- [ ] G2 PASS và DOC-008 approved baseline/version được xác định.
- [ ] Architecture drivers và quality attribute scenarios được mô tả, có cách đo/kiểm chứng.
- [ ] System context, boundaries, external dependencies và trust zones rõ.
- [ ] Components/services, responsibilities, ownership và source of truth rõ.
- [ ] Interfaces/API/events/data contracts đủ chi tiết và có version/error/auth rules khi liên quan.
- [ ] Security/privacy/threat model và controls được review; residual risks có authority/owner.
- [ ] Failure modes, resilience, recovery, observability và operational ownership được xác định.
- [ ] Deployment/runtime/environment và technology decisions có rationale.
- [ ] ADRs cho quyết định trọng yếu có alternatives/consequences/reversibility.
- [ ] Traceability từ requirements tới architecture/contracts và verification strategy được rà soát.
- [ ] Architecture artifacts/diagrams đủ cho implementer và reviewer; known limitations được công khai.
- [ ] Independent architecture review hoàn tất; blocker được đóng hoặc xử lý theo waiver hợp lệ.
- [ ] Product Owner/authorized authority ghi G3 decision, baseline version, scope và thời điểm.

Trạng thái:
- **PASS:** mọi điều kiện bắt buộc đạt; reviewer và authority decision có bằng chứng.
- **NOT READY:** thiếu artifact/chi tiết có thể hoàn thiện trong phạm vi.
- **NEEDS RESEARCH:** thiếu bằng chứng/khảo sát kỹ thuật hoặc domain cần thiết.
- **BLOCKED:** thiếu quyền, dependency, điều kiện môi trường hoặc quyết định bên ngoài.
- **WAIVED:** chỉ theo DOC-004, đúng authority, rationale, phạm vi, residual risk, expiry/review date; không tự động đồng nghĩa PASS.

Không được suy G3 PASS từ số lượng tài liệu, sơ đồ, ADR, commit hay sự đồng thuận AI.

## 10. Handoff sang 04_PLAN

Gói bàn giao gồm:
- DOC-008 approved requirements baseline và G2 decision reference.
- Architecture baseline/version và G3 decision reference.
- Architecture views/models, contracts, data ownership và trust boundaries.
- ADR Register và quyết định còn mở.
- Requirements-to-architecture traceability.
- Quality attribute scenarios và verification strategy.
- Security/privacy controls, residual risks và threat model.
- Failure/recovery/observability/operations requirements.
- Deployment/runtime/technology decisions.
- Dependencies, constraints, assumptions, limitations và risks.
- Candidate work packages/dependency hints ở mức phân rã kiến trúc; 04_PLAN mới là nơi lập kế hoạch/WP chính thức.
- Danh sách verification, prototype/spike hoặc evidence cần có trước BUILD.

04_PLAN được quyền lập trình tự, WP, owner, reviewer, dependency và milestone trong giới hạn baseline. Nếu plan cho thấy phải thay đổi WHAT/acceptance hoặc kiến trúc không còn đáp ứng, mở change request và quay lại phase thích hợp.

## 11. Checklist thực hiện

- [ ] A01 xác nhận G2, baseline và hiện trạng có provenance.
- [ ] A02 drivers và quality scenarios.
- [ ] A03 context, boundaries và ownership.
- [ ] A04 logical/component/service architecture.
- [ ] A05 API/event/data contracts.
- [ ] A06 security/privacy/threat model.
- [ ] A07 failure/recovery/observability/operations.
- [ ] A08 deployment/runtime/technology decisions.
- [ ] A09 ADR, traceability và independent review.
- [ ] A10 G3 decision và handoff.
- [ ] Cập nhật Document Register, Decision Log, Evidence Register và Work Execution Log khi phát sinh hồ sơ/decision/evidence.

## 12. Hướng dẫn AI tham gia ARCHITECT

1. Đọc DOC-001, DOC-002, DOC-004, DOC-005, DOC-008, DOC-009, DOC-010 và DOC-044 cùng tài liệu liên quan.
2. Xác nhận G2 trước khi coi phase ARCHITECT đã mở.
3. Đọc source/runtime cần thiết trước khi kết luận hiện trạng; ghi branch/ref/path/time/scope.
4. Tách IMPLEMENTED, DOCUMENTED, PROPOSED, ASSUMED, UNKNOWN và CONFLICTED.
5. Không tự thay đổi requirement, acceptance, product scope hoặc authority.
6. Mọi quyết định kiến trúc trọng yếu phải có ADR; mọi contract phải có producer/consumer và verification.
7. Không coi sơ đồ/API proposal là bằng chứng implementation.
8. Báo finding, counter-evidence và residual risk; không che giấu bất đồng.
9. Không fake PASS; ghi DONE/PASS/FAIL/BLOCKED/NOT RUN/NOT VERIFIED đúng nghĩa.
10. Nếu thiếu điều kiện, nêu blocker cụ thể, bằng chứng đã thử, bottleneck và điều kiện cần để tiếp tục.

## 13. Ví dụ minh họa (giả định)

Một sản phẩm có Dashboard đọc trạng thái Work từ Core. Architect có thể đề xuất Core là nguồn trạng thái chuẩn, Dashboard chỉ render projection, mọi endpoint có Work-scope authorization và source mode/freshness rõ. Tuy nhiên, nếu router hiện tại chưa có Work-scoped endpoint, hồ sơ phải ghi PROPOSED/NOT IMPLEMENTED; cần source inspection và integration tests trước khi đánh dấu triển khai. Ví dụ này minh họa phương pháp, không xác nhận một endpoint cụ thể đang tồn tại.

## 14. Kiểm soát và thay đổi

DOC-044 là chuẩn quy trình. Vinh là authority cuối cùng cho trade-off sản phẩm, scope, chi phí/rủi ro trọng yếu và G3. Xu điều phối, duy trì hồ sơ và chuẩn bị gate pack; không tự phê duyệt G3.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành A01–A10, architecture views/contracts, security, resilience, ADR, traceability, G3 và handoff standard. |
