# G1 Design — Usage Ledger (ACKED — REV 6 FINAL)

- Thời điểm: 2026-10-24 (UTC+7). Người soạn: Vibe (ủy quyền tự chủ của Vinh); thẩm định: Cla/Xu; ACK: Vinh.
- Trạng thái: **ACKED — REV 6 (FINAL)**. REV 5 đã được Xu thẩm định vòng cuối; Vinh ACK có điều kiện ngày 2026-10-24 (qua Vibe, điều kiện: chuẩn hóa nhãn §3 bị lặp — đã hoàn tất ở REV 6 này). Quyết định kèm theo ACK: #7c giữ mở, chưa cấp quyền triển khai; gitlink room-meeting-ai/ giữ nguyên, kiểm kê tiếp tục BLOCKED chờ URL nguồn. Nội dung thiết kế không đổi từ REV 5. KHÔNG tạo file thiết kế cạnh tranh — các REV thay thế nhau tại cùng đường dẫn.
- Căn cứ: DECISION_G0_INTEGRATION_POINT_20261024.md (hướng in-process `core/usage_ledger.py` + append-only JSONL, không proxy); G0 inventory gốc + expansion.

## 1. Module và nguyên tắc

`core/usage_ledger.py` — một hàm ghi duy nhất, non-blocking, fail-safe:

- `record_usage_event(event: dict) -> None`: append 1 dòng JSON vào file JSONL; mặc định dùng tên theo tháng `docs/usage_ledger-YYYYMM.jsonl` như §5b, có thể override đường dẫn bằng env `USAGE_LEDGER_PATH`.
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
  "meeting_id": null, "turn_number": null, "attempt_id": null, "parent_event_id": null,
  "caller": "meeting_turn|intent_router|chat",
  "provider_request_id": null,
  "cost_amount": null, "cost_currency": "USD", "pricing_version": null,
  "cost_status": "unavailable",
  "status": "ok|error",             "error_class": null, "latency_ms": null,
  "content_hash": null,             "redaction_status": "metadata_only",
  "schema_version": "1"
}
```

- **Cost trong schema v1 NGAY** (không phải chờ): 4 trường `cost_amount / cost_currency / pricing_version / cost_status` đã nằm trong envelope từ REV 2. Định nghĩa `cost_status`:
  - `"actual"`: match pricing entry `status: "verified"` (nguồn chính thức + người xác thực ghi tên) → `cost_amount` là số tính được.
  - `"estimated"`: dùng giá chưa xác thực → `cost_amount` là ước tính, bắt buộc kèm `pricing_version` để truy nguồn.
  - `"unavailable"`: không match pricing (hoặc lỗi tính) → `cost_amount: null`. KHÔNG bao giờ lấp 0. Ban đầu (chưa có #7b) mọi event đều `"unavailable"`.
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
- **Usage theo từng giai đoạn lỗi (3 trường hợp KHÔNG gộp chung):**
  1. **Lỗi trước khi có phản hồi** (timeout, DNS, connection refused, 429/5xx trả về nhưng body không có usage): ghi event `status="error"`, mọi token `null`, `usage_source="unavailable"` — KHÔNG bịa số token cho lần gọi thất bại.
  2. **Lỗi có phản hồi kèm usage** (response/headers chứa usage — ví dụ Groq 429 có rate-limit headers, hoặc HTTP error body có `usage`): ghi `status="error"`, trích token đúng như §3, `usage_source="provider_reported"`. Lần gọi hỏng mà provider vẫn đếm token phải hiện đúng trong ledger.
  3. **Lỗi khi ghi ledger** (file readonly, đĩa đầy): event đó KHÔNG vào JSONL — **mất CÓ KIỂM SOÁT nhưng KHÔNG được coi là mất 0**: ghi 1 dòng đếm vào `docs/usage_ledger_failures.log` (chỉ timestamp + count) + stderr.
  - **Giới hạn bộ đếm dự phòng (REV 3):** `failures.log` nằm CÙNG ổ/file hệ thống → có thể hỏng theo. Nó chỉ là **best-effort**, KHÔNG phải bằng chứng độc lập tuyệt đối. Quy tắc:
    a. Nếu ghi `failures.log` cũng lỗi → chỉ còn stderr; event đó KHÔNG có đường ghi bền vững nào.
    b. **Nguồn thu thập stderr (REV 4 — khai báo thẳng):** trong v1, KHÔNG có cơ chế thu thập stderr vào nguồn truy vấn được — stderr đi về môi trường khởi chạy tiến trình (terminal/service journal) và Work 104 KHÔNG kiểm soát được nó. Do đó khi cả hai path hỏng, G4 **không có số đếm loss chính xác từ bất kỳ nguồn nào của hệ thống**.
    c. Báo cáo/query layer (G4) PHẢI hiển thị rõ 3 mức: `số event trong ledger` / `số loss theo counter (nếu counter ghi được)` / `mất không xác định được đếm (khi counter cũng hỏng)`.
    d. **Nguồn xác định khoảng mất (REV 5 — điểm cuối theo thẩm định Xu):** hệ thống KHÔNG có nguồn quan sát độc lập nào để tự phát hiện khoảng thời gian mất khi cả hai đường ghi hỏng. Quy tắc:
       - Khoảng thời gian ghi trong báo cáo PHẢI là **khoảng vận hành được người vận hành xác nhận** (ví dụ "tiến trình chạy 14:00–15:00, người vận hành xác nhận ledger hỏng từ ~14:20") hoặc **khoảng nghi ngờ do người vận hành cung cấp** — KHÔNG PHẢI khoảng hệ thống tự phát hiện. Mỗi khoảng phải ghi kèm nguồn cung cấp (ai xác nhận, dựa trên gì).
       - Nếu không có căn cứ xác định thời điểm bắt đầu/kết thúc → báo cáo ghi thẳng **"thời gian và phạm vi thất thoát KHÔNG xác định được"**, không ghi khoảng suy đoán.
       - **KHÔNG tự suy ra** thời gian, số lượng hoặc phạm vi từ việc chỉ biết hai đường ghi đã hỏng; biết "cả hai path hỏng" chỉ cho phép phát biểu giới hạn, không cho phép phát biểu đo lường.
       - Việc đối soát service journal/đầu ra tiến trình bên ngoài (nếu có) là **đầu vào thủ công của người vận hành** cho báo cáo, không phải output tự động của hệ thống; báo cáo phải ghi rõ đấy là căn cứ ngoài hệ thống.
    e. **KHÔNG BAO GIỜ tuyên bố completeness** khi tồn tại loss "không xác định"; completeness chỉ phát biểu khi đối soát ledger + counter (+ index xoay vòng §5b) khớp nhau trong khoảng thời gian báo cáo.
    f. Kiểm thử G3 cho trường hợp kép được định nghĩa thành mục riêng #7 trong test plan §7 (REV 6: bỏ nhãn trùng lặp ở đây, chỉ giữ tham chiếu).

## 4. Idempotency & ghi trùng

- **Vòng đời event (event lifecycle — QUAN TRỌNG REV 3):**
  1. **KHỞI TẠO lúc bắt đầu cuộc gọi** (trước khi gửi request): cấp `event_id = uuid4`, ghi `occurred_at`, `ai_id/provider/model/caller`, correlation. Lúc này event là bản nháp trong bộ nhớ caller.
  2. **KẾT THÚC khi có một trong hai**: (a) nhận response (thành công hoặc lỗi-có-response) → điền token/usage/latency/content_hash rồi ghi 1 dòng hoàn chỉnh vào JSONL; (b) **hết thời gian/kết nối thất bại, KHÔNG có response** → ghi event với `status="error"`, `error_class`, mọi token null, `usage_source="unavailable"`.
  3. **Ghi một lần, dòng hoàn chỉnh** (không ghi bản nháp dở dang vào JSONL).
  - **Giới hạn tuyên bố (REV 4 — quan trọng):**
    - "1 cuộc gọi = 1 dòng" **CHỈ đúng cho cuộc gọi mà tiến trình sống đến lúc ghi dòng**. Bản nháp nằm trong bộ nhớ; **nếu tiến trình crash/kill giữa lúc bắt đầu gọi và lúc ghi, event biến mất cùng bộ nhớ và ledger KHÔNG có dấu vết nào về cuộc gọi đó** — đây là mất-không-dấu-vết được thiết kế chấp nhận ở v1.
    - Do đó `occurred_at`/`ingested_at` **KHÔNG tự phát hiện được mọi cuộc gọi bị treo**: chênh lệch 2 mốc chỉ là dấu vết *trên event đã ghi* (phát hiện ghi muộn/luồng bị nghẽn), KHÔNG phát hiện cuộc gọi crashed chưa từng ghi.
    - Phát hiện cuộc gọi crashed trong tương lai (nếu Vinh yêu cầu) phải đến từ **nguồn độc lập ngoài tiến trình** — ví dụ đối soát billing/usage từ provider, hoặc start-marker bền vững (ghi file trước khi gọi). Cả hai đều NGOÀI scope v1; ghi nhận đây là **đầu việc mở #7c — "crash-detection decision"**, chỉ làm khi có phê duyệt.
    - Mọi báo cáo reconciliation PHẢI ghi rõ giới hạn: "số liệu không bao gồm các cuộc gọi bị crash trước khi ghi".
  - Retry của caller = cuộc gọi mới = `event_id` mới + `parent_event_id` trỏ event lần thử trước (billed retry), KHÔNG phải duplicate logging.
- Không dedupe trong module (JSONL append-only); dedupe/reconciliation là việc của query layer (G4) dựa trên `provider_request_id` khi có.

## 4.2 Correlation (liên kết sự kiện — KHÔNG tạo mã giả)

- Chỉ điền `work_id/task_id/room_id/meeting_id/turn_number/attempt_id` khi **mã đã tồn tại ở caller** (ví dụ: meeting turn có sẵn room_id/meeting_id/turn_number trong MeetingManager; Work task có work_id/task_id từ Execution host). Caller truyền vào `record_usage_event(event, correlation=...)`.
- Caller KHÔNG có mã (intent router, chat tự do) → để `null`. **TUYỆT ĐỐI KHÔNG tự sinh mã nghiệp vụ giả** (không "work-unknown", không "task-0").
- Retry/lần thử: mỗi lần gọi có `attempt_id` riêng nếu caller đánh số attempt; `parent_event_id` trỏ event của lần thử trước trong cùng request khi caller giữ reference — không có thì null.
- Query layer (G4) sau này tự nối event → task qua các mã thật này; ledger không suy diễn quan hệ khi thiếu mã.

## 5. Pricing provenance (đặt sau, riêng phase)

- **Cấu trúc chốt ngay ở G1** (để không phải sửa schema sau); việc ĐIỀN DỮ LIỆU giá là #7b, làm sau G3:

```json
{
  "pricing_version": "2026-10-24.1",
  "entries": [{
    "provider": "groq", "model": "llama-3.3-70b-versatile",
    "effective_date": "2026-10-01", "currency": "USD",
    "per_1m_input": null, "per_1m_output": null,
    "source_url": "<url trang giá chính thức>", "fetched_at": "<ISO8601>",
    "verified_by": null, "status": "unverified"
  }]
}
```

- **Quy tắc tính giá (REV 4 — khớp §2, một nguồn chân lý duy nhất):**
  - Match entry `status: "verified"` → `cost_status="actual"`, `cost_amount` = số tính được từ giá đã xác minh.
  - Match entry `status: "unverified"` → `cost_status="estimated"`, `cost_amount` = ước tính, **bắt buộc** kèm `pricing_version` để truy nguồn.
  - Không match entry nào → `cost_status="unavailable"`, `cost_amount=null`. KHÔNG bao giờ lấp số 0.
  - (Đã bỏ câu "cost_amount CHỈ khi verified" cũ — quy tắc duy nhất là 3 nhánh trên, khớp đúng định nghĩa cost_status ở §2.)
- Envelope đã có sẵn 4 trường cost từ schema v1 (xem §2) — điền giá về sau KHÔNG phá schema.

## 5b. Retention & xoay vòng file ledger

- **Xoay vòng theo tháng**: file active `docs/usage_ledger-YYYYMM.jsonl` (mỗi tháng 1 file, đặt tên theo tháng UTC+7). Khởi tạo file mới khi ghi dòng đầu của tháng.
- **Ngưỡng xoay vòng bổ sung**: nếu file active vượt 20 MB → xoay sang hậu tố `.part2` trong cùng tháng (tránh file khổng lồ khó audit).
- **Thời hạn lưu**: tối thiểu **365 ngày** kể từ tháng ghi (yêu cầu audit theo Evidence First); sau 365 ngày, file cũ chuyển `docs/ledger_archive/` và **KHÔNG TỰ XÓA** — chỉ xóa khi có phê duyệt ghi rõ của Vinh theo đúng quy trình §06.4 (không hủy bằng chứng lịch sử tùy tiện).
- **Index**: mỗi lần xoay vòng ghi 1 dòng meta vào `docs/usage_ledger_index.jsonl` (file name, first/last event timestamp, event count, sha256 đầu-cuối) để reconciliation ở G4 đối chiếu không mất event qua các lần xoay.
- **Giới hạn ghi nhận**: đây là chính sách đề xuất chờ Vinh ACK cùng G1; thay đổi retention sau này KHÔNG phá schema event (chỉ đổi file layout, query layer đọc index).

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
7. **Test kép (REV 4, từ §3 mục 3d):** làm hỏng CẢ ledger path VÀ failures.log path → luồng AI chính vẫn PASS, stderr có dấu vết, và báo cáo reconciliation ghi đúng "đoạn thời gian mất không xác định được đếm" — không treo, không bịa số.
8. **Test crash-limit (REV 4, từ §4):** kill tiến trình giữa lúc bắt đầu gọi và lúc ghi dòng → xác nhận (a) ledger KHÔNG có dòng cho cuộc gọi đó, (b) báo cáo reconciliation ghi đúng giới hạn "không bao gồm cuộc gọi bị crash trước khi ghi" — xác minh tuyên bố giới hạn là đúng bằng chứng, không phải tuyên bố suông.

## 7b. Trạng thái verify MCP 5 tool (KHÔNG kết luận tương thích)

- Errata đã ghi: `integration/room_hop_integration.py` yêu cầu 5 tool (gồm `join_meeting`) trong khi static read của `room_hop_mcp/adapter/server.py` chỉ thấy 4 hằng số tool. **Đây MỚI chỉ là mâu thuẫn đọc tĩnh — KHÔNG được coi là đã xác minh hay phủ nhận tương thích.**
- Kết luận tương thích chỉ có sau khi chạy runtime kiểm tra `list_tools` thật qua MCP 8030 trong môi trường ủy quyền (điều kiện #2). Trước đó, mọi tài liệu Work 104 KHÔNG ghi "Public V1 có 4/5 tool" như fact — chỉ ghi kèm nguồn static.
- Nếu runtime cho thấy thiếu `join_meeting`: đó là finding mới, ghi vào 06_EVIDENCE và BIEN_BAN, KHÔNG sửa adapter trong scope Work 104 (tránh phạm ranh giới Core/Protected).

## 8. Điều kiện trước khi triển khai (lặp lại từ Decision W104-G0-006)

1. Vinh ACK bản G1 này — đã được ghi nhận có điều kiện ngày 2026-10-24, điều kiện chuẩn hóa nhãn §3 hoàn tất trong REV 6. 2. Môi trường test ủy quyền vẫn là điều kiện bắt buộc cho G3; hiện chưa được xác minh trong phiên này. 3. Triển khai trên đúng nhánh work/104, không đụng Protected Core authority. 4. agents/*.yaml cần model thật cho đường P1/P2 trước khi kỳ vọng usage thật.
