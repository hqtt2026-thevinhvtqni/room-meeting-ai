# WORK51 Architecture — A2A Coder–Tester Vertical Slice

Version: 1.0 — 2026-10-23 (UTC+07). Scope: PLAN_WORK51 §4 P2 (vertical slice) + P1 artifacts.

## 1. Thành phần

```
                ┌────────────────────────────────────────────────┐
                │                  ORCHESTRATOR                   │
                │  (a2a_ct.orchestrator.run_pipeline)             │
                │  - soạn brief/feedback, tách gate PASS/BLOCKED  │
                └───────┬───────────────────────────┬──────────────┘
        message/send    │                           │   message/send
        (JSON-RPC 2.0)  │                           │
              ┌─────────▼─────────┐       ┌─────────▼─────────┐
              │   CODER AGENT      │       │   TESTER AGENT    │
              │ CoderBackend       │       │ TesterBackend     │
              │ (thấy: brief,      │       │ (thấy: acceptance │
              │  feedback — KHÔNG │       │  programs +       │
              │  thấy acceptance) │       │  artifact thật)   │
              └─────────┬─────────┘       └─────────┬─────────┘
                        │ artifact (hashed,          │ verdict.json
                        │ versioned)                │ + evidence
                        └──────────┬────────────────┘
                                   │
                          ┌────────▼─────────┐
                          │ EXECUTION        │
                          │ SANDBOX          │
                          │ tempdir + python │
                          │ -I + timeout     │
                          └──────────────────┘
```

## 2. Sequence — đường chính (P2 vertical slice)

```
Orchestrator      Coder                    Tester                  Sandbox
     │  message/send (brief)  │                │                     │
     ├────────────────────►│  emit artifact v1 │                     │
     │◄─────────────────────┤  (task completed) │                     │
     │  message/send (artifact + acceptance)   │                     │
     ├────────────────────────────────────────►│  verify hash        │
     │                                        ├────────────────────►│  run artifact+program
     │                                        │◄────────────────────┤  ok/timeout/stderr
     │◄────────────────────────────────────────┤  verdict.json      │
     │  PASS + evidence?  -> status=PASS, stop │                    │
     │  FAIL, còn lượt?   -> feedback về Coder │                    │
     │  FAIL, hết lượt    -> BLOCKED (hard cap) │                   │
```

## 3. Mapping sang A2A (D-01)

| Khái niệm A2A | Triển khai trong slice | Ghi chú |
|---|---|---|
| Agent Card | `GET /.well-known/agent-card.json` | name, capabilities, metadata (role, self_approval=false) |
| message/send | JSON-RPC 2.0, payload là JSON trong 1 text part | Binding tối thiểu; SDK chính thức thay sau tại `a2a.py` |
| Task | `{id, kind:"task", state, artifacts[], status{}, metadata{}}` | state theo A2A lifecycle |
| Task states | submitted/working/input-required/completed/failed/canceled | `states.py` chặn transition trái luật; terminal = immutable |
| Continuation | `message.taskId` trỏ task đã có | feedback của Orchestrator dùng đúng cơ chế này |
| Artifact | `{artifactId, name, parts[], metadata:{sha256, version}}` | coder artifact + verdict.json |
| tasks/get | JSON-RPC method, read-only, idempotent | |

**BLOCKED mapping (D-02):** BLOCKED là *kết quả pipeline*, không phải A2A task state. Task khi BLOCKED nằm ở state `failed` (hoặc giữ `completed` — vì bản thân agent làm xong việc của mình) + verdict/report ghi rõ. `A2A completed ≠ test PASS` (charter §5).

## 4. Error model

| Lớp | Đại diện | Hành xử |
|---|---|---|
| Malformed JSON-RPC | `-32700 / -32600` | Server trả JSON-RPC error, không crash |
| Invalid params (payload sai, taskId lạ) | `-32602` | Như trên; test `test_http.py` lock hành vi |
| Agent-level failure | task state `failed` + status.message | VD: payload kind không hỗ trợ |
| Transport (agent chết, timeout) | `TransportError` -> pipeline BLOCKED reason `*_transport_error` | Không treo, không im lặng |
| Sandbox timeout | result `timeout:true` -> FAIL có evidence | Timeout demo: 3s trong test |
| PASS thiếu evidence | BLOCKED `pass_without_evidence` (D-06) | Tester hỏng không được tính là PASS |

## 5. Ranh giới bảo mật của slice này

- Coder **không bao giờ** nhận acceptance programs (`contract.coder_brief()` tách field).
- Tester **không sửa** artifact; chỉ verify hash + chạy trong sandbox.
- Sandbox: tempdir mới mỗi lần, `python -I`, timeout cứng, cwd=tempdir. **Chưa có** container/network egress blocking (D-04, cần phê duyệt để mở rộng).
- Không động vào Core :8000, không tạo Core thứ hai, không sửa main source (charter §2).

## 6. Giới hạn đã biết (deferred, cần quyết định)

1. Sandbox chưa container hóa; untrusted code có thể gọi network.
2. Task store in-memory: restart mất state (P3 yêu cầu "trạng thái sau restart" → cần persist layer — D-08).
3. Agent Card chưa ký (signed Agent Card của A2A v1.0) — trust nội bộ tạm bằng base_url kiểm soát được.
4. Coder là deterministic generator; LLM adapter là bước kế tiếp (D-03).
