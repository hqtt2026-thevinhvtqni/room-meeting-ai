# SECRETARY + LARGE FILE IMPORT: PASS

Ngày chốt: 2026-08-17

## Trạng thái

| Hạng mục | Trạng thái |
|---|---|
| `core/secretary.py` (Secretary v0.3) | 🟢 PASS — không sửa đổi |
| `core/importer.py` (component riêng, mới) | 🟢 PASS |
| File thật 525,263,027 bytes (~501 MB) — byte-identical | 🟢 PASS |
| File thật 525,263,027 bytes (~501 MB) — SHA-256 identical | 🟢 PASS |
| Restart → instance Secretary mới → read-back | 🟢 PASS |
| `tests/test_importer.py` | 🟢 9/9 PASS |
| Regression suite (phần liên quan Secretary/importer + repo, trừ governance) | 🟢 127/127 PASS |
| `tests/test_authority.py` (governance) | 🟡 BLOCKED/FAIL collection — issue độc lập, KHÔNG liên quan Secretary/importer |

## Evidence

### 1. File 500MB thật — hash gốc
```
SHA-256: ab7717fcef47f173bdcfe11db9f9d4dc5f9b96c7dcdaf667000d2ce95920a701
Size:    525,263,027 bytes
```

### 2. Import qua core/importer.py → Secretary.append()
```
import result: {'status': 'READY', 'chunks_written': 126}
elapsed (write via importer+Secretary): 6.58 s
```

### 3. So sánh input vs output
```
BYTE_SIZE: IDENTICAL (525263027)
SHA256: IDENTICAL
  input : ab7717fcef47f173bdcfe11db9f9d4dc5f9b96c7dcdaf667000d2ce95920a701
  output: ab7717fcef47f173bdcfe11db9f9d4dc5f9b96c7dcdaf667000d2ce95920a701
```

### 4. Restart / read-back (instance Secretary mới, mô phỏng process khác)
```
read() elapsed: 7.86 s
read() chars: 237,000,000
SHA256 of read()-then-reencoded text: ab7717fcef47f173bdcfe11db9f9d4dc5f9b96c7dcdaf667000d2ce95920a701
export() == read(): True
```

### 5. tests/test_importer.py
```
9 passed in 0.15s
```
Bao gồm:
- Chứng minh naive `bytes_chunk.decode("utf-8")` vỡ tại ranh giới multi-byte (UnicodeDecodeError tái hiện được).
- Incremental decoder tái tạo chính xác ở nhiều `chunk_size` (kể cả 1–7 byte, ép chia giữa ký tự multi-byte).
- Import roundtrip byte-identical + SHA-256 khớp.
- Số chunk >1 với file lớn.
- Restart → instance Secretary mới → read-back khớp.

### 6. Full regression (trừ test_authority.py)
```
127 passed in 0.90s
```

## Root cause đã sửa

Import file lớn bằng `raw_bytes[i:i+4MB].decode("utf-8")` trực tiếp trên từng
chunk byte cố định sẽ FAIL bất cứ khi nào ranh giới chunk (ranh giới *byte*)
rơi vào giữa một ký tự UTF-8 nhiều byte (dấu tiếng Việt, emoji...).

Fix: `core/importer.py` dùng `codecs.getincrementaldecoder("utf-8")`, tự
giữ phần byte dở dang ở cuối buffer nội bộ và ghép vào chunk kế tiếp trước
khi decode — không cần thay đổi `core/secretary.py`.

## Ghi chú phạm vi

- `core/secretary.py`: 0 dòng thay đổi. API vẫn đúng 3 method:
  `append() / read() / export()`.
- `core/importer.py`: component độc lập, gọi `Secretary.append()` như một
  caller bên ngoài — không import Meeting/Governance/Discussion/IntentRouter.
- `tests/test_authority.py` fail ở bước **collection** vì `core/governance.py`
  thiếu export `Action` — lỗi có sẵn trong archive, không liên quan đến
  Secretary hay importer, không bị đưa vào để hạ trạng thái PASS ở trên.
  → Mở task riêng cho governance, xử lý độc lập.
