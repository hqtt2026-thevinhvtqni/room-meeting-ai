# QUY ĐỊNH LÀM VIỆC AI — WORK 1111

1. Tự đọc registry, hồ sơ, source và nhật ký trước khi hỏi người dùng.
2. Tra cứu identity chính xác trong registry (ví dụ agents/*.yaml); không đoán ID, không dùng tên vai trò thay identity.
3. Không hỏi lại dữ kiện đã có trong lịch sử, hồ sơ hoặc hệ thống có thể truy cập.
4. Khi được giao toàn quyền trong phạm vi nhiệm vụ: chủ động READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF; không dừng ở việc nêu phương án hoặc yêu cầu người dùng làm hộ thao tác AI có thể tự thực hiện.
5. Ghi mọi lần kiểm tra, command/method, thời gian, phạm vi, bằng chứng và trạng thái vào 00_ROOT/NHAT_KY_THI_CONG.md hoặc nhật ký chuyên đề được liên kết.
6. Chỉ dùng DONE/PASS khi có bằng chứng; nếu thiếu điều kiện ghi BLOCKED và nêu vấn đề, lần thử/evidence, bottleneck, phương án và điều kiện còn thiếu.
7. Không lặp thao tác đã có kết quả, trừ khi có thay đổi hoặc bằng chứng lỗi mới.
8. Không tự ý sửa source chuẩn, commit/push hoặc thay đổi Work ngoài phạm vi được giao.
9. Không nhân bản tài liệu; một tài liệu có một vị trí chuẩn.
10. Bàn giao nêu rõ thay đổi, file/path, kiểm thử, evidence, trạng thái và rủi ro còn lại.

## Xử lý blocker
Trước khi báo BLOCKED, tự tìm cách tháo gỡ trong quyền và công cụ hiện có. Không chuyển việc tra cứu nội bộ hoặc dữ kiện đã lưu thành câu hỏi cho người dùng.
