# DASHBOARD ↔ ROOM-HOP CORE READ CONTRACT
# Hợp đồng đọc dữ liệu giữa Dashboard và ROOM-HOP Core

## 1. Nguyên tắc
Dashboard là read-only projection (màn hình chỉ đọc), không phải nguồn dữ liệu chuẩn và không có quyền đổi trạng thái Work. ROOM-HOP Core là nguồn trạng thái chuẩn khi API được triển khai và xác minh.

## 2. Luồng dự kiến
Browser Dashboard → Core Read API → Work-scoped product status projection → Dashboard renderer.

Không gọi trực tiếp database, Sandbox filesystem hoặc execution host từ trình duyệt. Không cho Dashboard ghi trạng thái, approve gate, tạo waiver hay trigger release.

## 3. Endpoint đề xuất (chưa khẳng định đã tồn tại)
GET /api/v1/works/{work_id}/product-status
GET /api/v1/works/{work_id}/lifecycle-events?limit={n}
GET /api/v1/works/{work_id}/work-packages

Các endpoint trên là thiết kế hợp đồng, KHÔNG phải endpoint đã được xác minh trong Core hiện tại.

## 4. Response envelope đề xuất
{
  "work_id": "70",
  "product_name": "ROOM-HOP Product Lifecycle & Work Dashboard",
  "lifecycle": {
    "current_phase": "05_BUILD",
    "phases": [
      {
        "phase_id": "01_DISCOVER",
        "status": "COMPLETE",
        "gate_status": "PASS",
        "owner": "product-owner",
        "evidence_refs": ["evidence://..."],
        "verified_at": "2026-10-30T00:00:00Z"
      }
    ]
  },
  "work_packages": [],
  "blockers": [],
  "risks": [],
  "decisions_needed": [],
  "source": {
    "mode": "core_live",
    "generated_at": "2026-10-30T00:00:00Z",
    "revision": "opaque-revision",
    "freshness": "FRESH"
  }
}

Đây là ví dụ cấu trúc, không phải dữ liệu thực tế của Work 70.

## 5. AuthN/AuthZ và bảo mật
- Authentication (xác thực): dùng cơ chế đăng nhập/session/token chính thức của ROOM-HOP; không nhúng secret vào HTML/JS.
- Authorization (phân quyền): chỉ trả Work mà caller được phép đọc; kiểm tra quyền ở Core, không tin work_id do client gửi.
- Mọi response phải loại bỏ secret, credential, dữ liệu cá nhân không cần thiết và nội dung file ngoài phạm vi.
- CORS, CSRF và cache policy phải theo chuẩn ứng dụng hiện hành.
- Audit log ghi caller, Work ID, thời gian, correlation ID; không ghi token/secret.

## 6. Freshness và lỗi
- 200: dữ liệu hợp lệ; bắt buộc có source mode, generated_at và revision.
- 401: chưa xác thực; không hiển thị dữ liệu cache nhạy cảm.
- 403: không có quyền đọc Work.
- 404: Work không tồn tại hoặc không được phép tiết lộ sự tồn tại.
- 429: giới hạn truy cập; UI hiển thị retry guidance.
- 5xx/network: giữ dữ liệu cũ nhưng gắn STALE; nếu chưa có dữ liệu thì UNKNOWN. Không tự chuyển thành live.
- Quá ngưỡng freshness do Core công bố: STALE, luôn hiển thị thời điểm cập nhật cuối.
- Không có evidence: UNKNOWN/NOT_READY, tuyệt đối không suy diễn PASS.

## 7. Chế độ nguồn
- core_live: response vừa lấy từ Core đã xác thực.
- core_cached: dữ liệu cache do Core phát hành, kèm generated_at và freshness.
- local_snapshot: JSON tĩnh trong Sandbox/Work; không phải live.
- sample: dữ liệu minh họa; không phải trạng thái dự án.

## 8. Điều kiện nghiệm thu tích hợp
Chỉ đánh dấu tích hợp PASS khi có: endpoint thật trong mã Core, test quyền 401/403/404, test dữ liệu Work scope, test stale/network failure, test không có write path, log/correlation evidence và kiểm thử UI hiển thị source mode chính xác.
