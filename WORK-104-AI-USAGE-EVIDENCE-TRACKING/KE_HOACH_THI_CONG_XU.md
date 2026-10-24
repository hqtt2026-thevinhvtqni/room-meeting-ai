# KE_HOACH_THI_CONG_XU.md — Work 104: AI Usage & Evidence Tracking

- Quản lý: Xu (coordinator). Bản chính thức duy nhất theo AGENTS.md §06.1.
- Lập: 2026-10-24 (UTC+7). Cập nhật khi quyết định/progress thay đổi, không tạo bản cạnh tranh.

## Trạng thái chung
ACTIVE — PLAN / INITIALIZATION. Gate hiện tại: G0 Discovery. Chưa có gate nào PASS.

## Đầu việc

| # | Đầu việc | Phụ trách | Tiêu chí nghiệm thu | Bằng chứng cần có | Trạng thái |
|---|---|---|---|---|---|
| 1 | Khởi tạo Work 104 + nhánh + tài liệu gốc | Xu | Nhánh tồn tại, manifest rõ | Commit tạo nhánh; WORK_MANIFEST.md | DONE 2026-10-24 |
| 2 | Kiến trúc đề xuất + Acceptance plan | Cla/Xu | Envelope, gates G0–G5 chốt | 03_ARCHITECTURE; 05_TEST | DONE (PROPOSED) |
| 3 | Chuẩn hóa 3 hồ sơ điều hành theo §06 | Vibe (ủy quyền Vinh) | BIEN_BAN/KE_HOACH/NHAT_KY tồn tại, journal cũ đánh dấu SUPERSEDED | Commit hợp nhất; link tương hỗ | DONE 2026-10-24 |
| 4 | Cập nhật PROJECT_STATE.md phản ánh Work 104 | Vibe (ủy quyền Vinh) | Truth Table có mục Work 104 | Commit; diff | DONE 2026-10-24 |
| 5 | G0 Discovery: inventory invocation paths, adapters, usage-discard points | Cla | Mỗi path có file/API evidence; danh sách điểm mất usage | 06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md + EXPANSION (mở rộng 2026-10-24: không thêm provider path; 2 errata; submodule chưa kiểm kê) | DONE — bản ghi + mở rộng; G0 vẫn NOT PASS vì submodule room-meeting-ai/ (SHA eeb497e9) chưa kiểm kê |
| 6 | G0: quyết định integration point nhỏ nhất | Cla → Xu phê | Decision record có so sánh phương án | 01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md | DONE — DECISION 2026-10-24; không phải G0 PASS |
| 7 | G1 Design approve: schema + privacy + pricing provenance | Xu → Vinh | Vinh ACK | Bản chính: 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md **REV 4** 2026-10-24 — REV2 (5 điểm Xu) + REV3 (3 nhất quán) + REV4: (A) giới hạn tuyên bố crash — "1 cuộc gọi = 1 dòng" chỉ đúng khi tiến trình sống đến lúc ghi, crash = mất-không-dấu-vết chấp nhận ở v1, mở #7c crash-detection; (B) quy tắc giá 3 nhánh duy nhất verified→actual / unverified→estimated / không-match→unavailable; (C) khai báo stderr không thu thập được vào nguồn truy vấn ở v1 — mất báo cáo bằng khoảng thời gian + phạm vi; test kép #7 và test crash-limit #8 vào §7 | REV 4 SẴN — CHỜ XU THẨM ĐỊNH LẦN CUỐI → VINH ACK |
| 7b | Điền dữ liệu pricing_provenance.json (thu thập giá, xác thực) | Co → Xu | Entry verified có source_url + người xác thực | docs/pricing_provenance.json | SAU G3 — theo G1 §5 |
| 8 | G2 Implementation: instrumentation + ledger + fail-safe | Co (build owner) | Code chạy, logging failure không mất event, idempotent | Test log, changed-file list | CHƯA XÁC MINH |
| 9 | G3 Verification: unit/integration/retry/idempotency/reconciliation | Co + Ka (independent) | Test tái hiện được PASS trong môi trường ủy quyền | Test report + reviewer Ka | CHƯA XÁC MINH |
| 10 | G4 E2E: trace AI → task → usage/cost → artifact → acceptance | Ka | 1 luồng end-to-end đầy đủ có hash/link | E2E report trong 06_EVIDENCE | CHƯA XÁC MINH |
| 11 | G5 Handoff: runbook, hạn chế, blocker còn lại | Xu | Vinh ACK bàn giao | Handoff record | CHƯA XÁC MINH |
| 12 | Dọn `tmp/`, `trash/`, `agent_test/` (cây repo gốc) | Chờ Vinh/Xu phê danh sách xóa | Không xóa bằng chứng lịch sử hợp lệ | Danh sách xóa được duyệt + commit | MỘT PHẦN 2026-10-24: đã xóa 3 desktop.ini rác (tmp/, core/, agents/) theo ủy quyền tự chủ của Vinh; giữ toàn bộ trash/ làm bằng chứng cách ly; agent_test/ chưa kiểm kê — CHƯA XÁC MINH |

## Phụ thuộc
- #5 → #6 → #7 → #8 → #9 → #10 → #11. #12 độc lập, cần phê duyệt riêng.
- Work 102 (AI Agent Loop Production Readiness) vẫn NOT PASS/NOT RELEASED trên nhánh riêng; không khai báo dependency chéo giữa 102 và 104 ngoài evidence đã ghi.

## Bước tiếp theo ngay
#7 G1 Design: hoàn thiện event schema, provider-specific usage extraction, privacy/redaction, failure isolation, idempotency, retention và pricing provenance; gửi Vinh ACK trước implementation. Mở rộng G0 inventory các invocation paths chưa khảo sát trước khi tuyên bố coverage toàn hệ thống. Agent nhận việc phải đọc BIEN_BAN.md + NHAT_KY_HOP_THI_CONG.md (mục mới nhất) trước khi bắt đầu.
