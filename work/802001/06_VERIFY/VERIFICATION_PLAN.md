# KẾ HOẠCH KIỂM CHỨNG / VERIFICATION PLAN — WORK 802001

- Version: 1.1
- Status: PLANNED — TESTS NOT RUN
- Governing standard: Work 70
- Scope: Agent Work Supervision & Guidance

## Nhóm kiểm chứng nghiệp vụ
1. Assignment briefing: Agent nhận đúng Work/WP, scope, vai trò, deliverable, deadline, canonical sources và journal requirement.
2. Acknowledgement: ghi nhận Agent đã nhận/hiểu; phát hiện hiểu sai trước khi làm việc rủi ro.
3. Checkpoint monitoring: trạng thái được cập nhật đúng mốc, đúng nguồn, freshness hiển thị rõ.
4. Early warning: phát hiện sắp trễ, không cập nhật, dependency blocked hoặc dấu hiệu lệch scope.
5. Deviation detection: phát hiện bỏ bước, sai cấu trúc, dùng sai source, thiếu journal/evidence, báo cáo không khớp thực tế.
6. Reminder quality: reminder có căn cứ, người nhận, việc cần làm, deadline; không spam hoặc nhắc trùng vô nghĩa.
7. Guided correction: chỉ đúng quy tắc, source/path, trình tự sửa, output cần nộp và điều kiện recheck.
8. Correction tracking: lưu phản hồi và evidence mới; không tự đóng finding chỉ bằng lời Agent.
9. Independent recheck: kiểm tra đúng tiêu chí; finding chỉ đóng khi evidence hỗ trợ.
10. Escalation: lỗi lặp, quá hạn, no-response, vượt quyền hoặc critical risk được chuyển đúng cấp.
11. Journal integrity: mọi lần theo dõi/nhắc/hướng dẫn/sửa/recheck có timestamp, actor, scope, method, evidence, status và next step.
12. W70 conformance: không tạo state/lifecycle/Gate trùng hoặc mâu thuẫn W70.

## Tình huống bắt buộc
- Agent bắt đầu làm khi chưa đọc nguồn chuẩn.
- Agent tự ý mở rộng scope hoặc tạo cấu trúc sai.
- Agent báo hoàn thành nhưng artifact/evidence chưa có.
- Agent trễ checkpoint hoặc im lặng.
- Agent lặp lại lỗi sau khi đã được hướng dẫn.
- Agent không hiểu hướng dẫn hoặc source đã stale.
- Agent sửa đúng nhưng không ghi nhật ký/readback.
- Agent gặp blocker ngoài quyền xử lý và cần escalation.
- Agent cố thực hiện hành động có rủi ro khi đã được yêu cầu dừng.

## Kết quả
Mỗi test phải có environment, assignment, actor, source/policy version, precondition, method, expected/actual, evidence và reviewer. NOT_RUN/NOT_VERIFIED/BLOCKED phải giữ nguyên nếu chưa có kiểm thử thực tế. Kế hoạch không phải bằng chứng hệ thống đã tự động giám sát Agent.
