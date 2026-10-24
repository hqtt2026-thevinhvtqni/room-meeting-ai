# G0 Discovery Inventory — Work 104: AI Usage & Evidence Tracking

- Thời điểm: 2026-10-24 (UTC+7)
- Người thực hiện: Vibe (agent hỗ trợ, ủy quyền tự chủ của Vinh)
- Trạng thái: DONE — bản ghi discovery; chưa phải PASS gate (chờ Xu/Cla phê duyệt theo #6)
- Phương pháp: đọc trực tiếp từng file trên nhánh `work/104-ai-usage-evidence-tracking` (commit c750ad6f); mỗi mục dưới đây đều có file evidence.

## 1. Inventory các đường AI invocation (AI → provider API)

| # | Đường gọi | File evidence | Provider / Model | Usage có sẵn ở response? | Hiện trạng ghi nhận usage |
|---|---|---|---|---|---|
| P1 | Meeting turn — Anthropic | `core/connectors.py` (AnthropicConnector.send_turn, POST api.anthropic.com/v1/messages) | Anthropic / theo `agents/*.yaml` | CÓ (field `usage` trong response JSON) | **BỎ QUA** — code chỉ parse text blocks, không đọc `usage` |
| P2 | Meeting turn — OpenAI | `core/connectors.py` (OpenAIConnector.send_turn, POST api.openai.com/v1/chat/completions) | OpenAI / theo yaml | CÓ (`data["usage"]`) | **BỎ QUA** — chỉ lấy `choices[0].message.content` |
| P3 | Meeting turn — Mock/Internal | `core/connectors.py` (MockConnector, InternalConnector) | none / local | KHÔNG (không gọi mạng) | N/A — usage = `unavailable`, cost = 0 không bịa |
| P4 | Intent routing — Claude | `core/intent_router.py` (tham chiếu từ llama/gemini router) | Anthropic | CÓ | **BỎ QUA** |
| P5 | Intent routing — Llama/Groq | `core/llama_intent_router.py` (Groq chat.completions, model llama-3.3-70b-versatile) | Groq | CÓ (`resp.x_groq.usage`) | **BỎ QUA** — chỉ đọc `choices[0].message` |
| P6 | Intent routing — Gemini | `core/gemini_intent_router.py` (google-genai generate_content, có fallback models) | Google | CÓ (`usage_metadata`) | **BỎ QUA** |
| P7 | Chat自如 qua Groq client chung | `core/groq_config.py` (get_groq_client, dùng cho llama_chat*.py) | Groq | CÓ (trong response) | **BỎ QUA** |

## 2. Nguồn định danh AI (ai_id / provider / model)

- `agents/*.yaml`: 12 agent (xu=openai, claude=anthropic, me_meta=internal, kha_gpt, kha_gemini, claude, coo, cto, cro, market, ka_csa, quan_gia). Field `provider`, `model` sẵn dùng làm ai_id/model.
- LƯU Ý BLOCKER: `model: ""` ở xu.yaml và claude.yaml → Real API Connector vẫn 🟡 PENDING (khớp PROJECT_STATE). Trước khi có usage thật từ P1/P2 cần Vinh khai báo model thật.
- Execution host: `execution_host/identity.py` (RuntimeIdentity, bind_address :8031) — định danh runtime, chưa có correlation sang ai_id.

## 3. Điểm instrument cho tool activity / work correlation

- MCP 8030: `room_hop_mcp/adapter/server.py` — 4 tool: list_meetings, get_meeting, get_transcript, add_paste_to_meeting. `add_paste_to_meeting` đã có `identity_id` tùy chọn (legacy path khi thiếu) → điểm gắn ai_id sẵn có.
- Execution host :8031: `execution_host/server.py` — POST /execute nhận `WorkContext` + `ExecutionRequest`, trả result dict → đã có sẵn work context correlation, chưa log usage.
- Audit log đang tồn tại: `core/file_ops_audit.jsonl` — tiền lệ JSONL append-only, tái dùng được cho usage ledger.

## 4. Usage-discard points (danh sách bắt buộc theo Request_and_Scope)

1. `AnthropicConnector.send_turn` — bỏ `data["usage"]`.
2. `OpenAIConnector.send_turn` — bỏ `data["usage"]`.
3. `LlamaIntentRouter.route` — bỏ `x_groq.usage`.
4. `GeminiIntentRouter.route` — bỏ `usage_metadata`.
5. `IntentRouter` (Claude) — bỏ usage.
6. `get_groq_client()` consumers — bỏ usage.

## 5. Kiến nghị integration point nhỏ nhất (chờ #6 phê duyệt)

KHÔNG cần proxy (LiteLLM/FastAPI). Đề xuất: 1 module `core/usage_ledger.py` ghi event JSONL theo envelope ở 03_ARCHITECTURE, được gọi tại 6 discard points trên. Lý do:
- Mọi provider response đều có usage sẵn, chỉ cần đọc thêm 1 field — thay đổi nhỏ nhất, đủ coverage P1–P7.
- Không chạm Meeting Manager / Discussion Engine / Core 4 lõi v0.1 (connector chỉ thêm ghi log sau khi nhận response).
- MCP 8030 và Execution host là 2 điểm cộng thêm tool-event; core/file_ops_audit.jsonl là tiền lệ format.

## 6. Hạn chế của bản ghi này (CHƯA XÁC MINH)

- Chưa chạy code (chỉ tĩnh đọc file trên nhánh work/104) — chưa xác minh runtime thực tế của :8000/:8030/:8031.
- Chưa khảo sát thư mục 30/, 10/COMPUTER-AGENT, integration/, research/ — có thể còn đường gọi AI khác; ghi thành đầu việc tiếp theo của #5 nếu Xu yêu cầu coverage 100%.
- Bảng giá (pricing) provider chưa thu thập → cost_status = `estimated/unavailable` cho đến khi có pricing provenance (#7).
