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
     │  message/send (artifact + acceptance)   │          

           │
     ├────────────────────────────────────────►│  verify hash        │
     │                                        ├────────────────────►│  run artifact+program
     │                                        │◄────────────────────┤  ok/timeout/stderr
     │◄────────────────────────────────────────┤  verdict.json      │
     │  PASS + evidence?  -> status=PASS, stop │                    │
     │  FAIL, còn lượt?   -> feedback về Coder │                    │
     │  FAIL, hết lượt    -> BLOCKED (hard cap) │                   │
```

## 3. Mapping sang A2A (D-01 / D-01c)

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
| Terminal operation | `CancelTask` → -32002; `SendMessage` continuation → -32004 | Official SDK semantics; legacy aliases remain separate |
| Transport (agent chết, timeout) | `TransportError` -> pipeline BLOCKED reason `*_transport_error` | Không treo, không im lặng |
| Sandbox timeout | result `timeout:true` -> FAIL có evidence | Timeout demo: 3s trong test |
| PASS thiếu evidence | BLOCKED `pass_without_evidence` (D-06) | Tester hỏng không được tính là PASS |

## 5. Ranh giới bảo mật của slice này

- Coder **không bao giờ** nhận acceptance programs (`contract.coder_brief()` tách field).
- Tester **không sửa** artifact; chỉ verify hash + chạy trong sandbox.
- Sandbox: ưu tiên `ContainerSandbox` khi Docker/image khả dụng; dùng `--network none`, Docker default seccomp profile, `--cap-drop ALL`, `no-new-privileges`, giới hạn CPU/RAM/PID, read-only filesystem và mount. Nếu Docker không khả dụng thì fallback về `Sandbox` subprocess với network isolation best-effort; không coi fallback này là đủ cho mã không tin cậy từ nguồn ngoài.
- Không động vào Core :8000, không tạo Core thứ hai, không sửa main source (charter §2).

## 6. Giới hạn đã biết (deferred, cần quyết định)

1. Container profile chưa có custom seccomp whitelist và image chưa pin theo digest; cần independent security review.
2. PersistentTaskStore có persistence JSON, nhưng giới hạn single-writer và flush O(n) mỗi update vẫn tồn tại.
3. Agent Card chưa ký (signed Agent Card của A2A v1.0) — trust nội bộ tạm bằng base_url kiểm soát được.
4. Coder là deterministic generator; LLM adapter là bước kế tiếp (D-03).

## 7. Iteration 2 — hardening theo D-01b / D-04b / D-08b

**D-04b — Sandbox hardening (sandbox.py v1.2):**
- Env scrub: child chỉ nhận PATH, LC_ALL=C, PYTHONDONTWRITEBYTECODE (SYSTEMROOT trên Windows) — secrets/API keys của parent không rò vào untrusted code.
- POSIX rlimits qua preexec_fn: RLIMIT_CPU 10s, RLIMIT_AS 1GB, RLIMIT_FSIZE 4MB, RLIMIT_NPROC 64 (best-effort, không fatal).
- Network isolation "auto": trên Linux dùng unshare -n khi probe xác nhận khả dụng; result có trường network_isolated.
- Input caps: artifact/program vượt 200KB bị chặn trước khi chạy (SandboxInputError).
- Giới hạn còn lại: chưa container/seccomp/cgroups — D-04 vẫn cần phê duyệt trước khi chạy untrusted code thật.

**D-08b — PersistentTaskStore (task_store.py):**
- TaskStore (in-memory, thread-safe) + PersistentTaskStore (JSON file, atomic rename qua .tmp + os.replace, load + validate khi khởi tạo, reload() mô phỏng restart).
- AgentBackend nhận store qua constructor; restart với cùng path → continuation, idempotency, audit sống lại. Giới hạn: single-writer, flush O(n) mỗi update.

**D-01b — Binding v1.2 (a2a.py):**
- Agent Card thêm protocolVersion "1.0", version "1.2.0", preferredTransport "JSONRPC".
- Task thêm contextId, createdAt, updatedAt; status có timestamp.
- tasks/cancel (server + A2AClient.cancel_task + LocalClient.cancel_task): chỉ task non-terminal được cancel, terminal là no-op, transition qua state machine (states.py).
- Vẫn stdlib-only, mọi wire code gom trong a2a.py — swap sang SDK chính thức sau vẫn chỉ sửa 1 file.

## 8. Iteration 3 — container-grade sandbox profile (D-04c)

sandbox_container.py — ContainerSandbox cùng contract run(artifact_code, program, timeout_s) như Sandbox nhưng chạy runner trong Docker container:
- --network none: không có interface mạng nào (mạnh hơn unshare -n best-effort của D-04b).
- --memory 512m, --cpus 1.0, --pids-limit 64: cap tài nguyên do kernel/cgroup cưỡng chế.
- --cap-drop ALL + no-new-privileges; Docker default seccomp profile được giữ nguyên bằng cách không truyền override `seccomp=default` (giá trị đó bị Docker hiểu là đường dẫn).
- --read-only + mount nguồn read-only: filesystem bất biến trong container.
- Env scrub và cap input 200KB tái dùng từ sandbox.Sandbox (composition).
- `TesterBackend` gọi `ContainerSandbox.available()` và chọn profile Docker khi sẵn sàng; nếu không thì dùng `Sandbox()`. `available()` probe Docker và pre-pull image.
- Giới hạn còn lại: chưa có seccomp whitelist tùy chỉnh; image chưa pin digest (supply-chain drift) — mở cho iteration sau.


## 9. Iteration 4 — official A2A SDK and signed Agent Card (D-01c)

- Wire adapter supports official A2A 1.0 JSON-RPC method names `SendMessage`, `GetTask`, `CancelTask`, returning the official Task/Artifact field shapes. Legacy lower-case methods remain only for internal compatibility.
- Agent Card exposes `supportedInterfaces`, `skills`, `defaultInputModes`, `defaultOutputModes` and a JWS signature. Public JWK set is served at `/.well-known/jwks.json`.
- CI pins `a2a-sdk[signing,encryption]==1.2.3` and uses the SDK client + verifier to validate round-trip, reject a tampered signed field, and enforce official terminal-task errors.
- Key management limit: signing key is ephemeral per server process in this prototype. Do not treat this as durable production identity; production must load a stable private key from a secret manager and enforce a trusted JWKS allowlist/rotation policy.
