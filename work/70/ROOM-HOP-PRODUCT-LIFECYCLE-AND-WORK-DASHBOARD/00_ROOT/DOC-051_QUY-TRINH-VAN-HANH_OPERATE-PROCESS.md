# QUY TRÌNH VẬN HÀNH / OPERATE PROCESS
- **STT / Document ID:** DOC-051
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 51
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-014; DOC-022; DOC-033; DOC-038; DOC-048; DOC-050
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.1 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-051 quy định 09_OPERATE (Vận hành): tiếp nhận sản phẩm đã phát hành, duy trì dịch vụ an toàn/ổn định, giám sát mục tiêu vận hành, xử lý sự cố, quản lý thay đổi và cải tiến dựa trên dữ liệu thực tế.

OPERATE chỉ được mở chính thức sau G8 RELEASE PASS và operations handoff được xác nhận. Tài liệu mô hình vận hành hoặc kế hoạch monitoring không chứng minh monitoring/alerting/backup thực tế đã chạy.

OPERATE quản lý hoạt động sau phát hành; thay đổi sản phẩm lớn quay lại DISCOVER/DEFINE/ARCHITECT/PLAN theo nature. Không tự sửa requirements, kiến trúc hoặc release scope ngoài change control.

## 2. Điều kiện đầu vào

- G8 RELEASE PASS và release record xác định đúng production version/environment.
- DOC-022 Operations Model được cụ thể hóa cho release.
- Named Operations Owner và backup, escalation path và support coverage.
- Runbooks, dashboards, alerts, access controls và incident procedures sẵn sàng.
- SLO/SLI, thresholds, freshness, retention, backup/restore và capacity limits được định nghĩa hoặc TBD có owner.
- Security/privacy, audit, data retention/deletion và vendor responsibilities rõ.
- Operations handoff package, release notes và known limitations đã nhận.

Nếu chưa có production deployment hoặc owner/runbook/monitoring, trạng thái là NOT ACTIVE / PRE-OPERATIONS; không giả định OPERATE đã bắt đầu.

## 3. Nguyên tắc

1. Service ownership: mọi production service có owner và backup.
2. Observe reality: trạng thái dựa trên telemetry/incident evidence, không suy đoán.
3. SLO-led: theo dõi user-facing reliability/quality objectives đã duyệt.
4. Least privilege: access, secrets và operational actions theo role.
5. Incident transparency: ghi severity, impact, timeline, communication và remediation.
6. Resilience: backup/restore, recovery và rollback phải được kiểm chứng định kỳ.
7. Change safety: production change có approval, risk, rollout và rollback.
8. Data governance: retention, deletion, export và privacy được thực thi theo policy.
9. Continuous improvement: incidents, feedback và usage signals quay lại Discover.
10. No false operational claims: dashboard/runbook tồn tại không chứng minh alert/backup/restore đang hoạt động.

## 4. Vai trò

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Quyết định thay đổi sản phẩm/risk trọng yếu và ưu tiên cải tiến |
| Operations Owner | Chịu trách nhiệm service health, incident, access, backup và handoff |
| Backup Operations Owner | Thay thế theo escalation/on-call policy |
| SRE/Platform | Reliability, monitoring, capacity, deployment, recovery |
| Security/Privacy Owner | Security events, access review, incident/privacy obligations |
| Support/Customer Owner | Tiếp nhận user impact, communication và feedback |
| Engineering Owner | Defect fix, change implementation và technical root cause |
| Xu / AI-01 | Điều phối lifecycle learning, record và follow-up; không tự thay Operations Owner |

## 5. Quy trình vận hành — O01 đến O10

### O01 — Tiếp nhận service và xác nhận readiness
- Xác nhận G8, release version, environment, service boundary và dependencies.
- Kiểm tra owner/backup, runbooks, dashboards, alerts, credentials/access và support contacts.
- Xác nhận SLO/SLI, error budget hoặc ghi TBD/owner/target date.
- Kiểm tra handoff completeness và open risks.
**Đầu ra:** Operational Acceptance/Handoff Record.

### O02 — Theo dõi service health và SLO
- Theo dõi availability, latency, error rate, throughput, saturation và user journey metrics khi phù hợp.
- Theo dõi freshness, missing/stale evidence, data integrity và access denials.
- Định nghĩa thresholds, alert routing, noise control và escalation.
- Phân biệt telemetry gap với service healthy; thiếu metrics không có nghĩa không có lỗi.
**Đầu ra:** Service Health/SLO Dashboard & Alert Records.

### O03 — Incident detection, triage và response
- Nhận alert/report, tạo Incident ID và xác định severity.
- Ghi impact, affected users/data/services, start time, detection time và current status.
- Assign Incident Commander/owner, technical responders và communications owner.
- Thực hiện containment, mitigation, rollback hoặc failover theo runbook.
- Cập nhật stakeholders theo cadence/severity policy.
**Đầu ra:** Incident Record & Timeline.

### O04 — Recovery và service restoration
- Xác định recovery objective, data consistency và dependencies.
- Thực hiện restore/failover/rollback đã được duyệt.
- Kiểm tra health, integrity, access và user-facing flows sau recovery.
- Ghi actual recovery time, data loss (nếu có), gaps và residual risk.
**Đầu ra:** Recovery Verification Record.

### O05 — Problem management và root-cause analysis
- Phân biệt symptom, trigger, root cause và contributing factors.
- Dùng timeline/logs/traces/metrics/deployment history.
- Xác định corrective/preventive actions, owners, due dates và validation criteria.
- Không quy lỗi cho cá nhân khi chưa có evidence; ưu tiên system causes.
**Đầu ra:** Post-Incident Review / Problem Record.

### O06 — Change/configuration management
- Mọi production change có Change ID, reason, scope, risk, approver và test evidence.
- Phân loại standard/normal/emergency change theo policy.
- Kiểm soát configuration, secrets, dependencies, access và drift.
- Thực hiện staged rollout, monitoring và rollback triggers.
- Emergency change phải audit và review sau thực hiện.
**Đầu ra:** Change Record & Configuration History.

### O07 — Capacity, cost và vendor management
- Theo dõi resource utilization, growth, quotas, storage, cost và forecast.
- Xác định capacity thresholds và scaling/optimization actions.
- Theo dõi vendor/service dependencies, SLA, expiry, contract and support.
- Escalate khi cost/availability/contract vượt ngưỡng đã duyệt.
**Đầu ra:** Capacity/Cost/Dependency Review.

### O08 — Security, privacy, backup và compliance operations
- Access review, credential rotation, vulnerability/patch management và audit.
- Theo dõi security/privacy incidents và retention/deletion obligations.
- Backup theo schedule; restore test định kỳ; ghi backup coverage và integrity.
- Kiểm tra export/access logs, data lifecycle và regulatory controls khi áp dụng.
- Báo cáo exception và residual risk.
**Đầu ra:** Security/Privacy/Backup Operations Evidence.

### O09 — User feedback và product learning
- Thu thập support tickets, feedback, usage patterns, accessibility issues và churn/adoption signals.
- Tách observation, anecdote, metric và causal inference.
- Xác định recurring pain points và opportunities.
- Tạo input cho 01_DISCOVER, không biến một incident đơn lẻ thành requirement nếu chưa đánh giá.
**Đầu ra:** Operational Learning Backlog / Discover Intake.

### O10 — Periodic review và lifecycle continuation
- Review SLO, incidents, defects, capacity, security, cost, vendor and user outcomes theo cadence.
- Đánh giá end-of-life, deprecation, migration và data retention.
- Quyết định continue, improve, re-architect, migrate, retire hoặc restart lifecycle.
- Mọi quyết định có owner, rationale, evidence và change history.
**Đầu ra:** Operations Review & Lifecycle Decision.

## 6. Incident severity và communication

Mỗi Work/service phải định nghĩa severity levels, ví dụ:
- SEV1: critical outage, major data/security impact hoặc widespread user harm.
- SEV2: significant degradation hoặc high-impact feature unavailable.
- SEV3: limited impact, workaround available.
- SEV4: minor issue/request.

Các ngưỡng, response time, communication cadence và escalation phải được Product/Operations Owner phê duyệt theo service context; ví dụ severity không tự tạo SLA cam kết.

Incident record tối thiểu: ID, severity, impact, timestamps, detection source, owner, timeline, actions, communications, recovery, evidence, root cause, corrective actions và closure authority.

## 7. Operational evidence

Đăng ký evidence tại DOC-014 theo DOC-048:
- Monitoring/alert events, SLO reports, traces, logs và health checks.
- Backup job, restore test, integrity checks và retention.
- Incident/change/postmortem records.
- Access/security review, vulnerability/patch records.
- Capacity/cost/vendor reviews.
- User feedback/usage data đã được phân loại và privacy-reviewed.

Mỗi record có environment, version, period, producer, verifier, integrity và scope. Không ghi VERIFIED chỉ vì dashboard hiển thị xanh.

## 8. G8 — Gate RELEASE → OPERATE

- [ ] G8 RELEASE PASS và production deployment exact version được xác minh.
- [ ] Operations Owner/backup và service boundaries được xác nhận.
- [ ] Runbooks, dashboards, alert routing và escalation được kiểm tra.
- [ ] SLO/SLI, thresholds và observation windows được duyệt.
- [ ] Incident response/communications và recovery/rollback có owner.
- [ ] Backup/restore và data integrity evidence phù hợp risk.
- [ ] Security/privacy/access/retention controls đã bàn giao.
- [ ] Capacity/cost/vendor dependencies có owner.
- [ ] Known limitations, open risks và support obligations được chấp nhận.
- [ ] Operations handoff record được xác nhận bởi receiving owner.
- [ ] Authority ghi G8 decision theo DOC-004.

G8 trạng thái: PASS / NOT READY / BLOCKED / WAIVED. Nếu không có production deployment, trạng thái OPERATE là NOT ACTIVE.

G9 trong DOC-004 là periodic OPERATE → improvement review, không phải gate mở phase OPERATE. O10 cung cấp đầu ra và bằng chứng cho đánh giá G9; decision/learning record phải được ghi nhận theo authority tương ứng.

## 9. Change, incident và retirement control

- Incident không tự động cho phép thay đổi requirement/architecture; remediation đi qua change control tương ứng.
- Emergency change phải ghi authorization, impact, evidence và post-review.
- Data deletion/retention phải tuân policy và legal hold; không tự xóa để dọn hệ thống.
- Retirement/decommission cần owner approval, user communication, dependency migration, backup/archive, credential revocation, DNS/infrastructure cleanup và evidence preservation.
- End-of-life decision có thể khởi động lại DISCOVER cho sản phẩm thay thế.

## 10. AI instructions

1. Không tự nhận service đang operational nếu thiếu production telemetry/evidence.
2. Không tự thực hiện production change, rollback, access grant hoặc data deletion ngoài authorization.
3. Không hiển thị secrets/PII trong logs hoặc summaries.
4. Tách alert, observation, root cause và hypothesis.
5. Ghi incident timeline và evidence references; không sửa lịch sử.
6. Không tuyên bố SLO đạt khi thiếu telemetry/measurement window.
7. Escalate security/data integrity incidents theo runbook.
8. Dùng operational learning làm đầu vào Discover, không tự biến thành scope commitment.
9. Khi tool/permission bị chặn, ghi BLOCKED; không vòng qua policy.
10. Ghi rõ NOT ACTIVE nếu chưa có G8/deployment/handoff.

## 11. Ví dụ minh họa (giả định)

Một dashboard có thể có giao diện hiển thị health xanh nhưng không có alert pipeline hoặc backup restore test. OPERATE review phải ghi monitoring/backup chưa được xác minh, không tuyên bố service operational-ready. Ví dụ này minh họa nguyên tắc, không phải mô tả runtime Work 70.

## 12. Kiểm soát và thay đổi

DOC-051 là chuẩn quy trình. Operations Owner chịu trách nhiệm vận hành thực tế; Vinh quyết định product/risk trọng yếu; Xu điều phối records và learning loop, không thay thế người trực vận hành hoặc authority.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-10-30 | Xu / AI-01 | Align operations entry gate with DOC-004: G8 RELEASE→OPERATE; G9 is periodic operational improvement review. |
| 1.0 | 2026-10-30 | Xu / AI-01 | Ban hành O01–O10, service health, incidents, recovery, changes, security, learning, G8 and retirement standard. |
