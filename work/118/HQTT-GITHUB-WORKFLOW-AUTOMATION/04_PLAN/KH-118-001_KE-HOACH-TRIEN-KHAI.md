# KH-118-001 — KẾ HOẠCH TRIỂN KHAI WORK 118

## Mục tiêu
Thiết kế và kiểm chứng có kiểm soát cơ chế điều phối GitHub → ROOM-HOP → CI → review → Work evidence.

| WP | Hạng mục | Đầu ra | Trạng thái |
|---|---|---|---|
| W118-01 | Kiểm kê hiện trạng GitHub và Work 70 | Danh mục workflow, events, quyền, CI, API, gaps | DONE 2026-11-20 — [EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md](../EVIDENCE/W118-01_GITHUB_DISCOVERY_20261120.md); gap chính: 0/8 cơ chế event-driven tồn tại; BLOCKED phụ: secrets/webhook cấp repo cần Vinh xác nhận |
| W118-02 | Chuẩn hóa Issue/Branch/Commit/PR | Quy ước và templates | DRAFT 2026-11-20 — [QC-118-002](../02_DEFINE/QC-118-002_QUY-UOC-ISSUE-BRANCH-COMMIT-PR.md); templates chỉ tạo sau G3 |
| W118-03 | Thiết kế CI và evidence contract | Ma trận jobs, artifacts, SHA, logs, exit code | PLANNED — khuyến nghị tái dùng schema evidence W70 |
| W118-04 | Thiết kế event orchestration | Event → actor → action → permission → result | PLANNED — khuyến nghị GitHub-native events trước, webhook sau |
| W118-05 | Thiết kế failure/retry/idempotency | State machine và giới hạn retry | PLANNED — gồm item chống vòng lặp CI autofix (w300) |
| W118-06 | Thiết kế review/acceptance/merge gates | Gate matrix và quyền phê duyệt | PLANNED |
| W118-07 | Thiết kế audit journal/dashboard | Data contract và provenance | PLANNED |
| W118-08 | Phản biện và chốt kiến trúc | Biên bản kiến trúc được duyệt | IN PROGRESS — [DC-118-003](../02_DEFINE/DC-118-003_BRIEF-PHAN-BIEN-KIEN-TRUC.md) brief 6 AD giao phản biện |
| W118-09 | Pilot có giới hạn | CI/event flow chạy thật trong phạm vi thử nghiệm | BLOCKED — chờ phê duyệt thiết kế |

## Cổng kiểm soát
- G0: xác nhận hiện trạng và phạm vi.
- G1: yêu cầu và state machine được xác định.
- G2: kiến trúc, bảo mật, quyền và evidence contract được phản biện.
- G3: Vinh phê duyệt trước BUILD.
- G4: pilot end-to-end có bằng chứng thật.
- G5: nghiệm thu độc lập trước khi mở rộng.

## Quy tắc thực hiện
- Không triển khai trước G3.
- Không coi trạng thái CI xanh là nghiệm thu sản phẩm.
- Không merge tự động trong pilot.
- Không ghi PASS nếu thiếu run URL, commit SHA, logs và kết quả thực tế.
- Mọi blocker phải nêu: vấn đề / bằng chứng đã thử / nút thắt / phương án / điều kiện còn thiếu.
