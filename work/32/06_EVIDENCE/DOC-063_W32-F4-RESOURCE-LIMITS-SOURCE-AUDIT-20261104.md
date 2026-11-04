# DOC-063 — F4 RESOURCE LIMITS SOURCE AUDIT AND IMPLEMENTATION DISPOSITION

- **Document Number:** DOC-063
- **Priority order:** P0 — Close resource-boundary gaps without inventing rate policy or changing Core authority
- **Work:** 32 — CI-CD-ROOM-HOP-PYTHON-NO-DOCKER
- **Date-Time:** 2026-11-04 14:02 Asia/Ho_Chi_Minh
- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Branch:** work/32-ci-cd-python-ci-v2
- **Audited exact commit:** 450c0b2409c0d19c68931cb0331652bac6f3b5df

## 1. Files read from the exact audited commit

| Path | Blob SHA | Finding |
|---|---|---|
| `core/secretary.py` | `b6bba7b7db0b76ad55e3cd9e15638827a4fc0944` | Enforces 1 MiB UTF-8 byte ceiling before opening/writing transcript; declares `MAX_PASTE_REQUESTS_PER_WINDOW = 100` but does not consume/enforce it |
| `core/meeting_service.py` | `0b80a81663c1be328c41878a6762d16d95378aab` | `add_paste` delegates to Meeting; no independent policy layer |
| `core/meeting_manager.py` | `d4d7b28f0f0df9208648d0870c42cb6e451eda50` | Meeting.add_paste delegates to Secretary.append before logging; oversized text raises before transcript write |
| `room_hop_mcp/adapter/server.py` | `fbd68be57ef5f904728d89baaab6292a5dcf164c` | Public MCP `text` schema has type=string only; no maxLength |
| `tests/test_f4_resource_limits.py` | `f4808b3307dfb3bd4a1a29ad183d9f5af699df3b` | Design/baseline tests; file explicitly says some failures are expected before F4 implementation |

## 2. Evidence-based disposition

### F4.1 — Secretary UTF-8 input byte ceiling
**SOURCE PRESENT.** The current implementation computes `len(text.encode("utf-8"))`, rejects values greater than 1 MiB before opening the transcript file, and therefore prevents partial transcript writes for this boundary. This is source evidence only; the F4 dedicated test file is not yet executed in GitHub CI.

### F4.2 — MeetingService / Core public boundary
**DELEGATION PRESENT; DEDICATED TEST NOT RUN.** MeetingService delegates to Meeting.add_paste; Meeting.add_paste calls Secretary.append before writing the logical paste message and event. The byte guard is therefore reached before transcript mutation. No independent service-level byte limit exists or is needed unless the architecture explicitly requires duplicated enforcement.

### F4.3 — MCP public schema
**GAP CONFIRMED.** The `add_paste_to_meeting` text property is declared as a string without `maxLength`. F4 tests ask for `maxLength=1,048,576`. JSON Schema maxLength counts Unicode characters, not UTF-8 bytes; therefore adding this property alone would not implement the byte policy for multi-byte text. Runtime byte enforcement remains necessary. A schema declaration is useful early rejection, but must not be represented as equivalent to byte enforcement.

### F4.4 — Repeated-request / rate policy
**PARTIAL DECLARATION; NO ENFORCEMENT EVIDENCE.** `MAX_PASTE_REQUESTS_PER_WINDOW=100` is declared in `core.secretary`, so the current test's introspection check can find a policy-like constant. The audited implementation contains no counter, time window, identity/meeting scoping, concurrency control, or rejection path using that constant. The constant alone is not a functioning rate limiter.

The test file does not specify the window duration, whether the quota is per caller/identity/meeting/process, what response is returned on limit, whether failed attempts count, or how state survives restarts/multiple workers. Ka will not invent these semantics or add an in-memory counter that could misrepresent enforcement in a multi-process deployment.

## 3. Required next actions

1. Keep F4 tests out of the mandatory green CI gate until the F4 contract is approved and all dedicated tests pass; do not delete, skip, weaken, or relabel them.
2. Request an explicit F4 policy decision through the existing architecture governance: rate window, scope key, limit, rejection contract, concurrency/process model, persistence requirement, and observability/audit.
3. Once policy is approved, implement schema early-boundary maxLength plus runtime UTF-8 byte enforcement (already present in Secretary), and implement rate limiting at the correct authority boundary rather than in a disconnected helper.
4. Run `tests/test_f4_resource_limits.py` and all regression suites on exact SHA; retain logs and artifacts. Promote to CI only after a fully green result and review.
5. Browser Adapter E2E remains separately deferred until same-host PC execution is available; it is not coupled to F4.

## BIÊN BẢN

- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 14:02 Asia/Ho_Chi_Minh
- **Record:** Read exact commit tree and the five source/test files listed above. Compared the implementation to the dedicated F4 test contract. No source changes made because rate semantics are not specified and the current authority record does not approve a new Core policy.

## NHẬT KÝ

- **Name:** Ka
- **Title:** CSA / Work 32 execution owner
- **Date-Time:** 2026-11-04 14:02 Asia/Ho_Chi_Minh
- **Priority:** P0
- **Action:** Audited F4 source and tests; distinguished existing 1 MiB UTF-8 runtime enforcement from missing MCP schema maxLength and missing rate-limit behavior.
- **Result:** F4.1 source present; F4.2 delegated path present; F4.3 schema gap; F4.4 constant exists but enforcement absent. Dedicated F4 test file remains NOT RUN BY CI. No false PASS assigned.
- **Boundary:** No Core code, MCP schema, CI gate, strict coverage, merge, CD or deployment changes. No policy inferred.
- **Disposition:** F4 = BLOCKED pending explicit policy decision and implementation; Browser Adapter E2E = DEFERRED — WAITING FOR PC ACCESS; Work 32 = ACTIVE — NOT RELEASED.
