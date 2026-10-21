# 03_ARCHITECTURE

Tài liệu kiến trúc và specification của Work 10 — COMPUTER-AGENT.

## Files

| File                              | Mô tả                                      | Status     |
|-----------------------------------|--------------------------------------------|------------|
| COMPUTER_AGENT_ARCHITECTURE.md    | Tổng quan kiến trúc                        | PASS       |
| ACTION_CONTRACT.md                | Contract action (click ≠ type, reject...)  | **LOCKED** |
| WORKFLOW_CONTRACT.md              | State machine PLANNED→...→PASS/FAIL/BLOCKED| **LOCKED** |
| SAFETY_POLICY.md                  | Retry, timeout, destructive, boundary      | **LOCKED** |
| P1_P5_IMPLEMENTATION.md           | Chi tiết implementation phases             | PASS       |

## Principle

- Specification được khóa trước khi chạy host E2E.
- Không ghi PASS cho phần chưa chạy thật trên host.
