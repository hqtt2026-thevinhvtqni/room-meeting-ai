# KẾ HOẠCH THỰC HIỆN — WORK 17
## ROOM-HOP AI Agent Capability Baseline & Focused Enablement

- Work ID: 17
- Chủ sở hữu / người quyết định: Vinh
- Điều phối: Xu / AI-01
- Trạng thái: ACTIVE — PORTFOLIO READ / TRACE ONLY
- Ngày cập nhật: 2026-11-19
- Phạm vi: Đối soát toàn bộ Work Sandbox, năng lực 13 loại AI Agent, năng lực vận hành từng AI thành viên và thiết kế nền tảng năng lực chung cho ROOM-HOP. Giai đoạn hiện tại chỉ kiểm kê/đọc/truy vết; chưa triển khai thay đổi.

## 1. Mục tiêu
1. Đối soát danh mục toàn bộ Work: ID, tên chuẩn, manifest, mục tiêu, trạng thái, lifecycle/gate, owner, repo/path/branch/commit, tài liệu chuẩn, evidence, dashboard, phụ thuộc và quan hệ trùng lặp.
2. Đối chiếu snapshot DOC-018 của W0000 với danh mục Sandbox hiện tại; phân loại chênh lệch, Work mới, Work lịch sử, thư mục bất thường, mục trùng và mục chưa rõ danh tính. Không tự đổi tên, xóa, đánh số lại hoặc hợp nhất.
3. Đánh giá 13 loại Agent theo tài liệu → source/config → runtime → luồng ROOM đang dùng → bằng chứng kết quả.
4. Đánh giá từng AI thành viên theo danh tính/provider/model/session, vai trò, quyền, công cụ, truy cập Work/GitHub, khả năng nhận việc/ACK, thực thi, ghi evidence, kiểm thử, review, bàn giao và usage/token telemetry.
5. Trace luồng end-to-end: yêu cầu → Work/WP → assignment/dispatch → AI/session → tool/provider → artifact → verification/review → evidence/journal → dashboard/handoff.
6. Xác định các năng lực nền tảng dùng chung còn thiếu, điểm đứt gãy, quyền hạn không nhất quán, provider/tool chưa nối và các Work chồng lấn.
7. Đề xuất kiến trúc năng lực chung + profile riêng theo từng AI/provider, kèm thứ tự ưu tiên hẹp, tiêu chí nghiệm thu và điều kiện an toàn. Không mặc định phải xây đủ 13 loại Agent.

## 2. Phạm vi năng lực
### 2.1 Mười ba loại Agent
1. Simple Reflex Agent
2. LLM-based Agent
3. Tool-Using Agent
4. Planning Agent
5. Memory-Enabled Agent
6. Multi-Agent System
7. Hierarchical Agent
8. Self-Improving Agent
9. RAG Agent
10. Coding Agent
11. Web-Browsing Agent
12. Computer-Using Agent
13. Autonomous Agent

### 2.2 Năng lực vận hành xuyên suốt cần kiểm tra
- Identity & session binding: định danh AI, provider/model/version, session/runtime identity.
- Authorization & policy: phân quyền theo vai trò, Work/WP, tool, môi trường; fail-closed.
- Context & memory: đọc nguồn chuẩn, truy xuất lịch sử, bộ nhớ có provenance, chống context drift.
- Planning & orchestration: phân rã nhiệm vụ, dependency, điều phối phân cấp, checkpoint/resume.
- Dispatch & acknowledgment: giao việc thực sự tới AI, delivery receipt, ACK có thể quy trách nhiệm.
- Tool/provider integration: adapter, credential boundary, capability discovery, timeout/retry/rate limit.
- Execution: sandbox/host/browser/computer, cách ly, phê duyệt thao tác và rollback.
- Collaboration: multi-agent handoff, hợp đồng đầu vào/đầu ra, xử lý xung đột và reviewer độc lập.
- Knowledge/RAG: ingest, indexing, retrieval, citations, freshness, permission filtering.
- Coding & testing: sửa mã có kiểm soát, CI, test, browser E2E, artifact verification.
- Safety/security: secrets, prompt injection, data boundaries, audit, human approval, kill switch.
- Observability & cost: event trace, logs, token/cost telemetry, latency, usage attribution.
- Quality & self-improvement: đánh giá chất lượng, regression, feedback loop có kiểm soát; không tự sửa production không duyệt.
- Evidence & governance: journal, decision, provenance, status truth, dashboard từ dữ liệu chuẩn.
- Resilience: queue, idempotency, retry, recovery, state persistence, degraded mode.

## 3. Phương pháp
- READ: đọc registry, manifest, canonical docs, decision/minutes, journal, code/config và evidence của từng Work.
- TRACE: truy vết hợp đồng và luồng thực tế giữa Core, Gateway, Agent, provider, tools, execution host và evidence.
- VERIFY: chỉ dùng evidence đã tồn tại hoặc phép kiểm tra read-only an toàn; không suy diễn từ tên file, sơ đồ, manifest hoặc roster.
- RECONCILE: so sánh các nguồn canonical; ghi rõ xung đột, nguồn ưu tiên và mức tin cậy.
- ANALYZE: ma trận năng lực, phụ thuộc, ownership, trùng lặp, blocker và khoảng trống.
- DECIDE: Xu trình khuyến nghị; thay đổi kiến trúc/triển khai chỉ sau quyết định của Vinh và hội ý theo quy trình Work 70.

## 4. Quy tắc trạng thái
- DOC_ONLY: chỉ mô tả trong tài liệu.
- SOURCE_EXISTS: có mã nguồn/cấu hình nhưng chưa chứng minh chạy.
- RUNTIME_VERIFIED: có bằng chứng runtime thực tế.
- ROOM_IN_USE: có bằng chứng luồng ROOM-HOP đang sử dụng.
- PARTIAL: chỉ có một phần năng lực.
- NOT_FOUND: đã rà phạm vi xác định nhưng không tìm thấy.
- NOT_VERIFIED: chưa đủ bằng chứng.
- BLOCKED: có blocker được ghi nhận.
- CONFLICT: nguồn canonical đang mâu thuẫn.
- LEGACY / DUPLICATE_CANDIDATE / NAME_ANOMALY: chỉ là phân loại điều tra, không tự động dẫn tới đóng/xóa/đổi tên.

Không dùng nhãn chung “Có”. Không ghi PASS nếu thiếu phương pháp, kết quả và evidence có thể kiểm tra lại. Roster/assignment không chứng minh online, dispatch, ACK hay năng lực.

## 5. Work ưu tiên truy vết
Nhóm control plane/governance: W0000, W70, W99, W01, W02, W11, W28, W37, W38, W39, W40.
Nhóm agent/runtime/orchestration: W09, W091, W10, W12, W13, W14, W16, W19, W20, W21, W22, W23, W27, W30, W31, W32, W50, W51, W52, W91, W102, W112.
Nhóm knowledge/evidence/data: W03, W05, W33, W103, W104, W114, W116.
Các Work còn lại vẫn thuộc phạm vi danh mục toàn bộ; phân loại trước, chỉ đọc sâu khi có quan hệ trực tiếp với năng lực AI hoặc có dấu hiệu dữ liệu/ownership bất thường.

## 6. Nguyên tắc tập trung và giới hạn
- Một năng lực — một owner/contract chuẩn; Work khác tiêu thụ qua interface, không tự dựng engine song song.
- Tận dụng Work hiện hữu; đề xuất hợp nhất trách nhiệm hoặc đóng băng nhánh trùng, nhưng không tự thay đổi.
- Không mở thêm Work con, không tạo dự án song song.
- Không viết/sửa code, không thay đổi runtime, không cài provider, không phát sinh chi phí trong giai đoạn kiểm kê.
- Không dispatch thử tới phiên riêng, không giả lập ACK, không ghi token bằng suy đoán.
- Không gọi hoặc sử dụng endpoint/listener lịch sử đã bị cấm; tuân thủ boundary an toàn hiện hành.
- Không sửa Work thành phần; mọi kết luận phải trỏ về canonical source.

## 7. Đầu ra
1. Master Work reconciliation: 71-entry snapshot đối chiếu DOC-018, tình trạng và độ tin cậy từng Work.
2. Ma trận 13 loại Agent với evidence và mức độ vận hành.
3. AI Member Capability Matrix cho từng thành viên/provider.
4. Bản đồ kiến trúc/luồng AI thực tế và điểm đứt gãy end-to-end.
5. Work ownership/dependency/overlap map; đề xuất canonical owner và consumer.
6. Capability gap register, ưu tiên P0/P1/P2, tác động và tiêu chí nghiệm thu.
7. Target capability architecture: shared core + per-AI profiles + policy/identity/evidence contracts.
8. Kế hoạch triển khai theo lát cắt nhỏ, có gate và human approval; chưa thực thi trong giai đoạn audit.

## 8. Gate
G0 — Inventory snapshot và đối chiếu nguồn registry.
G1 — Portfolio intake: manifest/owner/status/canonical source cho toàn bộ Work; ghi rõ UNASSESSED.
G2 — Capability matrix 13 Agent và AI Member profiles.
G3 — Trace luồng AI end-to-end và xác minh runtime/dispatch/evidence.
G4 — Gap, dependency, overlap, ownership và security analysis.
G5 — Phản biện độc lập, biên bản và nhật ký chuẩn.
G6 — Xu trình Vinh quyết định kiến trúc/ưu tiên.
G7 — Chỉ sau quyết định mới lập kế hoạch build/acceptance; không tự ý triển khai.

## 9. Điều kiện hoàn thành
Mỗi kết luận phải chỉ rõ Work ID, đường dẫn tài liệu/code, revision hoặc mốc evidence, phương pháp kiểm tra, trạng thái và giới hạn. Work chưa đọc phải giữ UNASSESSED; năng lực chưa chạy phải giữ NOT_VERIFIED. Hoàn tất kiểm kê không đồng nghĩa năng lực đã được xây dựng hoặc production-ready.
