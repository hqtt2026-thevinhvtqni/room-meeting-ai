# Work 28 — Full MCP Tool Scope (Planning Target: 54)
Date: 2026-10-21
Owner/coordinator: Xu
Status: DESIGN ONLY — not implementation evidence; no PASS implied.

## Goal
Define the intended scope for the Work 28 MCP-8020 Tooling Platform, including existing ROOM/meeting and sandbox capabilities plus Computer Agent and Browser Agent capabilities. Build and verify these tools in Work 28. Do not place Core :8000 inside Sandbox. Sandbox remains an isolated execution environment.

## Planned tool inventory

### A. ROOM / meeting / task tools (10)
1. `room_get_context`
2. `room_get_structure`
3. `room_list_meetings`
4. `room_get_meeting`
5. `room_get_transcript`
6. `room_start_meeting`
7. `room_join_meeting`
8. `room_append_meeting_message`
9. `room_get_pending_tasks`
10. `room_submit_proposal`

### B. Sandbox / file / execution / evidence tools (21)
11. `sandbox_list_works`
12. `sandbox_create_work`
13. `sandbox_list`
14. `sandbox_read`
15. `sandbox_write`
16. `sandbox_append`
17. `sandbox_delete`
18. `sandbox_search`
19. `sandbox_read_file_metadata`
20. `sandbox_create_directory`
21. `sandbox_copy_file`
22. `sandbox_move_file`
23. `sandbox_get_manifest`
24. `sandbox_validate_path`
25. `sandbox_run_python`
26. `sandbox_run_command`
27. `sandbox_get_execution_status`
28. `sandbox_get_execution_result`
29. `sandbox_collect_artifact`
30. `sandbox_generate_evidence`
31. `sandbox_create_handoff`

### C. Computer Agent tools (6)
32. `computer_screenshot`
33. `computer_click`
34. `computer_type`
35. `computer_keypress`
36. `computer_scroll`
37. `computer_get_screen_state`

### D. Browser Agent tools and OCR (13)
38. `browser_open`
39. `browser_get_text`
40. `browser_screenshot`
41. `browser_click`
42. `browser_fill`
43. `browser_find`
44. `browser_get_state`
45. `computer_find_text` (OCR / locate visible text)
46. `browser_wait`
47. `browser_press_key`
48. `browser_scroll`
49. `browser_back_forward`
50. `browser_get_tabs`

### E. Additional browser/computer support tools (4)
51. `browser_get_accessibility_tree`
52. `browser_upload_download`
53. `browser_drag_drop`
54. `browser_wait_for_change`

## Implementation and acceptance rules
- The count 54 is a planning target, not a claim that 54 tools exist or are registered.
- Every published tool must have an explicit input schema, output schema, handler binding, permission boundary, error contract, and tests; if not implemented, it must be explicitly marked not implemented and must not pretend to succeed.
- Test protocol: inspect `tools/list`, call each supported tool with safe fixtures, verify actual output and side effects, and retain evidence.
- Keep UI/computer and browser actions observable; destructive or external side-effect actions require explicit policy/confirmation.
- Validate all paths and enforce work-scoped access for Sandbox operations.
- Keep execution results and artifacts tied to a run ID and evidence record.
- Keep Core :8000 outside Sandbox. Do not create, install, or run Core inside Sandbox.
- No E2E PASS until live MCP → Core/runtime → tool handler → observable result is proven with evidence.
