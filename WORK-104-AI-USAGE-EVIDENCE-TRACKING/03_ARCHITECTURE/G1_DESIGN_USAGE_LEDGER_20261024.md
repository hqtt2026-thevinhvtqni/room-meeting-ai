# G1 Design — Usage Ledger (PROPOSED, chờ Vinh ACK)

- Thời điểm: 2026-10-24 (UTC+7). Người soạn: Vibe (ủy quyền tự chủ của Vinh); thẩm định: Cla/Xu; ACK: Vinh.
- Trạng thái: **PROPOSED**. Đây là bản thiết kế cho #7, KHÔNG phải phê duyệt triển khai.
- Căn cứ: DECISION_G0_INTEGRATION_POINT_20261024.md (hướng in-process `core/usage_ledger.py` + append-only JSONL, không proxy); G0 inventory gốc + expansion.

## 1. Module và nguyên tắc

`core/usage_ledger.py` — một hàm ghi duy nhất, non-blocking, fail-safe:

- `record_usage_event(event: dict) -> None`: append 1 dòng JSON vào file JSONL (default `docs/usage_ledger.jsonl`, cấu hình qua env `USAGE_LEDGER_PATH`).
- **Non-blocking**: lỗi ghi ledger KHÔNG BAO GIỜ làm hỏng luồng AI chính; lỗi được nuốt và ghi fallback vào `sys.stderr` (không print stdout — tránh phá MCP stdio protocol).
- KHÔNG import MeetingManager/Discussion/Governance; chỉ module này ghi file này (không có logger thứ hai — đúng Constitution §06 chống phân tán).

## 2. Event envelope (schema v1)

Mỗi dòng JSONL gồm (trường thiếu = `null`, KHÔNG BAO GIỜ điền 0 bịa):

```json
{
  "event_id": "<uuid4>",            "occurred_at": "<ISO8601+07:00>",
  "event_type": "provider_call",    "ingested_at": "<ISO8601+07:00>",
  "ai_id": "<agents/*.yaml id>",     "ai_role": "<yaml role>",
  "provider": "anthropic|openai|groq|google|internal",
  "model": "<model string>",        "usage_source": "provider_reported|gateway_observed|estimated|unavailable",
  "input_tokens": null, "output_tokens": null, "cached_input_tokens": null, "reasoning_tokens": null,
  "other_usage": {},                "work_id": null, "task_id": null, "room_id": null,
  "meeting_id": null,               "caller": "meeting_turn|intent_router|chat",
  "status": "ok|error",             "error_class": null, "latency_ms": null,
  "content_hash": null,             "redaction_status": "metadata_only",
  "schema_version": "1"
}
```

- Cost field **chưa thêm** ở v1: chưa có pricing provenance → ghi `cost_status: "unavailable"` chỉ khi triển khai bảng giá (xem §5).
- `content_hash` = SHA-256 của response text (không lưu text). KHÔNG lưu prompt/response raw (Request_and_Scope loại trừ).

## 3. Trích usage theo từng provider (provider-specific extraction)

| Điểm chèn (từ 6 discard points) | Nguồn usage | Ghi chú |
|---|---|---|
| `AnthropicConnector.send_turn` | `data["usage"]` → `input_tokens`, `output_tokens` | `usage_source="provider_reported"` |
| `OpenAIConnector.send_turn` | `data["usage"]["prompt_tokens"|"completion_tokens"|"prompt_tokens_details.cached_tokens"] | map tương ứng; thiếu → null |
| `LlamaIntentRouter.route` | `resp.x_groq.usage` → prompt/completion tokens | provider_reported |
| `GeminiIntentRouter.route` | `resp.usage_metadata` → prompt/candidates token count | provider_reported |
| `IntentRouter` (Claude) | response `usage` | provider_reported |
| `get_groq_client()` consumers | response usage | provider_reported |

- Mock/Internal connector: KHÔNG gọi provider → ghi event với `usage_source="unavailable"`, mọi token null. Ghi rõ type để phân biệt "không có dữ liệu" với "không ghi".
- Lỗi API (timeout, 429 như evidence 2026-08-15): vẫn ghi event `status="error"` + `error_class` — activity phải thấy cả chi phí của lần gọi thất bại.

## 4. Idempotency & ghi trùng

- `event_id = uuid4` ghi lúc nhận response → 1 response = 1 event; retry caller tạo request mới = event mới (billed retry), KHÔNG phải duplicate logging.
- Không dedupe trong module (JSONL append-only); dedupe/reconciliation là việc của query layer (G4) dựa trên `provider_request_id` khi có.

## 5. Pricing provenance (đặt sau, riêng phase)

- Bảng giá đặt `docs/pricing_provenance.json` (provider, model, effective_date, per_1k_input, per_1k_output, source URL, fetched_at). Cost chỉ tính khi có provenance; không có → `cost_status="unavailable"`. Ghi nhận đây là việc #7b, đề xuất làm sau G3 khi đã có event thật.

## 6. Redaction / privacy

- Mặc định chỉ metadata + số liệu + hash. Cấm log: API keys, header, full prompt, full response, path nội bộ máy (như trong secretary_log có lộ đường dẫn Windows — ledger KHÔNG lặp lại).
- Tool-call event (G4, phase sau): chỉ `tool_name`, `status`, `latency_ms`; arguments chỉ lưu hash.

## 7. Test plan cho G3 (nêu trước để Xu/ Cla phê)

1. Unit extraction: fixture response 4 provider → đúng mapping, null giữ nguyên null.
2. Missing usage: response không có field usage → mọi token null, không có số 0.
3. Idempotency: 1 response → đúng 1 dòng JSONL.
4. Fail-safe: ledger path không ghi được (readonly/permission) → luồng chính vẫn PASS, stderr có dấu vết.
5. Redaction: quét ledger输出 không chứa key/prompt raw.
6. E2E (điều kiện Decision #3): 1 lần gọi thật (hoặc test-provider) → 1 event correlated trong ledger + 1 query tổng hợp được.

## 8. Điều kiện trước khi triển khai (lặp lại từ Decision W104-G0-006)

1. Vinh ACK bản G1 này. 2. Môi trường test ủy quyền. 3. Triển khai trên đúng nhánh work/104, không đụng Protected Core authority. 4. agents/*.yaml cần model thật cho đường P1/P2 trước khi kỳ vọng usage thật.
