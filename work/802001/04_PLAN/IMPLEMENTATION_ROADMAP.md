# KẾ HOẠCH TRIỂN KHAI / IMPLEMENTATION ROADMAP — WORK 802001

- Version: 1.6 — DEFINE APPROVED / ARCHITECTURE EXPLORATION STARTED
- Date: 2026-11-17
- Status: DEFINE v0.3 APPROVED BY VINH; ARCHITECTURE EXPLORATION ACTIVE; BUILD NOT AUTHORIZED
- Governing standard: Work 70

## Mục tiêu
Chuẩn hóa và xây dựng nghiệp vụ theo dõi, nhắc nhở, hướng dẫn, điều chỉnh và kiểm tra lại Agent trong suốt quá trình thực hiện Work/assignment. AOG chỉ là một lớp kiểm soát trong quy trình tổng thể.

| WP | Nội dung | Deliverable | Trạng thái | Điều kiện hoàn thành |
|---|---|---|---|---|
| WP-802001-01 | DISCOVER: thu thập tình huống thực tế Agent nhận việc, thi công, báo cáo, sai/lệch/chậm/blocked | Case inventory + process trace | BASELINE COMPLETE — LIMITED TO 10 HISTORICAL CASES | Ghi rõ giới hạn nguồn; bổ sung khi có case từ Work khác; không khái quát hóa quá mức |
| WP-802001-02 | DEFINE: chuẩn hóa assignment, checkpoint, reminder, correction, recheck, escalation | Business rules + reminder matrix + independent review record | DONE — DEFINE v0.3 APPROVED BY VINH (2026-11-18) | Vibe independent review ACCEPT WITH CHANGES; Xu corrected DOC-096 misclassification and resolved VF-10 against DOC-033/DOC-035; Vinh approved the business baseline. |
| WP-802001-03 | ARCHITECT: mô hình dữ liệu/trạng thái và điểm quan sát/kiểm soát trong ROOM-HOP | Architecture v2.0 + ownership/interface map + ADR + independent review | IN_PROGRESS — AUTHORIZED EXPLORATION ONLY | READ/TRACE source and execution/observation paths; reconcile W70/W52/W16/W37/W14/W33/W112 ownership; Vibe independent architecture review; resolve blockers; G3 decision remains separate. |
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

## ARCHITECTURE execution plan — WP-802001-03

This is a documentation and design exploration only, authorized by D802001-001 and W70 DOC-047. It does not claim G2/G3 PASS and does not authorize BUILD.

| Step | Work | Required output | State |
|---|---|---|---|
| A-01 | Pin governing sources and map ownership boundaries across W70/W52/W16/W37/W14/W33/W112/W103 | Source pin table + ownership/conflict matrix | DONE — initial source trace recorded in Architecture v2.0 |
| A-02 | Separate Work/WP/assignment state from supervision case/finding/reminder/correction state | State ownership and mapping contract | DRAFT — independent review pending |
| A-03 | Define logical components and observation/event boundaries | Context diagram + component responsibility map | DRAFT — independent review pending |
| A-04 | Define conceptual records, provenance, journal/evidence links and data ownership | Conceptual data model and source-of-truth rules | DRAFT — owner/persistence decisions open |
| A-05 | Define identity, authorization, protected action boundary and threat model | Security/trust-boundary review | DRAFT — W37/W14 contracts not verified |
| A-06 | Define reminder delivery, quiet hours, deduplication, retry and failure/recovery behavior | Operational behavior and failure matrix | DRAFT — scheduler/channel/transport not verified |
| A-07 | Define measurable success measures and non-functional requirements | Metrics/NFR baseline; numeric targets remain open | OPEN |
| A-08 | Independent architecture review by Vibe; adjudicate findings and record exact readback | Review result, resolved findings and ADR disposition | PENDING — handoff recorded; ACK not verified |
| A-09 | Xu self-audit traceability and prepare G3 decision package for Vinh | G3 checklist, open-risk register and decision request | NOT STARTED |

## DEFINE baseline
W802001-DEF-001 đã qua phản biện độc lập của Vibe: verdict ACCEPT WITH CHANGES; DEFINE v0.3 giữ các thay đổi nghiệp vụ từ v0.2 và sửa sai tham chiếu Work 70. Vinh phê duyệt v0.3 làm baseline nghiệp vụ ngày 2026-11-18. Không có SLA cố định; không tuyên bố runtime automation.

## Điều kiện chuyển tiếp
WP-802001-02 is DONE: Vinh approved DEFINE v0.3 as the business baseline on 2026-11-18. WP-802001-03 may proceed as explicitly authorized architecture exploration under DOC-047; this does not claim G2 PASS or G3 PASS. BUILD remains NOT AUTHORIZED until architecture and plan are approved, G4 PASS is evidenced, and Vinh issues a separate BUILD authorization.
