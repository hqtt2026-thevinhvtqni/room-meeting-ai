# QUY TRÌNH QUẢN LÝ BẰNG CHỨNG / EVIDENCE PROCESS
- **STT / Document ID:** DOC-048
- **Priority / Mức ưu tiên:** P1
- **Read order / Thứ tự đọc:** 48
- **Depends on / Phụ thuộc:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-014; DOC-015; DOC-033; DOC-038; DOC-047
- **Status / Trạng thái:** ACTIVE — CROSS-PHASE PROCESS STANDARD
- **Version / Updated:** 1.0 / 2026-10-30
- **Owner / Phụ trách:** Xu / AI-01
- **Authority / Thẩm quyền:** Vinh — Product Owner

## 1. Mục đích và phạm vi

DOC-048 quy định quản lý bằng chứng (evidence) xuyên suốt vòng đời Work: tạo lập, định danh, lưu trữ, đăng ký, kiểm tra tính toàn vẹn, xác minh, sử dụng trong gate/acceptance/release/operations và lưu giữ lịch sử.

DOC-014 là sổ đăng ký bằng chứng chuẩn ở top-level 06_EVIDENCE. Các phase có thể tạo evidence, nhưng chỉ evidence được đăng ký theo DOC-014 mới được xem là tham chiếu chính thức trong gate package. 05_BUILD/06_EVIDENCE chỉ là staging; không phải sổ bằng chứng xuyên phase.

DOC-048 không biến việc có file thành bằng chứng cho mọi claim. Evidence phải liên quan trực tiếp tới claim, đúng target/version, có provenance, đủ integrity và được verifier đánh giá theo tiêu chí.

## 2. Nguyên tắc bắt buộc

1. **Claim-first:** mỗi evidence phải nói rõ claim/requirement/gate nào cần hỗ trợ.
2. **Provenance:** ghi producer, time, source, environment, tool/version và exact target.
3. **Integrity:** hash/version khi khả thi; không âm thầm thay artifact đã ghi nhận.
4. **Minimality:** chỉ thu thập dữ liệu cần thiết; tránh secrets và personal data không cần thiết.
5. **Independent verification:** RECORDED không đồng nghĩa VERIFIED; người tạo không tự xác nhận độc lập nếu yêu cầu verifier.
6. **Reproducibility:** người khác có thể tìm, mở và tái thực hiện hoặc hiểu giới hạn của evidence.
7. **Freshness:** evidence có thể stale; ghi thời điểm, expiry/review condition và scope.
8. **Immutable history:** correction tạo version/record mới; không xóa dấu vết.
9. **Fail honestly:** missing, inaccessible, corrupt, conflicting hoặc unverifiable phải thể hiện đúng trạng thái.
10. **Authority:** evidence hỗ trợ quyết định; không tự thay thế quyết định của Product Owner/gate authority.

## 3. Phân loại bằng chứng

Evidence type có thể gồm:
- SOURCE: source code, config, schema, contract, commit/PR.
- TEST: test case, execution log, CI run, test report.
- RUNTIME: trace, metric, audit event, deployment/runtime observation.
- REVIEW: code review, architecture review, independent QE report.
- DOCUMENT: approved specification, plan, decision, minutes, acceptance record.
- DATA: dataset snapshot, validation output, checksum, migration reconciliation.
- SECURITY: threat assessment, security test, access review, incident evidence.
- OPERATION: monitoring, backup/restore, runbook execution, SLO report.
- EXTERNAL: vendor/authority record or third-party confirmation.

Mỗi evidence phải có type cụ thể; không dùng “screenshot” hoặc “report” làm type duy nhất nếu cần mô tả claim/method rõ hơn.

## 4. Evidence lifecycle

### E01 — Xác định claim và nhu cầu
- Ghi claim, requirement, WP, test, risk, gate hoặc decision được hỗ trợ.
- Xác định evidence cần thiết, mức độc lập và tiêu chí đủ.
- Xác định dữ liệu nhạy cảm, retention và access classification.
**Đầu ra:** Evidence Need/Claim Map.

### E02 — Tạo và thu thập
- Thu thập từ source/tool/runtime chính thức trong phạm vi được phép.
- Ghi producer, timestamp, environment, tool/version, exact source/artifact commit.
- Không chỉnh sửa output để làm đẹp hoặc che lỗi; bản trình bày phải link về raw evidence.
**Đầu ra:** Raw Evidence Artifact.

### E03 — Định danh và đăng ký
- Cấp Evidence ID duy nhất theo quy tắc Work.
- Ghi artifact_ref, type, related Work/WP/requirement/test/gate, producer, created_at, source_environment.
- Ghi SHA-256, media_type, reviewer/verifier, status và limitation khi có.
- Đăng ký tại DOC-014 JSON source; Markdown index là human-readable mirror, không phải nguồn cạnh tranh.
**Đầu ra:** Evidence Register Record.

### E04 — Kiểm tra integrity và provenance
- Xác minh path/URI truy cập được và trỏ đúng artifact.
- Tính/đối chiếu hash khi khả thi; xác minh commit/version và timestamp.
- Kiểm tra tool output, environment, target và source identity.
- Nếu không thể hash hoặc source không truy cập được, ghi rõ lý do và mức tin cậy; không giả định integrity.
**Đầu ra:** Integrity/Provenance Check.

### E05 — Review và xác minh claim
- So evidence với claim/acceptance criteria và counter-evidence.
- Kiểm tra relevance, completeness, correctness, independence, freshness và reproducibility.
- Verifier ghi tên/role, thời điểm, phạm vi, phương pháp và kết quả.
- Nếu evidence chỉ được ghi nhận nhưng chưa xác minh, giữ RECORDED.
**Đầu ra:** Verification Decision.

### E06 — Sử dụng trong gate và quyết định
- Gate package trỏ tới Evidence ID cụ thể, không chỉ tên file.
- Gate authority kiểm tra evidence có đủ để kết luận criteria hay không.
- Evidence VERIFIED không tự động khiến gate PASS; quyết định gate phải được ghi riêng.
- Waiver phải nêu evidence thiếu, residual risk, scope, authority và expiry/review.
**Đầu ra:** Gate Evidence Map.

### E07 — Lưu giữ, cập nhật và retirement
- Áp dụng retention/access policy đã duyệt; hạn chế quyền theo need-to-know.
- Khi artifact thay đổi, tạo version/evidence record mới và link supersedes.
- Khi evidence hết hạn, đánh dấu STALE/REJECTED theo policy; không xóa lịch sử.
- Khi Work đóng, lưu trữ theo retention rule và bảo toàn khả năng audit.
**Đầu ra:** Retention/Version History.

## 5. Evidence state model

DOC-014 hiện quy định các state:
- **MISSING:** evidence được yêu cầu nhưng chưa có artifact.
- **RECORDED:** artifact/reference đã được ghi nhận; chưa có xác minh độc lập đầy đủ.
- **VERIFIED:** artifact, provenance, integrity và claim đã được verifier kiểm tra theo phạm vi.
- **REJECTED:** artifact không hợp lệ, không liên quan, sai target, sai integrity hoặc không hỗ trợ claim.

Quy tắc bổ sung:
- STALE, CONFLICTED, INACCESSIBLE và SUPERSEDED nên được biểu diễn bằng metadata/notes hoặc trạng thái mở rộng sau khi schema được kiểm soát; không tự thêm enum vào JSON trước khi cập nhật schema/version.
- MISSING không phải evidence artifact; đây là trạng thái gap cần action owner.
- VERIFIED phải có verifier, verified_at, verification_method/scope và target version.
- Evidence VERIFIED có thể chỉ hỗ trợ một claim/phạm vi cụ thể; không khái quát ra toàn hệ thống.

## 6. Evidence record và schema requirements

DOC-014 JSON là machine-readable source; JSON Schema là contract. Record chuẩn nên hỗ trợ:
- evidence_id, work_id, type, artifact_ref, media_type.
- claim/requirement/WP/test/gate/decision references.
- producer, created_at, source_environment, tool_version.
- source_commit/artifact_version, sha256, size khi phù hợp.
- reviewer/verifier, verified_at, verification_method, verification_scope.
- state, limitations, counter_evidence_refs, supersedes/equivalent refs.
- access_classification, retention_policy/expiry khi được phê duyệt.

Mọi schema extension phải version, validate sample data, backward compatibility và migration. Không chèn metadata Markdown vào JSON/schema. Nếu metadata không phù hợp với artifact format, dùng sidecar/register entry theo DOC-038.

## 7. Security, privacy và storage

- Không lưu password, API key, token, private prompt hoặc secret.
- Redact/mask dữ liệu cá nhân; chỉ giữ phần cần chứng minh claim.
- Phân quyền đọc/tải/xuất evidence theo Work scope và classification.
- Ghi audit event cho truy cập/thay đổi/export khi hệ thống hỗ trợ.
- Hash hỗ trợ integrity nhưng không chứng minh authenticity nếu không có provenance/trust chain.
- Storage location, encryption, backup, retention và deletion phải theo architecture/contract đã duyệt; DOC-048 không tuyên bố backend hiện có.
- Khi URI/path inaccessible, đánh dấu NOT VERIFIED và mở action; không tự thay bằng bản copy không rõ nguồn.

## 8. Conflict, correction và counter-evidence

- Không xóa evidence mâu thuẫn; liên kết cả hai và đánh dấu CONFLICTED trong metadata/notes cho tới khi được giải quyết.
- Ghi claim bị ảnh hưởng, nguồn, thời điểm, scope và phương pháp đối chiếu.
- Correction tạo evidence version mới, nêu lý do và supersedes; giữ artifact cũ theo retention.
- Counter-evidence phải được xem xét trong gate review, không chỉ chọn evidence ủng hộ kết luận.
- Nếu conflict làm thay đổi requirement/design, chuyển về DEFINE/ARCHITECT theo đúng quy trình.

## 9. G0 Evidence readiness và gate usage

Evidence readiness tối thiểu trước gate:
- [ ] Mỗi criterion có evidence requirement hoặc rationale NOT APPLICABLE.
- [ ] Evidence ID duy nhất và artifact_ref truy cập được.
- [ ] Target version/commit/environment rõ.
- [ ] Provenance và integrity được ghi.
- [ ] Verifier/verification scope có khi cần.
- [ ] RECORDED/VERIFIED/REJECTED/MISSING không bị đánh đồng.
- [ ] Counter-evidence, limitation và stale data được công khai.
- [ ] Evidence Register và schema hợp lệ.
- [ ] Gate decision tham chiếu evidence IDs và ghi authority riêng.

Evidence completeness là điều kiện hỗ trợ gate; không tự tạo gate PASS.

## 10. AI handling rules

1. Không tạo evidence ID cho artifact không tồn tại.
2. Không ghi VERIFIED nếu chỉ mới tạo file hoặc nhận lời xác nhận.
3. Không sửa timestamp, producer, source hoặc test result để khớp mong muốn.
4. Ghi chính xác tool output và giới hạn quan sát.
5. Hash chỉ ghi sau khi tính từ exact bytes; không đoán.
6. Không đưa secrets/private data vào evidence.
7. Không bỏ qua counter-evidence hoặc lỗi đọc artifact.
8. Khi connector/sandbox/tool bị chặn, ghi BLOCKED và dừng; không vòng qua policy.
9. Mỗi gate claim phải trỏ tới evidence cụ thể và đúng scope.
10. Giữ append-only history và ghi rõ supersession/correction.

## 11. Ví dụ minh họa (giả định)

Một CI run có thể được đăng ký là evidence loại TEST với workflow URL/run ID, commit SHA, branch, toolchain, timestamp, result và logs. Nếu run xanh nhưng thuộc commit cũ, nó không chứng minh commit mới đạt. Nếu run được ghi vào register nhưng chưa có người kiểm tra đúng target, state vẫn RECORDED, chưa VERIFIED. Đây là ví dụ phương pháp.

## 12. Kiểm soát và thay đổi

DOC-048 là chuẩn quản lý evidence xuyên phase. Vinh giữ authority đối với gate/acceptance decisions và residual risk trọng yếu. Evidence owner chịu trách nhiệm artifact/provenance; verifier chịu trách nhiệm xác minh trong phạm vi; Xu điều phối register và traceability.

## Change History
| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-30 | Ban hành E01–E07, evidence states, provenance/integrity, security/privacy, conflict handling and gate usage. |
