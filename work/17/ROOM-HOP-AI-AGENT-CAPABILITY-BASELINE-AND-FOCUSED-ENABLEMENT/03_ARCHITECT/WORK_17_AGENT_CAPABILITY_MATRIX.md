# MA TRẬN NĂNG LỰC 13 LOẠI AGENT — WORK 17 (G2)

- Work ID: 17 · Ngày lập: 2026-11-19 · Trạng thái: ACTIVE — READ/TRACE ONLY
- Quy tắc: chỉ đánh giá theo bộ tiêu chí evidence E0–E4 trong 02_DEFINE/WORK_17_EVIDENCE_ACCEPTANCE_CRITERIA.md.
- Mọi ô trống = UNASSESSED. Không dùng nhãn "Có". Không PASS khi thiếu phương pháp và evidence.
- Nguồn code-level có thể khai thác làm bằng chứng E1 (đã kiểm tra tồn tại trên GitHub main kỳ 2026-11-19):
  `core/` (Core HTTP runtime entrypoint, fail-closed mount), `room_hop_mcp/`, `execution_host/`, `integration/`, `schemas/`, `tests/`, `pytest.ini`, `w14_browser_e2e.py`, `w14_w13_real_execution_test.py`, `wee_work13_adapter.py`.

## Ma trận

| # | Loại Agent | Trạng thái | Cấp evidence tối đa | Điểm tra trong repo | Phương pháp xác minh còn thiếu | Work liên quan |
|---|------------|------------|---------------------|---------------------|-------------------------------|----------------|
| 1 | Simple Reflex Agent | UNASSESSED | E1 (candidate source) | `agents/me_agent.py` | Xác định agent này có đúng taxonomy reflex hay chỉ là rule-based placeholder; kiểm tra behavior bằng test/runtime | TBD |
| 2 | LLM-based Agent | UNASSESSED | E1 | `chat.py`, `claude_chat.py`, `gemini_chat.py`, `llama_chat_v2.py`, `core/connectors.py` | Session log thật từ provider; exact model/provider, request/response, retry/usage và ACK | W501, W502 |
| 3 | Tool-Using Agent | UNASSESSED | E1 | `core/file_ops_agent.py`, `core/vscode_agent.py`, `core/intent_router.py`, `core/gemini_intent_router.py`, `core/llama_intent_router.py` | Trace provider/tool request → dispatch → policy decision → tool result; negative authorization test and runtime log | W01, W02, W12, W13 |
| 4 | Planning Agent | UNASSESSED | E0 | `30/GPT-AUTONOMOUS-BUILD-TEAM/02_EXTENSION/MODEL_4AI_PLANNING_LOOP_V2.md` (protocol document only) | Source implementation of planner + one real task decomposition, dependency/checkpoint trace and result verification | W31, W30 |
| 5 | Memory-Enabled Agent | UNASSESSED | E1 (file-context candidate) | `core/context_loader.py`, `context/XU_MEMORY.md` | Prove retrieval/update lifecycle, source provenance, freshness, conflict handling and context-drift controls; current loader only suggests/packages manually selected files | TBD |
| 6 | Multi-Agent System | UNASSESSED | E1 (orchestration source; mock path) | `core/connectors.py`, `core/discussion.py`, `run_meeting_v2.py` | One real multi-provider E2E with authenticated recipient, dispatch receipt, explicit ACK, transcript and independent replay; current v2 runner builds MockConnector for most participants | W13, W14, W52 |
| 7 | Hierarchical Agent | UNASSESSED | — | No dedicated hierarchical supervisor/delegation implementation identified in this source pass | Find a canonical supervisor/delegation module and prove parent→child task authority, delegation scope, result aggregation and failure propagation | W09, W091, W30 |
| 8 | Self-Improving Agent | UNASSESSED | E0 | `work/502/ME-AUTONOMOUS-AI-BUILDER/04_PLAN/IMPLEMENTATION_ROADMAP.md` (provisional plan; BUILD NOT AUTHORIZED) | Find implemented feedback/evaluation/update loop, bounded change policy, approval gate, rollback and regression evidence | W502 |
| 9 | RAG Agent | UNASSESSED | E0 | `work/103/ROOM-HOP-RAG-RETRIEVAL-CAPABILITY/03_ARCHITECTURE/DECISIONRAG_RETRIEVAL_EXPERIMENT_PLAN_20261111.md` (experiment plan only) | Locate canonical retrieval implementation; run a read-only query with source citations, corpus/query hashes and retrieval trace; DecisionRAG plan is NOT EXECUTED | W103, W104 |
| 10 | Coding Agent | UNASSESSED | E0 | No dedicated coding-agent implementation identified; `core/file_ops_agent.py` is file-operation tooling, not proof of code-generation capability | Locate a canonical code-writing agent and prove prompt→patch→test→repair→verified artifact with exact source and CI evidence | W30, W51, W300, W1111 |
| 11 | Web-Browsing Agent | UNASSESSED | E1 | `room_hop_mcp/browser_agent_adapter/adapter.py`, `room_hop_mcp/adapter/browser_server.py`, `w14_browser_e2e.py` | Real browser session with correlated run ID, browser/network trace, artifact hash and teardown log; current finding is source-only | W09, W091, W14 |
| 12 | Computer-Using Agent | UNASSESSED | E1 | `10/COMPUTER-AGENT/04_CODE/agent_runtime.py`, `10/COMPUTER-AGENT/04_CODE/agent_api.py`, `execution_host/` | Host session record, authorized action trace, screenshot/artifact hash, teardown and negative safety test on exact revision | W10, W12, W13, W14 |
| 13 | Autonomous Agent | UNASSESSED | E0 | `work/502/ME-AUTONOMOUS-AI-BUILDER/04_PLAN/IMPLEMENTATION_ROADMAP.md` (BUILD NOT AUTHORIZED); W14 E2E harness is not itself proof of an autonomous agent | Bounded autonomous run from goal→plan→tool execution→verify→recovery with kill-switch, authority checks and independent evidence | W502, W75, W76 |

## Ghi chú kiểm soát

1. Nhiều nhánh agent script ở root repo (`chat.py`, `claude_chat.py`...) tồn tại mức E1 nhưng mang tính prototype; cần đối soát với `room_hop_mcp/` để xác định canonical engine, tránh vi phạm nguyên tắc "một năng lực — một owner".
2. Thư mục gốc còn dữ liệu runtime (`log.jsonl`, `pytest_output.txt`, `tmp/`, `trash/`, `desktop.ini`) là dấu hiệu "runtime data policy" chưa được thực thi sạch; ghi nhận cho GAP-10.
3. Ma trận này là khung G2 (bắt buộc): điền trạng thái là việc của Gate G2, mỗi ô phải đạt ít nhất E1 (SOURCE) trước khi coi là đã tiến hành.


## G2 source-trace addendum — 2026-11-19

- Snapshot: GitHub main `fe30ef4abf165f1534745281113da837c5c88304`; recursive tree SHA `309463636bc2bc420e5baf616ab1efeec54333f2` (`truncated=false`). Source/blob readback was performed for the candidate paths referenced in rows 1–6 and 11–12; relevant examples include `agents/me_agent.py` (`3915134e4f9cb8c3ad660b946edcac4e0cc597eb`), `core/agent_registry.py` (`7e4b98e68fa1a208ebd5788d9235d9c222e402a3`), `core/file_ops_agent.py` (`02fe29420699f5a7c5df19ea182d92d9899ca8e5`), `core/vscode_agent.py` (`47c9233c343c531cbe81353f62095e281f9d4d58`), `core/context_loader.py` (`0f686e594d248dfd93287271e8ac4d483feb5ef2`), `context/XU_MEMORY.md` (`af64eff272d353e6eec986aaa846904de687186d`), `core/connectors.py` (`809c4d2fca01e6fcdaf26b91bf34b1af26dfd15a`), `core/discussion.py` (`aa722f95235f613c288ba212074527ed2ce01ebc`), `room_hop_mcp/browser_agent_adapter/adapter.py` (`0ced9207c1897b9a7b572b7fefa44fec2dd92b76`), and `10/COMPUTER-AGENT/04_CODE/agent_runtime.py` (`e8153c180afc571efc5fe3e2b2afdee3afc88d13`).
- Source-level observations:
  1. `agents/me_agent.py` describes itself as a local rule-based placeholder; it is only a candidate for Simple Reflex classification, not a verified agent category.
  2. Provider/chat files and connector/router code exist for LLM-based and tool-using paths. Existence is E1 only; no provider call, token usage or live session was run in this audit.
  3. `core/context_loader.py` performs keyword suggestions and packages manually selected context files; `context/XU_MEMORY.md` is a static file. This does not establish autonomous memory retrieval, writeback or drift control.
  4. `run_meeting.py` explicitly states v0.1 uses scripted exchange instead of real AI API calls. `run_meeting_v2.py` constructs MockConnector for most participants; `core/connectors.py` and `core/discussion.py` provide orchestration source, but no real multi-provider dispatch/ACK E2E was run.
  5. Work 30 planning-loop file is a protocol document, not planner implementation. Work 103 DecisionRAG file is marked PROPOSED EXPERIMENT — NOT EXECUTED. Work 502 roadmap says BUILD NOT AUTHORIZED. These remain E0.
  6. Browser adapter and Work 10 computer-agent runtime source exist (E1); browser/computer sessions and artifact/teardown evidence were not generated in this pass.
  7. No dedicated hierarchical supervisor implementation or dedicated coding-agent implementation was identified in the inspected source paths. FileOpsAgent is file-operation tooling, not proof of coding-agent capability.
- Matrix status: all 13 rows remain `UNASSESSED`; E1 candidate source is not a capability PASS. Rows 4, 8, 9, 10 and 13 remain E0; row 7 has no identified implementation source. No E2/E3/E4 evidence was created.
- Execution status: READ/TRACE only; no test, model/provider call, browser session, computer session, runtime process or deployment was run. No source/runtime changes.
