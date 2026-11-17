# KẾ HOẠCH TRIỂN KHAI / IMPLEMENTATION ROADMAP — WORK 802001

- Version: 1.4 — DEFINE INDEPENDENT REVIEW COMPLETED (VIBE)
- Date: 2026-11-17
- Status: DEFINE REVIEWED — AWAITING VINH APPROVAL; BUILD NOT AUTHORIZED
- Governing standard: Work 70

## Mục tiêu
Chuẩn hóa và xây dựng nghiệp vụ theo dõi, nhắc nhở, hướng dẫn, điều chỉnh và kiểm tra lại Agent trong suốt quá trình thực hiện Work/assignment. AOG chỉ là một lớp kiểm soát trong quy trình tổng thể.

| WP | Nội dung | Deliverable | Trạng thái | Điều kiện hoàn thành |
|---|---|---|---|---|
| WP-802001-01 | DISCOVER: thu thập tình huống thực tế Agent nhận việc, thi công, báo cáo, sai/lệch/chậm/blocked | Case inventory + process trace | BASELINE COMPLETE — LIMITED TO 10 HISTORICAL CASES | Ghi rõ giới hạn nguồn; bổ sung khi có case từ Work khác; không khái quát hóa quá mức |
| WP-802001-02 | DEFINE: chuẩn hóa assignment, checkpoint, reminder, correction, recheck, escalation | Business rules + reminder matrix + independent review record | REVIEW COMPLETED (VIBE: ACCEPT WITH CHANGES; DEFINE v0.2) — AWAITING VINH APPROVAL | Xử lý open questions (DOC-096 path, readback rule); Vinh approval trước khi policy binding |
| WP-802001-03 | ARCHITECT: mô hình dữ liệu/trạng thái và điểm quan sát/kiểm soát trong ROOM-HOP | Business/technical architecture + ADR | PLANNED | READ/TRACE các nguồn và execution/observation paths; reviewer độc lập |
| WP-802001-04 | PLAN: WP, dependency, owner, acceptance, journal/evidence | WP register + test strategy | PLANNED | Bám lifecycle và Gate W70; một nguồn canonical |
| WP-802001-05 | BUILD: triển khai theo kiến trúc được duyệt | Source + build journal | NOT_AUTHORIZED | Chỉ mở sau G4 PASS và quyết định phê duyệt |
| WP-802001-06 | VERIFY: theo dõi, nhắc, hướng dẫn, sửa, recheck, escalation và enforcement nếu có | Verification report + evidence | NOT_STARTED | Kiểm thử thật, negative cases, reviewer độc lập |
| WP-802001-07 | ACCEPT/RELEASE/OPERATE | Acceptance, release, runbook | NOT_STARTED | Theo Gate/state và hồ sơ chuẩn W70 |

## Nguyên tắc
- Work 70 là chuẩn gốc; không tự tạo lifecycle hoặc cấu trúc song song.
- Trước hết chuẩn hóa nghiệp vụ thực tế đã dùng trong quá trình thi công; không mặc định phải tự động hóa toàn bộ ngay.
- Reminder cadence tùy risk/checkpoint; tránh spam; không đặt SLA chung khi chưa có dữ liệu.
- Tất cả hoạt động kiểm tra, nhắc nhở, hướng dẫn, sửa và kết quả phải có journal/evidence.
- Giữ nguyên hồ sơ E2E legacy; migration chỉ sau inventory và phê duyệt.
- Không mở BUILD, không sửa runtime/API/MCP trước khi kiến trúc được duyệt.

## Discovery baseline
Đã trích xuất 10 case từ hồ sơ lịch sử của chính Work 802001. Đây là historical-record evidence có phạm vi hạn chế; không đại diện toàn bộ Agent/Work và không phải kết luận vi phạm cá nhân.

## DEFINE baseline
W802001-DEF-001 đã qua phản biện độc lập của Vibe: verdict ACCEPT WITH CHANGES; DEFINE cập nhật v0.2 (bổ sung múi giờ/offline cho reminder, reviewer independence/appeal, multi-agent/multi-work linkage, NEEDS_BRIEFING, ghi chú DOC-096 unverified). Kết quả chi tiết tại `02_DEFINE/VIBE_INDEPENDENT_REVIEW_PACKAGE.md` mục 9. Tài liệu vẫn NOT APPROVED POLICY. Không có SLA cố định; không tuyên bố runtime automation.

## Điều kiện chuyển tiếp
WP-802001-02 chỉ hoàn tất sau khi xử lý open questions (canonical path DOC-096; quy tắc readback đề xuất) và Vinh phê duyệt policy. Sau đó mới chuyển sang truy vết ARCHITECT; BUILD vẫn phụ thuộc W70 G4 PASS và phê duyệt rõ ràng.
