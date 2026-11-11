# LEGACY_NOTICE — C01 CONSOLIDATION

This file is retained as a legacy pointer; its prior content was preserved verbatim in the canonical Work 1111 record.

Canonical destination: `ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/00_ROOT/NHAT_KY_THI_CONG.md`
Original source path: `00_ROOT/NHAT_KY_THI_CONG.md`
Migration date: 2026-11-09 (UTC+7)
Migration task: W1111-C01

Do not append new records here. Continue in the canonical destination above. This notice does not delete the file or erase its history.


TÊN: Co
CHỨC DANH: Technical Execution Assistant / Coder W1111
NGÀY: 2026-11-10
GIỜ: 09h, UTC+7 (phút không được cung cấp)

C07 — PC READ-ONLY PEB PROBE UPDATE
Người dùng đã chạy probe cho PID 7940 và 1472. Cả hai trả về NOT_VERIFIED với cùng lỗi PowerShell: Cannot convert the "8" value of type System.Int32 to type System.UIntPtr. Nguyên nhân trực tiếp là các đối số độ dài dùng cú pháp [UIntPtr]8; chưa có thao tác đọc PEB thành công trong lần chạy này. Không kết luận lỗi quyền truy cập hoặc lỗi tiến trình.
Khắc phục: tạo biến $u8 = [UIntPtr]::new([uint64]8) rồi dùng $u8 thay cho cả ba vị trí [UIntPtr]8 (đọc ProcessParameters pointer, đọc UNICODE_STRING, đọc buffer đường dẫn). Để tránh PSReadLine ArgumentOutOfRangeException khi dán khối dài, chạy mã từ file .ps1 thay vì nhập/dán toàn bộ vào console.
Trạng thái: PID 7940 CWD NOT_VERIFIED; PID 1472 lần chạy hiện tại NOT_VERIFIED (không phủ nhận kết quả xác minh trước đó). Không thay đổi tiến trình, không restart, không gọi /execute, không đọc secrets. Module provenance vẫn là hạng mục riêng.

## 2026-11-12 00:50:55 UTC+7 — CO — SANDBOX → GITHUB DOCUMENTATION SYNC
- **Phạm vi:** Đồng bộ 27 tệp hồ sơ canonical của W1111 từ Sandbox `1111` sang repository `hqtt2026-thevinhvtqni/room-meeting-ai`, nhánh `work/w1111-core-execution-authority-v1-2`, dưới thư mục `work/1111/ROOM-HOP-TECHNICAL-ENGINEERING-AND-DEBUG-LAB/`.
- **Nội dung:** 00_ROOT (6 tệp), 01_DISCOVER (2), 02_EXTENSION (7), 03_ARCHITECTURE (3), 04_CODE (1), 05_TEST (1), 06_EVIDENCE (7). Bao gồm nhật ký, manifest, quy tắc, biên bản, kế hoạch, phê duyệt, baseline, phân công 3 Agent, kiến trúc, patch/test và evidence C02/C07/Co/Vi/PC.
- **Kết quả ghi GitHub:** 27/27 tệp được tạo/cập nhật thành công qua GitHub Contents API; không ghi main, không merge PR #48, không deploy.
- **Commit cuối của đợt đồng bộ hồ sơ:** `c55bfe8b347eed86035eacd6be2641dc74358784`.
- **Lưu ý:** Đây là đồng bộ hồ sơ Sandbox → GitHub. Chưa phải xác nhận source code runtime parity, CI PASS hay E2E PASS. Trạng thái W1111 tiếp tục BLOCKED / NOT VERIFIED cho đến khi có bằng chứng các gate còn thiếu.
