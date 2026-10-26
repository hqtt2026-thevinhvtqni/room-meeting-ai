# v5 FIX GOVERNANCE G1-G5 - Theo báo cáo Xu

## Đã fix theo quyết định NOT ACCEPTED của Xu

### G1: Đồng bộ TurnResult, MeetingContext và contract - FIXED
- Lỗi cũ: TurnResult thiếu trường status gây TypeError
- Fix: Thêm status vào TurnResult với default COMPLETED, các giá trị: REQUESTED | PROCESSING | COMPLETED | FAILED | BLOCKED
- Thêm correlation_id, verified vào TurnResult
- MeetingContext thêm correlation_id, previous_output
- File: connectors/base.py

### G2: Chạy lại gói nguyên bản, không monkey-patch - FIXED
- Đảm bảo demo.py chạy được gói nguyên bản
- Không sửa code lúc chạy
- Test: python -m compileall và python demo.py phải PASS

### G3: Kiểm thử dependency, xác minh lượt và evidence - FIXED
- Trước: verification dùng OR giữa TURN_ID, CORRELATION_ID, VERIFIED -> yếu
- Sau: Yêu cầu BẮT BUỘC cả TURN_ID và CORRELATION_ID phải có trong file inbox
- Chỉ có VERIFIED mà không có 2 ID -> FAILED
- Thêm chống đọc lại: move file sang inbox/processed/ sau khi đọc
- Thêm kiểm tra: nội dung >=20 ký tự, chống phản hồi cũ, sai lượt
- Test trong demo.py: test case chỉ có VERIFIED phải FAILED, test đủ 2 ID phải COMPLETED

### G4: Phân loại 24 tool - FIXED
- Thêm TOOL_CATEGORIES:
  * core_image: 10 tool gốc Magnific - execution generic_manual
  * website: 4 tool website - execution specialized
  * image_edit: 4 tool cắt ghép ảnh - specialized
  * video_edit: 6 tool cắt ghép video - specialized
- Factory create_connector() phân loại rõ tool nào dùng logic chung, tool nào chuyên biệt
- Không còn tuyên bố cả 24 tool đều specialized khi thực tế dùng chung logic

### G5: Kiểm thử với Core thật - BLOCKED đúng governance
- Không tự tuyên bố tương thích Core khi chưa có bằng chứng
- Để BLOCKED chờ Core thật

## Cách test v5
```bash
python -m compileall -q .  # G1
python demo.py  # G2, G3, G4
```
Kết quả mong đợi:
- G1 PASS
- G2 PASS
- G3 PASS (test VERIFIED fail, test đủ ID pass)
- G4 PASS
- G5 BLOCKED (đúng)
