# GO BUILD CHECKPOINT — Trust Boundary + Authorization + Resource Limits
**Go — Delivery Owner**  
**15/10/2026 06:28 UTC+07**

## CONTRACT_VERSION: 1.3.0

## A. Source changes made

### `04_CODE/tool_contracts.py` (1.2.1 → 1.3.0)

**Trust Boundary (data contracts only)**
- `TrustedPrincipal(principal_id, source)` — rejects source in {caller, client, user-supplied, identity_id}.
- `WorkContext(work_id, principal, allowed_operations)` — shape-level permits() only.
- Explicit documentation: these do **not** prove authenticity or authorization. Adapter/Core must derive principal from trusted transport and reject caller-supplied identity_id.

**Authorization surface (fail-closed)**
- `SandboxOperation` enum: LIST, READ, CREATE, WRITE, APPEND, DELETE.
- `AuthorizedSandboxRequest` — requires WorkContext + operation; fails closed if operation not in allowed_operations, path missing, content missing for write-like ops, or path fails lexical validation.

**Resource limits (byte-based)**
- `max_read_bytes` (default 1 MiB, hard 16 MiB)
- `max_list_entries` (default 1000, hard 10 000)
- `max_write_bytes` (default 1 MiB, hard 16 MiB)
- `max_append_bytes` (default 256 KiB, hard 4 MiB)
- Content size checked at construction time against the chosen limit.

**KA-AUDIT-28-07**
- test_summary keys must be strings.
- NaN / ±Infinity rejected in scalars.

### `05_TEST/test_tool_contracts.py`
New / expanded tests covering all of the above.

## B. Tests added (summary)
| Area | Tests |
|------|-------|
| Trust boundary | rejects caller source; accepts server source; bad principal_id |
| WorkContext | requires ops; permits() shape check |
| Authorization fail-closed | missing permission, missing path, missing content, traversal path |
| Resource limits | defaults, write overflow, append overflow, bounded_limit range |
| KA-AUDIT-28-07 | NaN, non-string keys |
| Prior regressions | preserved (to_dict, deep freeze, execution PASS gates, path security) |

## C. Tests actually executed
**0** — no approved runner available.  
No claim of PASS.

## D. Tests not executed and why
```bash
python -m unittest discover -s 05_TEST -t . -v
```
BLOCKED until approved runner exists.

## E. SHA-256
Platform hash facility not exposed via current connector.  
Ka can hash the two source files directly on the sandbox.  
Go does not invent hashes.

## F. Explicit non-claims
- TrustedPrincipal / WorkContext are **data contracts only**. They do not prove a principal is authentic or authorized.
- identity_id supplied by caller is never treated as authority.
- Lexical path validation ≠ filesystem containment (symlink/reparse still adapter responsibility).
- Contract tests ≠ live MCP endpoint authentication or authorization enforcement.
- No live E2E was run. No MCP :8020 process was modified or restarted.

## G. Remaining blockers
| Item | Status |
|------|--------|
| Approved runner + test execution log | BLOCKED |
| G0 full source/runtime binding + raw tools/list | PARTIAL / BLOCKED |
| Core-derived principal enforcement | BLOCKED (interface ready; runtime not) |
| OS isolation / N08 | BLOCKED |
| Live E2E (G5–G6) | BLOCKED |
| Cla security review of 1.3.0 | NOT STARTED |
| Release / python_run / registry | NO-GO |

## Guardrails respected
No python_run, no live registry, no PC/GitHub write, no sync/merge/release, no restart of MCP :8020, no PASS claim without runner log.

---
Go — Delivery Owner  
15/10/2026 06:28 UTC+07
