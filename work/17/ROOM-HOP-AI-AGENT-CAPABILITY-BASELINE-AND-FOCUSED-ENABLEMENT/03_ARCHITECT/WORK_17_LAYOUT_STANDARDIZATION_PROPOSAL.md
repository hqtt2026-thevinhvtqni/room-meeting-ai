# ĐỀ XUẤT CHUẨN HÓA LAYOUT REPO — WORK 17 (chờ G4 / quyết định Vinh)

- Work ID: 17 · Ngày: 2026-11-19 · Người soạn: Vibe (lane GitHub-side QA)
- Trạng thái: PROPOSAL — CHƯA THỰC THI. Mọi dịch chuyển/sửa tên thư mục là thay đổi Work thành phần, cần Gate G7 và hội ý Work 70.
- Phạm vi áp dụng: toàn bộ 17 workfolder mirror hiện có và mọi Work mirror về sau.

## 1. Bối cảnh (dữ liệu từ bản quét 2026-11-19)

- 8 Work dùng layout nested `work/<ID>/<WORK-NAME>/` khớp cấu trúc Sandbox.
- 9 Work dùng layout flat `work/<ID>/…` không có thư mục tên.
- Tồn tại song song: `06_EVIDENCE` với `EVIDENCE` (0001, 115, 117, 502), `03_ARCHITECT` với `03_ARCHITECTURE` (502, 103), khu không chuẩn `02_EXTENSION` (1111), W103 có evidence cả trong lẫn ngoài thư mục Work.

## 2. Chuẩn đề xuất (một chuẩn duy nhất)

### 2.1 Layout
- Nested: `work/<ID>/<WORK-NAME>/` — khớp registry Sandbox, tên Work dài không phá cấu trúc `work/`.
- Flat chỉ hợp lệ cho work chỉ có 1 tài liệu nhỏ trong giai đoạn bootstrap; phải có Work Manifest ghi rõ FIX_PENDING.

### 2.2 Bộ khu chuẩn (đối chiếu work/70)
`00_ROOT, 01_DISCOVER, 02_DEFINE, 03_ARCHITECT, 04_PLAN, 05_BUILD, 06_VERIFY, 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD`
- Bằng chứng duy nhất: `06_EVIDENCE` (có số thứ tự). Không dùng `EVIDENCE` trần.
- Không tạo khu ngoài bộ trên (ví dụ `02_EXTENSION`); nếu cần, đặt trong `02_DEFINE/EXTENSION-...` kèm manifest.

### 2.3 Ánh xạ di trú (đề xuất, không tự chạy)

| Hiện trạng | Đích chuẩn |
|------------|------------|
| `EVIDENCE/` | `06_EVIDENCE/` |
| `03_ARCHITECTURE/` | `03_ARCHITECT/` |
| `02_EXTENSION/` | `02_DEFINE/` (nội dung đặt trong sub-folder có manifest) |
| flat `<ID>/…` | `<ID>/<WORK-NAME>/…` chép nguyên cây, không chỉnh sửa nội dung |

### 2.4 Quy tắc an toàn di trúc
1. Không xóa bản cũ trong cùng commit; di trú = thêm bản mới + giữ LEGACY_README trỏ đường dẫn mới trong 1 kỳ, xóa ở kỳ sau khi Xu xác nhận parity Sandbox.
2. Mỗi Work di trú một commit riêng, message `refactor(work-<ID>): migrate layout to standard v1`.
3. Sau di trú, cập nhật GAP-07 trong WORK_17_GAP_REGISTER.md; không chốt G1/G2 theo layout cũ.

## 3. Tiêu chí nghiệm thu chuẩn v1 (để G4 duyệt)

- 0 workfolder nào còn 2 kiểu evidence dir cùng lúc.
- 0 khu ngoài bộ 11 khu chuẩn.
- 100% workfolder có đủ 3 hồ sơ nền tảng: WORK_MANIFEST.md, Execution Plan, Audit Journal.
- Bảng coverage quay lại quét: 17/17 PASS cấu trúc.

## 4. Phân công

- Vibe: thực thi di trú GitHub-side theo đợt, mỗi Work một commit, sau khi có quyết định của Vinh.
- Xu: đối chiếu parity Sandbox ↔ GitHub sau từng đợt; chốt sync record.
- Vinh: phê duyệt/từ chối chuẩn v1 tại G4; quyết định không đồng ý thì khu flat được ghi làm LEGACY vĩnh viễn trong manifest tương ứng.
