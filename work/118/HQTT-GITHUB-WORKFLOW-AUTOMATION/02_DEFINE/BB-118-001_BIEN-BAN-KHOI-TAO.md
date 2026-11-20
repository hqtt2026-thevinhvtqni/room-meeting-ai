# BB-118-001 — BIÊN BẢN KHỞI TẠO WORK 118

- **Work:** W118 — HQTT GitHub Workflow Automation
- **Issue:** #65
- **Ngày:** 2026-11-20
- **Trạng thái:** DRAFT / BASELINE — chưa phải biên bản kiến trúc được phê duyệt

## 1. Bối cảnh
Qua trao đổi về GitHub, nhận thấy Issue (giao việc) và Push (đưa commit lên repository) đã có nhưng chưa tạo thành một chuỗi hành động tự động, có người/AI chịu trách nhiệm và bằng chứng xuyên suốt.

## 2. Mục tiêu khởi tạo
Thiết kế cơ chế liên kết và điều phối:
Issue → Assignment → Branch → Commit/Push → CI → xử lý FAIL hoặc Review → Acceptance → Merge → Nhật ký/Dashboard.

## 3. Quyết định phạm vi ban đầu
- Tạo W118 độc lập để nghiên cứu và xây dựng cơ chế dùng chung cho HQTT.
- Tham chiếu chuẩn vòng đời Work 70; không thay thế hoặc sao chép chức năng Work 70.
- Giai đoạn đầu chỉ khảo sát, định nghĩa và thiết kế.
- Chưa triển khai webhook, token/secret, thay đổi quyền, branch protection hay tự động merge.
- Mọi kết quả phải ghi trong Nhật ký W118 kèm thời gian, phạm vi, phương pháp, bằng chứng và trạng thái.

## 4. Các câu hỏi thiết kế cần giải quyết
1. Sự kiện Issue được tạo/gán/đổi trạng thái sẽ kích hoạt điều gì và ai là actor?
2. Làm sao xác nhận đúng AI nhận việc, không chỉ dựa trên GitHub assignee?
3. Push/commit được liên kết với Issue và Work bằng quy ước nào?
4. CI workflow nào chạy ở Push và Pull Request; cách lưu log, SHA, exit code?
5. Khi CI FAIL, ai nhận nhiệm vụ sửa, giới hạn retry và cách chống vòng lặp?
6. Khi CI PASS, điều kiện review độc lập và nghiệm thu là gì?
7. Webhook/API gửi sự kiện về ROOM-HOP ra sao; xác thực chữ ký, quyền tối thiểu, chống replay/duplicate thế nào?
8. Làm sao đồng bộ trạng thái về Work Journal và Dashboard mà không tạo nguồn sự thật trùng lặp?

## 5. Trạng thái
**DISCOVER / DEFINE — IN PROGRESS.** Chưa có kết luận về khả năng tích hợp end-to-end và chưa có kiểm thử vận hành.
