# WORK 10 — WORKFLOW CONTRACT

**Status:** LOCKED (Specification)
**Owner:** Work 10 — COMPUTER-AGENT
**Last update:** 2026-10-04

---

## 1. Purpose

Workflow Contract định nghĩa vòng đời thực thi của một task.  
Agent **không được** nhảy trạng thái tùy tiện.

Đặc biệt: **không được** coi “đã click thành công” = PASS.

---

## 2. State Machine (Bắt buộc)

```
PLANNED
   ↓
RUNNING
   ↓
VERIFYING
   ↓
┌── PASS
├── FAIL
└── BLOCKED
```

### Định nghĩa trạng thái

| State       | Ý nghĩa                                                                 | Được chuyển sang khi |
|-------------|--------------------------------------------------------------------------|----------------------|
| **PLANNED** | Workflow đã được tạo, chưa bắt đầu thực thi                              | Tạo mới              |
| **RUNNING** | Đang thực thi từng action theo thứ tự                                    | Bắt đầu execute      |
| **VERIFYING** | Đã chạy hết actions (hoặc dừng sớm), đang kiểm tra post-condition      | Hết actions / cần verify |
| **PASS**    | Verification thành công, post-condition thỏa mãn                         | Tất cả checks pass   |
| **FAIL**    | Action thất bại không recover được, hoặc verification fail               | Action fail / check fail |
| **BLOCKED** | Không thể tiếp tục an toàn (thiếu quyền, môi trường, policy, timeout...) | Safety / external block |

---

## 3. Quy tắc chuyển trạng thái

1. Chỉ được chuyển theo mũi tên trong state machine.
2. **Cấm tuyệt đối**:
   - Từ RUNNING → PASS (bỏ qua VERIFYING)
   - Từ một action success → PASS
   - Tự set PASS khi chưa chạy verification block
3. Verification là bước bắt buộc trước khi kết luận PASS.
4. Nếu không có verification block → mặc định chuyển sang VERIFYING với check tối thiểu (observation tồn tại).

---

## 4. Workflow Schema

```json
{
  "task": "string",
  "actions": [
    {"type": "navigate", "value": "https://example.test"},
    {"type": "observe"},
    {"type": "click", "target": "New"},
    {"type": "click", "target": "Folder"},
    {"type": "type", "target": "input[name='name']", "value": "ABC"},
    {"type": "click", "target": "Create"}
  ],
  "verification": {
    "checks": [
      {"field": "text", "contains": "ABC"},
      {"field": "url", "contains": "/folder"}
    ]
  },
  "recovery": {
    "max_retries": 2,
    "on_fail": "abort"
  }
}
```

---

## 5. Verification Rules

- Verification chỉ chạy sau khi actions kết thúc (hoặc dừng có kiểm soát).
- Mỗi check phải có kết quả rõ ràng: pass / fail.
- Tất cả checks pass → PASS.
- Bất kỳ check nào fail → FAIL.
- Không thể chạy verification → BLOCKED.

---

## 6. Evidence Requirement

Khi kết thúc (PASS / FAIL / BLOCKED), runtime **phải** ghi evidence gồm:

- sequence of actions + results
- final observation
- verification results
- timestamp + work_id

Không có evidence đầy đủ → không được tuyên bố PASS.

---

## 7. Anti-Pattern (Cấm)

```text
❌ "Tôi đã click Create thành công → PASS"
❌ Bỏ qua VERIFYING
❌ Tự set PASS vì "nhìn thấy text ABC" mà không chạy check chính thức
❌ Retry vô hạn
```

---

## 8. Versioning

Contract này là **LOCKED**.  
Thay đổi state machine hoặc ý nghĩa PASS/FAIL/BLOCKED phải tạo version mới và cập nhật WORK_MANIFEST.
