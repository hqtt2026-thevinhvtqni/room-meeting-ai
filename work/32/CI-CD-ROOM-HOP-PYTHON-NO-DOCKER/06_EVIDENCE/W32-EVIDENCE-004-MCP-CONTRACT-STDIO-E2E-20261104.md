# W32-EVIDENCE-004 — MCP Contract Reconciliation and Stdio E2E

- Document Number: W32-EVIDENCE-004
- Priority: P1
- Author: Ka — CSA / Architecture & Backend Owner (delegated)
- Date-Time: 2026-11-04 (hour/minute not captured; not inferred)
- Status: CI / AUTO E2E VALIDATED; CD BLOCKED / NOT RUN

## Evidence
- T8 failed because it expected six MCP tools while the adapter exposed four.
- Git history shows MCP Public Boundary V1 started with three tools in commit `73a454b4a806a47a738ab323b50ce4154a65d6b6`; `add_paste_to_meeting` was added as the fourth tool in commit `d9b0a1a5baea1498a940e8d4652c9e875915c05a`.
- Message v1.0 commit `a799106199976334ef740c80f566f801fb00c667` added T8 expecting six tools, but the Integration client itself describes four locked tools while incorrectly requiring `join_meeting`.
- `API_CONTRACT.md` puts join/start lifecycle actions on Core HTTP routes, not MCP Public V1.

## Changes committed on Work branch
- MCP adapter forwards optional `identity_id` into `MeetingService.add_paste`.
- T8 now asserts the four-tool Public V1 inventory and validates legacy and identified paste transcript metadata.
- Integration client requires only the four locked tools and no longer exposes unsupported MCP `join_meeting`.
- Added `tests/test_ci_mcp_stdio_e2e.py`, which launches the actual MCP stdio subprocess, checks exact tool inventory, list/get, legacy paste, identified paste, and transcript readback.
- Added the stdio E2E test to `.github/workflows/ci.yml`.

## Commit references
- Adapter: `9adce9b54e4c9a9394472c959d1e56cf25911169`
- T8: `b070c59d18f17b0b194caf6b36818aa8a482af53`
- Integration client: `f692dbd0fcc01d4507bb0f57a47745119164abb4`
- Stdio E2E test: `15503d0794d77e6a20d7594e3556c3dd2721f410`
- Workflow: `5309f89984e5ab61d85c22e404babec88ace5995`

## CI status
- Run `41718470071` at final SHA `5309f89984e5ab61d85c22e404babec88ace5995`: QUEUED/PENDING at report creation.
- No validation PASS is claimed for the updated code until the exact SHA run completes.
- Previous run `41718406486` is intermediate SHA and is not accepted as validation of the final changes.

## Branch safety
- Main HEAD observed: `4d2788158b08a48c39abf3d9c74c57314eea3ff4`.
- Work branch compare: 48 ahead / 31 behind; merge base `9e4002cbd93a6b92684b17623d79a1adda161d37`.
- No merge, rebase, cherry-pick, main update, deployment, secrets, or production mutation.
- Overall Work 32: ACTIVE — NOT RELEASED.


## Final exact-SHA validation — PASS

- Validation commit: `fa625d1d7b99f5b326c0ff87641e6c3344d2dd73`
- GitHub Actions run: `41719444619` (run #50), event `push`, conclusion `success`.
- Unit job: `Python 3.12 compile and bounded unit tests` — PASS; `157 passed`.
- Auto E2E job: `Auto E2E (in-process suites + live HTTP roundtrip)` — PASS; `38 passed, 1 warning`.
- Both jobs completed dependency installation, `pip check`, application `compileall`, and test execution successfully.
- MCP stdio subprocess E2E: PASS, including exact four-tool inventory, legacy paste path, identified paste path and transcript readback.
- Unit artifact: ID `13271935444`, SHA-256 `f65f5ded755fc64c51baa876e604e5f8d0cde2b67d748a6f6db46792a35bf9c5`, expires `2026-11-17T21:11:22Z`.
- E2E artifact: ID `13271058785`, SHA-256 `6e2a5149466a56b938d0e59ef5be93b533117c98d5d0b35477cf341481c938c9`, expires `2026-11-17T21:11:23Z`.
- Regression correction: the adapter now omits the optional `identity_id` keyword when it is absent, preserving the legacy `add_paste(meeting_id, raw_text)` service-call contract; when supplied, identity metadata is forwarded. This fixes the three failures observed on prior run #49 without weakening or skipping tests.
- Prior run #49 (`41718781204`, SHA `66a2b664...`) is retained as failed diagnostic evidence; run #50 validates the corrected exact SHA and supersedes it for current CI status.

## Scope and release boundary

- CI / bounded unit gate: PASS.
- Auto E2E / HTTP and MCP stdio gates: PASS.
- CD deployment: NOT RUN — no verified staging/VPS target, deployment credentials, protected environment approval, or tested rollback evidence is present.
- Main merge / production release: NOT AUTHORIZED by this evidence. Branch reconciliation and independent Vibe review remain required.
- Overall Work 32: CI VALIDATED; CD / RELEASE BLOCKED; ACTIVE — NOT RELEASED.


## Final pinned-workflow exact-SHA validation — PASS

- Final documentation/source branch SHA: `6ec0ca6aa9d8c32c912c9dfac140fab141c5b3aa`.
- GitHub Actions run #61: `41720062142` — SUCCESS on the exact SHA above.
- Unit job: PASS — 157 passed in 2.82s.
- Auto E2E job: PASS — 38 passed, 1 warning in 2.70s.
- Both jobs completed exact-SHA checkout, Python 3.12 setup, dependency installation, `pip check`, `compileall`, test execution and artifact retention.
- Unit artifact ID `13271771079`; SHA-256 `b792ec86244662b23a8ced58422500795d5324759ee7ae4dce67d7a7b0d36773`; expires `2026-11-17T21:15:58Z`.
- E2E artifact ID `13272230927`; SHA-256 `1315a1e2a74f760ed538ccd3e207e8f1ec3f549b3f05f7d2ba3c29420db6936e`; expires `2026-11-17T21:15:57Z`.
- Workflow hardening was separately validated on run #58, SHA `4d70e2fce18982cfdd8c3487dee1d15c2ca51fd3`, SUCCESS with the same 157 / 38 passing counts. The workflow uses audited SHA-pinned actions: setup-python `a26af69be951a213d495a4c3e4e4022e16d87065`; upload-artifact `ea165f8d65b6e75b540449e92b4886f43607fa02`.
- Run #59, SHA `64f6d2bc019052402a8e76bd5849e05a58824e37`, also passed after the executable workflow was mirrored into Work evidence.
- The branch push trigger was exercised repeatedly; every new push automatically queued the workflow. Pull requests targeting `main` and manual `workflow_dispatch` are also configured.

## Final disposition

- CI unit: PASS.
- Auto E2E: PASS.
- CD: BLOCKED / NOT RUN pending a verified staging target, protected approval, deployment credentials/host trust, health check and tested rollback.
- Main merge / production release: NOT AUTHORIZED by these CI results.
- Work 32: CI VALIDATED; CD / RELEASE BLOCKED; ACTIVE — NOT RELEASED.
