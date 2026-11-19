# ĐỀ XUẤT CHUẨN HÓA LAYOUT REPO — WORK 17 (v1.1 — chờ quyết định cuối của Vinh)

- Work ID: 17 · Ngày: 2026-11-19 · Người soạn: Vibe (lane GitHub-side QA) · Phản biện: Xu / AI-01
- Trạng thái: **G4 CONDITIONAL — MIGRATION NOT AUTHORIZED**. Xu đã duyệt CÓ ĐIỀU KIỆN hướng kiến trúc; di trú hàng loạt CHƯA được phép; xóa cấu trúc cũ BỊ CẤM ở giai đoạn đầu. Quyết định cuối: Vinh.
- Phân tách gate: **G4 phê duyệt kiến trúc** (chính sách này) ≠ **G7 cho phép thực thi** từng đợt di trú cụ thể.

## 1. Quyết định đã có (G4 điều kiện, của Xu)

| Nội dung | Quyết định |
|----------|------------|
| Nested layout `work/<ID>/<WORK-NAME>/` | Duyệt làm chuẩn (raw G4) |
| Flat layout | LEGACY, chưa di trú |
| 03_ARCHITECT | Chuẩn tên |
| 06_VERIFY | Giữ chức năng kiểm chứng |
| 06_EVIDENCE | Kho bằng chứng duy nhất |
| Di trú hàng loạt | Chưa cho phép |
| Xóa cấu trúc cũ | Cấm ở giai đoạn đầu |

## 2. Chuẩn v1.1

### 2.1 Layout
- Nested là chuẩn thống nhất cho GitHub Mirror và Sandbox (raw G4 điều 1).
- Flat được ghi LEGACY trong manifest tương ứng; KHÔNG dịch chuyển tới khi có quyết định di trú của Vinh.

### 2.2 Hai khu chức năng KHÁC NHAU, đều là chuẩn (chỉnh theo phản biện Xu)
- **06_VERIFY** — khu kiểm chứng: quy trình verify, biên bản kiểm thử, kết quả chạy lại. Không phải kho bằng chứng.
- **06_EVIDENCE** — kho bằng chứng duy nhất của Work: journal, artifact, hash, bản ghi đồng bộ.
- Sự đồng tồn của cả hai (0001, 115, 117, 76) là ĐÚNG chuẩn, không phải "lẫn lộn".
- Duy nhất khu **EVIDENCE trần** (không số thứ tự: 113, 115, 117, 802001, 502) là lệch → khi di trú: lift toàn bộ vào 06_EVIDENCE, giữ 06_VERIFY nguyên vị.

### 2.3 Tên khu duy nhất
03_ARCHITECT (không dùng 03_ARCHITECTURE — hiện tại W502, W103).

### 2.4 Ánh xạ di trú (chỉ áp dụng khi Vinh cho phép di trú theo đợt G7)
| Hiện trạng | Đích chuẩn |
|------------|------------|
| EVIDENCE/ (trần) | 06_EVIDENCE/ |
| 03_ARCHITECTURE/ | 03_ARCHITECT/ |
| 02_EXTENSION/ (W1111) | 02_DEFINE/ sub-folder kèm manifest |
| flat <ID>/… | <ID>/<WORK-NAME>/… chép nguyên cây, không sửa nội dung |

### 2.5 Maturity tiers — nghiệm thu theo mức trưởng thành (chỉnh theo phản biện Xu)
| Tier | Tên | Khu bắt buộc tối thiểu | Work thuộc nhóm (kỳ 2026-11-19) |
|------|-----|------------------------|--------------------------------|
| A | Bootstrap | 00_ROOT (có WORK_MANIFEST.md) + 01_DISCOVER hoặc 01_ORIGINAL | 116, 28 |
| B | Điều hành (planning) | Tier A + 02_DEFINE, 03_ARCHITECT, 04_PLAN | 112, 300, 501, 75 |
| C | Vận hành (build/verify) | Tier B + 05_BUILD, 06_VERIFY, 06_EVIDENCE | 113, 802001, 502, 103 |
| D | Release đầy đủ | Tier C + 07_ACCEPT, 08_RELEASE, 09_OPERATE, DASHBOARD | 0001, 115, 117, 70, 76 |

- Tiêu chí nghiệm thu chỉ ép đúng Tier của từng Work; Work sơ khai KhÔNG vi phạm vì thiếu khu Tier cao.
- Tier của mỗi Work do Xu xác nhận theo trạng thái Sandbox; Vibe chỉ đo cấu trúc mirror.

### 2.6 Điều kiện parity Sandbox ↔ trước khi di trú (bắt buộc, do Xu kiểm chứng)
1. Xu sandbox_read Work tương ứng khớp cấu trúc mirror (sau khi Sandbox phản ánh trạng thái mới).
2. Blob SHA từng file cũ ghi vào SYNC_RECORD; không mất nào.
3. WORK_MANIFEST của Work được cập nhật canonical path mới trong cùng commit di trú.
4. Read-back qua Contents API khớp nội dung, không dùng raw làm nguồn xác nhận duy nhất.

### 2.7 An toàn di trú (khi được G7 bật)
1. Một Work = một commit riêng, message chuẩn; KHÔNG xóa cấu trúc cũ trong cùng commit.
2. LEGACY README trỏ đường dẫn mới; dọn bản cũ ở kỳ sau sau khi Xu xác nhận parity.
3. Khôi phục khả thi: mọi commit giữ nguyên lịch sử; rollback = revert commit đó.

## 3. Tiêu chí nghiệm thu v1.1 (thay cho 17/17 cứng)
- Mỗi Work đúng Tier, đủ khu tối thiểu của Tier đó, không khu ngoài chuẩn, không EVIDENCE trần.
- 100% Work có đủ 3 hồ sơ nền tảng (manifest, plan, journal) — mục tiêu hướng tới, ghi rõ còn thiếu bao nhiêu, không cửa chốt cứng.
- Bảng coverage quét lại đúng tier; QA độc lập (Ka governance, Qw test nghiệm thu) xác nhận trước khi trình Vinh.

## 4. Phân công
- Vibe: GitHub-side —coverage, proposal, biên bản, chuẩn bị đợt di trú (KHÔNG thực thi chưa lệnh).
- Xu: kiến trúc, parity Sandbox ↔ GitHub, phản biện độc lập.
- Ka: nhất quán governance và gate.
- Qw: kiểm thử độc lập tiêu chí nghiệm thu.
- Vinh: quyết định cuối cùng cho phép di trú (G7 kích hoạt theo đợt).
