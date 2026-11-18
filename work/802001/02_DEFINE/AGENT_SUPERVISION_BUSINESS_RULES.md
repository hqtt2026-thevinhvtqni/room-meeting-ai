# DEFINE — QUY TẮC NGHIỆP VỤ THEO DÕI & HƯỚNG DẪN AGENT
## Agent Work Supervision & Guidance Business Rules

- Work: 802001
- Artifact ID: W802001-DEF-001
- Version: 0.3 — POST-REVIEW GOVERNANCE REFERENCE CORRECTION
- Date: 2026-11-17
- Governing standard: Work 70
- Status: APPROVED BY VINH — BASELINE BUSINESS POLICY (2026-11-18); ARCHITECTURE EXPLORATION AUTHORIZED; BUILD NOT AUTHORIZED
- Authority: Vinh (final approval); Xu / AI-01 (coordination and draft owner)

## 1. Mục đích và ranh giới
Tài liệu này chuyển 10 tình huống lịch sử trong DISCOVER thành bộ quy tắc nghiệp vụ ban đầu để điều phối viên theo dõi, nhắc nhở, hướng dẫn, yêu cầu điều chỉnh, kiểm tra lại và chuyển cấp trong suốt assignment.

Đây là bản DEFINE dự thảo, không phải quyết định phê duyệt policy, không phải đặc tả kỹ thuật cuối cùng và không chứng minh ROOM-HOP đã có runtime monitoring/reminder/enforcement.

W70 tiếp tục là chuẩn quản trị gốc. Trạng thái trong tài liệu này chỉ áp dụng cho assignment/finding; không thay thế lifecycle state hoặc Gate G0–G9 của W70. DOC-001 xác định authority/source boundaries; DOC-004/005 giữ chuẩn lifecycle/Gate; DOC-033 điều chỉnh tài liệu/lưu trữ; DOC-035 là nhật ký thi công cấp Work; DOC-057 kiểm tra điều kiện tham gia/nhận assignment. DOC-096 là tài liệu Retrieval/DecisionRAG, không phải chuẩn phiên hoặc nhật ký.

Đính chính truy nguyên sau phản biện Vibe: DOC-096 đã được tìm thấy tại `work/70/ROOM-HOP-PRODUCT-LIFECYCLE-AND-WORK-DASHBOARD/03_ARCHITECT/DOC-096_RETRIEVAL-STRATEGY-AND-DECISIONRAG-ADOPTION.md`; nội dung chính thức là Retrieval đa phương pháp/DecisionRAG (P1, research only), không phải session integrity hoặc journal control. W802001 đã gán sai nội dung cho DOC-096. Căn cứ nhật ký phải tham chiếu DOC-035; quy tắc tài liệu/lưu trữ tham chiếu DOC-033; DOC-057 chỉ áp dụng cho điều kiện entry/assignment. Không sử dụng DOC-096 làm căn cứ cho policy W802001.

## 2. Đơn vị theo dõi và dữ liệu tối thiểu
Đơn vị theo dõi là một assignment gắn với Work/WP cụ thể. Mỗi assignment cần có:
- Assignment ID; Work ID; WP/task; Agent/role được giao; người giao và người điều phối.
- Mục tiêu, phạm vi được phép, điều không được làm, đầu ra và tiêu chí nghiệm thu.
- Nguồn chuẩn (canonical paths, version/commit hoặc decision ID).
- Checkpoint/mốc kiểm tra, thời điểm hoặc điều kiện kích hoạt, người review.
- Kênh phản hồi; nơi ghi journal; yêu cầu evidence.
- Trạng thái acknowledgement và blocker/permission cần thiết.

Nếu thiếu dữ liệu thiết yếu để thực hiện an toàn/đúng hướng, trạng thái là NEEDS_BRIEFING hoặc BLOCKED; không suy diễn Agent đã nhận việc từ im lặng.

## 3. Taxonomy — phân loại finding
Một finding có một nhóm chính và có thể có nhãn phụ:
- SCOPE_ROLE: làm sai mục tiêu, phạm vi, vai trò hoặc vượt quyền.
- PROCESS: bỏ bước, sai thứ tự, không tuân thủ lifecycle/checkpoint đã duyệt.
- SOURCE_OF_TRUTH: dùng sai/đã cũ tài liệu, branch, commit, runtime hoặc decision.
- IDENTITY_AUTHORITY: actor không rõ, identity chưa xác thực, self-loop hoặc quyền không đủ.
- STRUCTURE_NAMING: sai cấu trúc Work, path, naming hoặc canonical location.
- EVIDENCE_JOURNAL: thiếu, không đọc lại được, không độc lập hoặc bị biến đổi evidence; journal không đủ.
- QUALITY_ACCEPTANCE: đầu ra không đạt tiêu chí hoặc claim PASS vượt quá bằng chứng.
- STATUS_REPORTING: báo cáo sai trạng thái, nhầm MOCK với REAL, queued với executed hoặc claimed với verified.
- DELAY_NO_RESPONSE: trễ checkpoint, không acknowledgement/phản hồi hoặc không nêu blocker.
- SYSTEM_DEPENDENCY: lỗi nền tảng, thiếu API/token/quyền/môi trường/connector hoặc dịch vụ.
- SAFETY_SECURITY: rủi ro bảo mật, credential, dữ liệu, hành động phá hủy hoặc tác động ngoài phạm vi.
- DOCUMENTATION_DRIFT: hồ sơ hướng dẫn/manifest/decision không khớp hiện trạng.
- UNKNOWN: chưa đủ bằng chứng để phân loại; giữ mở và tiếp tục TRACE.

Không mặc định mọi finding là lỗi cá nhân Agent. Trước khi quy trách nhiệm phải phân biệt: Agent execution error, system deficiency, missing prerequisite/permission, stale or conflicting documentation, reviewer/coordination error, and unknown cause. Không gắn nhãn động cơ (cố ý/vô ý) nếu thiếu bằng chứng; khi nghi ngờ lặp lại do hướng dẫn kém, xem xét cả trách nhiệm điều phối trước khi quy cho Agent.

Khi một finding liên quan đến nhiều Agent hoặc nhiều Work: ghi một bản ghi finding cho mỗi assignment bị ảnh hưởng, gắn chung một root-cause/correlation ID để truy nguyên; quyết định đóng/mở từng bản ghi độc lập theo evidence của assignment đó. Quy trình liên kết chi tiết là việc của ARCHITECT/PLAN, không chuẩn hóa thêm ở DEFINE v0.2.

## 4. Severity — mức độ ảnh hưởng
Mức độ dựa trên tác động thực tế và khả năng gây hậu quả, không dựa trên cảm xúc hay số lần nhắc đơn thuần.

| Level | Ý nghĩa | Ví dụ định hướng | Hành động |
|---|---|---|---|
| S0 Critical | Có nguy cơ tức thời về bảo mật, dữ liệu, hành động phá hủy, vượt quyền nghiêm trọng hoặc làm sai lệch nguồn sự thật trọng yếu | Lộ credential; xóa/ghi đè dữ liệu ngoài phạm vi; tiếp tục hành động bị cấm | Dừng/hold hành động rủi ro ngay; bảo toàn evidence; báo người có thẩm quyền; không tự ý khôi phục/xóa dấu vết |
| S1 High | Có khả năng làm sai quyết định, sai kiến trúc/scope, sai actor/authority hoặc tạo trạng thái PASS giả | Khẳng định Real E2E khi chỉ có MOCK; dùng identity chưa xác thực để thực hiện hành động có quyền | Cảnh báo rõ; hold bước phụ thuộc; yêu cầu correction và independent recheck |
| S2 Medium | Sai quy trình/nguồn/cấu trúc/chất lượng có thể sửa được, chưa gây tác động nghiêm trọng | Dùng tài liệu cũ; bỏ checkpoint; thiếu readback/evidence quan trọng (nếu bỏ checkpoint có thể che giấu trạng thái PASS giả thì nâng S1) | Hướng dẫn sửa có hạn/checkpoint; theo dõi correction và recheck |
| S3 Low | Sai sót nhỏ, phạm vi hẹp, không ảnh hưởng tính đúng đắn hoặc an toàn tổng thể | Lỗi định dạng/naming cục bộ, thiếu metadata không trọng yếu | Nhắc nhẹ hoặc gom vào checkpoint gần nhất; tránh spam |

Severity ban đầu là provisional. Supervisor phải ghi lý do, tác động, confidence và căn cứ. Khi chưa rõ mức độ, chọn mức tạm thời thận trọng, ghi UNKNOWN/NEEDS_TRACE; không tự nâng thành vi phạm.

## 5. Checkpoint và nhắc nhở theo sự kiện
Không đặt một SLA/tần suất chung cho mọi Agent/Work trong bản 0.1. Checkpoint được xác lập theo:
- Risk/severity và khả năng đảo ngược của hành động.
- Deadline, dependency và thời gian cần để tạo ra evidence có ý nghĩa.
- Độ mới/độ ổn định của nguồn chuẩn và mức độ quan trọng của deliverable.
- Lịch làm việc, thời gian phản hồi đã thống nhất và trạng thái blocked.

Múi giờ và thời gian không hoạt động: mọi mốc checkpoint/deadline trong reminder phải ghi rõ timezone (mặc định +07:00 trừ khi assignment ghi khác); không tính Agent là MISSED/NO_RESPONSE trong khoảng thời gian không hoạt động đã thống nhất; khi Agent offline/biết trước sẽ vắng, chuyển sang chờ đến thời điểm hoạt động kế tiếp thay vì xếp thành vi phạm.

Các loại nhắc:
1. UPCOMING: nhắc trước checkpoint theo lịch đã thống nhất; chỉ nhắc nếu có ích và chưa có evidence hoàn thành.
2. MISSED: checkpoint quá hạn mà chưa có update/evidence; hỏi trạng thái cụ thể, yêu cầu nêu blocker và thời điểm cập nhật.
3. DEVIATION: có bằng chứng sai/lệch; chỉ rõ finding ID, nguồn/tiêu chí bị lệch, tác động và bước cần sửa.
4. CORRECTION_REQUIRED: yêu cầu sửa chính thức; nêu phạm vi sửa, điều không được thay đổi, evidence cần nộp, reviewer và điều kiện recheck.
5. ESCALATION: lặp lại, không phản hồi sau các checkpoint đã thống nhất, vượt quyền hoặc có rủi ro cao; chuyển đúng người có thẩm quyền.

Chống spam: một finding đang mở chỉ có một reminder hiện hành cho cùng một checkpoint; reminder mới phải có thay đổi trạng thái, mốc đến hạn mới hoặc bằng chứng mới. Nếu Agent đã phản hồi và đang xử lý đúng hạn, không gửi nhắc trùng. Khi BLOCKED do điều kiện hệ thống/người khác, chuyển theo dõi blocker và báo owner điều kiện; không liên tục thúc Agent làm việc không thể làm.

## 6. Correction — yêu cầu điều chỉnh
Mỗi yêu cầu correction phải nêu đủ:
- Finding ID, severity, nhóm lỗi và bằng chứng cụ thể.
- Expected state/standard và nguồn chuẩn/version.
- Hành động cần sửa theo thứ tự; phạm vi được phép và hành động phải dừng.
- Người chịu trách nhiệm, reviewer, checkpoint/deadline đã thống nhất.
- Evidence đầu ra bắt buộc và cách readback/reproduce.
- Điều kiện chấp nhận hoặc điều kiện escalate.

Agent có thể tự sửa trong phạm vi assignment đã được duyệt nếu thay đổi an toàn, có thể đảo ngược và không làm đổi scope/architecture/permission/decision. Phải xin phê duyệt của Vinh hoặc người được Vinh ủy quyền khi thay đổi scope, kiến trúc, policy, quyền/credential, dữ liệu có tính phá hủy, chi phí hoặc quyết định đã chốt. Khi không rõ thẩm quyền, HOLD hành động có rủi ro và hỏi người có thẩm quyền; vẫn được phép đọc, phân tích, thu thập evidence và đề xuất phương án an toàn.

## 7. Recheck và đóng finding
Agent nộp correction không đồng nghĩa finding đã đóng. Recheck phải đối chiếu:
- Artifact/source thực tế, commit/version và đúng canonical path.
- Test/command/method, kết quả, timestamp, môi trường và phạm vi.
- Evidence readback; với claim quan trọng phải có bằng chứng độc lập phù hợp.
- Không có regression hoặc side effect trong phạm vi liên quan.
- Journal ghi rõ người kiểm tra và kết luận.

Trạng thái finding:
OPEN → ACKNOWLEDGED → GUIDANCE_SENT → CORRECTION_REQUIRED → CORRECTION_SUBMITTED → RECHECK → (VERIFIED_CLOSED | REOPENED | BLOCKED | ESCALATED).

Reviewer độc lập và tranh chấp: người recheck không được là Agent đã tạo correction, và với S0/S1 cần người không tham gia tạo evidence bị kiểm tra. Nếu reviewer có xung đột lợi ích (cùng tạo evidence, cùng assignment, quan hệ chỉ đạo trực tiếp với actor) thì thay reviewer khác do Xu chỉ định hoặc escalate lên Vinh. Agent/Work Owner không đồng ý kết luận recheck có quyền khiếu nại một lần: nêu căn cứ mới hoặc evidence mới cho Xu; nếu vẫn không thống nhất, Vinh quyết định. Khiếu nại không tự đổi trạng thái finding.

VERIFIED_CLOSED chỉ được reviewer/supervisor có thẩm quyền ghi sau recheck PASS. Agent không tự đóng finding do chính mình xử lý. Với S0/S1 hoặc thay đổi ảnh hưởng quyết định/nguồn sự thật, yêu cầu reviewer độc lập với người tạo correction. BLOCKED không phải CLOSED; phải có blocker, owner điều kiện và điều kiện tiếp tục.

## 8. Quyền hạn và trách nhiệm
- Vinh: thẩm quyền cuối cùng; phê duyệt thay đổi scope, kiến trúc, policy, quyền, chi phí, hành động rủi ro và các quyết định vượt ủy quyền.
- Xu / AI-01: điều phối nghiệp vụ; chuẩn hóa briefing/checkpoint; phát hiện và ghi finding; nhắc/hướng dẫn/yêu cầu correction trong phạm vi đã duyệt; chỉ định reviewer; đề xuất escalation. Xu không được tự biến đề xuất thành policy đã duyệt hoặc tự xác nhận runtime PASS khi thiếu evidence.
- Work Owner: xác nhận yêu cầu nghiệp vụ, deadline, acceptance criteria và nguồn chuẩn trong Work; quyết định các vấn đề thuộc phạm vi được giao.
- Agent thực hiện: acknowledgement, thực hiện đúng scope, báo tiến độ trung thực, nêu blocker sớm, nộp correction/evidence; không tự xác nhận PASS cuối cùng cho finding cần reviewer.
- Reviewer/QE độc lập: kiểm tra correction/evidence theo tiêu chí; có quyền giữ FAIL/BLOCKED và yêu cầu bổ sung căn cứ; không thay đổi scope thay người có thẩm quyền.
- System/Platform Owner: xử lý dependency, permission, token, runtime và lỗi nền tảng; không quy các blocker hệ thống thành lỗi Agent.

Ủy quyền phải có dấu vết và phạm vi cụ thể. Không suy diễn quyền từ tên hiển thị hoặc lời tự khai identity.

## 9. Journal và evidence bắt buộc
Mỗi sự kiện có ý nghĩa phải ghi vào journal canonical của Work, tối thiểu:
- Timestamp/timezone; Work/assignment/WP; finding ID; actor/recipient và trust level của identity.
- Loại sự kiện; trạng thái trước/sau; căn cứ/nguồn/version; severity và lý do.
- Reminder/guidance/correction được gửi; phản hồi của Agent; checkpoint/deadline.
- Artifact/evidence link hoặc path; method/command/environment; kết quả PASS/FAIL/BLOCKED.
- Reviewer; quyết định; next step và owner.

Không ghi credential/secret vào journal. Không sửa/xóa evidence gốc để làm test pass; lưu input, output và hash/readback tách biệt khi phù hợp.

## 10. Tiêu chí chuyển trạng thái
- ASSIGNED → NEEDS_BRIEFING: assignment đã ghi nhận nhưng chưa đủ dữ liệu briefing thiết yếu (mục 2); không suy diễn nhận việc từ im lặng.
- NEEDS_BRIEFING → BRIEFED: đủ mục tiêu, scope, role, nguồn chuẩn, output, acceptance, checkpoint và journal path.
- BRIEFED → ACKNOWLEDGED: Agent phản hồi xác nhận hiểu nhiệm vụ/giới hạn/checkpoint; acknowledgement không đồng nghĩa đã thực thi.
- IN_PROGRESS → ON_TRACK: có artifact/progress evidence phù hợp checkpoint.
- IN_PROGRESS → AT_RISK: checkpoint/quality/dependency có dấu hiệu đe dọa deadline hoặc acceptance; nêu căn cứ.
- ANY → BLOCKED: có điều kiện tiên quyết/quyền/dependency thực sự ngăn tiến hành; xác định owner và điều kiện gỡ.
- ANY → DEVIATION_FOUND: có evidence cụ thể về sai lệch so với nguồn/tiêu chí.
- CORRECTION_SUBMITTED → RECHECK: correction và evidence đã được nộp đầy đủ để kiểm tra.
- RECHECK → VERIFIED_CLOSED: reviewer xác nhận đủ acceptance evidence và không còn tác động tồn dư.
- ANY → ESCALATED: có điều kiện escalation theo mục 11 và đã ghi rõ người nhận/quyết định cần xin.

Ghi chú đồng bộ (v0.2): REMINDED/COACHED trong ARCHITECT v1.1 và Biên bản v1.1 là nhãn sự kiện (reminder/guidance đã gửi), không phải trạng thái assignment độc lập; việc gửi reminder không đổi trạng thái, chỉ đổi trạng thái finding/reminder hiện hành. Cần đối chiếu lại khi ARCHITECT được truy vết tiếp.

## 11. Điều kiện escalation
Escalate khi có một trong các tình huống:
- S0 hoặc rủi ro S1 có khả năng gây tác động lớn.
- Vượt quyền, dùng identity không xác thực cho hành động nhạy cảm, hoặc cố ý né kiểm soát.
- Lặp lại cùng finding sau correction/recheck hoặc nhiều checkpoint không phản hồi theo thỏa thuận.
- Scope drift, tự ý thay đổi architecture/policy/permission/decision.
- Evidence có dấu hiệu bị sửa, giả mạo, không thể tái lập hoặc claim trạng thái sai có ảnh hưởng quyết định.
- Blocker vượt thẩm quyền Agent/Work Owner hoặc cần quyết định của Vinh.

Escalation là yêu cầu xem xét/quyết định, không tự động kết luận vi phạm. Giữ nguyên evidence và trạng thái chưa được xác minh.

## 12. Các điểm cần reviewer phản biện trước khi chốt
> Cập nhật v0.2: phản biện độc lập của Vibe đã ghi tại `02_DEFINE/VIBE_INDEPENDENT_REVIEW_PACKAGE.md` mục 9; câu hỏi 1, 3, 4, 7 đã xử lý bằng chỉnh sửa v0.2; câu hỏi 2, 5, 6 còn mở ở mức observation/defer.
1. Taxonomy đã bao phủ đủ lỗi nghiệp vụ ngoài ví dụ kỹ thuật của W802001 chưa?
2. Severity S0–S3 có ranh giới rõ và phù hợp các Work khác nhau không?
3. Cơ chế checkpoint/event-driven reminder có chống spam và xử lý múi giờ/Agent không hoạt động hợp lý không?
4. Phân quyền Xu, Work Owner, QE và Vinh có điểm nào chồng lấn hoặc vượt ủy quyền?
5. Evidence tối thiểu cho từng chuyển trạng thái đã đủ kiểm chứng và có thể tự động hóa về sau chưa?
6. Có cần phân biệt thêm lỗi vô ý, lặp lại do hướng dẫn kém, và hành vi cố ý không tuân thủ không? Không gắn nhãn động cơ nếu thiếu bằng chứng.
7. Quy trình xử lý finding liên quan đến nhiều Agent hoặc nhiều Work cần quy tắc liên kết nào?

## 13. Giới hạn và điều kiện phê duyệt
- Đây là DEFINE v0.3 đã qua phản biện độc lập của Vibe (ACCEPT WITH CHANGES) và được Vinh phê duyệt làm baseline nghiệp vụ ngày 2026-11-18.
- Không đặt SLA cố định, không tuyên bố tự động hóa, không mở BUILD.
- Phản biện độc lập đã hoàn tất tại `02_DEFINE/VIBE_INDEPENDENT_REVIEW_PACKAGE.md` §9; đính chính nguồn chuẩn tại §10. Vinh đã phê duyệt baseline v0.3; mọi thay đổi nội dung policy tiếp theo phải có decision/change record.
- Sau khi được duyệt, phải cập nhật Biên bản/decision canonical nếu có thay đổi quyết định; không tạo biên bản song song.
- Phê duyệt DEFINE không phải phê duyệt kiến trúc kỹ thuật, API, runtime, provider, lưu trữ, chi phí hoặc BUILD. ARCHITECT được phép khảo sát/thiết kế theo DOC-047; G2 chưa được tự động đánh dấu PASS. BUILD chỉ được xem xét sau khi ARCHITECT/PLAN hoàn tất, G4 PASS theo DOC-004 và có quyết định cho phép riêng.
