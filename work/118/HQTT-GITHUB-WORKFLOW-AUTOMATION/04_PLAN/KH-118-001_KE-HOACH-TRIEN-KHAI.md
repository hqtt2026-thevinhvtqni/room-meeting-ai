# KH-118-001 — KẾ HOẠCH TRIỂN KHAI WORK 118

## Mục tiêu
Thiết kế và kiểm chứng có kiểm soát cơ chế điều phối GitHub → ROOM-HOP → CI → review → Work evidence.

| WP | Hạng mục | Đầu ra | Trạng thái |
|---|---|---|---|
| W118-01 | Kiểm kê hiện trạng GitHub và Work 70 | Danh mục workflow, events, quyền, CI, gaps | DONE — 01_DISCOVER/W118-01 + Entry 002 |
| W118-02 | Chuẩn hóa Issue/Branch/Commit/PR | Quy ước và templates | DONE (DRAFT) — 02_DEFINE |
| W118-03 | Thiết kế CI và evidence contract | Ma trận jobs, artifacts, SHA, logs, exit code | DONE (DRAFT) — 03_DESIGN |
| W118-04 | Thiết kế event orchestration | Event → actor → action → permission → result | DONE (DRAFT) — 03_DESIGN |
| W118-05 | Thiết kế failure/retry/idempotency | State machine và giới hạn retry | DONE (DRAFT) — 03_DESIGN |
| W118-06 | Thiết kế review/acceptance/merge gates | Gate matrix và quyền phê duyệt | DONE (DRAFT) — 03_DESIGN |
| W118-07 | Thiết kế audit journal/dashboard | Data contract và provenance | DONE (DRAFT) — 03_DESIGN |
| W118-08 | Phản biện và chốt kiến trúc | Biên bản kiến trúc được duyệt | IN_PROGRESS — bản DRAFT của Vibe đã có, chờ phản biện chéo Ka/Xu |
| W118-09 | Pilot có giới hạn | CI/event flow chạy thật trong phạm vi thử nghiệm | BLOCKED — chờ G3 (Vinh phê duyệt) |

## Cổng kiểm soát
- G0: hiện trạng và phạm vi. → **ĐẠT** (Entry 002).
- G1: yêu cầu và state machine được xác định. → **ĐẠT** (W118-02..05 DRAFT).
- G2: kiến trúc, bảo mật, quyền, evidence contract được phản biện. → **IN PROGRESS** (W118-08 DRAFT bên dưới; cần phản biện chéo Ka/Xu).
- G3: Vinh phê duyệt trước BUILD. → BLOCKED chờ G2.
- G4: pilot end-to-end có bằng chứng thật. → BLOCKED chờ G3.
- G5: nghiệm thu độc lập trước khi mở rộng. → BLOCKED chờ G4.

## Quy tắc thực hiện
- Không triển khai trước G3.
- Không coi trạng thái CI xanh là nghiệm thu sản phẩm.
- Không merge tự động trong pilot.
- Không ghi PASS nếu thiếu run URL, commit SHA, logs và kết quả thực tế.
- Mọi blocker phải nêu: vấn đề / bằng chứng đã thử / nút thắt / phương án / điều kiện còn thiếu.
