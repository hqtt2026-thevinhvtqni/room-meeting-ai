# BIEN_BAN.md — Work 52

## Quyết định khởi tạo
- **Thời điểm:** 2026-10-23 (UTC+07:00)
- **Điều phối:** Xu (AI-01, Planner)
- **Thẩm quyền:** Vinh > Xu > Agent
- **Trạng thái:** DECISION — mở Work để thiết kế nền tảng giao tiếp/điều phối AI dùng chung toàn ROOM-HOP.

### Bối cảnh
Codex có App Server/SDK; Qwen Code có giao diện điều khiển riêng như ACP hoặc service interface tùy phiên bản. Các giao diện không mặc nhiên tương thích. ROOM cần hợp đồng nội bộ chung và adapter theo runtime, không chọn một nhà cung cấp làm chuẩn duy nhất.

### Quyết định
1. Work 52 thiết kế ROOM Universal AI Communication & Orchestration dùng chung toàn ROOM-HOP.
2. Provider-neutral; mọi provider kết nối qua adapter.
3. A2A task contract là hợp đồng nội bộ chuẩn; giao thức bên ngoài chỉ là chi tiết adapter.
4. Tái sử dụng Core, Agent Runtime, Gateway, MCP 8030 và Sandbox sau khi truy vết; không dựng dịch vụ trùng.
5. Work 28 tiếp tục phụ trách nền tảng công cụ/MCP; Work 51 áp dụng A2A cho Coder–Tester; Work 30 có thể tiêu thụ nền tảng. Không chuyển phạm vi các Work đó sang Work 52.
6. Giữ ranh giới Core :8000, Dashboard :3000 render-only, Sandbox là vùng build; không tự commit/push/merge/release.
7. Triển khai theo READ → TRACE → ANALYZE → DECIDE → BUILD → VERIFY → HANDOFF.

### Chưa được kết luận
- Chưa xác minh runtime Codex App Server và Qwen ACP/service trong các môi trường thực tế.
- Chưa chốt vị trí triển khai, transport nội bộ hoặc schema cuối cùng trước khi đọc source/config hiện hữu.
- Chưa có E2E evidence; Work 52 chưa PASS và chưa RELEASED.
