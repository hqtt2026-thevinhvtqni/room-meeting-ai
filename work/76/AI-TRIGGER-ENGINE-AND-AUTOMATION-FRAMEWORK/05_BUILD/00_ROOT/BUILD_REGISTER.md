# WORK 76 — BUILD REGISTER / SỔ ĐĂNG KÝ THI CÔNG

| WP | Package | Owner | Reviewer | Status | Canonical evidence |
|---|---|---|---|---|---|
| WP-76-01 | Trigger Registry and schema | Co / AI-07 | Ka / AI-02 (independent QE pending) | IN_REVIEW — PR #60 draft; branch CI PASS | `05_BUILD/04_CODE/trigger_engine/{models,registry}.py`; `05_BUILD/05_TEST/test_trigger_engine.py` |
| WP-76-02 | Event Gateway and source validation | Co / AI-07 | Qw (ACK/entry pending) | IN_REVIEW — PR #60 draft; typed malformed event validation, strict canonical payload digest, validate-before-replay reservation and fail-closed replay-store errors added; production verifier/key provider pending; exact-head CI run 44192558442 PASS 58/58 on Python 3.11/3.12 | `trigger_engine/gateway.py`; `test_work_packages.py` |
| WP-76-03 | Scheduler and TIME triggers | Co / AI-07 | Qw (ACK/entry pending) | IN_REVIEW — PR #60 draft; UTC one-shot only; due-store exceptions/indeterminate results fail closed; recurrence/DST/HA BLOCKED by ADR-76-005; latest scheduler hardening exact-head CI run 44193037401 PASS 71/71 on Python 3.11/3.12 | `trigger_engine/scheduler.py`; `test_work_packages.py` |
| WP-76-04 | Typed Condition Evaluator | Co / AI-07 | Ka / AI-02 (independent QE pending) | IN_REVIEW — PR #60 draft; branch CI PASS | `trigger_engine/conditions.py`; `test_trigger_engine.py` |
| WP-76-05 | Policy adapter and approval | Co / AI-07 | Ka architecture review; Qw QE (ACK pending) | IN_REVIEW — PR #60 draft; fail-closed adapter contract; Core provider not integrated | `trigger_engine/policy.py`; `test_work_packages.py` |
| WP-76-06 | Orchestration, dedupe and retry | Co / AI-07 | Qw (ACK/entry pending) | IN_REVIEW — PR #60 draft; state/retry/idempotency ports; explicit duplicate vs store-unavailable outcomes and strict argument validation added; durable backend not integrated; exact-head CI run 44192865531 PASS 65/65 on Python 3.11/3.12 | `trigger_engine/orchestrator.py`, `retry.py`; `test_work_packages.py` |
| WP-76-07 | Verified AI dispatch adapter | Co / AI-07 (discovery/design only) | Xu + Qw | BLOCKED — no verified transport, target identity, receiver receipt or ACK | `05_BUILD/03_ARCHITECTURE` |
| WP-76-08 | Audit and evidence store | Co / AI-07 | Qw (ACK/entry pending) | IN_REVIEW — PR #60 draft; append-only sink contract only; strict canonical JSON audit digest + non-finite payload regression added; exact-head CI run 44192173589 PASS 54/54 on Python 3.11/3.12; durable store/retention ADR pending | `trigger_engine/audit.py`; `test_work_packages.py` |
| WP-76-09 | Read-only dashboard | Xu (accountable); Co (Vinh-authorized implementation contribution) | An / Qw | IN_REVIEW — separate Work Entry WE-G0…WE-G5 panel, descriptive-status filter normalization and responsive gate grid (tablet/mobile breakpoints) implemented; browser/mobile QE pending | `DASHBOARD` |

PR #55 contains a proposed implementation, tests and CI workflow on an unmerged branch. This is not a merged implementation on main, not runtime/integration verification, and not acceptance. WP status must be updated only with attributable evidence.


## Assignment control
- Co / AI-07 remains the originally delegated implementation owner for WP-76-01…WP-76-08 under DOC-007 / ASG-W76-CO-20261113-01. PR #55 separately contains a Vibe-authored proposal per PR description; Vibe's participant Work Entry/identity was not verified in this reconciliation. No retrospective authorization is inferred.
- Ka / AI-02 has a W76-specific Canonical QE Lead assignment recorded as ASG-W76-KA-QE-20261114-01; participant identity/capabilities remain unverified and G4/G5 BLOCKED. Qw and An remain reviewer nominations only; no ACK/Work Entry PASS is inferred.
- WP-76-07 remains BLOCKED until dispatch transport, identity binding, receipt and ACK are verified.

## Implementation proposal register (2026-11-14)

- Vibe (under Vinh delegation ASG-W76-VIBE-20261114-01) rebuilt a corrected implementation of WP-76-01/02/04/06-scoped core modules on branch `work/76-trigger-engine-vibe-v1`, proposed as draft PR #55 (base main).
- CI run 43541364364 (pytest 3.11/3.12, DOC-006 regression IDs W76-CE-001…004, W76-RG-001…002, W76-MD-001…002, W76-EV-001…002) COMPLETED SUCCESS on commit 8e73fdf.
- WP statuses above are unchanged: branch-level CI PASS is not canonical Build evidence. WP-76-01…08 may move out of PLANNED only after independent review (Xu/Ka), QE reproduction, PR merge approval by Vinh and read-back on main. WP-76-07 remains BLOCKED (no dispatch transport implemented or claimed).
- PR #53 (prototype) remains NOT APPROVED / preserved as audit evidence.


## Co autonomous implementation reconciliation — 2026-11-18
- PR #55 remains open/draft/unmerged as the original proposal history; its branch is divergent from current main and is not the active integration candidate.
- PR #59 is superseded by PR #60; do not merge PR #59.
- Active candidate: PR #60, branch `work/76-co-autonomous-build-v2`, head `acb6dd5052c4c6dfb5a2c5cc4d46fe2e94920da2`, based on current main `9b366fe5ade05568436644ac385d7504a2673605`.
- GitHub Actions run 44186456898 completed successfully: Python 3.11 = 50 passed; Python 3.12 = 50 passed. Raw JUnit artifacts are retained in Actions. This is branch CI only, not independent QE, merged-main verification, Core integration, runtime/E2E or release.
- The new packages expose injected ports and fail-closed behavior. No production crypto/key provider, Core authorization implementation, durable queue/database/audit store, recurrence/DST/HA policy or AI dispatch transport is claimed.
- All statuses remain IN_REVIEW/BLOCKED as above; no WP is marked DONE or accepted.

- Latest branch head after documentation/dashboard reconciliation: `acb6dd5052c4c6dfb5a2c5cc4d46fe2e94920da2`. GitHub Actions run 44186703015 on this exact head also completed SUCCESS: Python 3.11 50/50 and Python 3.12 50/50; JUnit artifacts 14374851948 and 14374162503. This is still branch CI only.

- Supplemental exact-head CI confirmation: run 44186877081 on head `f5e94766dc05286a634cb1883b61f4468e246507` completed SUCCESS (Python 3.11/3.12 each 50/50). Changes since the previous exact-head check were documentation/register/dashboard only; source and tests were unchanged.


## Co autonomous hardening — audit canonicalization — 2026-11-18 05:38 +07:00
- Source change: `trigger_engine/audit.py` now uses the shared strict `canonical_json` encoder for payload digests and record hashes. JSON key ordering/encoding is deterministic and NaN/Infinity are rejected before append.
- Regression additions in `test_work_packages.py`: equivalent mappings with different key insertion order yield identical payload digests; NaN, positive Infinity and negative Infinity are rejected and do not append to the sink.
- Commits: source `a7f2599d44f71a7ed3a9669d8ddc1528f5fd5140`; tests `f0db324f1ef68faf4ec8acf66868549bc5e2ca32`.
- Exact source/test commit CI: GitHub Actions run `44192090937`, status QUEUED at recording time. No PASS is claimed until completion and exact-head verification.
- WP-76-08 remains IN_REVIEW; durable store, atomic append, retention and recovery remain external dependencies under ADR-76-007. No WP status is DONE/accepted.


## Audit canonicalization CI result — 2026-11-18 05:40 +07:00
- Exact PR #60 head: `6489bb162cb37325b87cd4b35c9ab723a703e1be`.
- GitHub Actions run `44192173589` completed SUCCESS on this exact head:
  - Python 3.11: 54 passed / 0 failed; job `134424142019`; JUnit artifact `14376992432`; ZIP SHA256 `7aceb1286c5a98a300bed13e7994337f972ec4638111f018f2f640a067e6002d`.
  - Python 3.12: 54 passed / 0 failed; job `134424140869`; JUnit artifact `14378105646`; ZIP SHA256 `78b262e086b4be6e5da6c76518769df5acc9d13bbd9749e215dc55448cda8418`.
- This is exact-head GitHub branch CI, not independent Canonical QE, main verification, Core/runtime integration, E2E or acceptance.


## Event Gateway hardening — 2026-11-18 05:41 +07:00
- Source: `trigger_engine/gateway.py` now validates event_type before set membership, validates timezone-aware received_at, uses strict canonical JSON for payload digest, constructs/validates Event before reserving replay identity, and maps replay-store failure to declared GatewayRejected.
- Source registration now validates trusted Work id, event-type set and callable schema validator; constructor validates positive integer limits and registration mapping.
- Regression tests cover unhashable event_type, NaN payload not consuming replay key, replay-store outage and naive received_at.
- Commits: gateway source `ba418cbb26fc140564e3e10ea497fc19f47e756c`; tests `d891fe3ee11176a476eba26389edae2dfb20695a`.
- CI for this source/test head has not yet been observed; no test PASS is claimed for this change.
- WP-76-02 remains IN_REVIEW; production signature/key provider and durable replay store remain external dependencies (ADR-76-002 OPEN).


## Event Gateway exact-head CI — 2026-11-18 05:42 +07:00
- Exact PR #60 head: `1a5de9a7007f6b1f80e3153395f94d0342ea4595`.
- GitHub Actions run `44192558442` completed SUCCESS:
  - Python 3.11: 58 passed / 0 failed; job `134425485586`; JUnit artifact `14378131037`; ZIP SHA256 `14c67337ed3f281b546eca9da0b2f938b6b5aaabf027277aa7af920d02c4ff27`.
  - Python 3.12: 58 passed / 0 failed; job `134425485016`; JUnit artifact `14376393806`; ZIP SHA256 `caa7ef0f9243fb70ac2ffd496beb8ee6e69a90c3b2f71ee753f21dfca0e7d799`.
- CI is branch-level exact-head evidence only. No independent Canonical QE, merged-main, Core/runtime integration, E2E or release claim.


## WP-76-06 idempotency fail-closed hardening — 2026-11-18 05:43 +07:00
- `IdempotencyGuard` now distinguishes a true duplicate (`False`) from an unavailable/indeterminate store result or store exception; unavailable conditions raise `IdempotencyUnavailable` and remain fail-closed.
- Validates non-empty Work/key, positive integer TTL excluding bool, and timezone-aware datetime. `RetryPlanner` now validates the clock and requires a strict boolean retryable flag.
- Exported `IdempotencyUnavailable` from the package.
- Regression tests cover store exception, indeterminate response, malformed Work/key/TTL and retry planner malformed inputs.
- Commits: retry source `e22150bd6b9b5a0b101597f5a594ce33fed4569e`; package export `2da13d98bec7730620eba845d7127a394cb48bd1`; tests `987234acd5a5228d7c75e33ae510b1b4edfa7894`.
- CI exact-head for this source/test change not yet observed; no PASS is claimed. Durable atomic store remains external (ADR-76-004 OPEN).


## WP-76-06 exact-head CI — 2026-11-18 05:44 +07:00
- Exact head: `a50aae00e5d4679fbe801e8a0fd48d2ad30396f0`.
- GitHub Actions run `44192865531` SUCCESS:
  - Python 3.11: 65 passed / 0 failed; job `134426542685`; JUnit artifact `14376124853`; ZIP SHA256 `d074fd728886d714d71a02297c32e1159fce8e9bb51cb835b30adf488a154203`.
  - Python 3.12: 65 passed / 0 failed; job `134426542018`; JUnit artifact `14376353840`; ZIP SHA256 `6838b6fb6d2a77b38fce9630a96d30dcaef8b81b60626fa27c7f0543c3543614`.
- This exact-head CI includes WP-76-06 idempotency changes; it predates WP-76-03 scheduler changes committed afterwards. CI for latest scheduler changes remains pending.


## WP-76-03 scheduler exact-head CI — 2026-11-18 05:45 +07:00
- Exact head: `40b73865b0174132eb18e78500ff14e2684d91fa`.
- GitHub Actions run `44193037401` SUCCESS:
  - Python 3.11: 71 passed / 0 failed; job `134427144495`; JUnit artifact `14376823329`; ZIP SHA256 `09658c6f4ad99b827ecf18ed43f4616e5c67b40773baa5ce18840392ee5bec41`.
  - Python 3.12: 71 passed / 0 failed; job `134427144856`; JUnit artifact `14377871600`; ZIP SHA256 `541676ec20827b6261415feebee4b1d9220ab7665f09c245444264cb81cd84b2`.
- This exact-head CI includes scheduler hardening and all prior branch changes. It is branch CI only, not independent Canonical QE or runtime integration.


## Final exact-head CI after WP-76-03/06 hardening — 2026-11-18 05:46 +07:00
- Exact PR #60 head: `a2f8131c080826bd57916222da1308386e7aa215`.
- GitHub Actions run `44193167465` SUCCESS:
  - Python 3.11: 71 passed / 0 failed; job `134427588220`; JUnit artifact `14376898453`; ZIP SHA256 `02496a6479663053a60642b44dac0b5ee78dc309f4aa8faf4e5252e10bb27923`.
  - Python 3.12: 71 passed / 0 failed; job `134427587805`; JUnit artifact `14378400952`; ZIP SHA256 `f7c310009121d28e8603ae9afe2ad4aa3c50a853387a7c46473ffb95d16309aa`.
- Exact-head branch CI covers the current scheduler/idempotency changes. It remains branch CI, not independent QE, merged-main, Core/runtime or E2E.


## WP-76-09 static dashboard correction — 2026-11-18 05:47 +07:00
- Added a separate participant Work Entry panel for Co / AI-07, sourced from DOC-007 snapshot; WE-G0…WE-G3 PASS and WE-G4/G5 BLOCKED are displayed independently of lifecycle phase gates.
- Lifecycle gate summary explicitly labels its scope; no combined Work Entry/lifecycle gate count.
- Work Package filters and status colors now normalize descriptive values such as `IN_REVIEW — ...` and `BLOCKED — ...` to the leading status code.
- PRODUCT_STATUS schema now includes `work_entry`; snapshot identifies DOC-007 assessment date and stale/source limitation.
- Browser/mobile rendering, responsive interaction, accessibility and independent QE remain NOT RUN. No UI PASS is claimed.


## WP-76-09 responsive source adjustment — 2026-11-18 05:49 +07:00
- Work Entry gate grid now uses three columns on desktop, two on tablet and one on mobile.
- CSS breakpoint source updated; no browser rendering or device interaction test was run.


## Latest PR #60 branch-head CI after dashboard snapshot reconciliation — 2026-11-18 05:52 +07:00
- Exact branch head: `15ea37e9b102b8fa54a3ff035102f0e71e407e03`.
- GitHub Actions run `44194106594` SUCCESS:
  - Python 3.11: 71 passed / 0 failed; job `134430849431`; JUnit artifact `14377188728`; ZIP SHA256 `d299ca148895bb36d7dccc66e6e025157a3590248d9bb3e24c463f58c226bebe`.
  - Python 3.12: 71 passed / 0 failed; job `134430850089`; JUnit artifact `14376974287`; ZIP SHA256 `2293bb726d86d45986943955038e4e5fdc2356d482c61e3efbf7f353db0dbd5d`.
- This is exact current branch-head CI; it validates Python tests only and does not exercise browser/mobile dashboard behavior.


## WP-76-07 dispatch capability re-check — 2026-11-18 05:53 +07:00
- Current connected tool inventory was inspected for dispatch/send-agent/target identity/assignment/receiver receipt/authenticated ACK capabilities.
- Available ROOM-HOP tools in this session expose meeting join/start/paste and Work Sandbox operations; no verified AI dispatch provider/transport or receiver ACK action was exposed.
- This is bounded to the current tool session inventory. It does not prove no provider exists elsewhere; it does mean Co cannot honestly mark WP-76-07 implemented or verified.
- WP-76-07 remains BLOCKED pending provider owner/contract and real end-to-end receiver evidence.
