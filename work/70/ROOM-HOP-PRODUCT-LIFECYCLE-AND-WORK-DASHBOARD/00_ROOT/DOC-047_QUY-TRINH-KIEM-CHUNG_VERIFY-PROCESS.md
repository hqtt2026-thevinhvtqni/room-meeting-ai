# QUY TRÌNH KIỂM CHỨNG / VERIFY PROCESS
- **STT / Document ID:** DOC-047
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 47
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-008; DOC-009; DOC-014; DOC-015; DOC-019; DOC-033; DOC-038; DOC-046
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-047 quy định 06_VERIFY (Kiểm chứng): xác minh độc lập sản phẩm/deliverables có đáp ứng requirements, architecture, acceptance criteria, security, quality và operational expectations hay không; kết luận phải dựa trên test/inspection/analysis evidence có thể truy xuất và tái lập.

VERIFY không viết lại requirement, không tự sửa source thay implementer, không tự nghiệm thu thay Product Owner và không biến test pass cục bộ thành product acceptance. VERIFY ghi nhận kết quả thực tế, defect, residual risk, coverage gap và recommendation cho G6.

Top-level 06_EVIDENCE là sổ bằng chứng xuyên phase; 06_VERIFY chứa kế hoạch, quy trình, checklist và test specifications. Evidence chính thức phải được đăng ký tại 06_EVIDENCE theo DOC-014.

## 2. Điều kiện đầu vào

### 2.1 Entry criteria
- G5 BUILD → VERIFY đã PASS hoặc có authorization rõ theo DOC-004.
- Build handoff package và source/artifact versions được xác định.
- Requirements baseline, architecture baseline, plan/WP acceptance và verification scope được chốt.
- Test environment, test data, access, toolchain và dependencies sẵn sàng.
- Test cases có expected results, pass/fail criteria và evidence capture method.
- Reviewer/QE độc lập được chỉ định; xung đột lợi ích/self-review được khai báo.

Nếu G5 chưa PASS, chỉ được thực hiện test chuẩn bị hoặc exploratory test được ủy quyền; không tuyên bố phase VERIFY chính thức đã mở và không kết luận G6 PASS.

### 2.2 Nguyên tắc
1. Verify against approved criteria, not subjective impression.
2. Independence: người tạo deliverable không tự xác nhận độc lập deliverable đó.
3. Reproducibility: test có version, environment, steps, data và output.
4. Risk-based coverage: độ sâu test tương ứng impact/likelihood/uncertainty.
5. Positive and negative cases: kiểm tra cả happy path, boundary, error, permission và abuse.
6. Evidence integrity: kết quả gắn với đúng source commit, artifact, environment và timestamp.
7. Fail honestly: NOT RUN/SKIPPED/BLOCKED không phải PASS.
8. Defect transparency: không che giấu flaky test, known issue hoặc residual risk.
9. No scope drift: requirement thay đổi phải về DEFINE; design change theo ARCHITECT.
10. No gate inflation: G6 VERIFY không phải Product Acceptance (G7), Release (G8) hay Operations readiness (G9).

## 3. Đầu vào bắt buộc

- G5 decision, build handoff và exact source commit/artifact version.
- DOC-008 requirements baseline, DOC-009 architecture, ADR/contracts và acceptance criteria.
- DOC-011/WP baseline, DoD, risk register và known limitations.
- DOC-015 Verification Plan, DOC-019 Checklist và test specifications.
- DOC-014 Evidence Register/schema và evidence handling rules.
- Security/privacy/quality attribute scenarios, operational requirements.
- Test environment, test data, permissions, tool versions và external dependencies.

Mọi test target phải xác định chính xác Work/WP, source commit, artifact hash, configuration và environment. Không chạy trên “latest” không xác định.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Chốt acceptance intent, residual risk trọng yếu và G6 authority |
| Verification Lead / QE | Lập coverage, điều phối test độc lập, kết luận evidence và defect |
| Test Engineer | Thiết kế/thực thi test, lưu logs, reproduction và evidence |
| Implementer | Hỗ trợ reproduction/fix; không tự phê duyệt kết quả fix |
| Architect | Giải thích contract/design và đánh giá architecture deviation |
| Security/Privacy Reviewer | Kiểm tra threat/control và negative security cases |
| Operations Reviewer | Kiểm tra deployability, recovery, observability và support |
| Xu / AI-01 | Điều phối hồ sơ, traceability, gate pack; không tự thay independent QE |

## 5. Quy trình kiểm chứng — V01 đến V10

### V01 — Xác nhận test basis và target
- Xác định approved requirement/architecture/plan baseline và acceptance criteria.
- Xác định source commit, artifact hash, build provenance, config và environment.
- Kiểm tra G5, handoff completeness và unresolved deviations.
- Từ chối test target mơ hồ hoặc không khớp baseline; ghi blocker.
**Đầu ra:** Verification Intake & Test Basis.

### V02 — Phân tích rủi ro và coverage
- Map requirement → acceptance criteria → test case → evidence.
- Phân tích severity/likelihood, data sensitivity, external exposure và failure impact.
- Ưu tiên critical flows, authorization, data integrity, recovery và high-risk boundaries.
- Xác định test type, depth, sample size, performance load và independence level phù hợp.
**Đầu ra:** Coverage/Risk Matrix.

### V03 — Thiết kế test cases và expected results
Mỗi test case có:
- Test ID, linked requirement/WP/ADR/risk.
- Objective, preconditions, target version/environment.
- Input/test data, steps, expected result và measurable threshold.
- Positive/negative/boundary/failure category.
- Evidence capture, cleanup và pass/fail criteria.
- Owner, reviewer, automation/manual method.
**Đầu ra:** Test Case Catalogue.

### V04 — Xác nhận môi trường và test data
- Xác nhận environment parity, config, feature flags, dependencies và clock/timezone.
- Dùng synthetic/masked data khi phù hợp; hạn chế dữ liệu cá nhân.
- Kiểm tra permissions, test accounts, tenant/Work isolation và secret handling.
- Ghi tool/version, seed, dataset version và setup script.
- Nếu môi trường không đại diện, nêu limitation và không khái quát kết quả quá phạm vi.
**Đầu ra:** Test Environment & Data Record.

### V05 — Thực thi functional và integration verification
- Chạy unit/component/contract/integration/system/E2E theo scope.
- Kiểm tra state transitions, workflow, API schema, data ownership và compatibility.
- Thực hiện positive, negative, boundary, timeout, retry, duplicate và partial failure.
- Ghi từng test result, log, exit code, timestamps và exact target version.
**Đầu ra:** Functional/Integration Test Results.

### V06 — Security, privacy và resilience verification
- Kiểm tra authentication, authorization, privilege boundary, Work/tenant isolation và audit.
- Kiểm tra secret leakage, data minimization, retention/export/deletion theo scope.
- Thử unauthorized access, malformed input, replay, injection và abuse cases phù hợp.
- Kiểm tra timeout, unavailable dependency, stale/corrupt data, partial write, recovery và fail-closed behavior.
- Security testing chỉ thực hiện trong phạm vi được phép; không mở rộng thành hoạt động tấn công ngoài authorization.
**Đầu ra:** Security/Privacy/Resilience Results.

### V07 — Quality attributes và operational verification
- Kiểm tra performance/load/latency/throughput theo scenario và percentile đã duyệt.
- Kiểm tra availability, scalability, accessibility, usability, compatibility và maintainability khi có tiêu chí.
- Kiểm tra logging/metrics/tracing/alerts, backup/restore, RPO/RTO và runbook.
- Ghi rõ workload, hardware/runtime, warm-up, sample count và limitations.
**Đầu ra:** Quality & Operational Verification Results.

### V08 — Defect triage, retest và regression
- Mỗi defect có ID, severity, priority, reproduction, expected/actual, affected version và evidence.
- Phân loại defect, environment issue, flaky test, requirement ambiguity hoặc test gap.
- Fix do implementer thực hiện; QE retest độc lập.
- Regression scope dựa trên dependency/impact analysis.
- Không đóng defect bằng lời hứa; cần retest evidence hoặc waiver hợp lệ.
**Đầu ra:** Defect Register, Retest & Regression Report.

### V09 — Evidence validation và independent review
- Đăng ký evidence tại DOC-014: ID, type, URI/path, hash, producer, timestamp, environment, source version, verifier và status.
- Kiểm tra evidence completeness, integrity, reproducibility, relevance và freshness.
- Reviewer độc lập kiểm tra test selection, coverage, results, defect disposition và residual risk.
- RECORDED không đồng nghĩa VERIFIED; evidence thiếu provenance hoặc hash khi bắt buộc phải đánh dấu chưa xác minh.
**Đầu ra:** Verified Evidence Set và Independent QE Report.

### V10 — G6 review và handoff sang ACCEPT
- Tổng hợp coverage, pass/fail/not-run, defects, limitations và residual risks.
- Đối chiếu G6 criteria trong DOC-004.
- Product Owner/authorized authority quyết định PASS/NOT READY/BLOCKED/WAIVED.
- Chỉ khi G6 PASS mới handoff chính thức sang 07_ACCEPT.
**Đầu ra:** G6 Gate Review Record và Verification Summary.

## 6. Test result vocabulary

- **PASS:** test chạy đúng target/environment, expected result đạt, evidence đủ.
- **FAIL:** test chạy hợp lệ và actual result không đạt expected/threshold.
- **BLOCKED:** không thể chạy do prerequisite, permission, dependency hoặc environment.
- **NOT RUN:** chưa thực thi.
- **SKIPPED:** có lý do được ghi và scope ảnh hưởng xác định.
- **FLAKY:** kết quả không ổn định; chưa được tính PASS cho đến khi nguyên nhân và policy được xử lý.
- **NOT APPLICABLE:** có rationale và authority/reviewer xác nhận applicability.
- **WAIVED:** tiêu chí được miễn bởi đúng authority, có residual risk, scope và expiry/review date.

Không gộp các trạng thái trên thành một tỷ lệ PASS duy nhất mà che khuất NOT RUN/BLOCKED/FLAKY.

## 7. Evidence quality requirements

Evidence record cần có:
- Evidence ID và loại (test log, screenshot, trace, report, artifact, source inspection...).
- Work/WP/requirement/test IDs liên quan.
- Producer, verifier, timestamp và authority nếu có.
- Source commit/artifact version/hash.
- Environment/config/tool version.
- URI/path, integrity hash và retention/access classification.
- Result/status, limitations và reproducibility steps.

Không lưu secrets hoặc dữ liệu cá nhân không cần thiết. Screenshot đơn lẻ không thay thế logs/test metadata khi cần xác minh hành vi. Dashboard display hoặc AI summary không phải bằng chứng gốc nếu không dẫn tới artifact kiểm chứng được.

## 8. G6 — Gate VERIFY → ACCEPT

Điều kiện tối thiểu:
- [ ] G5 PASS và test basis/version rõ.
- [ ] Coverage map bao phủ requirements/acceptance bắt buộc và risk trọng yếu.
- [ ] Functional, integration, negative, boundary và failure tests được chạy theo scope.
- [ ] Security/privacy/resilience controls được kiểm tra theo risk.
- [ ] Quality/operational criteria có kết quả hoặc limitation được chấp nhận.
- [ ] Test results có exact source/artifact/environment provenance.
- [ ] Defects có severity, owner, disposition và retest; không có blocker không được chấp thuận.
- [ ] Evidence Register đầy đủ, integrity/freshness được kiểm tra.
- [ ] Independent QE report và review findings được ghi nhận.
- [ ] Residual risks, known limitations và NOT RUN/SKIPPED/BLOCKED được công khai.
- [ ] Product Owner/authorized authority ghi G6 decision theo DOC-004.

Trạng thái:
- **PASS:** tiêu chí bắt buộc đạt và authority decision có evidence.
- **NOT READY:** thiếu test/evidence có thể hoàn thiện.
- **BLOCKED:** thiếu môi trường, dependency, permission hoặc decision.
- **FAIL:** verification cho thấy không đáp ứng acceptance/quality.
- **WAIVED:** chỉ theo DOC-004, đúng authority, rationale, scope, residual risk và expiry/review date.

G6 PASS là xác nhận verification scope đã đạt, không thay thế G7 Product Acceptance.

## 9. Handoff sang 07_ACCEPT

- Approved requirement/architecture/plan references.
- G5/G6 decision records.
- Verification Summary, Coverage Matrix và Independent QE Report.
- Test Case Catalogue và test execution results.
- Evidence Register references và integrity information.
- Defect Register, retest/regression results và waivers.
- Security/privacy/operational results.
- Known limitations, residual risks và NOT RUN/SKIPPED/BLOCKED list.
- Reproduction instructions, exact artifacts/commits và recommendation.
- Items requiring Product Owner acceptance decision.

## 10. Checklist thực hiện

- [ ] V01 test basis/target.
- [ ] V02 risk and coverage.
- [ ] V03 test design/expected results.
- [ ] V04 environment/data.
- [ ] V05 functional/integration.
- [ ] V06 security/privacy/resilience.
- [ ] V07 quality/operations.
- [ ] V08 defects/retest/regression.
- [ ] V09 evidence integrity/independent review.
- [ ] V10 G6/handoff.
- [ ] Update DOC-014, DOC-015, DOC-019, journal and gate records.

## 11. Hướng dẫn AI tham gia VERIFY

1. Đọc DOC-001/002/004/005, DOC-008/009, DOC-014/015/019, DOC-046/047 và target WP.
2. Xác nhận G5 và exact target trước khi test.
3. Không tự kiểm chứng độc lập sản phẩm do mình triển khai.
4. Không sửa expected result để làm test PASS nếu chưa có requirement change approval.
5. Ghi command, environment, exit code, logs và evidence.
6. Không tính NOT RUN/BLOCKED/SKIPPED/FLAKY là PASS.
7. Không dùng screenshot/summary thay cho evidence gốc khi cần.
8. Phân biệt defect, requirement ambiguity, environment issue và test gap.
9. Không che giấu counter-evidence hoặc residual risk.
10. Không tự phê duyệt G6/acceptance.

## 12. Ví dụ minh họa (giả định)

Một endpoint đọc Work status cần test caller không đăng nhập (401), không có quyền (403), Work không tồn tại/không được phép tiết lộ (404 theo policy), cross-Work access, stale response, timeout và response provenance. Chỉ khi test chạy trên exact build với logs và independent review mới được kết luận theo phạm vi. Ví dụ này không xác nhận endpoint thực tế của Work 70 đã tồn tại.

## 13. Kiểm soát và thay đổi

DOC-047 là chuẩn quy trình. Vinh giữ authority đối với G6 và residual risk trọng yếu. QE/Verifier chịu trách nhiệm kết quả kiểm chứng độc lập; Xu điều phối hồ sơ và handoff, không tự thay QE hoặc Product Owner.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành V01–V10, risk-based verification, evidence integrity, independent QE, G6 and handoff standard. |
