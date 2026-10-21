# Work AI Dashboard — Template

> Sao chép mẫu này cho từng Work. Đây là bản ghi cấu hình/khung hiển thị, không phải bằng chứng dashboard đã chạy.

## Work Header
- Work ID:
- Work Name:
- Owner / Approver:
- Objective:
- Scope:
- Repository / Branch:
- Manifest revision:
- Current status:
- Data source status: GitHub / Sandbox / MCP
- Sync status: SYNCED / DRIFT / CONFLICT / SOURCE_UNAVAILABLE / UNKNOWN
- Last verified at:

## Executive Summary
| Metric | Value | Evidence / Formula |
|---|---|---|
| Deliverables total | UNKNOWN | Chưa nạp manifest |
| DONE | UNKNOWN | |
| PASS | UNKNOWN | |
| BLOCKED | UNKNOWN | |
| UNVERIFIED | UNKNOWN | |
| Milestones | UNKNOWN | |
| Open high risks | UNKNOWN | |

## AI Role Board
| Role ID | Vai trò | AI ID / Provider | Task(s) | Deliverable(s) | Reviewer | Status | Blocker / Dependency | Evidence | Revision |
|---|---|---|---|---|---|---|---|---|---|
| ROLE-ARCH | Kiến trúc | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-FE | Frontend | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-BE | Backend | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-QA | QA/QE | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-DEVOPS | DevOps/SRE | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-SECURITY | Bảo mật | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |
| ROLE-AUDIT | Kiểm toán độc lập | NOT_ASSIGNED | | | | NOT_ASSIGNED | | | |

> Bổ sung/bỏ các vai trò theo phạm vi. Vai trò không áp dụng phải ghi NOT_APPLICABLE và lý do. Không giả định AI đã được phân công.

## Work Pipeline
| Phase | Status | Entry criteria | Exit criteria | Evidence | Blocker |
|---|---|---|---|---|---|
| INTAKE | UNKNOWN | | | | |
| PLAN | UNKNOWN | | | | |
| ARCHITECTURE | UNKNOWN | | | | |
| BUILD | UNKNOWN | | | | |
| TEST | UNKNOWN | | | | |
| SECURITY/COMPLIANCE | UNKNOWN | | | | |
| RELEASE | UNKNOWN | | | | |
| HANDOFF | UNKNOWN | | | | |

## Evidence & Decisions
| ID | Kind | Summary | Source/revision | Created by/time | Reviewer | Verification |
|---|---|---|---|---|---|---|

## Sync Health
| Source | Reachability | Revision/hash | Last checked | Diff/conflicts |
|---|---|---|---|---|
| GitHub | UNKNOWN | | | |
| Sandbox | UNKNOWN | | | |
| MCP | UNKNOWN | | | |

## Rules
- Dashboard default is read-only.
- DONE is not PASS.
- No evidence means UNVERIFIED, not PASS.
- No baseline/formula means progress percentage is UNKNOWN.
- MCP failure does not block independent GitHub work.
- Never overwrite divergent sources without comparing revisions and resolving conflicts.
- Log every change with AI/person, role, date/time, Work/task, revision, reviewer and evidence.
