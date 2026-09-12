# ROOM HOP — Core Lifecycle HTTP Contract v0.1

Status: LOCKED (pending Xu/Mê final sign-off on implementation diff)
Repo: `D:\ROOM-HOP-CLEAN\room-meeting-ai`

## 1. Authority boundaries

- **Core (`:8000`) is the sole authority for meeting identity and
  lifecycle.** No other component (Bridge, Dashboard, Workspace) may
  decide or persist a meeting's `status`.
- **App Workspace (`:8010`) is the sole authority for working-state**
  (notes, participants shown in UI, minutes, actions, meta title/date).
  It references `core_meeting_id` but never validates it against Core.
- **HTTP adapter (`room_hop_mcp/adapter/http_server.py`) contains no
  business logic.** It validates request shape, calls `MeetingService`,
  maps the response. It never calls `MeetingManager` directly and never
  touches the filesystem, except for the read-only `/identities` route
  (see §5).

## 2. Meeting lifecycle — one-directional state machine

```
draft → open → active → closing → closed → completed
```

- No transition exists from `closed` back to `open`. This was verified
  directly in `Meeting._transition()` / `open_session()` (hard-checks
  `expected == "draft"`).
- **`closed` is immutable by design.** "Reopen" is NOT a Core concept.
  If a UI later needs a "reopen" affordance, it must be implemented as
  **creating a new meeting**, optionally copying content from the old
  Workspace snapshot for reference. This is a locked architectural
  decision, not an implementation gap.
- `close_meeting()` auto-calls `request_close()` internally when status
  is `active`, so there is no separate `/request-close` HTTP route.

## 3. Meeting ID allocation

- Format: `MEETING-{YYYY}-{seq:03d}` (UTC year).
- **Core allocates the ID, not the client.** `POST /meetings` accepts
  an optional `meeting_id`; if omitted, `MeetingManager._allocate_meeting_id()`
  computes `max(existing_seq_for_year) + 1`.
- Explicitly **not claimed atomic**. No lock/transaction exists. Policy
  is **race-tolerant / collision-detected**: if two allocations collide,
  the second `create_meeting()` call fails at `meeting_dir.mkdir()` with
  a clear `MeetingError` (mapped to HTTP 400). No silent overwrite, no
  retry logic in v0.1.
- Backward compatible: `meeting_id` stays a **required, first
  positional parameter** on `MeetingManager.create_meeting()` /
  `MeetingService.create_meeting()` — it is typed `str | None` but has
  **no default value**. Callers that already pass an explicit string
  positionally (confirmed evidence: `tests/test_meeting_lifecycle_v021.py`)
  keep working with zero changes. The HTTP layer (the only new caller)
  passes `meeting_id=None` explicitly by keyword to trigger the
  allocator. An earlier draft of this patch made the parameter
  keyword-only with a default — that broke the positional caller above
  and was reverted after `pytest` full-suite evidence caught it.

## 4. `created_by`

- Explicit only. The client (Main Dashboard) must obtain "who am I"
  from the user (identity picker, once per session) and send it as
  `created_by`. It is never inferred from `participants[0]`.
- Used downstream by `close_meeting(closer=...)` for `GOV.check()` /
  `GOV.audit()` — this is a governance-relevant field, not cosmetic.

## 5. Identity discovery — `GET /identities`

Read-only. Does not go through `MeetingService`; reads
`PrincipalRegistry` and `AgentRegistry` directly, since Identity Layer
is architecturally separate from Meeting lifecycle. Never mutates
either registry.

```json
{
  "principals": [
    { "id": "vinh", "name": "Vinh", "type": "human_principal" }
  ],
  "agents": [
    { "id": "xu", "name": "Xu", "role": "...", "type": "ai_agent" }
  ]
}
```

- `human_principal` (PrincipalRegistry) and `ai_agent` (AgentRegistry)
  are separate identity types by design (`PrincipalRegistry.from_dict`
  rejects any `type != "human_principal"`). They are **not** merged
  into one registry. The UI may present them in one combined picker,
  but must keep the `type` tag from the source.
- Core meeting participants (`join_meeting`) MUST be an `identity_id`
  from one of these two registries. Free-text is rejected implicitly
  by `resolve_identity()` failing inside `join_meeting`.
- **Workspace participants remain free-text** — unrelated concept, not
  validated against any registry. This boundary is unchanged.

## 6. `context_files`

- v0.1: always `[]`. No upload UI. `package_context([], ...)` is
  confirmed to no-op safely on an empty list.

## 7. Action item canonical format (for `close_meeting`)

Workspace action objects (`{id, text, assignee, deadline, done}`) are
flattened to strings before being sent to Core, since `close_meeting`
accepts `action_items: list[str]`:

```
{text} — phụ trách: {assignee} — hạn: {deadline} — trạng thái: {DONE|OPEN}
```

`assignee`/`deadline` keep Workspace's existing placeholders
(`"Chưa gán"` / `"Chưa đặt"`) when absent. This mapping happens in the
Bridge, not in Core or Workspace.

## 8. Endpoints

| Method | Path | Maps to | Notes |
|---|---|---|---|
| GET | `/identities` | `PrincipalRegistry` + `AgentRegistry` | read-only, new |
| GET | `/meetings?status=` | `service.list_meetings(status=)` | **status filter is NEW** — the pre-patch route ignored query params entirely even though `MeetingManager.list_meetings` already supported it |
| GET | `/meetings/{id}` | `service.get_meeting` | unchanged |
| GET | `/meetings/{id}/transcript` | `service.get_transcript` | unchanged |
| POST | `/meetings/{id}/paste` | `service.add_paste` | unchanged |
| POST | `/meetings` | `service.create_meeting` | `meeting_id` now optional |
| POST | `/meetings/{id}/open` | `service.open_meeting` | new, `draft → open` |
| POST | `/meetings/{id}/join` | `service.join_meeting` | new, call once per participant |
| POST | `/meetings/{id}/start` | `service.start_meeting` | new, `open → active`, needs ≥2 joined |
| POST | `/meetings/{id}/close` | `service.close_meeting` | new, `active/closing → closed` |

All new lifecycle routes surface `MeetingError` as **HTTP 400** with the
original message in `detail` (new global exception handler — see
implementation notes).

## 9. Known inconsistency — not fixed in this patch, flagged for Xu/Mê

`create_meeting` / `open_meeting` / `join_meeting` / `start_meeting` in
`MeetingService` all return `self._snapshot(meeting)` = raw
`dict(meeting.data)` (includes `join_records`, `governance`,
`permissions`, everything). `get_meeting` / `list_meetings` instead use
the filtered `_public_meeting` / `_public_meeting_list_item` DTOs. This
means the lifecycle write endpoints currently leak more internal data
than the read endpoints. Pre-existing in the codebase, out of scope for
this patch (mục VIII: không refactor ngoài scope). Recommend a
follow-up ticket to normalize all responses through `_public_meeting`.

## 10. Orchestration lives in the Bridge, not the UI

`Bridge.createSession(topic, participantIds)` and
`Bridge.closeSession(id)` are Application Service boundaries. The
Dashboard UI never calls the 4-step create sequence
(`create → open → join×N → start`) directly — it calls one Bridge
method. This is a **frontend** change, out of scope for this Core
patch; documented here so the contract stays the single source of
truth for both sides.