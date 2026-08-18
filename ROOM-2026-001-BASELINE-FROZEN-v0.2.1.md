# ROOM HOP v0.2.1 — REGRESSION BASELINE: PASS / CLEAN / FROZEN

**Ngày:** 2026-08-16

## Kết quả xác minh

```
pytest -q
→ 104 passed, 0 failed, 0 collection error (không cần --ignore)

pytest --collect-only -q
→ 104 tests collected, tests/legacy/ không bị collect mặc định

pytest -q tests/legacy/test_authority_v1.py
→ 45 passed (evidence Governance V1, chạy độc lập)
```

## Đã khóa (không tự ý sửa từ đây)

- `core/discussion.py`
- `core/meeting_manager.py`
- `core/governance.py`
- `core/governance_v1_backup.py` (evidence)
- `pytest.ini`
- `tests/legacy/test_authority_v1.py` (evidence)

## Lifecycle được regression suite bảo vệ

```
DRAFT → OPEN → JOIN_ACCEPTED → ACTIVE → DISCUSSION → CLOSING → CLOSED → COMPLETED
```

## Lịch sử đến baseline này (tóm tắt, chi tiết xem 2 file thread trước)

1. `core/discussion.py` — thêm guard `status != "active"` + `len(participants) < 2` → loại bỏ `ZeroDivisionError`, fail closed đúng lifecycle.
2. `tests/test_discussion.py`, `tests/test_meeting.py` (+2 test case mới), `tests/test_e2e.py` — cập nhật contract test theo lifecycle `draft→open→join→active`, không sửa `meeting_manager.py`.
3. `tests/test_authority.py` (root, trùng lặp/hỏng) và `tests/legacy/test_authority_v2_old.py` (bản sao thừa) — **đã xoá**, đúng phạm vi xác nhận, không đụng `tests/legacy/test_authority_v1.py`.

## Quy tắc từ đây

Baseline này **frozen**. Mọi thay đổi tiếp theo là một **patch mới**, phải chạy lại `pytest -q` để xác nhận regression trước khi được chấp nhận.
