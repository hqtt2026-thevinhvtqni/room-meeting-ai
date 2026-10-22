# HARNESS² — ĐÁNH GIÁ, RÚT KINH NGHIỆM VÀ HỌC TẬP CHO HQTT AI

- Work: 19 — Cấu trúc học tập
- Ngày ghi nhận: 2026-10-22
- Trạng thái: RESEARCH / DESIGN ONLY
- Nguồn tham khảo: https://github.com/google-research/harness2
- Phạm vi: Học nguyên lý; KHÔNG nhúng Harness² vào ROOM-HOP, KHÔNG triển khai framework mới ở giai đoạn này.

## 1. Mục tiêu học tập

Nghiên cứu cách Harness² tiếp cận việc cải thiện harness của AI Agent; rút ra các nguyên lý có thể chuyển hóa thành năng lực nội tại của HQTT AI. Mục tiêu không phải sao chép hoặc cài một hệ thống vào hệ thống hiện có, mà học cách thiết kế vòng phản hồi để AI đề xuất, thử nghiệm, đánh giá và tích lũy bài học có kiểm chứng.

## 2. Tóm tắt nguyên lý đáng học

Mô hình khái niệm tham khảo:
1. **Propose — Đề xuất:** sinh giả thuyết cải tiến cho prompt, chỉ dẫn công cụ, Skills hoặc quy trình.
2. **Probe — Thử nghiệm:** chạy ứng viên trong điều kiện có kiểm soát, thu kết quả và bằng chứng.
3. **Compose — Tổng hợp:** so sánh kết quả, chọn lọc các thay đổi có ích và ghi lại bài học tái sử dụng.

Lưu ý: khác biệt giữa các lần chạy tự nó không chứng minh kết quả nào đúng. Cần tiêu chí đánh giá phù hợp với nhiệm vụ, kiểm thử độc lập và kiểm soát hồi quy.

## 3. Đánh giá phù hợp với HQTT

### Có giá trị cao
- Biến kinh nghiệm sau mỗi nhiệm vụ thành giả thuyết cải tiến có thể kiểm thử.
- Thử nhiều phương án trong môi trường tách biệt trước khi sử dụng.
- Đánh giá bằng kết quả nhiệm vụ, độ tin cậy, số lỗi, số lần hỏi lại, thời gian và khả năng chuyển giao sang nhiệm vụ khác.
- Lưu cả điều kiện áp dụng, giới hạn, bằng chứng và trường hợp thất bại; không chỉ lưu kết luận thành công.
- Tách quyền đề xuất cải tiến khỏi quyền phê duyệt và triển khai.

### Không nên bê nguyên
- Không đưa nguyên Harness² hoặc một framework khác vào ROOM-HOP chỉ vì có tính năng hấp dẫn.
- Không thêm dịch vụ, runtime, cơ sở dữ liệu hoặc lớp điều phối mới nếu cơ chế hiện có đáp ứng được.
- Không cho AI tự sửa Core, quyền hạn, bảo mật hoặc môi trường production.
- Không xem kết quả do chính AI tạo ra là bằng chứng độc lập đủ để PASS.
- Không mở rộng phạm vi Work 19 thành một dự án code/runtime mới.

## 4. Bài học rút kinh nghiệm

1. **Học nguyên lý, không nhập hệ thống:** chỉ tiếp nhận khái niệm và cơ chế đã chứng minh giá trị; thiết kế phù hợp kiến trúc HQTT.
2. **Tối ưu bằng bằng chứng:** mọi cải tiến phải có baseline, bộ nhiệm vụ đánh giá, tiêu chí đo và kết quả so sánh trước/sau.
3. **Giữ ranh giới đề xuất–thử nghiệm–phê duyệt–triển khai:** AI có thể đề xuất và thử trong vùng an toàn; quyền triển khai phải theo chính sách phê duyệt.
4. **Bài học phải có thể truy xuất:** ghi nguồn, phiên bản, nhiệm vụ, môi trường, kết quả, giới hạn và lý do chọn/bác bỏ.
5. **Đo chuyển giao:** một cải tiến chỉ hữu ích bền vững khi cải thiện được nhiệm vụ mục tiêu mà không làm giảm chất lượng nhiệm vụ khác.
6. **Không tự tuyên bố thành công:** trạng thái PASS cần bằng chứng kiểm tra; thiếu bằng chứng là BLOCKED/NOT VERIFIED.
7. **Ưu tiên tận dụng năng lực sẵn có:** trước tiên thử trên quy trình Skills và hướng dẫn công cụ; chưa tạo lớp hệ thống mới.

## 5. Hướng ứng dụng nội bộ đề xuất (chưa triển khai)

Thử nghiệm quy trình học tập nhỏ, không phải framework mới:

READ → TRACE → ANALYZE → PROPOSE → TEST IN ISOLATED CONTEXT → EVALUATE → RECORD LESSON → APPROVAL → OPTIONAL ADOPTION

Mỗi thử nghiệm ghi:
- Vấn đề và baseline;
- Giả thuyết thay đổi;
- Nhiệm vụ kiểm thử và tiêu chí đạt;
- Kết quả trước/sau, lỗi phụ và bằng chứng;
- Phạm vi áp dụng, giới hạn và khả năng hồi quy;
- Quyết định: ADOPT / REVISE / REJECT / BLOCKED;
- Người/AI đề xuất, người/AI đánh giá, người phê duyệt và thời điểm.

## 6. Thứ tự ưu tiên học tập

1. Tool guidance — cải thiện việc chọn và gọi đúng công cụ.
2. Skills / workflow instructions — cải thiện quy trình làm việc và giảm hỏi lại không cần thiết.
3. Scripts / kiểm thử — tự động hóa kiểm tra có thể lặp lại.
4. Memory / experience library — chỉ lưu bài học đã kiểm chứng, có phạm vi và điều kiện áp dụng rõ.
5. Các thành phần nhạy cảm như guardrails, quyền hạn, runtime — chỉ nghiên cứu; không tự động sửa đổi.

## 7. Điều kiện để chuyển sang triển khai

Chỉ lập nhiệm vụ triển khai khi:
- Có một vấn đề cụ thể và số liệu/bằng chứng baseline;
- Có thử nghiệm nhỏ chứng minh lợi ích;
- Không trùng lặp năng lực hiện có;
- Có kiểm thử hồi quy, cách rollback và chủ sở hữu;
- Phạm vi thay đổi được anh Vinh phê duyệt.

## 8. Kết luận

Harness² là nguồn học tập để tham khảo cách tạo vòng cải tiến có phản hồi. Định hướng HQTT là xây năng lực tự cải thiện bằng các cơ chế nội tại, tích hợp vào quy trình hiện có khi cần — không nhúng một hệ thống vào một hệ thống. Hiện tại đây là tài liệu nghiên cứu/thiết kế; chưa có bằng chứng triển khai hay đo hiệu quả thực tế, vì vậy không đánh dấu implementation PASS.

## 9. Nhật ký
- 2026-10-22 — Xu ghi nhận theo yêu cầu của anh Vinh: đưa Harness² vào Work 19 để đánh giá và rút kinh nghiệm học tập; giữ nguyên tắc học hỏi, không sao chép/nhúng hệ thống.
