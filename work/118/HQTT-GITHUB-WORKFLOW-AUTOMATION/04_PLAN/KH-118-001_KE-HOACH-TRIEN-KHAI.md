# KH-118-001 — KẾ HOẠCH TRIỂN KHAI WORK 118

## Mục tiêu
Thiết kế và kiểm chứng có kiểm soát cơ chế điều phối GitHub → ROOM-HOP → CI → review → Work evidence.

| WP | Hạng mục | Đầu ra | Trạng thái |
|---|---|---|---|
| W118-01 | Kiểm kê hiện trạng GitHub và Work 70 | Danh mục workflow, events, quyền, CI, gaps | DONE — 01_DISCOVER/W118-01 + Entry 002 |
| W118-02 | Chuẩn hóa Issue/Branch/Commit/PR | Quy ước và templates | DONE (DRAFT) — 02_DEFINE + templates đã tạo |
| W118-03 | Thiết kế CI và evidence contract | Ma trận jobs, artifacts, SHA, logs, exit code | DONE (DRAFT) — 03_DESIGN |
| W118-04 | Thiết kế event orchestration | Event → actor → action → permission → result | DONE (DRAFT) — 03_DESIGN |
| W118-05 | Thiết kế failure/retry/idempotency | State machine và giới hạn retry | DONE (DRAFT) — 03_DESIGN |
| W118-06 | Thiết kế review/acceptance/merge gates | Gate matrix và quyền phê duyệt | DONE (DRAFT) — 03_DESIGN |
| W118-07 | Thiết kế audit journal/dashboard | Data contract và provenance | DONE (DRAFT) — 03_DESIGN |
| W118-08 | Phản biện và chốt kiến trúc | Biên bản kiến trúc được duyệt | IN_PROGRESS — DRAFT của Vibe; phản biện chéo Ka/Xu chuyển sau pilot |
| W118-09 | Pilot có giới hạn | CI/event flow chạy thật | DONE-PILOT — run #2 PASS 9s (commit 6c8e5d1); chờ nghiệm thu Xu (PR vào main) |

## Cổng kiểm soát
- G0: hiện trạng và phạm vi. → **ĐẠT** (Entry 002).
- G1: yêu cầu và state machine được xác định. → **ĐẠT** (Entry 003).
- G2: phản biện kiến trúc. → DEFERRED sau pilot, theo ủy quyền của Vinh trong phiên.
- G3: phê duyệt BUILD. → **ĐẠT trong phiên** (Vinh phê duyệt trực tiếp, 2026-11-20).
- G4: pilot end-to-end có bằng chứng thật. → **ĐẠT (giới hạn)** — CI validate PASS; diagnostic idempotency chỉ chứng minh qua thiết kế (limitation).
- G5: nghiệm thu độc lập trước khi mở rộng. → CHỜ XU một khi PR vào main đạt review.

## Quy tắc thực hiện
- Không coi trạng thái CI xanh là nghiệm thu sản phẩm.
- Không merge tự động; merge chỉ qua PR + review độc lập.
- Không ghi PASS nếu thiếu run URL, commit SHA, logs và kết quả thực tế.
- KHÔNG branch protection / secrets / webhook trong phạm vi pilot.
