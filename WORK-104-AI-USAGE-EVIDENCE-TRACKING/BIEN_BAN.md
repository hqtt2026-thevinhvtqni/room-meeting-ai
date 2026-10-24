# BIEN_BAN.md — Work 104: AI Usage & Evidence Tracking

- Quản lý: Co (build owner). Bản chính thức duy nhất theo AGENTS.md §06.1.
- Ngày lập: 2026-10-24 (UTC+7).

## 1. Phạm vi đã thống nhất
Xây dựng năng lực provider-neutral cho ROOM-HOP: ghi nhận định danh AI (ai_id, role), Work/task/room, provider/model, usage/token theo nguồn rõ ràng (provider_reported / gateway_observed / estimated / unavailable), chi phí kèm pricing provenance, latency/retry/error, tool calls, artifact và bằng chứng nghiệm thu độc lập.

## 2. Giới hạn cứng (quyết định của Vinh / Xu)
- Core :8000 nằm NGOÀI Sandbox; tuyệt đối không tạo Core/Host/Dispatcher thứ hai.
- MCP :8030 là đường build-zone hiện hành; không ép mọi provider qua một proxy khi chưa có bằng chứng.
- Thiếu dữ liệu ghi `null` + `unavailable`; không bịa zero. Không log secrets.
- File/đashboard được tạo KHÔNG đồng nghĩa PASS. Evidence First mọi tuyên bố.

## 3. Quyết định kỹ thuật đã thống nhất
- Bắt đầu bằng Discovery (G0): kiểm kê invocation paths, adapters, điểm mất usage trước khi chọn integration point. Quyết định ngày 2026-10-24 bởi Xu, ghi tại JOURNAL_THI_CONG_20261024 (đã hợp nhất vào NHAT_KY_HOP_THI_CONG.md).
- Event envelope chuẩn hóa + usage ledger là thiết kế đề xuất (03_ARCHITECTURE/AI_USAGE_EVIDENCE_ARCHITECTURE.md — Status: PROPOSED, chưa phải implementation evidence).
- PostgreSQL là candidate cho bản ghi vận hành; ClickHouse hoãn đến khi có đo đạc quy mô. LiteLLM/FastAPI proxy chỉ cân nhắc khi discovery chứng minh cần.
- Acceptance gates G0–G5 và điều kiện Necessary/Sufficient đã chốt tại 00_ROOT/WORK_MANIFEST.md và 05_TEST/ACCEPTANCE_AND_E2E_PLAN.md.

## 4. Quyết định vận hành 2026-10-24 (bổ sung bởi Vibe theo ủy quyền của Vinh)
- Chuẩn hóa hồ sơ điều hành Work 104 theo AGENTS.md §06: tạo BIEN_BAN.md, KE_HOACH_THI_CONG_XU.md, NHAT_KY_HOP_THI_CONG.md tại thư mục gốc Work; JOURNAL_THI_CONG_20261024.md được hợp nhất có kiểm soát và đánh dấu SUPERSEDED.
- Cập nhật context/PROJECT_STATE.md bổ sung trạng thái Work 104 (ACTIVE — INITIALIZATION) để Truth Table phản ánh thực trạng.

## 5. Chưa quyết / chờ evidence
- Integration point cuối cùng (chờ G0 Discovery).
- Lựa chọn persistence cuối cùng (chờ G0).
- Dọn cây repo gốc: `tmp/`, `trash/`, `agent_test/` chứa file rác (desktop.ini, *.bak, hello.txt). Không xóa trong lần này vì Evidence First cấm hủy bằng chứng lịch sử tùy tiện; chờ Vinh/Xu phê duyệt danh sách xóa.
