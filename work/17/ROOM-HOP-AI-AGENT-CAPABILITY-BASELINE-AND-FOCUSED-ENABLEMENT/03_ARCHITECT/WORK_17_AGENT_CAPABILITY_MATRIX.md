# MA TRẬN NĂNG LỰC 13 LOẠI AGENT — WORK 17 (G2)

- Work ID: 17 · Ngày lập: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Quy tắc: chỉ đánh giá theo bộ tiêu chí evidence E0–E4 trong 02_DEFINE/WORK_17_EVIDENCE_ACCEPTANCE_CRITERIA.md.
- Mọi ô trống = UNASSESSED. Không dùng nhãn "Có". Không PASS khi thiếu phương pháp và evidence.
- Nguồn code-level có thể khai thác làm bằng chứng E1 (đã kiểm tra tồn tại trên GitHub main kỳ 2026-11-19):
  `core/` (Core HTTP runtime entrypoint, fail-closed mount), `room_hop_mcp/`, `execution_host/`, `integration/`, `schemas/`, `tests/`, `pytest.ini`, `w14_browser_e2e.py`, `w14_w13_real_execution_test.py`, `wee_work13_adapter.py`.

## Ma trận

| # | Loại Agent | Trạng thái | Cấp evidence tối đa | Điểm tra trong repo | Phương pháp xác minh còn thiếu | Work liên quan |
|---|------------|------------|---------------------|---------------------|-------------------------------|----------------|
| 1 | Simple Reflex Agent | UNASSESSED | — | — | Xác định module phản xạ đơn giản (nếu có) trong core/ | TBD |
| 2 | LLM-based Agent | UNASSESSED | E0 | `chat.py`, `claude_chat.py`, `gemini_chat.py`, `llama_chat_v2.py`, `build_prompt.py` | Session log thật từ một cuộc gọi model | W501, W502 |
| 3 | Tool-Using Agent | UNASSESSED | E0 | `room_hop_mcp/`, `work/28/MCP-8020-TOOLING-PLATFORM` | Attempt log tool-call + retry/timeout | W28, W12 |
| 4 | Planning Agent | UNASSESSED | E0 | `docs/` (planning briefs) | Một lần phân rã nhiệm vụ thật → checkpoint được ghi | W31, W30 |
| 5 | Memory-Enabled Agent | UNASSESSED | — | `context/` | Provenance của memory + chống context drift | TBD |
| 6 | Multi-Agent System | UNASSESSED | E0 | `agents/`, `meeting room scripts (run_meeting*.py)` | One E2E multi-agent handoff có log liền mạch | W13, W14 |
| 7 | Hierarchical Agent | UNASSESSED | — | — | Bằng chứng điều phối phân cấp thật | W09, W091 |
| 8 | Self-Improving Agent | UNASSESSED | — | — | Feedback loop có kiểm soát; cần approval gate | W502 |
| 9 | RAG Agent | UNASSESSED | E0 | `work/103` (DecisionRAG experiment plan) | Truy vấn thử read-only trả citation | W103, W104 |
| 10 | Coding Agent | UNASSESSED | E1 | `core/`, `tests/`, GitHub Actions workflow, 1379 commits | CI run xanh gần nhất + test report lưu 06_EVIDENCE | W300, W1111 |
| 11 | Web-Browsing Agent | UNASSESSED | E1 | `w14_browser_e2e.py`, `w14_w13_real_execution_test.py` | Session browser thật + artifact hash | W14, W13 |
| 12 | Computer-Using Agent | UNASSESSED | E0 | `work/10/COMPUTER-AGENT`, `execution_host/` | Session record + teardown log | W10, W12 |
| 13 | Autonomous Agent | UNASSESSED | — | `work/502/ME-AUTONOMOUS-AI-BUILDER` | Kịch bản chạy tự chủ có kill switch test | W502, W75, W76 |

## Ghi chú kiểm soát

1. Nhiều nhánh agent script ở root repo (`chat.py`, `claude_chat.py`...) tồn tại mức E1 nhưng mang tính prototype; cần đối soát với `room_hop_mcp/` để xác định canonical engine, tránh vi phạm nguyên tắc "một năng lực — một owner".
2. Thư mục gốc còn dữ liệu runtime (`log.jsonl`, `pytest_output.txt`, `tmp/`, `trash/`, `desktop.ini`) là dấu hiệu "runtime data policy" chưa được thực thi sạch; ghi nhận cho GAP-10.
3. Ma trận này là khung G2 (bắt buộc): điền trạng thái là việc của Gate G2, mỗi ô phải đạt ít nhất E1 (SOURCE) trước khi coi là đã tiến hành.
