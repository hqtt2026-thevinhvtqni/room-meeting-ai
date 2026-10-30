# QUY TRÌNH XÁC ĐỊNH YÊU CẦU / DEFINE PROCESS
- **STT / Document ID:** DOC-043
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 43
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-007; DOC-008; DOC-042
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích

DOC-043 quy định cách thực hiện phase 02_DEFINE (Xác định yêu cầu): chuyển kết quả Discover đã được chấp thuận thành định nghĩa sản phẩm đủ rõ để thiết kế kiến trúc và lập kế hoạch.

DEFINE trả lời: sản phẩm cần tạo ra giá trị gì, cho ai, trong phạm vi nào, hành vi/capability nào bắt buộc, chất lượng và giới hạn ra sao, đo thành công thế nào, điều kiện nào để nghiệm thu?

DEFINE không chọn kiến trúc chi tiết, framework, nhà cung cấp hay thiết kế giao diện cuối cùng. Những nội dung đó thuộc ARCHITECT hoặc các quyết định chuyên biệt được phê duyệt.

## 2. Điều kiện đầu vào và nguyên tắc

### 2.1 Entry criteria — điều kiện vào phase
- G1 DISCOVER → DEFINE đã PASS bởi Product Owner/authority theo DOC-004.
- Có DOC-007 Discover Brief phiên bản được chấp thuận.
- Có outcome PROCEED và gói bàn giao Discover.
- Các giả định/rủi ro chưa đóng được chuyển tiếp rõ ràng, có owner và điều kiện xử lý.
- Nếu G1 chưa PASS, chỉ được chuẩn bị/phân tích nháp; không đánh dấu DEFINE là phase ACTIVE chính thức và không tạo baseline yêu cầu đã duyệt.

### 2.2 Nguyên tắc bắt buộc
1. **Trace to value:** mỗi yêu cầu quan trọng phải truy về vấn đề, người dùng, outcome hoặc nghĩa vụ đã xác định ở Discover.
2. **One requirement, one meaning:** yêu cầu rõ, đơn nghĩa, có thể kiểm chứng; tránh “nhanh”, “thân thiện”, “an toàn”, “dễ dùng” nếu không định nghĩa cách đo.
3. **Solution-neutral:** mô tả WHAT/WHY; không khóa HOW trừ khi có constraint hoặc quyết định được duyệt.
4. **Necessary and sufficient:** không thêm tính năng chỉ vì có thể làm; phân biệt bắt buộc, mong muốn và ngoài phạm vi.
5. **Testability by design:** mỗi requirement có cách xác minh/acceptance criteria trước khi sang ARCHITECT.
6. **Explicit uncertainty:** TBD, assumption, dependency, conflict và decision pending phải hiển thị; không lấp bằng phỏng đoán.
7. **Single baseline:** có một phiên bản yêu cầu được duyệt; thay đổi phải có lịch sử và đánh giá tác động.
8. **No authority inflation:** AI/analyst có thể đề xuất và phân tích; Product Owner phê duyệt mục tiêu, scope, trade-off và G2.

## 3. Đầu vào

- DOC-007 Discover Brief đã qua G1.
- G1 decision record và reviewer findings.
- Evidence Register, stakeholder needs, assumptions/unknowns, risks.
- Ràng buộc pháp lý, bảo mật, quyền riêng tư, vận hành, chi phí, thời gian và nền tảng đã biết.
- Các chuẩn bắt buộc, hợp đồng hoặc giao diện hiện hữu nếu có.
- Những quyết định sản phẩm đã được ghi trong Decision Log.

Đầu vào thiếu phải được ghi vào Open Questions/Decision Register. Không tự suy diễn thành requirement đã phê duyệt.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Chốt product outcome, scope, ưu tiên, trade-off, tiêu chí thành công và G2 |
| Define Coordinator (Xu / AI-01) | Điều phối elicitation, chuẩn hóa yêu cầu, traceability, phiên bản và gate pack |
| Business/Product Analyst | Phân rã nhu cầu, use cases, workflows, rules và acceptance criteria |
| User/Stakeholder | Xác nhận nhu cầu, luồng công việc, ngoại lệ và tính phù hợp |
| Architect / Technical Advisor | Tư vấn feasibility, constraints, interface/security implications; không tự thay đổi mục tiêu |
| Reviewer / QE | Rà soát tính rõ ràng, đầy đủ, nhất quán, testability và traceability |

Người viết requirement không được tự nhận là reviewer độc lập. Với requirement có rủi ro cao, cần reviewer/chuyên gia phù hợp. Việc tham gia của AI phải có bằng chứng; roster không chứng minh đã review.

## 5. Quy trình thực hiện — F01 đến F09

### F01 — Xác nhận đầu vào Discover
- Kiểm tra G1 decision, brief version, outcome và authority.
- Đối chiếu các vấn đề, users, evidence, assumptions, unknowns, constraints và risks.
- Ghi các điểm chưa rõ, mâu thuẫn hoặc không còn đúng.
- Nếu phát hiện vấn đề nền tảng sai, đề nghị quay lại DISCOVER; không âm thầm sửa baseline.
**Đầu ra:** Define Intake & Trace Map.

### F02 — Xác định Product Outcome và Success Measures
- Viết outcome theo giá trị người dùng/sản phẩm, không phải danh sách tính năng.
- Xác định metric, định nghĩa, baseline, target, đơn vị, nguồn dữ liệu, tần suất và owner.
- Nếu chưa có baseline/target, ghi TBD, lý do và kế hoạch đo; không tự đặt số làm cam kết.
- Phân biệt outcome metric, output/delivery metric và operational guardrail.
**Đầu ra:** Outcome & Success Metrics Register.

### F03 — Xác định actors, use cases và workflows
- Liệt kê actor, quyền hạn, mục tiêu, trigger, precondition, main flow, alternate flow, exception và postcondition.
- Mô tả workflow hiện tại và workflow mong muốn khi cần.
- Bao gồm tình huống lỗi, retry, timeout, mất kết nối, dữ liệu thiếu và thao tác bị từ chối nếu liên quan.
- Không bỏ qua người vận hành, kiểm toán, hỗ trợ và hệ thống tích hợp.
**Đầu ra:** Actor Map, Use Case List và Workflow Catalogue.

### F04 — Xác định scope và boundaries
- Ghi rõ In Scope, Out of Scope, deferred và assumptions.
- Xác định system boundary, external actors/systems và ownership.
- Nêu các interface/data exchange cần có ở mức nhu cầu, chưa áp đặt thiết kế.
- Ghi constraint và dependency nội bộ/bên ngoài.
**Đầu ra:** Scope & Boundary Statement.

### F05 — Phân rã và viết requirements
Phân loại tối thiểu khi phù hợp:
- **BUS:** business/product outcome và policy.
- **USR:** user/stakeholder needs.
- **FR:** functional requirements — hành vi/chức năng.
- **NFR:** non-functional requirements — hiệu năng, độ sẵn sàng, khả năng mở rộng, khả dụng, accessibility, portability, maintainability.
- **DATA:** dữ liệu, chất lượng, provenance, retention, export, deletion và ownership.
- **SEC/PRIV:** bảo mật, quyền, audit, privacy, threat/control expectations.
- **INT:** tích hợp, API/interface, event, protocol và compatibility.
- **OPS:** logging, monitoring, backup, recovery, support và operability.
- **REG:** pháp lý, compliance, tiêu chuẩn hoặc hợp đồng bắt buộc.

Mỗi requirement có ID ổn định, statement, rationale, source/trace, priority, owner, dependencies, verification method, acceptance criteria và status. Một requirement phải đủ nhỏ để kiểm chứng; không gộp nhiều nghĩa không liên quan.

**Đầu ra:** Requirements Catalogue.

### F06 — Định nghĩa acceptance criteria và quality attributes
- Viết tiêu chí quan sát/đo được, ưu tiên Given–When–Then hoặc điều kiện đầu vào/hành động/kết quả.
- Với NFR, ghi ngưỡng, tải, môi trường, percentile, cửa sổ đo và cách thu thập khi thích hợp.
- Với security/privacy/data, xác định control expectation, negative cases và evidence cần có.
- Nêu hành vi khi lỗi: fail-safe/fail-closed, retry, idempotency, recovery, degradation hoặc escalation khi phù hợp.
- Không ghi “100% an toàn”, “không lỗi”, “real-time” nếu không định nghĩa được.
**Đầu ra:** Acceptance Criteria & Quality Attribute Register.

### F07 — Ưu tiên, trade-off và quyết định
- Dùng MoSCoW (Must/Should/Could/Won't for now) hoặc thang ưu tiên đã được Work chấp thuận.
- Mỗi Must phải có lý do: outcome, rủi ro, nghĩa vụ hoặc dependency.
- Nêu chi phí cơ hội, độ phức tạp, rủi ro và phương án thay thế.
- Ghi quyết định pending và người có thẩm quyền; không dùng điểm số AI làm quyết định cuối.
**Đầu ra:** Prioritized Backlog & Decision Register.

### F08 — Kiểm tra chất lượng và lập Product Requirements
- Kiểm tra mỗi requirement: cần thiết, rõ, đơn nghĩa, khả thi ở mức sơ bộ, không trùng, nhất quán, truy xuất được và kiểm chứng được.
- Kiểm tra coverage: outcome → need/use case → requirement → acceptance criteria → verification method.
- Kiểm tra negative/edge cases, permission boundaries, failure modes và data lifecycle.
- Reviewer ghi findings; sửa theo version, không xóa dấu vết.
- Cập nhật DOC-008 và tạo baseline ứng viên.
**Đầu ra:** DOC-008 Product Requirements vX.Y — READY FOR G2 REVIEW.

### F09 — Rà soát và quyết định G2
- Đối chiếu tiêu chí G2 trong DOC-004.
- Xác nhận scope, requirements, success metrics, constraints, risks và open decisions.
- Reviewer xác nhận chất lượng; Product Owner quyết định phê duyệt baseline và cho phép sang ARCHITECT.
- Ghi G2 decision record, authority, thời gian, baseline version và phạm vi.
**Đầu ra:** G2 Gate Review Record và approved requirements baseline (nếu PASS).

## 6. Quy tắc viết requirement

Một requirement tốt:
- Có một ID không đổi qua các lần sửa.
- Dùng ngôn ngữ chủ thể + hành vi/kết quả + điều kiện.
- Tránh từ mơ hồ: nhanh, dễ, tốt, đầy đủ, thân thiện, mạnh mẽ, phù hợp.
- Có rationale và nguồn truy xuất.
- Có priority và người chịu trách nhiệm.
- Có verification method và acceptance criteria.
- Có trạng thái: DRAFT, PROPOSED, APPROVED, DEFERRED, REJECTED, SUPERSEDED.
- Không trộn requirement với implementation task hoặc design decision.

Ví dụ dạng statement: “Khi [điều kiện], hệ thống phải [hành vi có thể quan sát] để [mục tiêu/rationale].” Đây là cấu trúc minh họa, không phải requirement của Work 70.

## 7. Traceability — truy xuất hai chiều

Mỗi requirement quan trọng phải truy được:
Discover problem/evidence → user need/outcome → use case → requirement → acceptance criteria → verification evidence → decision.

Phải hỗ trợ truy ngược: nếu một problem/outcome bị loại bỏ hoặc thay đổi, xác định được requirements, design, tests và WPs bị ảnh hưởng.

Không được:
- Tạo requirement không có rationale/source.
- Ghi acceptance criteria không gắn requirement.
- Đánh dấu requirement APPROVED khi G2 chưa PASS.
- Xóa requirement bị loại; chuyển REJECTED/SUPERSEDED và ghi lý do.

## 8. G2 — Gate DEFINE → ARCHITECT

Điều kiện tối thiểu:
- [ ] G1 PASS và DOC-007 được chấp thuận.
- [ ] Product outcome và success measures được định nghĩa hoặc khoảng trống có kế hoạch/authority chấp nhận.
- [ ] Actors, stakeholder needs và use cases trọng yếu được xác định.
- [ ] In-scope, out-of-scope và system boundary rõ.
- [ ] Requirements catalogue có ID, rationale, priority, source và owner.
- [ ] Acceptance criteria/verification method đủ kiểm chứng cho requirements bắt buộc.
- [ ] NFR, data, security/privacy, integration, operations và compliance được xem xét khi liên quan.
- [ ] Constraints, dependencies, risks, open questions và trade-offs được ghi.
- [ ] Traceability hai chiều được rà soát.
- [ ] Reviewer hoàn tất findings hoặc ghi rõ ngoại lệ.
- [ ] Product Owner phê duyệt baseline và quyết định G2.

Trạng thái:
- **PASS:** tiêu chí bắt buộc đạt, baseline version xác định, authority ghi quyết định.
- **NOT READY:** thiếu hoặc mơ hồ các artifact có thể hoàn thiện.
- **NEEDS RESEARCH:** thiếu bằng chứng/khảo sát cần thiết để xác định yêu cầu.
- **BLOCKED:** quyền quyết định, dependency hoặc điều kiện bên ngoài chưa được giải quyết.
- **WAIVED:** chỉ theo DOC-004, có authority, rationale, scope, expiry/review date và residual risk; không mặc định tương đương PASS.

Dashboard status, số lượng requirements hoặc AI consensus không thay thế G2 decision record.

## 9. Change control — kiểm soát thay đổi baseline

Mọi thay đổi sau khi G2 PASS phải có Change Request:
- CR ID, requester, ngày và lý do.
- Requirement/metric/scope bị ảnh hưởng.
- Trace impact tới architecture, data, security, plan, WPs, tests, evidence, cost và schedule.
- Options, trade-offs, risks và recommendation.
- Reviewer và Product Owner decision.
- Version mới, ngày hiệu lực và danh sách tài liệu cần cập nhật.

Không sửa lặng lẽ baseline đã duyệt. Thay đổi nhỏ không làm đổi outcome có thể xử lý theo quyền được ủy quyền; thay đổi mục tiêu, scope trọng yếu, security/privacy, chi phí hoặc acceptance phải escalated.

## 10. Handoff sang ARCHITECT

Gói bàn giao tối thiểu:
- DOC-007 và G1 decision reference.
- DOC-008 approved baseline và G2 decision reference.
- Outcome & Success Metrics Register.
- Actors/use cases/workflows và scope boundaries.
- Requirements catalogue và traceability matrix.
- Acceptance criteria, quality attributes và verification expectations.
- Constraints, dependencies, risks, assumptions, open questions và decisions.
- Change history và known limitations.

ARCHITECT được quyền quyết định HOW trong phạm vi yêu cầu/constraint đã duyệt. Nếu kiến trúc cho thấy yêu cầu không khả thi hoặc có trade-off trọng yếu, trả lại DEFINE để Product Owner quyết định; không âm thầm hạ requirement.

## 11. Checklist đóng phase

- [ ] F01 xác nhận G1 và đầu vào Discover.
- [ ] F02 outcomes và metrics có định nghĩa/owner.
- [ ] F03 actors, use cases và workflows.
- [ ] F04 scope và boundaries.
- [ ] F05 requirements catalogue.
- [ ] F06 acceptance criteria và quality attributes.
- [ ] F07 priority, trade-offs và decisions.
- [ ] F08 quality review, traceability và DOC-008 baseline candidate.
- [ ] F09 reviewer findings và G2 decision.
- [ ] Handoff package đầy đủ.
- [ ] Document Register, Decision Log, Evidence Register và Work Execution Log được cập nhật khi phát sinh artifact/decision tương ứng.

## 12. Hướng dẫn AI khi tham gia DEFINE

1. Đọc DOC-001, DOC-002, DOC-004, DOC-005, DOC-007, DOC-008 và DOC-043.
2. Kiểm tra G1 PASS trước khi coi DEFINE là phase đã mở.
3. Tách fact/evidence, stakeholder report, inference, assumption, recommendation và decision.
4. Không tự đặt metric target, scope, priority hoặc acceptance thay Product Owner.
5. Không áp đặt công nghệ/kiến trúc ở phase DEFINE.
6. Mọi requirement có ID, rationale, trace, priority, owner và verification method.
7. Không tạo fake PASS; ghi DONE/PASS/NOT RUN/BLOCKED/NOT VERIFIED đúng nghĩa.
8. Khi mâu thuẫn yêu cầu, ghi conflict và chuyển đúng authority; không tự chọn một phía.
9. Giữ baseline và change history; không xóa dấu vết.
10. Handoff đủ dữ liệu cho ARCHITECT; không chuyển unresolved risk thành “đã xử lý”.

## 13. Ví dụ minh họa (giả định)

Discover xác định vấn đề là “người quản lý không phân biệt được hoàn tất tác vụ với nghiệm thu Work”. DEFINE cần xác định nhóm người dùng, outcome mong muốn, định nghĩa chính xác của các trạng thái, quyền cập nhật, nguồn dữ liệu, điều kiện stale/unknown, tiêu chí truy xuất evidence và cách đo tỷ lệ Work có trạng thái đáng tin cậy.

Không mặc định requirement là “xây Dashboard”. Có thể kết quả DEFINE cho thấy cần chuẩn hóa state model và evidence contract trước, Dashboard chỉ là một consumer. Đây là ví dụ phương pháp, không phải xác nhận trạng thái runtime của Work 70.

## 14. Kiểm soát thay đổi

DOC-043 là chuẩn quy trình. Vinh là authority cuối cùng đối với mục tiêu, scope, acceptance, trade-off trọng yếu và G2. Xu duy trì quy trình, chuẩn hóa hồ sơ và chuẩn bị quyết định; không tự phê duyệt baseline.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành F01–F09, requirements taxonomy, traceability, G2, change control and handoff standard. |
