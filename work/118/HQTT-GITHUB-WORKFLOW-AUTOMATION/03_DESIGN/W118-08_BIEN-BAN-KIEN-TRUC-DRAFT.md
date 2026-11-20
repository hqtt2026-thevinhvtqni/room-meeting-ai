# W118-08 — PHẢN BIỆN VÀ BIÊN BẢN KIẾN TRÚC (BẢN DỰ THẢO CỦA VIBE)

- **Work:** W118 (Issue #65) · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT — chờ phản biện chéo Ka/Xu và phê duyệt Vinh

## 1. Trả lời 8 câu hỏi BB-118-001

1. **Kích hoạt sự kiện:** Polling-driven ROOM-HOP (khả thi ngay); webhook BLOCKED chờ pilot — do connector không có tool Actions/Webhooks.
2. **AI nhận việc:** Đổi label \`status/in-progress\` + comment có evidence (timestamp, kế hoạch ngắn); idempotency key \`<issue>#<bước>\`.
3. **Quy ước commit:** \`<type>(w<số>): ... (refs #issue)\` + body \`actor/intent/evidence\`.
4. **Evidence:** EVIDENCE_REGISTER.json schema v1.1; không ghi PASS khi thiếu run URL + SHA + logs.
5. **CI FAIL:** phân loại intentional debt vs lỗi thực; tối đa 2 retry rồi \`blocked\` + debt.
6. **Review/merge:** Gates G0..G5; reviewer độc lập; không auto-merge.
7. **Webhook:** BLOCKED, thay bằng polling; ghi limitations.
8. **Dashboard sync:** Dashboard chỉ đọc EVIDENCE_REGISTER + labels.

## 2. Rủi ro chính và biện pháp

| Rủi ro | Ảnh hưởng | Biện pháp |
|---|---|---|
| Polling có độ trễ | Phản ứng chậm | Chấp nhận cho DESIGN; W118-09 đo độ trễ trong pilot |
| Thiếu quyền admin (branch protection, job log) | Merge gate không ép buộc | Ghi limitation; Vinh cân nhắc cấp quyền nếu chốt G5 |
| State machine sinh fix-issue lặp cho intentional FAIL | Nhiễu | Idempotency + label \`type/debt\` (W118-05) |
| AI vượt thẩm quyền mutation | Vi phạm nguyên tắc Work 103 | G3/G5 chốt thẩm quyền trước BUILD |

## 3. Điểm chờ Ka/Xu phản biện

- Có chấp nhận polling thay webhook giai đoạn đầu?
- EVIDENCE_REGISTER dùng chung nhiều Work có xung đột ghi?
- Bộ label có cần chuẩn hóa toàn repo trước khi mở rộng cho W15/17/21?

## 4. Điều kiện chuyển G3

- Ka/Xu xác nhận phản biện (ít nhất 3 điểm trên).
- Vinh phê duyệt kiến trúc trực tiếp trên Issue #65.
