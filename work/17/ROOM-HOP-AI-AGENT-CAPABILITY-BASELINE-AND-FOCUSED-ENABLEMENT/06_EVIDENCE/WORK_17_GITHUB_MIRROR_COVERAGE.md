# BÁO CÁO COVERAGE MIRROR GITHUB — WORK 17 (hỗ trợ GAP-06/GAP-07)

- Work ID: 17 · Kỳ quét: 2026-11-19 · Người quét: Vibe (lane GitHub-side, không đụng Sandbox)
- Phương pháp: get_file_contents đệ quy 1 cấp cho 17 workfolder trên `main`; đối chiếu với danh mục Sandbox 71 Work (Journal Entry 002).
- Giới hạn: chỉ nhìn thấy mirror; 54 Work còn lại KHÔNG đánh giá được từ phía GitHub (mặc định MIRROR_MISSING, không phải NOT_FOUND).

## 1. Kết luận nhanh

| Chỉ tiêu | Giá trị |
|----------|---------|
| Workfolder mirror | 17 |
| Sandbox | 71 → 54 Work MIRROR_MISSING (GAP-07) |
| Layout chuẩn nested `work/<ID>/<WORK-NAME>/` | 9/17 (17, 28, 70, 75, 76, 103, 300, 501, 502) |
| Layout legacy flat `work/<ID>/...` (G4: LEGACY, chưa di trú) | 8/17 (0001, 1111, 112, 113, 115, 116, 117, 802001) |
| Workfolder có đủ vòng đời 00_ROOT→09_OPERATE | 3/17 (0001, 115, 117) |
| Workfolder còn thiếu khu trong vòng đời | 116 (thiếu 05_BUILD), 112 (thiếu 01–02) |

## 2. Bảng chi tiết 17 workfolder

| Work | Layout | Cấu trúc có mặt | Đánh giá cấu trúc |
|------|--------|------------------|-------------------|
| 0001 | flat | 00_ROOT→09_OPERATE + DASHBOARD, 06_VERIFY và 06_EVIDENCE | Đủ vòng đời; 06_VERIFY (kiểm chứng) và 06_EVIDENCE (kho bằng chứng) là hai khu ĐỀU CHUẨN, không trùng chức năng |
| 103 | nested (kèm evidence flat) | ROOM-HOP-RAG-RETRIEVAL-CAPABILITY + 06_EVIDENCE | LẪN LỘN: evidence nằm ngoài thư mục Work chuẩn |
| 1111 | flat | 00_ROOT, 01_DISCOVER, 02_EXTENSION (không chuẩn), 03-06, EVIDENCE | 02_EXTENSION là tên khu không thuộc bộ chuẩn |
| 112 | flat | 00_ROOT, 03_ARCHITECT, 04_PLAN | Thiếu 01–02 lifecycle |
| 113 | flat | 00_ROOT–06_VERIFY + DASHBOARD, EVIDENCE | Gần đủ; thiếu 07–09; khu EVIDENCE trần cần lift lên 06_EVIDENCE |
| 115 | flat | đủ 00_ROOT→09_OPERATE + DASHBOARD, EVIDENCE | Đầy đủ nhất |
| 116 | flat | 00_ROOT, 01_DISCOVER + README | Sơ khai |
| 117 | flat | đủ 00_ROOT→09_OPERATE | Đầy đủ |
| 17 | nested | 00_ROOT, 01_ORIGINAL, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 06_EVIDENCE | Theo cấu trúc mặc định Sandbox |
| 28 | nested | 01_PLAN | Chỉ một khu |
| 70 | nested | đủ 00_ROOT→09 + DASHBOARD | Control plane |
| 75 | nested | 00_ROOT, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 06_VERIFY, DASHBOARD | Thiếu 01_DISCOVER, 05_BUILD và khu evidence chuẩn |
| 76 | nested | đủ 00_ROOT→09_OPERATE (có cả 06_VERIFY và 06_EVIDENCE) + DASHBOARD | Đầy đủ và đúng chuẩn: hai khu có chức năng khác nhau |
| 300 | nested | 00_ROOT, 03_ARCHITECT, 04_PLAN, 05_BUILD | Thiếu 01–02, 06–09 |
| 501 | nested | 00_ROOT, 03_ARCHITECT, 04_PLAN | Thiếu 01–02, 05–09 |
| 502 | nested | 00_ROOT, 03_ARCHITECTURE (không chuẩn), 04_PLAN, EVIDENCE (không chuẩn) | Tên khu lệch chuẩn: ARCHITECTURE vs ARCHITECT; EVIDENCE không có tiền tố số |
| 802001 | flat | 00_ROOT–06_VERIFY + DASHBOARD, EVIDENCE | ID 6 chữ số không khớp dãy chuẩn; khu EVIDENCE trần cần lift lên 06_EVIDENCE |

## 3. Các phát hiện cấu trúc — cập nhật theo quyết định điều kiện của Xu (G4)

1. HAI CHUẨN LAYOUT SONG SONG: nested `<ID>/<WORK-NAME>/` (theo Sandbox) và flat `<ID>/…` → nguy cơ bằng chứng rơi vào nhánh không canonical. Khuyến nghị: coi flat là LEGACY cho tới khi có quyết định của Vinh, không tự dịch chuyển.
2. LẪN LỘN 06_EVIDENCE vs EVIDENCE, song song với 06_VERIFY (0001, 115, 117): cần một tên chuẩn duy nhất trước G5.

3. MATURITY KHÁC NHAU (theo Xu): Work sơ khai (W116, W28, W501...) không bị ép đủ vòng đời; nghiệm thu theo maturity tier — xem proposal v1.1 mục 2.5.

## 4. Trạng thái cập nhật

- Kỳ 2 (2026-11-19): quét sâu 7 workfolder nested (75, 76, 300, 501, 502, 28, 103).
- Kỳ 3 (2026-11-19): sửa số liệu nested 9/17, flat 8/17 theo đối chiếu của Xu; tách 06_VERIFY (kiểm chứng) và 06_EVIDENCE (kho bằng chứng); tiêu chí theo maturity tier.
- Quyết định G4 của Xu: APPROVE CÓ ĐIỀU KIỆN (nested = chuẩn; flat = legacy; KHÔNG di trú hàng loạt; cấm xóa cấu trúc cũ) — biên bản tại 00_ROOT/WORK_17_G4_DECISION_RECORD.md; chờ Vinh quyết định cuối cùng trước khi di trú.
