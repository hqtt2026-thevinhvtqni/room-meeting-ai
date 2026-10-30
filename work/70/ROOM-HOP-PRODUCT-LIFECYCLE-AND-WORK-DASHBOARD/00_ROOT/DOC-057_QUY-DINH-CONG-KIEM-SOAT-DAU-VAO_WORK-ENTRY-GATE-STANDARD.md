# QUY ĐỊNH CỔNG KIỂM SOÁT ĐẦU VÀO WORK / WORK ENTRY GATE STANDARD
- **STT / Document ID:** DOC-057
- **Priority:** P0
- **Read order:** 57
- **Depends on:** DOC-001; DOC-002; DOC-004; DOC-005; DOC-033; DOC-038; DOC-039; DOC-040; DOC-042; DOC-043; DOC-044; DOC-055; DOC-056
- **Status:** ACTIVE — POLICY APPROVED / ENFORCEMENT IMPLEMENTATION REQUIRED
- **Version / Updated:** 1.0 / 2026-10-31
- **Owner:** Xu / AI-01
- **Authority:** Vinh

## 1. Mục đích và quyết định bắt buộc

WORK ENTRY GATE là cổng xác minh điều kiện tham gia Work trước khi AI hoặc con người thực hiện bất kỳ thay đổi sản phẩm nào thuộc phạm vi kiểm soát.

Nguyên tắc:
1. Không có Work Entry PASS hợp lệ thì không được bắt đầu thực thi chính thức.
2. Không có bằng chứng kiểm tra được thì không được đánh dấu PASS.
3. BLOCKED phải giải thích nguyên nhân và hướng dẫn khắc phục cụ thể.
4. Kiểm soát phải đúng phạm vi: không khóa các hoạt động đọc, tìm hiểu, thu thập bằng chứng hoặc khắc phục vốn được phép.
5. Quyền thực thi phải được kiểm tra tại lớp công cụ/hệ thống; tài liệu hoặc lời cam kết đơn thuần không chứng minh được enforcement.
6. Quy định này áp dụng chung cho mọi Work và mọi AI/person tham gia; Work-specific rules có thể bổ sung nhưng không được hạ chuẩn.

## 2. Phạm vi và phân biệt hoạt động

### 2.1 Hoạt động chuẩn bị được phép khi chưa PASS
Nếu quyền truy cập cho phép, người tham gia có thể:
- Xác định Work, tìm kiếm và đọc tài liệu.
- Đọc trạng thái, nhật ký, quyết định, phân công.
- Kiểm tra quyền truy cập ở chế độ chỉ đọc.
- Thu thập bằng chứng, lập checklist dự thảo và báo cáo thiếu sót.
- Thực hiện các bước khắc phục để hoàn thành Gate.

Các hoạt động trên không được làm thay đổi sản phẩm, cấu hình, dữ liệu vận hành hoặc trạng thái chính thức của Work.

### 2.2 Hoạt động bị kiểm soát cho đến khi PASS
Trừ khi có quyền khẩn cấp riêng được phê duyệt và ghi log, không được:
- Tạo/sửa/xóa/di chuyển artifact chính thức hoặc mã nguồn.
- Ghi dữ liệu hoặc thay đổi trạng thái Work/WP.
- Chạy triển khai, migration, release hoặc thao tác có tác động môi trường.
- Thay đổi quyền, cấu hình, hợp đồng API hoặc quyết định đã khóa.
- Thực hiện thao tác vượt nhiệm vụ hoặc phạm vi được giao.

Chỉ đọc không đồng nghĩa với quyền ghi. Có quyền dùng công cụ không đồng nghĩa có quyền dùng công cụ cho mọi Work.

## 3. Sáu Gate bắt buộc

Mỗi AI/person phải hoàn thành riêng cho từng Work và từng assignment. PASS của một người không chuyển nhượng cho người khác.

| Gate | Nội dung | Bằng chứng tối thiểu | Điều kiện PASS |
|---|---|---|---|
| G0 | Nhận diện Work, chủ sở hữu, nguồn làm việc | Work ID/name, Manifest, Sandbox/repository/branch, authority | Khớp Work được giao và nguồn chuẩn |
| G1 | Đọc quy trình, quy định, hướng dẫn áp dụng | Danh sách tài liệu, canonical path, version/commit, nội dung yêu cầu liên quan | Đọc được và hiểu các quy trình bắt buộc |
| G2 | Đọc tiêu chuẩn tài liệu và đăng ký | Naming/type-code standards, official code register, Document Register, storage standard | Xác định được cách đặt mã/tên, nơi lưu, đăng ký và ngoại lệ |
| G3 | Đọc trạng thái và lịch sử hiện hành | Manifest/state, Decision Log, Execution Log, minutes, evidence/status liên quan | Nắm đúng trạng thái, việc mở, blocker và quyết định còn hiệu lực |
| G4 | Xác minh phân công, quyền và phụ thuộc | Assignment contract, role matrix, scope, owner, dependencies, tool permissions | Nhiệm vụ rõ, quyền đủ và không vượt giới hạn |
| G5 | Xác nhận sẵn sàng thực hiện | Entry checklist, tóm tắt phạm vi, kế hoạch, tiêu chí hoàn thành, risk/rollback khi cần | Tất cả G0–G4 PASS; không còn mâu thuẫn/blocker đầu vào |

Không được gộp bằng chứng của nhiều Gate thành một câu xác nhận chung. Gate không áp dụng phải ghi N/A kèm lý do và người có thẩm quyền xác nhận; không được tự bỏ qua.

## 4. Bản ghi Work Entry bắt buộc

Mỗi lần tham gia phải tạo một bản ghi có tối thiểu:
- Work ID và tên Work.
- AI/person ID, vai trò, người giao việc và người có thẩm quyền.
- Assignment ID, mục tiêu, phạm vi được phép và phạm vi cấm.
- Repository/Sandbox, canonical source, branch/ref và commit/version đã kiểm tra.
- Danh sách Gate G0–G5, trạng thái từng Gate, bằng chứng, thời điểm và người xác minh.
- Checklist tuân thủ trước thực thi.
- Quyết định cuối: PASS hoặc BLOCKED.
- Quyền được cấp, giới hạn thao tác, thời hạn/điều kiện hết hiệu lực.
- Các thay đổi/phạm vi khiến phải xác minh lại.

Bản ghi phải được lưu tại vị trí Work quy định, đăng ký theo DOC-055 và ghi tham chiếu trong DOC-035. Không được ghi bí mật, token hoặc thông tin xác thực vào bằng chứng.

## 5. Quy tắc PASS, BLOCKED và hướng dẫn khắc phục

### 5.1 PASS
Chỉ được cấp khi đủ bằng chứng cho G0–G5 và xác minh không có xung đột quyền/phạm vi. PASS phải gắn với đúng Work + participant + assignment + scope + source revision. PASS không phải quyền vô thời hạn hoặc quyền tổng quát.

### 5.2 BLOCKED — bắt buộc giải thích và chỉ đường
Mọi phản hồi BLOCKED phải có đủ:
1. **Rule:** Quy định/Gate/điều kiện chưa đạt.
2. **Reason:** Lý do cụ thể.
3. **Evidence:** Bằng chứng thiếu, sai hoặc mâu thuẫn.
4. **Impact:** Rủi ro nếu tiếp tục.
5. **Allowed now:** Việc vẫn được phép làm trong lúc bị chặn.
6. **Remediation:** Các bước khắc phục theo thứ tự, có đường dẫn/tài liệu/công cụ khi biết.
7. **Owner:** Ai chịu trách nhiệm khắc phục hoặc quyết định.
8. **Verification:** Ai/công cụ nào kiểm tra lại và kiểm tra gì.
9. **Exit condition:** Điều kiện cụ thể để mở Gate.

Không dùng thông báo cụt như “không đủ quyền”, “thiếu tài liệu”, “hãy thử lại” mà không hướng dẫn bước tiếp theo. Nếu chưa biết cách khắc phục, phải nói rõ điều chưa biết, chỉ ra thông tin cần tìm và người có thể quyết định; không tự bịa hướng dẫn.

### 5.3 Ít hạn chế nhất nhưng vẫn an toàn
Chỉ chặn thao tác có rủi ro hoặc vượt quyền. Không chặn đọc, phân tích, thu thập bằng chứng và các bước khắc phục hợp lệ. Phải nêu rõ hoạt động nào được phép và hoạt động nào chưa được phép.

## 6. Work Entry Authorization — cấp quyền thực thi

Mục tiêu kiến trúc là lớp thực thi kiểm tra quyền trước mỗi thao tác bị kiểm soát. Authorization phải ràng buộc:
- Work ID.
- Participant/AI ID và role.
- Assignment ID.
- Allowed actions và resource/path scope.
- Source revision/branch khi phù hợp.
- Thời hạn hoặc điều kiện hết hiệu lực.
- Evidence/decision ID của Work Entry PASS.

Từ chối mặc định (fail closed) khi thiếu, hết hạn, sai Work, sai participant, sai assignment, sai scope hoặc không xác minh được authorization. Mỗi lần từ chối phải trả về mã lỗi ổn định, lý do dễ hiểu và remediation theo Mục 5.2.

Khi assignment, scope, role, source revision hoặc quyết định nền thay đổi đáng kể, phải đánh giá lại Gate liên quan và thu hồi/cấp lại authorization nếu cần.

**Giới hạn hiện trạng:** Việc ban hành DOC-057 không tự tạo enforcement kỹ thuật. Cho đến khi các công cụ ghi/sửa/triển khai được tích hợp kiểm tra authorization và có negative-test evidence, trạng thái phải ghi POLICY ACTIVE / TECHNICAL ENFORCEMENT NOT VERIFIED. Không được tuyên bố AI bị ngăn tuyệt đối chỉ vì có tài liệu này.

## 7. Vai trò và phân tách trách nhiệm

- **Vinh:** thẩm quyền cuối cùng theo Manifest; phê duyệt các quyết định thuộc quyền Product Owner.
- **Xu / AI-01:** duy trì chuẩn, điều phối entry, xác định tài liệu áp dụng, ghi nhận quyết định và theo dõi enforcement.
- **Ka / AI-02:** kiểm tra độc lập về kiến trúc và tuân thủ; phải tự qua Gate như mọi participant; không tự miễn trừ hoặc tự cấp quyền cho chính mình.
- **Coder:** xác nhận entry, chỉ sửa trong assignment/scope được cấp.
- **Tester/QE:** kiểm tra sản phẩm, bằng chứng Gate, negative cases và việc thực thi quyền; không sửa implementation để làm cho test PASS.
- **Execution Layer:** xác minh authorization trước thao tác được bảo vệ; ghi audit event và trả hướng khắc phục.
- Người tạo bằng chứng không được tự xác nhận độc lập cho chính bằng chứng đó khi yêu cầu kiểm tra độc lập.

## 8. Khi nào phải chạy lại Work Entry

Phải tạo entry mới hoặc tái xác minh phần bị ảnh hưởng khi:
- Participant hoặc vai trò thay đổi.
- Assignment, phạm vi, resource/path hoặc quyền thay đổi.
- Chuyển Work, repository, branch hoặc canonical source.
- Có quyết định mới làm thay đổi quy trình, tiêu chuẩn hoặc trạng thái.
- Authorization hết hạn/bị thu hồi.
- Phát hiện bằng chứng cũ sai, thiếu hoặc không còn đáng tin cậy.

## 9. Quy trình thao tác dành cho AI/person

1. Dừng thao tác làm thay đổi sản phẩm; xác định Work ID và assignment.
2. Đọc Manifest và Document Register để tìm đúng tài liệu chuẩn.
3. Đọc đủ tài liệu theo G0–G4; ghi lại canonical path và version/commit.
4. Nếu không tìm thấy, tìm trong register, alias, manifest và mapping; không kết luận “không tồn tại” chỉ từ một lần tìm.
5. Nếu không đọc được hoặc nguồn mâu thuẫn: BLOCKED, báo bằng chứng và yêu cầu đúng owner xử lý; không suy diễn.
6. Lập checklist G5, khai báo phạm vi được phép/cấm và rủi ro.
7. Gửi bản ghi để xác minh; chỉ khi có quyết định PASS hợp lệ mới bắt đầu thao tác bị kiểm soát.
8. Trước mỗi thao tác được bảo vệ, Execution Layer phải kiểm tra authorization.
9. Ghi nhật ký kết quả, thay đổi, lỗi, blocker và bằng chứng; khi hoàn tất assignment, đóng/thu hồi quyền phù hợp.

## 10. Kế hoạch kiểm chứng enforcement

Tối thiểu phải có kiểm thử:
- Không có entry: thao tác ghi/sửa/triển khai bị từ chối.
- G0–G5 chưa đủ hoặc thiếu evidence: bị từ chối.
- PASS của AI A không dùng được cho AI B.
- PASS của Work A không dùng được cho Work B.
- Assignment/scope/path không khớp: bị từ chối.
- Authorization hết hạn/thu hồi: bị từ chối.
- Read-only và remediation hợp lệ vẫn hoạt động.
- BLOCKED trả đủ reason, evidence, allowed actions, remediation, owner và exit condition.
- Audit log ghi được quyết định cấp/từ chối và actor/resource/action.
- Race/replay/idempotency không cho tái sử dụng quyền sai ngữ cảnh.

Chỉ báo TECHNICAL ENFORCEMENT PASS khi negative tests và positive/remediation tests chạy trên đường thực thi thật, có kết quả và QE độc lập. Nếu mới có mock/unit tests, phải ghi rõ phạm vi mock; không tuyên bố đã khóa công cụ production.

## 11. Ví dụ phản hồi

**BLOCKED — G2 chưa đạt**

- Rule: DOC-038 và DOC-055 yêu cầu dùng canonical filename và path đã đăng ký.
- Reason: Chưa xác minh được canonical path của artifact.
- Evidence: Register có hai candidate path, chưa có mapping được phê duyệt.
- Impact: Có thể tạo bản trùng hoặc ghi nhầm nguồn.
- Allowed now: Đọc hai candidate, kiểm tra mapping và inbound links.
- Remediation: Đối chiếu Manifest → DOC-055 → mapping register; yêu cầu owner xác nhận path còn thiếu.
- Owner: Xu / owner tài liệu.
- Verification: Ka hoặc QE kiểm tra mapping và readback.
- Exit condition: Một canonical path được xác nhận, đăng ký và đọc lại thành công; G2 được đánh giá lại.

## 12. Chỉ số trạng thái và báo cáo

Dùng đúng các trạng thái:
- NOT_STARTED: chưa thực hiện entry.
- IN_PROGRESS: đang kiểm tra Gate.
- BLOCKED: thiếu điều kiện; phải có remediation.
- PASS: đủ bằng chứng và được xác minh.
- REVOKED/EXPIRED: quyền không còn hiệu lực.
- NOT_VERIFIED: chưa có kiểm chứng kỹ thuật độc lập.

Không dùng DONE/PASS cho policy, authorization hoặc enforcement nếu chỉ mới tạo tài liệu. Tách rõ POLICY APPROVED, PROCESS OPERATING, TECHNICAL ENFORCEMENT VERIFIED.

## 13. Quan hệ tài liệu và hiệu lực

DOC-057 là chuẩn P0 dùng chung cho tất cả Work. DOC-002 phải dẫn chiếu quy định này trong intake; DOC-042 áp dụng nó trong điều phối; DOC-043 ràng buộc role/permission; DOC-044 chứa trường Work Entry evidence/decision; DOC-055 đăng ký mọi bản ghi/tài liệu chính thức theo quy tắc tài liệu.

Work 70 phải áp dụng ngay cho mọi assignment mới và mọi assignment chưa bắt đầu thực thi. Không hồi tố hợp thức hóa thay đổi đã thực hiện trước khi có Gate; các trường hợp đó phải được rà soát và ghi nhận trung thực.

Mọi thay đổi DOC-057 phải qua versioning, decision log, document register, execution log và verification theo các chuẩn hiện hành.
