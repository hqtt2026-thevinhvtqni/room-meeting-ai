# W118-06 — THIẾT KẾ REVIEW / ACCEPTANCE / MERGE GATES

- **Work:** W118 (Issue #65) · Xử lý Gap #4 · **Ngày:** 2026-11-20 (UTC+07) · **Trạng thái:** DRAFT chờ phản biện

## 1. Gate matrix

| Gate | Điều kiện pass | Ai duyệt | Bằng chứng |
|---|---|---|---|
| G0 Kiểm kê | Hiện trạng + gaps thống kê xong | Vibe + Xu xác nhận | W118-01 + Entry 002 |
| G1 Yêu cầu | State machine + yêu cầu rõ | Xu + Vibe | W118-02..05 DRAFT |
| G2 Phản biện kiến trúc | 8 câu hỏi BB-118-001 được trả lời | Ka/Xu + Vibe độc lập | W118-08 + comments |
| G3 Phê duyệt trước BUILD | Biên bản kiến trúc được duyệt | **Vinh** | Approve trên Issue #65 |
| G4 Pilot có giới hạn | Pilot chạy, bằng chứng thật | Vibe thực thi, Ka/Xu chứng kiến | Evidence entries |
| G5 Nghiệm thu mở rộng | Đánh giá độc lập đạt | Ka/Xu/Vinh | Entry nghiệm thu |

## 2. Review gate

- Reviewer **độc lập** với actor (ka không review của chính mình; Vibe không tự review).
- Checklist review: (a) acceptance criteria của Issue, (b) evidence đầy đủ theo W118-03, (c) không đụng khu cấm (labels/thresholds/gate chuẩn — theo quy ước Work 103).
- pull_request CI là điều kiện tiên quyết trước review — xử lý Gap #4.

## 3. Merge policy

- Merge chỉ qua PR; required checks phải bật — hiện chưa kiểm chứng được (cần admin, BLOCKED, ghi limitation).
- Hotfix khẩn cũng qua PR + ít nhất một reviewer; Vinh acknowledge trên Issue.
