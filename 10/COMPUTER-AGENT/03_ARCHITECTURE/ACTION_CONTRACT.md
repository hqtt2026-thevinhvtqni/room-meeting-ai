# WORK 10 — ACTION CONTRACT

**Status:** LOCKED (Specification)
**Owner:** Work 10 — COMPUTER-AGENT
**Last update:** 2026-10-04

---

## 1. Purpose

Action Contract là biên giới ổn định giữa AI Planner và Computer Agent Runtime.

Mọi action phải tuân thủ contract này. Runtime **không được** suy diễn, thay thế, hoặc “thông minh hóa” ý nghĩa action.

---

## 2. Core Rules (Bắt buộc)

1. **Một action = một semantic intent duy nhất.**
2. **click ≠ type.**  
   - `click` thực hiện thao tác click UI.  
   - `type` chỉ nhập text vào target.  
   - Tuyệt đối không được encode click bằng cách type tên button.
3. **Unknown action type → REJECT ngay lập tức.**
4. Mọi action phải trả về **observable result** (success / fail + observation).
5. Runtime failure dừng sequence hiện tại, trừ khi workflow khai báo recovery step có giới hạn.
6. **PASS chỉ được ghi sau khi verification post-condition thành công.**
7. Target phải đủ rõ để resolve deterministic (selector, role, text, coordinates có kiểm soát).

---

## 3. Canonical Action Types

| Action       | Semantic Intent                          | Required Fields          | Forbidden Interpretation          |
|--------------|------------------------------------------|--------------------------|-----------------------------------|
| `observe`    | Chụp + phân tích trạng thái hiện tại     | —                        | Không thực hiện side-effect       |
| `navigate`   | Chuyển đến URL                           | `value` (url)            | Không click link thay vì navigate |
| `click`      | Click vào target                         | `target`                 | Không type text thay vì click     |
| `type`       | Nhập text vào target                     | `target`, `value`        | Không click button bằng type      |
| `key_press`  | Nhấn phím / tổ hợp phím                  | `value` (key)            | —                                 |
| `scroll`     | Cuộn trang / element                     | `target?`, `value?`      | —                                 |
| `wait`       | Chờ điều kiện hoặc thời gian             | `value` (ms hoặc condition) | —                              |
| `extract`    | Trích xuất dữ liệu theo schema           | `target?`, `schema?`     | Chỉ trong boundary của Work       |
| `screenshot` | Chụp màn hình / element                  | `target?`                | Chỉ trong boundary của Work       |
| `download`   | Tải file                                 | `target?`, `value?`      | Phải có policy riêng nếu destructive |
| `close`      | Đóng session / tab                       | —                        | —                                 |

---

## 4. Click vs Type — Khóa cứng

```json
// ĐÚNG
{"type": "click", "target": "button:has-text('Create')"}
{"type": "type", "target": "input[name='name']", "value": "ABC"}

// SAI — Runtime phải REJECT
{"type": "type", "target": "Create"}          // không được hiểu là click
{"type": "click", "value": "ABC"}             // thiếu target hợp lệ
{"type": "unknown_action", ...}               // unknown → reject
```

---

## 5. Result Contract

Mọi action trả về:

```json
{
  "action_id": "uuid",
  "type": "click",
  "status": "success" | "fail" | "blocked",
  "observation": { ... },
  "error": null | "string",
  "timestamp": "ISO8601"
}
```

- `status = success` chỉ nghĩa là action đã thực thi, **không** nghĩa là task PASS.
- Task PASS chỉ được set ở tầng Workflow Verification.

---

## 6. Rejection Rules

Runtime **phải reject** khi:

- `type` không thuộc Canonical Action Types
- thiếu field bắt buộc
- target không resolve được (và không có fallback được phép)
- action nằm ngoài Safety Policy

---

## 7. Versioning

Contract này là **LOCKED** cho phase hiện tại.  
Mọi thay đổi semantic phải tạo version mới và cập nhật WORK_MANIFEST.
