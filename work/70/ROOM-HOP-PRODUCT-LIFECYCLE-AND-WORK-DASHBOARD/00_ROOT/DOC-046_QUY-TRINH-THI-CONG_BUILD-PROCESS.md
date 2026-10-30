# QUY TRÌNH THI CÔNG / BUILD PROCESS
- **STT / Document ID:** DOC-046
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 46
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-009; DOC-011; DOC-033; DOC-036; DOC-038; DOC-044; DOC-045
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-046 quy định cách thực thi 05_BUILD (Thi công): nhận WP đã được lập kế hoạch và cho phép thực thi, triển khai thay đổi trong đúng canonical source repository, kiểm soát code/artifact, review, CI, integration và bàn giao sang VERIFY.

05_BUILD là lớp điều phối/mapping kỹ thuật, không phải nguồn kế hoạch WP cấp Work và không phải canonical source repository mặc định. Kế hoạch WP thuộc 04_PLAN. Source code, tests và artifact gốc thuộc repository/path được khai báo trong Manifest hoặc controlled artifact register. Branch work/70/05-build chỉ là branch mapping/engineering coordination cho Work 70; không được suy diễn thành nơi lưu source chuẩn.

DOC-046 không cho phép thực thi nếu G4 chưa PASS hoặc WP chưa READY/DoR. Không có quyền tự mở gate, tự thay đổi requirement/architecture baseline hay tự xác nhận nghiệm thu.

## 2. Điều kiện đầu vào và nguyên tắc

### 2.1 Entry criteria
- G4 PLAN → BUILD PASS bởi Product Owner/authorized authority.
- DOC-011/WP plan baseline version được xác định.
- WP ở READY, DoR đạt, owner và independent reviewer được chỉ định.
- Requirements/architecture baseline, interface contracts, ADR và security constraints liên quan được xác định.
- Canonical source repository/path, branch/ref strategy và permissions đã xác minh.
- Acceptance/DoD, test strategy, evidence location và rollback approach xác định.
- Dependency, environment, credentials/secrets, test data và external approvals sẵn sàng.

Nếu thiếu G4 hoặc DoR, chỉ được chuẩn bị tài liệu, prototype/spike được ủy quyền rõ; không đánh dấu execution WP là IN_PROGRESS và không ghi nhận BUILD chính thức.

### 2.2 Nguyên tắc
1. Plan before build: chỉ thực thi WP có trong 04_PLAN approved baseline.
2. Canonical source only: sửa source tại repo/path đã khai báo; 05_BUILD chỉ map.
3. Least privilege: mỗi actor/adapter chỉ có quyền tối thiểu trong WP scope.
4. Small, traceable changes: commit/PR liên kết WP, requirement, ADR và issue.
5. Tests are executable evidence: test phải chạy thật trong môi trường xác định; không fake PASS.
6. Independent review: implementer không tự duyệt thay reviewer.
7. Fail closed: thiếu permission, contract, dependency hoặc test evidence thì dừng/giữ BLOCKED.
8. Reproducibility: ghi commit, toolchain, environment, commands, logs và artifacts.
9. No hidden scope: phát sinh ngoài baseline phải có change request.
10. No gate inflation: merge/CI green không đồng nghĩa WP DONE, G5 PASS, acceptance hoặc release.

## 3. Đầu vào bắt buộc
- Approved DOC-011/WP baseline, G4 decision và WP ID.
- WP scope, objective, owner, reviewer, dependencies, DoR/DoD.
- DOC-008 requirements, DOC-009 architecture, contracts, ADRs và security controls.
- Canonical source repository/path, branch protection, review policy và build/test instructions.
- Test plan, test data, environment, secrets handling và evidence path.
- Risk, rollback/recovery plan, integration/deployment constraints.
- Mapping record trong DOC-036 hoặc approved mapping register.

## 4. Vai trò và trách nhiệm

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Quyết định thay đổi scope/trade-off trọng yếu, gate và ngoại lệ |
| Build Coordinator (Xu / AI-01) | Điều phối WP, mapping, dependencies, execution records và handoff |
| WP Owner | Chịu trách nhiệm deliverable, progress, blockers, quality và evidence |
| Implementer / Coder | Thực hiện thay đổi tại canonical source, tests, commit/PR và technical log |
| Independent Reviewer | Review diff, design, tests, security và acceptance evidence |
| QE / Tester | Thực thi kiểm thử độc lập, xác nhận kết quả và defect disposition |
| Architect | Xử lý ADR/architecture impact và contract deviations |
| Repo/Platform Owner | Cấp quyền, branch policy, CI environment, secrets và deployment controls |

AI/adapter chỉ thực hiện action được permission/tool thực tế cho phép. Không ghi nhận “AI đã làm” chỉ dựa trên roster hoặc lời khẳng định; cần commit, tool result, log hoặc evidence tương ứng.

## 5. Quy trình thực thi — B01 đến B10

### B01 — Nhận và xác minh WP
- Đối chiếu WP ID, approved plan version, G4 decision và READY status.
- Kiểm tra DoR, scope, outputs, owner/reviewer, dependency và acceptance.
- Xác nhận canonical source repo/path/branch/ref và permission.
- Nếu WP hoặc source mapping không khớp, dừng và tạo finding.
**Đầu ra:** Build Intake Record.

### B02 — Chuẩn bị môi trường và execution branch
- Xác nhận toolchain/version, environment, dependency lock và reproducible setup.
- Xác nhận branch/PR strategy, protection, required checks và rollback.
- Kiểm tra secrets qua secret manager/approved channel; không đưa vào source, prompt hoặc log.
- Ghi baseline commit/ref trước khi sửa.
**Đầu ra:** Environment & Baseline Record.

### B03 — Phân rã task và implementation approach
- Chia WP thành tasks có outcome, owner, acceptance và dependency.
- Liên kết task với requirements, architecture components, contracts và ADR.
- Xác định test-first/contract-first, migration, feature flag hoặc compatibility strategy.
- Nếu cần spike, timebox và mục tiêu học tập phải được duyệt; spike không tự thành production implementation.
**Đầu ra:** Task Breakdown & Implementation Notes.

### B04 — Thực hiện thay đổi có kiểm soát
- Sửa đúng canonical repository/path.
- Tuân thủ architecture, coding standards, security controls và interface contracts.
- Mỗi thay đổi liên kết WP/task/requirement/ADR.
- Không sửa file ngoài scope hoặc ghi đè thay đổi không rõ ownership.
- Ghi commit nhỏ, meaningful; không chứa secrets/generated clutter không cần thiết.
**Đầu ra:** Source changes/commits và execution log.

### B05 — Test tại chỗ và kiểm tra chất lượng
- Thực thi unit/component/static/type/lint/schema/contract tests theo WP.
- Test phải có command, tool/version, environment, exit code và output.
- Phân biệt NOT RUN, SKIPPED, BLOCKED, FAIL và PASS.
- Nếu test framework thiếu hoặc test không chạy, ghi BLOCKED/NOT RUN; không thay bằng giả định.
- Kiểm tra regression và negative cases.
**Đầu ra:** Test Run Records và defect list.

### B06 — Review độc lập và sửa findings
- Reviewer kiểm tra diff, traceability, design, error handling, security, tests và maintainability.
- Findings có ID, severity, owner, disposition và evidence retest.
- Người viết không tự đóng finding cần independent verification.
- Thay đổi architecture/contract phải có ADR/ACR và approval trước khi tiếp tục.
**Đầu ra:** Review Record và resolved/open findings.

### B07 — CI, integration và build artifact
- Chạy CI bắt buộc trên branch/PR; xác minh đúng commit SHA và workflow run.
- Thực hiện integration/contract tests với dependency thật hoặc test double được khai báo rõ.
- Artifact build ghi version, hash, provenance, toolchain và source commit.
- Không coi badge/summary hoặc CI của commit khác là evidence cho commit hiện tại.
**Đầu ra:** CI/Integration Evidence và Build Artifact Manifest.

### B08 — Mapping và evidence registration
- Cập nhật DOC-036/05_BUILD mapping: WP → build area → canonical source path → exact branch/ref/commit.
- Đăng ký cross-phase evidence tại top-level 06_EVIDENCE theo DOC-014.
- 05_BUILD/06_EVIDENCE chỉ là staging; evidence chính thức phải có canonical reference.
- Working copy phải ghi TEMPORARY, source version/hash và cleanup condition.
**Đầu ra:** Verified Mapping Update và Evidence References.

### B09 — WP review và Definition of Done
- Đối chiếu toàn bộ deliverables/acceptance/DoD.
- Kiểm tra tests, review findings, CI, security, documentation, mapping và evidence.
- Reviewer xác nhận độc lập; WP Owner đề xuất DONE.
- Nếu còn blocker/critical finding, WP giữ BLOCKED/IN_REVIEW; không hạ tiêu chí.
**Đầu ra:** WP Completion Candidate và reviewer disposition.

### B10 — Handoff sang VERIFY
- Gói source commit/PR, build artifacts, test records, CI run, review findings, risks và evidence.
- Ghi known limitations, deferred defects, environment/configuration và reproduction steps.
- Chỉ đánh dấu WP DONE khi DoD đạt; phase BUILD chỉ đóng theo gate DOC-004 sau khi đủ các WP/criteria.
- VERIFY thực hiện xác minh độc lập ở phạm vi system/acceptance; BUILD không tự nghiệm thu sản phẩm.
**Đầu ra:** Build Handoff Package.

## 6. Execution record tối thiểu

Mỗi execution event ghi:
- Work ID, WP ID, task ID và baseline version.
- Actor/AI ID, role, authorization scope.
- Start/end time, environment, tool/version.
- Source repo/path, branch, before/after commit SHA.
- Action/command, exit code và output/log reference.
- Tests run/skipped/blocked/failed và kết quả.
- Review/CI/PR references.
- Artifact/evidence IDs, URI/path, hash, producer, timestamp.
- Blockers, deviations, change requests và disposition.

Không ghi secret, token hoặc dữ liệu cá nhân không cần thiết vào execution record.

## 7. 05_BUILD mapping rules

- Giữ đúng chín child areas đã khai báo trong Manifest; không tự tạo top-level hoặc child folder ngoài chuẩn.
- Mọi WP mapping phải trỏ tới canonical Work plan và source repository/path thật.
- Build Register hiện hữu trên branch là legacy candidate đang reconciliation; không được coi là authoritative WP plan song song với 04_PLAN.
- Mapping thiếu target/version/commit/hash là NOT VERIFIED.
- Không move/delete/overwrite legacy candidate trước inventory, backup, duplicate analysis, owner approval và independent review.
- Mọi source change diễn ra tại canonical source repository; branch work/70/05-build không tự động là source code branch.
- Mapping migration chỉ PASS khi target, hash/version, links, branch/Sandbox readback và QE evidence đã xác minh.

## 8. Change control và xử lý lỗi

- Thay đổi requirement/outcome/acceptance: quay lại DEFINE theo DOC-043.
- Thay đổi architecture/interface/security boundary: ACR/ADR theo DOC-044 và authority approval.
- Thay đổi sequencing/estimate/WP scope: PCR theo DOC-045.
- Build failure: giữ trạng thái FAIL/BLOCKED, lưu logs, xác định root cause, fix có trace và rerun.
- CI unavailable: NOT RUN/BLOCKED; không coi local pass là CI pass.
- Permission denied hoặc source target mơ hồ: dừng; không dùng credential/route khác để vượt kiểm soát.
- Rollback theo kế hoạch đã duyệt; ghi commit/tag/artifact và verification sau rollback.

## 9. G5 — Gate BUILD → VERIFY

Điều kiện tối thiểu theo phạm vi Work:
- [ ] G4 PASS và WP execution có authorization.
- [ ] Các WP bắt buộc đã đạt DoD hoặc ngoại lệ có authority.
- [ ] Source artifacts nằm tại canonical repositories, commit/version rõ.
- [ ] Required unit/component/contract/integration/static/security tests có kết quả và evidence.
- [ ] CI evidence gắn đúng commit và workflow run.
- [ ] Independent code/design review hoàn tất; findings có disposition.
- [ ] Artifact provenance/hash và mapping/evidence registry đầy đủ.
- [ ] Không có critical blocker hoặc unapproved architecture/requirement deviation.
- [ ] Known limitations, deferred defects và residual risks được công khai.
- [ ] Build handoff package đủ để VERIFY tái thực hiện và kiểm tra độc lập.
- [ ] Product Owner/authorized authority ghi G5 decision theo DOC-004.

Trạng thái:
- **PASS:** mọi điều kiện bắt buộc đạt và authority decision có evidence.
- **NOT READY:** thiếu deliverable/test/review có thể hoàn thiện.
- **BLOCKED:** thiếu permission, dependency, environment, owner hoặc quyết định.
- **FAIL:** kiểm chứng cho thấy deliverable không đáp ứng tiêu chí.
- **WAIVED:** chỉ theo DOC-004, có authority, scope, rationale, residual risk và expiry/review date; không mặc định là PASS.

CI green, PR merged hoặc file tồn tại không tự tạo G5 PASS.

## 10. Handoff sang VERIFY

Gói bàn giao tối thiểu:
- Approved WP/plan baseline, G4/G5 references.
- Requirement/architecture baseline và trace map.
- Canonical source repo/path, branch, commit SHA và artifact hashes.
- Implementation notes, changed components/contracts/ADRs.
- Unit/component/contract/integration/static/security test records.
- CI workflow run và environment/toolchain.
- Independent review findings và disposition.
- Defect list, known limitations, risks và rollback notes.
- Evidence Register references và reproduction instructions.
- Verification scope/questions chưa được BUILD tự kết luận.

## 11. Checklist thực hiện

- [ ] B01 WP/G4/DoR/source verified.
- [ ] B02 environment, permissions, branch and baseline.
- [ ] B03 task breakdown and implementation approach.
- [ ] B04 canonical source changes and execution log.
- [ ] B05 tests and quality evidence.
- [ ] B06 independent review and findings.
- [ ] B07 CI/integration/artifact provenance.
- [ ] B08 mapping and evidence registration.
- [ ] B09 DoD and reviewer disposition.
- [ ] B10 handoff to VERIFY.
- [ ] Update Work journal, WP plan status, mapping and evidence records.

## 12. Hướng dẫn AI tham gia BUILD

1. Đọc Manifest, DOC-002, DOC-004/005, approved DOC-011, DOC-036, DOC-044/045/046 và WP cụ thể.
2. Kiểm tra G4, WP READY, DoR, source path và permissions trước khi thực thi.
3. Không coi branch mapping là source repository.
4. Không tự thay đổi scope, requirement, architecture hoặc acceptance.
5. Ghi mọi thao tác quan trọng bằng commit/log/test evidence.
6. Chỉ gọi PASS khi test thực sự chạy và đúng commit/environment.
7. Không tự review độc lập code do mình tạo.
8. Không lách permission/safety boundary khi tool bị từ chối; báo blocker.
9. Đăng ký evidence có provenance và hash khi khả thi.
10. Handoff đầy đủ để QE có thể tái lập, kiểm tra và phản biện.

## 13. Ví dụ minh họa (giả định)

Một WP thay đổi Dashboard UI phải xác định source repository thật, approved contract, branch/commit, test cases cho local_snapshot/core_cached/core_live, UNKNOWN/STALE behavior, read-only constraint, reviewer và CI evidence. Nếu source repository hoặc Core contract chưa được xác minh, WP không được tự chuyển READY. Đây là ví dụ phương pháp, không xác nhận trạng thái triển khai cụ thể.

## 14. Kiểm soát và thay đổi

DOC-046 là chuẩn quy trình. Vinh giữ authority đối với scope, ngoại lệ, G5 và các quyết định trọng yếu. Xu điều phối build, mapping, execution records và handoff; không tự phê duyệt gate hoặc acceptance.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành B01–B10, canonical source rules, execution evidence, review/CI, mapping, G5 and handoff standard. |
