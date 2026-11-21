# WORK 28 — NHẬT KÝ THI CÔNG / WORK EXECUTION JOURNAL

**Canonical journal:** This is the only Work-wide execution journal for Work 28.  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Branch:** `work/28-mcp-tooling-platform`

## 2026-11-03 — JRN-W28-001 — Governance and GitHub-first restart

**Instruction:** Vinh delegated end-to-end coordination and requested a four-AI team, GitHub-first delivery and minimal PC involvement.

**READ / TRACE**
- Confirmed repository and branch exist; branch HEAD at initial inspection: `a652c49fdc738424a27c6408b386df2dd1af4540`.
- Read current Work 28 manifest, continuation plan, architecture plan, CI workflow, process lifecycle implementation and related tests.
- Found governance drift: the GitHub manifest still assigned Ka as execution lead, treated MCP :8020 as the active AI-facing interface, and prohibited AI GitHub commits/pushes. These statements conflict with the current approved direction.
- Found the current Windows process lifecycle code starts the process before attempting Job Object attachment. The execution path checks the gate after spawn and then attempts cleanup if attachment is missing. This does not yet prove that no command can run before containment is established.
- Confirmed GitHub Actions workflow `.github/workflows/work28-mcp-tooling.yml` has Linux and Windows jobs and is configured for pushes to the Work 28 branch, pull requests and manual dispatch.

**DECIDE**
- GitHub branch `work/28-mcp-tooling-platform` is canonical for code and controlled documents.
- Team is restricted to Xu, Vi, Ka and An; Co excluded.
- Preserve MCP :8030 as Build/Verification lane. Quarantine the historical MCP :8020 listener; do not interact with it. Rebuild Runtime MCP independently.
- Keep Core :8000 as sole authorization/application authority; Execution Host :8031 remains the controlled execution boundary.
- Keep Work status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED and Execution Gate CLOSED.

**BUILD**
- Updated `00_ROOT/WORK_MANIFEST.md` on GitHub to reflect the new authority, team, source-of-truth and architecture rules.
- Commit returned by GitHub: `57d6643f6e5c00849dffff72380aaf59fcbf8b93`.

**VERIFY**
- GitHub API confirmed the manifest update commit was created on the requested branch.
- This is documentation persistence evidence only. No code test, CI result, live runtime test, independent AI acknowledgement or product acceptance is claimed.

**NEXT**
- Add canonical minutes, journal, document register, master execution plan and architecture decision to GitHub.
- Trace the full current code/runtime surface and reconcile old Work 28 reports as evidence.
- Vi: implement only after reading the master plan and exact current branch state.
- Ka: independently review architecture and code changes.
- An: independently reproduce CI and targeted security/lifecycle tests.
- Xu: integrate findings, resolve within delegated authority, maintain blockers and release gate.

## Journal rules
Each entry must include date, task/decision ID, READ/TRACE evidence, action, changed paths/commit, tests and results, unresolved blockers, and next owner. Do not record an assignment as completed work. Never label a run PASS without its actual output.


## 2026-11-03 — JRN-W28-002 — GitHub controlled-document baseline published

**BUILD**
- Published the canonical minutes register: commit `96785335115689f3ef8e8b710968e9131509e7ff`.
- Published the Work-wide journal: commit `2e1f35f8ea91ad2d92c2e8a3137e1206a20c47cc`.
- Published Work 70-aligned structure standard: commit `cf8fe601572777867f4382e753994f3cfa6b5542`.
- Published controlled document register: commit `58811ab648defbff90af56b82501ea7d5b7f39f2`.
- Published master execution plan V2.0: commit `a2c1a2af7f4cf3ca3872551fdb0cfd8771e7a26c`.
- Published architecture decision V2: commit `3f8dcc8e9ac26ec792da7ab2dfdf70156485e40c`.
- Updated Work 28 entry README: commit `236b3e9b5615eff8001ec4da06cdfc1c20eb28ab`.

**VERIFY**
- Read back all eight canonical files from GitHub; contents and blob SHAs were returned successfully.
- Branch HEAD verified as `236b3e9b5615eff8001ec4da06cdfc1c20eb28ab`; compare from initial HEAD `a652c49fdc738424a27c6408b386df2dd1af4540` reports 8 commits ahead and 0 behind.
- GitHub Actions run #265 for commit `3f8dcc8e9ac26ec792da7ab2dfdf70156485e40c` completed SUCCESS. This confirms the configured workflow completed successfully for that commit; it does not verify the later README commit or runtime/product acceptance.
- GitHub Actions run #266 for HEAD `236b3e9b5615eff8001ec4da06cdfc1c20eb28ab` was IN_PROGRESS at the last check. Do not mark it PASS until a completed result is read.

**LIMITATION / BLOCKER**
- The GitHub commit history and file readbacks prove document persistence, not dispatch/acknowledgement by Vi, Ka or An.
- No code implementation was changed in this documentation checkpoint.
- Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate remains CLOSED.


## 2026-11-03 — JRN-W28-003 — Latest documentation commit CI completed

- **Commit:** `17a556b4570e42ee759ea7ece2fc19f19ed216ea`.
- **GitHub Actions run:** #267 — `41548184850`.
- **Conclusion:** SUCCESS.
- **Jobs:** `unit-regression-tests` PASS; `execution-host-lifecycle-linux` PASS; `execution-host-lifecycle-windows` PASS.
- **Scope:** the repository's currently configured Work 28 unit/regression and lifecycle suites on the exact commit above.
- **Interpretation:** this confirms the current configured CI suites pass on Linux and Windows. It does not prove live MCP 8030 provenance, new Runtime MCP deployment, Core E2E, pre-execution Windows containment, OS sandbox isolation, independent Ka review, or release acceptance.
- **Work status:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.


## 2026-11-03 — JRN-W28-004 — Formal work assignments through the canonical journal

**Assignment authority:** Vinh's delegation to Xu.  
**Assignment channel:** This canonical Work 28 journal on GitHub.  
**Scope:** Master Execution Plan V2.0, WP0–WP7.  
**Team limit:** Xu, Vi, Ka and An only. Co is excluded.

### ASSIGNMENT W28-VI-001 — Implementation and integration lead
**Owner:** Vi  
**Status:** ASSIGNED — acknowledgement / execution evidence PENDING  
**Priority:** P0 — start with current branch HEAD; no waiting for PC access.

**Mission:** Execute the approved Work 28 plan end-to-end, WP0 through WP7, within the architecture and safety constraints.

**First deliverables:**
1. Reconcile current branch HEAD and inspect the full source/test/workflow surface; publish an evidence-based WP0 inventory with exact paths and commit.
2. Trace all process creation paths and fix WP2 so Windows Job Object containment is established before untrusted code can execute; POSIX process-group containment must also be verified.
3. Implement in reviewable commits with focused tests and CI evidence. Do not change unrelated scope.
4. Continue WP1, WP3, WP4, WP5 and WP6 according to the master plan; identify true dependencies and do not represent mocks as live integration.
5. Deliver an integrated release-candidate handoff for WP7, including changed paths, commits, commands, test output, known risks and rollback notes.

**Acceptance:** Each package has code-level evidence, reproducible tests and a handoff to Ka and An. No unsupported PASS. Do not touch the historical MCP :8020 listener.

### ASSIGNMENT W28-KA-001 — Independent architecture and security review
**Owner:** Ka  
**Status:** ASSIGNED — acknowledgement / review evidence PENDING  
**Independence:** Review Vi's actual branch diffs and evidence; do not approve based only on descriptions.

**Mission:**
1. Independently review the Work 28 architecture and identify conflicts with Core :8000 authority, MCP :8030 Build/Verification, clean Runtime MCP rebuild and Execution Host :8031.
2. Review WP2 process lifecycle, especially proof that Windows containment exists before command execution and fail-closed behavior on every failure path.
3. Review WP1 registry/contracts, WP3 provenance and sandbox boundaries, WP4 runtime identity, WP5 authorization boundaries, and WP6 audit/evidence controls as their implementation becomes available.
4. Record findings by severity with exact file/line or commit evidence, exploit/failure scenario, required remediation and retest criteria.
5. Issue a final independent architecture/security assessment before release recommendation.

**Acceptance:** Review report references exact commit SHAs and test evidence; unresolved critical/high findings remain explicit blockers. Do not interact with historical MCP :8020.

### ASSIGNMENT W28-AN-001 — Independent QA and verification
**Owner:** An  
**Status:** ASSIGNED — acknowledgement / execution evidence PENDING  
**Independence:** Reproduce results independently; developer test claims are not QA evidence.

**Mission:**
1. Establish the test baseline for the current branch and record exact workflow/run IDs and commit SHAs.
2. Independently run/reproduce unit and regression tests on Linux and Windows CI.
3. Build adversarial/failure-injection coverage for WP2: process spawn failure, Job Object creation/assignment failure, child-process escape, timeout, cancellation, cleanup failure and concurrent jobs.
4. Verify WP1 schema/registry parity and invalid-input behavior; WP3 runtime tools/list and safe I/O evidence; WP4 authorization denial and service identity; WP5 Core authorization and cross-Work isolation; WP6 evidence correlation and redaction.
5. Run end-to-end acceptance tests only against approved, identified services. Never test the quarantined historical MCP :8020 listener.

**Acceptance:** QA report lists exact commit, environment, command, result, logs/artifacts and untested areas. Separate unit, integration, live E2E and security claims.

### COORDINATION W28-XU-001 — End-to-end coordination and acceptance control
**Owner:** Xu  
**Status:** ACTIVE

- Maintain the master plan, canonical minutes, this journal and document register.
- Resolve implementation decisions within the delegated scope; keep the four-AI limit.
- Review Vi handoffs, obtain Ka's independent review and An's independent verification, reconcile findings and assign bounded remediation.
- Keep the release gate CLOSED until all required acceptance evidence exists.
- Report only material blockers or verified milestones to Vinh; do not ask for routine step-by-step approvals.

### Dispatch and acknowledgement rule

This entry is the formal assignment record under the agreed journal-based workflow. GitHub persistence confirms the tasks are recorded and available in the canonical Work 28 location. It does **not** prove that Vi, Ka or An have opened, acknowledged or started them. Each owner must create an acknowledgement/execution artifact referencing the assignment ID. Until that evidence appears, the assignment state remains **ASSIGNED — ACKNOWLEDGEMENT PENDING**.

### Immediate execution order

1. Vi: W28-VI-001 / WP0 inventory and WP2 containment fix.
2. An: W28-AN-001 / independent baseline and native Linux/Windows test plan, in parallel.
3. Ka: W28-KA-001 / architecture and WP2 security review against current source, then review Vi's patch.
4. Xu: coordinate integration, record evidence and resolve blockers across all packages.

## 2026-11-04 — JRN-W28-005 — Add Work Sandbox binary upload to WP3

**Instruction:** Vinh approved adding a reusable Sandbox binary upload capability to the Work 28 build plan.

**READ / TRACE**
- Read current Work 28 Master Execution Plan V2.0, Manifest, Architecture Decision V2 and Controlled Document Register on branch `work/28-mcp-tooling-platform`.
- Existing WP3 already requires Sandbox path containment, Work isolation, read/write authorization, size limits and readback, but did not explicitly define binary upload, byte preservation or checksum verification as a feature/acceptance item.
- Earlier source audit evidence in Work 0001 records that the exposed Sandbox operations were text-oriented and that the uploaded source ZIP had not been transferred byte-for-byte. This is evidence of the gap, not proof of the current deployed service state.

**DECIDE**
- Add shared platform feature W28-WP3-F01 — `sandbox_upload_file` under WP3, not a Work 0001-only workaround.
- Required controls: binary-safe bounded streaming/chunking, Core-authorized Work scope, path/symlink containment, quotas, no-overwrite-by-default, temporary staging, atomic promotion, byte count, SHA-256, readback, audit and failure cleanup.
- Sandbox-to-GitHub publication is a separate controlled capability. Do not claim bidirectional synchronization until implementation and checksum-parity tests exist.
- Keep Work 28 status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED and Execution Gate CLOSED. No tool availability or implementation PASS is claimed by this planning change.

**BUILD**
- Update Master Execution Plan V2.0 with feature scope, ownership, contract and acceptance evidence.
- Update Architecture Decision V2 with mandatory binary upload security properties and service contract.
- Update this canonical journal and controlled document register.

**ASSIGNMENTS (journal-based; dispatch acknowledgement remains pending)**
- Vi: implement W28-WP3-F01 end-to-end after reconciling current branch HEAD, actual MCP 8030 source provenance and transport constraints; deliver code, registry/schema, tests and evidence.
- Ka: independently review upload threat model, authorization, path containment, staging/atomicity, quota and checksum design/diff.
- An: independently test binary fidelity, SHA-256 readback, large/zero-byte files, traversal, symlinks, overwrite, quotas, interrupted/chunked transfer, cancellation and concurrent uploads.
- Xu: coordinate WP3 integration, maintain evidence and prevent unsupported claims; keep the feature NOT VERIFIED until acceptance is met.

**VERIFY**
- This journal entry records the approved scope and formal assignments only. Implementation, runtime deployment, live upload, checksum readback, CI and AI acknowledgement have not yet been demonstrated by this change.

**STATUS:** PLAN UPDATED / IMPLEMENTATION PENDING / WP3 GATE NOT VERIFIED.

## 2026-11-04 04:03 UTC+07:00 — JRN-W28-006 — Resume implementation and reconcile GitHub → Sandbox

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]  
**Source branch:** `work/28-mcp-tooling-platform`  
**Observed HEAD before this journal update:** `af025659baea1a1fdd319e6d57ec3b3a18d664bc`

### READ / TRACE
- Re-read Work 28 through ROOM-HOP MCP 8030 Sandbox and the canonical GitHub branch.
- Confirmed the Work Manifest identifies GitHub branch `work/28-mcp-tooling-platform` as the canonical source; MCP 8030 Sandbox is the controlled build/verification and evidence environment, not an independent source of truth.
- Confirmed the latest observed GitHub HEAD before this journal update was `af025659baea1a1fdd319e6d57ec3b3a18d664bc`.
- Confirmed GitHub Actions run `41716789801` completed with three successful jobs: unit-regression-tests, execution-host-lifecycle-linux and execution-host-lifecycle-windows. This CI result is for the observed HEAD and is not live MCP → Core → W13 E2E evidence.
- Re-read `execution_host/process_job.py` on the branch (blob `47ab511151e81aef120527a2524fb01f4d6cb87b`). The current source still starts the process with Popen before creating/assigning the Windows Job Object; the suspended-spawn candidate is not yet integrated into this canonical source.
- Re-read the Sandbox WP2 validation candidate: 17 test functions are present. They have NOT been executed. Four native-Windows cases require a real Windows runner; concurrent spawn/cleanup race coverage remains absent.
- Re-read the latest WP3 journal decision: shared feature W28-WP3-F01 `sandbox_upload_file` is approved for planning, but implementation, runtime availability, byte-preservation and SHA-256 readback have NOT been demonstrated.
- Sandbox journal readback was behind the GitHub journal: its readable copy ended before the 2026-11-04 WP3 entry. This is a journal synchronization gap, not evidence that GitHub changes were absent.

### ANALYZE / DECIDE
- GitHub remains the canonical source. Continue writing controlled Work 28 source and records to the official branch first; then synchronize the verified corresponding artifacts into Sandbox and read them back.
- Do not bulk-copy an unverified Sandbox candidate over GitHub. Reconcile exact branch HEAD and file blob SHA before each source edit.
- Prioritize WP2 suspended-spawn integration because the canonical source still contains the start-before-Job-Object race. Preserve fail-closed behavior; do not weaken the Job Object gate. Add missing concurrent/repeated cleanup coverage before claiming adequate test coverage.
- Continue WP3-F01 as a separate bounded implementation slice after tracing the live MCP 8030 Sandbox provider/transport and authorization contract. Do not invent an upload endpoint or claim binary capability from the plan alone.
- Keep Core :8000 as the sole authorization authority; do not probe or activate the quarantined historical MCP :8020 listener.

### BUILD / VERIFY — THIS CHECKPOINT
- Appended this continuation record to the canonical GitHub journal first.
- Next implementation slice: reconcile current WP2 candidate against branch HEAD, inspect all spawn/cleanup callsites, port only reviewed changes to the official branch, add/run focused tests on Linux and native Windows, then hand the exact commit and raw outputs to An for independent verification.
- In parallel, trace WP3 binary-upload provider capability and document the exact missing contract/source components before implementing.
- After each GitHub artifact is persisted, synchronize that exact artifact to Work 28 Sandbox and verify readback. This checkpoint synchronizes the canonical journal only; it does not claim source-code synchronization.

### GATES / STATUS
- Work: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.
- WP2: HIGH / OPEN / RELEASE BLOCKER; candidate tests NOT RUN; source integration pending.
- WP3-F01: PLAN APPROVED / IMPLEMENTATION NOT VERIFIED.
- Core authorization and live MCP → Core → W13 E2E: BLOCKED / NOT PROVEN.
- Execution Gate: CLOSED.
- No release, deployment, runtime activation or acceptance is claimed.


## 2026-11-04 04:06 UTC+07:00 — JRN-W28-007 — WP2 suspended-spawn integration checkpoint

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]  
**Branch:** `work/28-mcp-tooling-platform`

### READ / TRACE
- Reconciled canonical branch source `execution_host/process_job.py` (prior blob `47ab511151e81aef120527a2524fb01f4d6cb87b`) against the reviewed suspended-spawn candidate at GitHub blob `85f4866df7710aa2ad0fe1601ae319c470f1718a`.
- Confirmed the candidate blob and the corresponding Sandbox candidate file are byte-for-byte identical at the text-content level (750 lines); no Sandbox-only delta was promoted.
- Candidate lifecycle is: create/configure Job Object before process creation; create Windows process suspended; assign it to the Job Object; resume only after assignment; abort suspended process and raise `JobObjectUnavailable` on failure. POSIX spawn path remains session-based.
- Adapted the 17-case focused validation file to import the canonical `execution_host.process_job` module rather than loading a patch-candidate path.

### BUILD — GITHUB FIRST
- Updated canonical `execution_host/process_job.py` on the official branch. Source commit: `2306b2899537ed40b56630d66abf69674c3cda4c`; resulting blob: `85f4866df7710aa2ad0fe1601ae319c470f1718a`.
- Added `tests/test_process_job_suspended_spawn.py` with 17 focused tests. Test commit: `25a6d96cbf8d7b2c08ef0d907417d9cc5ce640b6`; resulting blob: `831691a44a56d8634a4b13243d664b21b47f64ae`.
- No unrelated files were intentionally changed in this code slice.

### SYNC — GITHUB → ROOM-HOP MCP 8030 SANDBOX
- Synchronized the exact GitHub source blob to `MCP-8020-TOOLING-PLATFORM/04_CODE/execution_host/process_job.py`.
- Synchronized the exact GitHub test blob to `MCP-8020-TOOLING-PLATFORM/05_TEST/test_process_job_suspended_spawn.py`.
- Both Sandbox writes returned `status: ok`; diagnostic readback returned `status: ok` and exact text-content equality with the fetched GitHub file for both artifacts.

### VERIFY / LIMITATIONS
- GitHub Actions run `41718726116` was observed IN_PROGRESS for source commit `2306b2899537ed40b56630d66abf69674c3cda4c` when checked. The test-file commit followed; the final branch-head workflow result is still pending. No test PASS is claimed here.
- No local or Sandbox execution of the 17 tests is claimed. Native Windows behavior must be confirmed by the Windows CI job and, for release acceptance, the required process-tree tests.
- Concurrency/repeated spawn-cleanup race coverage remains an open gap; verify and extend before closing WP2.
- `start_service()` outer API mapping of `JobObjectUnavailable` still requires independent confirmation that callers surface structured BLOCKED rather than an uncaught error.

### NEXT
1. Read final GitHub Actions run for the latest branch HEAD and inspect all Linux/Windows job results and logs.
2. If CI fails, diagnose from raw logs and fix only the failing contract; rerun CI.
3. Send An the exact branch HEAD, changed paths, 17-test suite and raw CI evidence for independent verification; acknowledgement is pending until An records it.
4. Ask Ka to review the actual canonical diff and failure cleanup semantics; no review PASS is assumed.
5. Add concurrency/repeated cleanup tests and verify service-start error mapping.

**STATUS:** WP2 SOURCE INTEGRATED / CI VERIFICATION PENDING / INDEPENDENT REVIEW PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.


## 2026-11-04 04:08 UTC+07:00 — JRN-W28-008 — Make suspended-spawn tests part of native CI

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### VERIFY — TEST DISCOVERY GAP FOUND
- Inspected the actual workflow `.github/workflows/work28-mcp-tooling.yml` and the job logs for run `41718808878`.
- Found that the prior CI workflow used `unittest discover` against named legacy files and did not invoke the new pytest-style `tests/test_process_job_suspended_spawn.py`. Therefore the preceding all-green workflow did NOT execute the new 17-test suspended-spawn suite; it must not be used as proof for the new patch.
- The prior Windows lifecycle job also emitted unrelated errors in the Work 28 evidence/readback suites in its log while the step/job reported success. Those outputs need separate triage; job conclusion alone is not sufficient to claim those individual tests passed.

### BUILD — GITHUB FIRST
- Updated `.github/workflows/work28-mcp-tooling.yml` to install pytest and explicitly run `python -m pytest tests/test_process_job_suspended_spawn.py -q` in both Linux and native Windows lifecycle jobs.
- Workflow commit: `d348dcfad20dd6f7a6e9f09e07eac93121e651e7`; blob: `f9fdfebd4d638be0b7f3d51e6363f4edcbf914ce`.

### SYNC — GITHUB → SANDBOX
- Mirrored the exact workflow file to `MCP-8020-TOOLING-PLATFORM/05_TEST/work28-mcp-tooling.yml` in Sandbox.
- Sandbox write returned `status: ok`; diagnostic readback returned `status: ok` and exact text-content equality with GitHub.

### VERIFY — PENDING
- GitHub Actions run `41718980423` targets workflow commit `d348dcfad20dd6f7a6e9f09e07eac93121e651e7` and was IN_PROGRESS at this checkpoint. No result for the newly added pytest invocation is claimed yet.
- Required next evidence: Linux pytest result, native Windows pytest result, complete job conclusions and raw logs. If native Windows tests fail, remediate and rerun before handoff.

**STATUS:** TEST-DISCOVERY GAP FIXED IN WORKFLOW / NATIVE CI RE-RUN PENDING / WP2 NOT ACCEPTED YET.


## 2026-11-04 04:09:53 UTC+07:00 — JRN-W28-009 — WP2 native CI evidence and WP3 source trace

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### WP2 — NATIVE CI RESULT
- GitHub Actions run `41719053902` targeted the workflow branch after the suspended-spawn pytest command was added.
- Linux focused suspended-spawn suite: **13 passed, 4 skipped**; the four skips are explicitly native-Windows-only tests.
- Native Windows focused suspended-spawn suite: **17 passed**.
- The run reported all three jobs as success, but raw Windows logs also contain four failures in existing unrelated suites: two errors in `test_work28_evidence.py` (`EvidenceError: evidence_tampered`) and two errors in `test_work28_readback.py` (HTTP 409 Conflict and evidence readback errors). The workflow shell did not propagate each intermediate Python exit code, so the job conclusion masked these failures. Do not describe the overall Windows lifecycle suite as clean.
- The new WP2 focused suite itself passed on both operating systems. This is focused test evidence, not final WP2 acceptance: concurrency/repeated-cleanup coverage and service-start structured error mapping remain open.

### CI HARNESS REMEDIATION
- Updated `.github/workflows/work28-mcp-tooling.yml` so each of the 13 Windows Python test invocations checks `$LASTEXITCODE` and exits nonzero immediately on failure.
- Workflow commit: `2987b1b49bd8b6a6549769307d64dd5e2f7468e0`; blob: `a0980124a4eb9e66b5f87ee56de126c4d4cf243e`.
- Synchronized the exact workflow file to Sandbox path `MCP-8020-TOOLING-PLATFORM/05_TEST/work28-mcp-tooling.yml`; write and diagnostic readback succeeded with exact content equality.
- A new Actions run for the guarded workflow is pending; its outcome, not the earlier masked result, determines whether the Windows job is green.

### WP3 — SOURCE TRACE
- Created `06_EVIDENCE/VI_WP3_BINARY_UPLOAD_SOURCE_TRACE_20261104.md` on GitHub (commit `27286da460af5ba1283da876f9807c4cb0e37480`) and synchronized it to Sandbox with exact readback.
- Trace confirms current v54 and v1 Sandbox write/read surfaces are text-only UTF-8; no `sandbox_upload_file` tool/schema/registration or chunked binary path exists in the inspected branch.
- Core authorizer and Core execution session modules are explicitly staged/not wired into v54 Sandbox registration/dispatch. A public upload handler must not be added until trusted Core identity + Work scope is injected and enforced server-side.
- WP3 implementation remains pending; the trace is not runtime evidence.

### NEXT
1. Inspect the guarded Windows CI run; if it now fails at Evidence/Readback, investigate the four exact failures and correct their platform/path semantics or isolate an explicitly documented unsupported suite without suppressing errors.
2. Extend WP2 concurrency/repeated cleanup coverage and verify `start_service()` error mapping; hand exact evidence to An and Ka for independent review.
3. Design the WP3 upload session contract around a trusted Core authorization context before adding tool/schema/provider code.

**STATUS:** WP2 FOCUSED SUSPENDED-SPAWN TESTS PASS ON LINUX/WINDOWS; OVERALL WINDOWS LIFECYCLE SUITE HAS MASKED FAILURES UNDER REMEDIATION. WP3 SOURCE GAP CONFIRMED; IMPLEMENTATION PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.


## 2026-11-04 04:09:53 UTC+07:00 — JRN-W28-010 — Fix Windows evidence seal newline instability

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- With Windows CI exit-code propagation enabled, run `41719266080` failed at `tests/test_work28_evidence.py`: two tests raised `EvidenceError: evidence_tampered` immediately after creating a seal.
- Traced the cause to `execution_host/work28_evidence.py`: `seal_evidence()` hashed a JSON string encoded as UTF-8 with LF, then used text-mode `Path.write_text()`. On Windows, newline translation writes CRLF, so the bytes on disk differ from the bytes hashed. The verifier hashes on-disk bytes and correctly rejects them.
- The earlier readback suite also showed HTTP 409/evidence verification errors; these are consistent with the same cross-platform evidence-byte mismatch and must be rechecked after the fix.

### BUILD — GITHUB FIRST
- Changed evidence persistence to write exact bytes using `write_bytes(body.encode("utf-8"))` and ASCII bytes for the SHA-256 sidecar. This prevents platform newline translation after hashing.
- GitHub source commit: `f60091bbd3ab92368d786d517f0eaed370723472`; blob: `3d2560024b7f08050b0b0ad07a2ce750e5a92a95`.

### SYNC — GITHUB → SANDBOX
- Synchronized exact source to `MCP-8020-TOOLING-PLATFORM/04_CODE/execution_host/work28_evidence.py`.
- Sandbox write returned `status: ok`; diagnostic readback returned `status: ok` with exact text-content equality.

### VERIFY — PENDING
- GitHub Actions run `41719431129` targets source commit `f60091bbd3ab92368d786d517f0eaed370723472`; it was QUEUED/IN_PROGRESS at this checkpoint. Do not claim the Windows fix or downstream readback tests PASS until raw run logs confirm.

**STATUS:** ROOT CAUSE IDENTIFIED / CROSS-PLATFORM BYTE-WRITE FIX COMMITTED / NATIVE CI VERIFICATION PENDING.


## 2026-11-04 04:09:53 UTC+07:00 — JRN-W28-011 — WP2 focused CI verified; An handoff issued

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### VERIFY — GITHUB ACTIONS
- Final CI run for the WP2 implementation and Windows evidence byte-stability fix: `41719431129`, tested commit `f60091bbd3ab92368d786d517f0eaed370723472`.
- All three jobs completed SUCCESS: Linux lifecycle `126207966906`; Windows lifecycle `126207966141`; unit/regression `126207966714`.
- Focused suspended-spawn suite: Linux **13 passed / 4 skipped** (four native-Windows tests); Windows **17 passed**.
- Windows evidence suite: the two previously failing seal tests now pass; Windows readback HTTP tests now pass. No `ERROR` or `FAILED` markers were found in the final Windows job log.
- This verifies the tested source/workflow commit above. It is not live Core E2E, runtime deployment, OS isolation or release acceptance.

### HANDOFF — AN
- Created canonical handoff `10_AI_DEBUG_HANDOFF/00_INBOX/AN/VI_WP2_SUSPENDED_SPAWN_INDEPENDENT_QA_HANDOFF_20261104.md` on GitHub (commit `120bf1ec843c393b0bc6ac181ec63fc8f7816130`).
- Handoff synchronized to Sandbox; write returned `status: ok`; diagnostic readback returned `status: ok` with exact text equality.
- An is asked to independently reproduce both OS suites, inspect all failure-injection paths, add concurrent/repeated spawn-cleanup race tests, and verify `start_service()` structured BLOCKED mapping.
- **Acknowledgement is pending.** GitHub persistence does not prove An opened or accepted the handoff.

### WP2 REMAINING
- Concurrent/repeated spawn-cleanup race coverage remains incomplete.
- `start_service()` outer API error mapping remains unverified.
- OS sandbox isolation remains NOT_VERIFIED.
- Independent Ka security review and An QA acceptance remain pending.

### WP3 REMAINING
- Source trace report `06_EVIDENCE/VI_WP3_BINARY_UPLOAD_SOURCE_TRACE_20261104.md` is published and mirrored to Sandbox.
- Current upload gap is confirmed: no binary upload tool/schema/registration; existing v54 and v1 Sandbox operations are text/UTF-8; Core authorizer is staged and not wired into v54 Sandbox dispatch.
- Next WP3 step is to design trusted Core authorization context and upload session/chunk/finalize contract before implementing provider or exposing a public tool.

**STATUS:** WP2 SUSPENDED-SPAWN FOCUSED CI VERIFIED / INDEPENDENT QA PENDING / RACE + SERVICE MAPPING OPEN. WP3 SOURCE GAP DOCUMENTED / IMPLEMENTATION PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.


## 2026-11-04 04:09:53 UTC+07:00 — JRN-W28-012 — Ka review handoff and WP3 authorization contract proposal

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### HANDOFF — KA
- Created `10_AI_DEBUG_HANDOFF/00_INBOX/KA/VI_WP2_SUSPENDED_SPAWN_SECURITY_REVIEW_HANDOFF_20261104.md` on GitHub (commit `11e9c010423ad806fa090d35652e7fd92bc27539`).
- Synchronized the exact handoff to Sandbox; write returned `status: ok`; diagnostic readback returned `status: ok` and exact content equality.
- Ka is asked to review pre-execution Job Object ordering, kill-on-close/breakaway policy, all failure cleanup paths, POSIX regression, race/reentrancy and start_service error mapping. Acknowledgement is pending; no review result is claimed.

### WP3 — AUTHORIZATION CONTRACT PROPOSAL
- Created `06_EVIDENCE/VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md` on GitHub (commit `f8c27e4e4f38afb3fb6d5646385e4911df22a32c`) and synchronized it to Sandbox with exact readback.
- Proposal identifies the required server-side trusted caller context, Core authorization before filesystem side effects, explicit Core Work ID (W28) to internal Sandbox ID (28) mapping, and bounded begin/chunk/finalize upload session with checksum/readback/audit/atomic promotion.
- Proposal is NOT an approved architecture change. Trusted MCP transport context, Work-ID mapping and Core capability-grant semantics must be confirmed before wiring or exposing upload operations.

**STATUS:** WP2 FOCUSED CI VERIFIED; AN QA AND KA SECURITY REVIEW HANDOFFS SENT / ACKNOWLEDGEMENT PENDING. WP3 SOURCE GAP AND SECURE CONTRACT PROPOSAL DOCUMENTED; IMPLEMENTATION BLOCKED ON VERIFIED TRUST CONTEXT / WORK-ID MAPPING / CAPABILITY CONTRACT. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.


## 2026-11-03 21:32:46.323 UTC — JRN-W28-AUTO-E2E-001 — Establish automated E2E preflight and evidence gate

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Read the canonical Master Execution Plan V2.0, Architecture Decision V2, Manifest, Test Plan and legacy Automatic E2E Blueprint on GitHub.
- Confirmed the legacy Blueprint still contains obsolete participant assignments; its A01–A18 technical matrix is retained, while operating ownership is superseded by the current four-role Manifest and this Auto E2E Runbook.
- Confirmed Core execution session and authorized execution adapter remain staged/not wired into MCP v54 dispatch; test doubles do not prove deployed Runtime integration.

### BUILD — GITHUB FIRST
- Added `04_CODE/work28_auto_e2e_gate_v1.py`: fail-closed evidence evaluator. It requires canonical source commit; MCP/Core/runtime/Execution Host identities; tools/list digest; trusted principal and Core authorization reference; canonical Work ID; expected/snapshot/runtime source hash equality; immutable snapshot; approved runtime identity; OS-isolation attestation; actual exit code; process cleanup; non-empty test summary for RUN_TESTS; protected evidence; explicit readback verification and matching SHA-256. It rejects secret material and ignores caller-reported PASS.
- Added `05_TEST/test_work28_auto_e2e_gate_v1.py` with 13 gate contract cases covering valid evidence, missing identity, authorization denial, unattested isolation, zero tests, nonzero exit, source/checksum/runtime mismatch, secret leakage, missing cleanup, unprotected evidence and unverified readback.
- Updated `.github/workflows/work28-mcp-tooling.yml` to display **Work 28 Automatic E2E Gate**, trigger for Work 28 / Execution Host / Core execution authority / MCP adapter changes, and add a final report job that runs even when a test job fails. The report is a 30-day machine-readable artifact and never upgrades local CI to deployed E2E.
- Added `01_PLAN/WORK28_AUTO_E2E_RUNBOOK_V2.0.md`; registered it; linked it from Test Plan; marked the old blueprint's operating assignments as superseded while retaining A01–A18.

### VERIFY — GITHUB ACTIONS
- Final first pipeline run: `41722405589`, tested commit `952f85bb29e5c67b89d32109cc2c3cf59fa6eae7`.
- All four jobs SUCCESS: unit/regression, Linux lifecycle, Windows lifecycle and automatic E2E gate report.
- Unit/regression: **341 tests, OK**.
- Linux suspended-spawn: **13 passed, 4 skipped** (native Windows cases); Windows suspended-spawn: **17 passed**.
- Core authority boot test exercised a real local CI subprocess and local HTTP socket; it does not prove deployed Core integration.
- Machine artifact: `work28-auto-e2e-report-41722405589`, artifact ID `13273471450`.
- The report correctly returns deployed MCP → Core → Runtime E2E BLOCKED, Execution Gate CLOSED and Release NOT RELEASED.
- Intermediate run `41722309522` failed unit tests after tightening the evidence schema; the test fixture was updated to include the required snapshot hash/protected-readback evidence. The subsequent run `41722328530` and final run `41722405589` passed. This records the red→fix→green iteration without hiding the failure.

### SYNC — SANDBOX
- Synchronized Auto E2E evaluator, its tests, workflow, Runbook V2, Test Plan, Document Register and supersession notice for the old Blueprint to Work 28 Sandbox via MCP 8030.
- Each synchronized file returned diagnostic readback `status: ok` with exact text equality against its GitHub branch content.

### REMAINING LIVE E2E BLOCKERS
1. No verified live MCP :8030 build/process identity plus raw tools/list/schema parity bound to the canonical source.
2. No trusted deployed Core principal/WorkContext integration wired into MCP v54 dispatch.
3. No approved canonical Runtime MCP and Execution Host :8031 deployment/isolation attestation connected to the E2E runner.
4. No deployed end-to-end protected evidence persistence and authorized readback chain.
5. Historical MCP :8020 remains DO NOT USE; no fallback endpoint or parallel host is allowed.

**STATUS:** AUTO E2E CI PREFLIGHT + FAIL-CLOSED EVIDENCE GATE IMPLEMENTED AND FIRST RUN PASS. DEPLOYED AUTO E2E REMAINS BLOCKED. An independent QA and Ka security review remain separate; Vi does not claim their PASS. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.


## 2026-11-03 21:35:45.526 UTC — JRN-W28-AUTO-E2E-002 — HMAC-attested evidence gate hardening and CI rerun

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### SECURITY HARDENING
- During self-review of the first evaluator, identified that a complete but unsigned JSON evidence record could otherwise be forged. A status/evidence gate must authenticate its evidence source, not merely check field completeness.
- Updated `work28_auto_e2e_gate_v1.py` to require HMAC-SHA256 over canonical JSON using a deployment-held `WORK28_E2E_ATTESTATION_HMAC_KEY` and pinned `WORK28_E2E_ATTESTATION_KEY_ID`. The secret is injected out-of-band and is never stored in the evidence record or printed. Missing verifier configuration = BLOCKED; wrong key ID or tampered signature = FAIL.
- Added tests for missing attestation key, tampered signed record and wrong key ID. Total Auto E2E gate contract cases: 16.
- Synchronized updated evaluator, tests and Runbook V2 to Sandbox; diagnostic readback returned `status: ok` with exact content equality.

### VERIFY — HMAC-HARDENED AUTOMATIC PIPELINE
- GitHub Actions run `41723033942`, commit `ae722bd5e2cbbff4112358d6f62c701760afe940`.
- All four jobs SUCCESS: unit/regression, Linux lifecycle, Windows lifecycle and automatic gate report.
- Unit/regression: **344 tests, OK**; Auto E2E evidence gate includes 16 test cases.
- Linux suspended-spawn: **13 passed, 4 skipped**; Windows suspended-spawn: **17 passed**.
- Machine report artifact `work28-auto-e2e-report-41723033942`, artifact ID `13271878443`.
- The report intentionally remains deployed E2E BLOCKED because the live MCP/Core/Runtime/Execution Host identities and protected deployed evidence chain are not wired. Execution Gate remains CLOSED.

**STATUS:** AUTOMATIC CI PRECONDITIONS AND SIGNED EVIDENCE GATE VERIFIED ON LINUX/WINDOWS CI. LIVE DEPLOYED AUTO E2E REMAINS BLOCKED ON TRUSTED DEPLOYMENT INTEGRATION. Independent QA and security review remain An/Ka's responsibility; no PASS/review claim is made for them.


## 2026-11-03 21:39:43.983 UTC — JRN-W28-AUTO-E2E-003 — Path/symlink and recursive secret evidence gates verified

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### GATE HARDENING
- Extended `work28_auto_e2e_gate_v1.py` to require a Work-relative `entry_path`, explicit path-containment attestation and explicit symlink-rejection attestation before PASS.
- Extended secret-material detection recursively through nested dictionaries/lists; a nested `token`/credential field now fails the evidence record.
- Added two tests: path containment not verified → BLOCKED; symlink rejection not verified → BLOCKED; plus nested secret rejection → FAIL. Total gate tests: **19**.
- Synced evaluator, test suite and Runbook V2 to Sandbox; all diagnostic reads returned `status: ok` and exact equality with canonical GitHub file contents.

### VERIFY — LATEST AUTO E2E RUN
- GitHub Actions run `41723678492`, source commit `a8c7ead911ef88334942175c3c8cd7c1df78c662`.
- All four jobs SUCCESS: unit/regression, Linux lifecycle, Windows lifecycle, automatic E2E gate report.
- Unit/regression: **347 tests, OK**, including 19 Auto E2E evidence-gate cases.
- Linux suspended-spawn: **13 passed, 4 skipped** (native-Windows-only tests); Windows suspended-spawn: **17 passed**.
- Report artifact: `work28-auto-e2e-report-41723678492`, artifact ID `13272063957`.
- The machine report still correctly marks deployed MCP → Core → Runtime E2E BLOCKED; Execution Gate CLOSED; Release NOT RELEASED.

**STATUS:** AUTO E2E CI PREFLIGHT AND SIGNED/PATH-ATTESTED EVIDENCE EVALUATOR PASS ON THE TESTED SOURCE. DEPLOYED E2E STILL BLOCKED ON REAL SERVICE IDENTITY, AUTHENTICATED CORE WIRING, APPROVED RUNTIME/ISOLATION AND PROTECTED EVIDENCE READBACK. Independent An/Ka review remains separate.


## 2026-11-04 06:37:00 UTC+07:00 — JRN-W28-W32-AUTO-E2E-ADOPTION-001

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Đã đọc Sandbox Work 32: W32-EVIDENCE-004 (MCP contract + stdio E2E), W32-EVIDENCE-005 (product journey qua HTTP + MCP + persistence), W32-EVIDENCE-007 (exact-SHA immutable artifact pipeline), W32-EVIDENCE-008 (Dashboard integration gap), W32-ADR-001, W32-ADR-002, CI_GATE_MATRIX, product E2E source và fail-closed result classifier.
- Work 32 chứng minh mô hình cần áp dụng là CI-first, exact-SHA, real MCP stdio boundary, product lifecycle E2E, persisted evidence readback, immutable artifact extraction/retest và tách riêng CI / product / browser / CD / release gates.
- Không sao chép meeting-domain API hoặc giả định Dashboard của Work 32 vào Work 28.

### DECIDE / APPLY
- Lập tài liệu chính thức `01_PLAN/WORK28_WORK32_PRODUCT_AUTO_E2E_ADOPTION_20261104.md` để ánh xạ mô hình Work 32 sang luồng Work 28 DISCOVER → AUTHORIZE → SNAPSHOT → HASH → DISPATCH → COLLECT → VERIFY → PERSIST → READBACK → REPORT.
- Giữ Work 28 evaluator, HMAC, path-containment, symlink-rejection, secret checks và các test Linux/Windows hiện có.
- Bước tiếp theo: nâng workflow theo exact-SHA + Python 3.12 + dependency check + compileall + actual MCP stdio contract + immutable artifact build/extract/retest. Product E2E deployed chỉ mở khi có trusted Core grant, approved Runtime và Execution Host :8031 cùng evidence/readback thật.
- Work 32 CI evidence không được dùng làm bằng chứng thay thế cho Work 28 live runtime.

### BASELINE / STATUS
- Work 28 branch baseline read: `1f440eb9f21c356423d3a0eb13cb8b717a8694f3`.
- Latest recorded Work 28 CI run: `41723833958`; bốn job thành công chỉ xác nhận CI preflight.
- Live MCP 8030 → Core → Runtime → Execution Host chain vẫn chưa có đủ trusted identity/authorization/isolation/persistence/readback evidence.
- Execution Gate CLOSED; Work ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.
- An và Ka giữ vai trò kiểm thử/review độc lập; chưa ghi nhận kết quả thay họ.

**STATUS:** WORK 32 PRODUCT AUTO E2E MODEL READ AND MAPPED TO WORK 28. IMPLEMENTATION OF WORKFLOW HARDENING AND ARTIFACT-LEVEL E2E IS NEXT; DEPLOYED PRODUCT E2E REMAINS BLOCKED.


## 2026-11-04 06:59:00 UTC+07:00 — JRN-W28-W32-AUTO-E2E-002 — Exact-SHA artifact and MCP stdio gates implemented

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

### BUILD / FIX
- Reworked `.github/workflows/work28-mcp-tooling.yml` to follow Work 32's exact-SHA CI pattern: explicit detached checkout without submodule recursion, Python 3.12, audited SHA-pinned setup-python/upload-artifact actions, dependency consistency check, compileall, timeouts and a five-job pipeline.
- Added `immutable-source-artifact`: archive exact triggering SHA, calculate and verify SHA-256, extract into a clean directory, reinstall declared dependencies, run pip check/compileall, and rerun all Work 28 unit tests against extracted bytes.
- Added `test_mcp8020_unified_server_stdio_contract_v1.py`: actual child-process MCP stdio session; exact 31 tool names and schemas are compared against the canonical registry. Test doubles are inert and scope is limited to G3 transport/schema contract.
- Constrained root dependency to `mcp>=1.2.0,<2.0.0`. The first exact-SHA pipeline surfaced SDK 2.3.0 incompatibility (`Server.list_tools` missing) and a Windows PowerShell interpolation issue in the manual checkout. Both were fixed; prior successful Work 28 CI had resolved MCP SDK 1.30.0.

### VERIFY — EXACT SHA
- Intermediate run `41743180559`, source `329d3a3a1fdb1e52f35c578d2e730ba553b05cf0`: all five jobs SUCCESS; 347 unit tests; exact-SHA artifact extracted and retested (347 tests).
- Final run `41743292650`, source `e835a13ae0cddd84a077e17055cd9354a874f212`: all five jobs SUCCESS.
- Unit/regression: **348 tests, OK**, including the new real stdio subprocess test.
- Artifact-level retest: **348 tests, OK** after clean extraction; source archive SHA-256 `23dc6b188eb381569f476b6e043b5a12290f4ae610183d926e8a1ab7da3348d6`.
- Linux suspended-spawn: **13 passed, 4 skipped** (native-Windows-only); Windows suspended-spawn: **17 passed**.
- Source artifact ID `13282017725`, uploaded ZIP digest `d41c32f237c795c17892b721e847577e584ca0d89666b8b54863fd706a13fd9c`.
- Auto E2E report artifact ID `13283075166`; report correctly includes unit, Linux, Windows and artifact results.

### HONEST SCOPE
- G3 MCP stdio/tool-schema contract is verified with inert providers only. It is not a live Core-authorized product call.
- Deployed MCP 8030 → Core :8000 → approved Runtime MCP → Execution Host :8031 → protected evidence/readback remains BLOCKED / NOT RUN.
- Execution Gate remains CLOSED; Work ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.
- An and Ka remain independent; no QA/review acceptance is claimed.

**STATUS:** WORK 32 EXACT-SHA + IMMUTABLE ARTIFACT PATTERN ADOPTED; WORK 28 CI/ARTIFACT AND MCP STDIO CONTRACT VERIFIED ON EXACT SHA. DEPLOYED PRODUCT E2E STILL BLOCKED ON TRUSTED SERVICE INTEGRATION.


## 2026-11-04 07:02:00 UTC+07:00 — JRN-W28-W32-AUTO-E2E-003 — Final documentation SHA revalidation

**Role:** VI | CODER  
**Signature:** [KÝ: VI | CODER]

- Updated Runbook V2.0 and Work 28 Test Plan with the adopted Work 32 pattern, exact five-job workflow, MCP stdio contract scope, immutable artifact procedure and current gate boundaries.
- GitHub canonical commit: `61e7b138eaaf0a26e66faad7a4b375b08c6a21b2`.
- Exact-SHA GitHub Actions run `41743643438`: SUCCESS; all five jobs SUCCESS.
- Unit/regression: **348 tests, OK**. Artifact extraction/retest: **348 tests, OK**.
- Linux lifecycle and Windows lifecycle jobs SUCCESS; immutable source archive SHA-256: `9937f4c150638707916ea13a7562205f4bc12b7122697f8aae3f684eb57ec098`.
- Source artifact ID `13281349538`; uploaded ZIP digest `c8480543fd9ce873a78f0b38987eea270c2537e2511adc74161cd08c9a851f0c`.
- Auto E2E report artifact ID `13281513672`; uploaded ZIP digest `a8d46cc509775f24f28d96e8665ab0a23788ec1dcd636d4b18072a671883b4e4`.
- The report preserves the correct boundary: CI and artifact-level regression PASS; deployed MCP 8030 → Core → Runtime → Execution Host remains BLOCKED; Execution Gate CLOSED; NOT RELEASED.
- Runbook, Test Plan and journal were synchronized GitHub → Sandbox Work 28. Diagnostic readbacks returned `status: ok` and exact byte-for-byte text equality.

**STATUS:** WORK 32 MODEL APPLIED TO WORK 28 CI/AUTOMATION AND EVIDENCE PIPELINE; PRODUCT-LEVEL DEPLOYED E2E REMAINS BLOCKED ON REAL TRUSTED SERVICE INTEGRATION.



## 2026-11-13 — JRN-W28-013 — WP2 close-out: start_service BLOCKED mapping + race coverage (Vibe)

**Role:** VIBE | theo ủy quyền tự chủ của Vinh (triển khai phần khả thi, không hỏi lại từng bước)  
**Branch:** `work/28-mcp-tooling-platform`  
**Baseline HEAD đọc trước khi sửa:** `1fdd7b8c8329ed783d068788cd2868f409bdbaa1`

### READ / TRACE
- Đối soát lại nhánh: 2 evidence file của Xu (XU_INTEGRATION_TRACE_V54_TO_W13_W12_20261025.md, XU_EXECUTION_TOOL_CONTINUATION_JOURNAL_20261025.md) đã có trên nhánh — nợ sync cũ đã tất.
- Re-read `execution_host/process_job.py` (blob `85f4866d...`) và `execution_host/host.py` tại baseline: suspended-spawn lifecycle đúng thứ tự; `start_service()` vẫn để `JobObjectUnavailable` (OSError) nổ ra khỏi API — đúng 2 mục WP2 còn mở trong JRN-W28-011/009: (1) race coverage, (2) structured BLOCKED mapping.
- Xác nhận không có route production gọi `start_service()` (server.py /execute → dispatch_execute → execute_work); việc sửa mapping là an toàn cho caller hiện tại và bắt buộc trước khi lộ service API ra ngoài.

### BUILD
- `execution_host/host.py`: `start_service()` bắt `JobObjectUnavailable` và trả kết quả cấu trúc `{status: BLOCKED, blocker: job_object_attach_failed, notes, process_reaped, pid: None, job_object: NOT_ATTACHED}` thay vì raise; không đăng ký process khi BLOCKED. Commit: `98d68a7209447aa0e234455991975b9df59102d8`.
- `tests/test_wp2_service_mapping_and_race.py` (mới, 5 test): BLOCKED mapping, BLOCKED không đăng ký + retry PASS, 5 vòng spawn/cleanup lặp đều reaped, spawn/cleanup process đã exit, 4 worker spawn/cleanup đồng thời đều reaped. Commit: `31f21c34e6296121cd3d086077db7a7f6ab20d8f`.

### VERIFY — PENDING
- Chưa chạy test nào trong môi trường này; bằng chứng duy nhất hợp lệ là GitHub Actions trên commit test. Trước khi có run xanh: WP2 race + service mapping vẫn OPEN, không khai PASS.
- Không đụng MCP :8020; không đổi Core/Runtime/Execution Host; không đổi scope khác.

### NEXT
1. Đọc kết quả Actions run cho commit `31f21c34...` (unit + Linux + Windows + artifact + auto E2E gate); nếu Windows fail do hành vi process khác platform → sửa chỉ phần đó.
2. Handoff evidence cho An (QA độc lập) và Ka (review diff `host.py` + test mới) theo đúng quy trình JRN-W28-011/012.
3. WP3-F01 vẫn BLOCKED chờ 4 quyết định trong VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md (trusted transport context; mapping W28↔28; 1 tool streaming hay 3 tool begin/chunk/finalize; capability-grant semantics) — chờ Vinh quyết.

**STATUS:** WP2 SERVICE MAPPING + RACE COVERAGE COMMITTED / CI VERIFICATION PENDING / INDEPENDENT REVIEW PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.



## 2026-11-13 — JRN-W28-014 — Vinh's WP3-F01 decision input recorded; routed to Xu

**Role:** VIBE | ghi theo chỉ dẫn trực tiếp của Vinh trong phiên làm việc 2026-11-13  
**Branch:** `work/28-mcp-tooling-platform`

### DECISION INPUT FROM VINH (WP3-F01 — sandbox_upload_file authorization contract)
Vinh trả lời 4 câu hỏi mở trong `06_EVIDENCE/VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md` như sau:
1. **Trusted caller context:** CHƯA QUYẾT — không chọn giữa MCP/transport session đã xác thực và service credential pinned.
2. **Mapping Work ID (Core W28 ↔ Sandbox 28):** CHƯA QUYẾT.
3. **Hình thức tool (1 streaming vs 3 begin/chunk/finalize):** CHƯA QUYẾT.
4. **Core capability-grant cho upload:** CHƯA CHẤP THUẬN — yêu cầu Ka review trước khi cấp.

### ROUTING (theo chỉ dẫn của Vinh)
- Các quyết định trên được ghi lại tại đây để **Xu quyết** trong phạm vi ủy quyền điều phối; Vibe không tự chốt thay Xu/Ka.
- Hồ sơ trình quyết định tổng hợp (options + hệ quả từng phương án) được chuẩn bị trên **nhánh riêng** `work/28-wp3-xu-decision-brief` (không đụng nhánh canonical cho đến khi Xu quyết).
- WP3-F01 giữ nguyên: IMPLEMENTATION BLOCKED. Không có code upload nào được viết.

### WP2 STATUS (từ JRN-W28-013)
- Commit `98d68a7` (start_service BLOCKED mapping) + `31f21c3` (5 test race/mapping) đã lên nhánh; run #325 bị cancel do concurrency, run #327 trên HEAD `8c9ff9d` đang IN_PROGRESS lúc ghi dòng này. Chưa khai PASS.

**STATUS:** WP3-F01 DECISIONS PENDING AT XU (Ka review required for capability-grant) / WP2 CI PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.



## 2026-11-13 — JRN-W28-015 — WP2 handoff evidence to An and Ka; decision brief branch published (Vibe)

**Role:** VIBE | theo ủy quyền tự chủ của Vinh  
**Branch:** `work/28-mcp-tooling-platform`  
**HEAD trước entry này:** `563b03f` (JRN-W28-014, đã xác minh append-only +24/−0 qua commit stats)

### BUILD
- Handoff AN (QA độc lập): `10_AI_DEBUG_HANDOFF/00_INBOX/AN/VI_WP2_SERVICE_BLOCKED_MAPPING_RACE_QA_HANDOFF_20261113.md` — yêu cầu An đọc run #327 từng job trên đúng commit, tự chạy lại 5 test mới trên Linux + Windows native, adversarial coverage (cleanup raise, registry state sau BLOCKED, signal/timeout), xác nhận không route production bị ảnh hưởng.
- Handoff KA (security review): `10_AI_DEBUG_HANDOFF/00_INBOX/KA/VI_WP2_SERVICE_BLOCKED_MAPPING_RACE_SECURITY_REVIEW_HANDOFF_20261113.md` — 5 câu hỏi review: fail-closed semantics của BLOCKED, reap semantics (handle/zombie leak), race/reentrancy đủ chưa, BLOCKED có cần mã lỗi chuẩn hóa/audit event cho WP6, scope diff thực tế.
- Cả hai handoff trong 1 commit docs-only: `c13adcc7575243040567b8c7a14ff7cbbfb1025f` (2 file mới, không đổi code).

### WP3 DECISION BRIEF (nhánh riêng, theo chỉ dẫn JRN-W28-014)
- Nhánh `work/28-wp3-xu-decision-brief` tạo từ `563b03f`; hồ sơ `06_EVIDENCE/XU_WP3_F01_DECISION_BRIEF_20261113.md` (commit `a37a5bea115c962ebd879e0384e520ca7ff114a6`): bảng options + tradeoffs cho 4 câu hỏi, khuyến nghị kỹ thuật không ràng buộc (A cho caller context làm bước đầu; mapping động từ Core là đích đúng; 3-tool begin/chunk/finalize khớp acceptance JRN-W28-005), quy tắc thi công sau quyết định, capability-grant bắt buộc Ka review trước.
- Không viết code upload; WP3-F01 giữ IMPLEMENTATION BLOCKED.

### VERIFY — PENDING
- Run #327 (HEAD `8c9ff9d`) vẫn IN_PROGRESS lúc ghi entry này; run #324/#326 SUCCESS, #325 cancel do concurrency. Không khai PASS cho WP2 service mapping + race coverage cho đến khi #327 xanh trên commit `8c9ff9d` hoặc commit sau đó chứa cùng code.
- Acknowledgement của An và Ka CHƯA có; GitHub persistence không chứng minh họ đã đọc handoff.

### NEXT
1. Đọc kết quả run #327; nếu xanh → ghi CI evidence vào journal; nếu Windows fail → sửa chỉ phần fail.
2. Chờ An/Ka acknowledge + kết quả độc lập; chờ Xu quyết 4 câu WP3 trên hồ sơ decision brief.
3. Sau khi Xu quyết: triển khai WP3-F01 trên nhánh riêng, PR có CI xanh mới merge về canonical.

**STATUS:** WP2 HANDOFFS ISSUED (AN + KA ACK PENDING) / WP3 DECISION BRIEF PUBLISHED ON SEPARATE BRANCH / CI #327 PENDING. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.


## 2026-11-13 — JRN-W28-016 — Xu contract decisions for WP3-F01; Q4 held for Ka review

**Role:** XU | delegated Work 28 architecture and integration decision owner  
**Branch:** `work/28-mcp-tooling-platform`  
**Decision record:** `06_EVIDENCE/XU_WP3_F01_DECISION_RECORD_20261113.md`  
**Decision record commit:** `0d62088bf55401441ed589682f109f51a0b0084f`  
**Source brief:** `work/28-wp3-xu-decision-brief`, commit `a37a5bea115c962ebd879e0384e520ca7ff114a6`

### READ / TRACE
- Read the full WP3-F01 decision brief on its dedicated branch and the original `VI_WP3_BINARY_UPLOAD_AUTHORIZATION_CONTRACT_PROPOSAL_20261104.md` on the canonical branch.
- Confirmed the source trace states v54 currently has text UTF-8 read/write only; binary upload tool/schema/registration is absent, and the staged Core authorizer is not yet wired into v54 dispatch.
- Confirmed the proposal explicitly rejects caller-supplied identity/work claims as authentication, requires Core authorization before Sandbox side effects, and requires an explicit Work-ID mapping.
- Confirmed canonical journal JRN-W28-015 is present at HEAD `7f731b49488e09fd6d19ae34243da85d6de710fe`; compare against `work/28-mcp-tooling-platform` returned identical (0 ahead / 0 behind) before this decision update.

### DECIDE
Xu approves three contract directions:
1. **Q1 — Trusted caller context: Option A.** Use authenticated MCP/transport session context resolved server-side and passed out-of-band. Missing/invalid/expired context denies before filesystem access. stdio is trusted only under an approved trusted parent/runtime with principal binding; HTTP upload must not be exposed before authentication is enforced. This does not claim current v54 already implements the context.
2. **Q2 — Work ID mapping: Option B.** Core :8000 returns the authoritative dynamic Sandbox/provider mapping in trusted WorkContext/authorization response. No hardcoded W28→28 mapping, caller-derived normalization or production static fallback. Missing/conflicting/stale mapping blocks before side effects.
3. **Q3 — Upload protocol: Option B.** Adopt begin/chunk/finalize with bounded chunks, opaque short-lived sessions bound to caller/Work/path/quota/expiry, strict ordering and byte limits, final exact byte-count + SHA-256 verification, atomic promotion, independent readback and audit. Abort/cancel or equivalent server-side cancellation and idempotent staging cleanup are mandatory.

**Q4 — Core capability grant: NOT APPROVED.** Vinh required Ka review before approval. Ka must review the concrete grant design against principal/Work binding, operation/path scope, quotas, TTL, revocation/replay, overwrite policy, pre-side-effect checks and audit behavior. Xu will not approve a grant broader than Ka's reviewed revision. Until Ka's evidence-backed review and a subsequent Xu decision, upload remains DENY/BLOCKED with no staging or filesystem side effect.

### BUILD
- Published the controlled decision record as a new evidence file in the canonical branch; commit `0d62088bf55401441ed589682f109f51a0b0084f`.
- No code, runtime, routing, Core, Execution Host or capability grant was changed.

### VERIFY
- Decision record commit returned by GitHub create-file operation.
- Journal update is appended below JRN-W28-015; no prior entry is rewritten.
- CI #327 remains a separate pending verification item; this decision does not infer its result.
- An/Ka acknowledgements for the WP2 handoffs remain pending until their own evidence artifacts are published.

### NEXT
1. **Ka:** review Q4 capability-grant design and publish an independent artifact tied to the exact revision.
2. **Xu:** decide Q4 only after Ka's review; record the decision append-only.
3. **An:** independently complete WP2 QA handoff against exact tested commit and CI run.
4. **Xu/CI owner:** read run #327 live result; record PASS only if completed green on the code-bearing SHA.
5. After Q4 is approved, prepare implementation plan/test matrix; do not start WP3-F01 code before the decision gate is closed.

**STATUS:** Q1–Q3 DECIDED / Q4 BLOCKED PENDING KA REVIEW / WP3-F01 IMPLEMENTATION BLOCKED. WP2 CI #327 and An/Ka handoff acknowledgements remain independent pending items. Work ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.



## 2026-11-13 — JRN-W28-017 — WP2 CI verified on code-bearing SHA; runs #327–#332 green (Vibe)

**Role:** VIBE | thực hiện mục NEXT #4 của JRN-W28-016 (đọc run #327, ghi PASS nếu xanh trên commit chứa code)  
**Branch:** `work/28-mcp-tooling-platform`  
**HEAD trước entry này:** `d2822b0a` (JRN-W28-016 của Xu)

### VERIFY — GITHUB ACTIONS (workflow "Work 28 MCP Tooling Tests", branch work/28-mcp-tooling-platform)
- **Run #327 — commit `8c9ff9d` (code-bearing: chứa `host.py` BLOCKED mapping `98d68a7` + 5 test race/mapping `31f21c3`; `8c9ff9d` chỉ khôi phục 4 dòng journal): COMPLETED SUCCESS.** Đây là bằng chứng CI cho WP2 service mapping + race coverage.
- Run #328 (`563b03f`, docs JRN-W28-014): SUCCESS. Run #329 (`c13adcc`, docs handoffs): SUCCESS. Run #330 (`7f731b4`, docs JRN-W28-015): SUCCESS. Run #331 (`0d62088b`, Xu decision record): SUCCESS. Run #332 (`d2822b0a`, JRN-W28-016): SUCCESS (2m11s).
- Run #325 bị cancel do concurrency; không dùng làm bằng chứng.
- Kết quả đọc trực tiếp từ trang Actions của workflow; không suy diễn từ commit docs.

### INTERPRETATION (giới hạn đúng)
- CI xanh trên commit chứa code xác nhận: unit/regression + Linux lifecycle + Windows lifecycle + immutable artifact retest + auto E2E gate report đều pass với mapping BLOCKED và 5 test mới trong suite.
- KHÔNG chứng minh: acknowledgement QA của An, security review của Ka, OS sandbox isolation, live MCP 8030 → Core → Runtime → Execution Host E2E, release acceptance.
- WP2 vẫn cần An + Ka acknowledge độc lập theo handoff `c13adcc`.

### WP3-F01 STATUS (theo XU-W28-WP3-F01-DEC-20261113-01)
- Q1=A (caller context từ transport session, có điều kiện), Q2=B (mapping động từ Core), Q3=B (begin/chunk/finalize + abort): DECIDED.
- Q4 capability-grant: BLOCKED chờ Ka review; WP3-F01 giữ IMPLEMENTATION BLOCKED; không viết code upload. Implementation plan/test matrix sẽ chuẩn bị sau khi Q4 được phê duyệt (theo NEXT #5 của JRN-W28-016).

**STATUS:** WP2 SERVICE MAPPING + RACE COVERAGE CI-VERIFIED ON `8c9ff9d` (RUN #327 SUCCESS) / AN + KA ACK PENDING / Q4 PENDING KA. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.

## 2026-11-13 — AN | TESTER — Git/Sandbox sync checkpoint

- Thời điểm ghi: 2026-11-13 UTC+07:00.
- Vai trò: An | TESTER / Independent QA.
- Yêu cầu vận hành: chuyển Git thành lane xây dựng/kiểm thử chính; Sandbox là lane hồ sơ/evidence hỗ trợ.
- GitHub branch search xác nhận branch work/28-mcp-tooling-platform tồn tại.
- GitHub commit search theo repository với từ khóa work-28 trả về commit Work 28 mới nhất tìm thấy: 157e88e2cd821a0b53bdcabd6483956e6bc2074a — docs(work-28): define automatic E2E operating runbook v2 (2026-11-04 04:27:37 UTC+07).
- Commit này chỉ thay đổi work/28/MCP-8020-TOOLING-PLATFORM/01_PLAN/WORK28_AUTO_E2E_RUNBOOK_V2.0.md.
- Truy workflow runs theo commit này: danh sách rỗng; combined status: không có status records. Không được diễn giải thành CI PASS/FAIL.
- Sandbox master journal có nội dung đến 2026-11-12, bao gồm các phát hiện P0 về Core Authority ↔ Execution Host: Boolean authorized trust, local FileGrantSource fallback, thiếu atomic grant/revoke/run, thiếu exact-SHA binding, protocol mismatch và OS sandbox isolation NOT VERIFIED. Các nội dung này là static source trace/decision records; lượt đọc hiện tại không chạy test.
- Chênh lệch đồng bộ: nội dung nhật ký Sandbox mới hơn commit Work 28 mới nhất tìm thấy trên GitHub. Chưa thể kết luận branch HEAD thực tế chỉ là commit nêu trên vì connector search commits là kết quả tìm kiếm, không phải branch-ref HEAD endpoint.
- GitHub connector trong phiên không có shell runner để An thực thi pytest; workflow/status truy vấn không trả kết quả. QE execution trong lượt này: NOT RUN.
- Không ghi đè nhật ký Sandbox bằng bản Git cũ; giữ nguyên toàn bộ lịch sử Sandbox. Không thực hiện Git write/commit/push vì quyền push của connector chưa được xác nhận/đang read-only.
- Hành động đồng bộ: ghi nhận checkpoint này trực tiếp vào Sandbox master journal; yêu cầu lane Coder/authorized Git operator đưa các bản ghi canonical đã duyệt và cập nhật cần thiết lên branch Work 28; sau đó An sẽ đối chiếu blob SHA và nội dung hai chiều.
- Trạng thái: Git branch FOUND; Git↔Sandbox FULL SYNC NOT ACHIEVED; Sandbox journal checkpoint WRITTEN; pytest NOT RUN; Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

[KÝ: AN | TESTER]

## 2026-11-13 — JRN-W28-018 — GitHub pytest lane enabled; exact-SHA CI #337 PASS (Xu)

**Role:** XU | Work 28 coordinator and technical decision owner  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Source commit under test:** `5c7bbfd452a6948fccae1717d3d2a7159b69520f`  
**GitHub Actions:** Run #337 / ID `43385810696`  
**Workflow:** `Work 28 Automatic E2E Gate`

### READ / TRACE
- Read the canonical Work 28 workflow and confirmed the main regression job ran unittest discovery for `05_TEST`, while pytest was previously limited to selected execution-host lifecycle tests.
- Confirmed the canonical test directory is `work/28/MCP-8020-TOOLING-PLATFORM/05_TEST` and the CI runner checks out the exact triggering Git SHA.
- Preserved the earlier Sandbox-only An checkpoint as a historical record below this entry's predecessor, rather than silently deleting or rewriting it.

### BUILD
- Updated `.github/workflows/work28-mcp-tooling.yml` to install pytest in the primary regression job and run the complete Work 28 test directory:
  `python -m pytest 05_TEST -q`
- Change committed directly to the canonical GitHub branch as `5c7bbfd452a6948fccae1717d3d2a7159b69520f`.
- Synced the exact workflow file GitHub → Work 28 Sandbox at `MCP-8020-TOOLING-PLATFORM/.github/workflows/work28-mcp-tooling.yml`.
- Sandbox readback returned `status: ok`, size 15,343 bytes, and exact text equality with the GitHub file (blob `aef70150c274ecb076bcb3e94c558892e3b52573`).

### VERIFY — EXACT SHA / RUN #337
- Overall GitHub Actions run #337: **COMPLETED SUCCESS** on source commit `5c7bbfd452a6948fccae1717d3d2a7159b69520f`.
- Unit/regression job: **348 tests, OK**.
- Full pytest suite: **348 passed, 238 subtests passed** in 10.24 seconds.
- Linux execution-host lifecycle job: **SUCCESS**.
- Windows execution-host lifecycle job: **SUCCESS**.
- Immutable exact-SHA source artifact build, extraction and retest: **SUCCESS**; artifact ID `14018072815`; retest log reports 348 tests, OK.
- Automatic E2E gate report job: **SUCCESS**; artifact ID `14018358159`.
- The generated report explicitly keeps deployed MCP → Core → Runtime E2E **BLOCKED**, Execution Gate **CLOSED**, and release **NOT_RELEASED**. Its blockers are absent live MCP build/process provenance, trusted deployed Core principal/WorkContext evidence, approved Runtime/Execution Host deployment/isolation attestation, and complete deployed request-to-evidence readback.
- Run link: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/43385810696

### INTERPRETATION / LIMITS
- This is a real GitHub-hosted pytest run against the exact source SHA, not a local or Sandbox test claim.
- Pytest and the configured regression/lifecycle/artifact jobs are CI-verified for this SHA.
- It does not establish independent An QA acceptance, Ka security review, deployed product E2E, OS sandbox isolation, or release acceptance.
- Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate remains CLOSED.

### NEXT
1. Continue implementation only within approved gates; WP3-F01 code remains blocked until Ka reviews Q4 capability-grant semantics and Xu records the final decision.
2. Obtain An's independent WP2 reproduction and Ka's independent WP2 security review on the code-bearing SHA.
3. Continue WP0–WP7 source/runtime integration with exact-SHA pytest and CI evidence.
4. Sync this canonical journal revision to Sandbox and verify exact readback.

**STATUS:** GITHUB PYTEST LANE ENABLED / 348 PYTEST PASSED / RUN #337 SUCCESS / WORK 28 NOT RELEASED.


## 2026-11-15 13:07 UTC+07:00 — JRN-W28-019 — Ka independent Q4 capability-grant review

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0  
**Scope:** Xu decision XU-W28-WP3-F01-DEC-20261113-01, Q4 — Core capability-grant semantics for W28-WP3-F01 `sandbox_upload_file`.

### READ / TRACE
- Read canonical Xu decision record, Vi upload authorization proposal and source trace, Core Execution Authority V1.2 proposal, Core authority implementation, HTTP surface, append-only store, Execution Host grant client/dispatch and related tests.
- Review artifact: `06_EVIDENCE/KA_WP3_F01_Q4_CAPABILITY_GRANT_SECURITY_REVIEW_20261115.md`.
- Review artifact GitHub commit: `89244da15a7b56de5df67345110f45cd1eeaf6c5`; pinned-revision update commit: `446242dbeb8562d96889df25d254cf5d22677a4f`; final report blob SHA: `268ae8ec4d96c442b7e61bae4f83c5c6294b36d8`.
- Reviewed exact source blobs include: Xu decision `8dbd82b69b4c295626ab5fb101c28b9bb0b6195e`; Vi proposal `b957eba4fce949bfdfba56ba8da9dd71d9bfc29`; Vi source trace `fb4a95a49214b54c5c28407179860999f5bf7a16`; Core authority contract V1.2 `80199539afc45022980a481e1bc81b8aed160096`; authority implementation `bfb052fed0fde69767dd219f17a0b14ae6383560`; Core HTTP `6363c277ce410d3f5465f449b730199e06e5024c`; store `a628dc578c68c05bb875318d1b74528b26f0e4eb`; Host grant client `75b28b49a8d2ce7561d722519af293d00fac13aa`; Execution Host server `87644127a9a2df638b5677758cfc4d0c883b2985`.
- Branch HEAD was not independently pinned by the available connector operation. Findings are bound to the listed file blob SHAs, not asserted as an immutable branch-wide snapshot.

### REVIEW RESULT
- **Q4 = NOT APPROVED / BLOCKED.** No complete upload-specific capability-grant schema exists in the reviewed revision.
- Core Execution Authority V1.2 is an execution-grant proposal, explicitly NOT APPROVED / NOT IMPLEMENTED / NOT WIRED; it is not an upload capability contract and must not be silently reused.
- Gaps: no explicit capability/operation allow-list, normalized destination scope binding, grant/session mapping-version binding, atomic quota reservation, defined TTL relationship, upload-session revocation, replay/idempotency semantics, per-operation reauthorization/state checks, or durable audit ordering.
- Adjacent P0 risks recorded separately: Core grant client can select local FileGrantSource fallback when Core URL is absent or fetch fails; Execution Host command mode remains available unless snapshot_only is enabled and uses static token/Work allow-list rather than proof of a Core-issued upload grant. These do not get fixed by Q4 approval.
- The Core authority test docstring calls DR-1..DR-4 “approved decision requests”, while the V1.2 contract explicitly remains NOT APPROVED awaiting Vinh. This is a documentation/provenance contradiction, not evidence of approval.
- No code was changed; no test or live service was run; no upload tool, staging, filesystem write, grant issuance or execution gate was enabled.

### DECISION / NEXT
- Ka does not approve Q4 on the current revision. Xu must record Q4 as NOT APPROVED and request a revised versioned upload-capability contract from Vi.
- Vi to revise grant schema/state machine and defect-to-test matrix; no WP3-F01 implementation until Xu records a subsequent Q4 decision.
- An to independently review the revised test plan after contract revision; no acknowledgement or execution is assumed.
- Ka to re-review exact revised blob SHAs before Q4 can be reconsidered.
- Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

### RECORD CORRECTIONS
- The previous assistant turn incorrectly appended an entry named `W28-JRN-20261103-01` to the legacy `06_EVIDENCE/NHAT_KY_THI_CONG.md`, using an incorrect date/time and incorrectly naming Co in the active role assignment. That entry is NOT a canonical Work-wide journal record and must not be used as an assignment or status authority. The legacy file is preserved unchanged as historical evidence; this correction is authoritative.
- The current approved Work 28 team is exactly Xu (Coordinator/Decision Owner), Vi (Implementation Lead), Ka (Independent Architecture/Security Reviewer), and An (Independent QA). Co is excluded, per Manifest and official minutes.
- The earlier assistant's labels “WP-A0” and “WP-B0” were shorthand, not canonical Work package IDs. The controlling plan is WP0–WP7 in `WORK28_MASTER_EXECUTION_PLAN_V2.0.md`; no official package was created under those shorthand labels.

**STATUS:** Q4 REVIEW COMPLETE / Q4 NOT APPROVED / WP3-F01 IMPLEMENTATION BLOCKED / EXECUTION GATE CLOSED.


## 2026-11-15 13:07 UTC+07:00 — JRN-W28-020 — Ka independent WP2 service lifecycle and cleanup review

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0  
**Reviewed tree:** `8c9ff9d3a8f25faad03f0254954930de2031bedf`  
**Evidence:** `06_EVIDENCE/KA_WP2_SERVICE_REGISTRY_CLEANUP_SECURITY_REVIEW_20261115.md`  
**Evidence create commit:** `5f60ba8e607896a5de49958e5aa449b70154b66f`  
**Evidence readback blob:** `df8d857b602fb4d0b5ff555b0714a53907d33d2d`

### READ / TRACE
- Read exact source blobs for ExecutionHost service registry, execute-command path, suspended-spawn process manager, cleanup bridge and WP2 test suites. Blob SHAs are recorded in the review artifact.
- Static positive: Windows Job Object is created/configured before CREATE_SUSPENDED process creation; assignment precedes ResumeThread; assignment/resume failures abort without intentionally running user code; command and service paths share the spawn helper.
- Native Windows marker tests exist for command/service success and assignment/resume failure. Ka did not execute these tests in this review.
- Canonical JRN-W28-017 reports GitHub Actions run #327 SUCCESS on the reviewed code-bearing tree. Independent workflow/status lookups for full commit `8c9ff9d3a8f25faad03f0254954930de2031bedf` returned empty arrays in this session; run #327 is therefore recorded as journal-reported, not independently revalidated by Ka.

### REVIEW FINDINGS
- **WP2-SVC-01 HIGH:** `stop_service()` removes the registry entry before cleanup succeeds. If cleanup returns process_reaped=false, the handle is lost; a later call can incorrectly return STOPPED.
- **WP2-SVC-02 HIGH:** `start_service()` overwrites an exited leader's ManagedProcess without draining possible surviving Job/process-group children.
- **WP2-SVC-03 HIGH:** no per-service lock protects check → spawn → register; concurrent same-name starts can create duplicate processes and leave one untracked.
- **WP2-EVID-04 HIGH:** `run_execute_command()` loses `JobObjectUnavailable.process_reaped` when spawn fails; `attested_cleanup(None)` then reports process_reaped=true/no_process even when abort was not confirmed.
- Test gap: existing concurrency test covers direct spawn/cleanup, not shared ExecutionHost service registry, same-name start, stale-leader replacement or cleanup retry.
- `ISOLATION_STATUS` remains NOT_VERIFIED; Job Object containment is not OS sandbox isolation.

### DECISION / NEXT
- **WP2 = PARTIAL / HIGH FINDINGS OPEN / NOT ACCEPTED.** Suspended-spawn design is statically positive; service registry and cleanup/evidence callers remain release blockers.
- Vi to patch the four findings and add exact regression tests; An to independently test native Windows and Linux; Xu to retain WP2 open until acceptance evidence exists; Ka to review the exact patched blobs.
- No tests run by Ka, no production listener touched, no code changed and no execution gate opened.

**STATUS:** WP2 STATIC REVIEW COMPLETE / WP2 NOT ACCEPTED / EXECUTION GATE CLOSED.


## 2026-11-15 21:36 UTC+07:00 — JRN-W28-021 — Ka independent WP0 MCP :8030 provenance reconciliation

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0 — Source/runtime provenance gate  
**Inspected branch HEAD:** `9a19d6df9a2a7bb122817d65df90426b48b57116`  
**Evidence:** `06_EVIDENCE/KA_WP0_MCP8030_PROVENANCE_RECONCILIATION_20261115.md`  
**Evidence create commit:** `c26fb9ea2a525e0c34b7a2ed1e2c1e84a054c188`  
**Evidence readback blob:** `e69dbc57651bd5d76c1a9ce82e5b69fc0741c84f`

### READ / TRACE
- Read the canonical Manifest, Master Execution Plan V2.0, current Work journal, historical 18-tool inventory, v54 contract catalog, v54 catalog/service/server source, unified 31-tool registry/server factory and Sandbox v54 provider source.
- Pinned exact source blob SHAs in the review artifact.
- Read-only connected Build MCP calls returned service label `room-hop-build` version `1.0`; structure reports eight Sandbox capabilities; Work listing returned 66 Work entries.
- These helper-call outputs are not raw protocol-level `tools/list`, do not include full schemas, and do not identify the exact Work 28 deployment process/build. No raw tools/list response or source-to-runtime attestation was available in the connected tool surface.

### FINDINGS
- **WP0-PROV-01 HIGH:** branch contains three incompatible registry generations: historical 18 legacy names, 54-tool v54 draft catalog and 31-tool unified registry. Names and schemas differ; no evidence selects one as the current deployed :8030 registry.
- **WP0-PROV-02 HIGH:** v54 and unified MCP server factories explicitly do not open listeners; source existence does not prove either factory is used by the running Build MCP.
- **WP0-PROV-03 MEDIUM:** current connected Build MCP reports eight capabilities, but this is not a raw MCP tools/list response and does not establish deployed source/build identity.
- **WP0-PROV-04 MEDIUM:** listing 66 Sandbox Works proves enumeration only, not Core authorization, Work mapping or isolation.
- **WP0-PROV-05 HIGH (WP3-F01):** reviewed 31-tool registry and v54 catalog/provider do not contain the approved binary upload capability/session contract; existing Sandbox write/append paths are text-oriented.

### DECISION / NEXT
- **WP0 = PARTIAL / BLOCKED; G0 remains OPEN.** No deployed :8030 provenance PASS or tools/list parity PASS is issued.
- Xu/Vi must identify the intended deployment and canonical registry version, then capture raw tools/list schemas + response digest and bind them to the exact running service/build identity.
- An must independently reproduce protocol-level discovery and schema digest against that identified target.
- Ka will re-review exact pinned deployment and registry evidence.
- Historical MCP :8020 remains DO NOT USE. No probe, restart or modification occurred. No tests were run; no code/runtime configuration changed; Execution Gate remains CLOSED.

**STATUS:** WP0 SOURCE INVENTORY PARTIAL / LIVE PROVENANCE BLOCKED / G0 OPEN / WORK NOT RELEASED.


## 2026-11-16 — JRN-W28-022 — GitHub App write and manual-dispatch verification

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0 — GitHub integration evidence  
**Repository / branch:** `hqtt2026-thevinhvtqni/room-meeting-ai` / `work/28-mcp-tooling-platform`

### READ / TRACE
- Re-read Work Manifest, Master Execution Plan V2.0, canonical journal and controlled document register before recording this checkpoint.
- GitHub App identity: App ID `5775206`; Installation ID `182362333`.
- User-executed installation-token test returned permissions: Actions=write, Contents=write, Pull Requests=read, Checks=read, Statuses=read, Metadata=read.
- Read-only API checks returned CONTENTS HTTP 200, PULL_REQUESTS HTTP 200 and ACTIONS HTTP 200.
- Isolated write probe used temporary branch `probe-work28-github-app-write-20261116` from base commit `3fea73071eed757dbde337f0d2be79d9fcd74745`. User terminal evidence: branch create PASS; temporary file create PASS; exact content readback PASS; file deletion PASS; branch deletion PASS.
- Manual dispatch API returned HTTP 204 for `.github/workflows/work28-mcp-tooling.yml` against `work/28-mcp-tooling-platform`.

### VERIFY — GITHUB ACTIONS RUN #347
- Initial local polling printed `WORKFLOW RUN: NOT FOUND`. This was a polling defect: `time.mktime(time.strptime(...))` interpreted GitHub's UTC `created_at` timestamp as local time, causing the candidate filter to reject the run.
- Independent GitHub Actions API lookup found Run #347 / ID `43773392184`, event `workflow_dispatch`, actor `room-hop-work28-integration[bot]`, branch `work/28-mcp-tooling-platform`, source commit `3fea73071eed757dbde337f0d2be79d9fcd74745`, conclusion SUCCESS.
- All five jobs completed SUCCESS: `unit-regression-tests`, `execution-host-lifecycle-linux`, `execution-host-lifecycle-windows`, `Build and retest exact-SHA Work 28 source artifact`, `automatic-e2e-gate-report`.
- Report artifact: ID `14185621545`, name `work28-auto-e2e-report-43773392184`, SHA-256 `1fd66ac8ee865e8971e65da12d6468e8cd5eabe5acedda52e6ef27df439166ad`.
- Source artifact: ID `14185636344`, name `work28-source-artifact-3fea73071eed757dbde337f0d2be79d9fcd74745`, SHA-256 `43cf21140e472c3fc54abbbfd99cfb6f2ce2bc0671d46471f5074af7f80e293b`.
- Read the automatic report job log. It explicitly sets CI preconditions PASS but deployed MCP → Core → Runtime E2E BLOCKED, overall status BLOCKED, Execution Gate CLOSED and Release NOT_RELEASED.

### BLOCKERS — NOT CLEARED BY GREEN CI
1. No verified live MCP 8030 build/process identity and raw `tools/list` parity artifact is wired to the workflow.
2. No trusted deployed Core principal / WorkContext authorization evidence is available to the runner.
3. No approved canonical Runtime MCP and Execution Host deployment/isolation attestation is wired to the workflow.
4. No complete deployed request-to-protected-evidence readback chain exists; local CI and mocks cannot substitute.
5. Existing WP0 provenance findings remain open; WP2 HIGH service lifecycle findings remain open; WP3 Q4 capability-grant remains NOT APPROVED per JRN-W28-019.

### DECISION / NEXT
- GitHub App authentication, repository read access, isolated Contents write/readback/delete, temporary branch cleanup and Actions manual dispatch are VERIFIED PASS for this probe.
- Workflow Run #347 and its five CI jobs are VERIFIED SUCCESS. The earlier NOT FOUND line is classified as a local timestamp-filter false negative, not a GitHub dispatch failure.
- Do not promote product E2E, Execution Gate or release status. Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
- Next priority: continue WP0 provenance reconciliation by identifying the actual deployed Build MCP :8030 process/build and obtaining raw protocol-level `tools/list` response plus full schema digest bound to that identity. Do not touch historical MCP :8020.
- Ka review and An independent verification must remain distinct; this checkpoint does not claim An acknowledgement or independent QA acceptance.

**STATUS:** GITHUB APP WRITE + DISPATCH PASS / CI RUN #347 SUCCESS / DEPLOYED PRODUCT E2E BLOCKED / NOT RELEASED.


## 2026-11-16 20:50 UTC+07:00 — JRN-W28-023 — GitHub canonical branch synchronization checkpoint

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0 — Source-of-truth and synchronization integrity  
**Repository / branch:** `hqtt2026-thevinhvtqni/room-meeting-ai` / `work/28-mcp-tooling-platform`

### READ / TRACE
- Re-read the canonical Work Manifest, official minutes register, current Work-wide journal and Work 28 README before any write.
- Confirmed the Manifest defines GitHub branch `work/28-mcp-tooling-platform` as the canonical source for code and controlled documents. MCP 8030 Sandbox is a supporting build/verification environment, not a competing source of truth.
- Confirmed the canonical branch exists and contains the Work 28 manifest, official minutes, master plan, architecture decision, document register, workflow, source, tests and journal.
- GitHub compare `main...work/28-mcp-tooling-platform` reports `diverged`, with 393 commits ahead and 1,173 behind; the compare response is capped at 300 changed files. This is a cross-branch divergence observation only, not proof that the Work 28 branch is missing its own canonical records.
- The current journal contains JRN-W28-022 recording GitHub App write/readback/delete verification and Actions run #347 SUCCESS. That run's report keeps deployed MCP → Core → Runtime E2E BLOCKED, Execution Gate CLOSED and release NOT_RELEASED.
- Sandbox inventory includes generated `__pycache__` artifacts and other implementation/evidence files. A blind bulk copy would not be a safe synchronization operation; each promoted artifact requires exact source, path, content and SHA reconciliation.

### DECISION
- Preserve `work/28-mcp-tooling-platform` as the canonical Work 28 branch.
- Do not merge `main` into Work 28, merge Work 28 into `main`, force-update refs, or bulk-copy Sandbox content. The observed divergence requires a separately reviewed integration plan and file-level conflict analysis.
- Do not treat Sandbox listing as proof of content parity. Do not promote generated bytecode/cache artifacts.
- Continue artifact-level synchronization only: reconcile the canonical GitHub path/blob SHA, transfer the exact approved artifact to the supporting Sandbox when needed, then verify byte/content parity. For source changes, GitHub remains first.
- Keep historical MCP :8020 quarantined and DO NOT USE.

### BUILD / VERIFY
- Appended this checkpoint to the canonical GitHub Work 28 journal.
- This is a GitHub journal synchronization/status record only. It does not claim that all Sandbox files are synchronized, that code was changed, or that a full Git branch merge/push occurred.
- The existing GitHub App write/readback/delete and Actions dispatch capability remains as recorded in JRN-W28-022; this entry does not independently rerun CI.

### BLOCKERS / NEXT
1. Continue WP0 live MCP :8030 provenance and raw protocol `tools/list` schema-digest binding.
2. Keep WP2 HIGH lifecycle findings open pending fixes and independent retest.
3. Keep WP3 Q4 capability-grant NOT APPROVED; no upload implementation promotion.
4. Plan any main-branch integration separately, with exact merge-base, changed-path inventory, conflict review and protected CI; do not use the raw 393/1,173 compare as a merge instruction.

**STATUS:** GITHUB CANONICAL JOURNAL UPDATED / FULL SANDBOX SYNC NOT CLAIMED / BRANCH MERGE NOT PERFORMED / WORK ACTIVE — INTEGRATION BLOCKED — NOT RELEASED / EXECUTION GATE CLOSED.


## 2026-11-16 — JRN-W28-024 — Canonical GitHub → Sandbox artifact synchronization batch

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Priority:** P0 — Canonical record and source synchronization

### READ / TRACE
- Re-read the Work Manifest and confirmed GitHub branch `work/28-mcp-tooling-platform` is canonical; Sandbox is a supporting verification/evidence copy.
- The Sandbox inventory showed stale canonical records and generated `__pycache__` artifacts. No cache/bytecode artifact was promoted or treated as source.
- Used GitHub Contents as source for each artifact below. For every transfer, readback was obtained through the Sandbox diagnostic read and compared by exact text equality.

### BUILD / VERIFY — EXACT READBACK
| Artifact | GitHub source blob SHA | Sandbox readback |
|---|---|---|
| `00_ROOT/WORK_MANIFEST.md` | `3aa82147c525f6c8b3befd726fb91d3489fc578d` | EXACT MATCH |
| `00_ROOT/BIEN_BAN.md` | `7130a0ed258baef8e57575b8baf1bbab39f570cf` | EXACT MATCH |
| `00_ROOT/WORK_STRUCTURE_STANDARD.md` | `69e082a9080e22b70b21d77539a31b5d15609948` | EXACT MATCH |
| `00_ROOT/WORK_DOCUMENT_REGISTER.md` | `c16008efe6ae2059f4dddb2c9c3d936d208ca7f3` | EXACT MATCH |
| `00_ROOT/NHAT_KY_THI_CONG.md` | `b62a42446502ec763a390936aa110ed40f615918` | EXACT MATCH; includes JRN-W28-023 |
| `01_PLAN/WORK28_MASTER_EXECUTION_PLAN_V2.0.md` | `bdc4f682a8fbff346357e2394c3c512176d85764` | EXACT MATCH |
| `03_ARCHITECTURE/WORK28_ARCHITECTURE_DECISION_V2.md` | `3720ee455e5bb8e07de1bc4b4756615506ed5799` | EXACT MATCH |
| `.github/workflows/work28-mcp-tooling.yml` | `aef70150c274ecb076bcb3e94c558892e3b52573` | EXACT MATCH |
| `04_CODE/execution_host/process_job.py` | `85f4866df7710aa2ad0fe1601ae319c470f1718a` | EXACT MATCH |
| `05_TEST/test_process_job_suspended_spawn.py` | `831691a44a56d8634a4b13243d664b21b47f64ae` | EXACT MATCH |

- Each Sandbox readback matched the GitHub source text exactly. No code was edited in this batch; this was a one-way canonical artifact sync.
- The journal itself is synchronized after this entry is committed, then read back and checked in Sandbox.

### LIMITATIONS / NOT CLAIMED
- This batch does not establish complete synchronization of every Work 28 file, binary artifacts, local PC checkout, or runtime deployment.
- Sandbox inventory contains additional historical/evidence/source files requiring file-by-file classification and SHA reconciliation. Generated caches are excluded.
- No pytest, CI, live MCP protocol test, runtime restart, or product E2E was run by this synchronization operation.
- Branch divergence from `main` is not resolved; no merge/rebase/force-push was performed.

**STATUS:** 10 CANONICAL / SELECTED ARTIFACTS GITHUB → SANDBOX EXACT-MATCH / FULL WORKSPACE SYNC STILL OPEN / WORK ACTIVE — INTEGRATION BLOCKED — NOT RELEASED / EXECUTION GATE CLOSED.


## 2026-11-18 — JRN-W28-027 — Ka independent security review of PR #61 (WP2 recovery)

**Người thực hiện:** Ka  
**Chức danh:** Chief Security Architect (CSA) — Independent Architecture/Security Reviewer  
**Execution time:** 2026-11-18 05:26 UTC+07:00  
**Priority:** P1 — WP2 process-tree cleanup integrity  
**Review target:** PR #61 — `auto/work28-vi-wp2-recovery-20261118`  
**PR HEAD reviewed:** `d6cf0763870eb860fe630e890bc0190ef3de9335`  
**Code commit under test:** `27ecdebc94a1ec177a899db8971ed4d76d7d2004`  
**CI evidence:** Actions run #357 SUCCESS; WP2 workflow run #19 SUCCESS.

### READ / TRACE
- Re-read the canonical Work Manifest, Master Execution Plan and Architecture Decision. Confirmed GitHub branch `work/28-mcp-tooling-platform` remains canonical; PR branch is isolated and is not merged.
- Confirmed the governance boundary: Core :8000 remains the sole authority; MCP :8030 is the supported Build/Verification lane; historical MCP :8020 remains quarantined and DO NOT USE; Execution Gate CLOSED; release NOT_RELEASED.
- Read PR #61 metadata, complete changed-file inventory, patch, `execution_host/host.py`, `execution_host/host_run.py`, `execution_host/process_job.py`, `execution_host/host_cleanup_bridge.py`, regression tests, Vi's security handoff and existing journal entries JRN-W28-025/026.
- PR #61 is OPEN and unmerged. PR HEAD is `d6cf076...`; code commit `27ecdeb...` is the commit named in the CI evidence. GitHub currently shows no submitted PR reviews, inline review threads or discussion comments.
- Actions run #357 and WP2 run #19 both report SUCCESS. This verifies CI execution only; Ka did not independently execute pytest or native Windows tests in this review.

### REVIEW — FINDINGS

**KA-W28-PR61-01 — HIGH / P1 — Legacy Popen cleanup can falsely attest process-tree cleanup**
- Location: `execution_host/host.py`, `_cleanup_service_entry()` legacy non-`ManagedProcess` branch and `service_status()` legacy branch.
- The fallback terminates/waits only for the raw Popen leader, then sets `process_reaped=True` when that leader exits. It does not inspect or drain descendants, and records only `legacy_unmanaged_process_cleanup`. `service_status()` also reports a dead raw Popen as STOPPED with `members=0` without membership proof.
- A surviving child can therefore outlive the registry entry while cleanup is reported PASS.
- Required remediation: fail closed for raw/unmanaged Popen entries unless process-tree membership can be independently proven and drained. Do not retrofit/claim Windows Job Object containment after spawn. Retain the registry handle and return BLOCKED when tree state is unknown.
- Required regression: raw Popen leader exits while child remains; verify stop/restart stays BLOCKED, handle is retained, and no replacement starts. Include unknown membership and native Windows behavior.

**KA-W28-PR61-02 — HIGH / P1 — POSIX process-membership probe converts inspection failure into zero members**
- Location: `execution_host/process_job.py`, `_posix_group_members()`, consumed by `ManagedProcess.members_count()` and `_drain_posix_group()`.
- The helper returns integer 0 on `OSError` or `subprocess.TimeoutExpired`. Callers interpret 0 as an empty process group: `_drain_posix_group()` returns drained=True, and `service_status()` can report a dead leader STOPPED. An unavailable or timed-out `ps` probe is indistinguishable from verified zero descendants.
- Although this helper predates PR #61, the recovery patch relies on its result to decide whether to release the service registry entry. It is therefore in the security-critical acceptance path.
- Required remediation: represent inspection failure as UNKNOWN (for example `None`), propagate UNKNOWN as BLOCKED, and never release the registry handle or spawn a replacement unless group emptiness is positively verified.
- Required regression: inject missing `ps`, timeout, non-zero exit and unusable output while a child remains; verify cleanup and status remain BLOCKED and registry ownership is retained.

**KA-W28-PR61-03 — MEDIUM / P2 — Concurrency regression does not cover start/stop interleavings**
- The new same-name concurrency test verifies multiple concurrent starts, but not concurrent start/stop/status interleavings or a cleanup exception racing a new start.
- Required additional regression: coordinate same-name start and stop threads with barriers/fault injection; assert one registry owner, no orphan process, no replacement before verified cleanup, and stable BLOCKED recovery. Repeat on Linux and Windows.

### POSITIVE REVIEW NOTES
- The RLock around inspect → cleanup → spawn → register and around stop/status is a sound direction for same-instance registry serialization.
- Failed ManagedProcess cleanup retains the registry object and sets a BLOCKED marker; restart retries cleanup instead of spawning over uncertain state.
- Suspended-spawn abort evidence preserves the supplied `process_reaped` boolean and avoids manufacturing `no_process` when abort is unconfirmed.
- Runtime identity is expanded before service-specific `pid` fields, avoiding the reported PID-key collision in the inspected response paths.
- `readiness=NOT_CHECKED` correctly avoids treating process existence as application readiness.

### DECISION / REQUIRED NEXT
- **PR #61: NOT APPROVED — REQUEST CHANGES.** GitHub rejected a formal REQUEST_CHANGES review because the connected GitHub identity is also the PR author; the findings are recorded as a PR conversation comment and in this canonical journal.
- The two HIGH findings block acceptance of the WP2 recovery slice until fixed and retested on the exact updated PR head.
- Vi remains BUILD OWNER and may autonomously remediate within the isolated PR branch. No merge, force-push, production deployment, Core mutation, listener restart or Execution Gate opening is authorized by this review.
- An's independent QA remains a separate required gate; CI results do not substitute for An's acknowledgement/reproduction.
- Auto E2E remains BLOCKED pending verified live MCP :8030 process/build identity and raw `tools/list` name/schema parity evidence. PC G1–G4 remain NOT RUN.
- Preserve Execution Gate CLOSED and release NOT_RELEASED.

**STATUS:** SOURCE REVIEW COMPLETE / NOT APPROVED — REQUEST CHANGES / 2 HIGH + 1 MEDIUM FINDINGS / AN INDEPENDENT QA PENDING / LIVE E2E BLOCKED / EXECUTION GATE CLOSED / NOT RELEASED.

**Signature:** [KÝ: KA | CSA — INDEPENDENT REVIEWER]


## 2026-11-19 — JRN-W28-028 — Xu GitHub verification and continuation handoff for PR #61 / WP2 recovery

**Người thực hiện:** Xu — Work coordinator / acceptance control  
**Scope:** Read-only verification of PR #61, its feature branch, workflow evidence, review comments and Windows retest handoff; canonical journal append only.  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**PR:** #61 — `Work 28: recover WP2 service registry cleanup and abort evidence`  
**Feature branch:** `auto/work28-vi-wp2-recovery-20261118`

### READ / TRACE — GitHub state at this checkpoint
- Read the canonical Work 28 journal on `work/28-mcp-tooling-platform`; source blob before this append: `88d5a746ac60a5d02af56cc661983ed7ffa5c672`. The latest entry present in this canonical journal readback was JRN-W28-027. PR-side references to later Vi remediation notes were not treated as proof that those notes had already been appended to this canonical journal.
- Read PR #61 and confirmed: state OPEN; merged=false; mergeable=false; head SHA `1455283d99d647aae45462149bcf5f02372ee4ea`; base branch `work/28-mcp-tooling-platform`; base SHA `8301a7f8fb6a91689482710a9006e2cdbab709c4`. Feature branch HEAD independently read back as the same `1455283d99d647aae45462149bcf5f02372ee4ea`.
- Read PR comments/reviews:
  - Ka comment `6962882614`: NOT APPROVED / REQUEST CHANGES against earlier reviewed HEAD `d6cf0763870eb860fe630e890bc0190ef3de9335`; two HIGH/P1 findings (legacy raw Popen cleanup could falsely attest tree cleanup; POSIX membership probe could convert inspection failure to zero members) and one MEDIUM/P2 concurrency interleaving gap.
  - An formal review `5947789771`: CHANGES_REQUESTED against the same earlier HEAD; independently identified the POSIX fail-open cleanup evidence issue and requested native Linux retest.
  - Vi comment `6963584185`: reports isolated Windows retest on exact source SHA `1455283d99d647aae45462149bcf5f02372ee4ea`, PowerShell/Python 3.12.9; compileall PASS; test_process_job 18 tests with 1 POSIX-only skip; service mapping/race 17 passed; suspended-spawn 17 passed; total 52 passed, 1 skipped. This is a developer-reported PC transcript handoff, not an independent execution by Xu or An.
- Queried GitHub Actions workflow runs on the feature branch:
  - Runs #357 and WP2 #19: SUCCESS on code SHA `27ecdebc94a1ec177a899db8971ed4d76d7d2004`.
  - Runs #358 and WP2 #20: SUCCESS on documentation/handoff SHA `d6cf0763870eb860fe630e890bc0190ef3de9335`.
  - No listed workflow run was associated with latest code SHA `1455283d99d647aae45462149bcf5f02372ee4ea` at this check.
- Inspected selected PR patches for POSIX membership fault handling, process-job regression tests, suspended-spawn abort evidence and this journal path. The diff includes tri-state UNKNOWN handling and fail-closed tests; static patch inspection is not runtime proof.

### ANALYZE
- The two HIGH findings have corresponding source-level remediation in the latest PR branch, and the Windows focused test results are reported by Vi. However, the latest code SHA has no matching GitHub Actions run in the queried run list, and the Windows transcript is not an independent QA result.
- Earlier green CI runs do not transfer to the latest code SHA. Run #358 / WP2 #20 tested the documentation/handoff SHA, not the current feature head.
- Ka's and An's REQUEST CHANGES decisions remain the latest independent review dispositions visible in PR comments. No later APPROVED review or independent retest evidence was found in the inspected PR comments.
- PR remains OPEN, unmerged and mergeable=false. Do not infer merge readiness from a green workflow on an earlier SHA or from source patch presence.

### DECIDE
- Keep PR #61 OPEN and **DO NOT MERGE**.
- Preserve Work 28 status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.
- Do not deploy, restart listeners, mutate Core, change branch refs, force-push, or interact with the quarantined historical MCP :8020 listener.
- Continue the approved four-AI boundary: Vi = implementation owner; An = independent QA; Ka = independent security/architecture review; Xu = coordination and acceptance control.

### NEXT — execution order
1. **Vi:** trigger/obtain Linux + Windows CI for the exact latest feature code SHA `1455283d99d647aae45462149bcf5f02372ee4ea` (or a later final code SHA if source changes); record run IDs, tested SHA, jobs and raw logs. Do not claim the existing #357/#358 runs as evidence for this latest SHA.
2. **An:** independently retest the exact final code SHA, prioritizing POSIX OSError/timeout/non-zero/malformed probe cases, surviving descendants, legacy raw Popen registry retention/no replacement, and start/stop/status interleavings. Record environment, commands, raw output and untested areas. If independent execution is unavailable, record BLOCKED / NOT RUN rather than PASS.
3. **Ka:** re-review the exact final code SHA and confirm each HIGH/MEDIUM finding is closed with source and test evidence; retain REQUEST CHANGES if any acceptance condition remains unresolved.
4. **Xu:** reconcile exact-SHA CI, An QA and Ka review; update this canonical journal before any merge decision. Merge remains prohibited until all required gates pass.

### STATUS
**GITHUB PR/BRANCH READBACK PASS / PATCH-LEVEL REMEDIATION OBSERVED / WINDOWS FOCUSED TESTS REPORTED BY VI (NOT INDEPENDENT) / LATEST-HEAD CI NOT VERIFIED / AN RETEST PENDING / KA APPROVAL PENDING / PR OPEN — DO NOT MERGE / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | WORK COORDINATOR]


## 2026-11-19 — JRN-W28-030 — Vi tiếp tục sau đánh giá Xu: tạo exact-SHA CI trigger handoff

**Người thực hiện:** Vi  
**Chức danh:** CODER / Implementation Lead  
**Execution time:** 2026-11-19 20:14 UTC+07:00  
**PR:** #61 — WP2 recovery  
**Feature branch:** `auto/work28-vi-wp2-recovery-20261118`

### READ / TRACE
- Re-read Xu's JRN-W28-028 on canonical branch and confirmed required sequence: exact-SHA CI → An independent retest → Ka independent review → Xu acceptance.
- Re-read PR #61 metadata and branch ref. Before this action, PR was OPEN, unmerged, head `1455283d99d647aae45462149bcf5f02372ee4ea`, base `8301a7f8fb6a91689482710a9006e2cdbab709c4`.
- Confirmed the workflow file declares `pull_request` and path filter `work/28/**`, and includes Linux/Windows lifecycle jobs, full Work 28 regression, immutable artifact and Auto E2E gate report.

### BUILD — DOCUMENTATION-ONLY TRIGGER
- Created `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/VI_EXACT_SHA_CI_TRIGGER_HANDOFF_20261119.md` on the isolated PR branch.
- Commit: `46888f44b4913ed371c89cddd4ebce9a737a39e8`.
- The commit is documentation-only; no product source, canonical base branch, Core, runtime or listener was changed.
- PR and feature branch readback both confirm new head `46888f44b4913ed371c89cddd4ebce9a737a39e8`; base remains `8301a7f8fb6a91689482710a9006e2cdbab709c4`.

### VERIFY
- Queried PR-triggered workflow runs for the new SHA: empty result.
- Queried GitHub Checks API for the new SHA: `total_count=0`.
- Queried commit status: `state=pending`, `total_count=0`.
- Therefore the documentation commit was created and read back, but CI has **NOT RUN / NOT VERIFIED**. Do not claim this triggered a successful workflow. A manual workflow dispatch or authorized Actions UI action is still required.

### HANDOFF
- An: independently retest the latest code-bearing commit `1455283d99d647aae45462149bcf5f02372ee4ea` (the new head differs only by documentation); record BLOCKED / NOT RUN if no runner.
- Ka: re-review the same code-bearing commit and disposition two HIGH + one MEDIUM.
- Xu: reconcile the evidence; no merge until all gates pass.
- PR conversation updated with the new documentation commit and explicit no-CI result.

### SAFETY / STATUS
PR #61 remains OPEN / UNMERGED. No deployment, Core mutation, listener restart or activity against quarantined MCP :8020. Execution Gate CLOSED; release NOT_RELEASED.

**STATUS:** DOC-ONLY HANDOFF COMMITTED / PR HEAD READBACK PASS / CI NOT RUN — MANUAL DISPATCH REQUIRED / AN RETEST PENDING / KA APPROVAL PENDING / DO NOT MERGE.

**Signature:** [KÝ: VI | CODER]


## 2026-11-21 17:05 UTC+7 — JRN-W28-031 — Ka rà soát Issue / PR / push tồn đọng toàn repository

**Name:** Ka / AI-02  
**Title:** CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner (delegated)  
**Date-Time:** 2026-11-21 16:28 +07:00  
**Priority:** P1  
**Read order:** 31  
**Reference:** RA-W28-20261121-001 — ROOM-WIDE GITHUB ISSUE / PR / PUSH RECONCILIATION

### READ / TRACE
- Kiểm kê open Issues, open PRs, branches và recent commits của `hqtt2026-thevinhvtqni/room-meeting-ai`.
- 22 Issues mở; 16 Issues được tạo trước 2026-11-01.
- 30 PR mở; 10 PR không được cập nhật kể từ trước 2026-11-01.
- Đối chiếu branch với main và với branch canonical của Work 15, 28, 33, 51, 76, 98.
- Đọc Work28 manifest/journal, Work51 sync status, Work98 manifest/preview config, Work15 WORK.md, Work200 manifest và nội dung các Issue liên quan.

### FINDINGS
- Nhiều PR cũ đã DIVERGED với main trên 1,000 commit; không có căn cứ merge/rebase hàng loạt.
- W28 vẫn execution gate CLOSED; MCP :8020 historical listener QUARANTINED / DO NOT USE; PR #61 có test candidate evidence nhưng PC/live E2E, An QA, Ka review còn pending.
- W98 source transfer staged; build/E2E/live NOT VERIFIED; preview MOCK/BLOCKED.
- W51 remains NOT DONE; sync record exists but independent QA/security/key-management gates remain.
- W15 remains PHASE 0; PR #18 contains backend candidate but branch divergence 1/1 requires review.
- W200 remains ACTIVE / PLAN-BUILD-VERIFY incomplete; Sandbox-only; AI cannot commit/push; live trading out of scope.
- Core Issue #3: methods exist on main, but explicit get_transcript not-found regression coverage was not found in inspected test file.

### ACTIONS EXECUTED
- CLOSED PR #53: PR #55 explicitly replaces this prototype and preserves it as audit evidence.
- CLOSED PR #35: current Work33 branch is 11 commits ahead, PR branch 0 ahead; no unique commits.
- CLOSED PR #43: current Work51 branch is 72 commits ahead, PR branch 0 ahead; no unique commits.
- CLOSED PR #7: stale Work98 branch contains generated .output/, node_modules/, .gitbundle and old workflow; current Work98 branch remains canonical source-transfer lane. No commits merged.
- All four PR branches retained; no branch deletion, merge, rebase, force-push or main mutation.
- All other old PRs with unique code/evidence or unresolved review gates remain open; no bulk closure.

### RESULT / STATUS
- **PASS:** inventory and branch comparisons recorded; four stale PRs safely closed and readback status verified by GitHub mutation responses.
- **BLOCKED / PENDING:** remaining Issue and PR gates require owner review, exact-head CI, independent QA/security review or runtime evidence.
- **NO MERGE / NO RELEASE:** preserved.
- Work 28 status unchanged: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; execution gate CLOSED.

**Signature:** Ka / AI-02 — CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner.


## 2026-11-21 16:28 UTC+7 — JRN-W28-032 — Ka follow-up P0 / stale Issue triage

**Name:** Ka / AI-02  
**Title:** CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner (delegated)  
**Date-Time:** 2026-11-21 16:28 +07:00  
**Priority:** P1  
**Read order:** 32  
**Reference:** RA-W28-20261121-001, Section 7.

### Additional issue dispositions
- Issue #39: retained as historical append-only Work32 CI log; historical 188/188 pilot runs are not current Work32 acceptance.
- Issue #44 / PR #45: P0 remains OPEN; PR #45 is only audit-truthfulness correction, branch 2 ahead / 1,111 behind main, zero formal review/thread; no trusted Manus session authentication or Work99 binding; no merge.
- Issue #56: W300 TS2345 diagnostic remains tied to exact SHA `cffe439a919bbee5f181cdfa1d16f832ecf5e9de`; no matching canonical Work300 source branch found in this repo snapshot; OPEN / BLOCKED.
- Issue #57: explicit REJECT / BLOCKED for current bounded Work32 execution proposal; protected execution DENIED; no implementation/test/runner/PC/PR mutation permission; Cla response absent, no ACK inferred.
- Issue #58: PR #60 remains active W76 v2 draft; dispatch transport/target receipt/authenticated ACK, runtime/PC E2E and canonical QE remain blocked/pending.

### Result
- **PASS:** comments and current dispositions recorded for the additional long-standing/P0 tickets.
- **BLOCKED:** all protected execution and product acceptance gates remain controlled by their respective Work owners.
- **NO MERGE / NO RELEASE:** unchanged.

**Signature:** Ka / AI-02 — CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner.
