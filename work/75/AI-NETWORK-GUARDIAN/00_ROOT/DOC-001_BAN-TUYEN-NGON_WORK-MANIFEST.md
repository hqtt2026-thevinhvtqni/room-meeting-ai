# DOC-001 — Bản tuyên ngôn / Work Manifest

- Work ID: 75
- Tên: AI-NETWORK-GUARDIAN
- Product: AI-assisted Network Infrastructure Management
- Platforms: Mobile App, PC Dashboard
- Repository: hqtt2026-thevinhvtqni/room-meeting-ai
- Canonical path: work/75/AI-NETWORK-GUARDIAN/
- Branch: main (không tạo nhánh Work riêng)
- Standard: Work 70, lifecycle and documentation rules
- Status: ACTIVE / DESIGN BASELINE / NOT RELEASED
- Current phase: 01_DISCOVER → 02_DEFINE → 03_ARCHITECT baseline established; implementation not verified.
- Authority: Vinh — product owner and final approval; Xu/AI-01 — coordinator; specialist agents by explicit assignment.
- Data posture: local-first, read-only collection in initial release.
- AI posture: advisory/diagnostic; no autonomous network changes.
- Git bootstrap: 2026-11-06. Main head before bootstrap: d7266eb9bfedfc534fc87d56548e47841bb583b9.
- Sync status: GITHUB_BASELINE_CREATED; full Sandbox 8030 parity NOT VERIFIED.

## Product statement
Một hệ thống quản lý hạ tầng mạng nội bộ thống nhất, vận hành trên Mobile và PC, có AI hỗ trợ quan sát, phát hiện, phân tích và đề xuất xử lý sự cố.

## Lifecycle
00_ROOT → 01_DISCOVER → 02_DEFINE → 03_ARCHITECT → 04_PLAN → 05_BUILD → 06_VERIFY → 06_EVIDENCE → 07_ACCEPT → 08_RELEASE → 09_OPERATE → DASHBOARD.

## Safety boundaries
1. Không ghi cấu hình router trong giai đoạn đầu.
2. Không tự động cô lập/chặn thiết bị.
3. Không hiển thị kết luận AI như sự thật nếu thiếu bằng chứng.
4. Mọi đề xuất phải có lý do, dữ liệu hỗ trợ, độ tin cậy và người phê duyệt.
