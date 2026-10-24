# KE_HOACH_THI_CONG_XU.md — Work 104: AI Usage & Evidence Tracking

- Quản lý: Xu (coordinator). Bản chính thức duy nhất theo AGENTS.md §06.1.
- Lập: 2026-10-24 (UTC+7). Cập nhật khi quyết định/progress thay đổi, không tạo bản cạnh tranh.

## Trạng thái chung
ACTIVE — IMPLEMENTATION. G0 Discovery vẫn NOT PASS do gitlink chưa kiểm kê; G1 Design REV 6 đã ACK theo tiêu chí #7; G2 Implementation IN PROGRESS, chưa PASS vì test chưa chạy.

## Đầu việc

| # | Đầu việc | Phụ trách | Tiêu chí nghiệm thu | Bằng chứng cần có | Trạng thái |
|---|---|---|---|---|---|
| 1 | Khởi tạo Work 104 + nhánh + tài liệu gốc | Xu | Nhánh tồn tại, manifest rõ | Commit tạo nhánh; WORK_MANIFEST.md | DONE 2026-10-24 |
| 2 | Kiến trúc đề xuất + Acceptance plan | Cla/Xu | Envelope, gates G0–G5 chốt | 03_ARCHITECTURE; 05_TEST | DONE (PROPOSED) |
| 3 | Chuẩn hóa 3 hồ sơ điều hành theo §06 | Vibe (ủy quyền Vinh) | BIEN_BAN/KE_HOACH/NHAT_KY tồn tại, journal cũ đánh dấu SUPERSEDED | Commit hợp nhất; link tương hỗ | DONE 2026-10-24 |
| 4 | Cập nhật PROJECT_STATE.md phản ánh Work 104 | Vibe (ủy quyền Vinh) | Truth Table có mục Work 104 | Commit; diff | DONE 2026-10-24 |
| 5 | G0 Discovery: inventory invocation paths, adapters, usage-discard points | Cla | Mỗi path có file/API evidence; danh sách điểm mất usage | 06_EVIDENCE/G0_DISCOVERY_INVENTORY_20261024.md + EXPANSION (mở rộng 2026-10-24: không thêm provider path; 2 errata; submodule chưa kiểm kê) | DONE — bản ghi + mở rộng; G0 vẫn NOT PASS vì submodule room-meeting-ai/ (SHA eeb497e9) chưa kiểm kê |
| 6 | G0: quyết định integration point nhỏ nhất | Cla → Xu phê | Decision record có so sánh phương án | 01_ORIGINAL/DECISION_G0_INTEGRATION_POINT_20261024.md | DONE — DECISION 2026-10-24; không phải G0 PASS |
| 7 | G1 Design approve: schema + privacy + pricing provenance | Xu → Vinh | Vinh ACK | Bản chính: 03_ARCHITECTURE/G1_DESIGN_USAGE_LEDGER_20261024.md **REV 6 (FINAL, ACKED)** 2026-10-24 — REV2 (5 điểm Xu) + REV3 (3 nhất quán) + REV4 + REV5 (§3d: nguồn xác định khoảng mất = người vận hành cung cấp/xác nhận, không tự phát hiện, không suy đoán; test #7-#8 giữ nguyên): (A) giới hạn tuyên bố crash — "1 cuộc gọi = 1 dòng" chỉ đúng khi tiến trình sống đến lúc ghi, crash = mất-không-dấu-vết chấp nhận ở v1, mở #7c crash-detection; (B) quy tắc giá 3 nhánh duy nhất verified→actual / unverified→estimated / không-match→unavailable; (C) khai báo stderr không thu thập được vào nguồn truy vấn ở v1 — mất báo cáo bằng khoảng thời gian + phạm vi; test kép #7 và test crash-limit #8 vào §7 | DONE — VINH ACK (có điều kiện) 2026-10-24: điều kiện chuẩn hóa nhãn §3 đã hoàn tất trong REV 6; #7c giữ mở; gitlink giữ nguyên BLOCKED |
| 7b | Điền dữ liệu pricing_provenance.json (thu thập giá, xác thực) | Co → Xu | Entry verified có source_url + người xác thực | docs/pricing_provenance.json | SAU G3 — theo G1 §5 |
| 8 | G2 Implementation: instrumentation + ledger + fail-safe | Co (build owner) / Xu điều phối | Module + test + 6 điểm instrument đã được ghi vào nhánh; tiêu chí chạy/ fail-safe/idempotency còn chờ test | 06_EVIDENCE/G2_IMPLEMENTATION_PROGRESS_20261024.md; commit list trong evidence | IN PROGRESS — code written; tests NOT RUN; Vibe review tĩnh độc lập 2026-10-24: NHẤT QUÁN với G1 REV 6 ở mức tĩnh (05_TEST/G2_STATIC_REVIEW_20261024.md — 8 mục đạt, findings F1–F5; F1 test kép đã bổ sung vào tests/; F2 concurrency/F3 rotation-race chờ Co; F5 correlation truyền ở G4) |
| 9 | G3 Verification: unit/integration/retry/idempotency/reconciliation | Co + Ka (independent) | Test tái hiện được PASS trong môi trường ủy quyền | Test report + reviewer Ka | CHƯA XÁC MINH |
| 10 | G4 E2E: trace AI → task → usage/cost → artifact → acceptance | Ka | 1 luồng end-to-end đầy đủ có hash/link | E2E report trong 06_EVIDENCE | CHƯA XÁC MINH |
| 11 | G5 Handoff: runbook, hạn chế, blocker còn lại | Xu | Vinh ACK bàn giao | Handoff record | CHƯA XÁC MINH |
| 12 | Dọn `tmp/`, `trash/`, `agent_test/` (cây repo gốc) | Chờ Vinh/Xu phê danh sách xóa | Không xóa bằng chứng lịch sử hợp lệ | Danh sách xóa được duyệt + commit | MỘT PHẦN 2026-10-24: đã xóa 3 desktop.ini rác (tmp/, core/, agents/) theo ủy quyền tự chủ của Vinh; giữ toàn bộ trash/ làm bằng chứng cách ly; agent_test/ chưa kiểm kê — CHƯA XÁC MINH |

## Phụ thuộc
- #5 → #6 → #7 → #8 → #9 → #10 → #11. #12 độc lập, cần phê duyệt riêng.
- Work 102 (AI Agent Loop Production Readiness) vẫn NOT PASS/NOT RELEASED trên nhánh riêng; không khai báo dependency chéo giữa 102 và 104 ngoài evidence đã ghi.

## Bước tiếp theo ngay
#8 G2 đang IN PROGRESS theo lệnh Vinh. Đã ghi module ledger, unit tests và instrumentation tại các điểm đã biết; bằng chứng tiến độ: 06_EVIDENCE/G2_IMPLEMENTATION_PROGRESS_20261024.md. Chưa chạy pytest trong môi trường ủy quyền, nên G2 NOT PASS và G3 chưa bắt đầu. Bước kế: kiểm thử có ủy quyền + review code độc lập; giữ G0 NOT PASS cho đến khi gitlink được kiểm kê. #7b sau G3; #7c OPEN, không triển khai.
