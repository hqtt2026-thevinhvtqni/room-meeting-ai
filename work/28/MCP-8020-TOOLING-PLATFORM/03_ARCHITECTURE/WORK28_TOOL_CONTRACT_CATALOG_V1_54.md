# Work 28 — Tool Contract Catalog v1 (54-tool planning set)
Date: 2026-10-21
Status: DESIGN / CONTRACT DRAFT. This file defines a common contract envelope and per-tool intent; it does not claim handlers are implemented.

## Common contract envelope
All tools should expose:
- `name`: stable MCP tool name.
- `description`: specific action and limits.
- `inputSchema`: JSON Schema; reject unknown/invalid fields where feasible.
- Output: structured result with `ok`, `data` (when successful), and `error` (stable code/message when failed); include `run_id` for executions.
- No fabricated success. Unsupported actions return a clear `NOT_IMPLEMENTED` / capability status.
- Enforce caller/work scope, path validation, least privilege, timeout/resource limits, and audit evidence.
- Do not expose secrets or unrestricted host access. Core :8000 must not be deployed inside Sandbox.

## ROOM / meeting / task group
| Tool | Input intent | Output intent |
|---|---|---|
| room_get_context | Optional meeting/work context selector | Current authorized ROOM context |
| room_get_structure | Optional scope | ROOM hierarchy/structure |
| room_list_meetings | Filters and pagination | Meeting summaries |
| room_get_meeting | Meeting ID | One meeting record |
| room_get_transcript | Meeting ID and optional range | Transcript segments |
| room_start_meeting | Title, participants, optional metadata | Created meeting record or policy error |
| room_join_meeting | Meeting ID, participant identity | Join result/state |
| room_append_meeting_message | Meeting ID, content, speaker metadata | Appended message receipt |
| room_get_pending_tasks | Optional owner/status filters | Pending task list |
| room_submit_proposal | Proposal content, scope, evidence refs | Proposal receipt/status |

## Sandbox / file / execution / evidence group
| Tool | Input intent | Output intent |
|---|---|---|
| sandbox_list_works | Optional filter/pagination | Accessible Work IDs |
| sandbox_create_work | Work ID/title and authorized metadata | Creation receipt |
| sandbox_list | Work ID, relative path | Entries within authorized Work |
| sandbox_read | Work ID, relative path, optional bounded range | Text content or typed read error |
| sandbox_write | Work ID, relative path, content, overwrite policy | Write receipt and content hash |
| sandbox_append | Work ID, relative path, content | Append receipt and content hash |
| sandbox_delete | Work ID, relative path, explicit policy guard | Deletion receipt or refusal |
| sandbox_search | Work ID, query, optional path/globs | Matching paths/snippets |
| sandbox_read_file_metadata | Work ID, relative path | Size/type/hash/timestamps when available |
| sandbox_create_directory | Work ID, relative path | Directory receipt |
| sandbox_copy_file | Work ID, source and destination paths | Copy receipt |
| sandbox_move_file | Work ID, source and destination paths | Move receipt |
| sandbox_get_manifest | Work ID, optional path | Work manifest with provenance |
| sandbox_validate_path | Work ID, relative path, operation | Normalized path and allow/deny result |
| sandbox_run_python | Work ID, script/entrypoint, bounded args/resources | Run ID, exit status, stdout/stderr refs |
| sandbox_run_command | Work ID, allowlisted command/args, timeout | Run ID and process result; deny arbitrary unsafe commands |
| sandbox_get_execution_status | Run ID | Current execution state |
| sandbox_get_execution_result | Run ID | Exit status and captured output refs |
| sandbox_collect_artifact | Run ID, artifact path | Artifact metadata/hash |
| sandbox_generate_evidence | Run ID, evidence type and refs | Evidence record ID |
| sandbox_create_handoff | Work ID, status, evidence refs, next action | Handoff record |

## Computer Agent group
| Tool | Input intent | Output intent |
|---|---|---|
| computer_screenshot | Display/region selector | Screenshot artifact/reference |
| computer_click | Coordinates/target and safety options | Action result and observed state |
| computer_type | Text and target/focus policy | Action result; sensitive input guarded |
| computer_keypress | Key/chord allowlist | Action result |
| computer_scroll | Direction/distance/target | Action result and observed state |
| computer_get_screen_state | Optional capture/OCR settings | Screen state, capture timestamp, artifact refs |

## Browser Agent and OCR group
| Tool | Input intent | Output intent |
|---|---|---|
| browser_open | URL, navigation policy | Current URL/title/navigation result |
| browser_get_text | Selector or page scope | Visible text and source metadata |
| browser_screenshot | Page/viewport selector | Screenshot artifact/reference |
| browser_click | Locator/selector and timeout | Action result and post-action state |
| browser_fill | Locator/selector and value | Fill result; secrets guarded |
| browser_find | Text/selector query | Matches and locations |
| browser_get_state | Current tab/page selector | URL/title/loading state |
| computer_find_text | Text/OCR query and screen region | Text matches with coordinates/confidence |
| browser_wait | Condition and bounded timeout | Condition result; timeout is explicit |
| browser_press_key | Key/chord and target | Action result |
| browser_scroll | Direction/distance/target | Action result and observed state |
| browser_back_forward | Direction and bounded step count | Navigation result |
| browser_get_tabs | Optional active-tab details | Tab IDs, titles, URLs, active state |

## Additional browser/computer support group
| Tool | Input intent | Output intent |
|---|---|---|
| browser_get_accessibility_tree | Page/region scope | Accessibility tree or bounded subset |
| browser_upload_download | Transfer direction, file reference, target and policy | Transfer status and artifact metadata; enforce allowlist |
| browser_drag_drop | Source and target locators/coordinates | Action result and observed state |
| browser_wait_for_change | Baseline state and bounded timeout | Change detected / timeout with before-after evidence |

## Required test layers
1. Schema validation and invalid-input tests for all tools.
2. Handler-binding test: each published tool maps to the intended handler or explicitly reports not implemented.
3. Permission/path-boundary and negative tests.
4. Deterministic unit tests with safe fixtures.
5. Live MCP `tools/list` and `tools/call` smoke tests, preserving actual response evidence.
6. End-to-end proof for real runtime actions before any PASS claim.
