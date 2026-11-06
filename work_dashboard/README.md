# ROOM HOP — Work Management Dashboard

Dashboard **chỉ đọc (read-only)** để quản lý các Work trong `work/<sandbox>/<WORK>/`,
tuân thủ quy tắc hồ sơ điều hành **AGENTS.md §06**:

- `BIEN_BAN.md` — Co quản lý
- `KE_HOACH_THI_CONG_XU.md` — Xu quản lý
- `NHAT_KY_HOP_THI_CONG.md` — Mọi AI cùng ghi
- `WORK_MANIFEST.md` — manifest Work

Dashboard **không sửa/xóa bất kỳ hồ sơ nào** — chỉ quét và hiển thị:
tình trạng đủ/thiếu 3 hồ sơ chuẩn, trạng thái tổng hợp (DESIGN / DONE / PASS /
BLOCKED…), số mục ghi Nhật ký, cấu trúc thư mục, số file bằng chứng, hoạt động cuối
(múi giờ UTC+07:00).

## Chạy

```bash
pip install flask            # nếu chưa có
python work_dashboard/app.py
# mở http://127.0.0.1:8055
```

## Cấu trúc

| File | Vai trò |
|---|---|
| `scanner.py` | Quét `work/`, trích xuất status & kiểm kê hồ sơ (§06). Chạy độc lập được: `python work_dashboard/scanner.py` để xem JSON. |
| `app.py` | Flask server: `/` (UI) và `/api/works` (JSON). |
| `templates/dashboard.html` | UI dark-theme: KPI, tìm kiếm, bộ lọc (Done/Pass, Design/Pending, Blocked, Thiếu hồ sơ chuẩn), card từng Work, tự làm mới 60s. |

## API

- `GET /api/works` → JSON toàn bộ Works (mỗi lần gọi quét lại trực tiếp trên đĩa).

## Lưu ý governance

- Dashboard là công cụ quan sát, **không phải nguồn state**. Nguồn truth vẫn là
  `context/PROJECT_STATE.md` + 3 hồ sơ chính thức của từng Work.
- Work thiếu hồ sơ chuẩn sẽ được cảnh báo ⚠️ theo §06.4 (chống phân tán) — việc
  hợp nhất/phải hóa tên file phải do người có thẩm quyền quyết định, dashboard không tự làm.
