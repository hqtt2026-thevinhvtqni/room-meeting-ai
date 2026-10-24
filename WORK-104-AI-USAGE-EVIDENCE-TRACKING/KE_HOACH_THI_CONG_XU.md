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
| 5 | G0 Discovery: inventory invocation paths, adapters, usage-discard points | Cla | Mỗi path có file/API evidence; danh sách điểm mất usage | Discovery record trong 06_EVIDENCE | CHƯA XÁC MINH |
| 6 | G0: quyết định integration point nhỏ nhất | Cla → Xu phê | Decision record có so sánh phương án | 01_ORIGINAL/decision record | CHƯA XÁC MINH |
| 7 | G1 Design approve: schema + privacy + pricing provenance | Xu → Vinh | Vinh ACK | Meeting/ACK record | CHƯA XÁC MINH |
| 8 | G2 Implementation: instrumentation + ledger + fail-safe | Co (build owner) | Code chạy, logging failure không mất event, idempotent | Test log, changed-file list | CHƯA XÁC MINH |
| 9 | G3 Verification: unit/integration/retry/idempotency/reconciliation | Co + Ka (independent) | Test tái hiện được PASS trong môi trường ủy quyền | Test report + reviewer Ka | CHƯA XÁC MINH |
| 10 | G4 E2E: trace AI → task → usage/cost → artifact → acceptance | Ka | 1 luồng end-to-end đầy đủ có hash/link | E2E report trong 06_EVIDENCE | CHƯA XÁC MINH |
| 11 | G5 Handoff: runbook, hạn chế, blocker còn lại | Xu | Vinh ACK bàn giao | Handoff record | CHƯA XÁC MINH |
| 12 | Dọn `tmp/`, `trash/`, `agent_test/` (cây repo gốc) | Chờ Vinh/Xu phê danh sách xóa | Không xóa bằng chứng lịch sử hợp lệ | Danh sách xóa được duyệt + commit | CHƯA XÁC MINH |

## Phụ thuộc
- #5 → #6 → #7 → #8 → #9 → #10 → #11. #12 độc lập, cần phê duyệt riêng.
- Work 102 (AI Agent Loop Production Readiness) vẫn NOT PASS/NOT RELEASED trên nhánh riêng; không khai báo dependency chéo giữa 102 và 104 ngoài evidence đã ghi.

## Bước tiếp theo ngay
Thi công #5 (G0 Discovery). Agent nhận việc phải đọc BIEN_BAN.md + NHAT_KY_HOP_THI_CONG.md (mục mới nhất) trước khi bắt đầu.
