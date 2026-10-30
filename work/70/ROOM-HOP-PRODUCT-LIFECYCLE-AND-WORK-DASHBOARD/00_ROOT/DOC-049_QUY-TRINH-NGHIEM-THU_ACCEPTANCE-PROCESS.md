# QUY TRÌNH NGHIỆM THU / ACCEPTANCE PROCESS
- **STT / Document ID:** DOC-049
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 49
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-008; DOC-014; DOC-020; DOC-033; DOC-038; DOC-047; DOC-048
- **Status / Trạng thái:** ACTIVE — PROCESS STANDARD
- **Version / Updated:** 1.1 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và ranh giới

DOC-049 quy định 07_ACCEPT (Nghiệm thu): quyết định chính thức sản phẩm/deliverable có được Product Owner chấp nhận theo approved requirements, acceptance criteria, scope, quality, risk và evidence hay không.

Acceptance là quyết định có thẩm quyền, không phải hoạt động test. VERIFY cung cấp kết quả kiểm chứng và recommendation; Product Owner quyết định chấp nhận, chấp nhận có điều kiện nếu policy cho phép, từ chối hoặc yêu cầu sửa.

Acceptance không đồng nghĩa RELEASE hoặc OPERATE. G6 PASS chỉ xác nhận quyết định chấp nhận trong scope được ghi; không tự cho phép phát hành production.

## 2. Điều kiện đầu vào

- G6 VERIFY → ACCEPT PASS theo DOC-004.
- Approved DOC-008 requirements baseline và acceptance criteria được xác định.
- DOC-014 evidence register và gate evidence map đầy đủ.
- Verification Summary, Coverage Matrix, Independent QE Report và defect disposition có sẵn.
- Critical/high defects, waivers, residual risks và known limitations được công khai.
- Release scope, exclusions và post-acceptance obligations được nêu rõ.
- Người có thẩm quyền và acceptance scope được xác định.

Nếu G6 chưa PASS, chỉ được chuẩn bị acceptance pack; không ghi ACCEPTED và không phát hành quyết định thay Product Owner.

## 3. Nguyên tắc
1. Acceptance dựa trên criteria đã duyệt, không dựa vào cảm nhận hoặc số lượng tài liệu.
2. Product Owner/authorized authority là người quyết định; AI/QE chỉ tư vấn.
3. Decision phải chỉ rõ scope, version, commit/artifact, environment và evidence.
4. Không che giấu defects, exclusions, waivers hoặc residual risk.
5. Conditional acceptance chỉ được dùng nếu DOC-004/policy cho phép, có điều kiện, owner, due date và consequence.
6. Acceptance không tự động mở RELEASE hoặc OPERATE.
7. Mọi từ chối/yêu cầu sửa phải truy được về criterion/evidence.
8. Không sửa acceptance criteria hồi tố để biến kết quả FAIL thành PASS; thay đổi phải qua DEFINE/change control.

## 4. Vai trò

| Vai trò | Trách nhiệm |
|---|---|
| Product Owner (Vinh) | Quyết định G6, scope, exception và residual risk |
| Acceptance Coordinator (Xu / AI-01) | Chuẩn bị pack, kiểm tra completeness, ghi decision và handoff |
| Independent QE | Trình bày verification coverage, defects và confidence |
| WP/Delivery Owner | Giải trình deliverables, known limitations và remediation |
| Security/Operations Owner | Xác nhận các obligations thuộc security/operations |
| Stakeholders | Xác nhận nhu cầu/impact trong phạm vi được mời |

## 5. Quy trình — AC01 đến AC08

### AC01 — Xác định acceptance scope
- Chốt product/deliverable, version, commit, environment và boundary.
- Liệt kê in-scope, out-of-scope, exclusions và dependencies.
- Xác nhận acceptance criteria/baseline không bị thay đổi ngoài quy trình.
**Đầu ra:** Acceptance Scope Statement.

### AC02 — Kiểm tra điều kiện G6 và evidence
- Xác minh G6 decision và authority.
- Đối chiếu criteria với Evidence IDs trong DOC-014.
- Kiểm tra evidence state, provenance, integrity, freshness và verifier.
- Liệt kê evidence MISSING/RECORDED/REJECTED, NOT RUN và limitation.
**Đầu ra:** Acceptance Evidence Matrix.

### AC03 — Đánh giá defects và residual risk
- Tổng hợp open/closed defects, severity, impact và workaround.
- Xác nhận retest/regression evidence.
- Ghi waiver, residual risk, owner, due date, expiry/review date.
- Đánh giá tác động người dùng, dữ liệu, bảo mật, vận hành và pháp lý.
**Đầu ra:** Defect & Residual Risk Summary.

### AC04 — Đánh giá nghĩa vụ bàn giao
- Kiểm tra documentation, support, training, ownership, licensing và data handoff khi liên quan.
- Xác định nghĩa vụ còn lại, service boundary và dependency bên ngoài.
- Ghi rõ phần chưa hoàn thiện và ai chịu trách nhiệm sau acceptance.
**Đầu ra:** Handover/Obligations Checklist.

### AC05 — Chuẩn bị Acceptance Pack
- Tập hợp baseline, G6, coverage, QE report, evidence map, defects, risks và limitations.
- Đưa ra recommendation ACCEPT / CONDITIONAL / REJECT / DEFER; recommendation không phải decision.
- Đảm bảo decision maker có thể xem evidence gốc và phản biện.
**Đầu ra:** Acceptance Decision Pack.

### AC06 — Product Owner review và quyết định
Các quyết định có thể gồm:
- **ACCEPT:** criteria bắt buộc đạt, scope/version rõ, residual risk được chấp nhận.
- **CONDITIONAL ACCEPT:** chỉ nếu policy cho phép; điều kiện/owner/due date/expiry và consequence rõ.
- **REJECT:** không đáp ứng criteria hoặc risk không chấp nhận.
- **DEFER:** chưa đủ evidence/decision/context.
Product Owner ghi decision, rationale, scope, timestamp, authority và evidence refs.
**Đầu ra:** G6 Decision Record.

### AC07 — Ghi nhận và thông báo
- Cập nhật DOC-020 Acceptance Record và Decision Log.
- Liên kết decision tới baseline/evidence/defects/waivers.
- Thông báo các owner/stakeholders liên quan và obligations.
- Không thay đổi release status tại bước này.
**Đầu ra:** Approved Acceptance Record hoặc rejection/defer record.

### AC08 — Handoff sang RELEASE hoặc remediation
- Nếu ACCEPT và release được phép: chuyển acceptance pack sang 08_RELEASE.
- Nếu CONDITIONAL ACCEPT: kiểm tra policy và các điều kiện có thể chặn release.
- Nếu REJECT/DEFER: tạo remediation/change requests, quay về phase phù hợp.
**Đầu ra:** Release Handoff hoặc Remediation Plan.

## 6. G6 — Gate VERIFY → ACCEPT

- [ ] G6 PASS có authority và evidence.
- [ ] Acceptance scope/version/commit/environment xác định.
- [ ] Approved requirements và acceptance criteria được đối chiếu.
- [ ] Evidence matrix bao phủ criteria; trạng thái evidence chính xác.
- [ ] Independent QE report và coverage được xem xét.
- [ ] Defects, waivers, limitations và residual risks có disposition.
- [ ] Security/privacy/data/operations obligations được đánh giá khi liên quan.
- [ ] Handover ownership và outstanding obligations rõ.
- [ ] Product Owner/authorized authority ghi quyết định G6.

G6 trạng thái: PASS / NOT READY / BLOCKED / REJECTED / CONDITIONAL (nếu policy cho phép). Không có quyết định ghi nhận thì acceptance vẫn PENDING.

## 7. Acceptance record tối thiểu

DOC-020 phải ghi:
- Work/product/deliverable và acceptance scope.
- Requirements/architecture baseline version.
- Source commit/artifact version/hash/environment.
- G6 reference, QE report và evidence IDs.
- Criteria result và exclusions.
- Defects, waivers, residual risks, limitations.
- Decision: ACCEPT/CONDITIONAL/REJECT/DEFER.
- Decision maker/authority, timestamp, rationale.
- Conditions, owner, due date, expiry/review date (nếu có).
- Handoff target và obligations.

## 8. AI instructions

- Không tự ghi ACCEPTED, không ký thay Product Owner.
- Không suy acceptance từ CI green, demo, file creation hoặc AI consensus.
- Không bỏ qua evidence conflict hoặc defect.
- Nếu G6 thiếu, giữ PENDING/NOT READY.
- Decision record phải được lưu append-only; correction tạo entry mới.
- Không dùng conditional acceptance để lách critical security/legal blocker.

## 9. Ví dụ minh họa (giả định)

Một Dashboard có thể vượt qua functional tests nhưng chưa có browser E2E hoặc Core live integration. Acceptance pack phải công khai giới hạn đó và đối chiếu với scope/criteria đã duyệt. Nếu Core live là acceptance criterion bắt buộc thì không được ACCEPT; nếu ngoài scope được phê duyệt, Product Owner mới có thể quyết định trong phạm vi giới hạn được ghi. Đây là ví dụ phương pháp.

## 10. Kiểm soát và thay đổi

DOC-049 là chuẩn quy trình. Vinh giữ final authority đối với G6. Xu chuẩn bị hồ sơ và điều phối; QE đưa ra bằng chứng/recommendation; không vai trò nào được tự nâng quyền thành Product Owner.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-10-30 | Xu / AI-01 | Align acceptance gate with DOC-004: G6 VERIFY→ACCEPT. |
| 1.0 | 2026-10-30 | Ban hành AC01–AC08, acceptance decision, G6, evidence/defect review and handoff standard. |
