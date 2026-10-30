# QUY TRÌNH PHÁT HÀNH / RELEASE PROCESS
- **STT / Document ID:** DOC-050
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 50
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-014; DOC-020; DOC-021; DOC-033; DOC-038; DOC-048; DOC-049
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.1 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-050 quy định 08_RELEASE (Phát hành): chuẩn bị, phê duyệt, triển khai và xác minh một release có kiểm soát từ sản phẩm đã được nghiệm thu. RELEASE quản lý version, package, deployment, rollout, rollback, communication và post-release checks.

G7 ACCEPT là điều kiện đầu vào; G7 RELEASE là quyết định phát hành riêng. ACCEPTED không tự động có nghĩa RELEASED. Một release chỉ được công bố sau khi có authority approval và deployment evidence.

Nếu sản phẩm chỉ là prototype/reference design hoặc chưa có production environment, ghi rõ NOT RELEASED; không dựng release record giả để hoàn tất checklist.

## 2. Điều kiện đầu vào

- G7 ACCEPT PASS hoặc quyết định acceptance hợp lệ theo DOC-004.
- DOC-020 Acceptance Record có scope, version, authority và evidence.
- DOC-021 Release Plan được cập nhật cho release candidate cụ thể.
- Release artifact/version/commit/hash/provenance xác định.
- Deployment target/environment, owner, access và configuration đã xác minh.
- Security review, secret scan, dependency/license review và operational readiness phù hợp scope.
- Backup/restore, rollback, smoke test, monitoring và incident escalation đã chuẩn bị.
- Outstanding defects, waivers, residual risks và communication obligations được chấp thuận.

Thiếu acceptance hoặc production target thì chỉ được lập release preparation plan; không được tuyên bố release approved/deployed.

## 3. Nguyên tắc

1. No acceptance, no production release.
2. Immutable release identity: version, source commit, artifact hash và build provenance phải cố định.
3. Reproducible deployment: configuration, procedure và environment được version/ghi nhận.
4. Least privilege: deploy credentials và approvals được kiểm soát.
5. Progressive rollout: canary/staged rollout khi phù hợp risk.
6. Rollback first: tiêu chí và cách rollback phải xác định trước.
7. Observe after deploy: smoke/health/metrics/logs sau triển khai.
8. Explicit communication: người dùng/owner biết thay đổi, downtime và limitation.
9. No silent hotfix: emergency changes vẫn phải có audit, review và post-incident reconciliation.
10. No false release claim: tag/merge/package creation không đồng nghĩa production deployment.

## 4. Vai trò

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Phê duyệt G7, scope và risk/exception trọng yếu |
| Release Manager | Điều phối release candidate, checklist, approvals và communication |
| Engineering/Platform Owner | Build/deploy, configuration, rollback và technical evidence |
| Security Reviewer | Security posture, secret/dependency scan và residual risk |
| Operations Owner | Monitoring, incident response, support và runbook readiness |
| QE | Xác nhận acceptance/verification evidence và smoke/regression scope |
| Xu / AI-01 | Điều phối hồ sơ, release traceability và handoff; không tự approve G7 |

## 5. Quy trình — R01 đến R10

### R01 — Xác định release scope
- Xác định release ID/version, target audience, product components và included changes.
- Link G7 acceptance record, source commits, artifacts và exclusions.
- Ghi compatibility, migration và external dependency.
**Đầu ra:** Release Scope & Candidate Identity.

### R02 — Tạo release candidate và provenance
- Build/package từ exact approved commit/tag.
- Ghi hash, build run, toolchain, dependency lock, SBOM (nếu policy yêu cầu) và provenance.
- Không chỉnh sửa artifact sau khi hash/approval; rebuild tạo candidate mới.
**Đầu ra:** Release Candidate Manifest.

### R03 — Kiểm tra release readiness
- Xác nhận acceptance, QE, defect disposition, security/privacy, license/compliance và documentation.
- Kiểm tra config/secrets, permissions, capacity, data migration và external service readiness.
- Kiểm tra support owner, monitoring, alerting và incident runbooks.
**Đầu ra:** Release Readiness Review.

### R04 — Lập deployment và rollout plan
- Xác định deployment steps, order, windows, expected duration và dependencies.
- Chọn rolling/canary/blue-green/full rollout theo risk.
- Xác định health checks, success thresholds, pause/abort conditions và stakeholder communication.
**Đầu ra:** Deployment/Rollout Plan.

### R05 — Chuẩn bị backup và rollback
- Xác định backup/snapshot, restore test, rollback artifact/config/data strategy.
- Nêu rõ rollback triggers, decision owner, maximum recovery time và verification.
- Data migration/destructive changes cần backward compatibility hoặc explicit recovery path.
**Đầu ra:** Backup/Rollback Plan & Evidence.

### R06 — G7 approval
- Tổng hợp acceptance, candidate manifest, readiness, deployment, rollback và residual risk.
- Reviewer xác nhận; Product Owner/authorized authority quyết định G7.
- Không deploy production trước approval trừ emergency procedure đã được policy cho phép và audit.
**Đầu ra:** G7 Release Authorization.

### R07 — Deploy và rollout
- Deploy đúng approved artifact/config/environment.
- Ghi actor, approvals, start/end, commands/tool, deployment ID và logs.
- Theo dõi rollout thresholds; pause/abort khi trigger xảy ra.
- Không ghi production nếu target chỉ là local/dev/staging.
**Đầu ra:** Deployment Execution Record.

### R08 — Smoke test và post-deploy verification
- Kiểm tra health, core flows, access controls, data integrity và integrations.
- Đối chiếu deployed version/hash với approved candidate.
- Theo dõi error rate, latency, availability và alerts trong observation window.
- Ghi pass/fail và rollback decision.
**Đầu ra:** Post-Deployment Verification.

### R09 — Release closeout và communication
- Công bố release notes, known limitations, migration/support guidance và incident contact.
- Lưu release record, artifacts, approvals, evidence và communication.
- Ghi release state: RELEASED, PARTIAL, ROLLED_BACK, CANCELLED hoặc NOT RELEASED.
**Đầu ra:** Release Record & Communication Log.

### R10 — Handoff sang OPERATE
- Bàn giao owner, runbooks, SLO/SLI, dashboards, alert routing, backup, retention và support model.
- Xác nhận Operations Owner/backup đã nhận trách nhiệm.
- Theo dõi hypercare/early-life support nếu cần.
**Đầu ra:** Operations Handoff Package.

## 6. G7 — Gate ACCEPT → RELEASE

- [ ] G7 ACCEPT PASS và DOC-020 decision được xác minh.
- [ ] Release scope/version/candidate exact identity rõ.
- [ ] Artifact hash/provenance gắn với approved source commit.
- [ ] Security/privacy/license/compliance checks phù hợp scope.
- [ ] Deployment target, config, permissions và owner sẵn sàng.
- [ ] Backup/restore/rollback được thiết kế và kiểm chứng phù hợp risk.
- [ ] Rollout thresholds, pause/abort triggers và smoke tests xác định.
- [ ] Monitoring/alerting/incident/support readiness được xác nhận.
- [ ] Defects/waivers/residual risks được authority chấp nhận.
- [ ] Release communication và operations handoff plan sẵn sàng.
- [ ] Product Owner/authorized authority ghi G7 approval.

G7 trạng thái: PASS / NOT READY / BLOCKED / CANCELLED / WAIVED theo DOC-004. Chỉ G7 PASS mới cho phép release trong scope được duyệt.

## 7. Release record tối thiểu

- Release ID, semantic/version label, date/time và status.
- Product scope, audience, environment/region.
- Acceptance/G7 reference và G7 approval.
- Source commit/tag, artifact URI/hash, build provenance.
- Deployment config/version, actor, tool/run ID và logs.
- Backup/rollback reference và outcome.
- Smoke/post-deploy test results.
- Monitoring observation window và anomalies.
- Release notes, known limitations, waivers và residual risks.
- Operations Owner, handoff confirmation và support channel.

## 8. Rollback và emergency release

Rollback bắt buộc khi trigger đã định nghĩa xảy ra: critical security/data issue, failed health threshold, data corruption, unauthorized behavior hoặc service degradation vượt ngưỡng.
- Người quyết định rollback và người thực hiện phải được chỉ định.
- Ghi artifact/config/data version trước và sau rollback.
- Kiểm tra data consistency và service health sau rollback.
- Mở incident/postmortem và corrective action.
Emergency release chỉ theo policy có sẵn, có authority, scope/time limit, audit và post-release review; không dùng emergency label để né G7.

## 9. AI instructions

- Không tuyên bố RELEASED khi chưa có deployment evidence đúng production target.
- Không tự tạo version/tag hoặc approval thay authority.
- Không tiết lộ secrets trong logs/release notes.
- Không deploy nếu acceptance, permission hoặc rollback prerequisite thiếu.
- Ghi exact artifact hash, commit, environment và deployment run.
- Nếu tool/permission bị chặn, ghi BLOCKED và dừng; không tìm đường vượt kiểm soát.

## 10. Ví dụ minh họa (giả định)

Một bản Dashboard được tag và deploy lên staging chưa phải production release. Release record phải phân biệt candidate, staging deployment và production deployment; chỉ khi G7 được duyệt, đúng artifact được triển khai production và post-deploy verification có evidence mới được ghi RELEASED. Đây là ví dụ phương pháp.

## 11. Kiểm soát và thay đổi

DOC-050 là chuẩn quy trình. Vinh giữ authority G7. Release Manager/Operations/Engineering chịu trách nhiệm execution trong phạm vi; Xu điều phối và ghi nhận, không tự phê duyệt hoặc tuyên bố production release.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-10-30 | Xu / AI-01 | Align release gate with DOC-004: G7 ACCEPT→RELEASE. |
| 1.0 | 2026-10-30 | Ban hành R01–R10, release candidate, readiness, rollout, rollback, G7 and operations handoff. |
