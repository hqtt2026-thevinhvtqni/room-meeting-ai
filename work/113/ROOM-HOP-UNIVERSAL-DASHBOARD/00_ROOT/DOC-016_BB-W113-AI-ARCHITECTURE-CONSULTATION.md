# W113 — BIÊN BẢN THAM VẤN KIẾN TRÚC ĐA AI
- DOC-ID: DOC-016
- Mã nghiệp vụ dự kiến: BB-W113-20261112-001 (PROPOSED — CHƯA ĐƯỢC XU CẤP / CHƯA PHÁT HÀNH)
- Phiên bản: 1.0 — DRAFT
- Work: 113 — ROOM-HOP-UNIVERSAL-DASHBOARD
- Tham chiếu: W70-AI-CONSULT-01
- Người ghi nhận: Co — AI-07 / Coder Assistant
- Chủ trì tham vấn: Xu — AI-01
- Chủ sở hữu / thẩm quyền quyết định: Vinh
- Thời gian ghi nhận: 2026-11-12 21:45 UTC+7
- Hình thức: tham vấn kiến trúc độc lập; không phải cuộc họp có đầy đủ xác nhận của các thành viên.
- Trạng thái: DRAFT / CHỜ XU TỔNG HỢP / CHỜ VINH QUYẾT ĐỊNH.

## 1. Mục đích
Ghi nhận ý kiến độc lập của Co về kiến trúc cộng tác đa AI và Dashboard, theo yêu cầu W70-AI-CONSULT-01. Biên bản này chỉ ghi nhận ý kiến của Co; không đại diện kết luận đồng thuận của Xu, Ka hoặc các AI khác.

## 2. Phạm vi đã tham vấn
A. Multi-Agent Architecture; B. Task Management; C. AI Runtime/Execution Authority; D. Dashboard; E. Data & Integration; F. Governance & QA.

## 3. Nội dung chính
1. Co kiến nghị Hybrid Multi-Agent: Manager-led orchestration với Peer-to-Peer collaboration có kiểm soát.
2. Xu là Lifecycle Orchestrator; Vinh giữ quyền quyết định cuối.
3. Phải xác minh identity, session binding và recipient ACK; không coi tin nhắn giao việc là bằng chứng AI đã nhận hoặc thực thi.
4. Assignment, Transport, Execution và Review phải có state machine riêng, liên kết bằng IDs.
5. Core là authority cho domain dữ liệu/quyền mà Core thực sự sở hữu; Agent Runtime quản lý adapter/session/dispatch; Execution Host enforce quyền tại ranh giới thực thi.
6. Run Record và evidence phải truy xuất được về principal, assignment, source revision, action, result và artifact hash.
7. Đồng ý phân biệt Work Execution Dashboard với Product Dashboard; dùng projection có provenance/freshness, không tạo database/authority trùng lặp.
8. Kế thừa các Work/dịch vụ hiện hữu theo domain ownership; không viết lại ROOM khi chưa chứng minh cần thiết.
9. Independent Review bắt buộc; AI không tự nghiệm thu phần việc của mình.
10. Kiến nghị triển khai theo các giai đoạn reconciliation → contracts → pilot → runtime integration → dashboard → production readiness.

## 4. FACT / ASSUMPTION / RECOMMENDATION
- FACT: W113 DOC-013 ghi G0–G5 NOT ASSESSED; product source NOT DECLARED; UI implementation NOT STARTED; E2E NOT RUN; acceptance/release NOT AUTHORIZED.
- FACT: W113 DOC-008 đang DRAFT và nói rõ endpoint/API/permission/live service chưa được phê duyệt bởi tài liệu thiết kế.
- ASSUMPTION: native dispatch vào phiên AI hiện tại, recipient ACK gate, Core grant/run services và live Dashboard data chưa có đủ bằng chứng xác minh.
- RECOMMENDATION: Hybrid architecture là phương án ưu tiên để Xu tổng hợp, không phải quyết định đã được Vinh phê duyệt.

## 5. Ý kiến khác biệt / điểm cần xử lý
- Không dùng một state machine duy nhất cho assignment/transport/execution/review.
- Không coi Meeting message hoặc transport receipt là recipient ACK.
- Không coi session_ref là bằng chứng phiên đang hoạt động.
- Không mặc định Core API/runtime contract đã tồn tại.
- Không cho Dashboard tự ghi trạng thái chính thức hoặc tự nghiệm thu.
- Không mở Peer-to-Peer tự do; authority và audit phải tập trung.
- Không triển khai đồng loạt nhiều adapter trước pilot có bằng chứng.

## 6. Kết luận tham vấn của Co
Co đề xuất Hybrid Multi-Agent và hai Dashboard theo domain separation. Các năng lực dispatch/session/ACK/Core grant/Host enforcement/live projection vẫn phải kiểm chứng. Tài liệu phương án DOC-015 là hồ sơ chi tiết đi kèm.

## 7. Quyết nghị / thẩm quyền
- Không có quyết định thi công nào được ban hành tại biên bản này.
- Xu tổng hợp ý kiến và bất đồng của các AI.
- Vinh là người quyết định cuối cùng.
- Chỉ mở thi công sau khi có phê duyệt hợp lệ, biên bản/quyết định chính thức, Work Entry/G0–G5 và assignment/scope theo chuẩn W70.
- Mã BB nêu trên chỉ là mã dự kiến; cần Xu kiểm tra/cấp mã theo DOC-039/DOC-040 và sổ đăng ký W113. Không được coi là ISSUED.

## 8. Xác nhận
- Người ghi nhận: Co — AI-07.
- Chủ trì tổng hợp: Xu — chưa xác nhận trong hồ sơ này.
- Chủ sở hữu: Vinh — chưa có quyết định trong hồ sơ này.
- Các thành viên khác: không ghi nhận xác nhận nếu chưa có ACK/ý kiến thực tế.

**Disposition:** CONSULTATION RECORDED — DRAFT / NOT ISSUED / NO IMPLEMENTATION AUTHORIZATION.
