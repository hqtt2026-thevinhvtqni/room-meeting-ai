# WORK 10 — OFFLINE TEST MATRIX

**Status:** FULL COVER (Offline executable)
**Owner:** Work 10 — COMPUTER-AGENT
**Last update:** 2026-10-04 (evening hardening)

---

## 1. Mục tiêu

Những thứ **không cần Chromium / Playwright / real browser** vẫn phải test được đầy đủ.

Mục tiêu: khi anh Vinh vào PC chỉ việc chạy E2E thật, không phải quay lại thiết kế contract.

---

## 2. Offline Test Categories

### 2.1 Action Contract

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| Known action types accepted        | parse OK                                 | **PASS**    |
| Unknown action type                | REJECT (ActionValidationError)           | **PASS**    |
| click without target               | REJECT                                   | **PASS**    |
| type without value                 | REJECT                                   | **PASS**    |
| type without target                | REJECT                                   | **PASS**    |
| navigate without value             | REJECT                                   | **PASS**    |
| Result schema validation           | luôn có action, ok, observation, status  | **PASS**    |

### 2.2 Click / Type Separation

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| Explicit click action              | semantic = click                         | **PASS**    |
| Explicit type action               | semantic = type                          | **PASS**    |
| type cannot fake click             | type vẫn giữ semantic type               | **PASS**    |
| Mixed sequence click → type        | giữ đúng thứ tự semantic                 | **PASS**    |

### 2.3 Workflow State Machine

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| PLANNED → RUNNING                  | allowed                                  | **PASS**    |
| RUNNING → VERIFYING                | allowed                                  | **PASS**    |
| VERIFYING → PASS                   | chỉ khi tất cả checks pass               | **PASS**    |
| VERIFYING → FAIL                   | khi check fail                           | **PASS**    |
| RUNNING → PASS (skip VERIFYING)    | **FORBIDDEN**                            | **PASS**    |
| Action success → auto PASS         | **FORBIDDEN**                            | **PASS**    |
| BLOCKED on unknown action          | chuyển đúng sang BLOCKED                 | **PASS**    |

### 2.4 Verification Logic

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| All checks pass                    | PASS                                     | **PASS**    |
| One check fails                    | FAIL                                     | **PASS**    |
| Missing verification block         | vẫn PASS nếu có evidence                 | **PASS**    |
| Verification result in evidence    | có entry verification: PASS/FAIL         | **PASS**    |

### 2.5 Evidence Completeness

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| Evidence có đủ actions + results   | required                                 | **PASS**    |
| Evidence có observation            | required                                 | **PASS**    |
| Evidence có verification results   | required khi có verification             | **PASS**    |
| Thiếu evidence mà claim PASS       | **FORBIDDEN**                            | **PASS**    |

### 2.6 API Validation

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| Invalid payload / unknown type     | ActionValidationError                    | **PASS**    |
| Missing required fields            | reject                                   | **PASS**    |
| Valid minimal workflow             | accepted                                 | **PASS**    |

### 2.7 Failure Handling

| Test Case                          | Expected Result                          | Status      |
|------------------------------------|------------------------------------------|-------------|
| Action fail + no recovery          | Workflow → FAIL                          | **PASS**    |
| Adapter exception                  | FAIL + error message preserved           | **PASS**    |
| Unknown action                     | BLOCKED                                  | **PASS**    |

---

## 3. Cách chạy Offline

```bash
cd COMPUTER-AGENT/05_TEST
python test_p0_p5.py
```

Chạy được trên môi trường **không có Chromium**.

---

## 4. Những gì **KHÔNG** thuộc Offline

- Chromium launch
- Real navigate / observe / click / type / scroll
- Real screenshot / download
- Full E2E workflow
- Release smoke

→ Vẫn giữ **READY / HOST RUN REQUIRED**. Không ghi PASS.

---

## 5. Definition of Done (Offline) — ĐÃ ĐẠT

- [x] Tất cả test case trong bảng trên đều có test code
- [x] Chạy được trên môi trường không có Chromium
- [x] Contract được enforce trong code (models.py + agent_runtime.py), không chỉ nằm trong tài liệu
- [x] State machine có state_trace kiểm chứng được
