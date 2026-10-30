# CORE CAPABILITY GAP ASSESSMENT — WORK 70

Date: 2026-10-30
Status: READ-ONLY SOURCE REVIEW — WORK LIFECYCLE INTEGRATION NOT VERIFIED

## 1. Review scope
Reviewed the repository's current Core meeting lifecycle contract and implementation to determine whether Work 70 can reuse existing artifact/storage APIs without inventing a new contract.

Sources reviewed:
- `core/meeting_manager.py` at repository commit `fc6a19888765d174aea9aea839620338ac9f71e8`.
- `API_CONTRACT.md` at repository commit `fc6a19888765d174aea9aea839620338ac9f71e8`.
- `room_hop_mcp/adapter/http_server.py` at blob `54cb3ecbce2e6b13083f31c14f0c1f0738f1457d`.
- `core/meeting_service.py` at blob `0b80a81663c1be328c41878a6762d16d95378aab`.
- GitHub repository search for `product-status`, `/api/v1/works`, `work registry`, `evidence registry` and `storage artifact`.

## 2. Observed existing capability
The inspected Core code is Meeting-centric:
- `Meeting.save_artifact(artifact_name="final.md")` is permitted only after a Meeting reaches `closed`.
- It copies a file from that Meeting directory into that Meeting's `artifacts/` directory.
- It then changes the Meeting state to `completed` and records a `SAVE_ARTIFACT` event.
- The HTTP router registers `/identities` and Meeting routes only: `/meetings`, `/meetings/{id}`, `/meetings/{id}/transcript`, `/meetings/{id}/paste`, `/meetings/{id}/open`, `/meetings/{id}/join`, `/meetings/{id}/start`, and `/meetings/{id}/close`. `MeetingService.save_artifact()` exists as a MeetingService method, but the reviewed HTTP router does not expose a generic Work upload/export route.

This is useful evidence that ROOM-HOP has a Meeting-specific artifact operation and audit event. It is NOT a generic Work evidence registry, Work file store, Work versioning service, or export service.

## 3. Work 70 capability findings
| Capability | Finding | State |
|---|---|---|
| Work registry / Work identity API | No Work-specific route found in reviewed API contract | NOT VERIFIED |
| Work lifecycle/status read API | No `product-status` or `/api/v1/works` route found in reviewed search/contract | NOT VERIFIED |
| Work Package registry | No Work-scoped WP API found in reviewed contract | NOT VERIFIED |
| Work evidence metadata registry | No generic Work evidence API found in reviewed contract | NOT VERIFIED |
| Generic artifact upload/versioning | Meeting-only save_artifact is insufficient for Work evidence | NOT VERIFIED |
| Work JSON/CSV/Markdown export | No Work export API found in reviewed contract | NOT VERIFIED |
| Work-scoped authorization | Must be discovered from actual Core auth model; no Work policy evidence reviewed | NOT VERIFIED |

A repository search returning no result is not proof that no implementation exists anywhere. It means Work 70 cannot claim these capabilities until the actual Core routes/services and tests are located and inspected.

## 4. Architecture decision
Do not repurpose Meeting.save_artifact as Work storage. Do not add a parallel database or direct Dashboard-to-filesystem write path. Keep the Work 70 interfaces as proposed contracts only until Core ownership, storage provider, permissions, retention and audit requirements are resolved against the actual Core implementation.

## 5. Required next investigation
1. Inspect the actual HTTP router and service registration in the current default branch.
2. Identify Core's authoritative identity/authorization interfaces.
3. Confirm whether an existing generic file/evidence service exists outside MeetingManager.
4. If absent, prepare a Core-owned Work Registry/Evidence Registry/Export Service proposal; no implementation before the Core owner approves the boundary.
5. Verify routes and behavior with integration tests and audit evidence.

## 6. Decision
WP-70-04 remains BLOCKED / NOT VERIFIED. WP-70-05 storage/export remains DESIGN ONLY. Dashboard source remains local_snapshot. No Core live, persistent Work storage or file export claim is authorized.
