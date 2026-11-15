# WP0 — Vibe verification of runtime evidence handoff
Date: 2026-10-29 (UTC)
Verifier: Vibe (Work agent, GitHub side)
Handoff branch: work/28/wp0-evidence-handoff-20261029
Handoff commit: f0ff39cdaee56a3513b095b6651cba3aae79ef9e
Files verified:
- 06_EVIDENCE/WP0_MCP8030_tools_list_capture_20261029.txt
- 06_EVIDENCE/WP0_VIBE_HANDOFF_20261029.md

## 1. Hash and byte-count verification — MISMATCH (FAILS the handoff's own gate)

Declared in the handoff doc:
- SHA-256: 3B0F2B82230354729062493EADF6C5E8FDB110CE73E674AB7830440DDFA08299
- Size: 5025 bytes

Authoritative committed-file metadata (GitHub Contents API, branch work/28/wp0-evidence-handoff-20261029):
- Committed size: 5022 bytes
- Git blob SHA-1: 7c16429d1732ffa75cdb520c94113d198cbfc602

The declared size does not equal the committed size (5025 vs 5022, delta = 3 bytes).
Per the handoff's own rule ("Recompute the hash and byte count from this committed
file before relying on it"), the declared SHA-256/size CANNOT certify the committed
file. No tested normalization reproduces the declared hash (LF, CRLF, UTF-8 BOM,
trailing-newline variants all tried; none match).

Most probable cause (not proven): the hash was computed over a byte sequence that
differed from what was committed — a 3-byte delta consistent with a UTF-8 BOM or a
line-ending difference introduced between capture and commit.

Required remediation before this capture can serve as certified evidence:
re-capture or re-export the exact committed bytes, recompute SHA-256 and size from
the committed blob, and update the handoff doc. Until then the capture is
USABLE AS CONTEXT, NOT AS HASH-CERTIFIED EVIDENCE.

## 2. Tool name and schema comparison vs Registry V1 (unified_registry_v1.py)

Result: 16 of 17 runtime tools match the V1 registry line on name and required
arguments. All 17 runtime tools verified from the capture JSON.

- list_meetings, get_meeting, get_transcript, join_meeting, add_paste_to_meeting,
  start_meeting (meeting_id+starter), get_room_structure, get_room_context:
  name + required fields MATCH registry V1.
- sandbox_read / sandbox_create / sandbox_write / sandbox_append / sandbox_delete /
  sandbox_list / sandbox_list_works / sandbox_create_work: name + required fields
  MATCH registry V1 (work_id + relative_path argument style).
- sandbox_read_probe: NOT present in registry V1 nor catalog V54 (unchanged finding;
  governance decision still required).

Structural differences observed (consistent across all runtime schemas):
- Runtime schemas omit additionalProperties:false (both catalogs enforce it) ->
  the runtime accepts unknown argument keys that the contracts would reject.
- Runtime schemas use Pydantic v2 style ("title" on every schema, "anyOf" for
  nullable, explicit "default") — indicating a Pydantic-based server generator,
  not the hand-written _schema() helpers in this repo.

## 3. Handler trace

Unchanged from the prior trace: no source file in this repository (default branch
or work/28-mcp-tooling-platform) implements the deployed room-hop-build v1.28.1
service; room_hop_mcp/adapter/server.py publishes only 4 meeting tools (Public
Boundary V1). The deployed handler source therefore cannot be audited from this
repository — provenance gap stands.

## 4. CI note

Pushing to work/28/wp0-evidence-handoff-20261029 does NOT trigger the Work 28 CI
workflow (its push trigger is restricted to branch work/28-mcp-tooling-platform).
No CI claim is made or implied for this handoff branch.

## Verdict

- WP0 content conclusion (17 tools listed by runtime at capture time): SUPPORTED by
  the committed capture as context.
- WP0 evidence certification: FAIL — declared hash/size do not match the committed
  blob. Remediation required as in section 1.
- No claim of execution, authorization, OS isolation, integration, or release PASS.
- Work 28: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; execution gate CLOSED.
