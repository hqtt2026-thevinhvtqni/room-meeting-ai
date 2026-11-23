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
- 32 PR mở; 10 PR không được cập nhật kể từ trước 2026-11-01 (đã đối soát lại danh sách 32 PR trước khi đóng 4 PR).
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


## 2026-11-21 — JRN-W28-033 — Ka cập nhật kết quả xử lý Issue/PR tồn đọng

**Name:** Ka / AI-02  
**Title:** CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner (delegated)  
**Date-Time:** 2026-11-21; exact time not returned by GitHub connector (UTC+07)  
**Priority:** P1  
**Read order:** 33  
**Reference:** RA-W28-20261121-001, Section 8.

### READ / TRACE
- Đọc lại canonical main, các Issue #3/#44/#56/#57, PR #2/#45/#61, branch refs, source files, PR reviews và exact-SHA CI/status.
- Đối chiếu Work300 diagnostic với đúng source path trong Work300; kiểm tra commit sửa lỗi và toàn bộ steps của CI run #43682996529.
- Đối chiếu PR #45 với current main; kiểm tra PR #61 đúng head SHA và test fault-injection theo phản biện An.

### ACTIONS EXECUTED
- **Issue #56 CLOSED / COMPLETED:** xác minh fix commit `d07307c459a8fc44afaee7be40d4732823da3497`, follow-up CI run #43682996529 SUCCESS (TypeScript, ESLint, unit tests, production build); thêm comment bằng chứng trước khi đóng.
- **PR #45 COMMENT review:** xác nhận narrow correction source-level đúng, nhưng main vẫn còn auth_verified=true; PR stale 2 ahead / 1,139 behind, zero checks. P0 Issue #44 vẫn OPEN; Cla implementation, Go QE/QA, Ka review, Xu coordination theo owner split ghi trên Issue.
- **PR #61 COMMENT review:** xác nhận An HIGH POSIX probe failure remediation đã có source/test; exact head zero checks, 24 ahead / 12 behind Work28, DIVERGED/mergeable=false. No approval.
- **Issue #3 / PR #2:** ghi nhận APIs đã hiện diện trên main và một phần tests, nhưng empty/single list + transcript not-found focused cases chưa được chứng minh; PR #2 stale 11 ahead / 1,774 behind, giữ OPEN/DRAFT.
- **Issue #44:** bổ sung review follow-up, không nâng trạng thái P0; session authentication và Work99 binding vẫn chưa hoàn tất.
- **Issue #57:** giữ REJECT / BLOCKED; không thực hiện protected execution.
- Cập nhật RA-W28-20261121-001 Section 8; giữ nguyên các bản ghi lịch sử trước đó.

### RESULT / STATUS
- **PASS:** W300 TS2345 diagnostic đã được xác minh sửa và đóng đúng phạm vi.
- **COMMENT / BLOCKED:** PR #45, PR #61 và PR #2 còn các gate nêu trên; không có approval.
- **OPEN:** Issue #3, #44, #57 và các Work tương ứng vẫn theo dõi.
- **NO MERGE / NO RELEASE:** không merge, rebase, force-push, xóa branch, sửa main, deploy hoặc mở Execution Gate.

**Signature:** Ka / AI-02 — CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner.


## 2026-11-21 — JRN-W28-034 — Ka rà soát W76 PR #60 exact-head

**Name:** Ka / AI-02  
**Title:** CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner (delegated)  
**Date-Time:** 2026-11-21; exact time not returned by GitHub connector (UTC+07)  
**Priority:** P1  
**Read order:** 34  
**Reference:** RA-W28-20261121-001, Section 9; Issue #58; PR #60.

### READ / TRACE
- Đọc Issue #58 và PR #60, kiểm tra branch head/base, formal reviews và exact-SHA checks.
- Đối chiếu exact head `d524ca56003518fd339572570612fd6f33e3269f` với current main `97fdd719e8468e0eca667f49fdc28f9ff5c66eff`.

### FINDINGS / ACTIONS
- PR #60 là W76 v2 draft, supersedes PR #59; PR #55 giữ vai trò baseline lịch sử.
- Exact-SHA CI: pytest Python 3.11 PASS; pytest Python 3.12 PASS.
- Branch DIVERGED: 228 ahead / 355 behind main. PR DRAFT; chưa có formal review.
- WP-76-07 vẫn BLOCKED vì chưa có transport, target identity, receipt và authenticated ACK.
- Ka tạo formal COMMENT review trên PR #60 và cập nhật Issue #58; không APPROVE.
- Cập nhật RA-W28-20261121-001 Section 9; không merge/rebase, không chuyển lifecycle gate, không release.

### RESULT
- **PASS:** exact-head CI evidence được xác nhận.
- **BLOCKED:** integration, WP-07 dispatch, canonical QE, review và branch reconciliation.
- **NO MERGE / NO RELEASE:** giữ nguyên.

**Signature:** Ka / AI-02 — CSA / ROOM-WIDE GitHub + Sandbox Reconciliation Owner.


## 2026-11-22 — JRN-W28-035 — Xu tiếp quản Work 28 và lập phương án tích hợp sạch WP2

**Người thực hiện:** Xu — Coordinator / technical decision owner  
**Authority:** Vinh (ủy quyền tạm thời tiếp quản, không yêu cầu Vinh thao tác PC hoặc giao việc AI trong giai đoạn này)  
**Scope:** GitHub source-of-truth reconciliation, WP2 PR #61 recovery, CI evidence review and safe integration preparation.  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Canonical journal source blob before append:** `f7a5d6b9ac76bdc6faa3573d92cd7471477e670a`

### READ / TRACE — current verified state
- Re-read WORK_MANIFEST, Master Execution Plan V2.0, Architecture Decision V2 and the canonical Work journal. Manifest confirms exactly four approved Work 28 AI roles (Xu, Vi, Ka, An); Co is excluded. Vinh has now temporarily delegated coordination and technical execution to Xu while unavailable.
- Canonical branch HEAD at this checkpoint: `cc7dd01ec75e89bfec8c91010e0976589aef76dc`.
- PR #61 current head: `46888f44b4913ed371c89cddd4ebce9a737a39e8`; code-bearing remediation source checkpoint: `1455283d99d647aae45462149bcf5f02372ee4ea`; PR base was originally `8301a7f8fb6a91689482710a9006e2cdbab709c4`.
- GitHub compare against current canonical branch confirms PR #61 is DIVERGED: 24 commits ahead / 16 commits behind; mergeable=false; OPEN / UNMERGED. Do not merge or rewrite the shared feature branch.
- PR #61 has 10 changed paths: workflow, execution_host/host.py, host_run.py, process_job.py, two test files, canonical journal and three evidence/handoff files. Source-level review confirms the patch adds service registry locking, fail-closed legacy Popen handling, structured spawn failure, POSIX UNKNOWN membership handling, abort evidence preservation and WP2 lifecycle regression tests.
- Formal review state: An's CHANGES_REQUESTED review targets older head `d6cf0763870eb860fe630e890bc0190ef3de9335`; Ka's latest formal review is COMMENTED (not APPROVED) on current PR head `46888f44b4913ed371c89cddd4ebce9a737a39e8`. Ka observes source/test-level remediation of An's POSIX finding but explicitly keeps PR acceptance BLOCKED. No current An independent re-test approval was found.
- GitHub Actions run `44892829201` on canonical source SHA `cc7dd01ec75e89bfec8c91010e0976589aef76dc`: jobs `execution-host-lifecycle-linux`, `execution-host-lifecycle-windows`, `unit-regression-tests`, `Build and retest exact-SHA Work 28 source artifact`, and `automatic-e2e-gate-report` all SUCCESS. This is evidence for canonical SHA `cc7dd01...`, not PR #61 remediation SHA `1455283...` or PR head `46888...`. The E2E report job's SUCCESS is not equivalent to live deployed MCP/Core E2E PASS; PR body still records live E2E BLOCKED.
- PR #61 head `46888...` has no PR-triggered workflow run and zero commit statuses at this checkpoint. Do not transfer historical CI results to it.
- Master Plan V2.0 still marks G1–G6 NOT VERIFIED and G7 CLOSED; Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

### ANALYZE
- PR #61 contains valuable WP2 remediation, but merging it as-is would import a divergent history and outdated journal/evidence snapshots. Direct merge, rebase or force-push is not a safe autonomous action.
- The canonical branch already has a verified CI baseline at `cc7dd...`; it is the correct base for an isolated integration candidate.
- File-level transplant of only the six WP2 implementation/test/workflow files onto a fresh branch from the current canonical HEAD is safer and reviewable than merging the divergent PR history. Preserve the existing PR #61 and its branch as immutable historical evidence.
- Xu cannot truthfully provide independent An QA or Ka approval while acting as sole active executor. Such gates must remain PENDING / NOT VERIFIED. Xu may perform additional source review and CI orchestration, clearly labeled as coordinator self-check, not independent approval.

### DECIDE
- Xu accepts temporary coordination and implementation control within the existing Work 28 scope.
- Keep canonical branch protected from unreviewed product-source changes; prepare an isolated candidate branch from the latest canonical HEAD.
- Do not merge/close PR #61, rebase or force-push its branch, alter main, deploy, mutate Core, restart listeners, or interact with the quarantined historical MCP :8020 listener.
- Preserve Core :8000 as sole authorization authority, Build/Verification MCP :8030 as supported lane, and Execution Host :8031 as the only approved execution boundary.
- No release or Execution Gate opening without required evidence and Vinh's authority where specified.

### BUILD / NEXT ACTIONS
1. Create isolated branch `xu/work28-wp2-integration-20261122` from the current canonical branch after this journal append.
2. Transplant only these reviewed PR #61 paths: `execution_host/host.py`, `execution_host/host_run.py`, `execution_host/process_job.py`, `tests/test_process_job.py`, `tests/test_wp2_service_mapping_and_race.py`, `.github/workflows/work28-mcp-tooling.yml`. Do not copy the feature branch's stale journal or handoff files over canonical records.
3. Read back every changed file and compare candidate to source. Inspect test assumptions and the Windows pre-execution Job Object containment path against the Master Plan before treating the candidate as ready.
4. Open a new draft integration PR against `work/28-mcp-tooling-platform`; require exact-head Linux + Windows + full regression CI. Keep PR #61 open as historical remediation source until the candidate's results are understood.
5. Continue source-level WP0–WP7 inventory after WP2 candidate CI; prioritize WP3 :8030 provenance and safe I/O, then clean Runtime MCP, Core authority and full E2E.
6. Append a new journal checkpoint after each completed write/run/readback. Never mark PASS without exact run and evidence.

### STATUS
**XU TEMPORARY TAKEOVER ACKNOWLEDGED / CANONICAL BASELINE CI PASS ON SHA cc7dd01... / PR #61 SOURCE REMEDIATION OBSERVED BUT DIVERGED 24 AHEAD–16 BEHIND / PR #61 EXACT-HEAD CI NOT RUN / AN INDEPENDENT QA PENDING / KA APPROVAL NOT GRANTED / CLEAN WP2 INTEGRATION CANDIDATE TO BE PREPARED / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 — JRN-W28-036 — Xu tích hợp WP2 candidate, sửa POSIX probe và xác minh exact-head CI

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Integration branch:** `xu/work28-wp2-integration-20261122`  
**Draft PR:** #69 — `https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/69`  
**Canonical journal source blob before append:** `d3d05dc96103a4bdec3a27e336a1020cdb61cb46`

### BUILD — clean integration candidate
- Created integration branch from canonical commit `8179c8af90c19c36a15e4eeeef67c691f9d0839a`; no history from divergent PR #61 was merged/rebased.
- Transplanted only six WP2 code/test/workflow files from PR #61: `execution_host/host.py`, `execution_host/host_run.py`, `execution_host/process_job.py`, `tests/test_process_job.py`, `tests/test_wp2_service_mapping_and_race.py`, `.github/workflows/work28-mcp-tooling.yml`.
- GitHub compare before Xu's POSIX fix: 6 commits ahead / 0 behind. After fix: 8 commits ahead / 0 behind; six intended paths only.
- Opened PR #69 as DRAFT. PR #61 remains OPEN and unchanged as the historical source branch. No merge or deployment.

### RUN / DEBUG — exact first attempt
- PR #69 initial head `91417f7d993457ea43cd133efab489298c25b6a3`; workflow run `44976860569`.
- Windows lifecycle PASS; Linux lifecycle FAIL (5 tests); full unit regression later PASS.
- Exact Linux failure evidence: `_posix_group_members()` used `ps -o pid=,pgid=,stat= -g <pgid>`. On an empty process group, the command may exit non-zero, and the fail-closed parser correctly returned UNKNOWN; this made legitimate empty-group cleanup unverifiable. This was a probe-command semantics defect, not grounds to weaken fail-closed behavior.

### BUILD — Xu POSIX probe correction
- Changed the probe to execute a successful full process-table snapshot `ps -o pid=,pgid=,stat=` and filter rows by the requested PGID in Python. A verified snapshot with no matching live members now returns 0; OSError, timeout, non-zero exit and malformed output remain UNKNOWN.
- Replaced the empty-group unit case with a regression proving that a group is empty even while unrelated process groups remain active; asserted the exact ps invocation.
- Source commit: `cd348175f4f33c02bc5c7e254b74177ef442b217`; test commit / candidate head: `f02084e1ada2e193aa798ee3f91452f55bef402b`.
- Read back both files on the candidate branch and verified the updated source/test content.

### VERIFY — GitHub Actions run #44976943948
**PR head SHA:** `f02084e1ada2e193aa798ee3f91452f55bef402b`  
**PR merge-ref/source snapshot used by workflow report:** `0ccad176010b3f719292a762cfa02b7e2ba81f2e`  
**Run URL:** `https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44976943948`

| Job | Result | Evidence |
|---|---|---|
| execution-host-lifecycle-linux | PASS | 18 unittest cases; 13 passed + 4 skipped in suspended-spawn pytest suite; WP2 service suite 17 passed; additional contract/security suites passed |
| execution-host-lifecycle-windows | PASS | 18 unittest cases; suspended-spawn 17 passed; WP2 service suite 17 passed; additional contract/security suites passed |
| unit-regression-tests | PASS | 348 passed; 238 subtests passed; compile step PASS |
| immutable-source-artifact | PASS | exact-SHA source archive built and extracted/retested successfully |
| automatic-e2e-gate-report | Job PASS; product E2E BLOCKED | report artifact uploaded; report says CI preconditions PASS, deployed MCP/Core/Runtime E2E BLOCKED |

- Artifacts: `work28-auto-e2e-report-44976943948` (artifact ID `14736282057`); `work28-source-artifact-0ccad176010b3f719292a762cfa02b7e2ba81f2e` (artifact ID `14736013612`).
- CI report explicitly records blockers: no verified live Build MCP process/build identity and tools/list parity artifact; no trusted deployed Core principal/WorkContext authorization evidence; no approved deployed Runtime MCP and Execution Host/isolation attestation; no complete deployed request-to-protected-evidence readback chain.
- Therefore the workflow is green for source/CI/artifact preconditions only. It does not establish live E2E, independent QA/security approval, or product acceptance.

### WP0 — Sandbox provenance spot-check
- ROOM-HOP Build service read-only identity response: `service=room-hop-build`, `version=1.0`; returned room structure did not include a process ID, source commit, build hash or deployed artifact digest.
- Sandbox Work `28` exists. Diagnostic readback via the proven probe confirmed exact content equality with canonical GitHub for `WORK_MANIFEST.md` and `WORK28_MASTER_EXECUTION_PLAN_V2.0.md`.
- Sandbox canonical journal content does not match the current GitHub journal and does not contain JRN-W28-035; Sandbox journal snapshot is stale. No Sandbox write/sync was attempted.
- Sandbox listing includes older implementation/evidence snapshot paths; no source-to-runtime provenance or registry parity is inferred from directory presence. Historical quarantined service/code is not used.
- This confirms Sandbox is available for supporting read/verification, but the current live build identity and complete source-to-runtime correspondence remain NOT VERIFIED.

### ANALYZE / DECIDE
- WP2 source candidate now passes the currently configured native Linux/Windows lifecycle jobs, full Work 28 regression, and immutable source-artifact build/retest on the PR head/merge snapshot.
- Keep PR #69 DRAFT and do not merge: independent An QA is not available in this temporary single-agent execution period; Ka's current COMMENTED review on PR #61 is not an approval of PR #69; live deployment/E2E remains BLOCKED.
- PR #61 remains DIVERGED and must not be merged or rewritten.
- Keep Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED; `ISOLATION_STATUS=NOT_VERIFIED`.

### NEXT
1. Continue Xu source-level review of WP2 and exact-head evidence; inspect workflow and source for any missing cases not covered by CI.
2. Reconcile PR #69 base with any later canonical-branch movement before requesting merge; keep it a draft until independent review/QA gates are satisfied.
3. Continue WP0 provenance inventory, especially live Build MCP process/build identity and tools/list schema parity. Use read-only probes; do not infer from Sandbox files.
4. Advance WP3 binary upload only after mapping the existing Sandbox provider contract, authorization path, size limits, streaming behavior, checksum and readback. Do not claim implementation from the plan alone.
5. Then trace clean Runtime MCP, Core :8000 authority and the :8031 execution boundary. No live execution/deployment until the authorized boundary and evidence chain are verified.

### STATUS
**WP2 CANDIDATE EXACT-HEAD CI PASS / LINUX POSIX EMPTY-GROUP PROBE FIXED / WINDOWS LIFECYCLE PASS / FULL REGRESSION 348 PASS + 238 SUBTESTS PASS / IMMUTABLE ARTIFACT PASS / LIVE MCP-CORE-RUNTIME E2E BLOCKED / SANDBOX JOURNAL STALE / AN INDEPENDENT QA NOT AVAILABLE / KA APPROVAL NOT GRANTED FOR PR #69 / PR #69 DRAFT — DO NOT MERGE / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 — JRN-W28-038 — Xu exact-head CI confirmation and WP3-F01 Q4 design revision

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**PR #69 latest tested head:** `449b8ef7cfbc9f0af6d8cfd09564b48269eb9ab4`

### VERIFY — third PR #69 workflow
- GitHub Actions run `44977448394` completed SUCCESS for PR #69 head `449b8ef7cfbc9f0af6d8cfd09564b48269eb9ab4`.
- Jobs SUCCESS: `execution-host-lifecycle-linux`, `execution-host-lifecycle-windows`, `unit-regression-tests`, `Build and retest exact-SHA Work 28 source artifact`, `automatic-e2e-gate-report`.
- The workflow report source snapshot is merge commit `04f01597ef38f6744c59cd7efce5c5da8b202961`; run head remains the PR head above.
- E2E report artifact `work28-auto-e2e-report-44977448394` (ID `14735219634`); immutable source artifact `work28-source-artifact-04f01597ef38f6744c59cd7efce5c5da8b202961` (ID `14736193860`).
- Automatic E2E report remains `overall_status=BLOCKED` because deployed Build MCP identity/tools-list parity, trusted Core principal/WorkContext evidence, approved deployed Runtime MCP + Execution Host/isolation attestation and the complete deployed request-to-evidence readback chain are not wired. Green CI jobs are not live E2E acceptance.

### READ / ANALYZE — WP3-F01 Q4
- Re-read `sandbox_tools_v1.py`, `mcp8020_sandbox_tools_v54.py`, `mcp_tool_registration_v1.py`, the existing Vi binary-upload source trace, Xu's Q1–Q3 decision record and Ka's Q4 review.
- Confirmed no binary upload implementation or registration: current v1/v54 paths accept UTF-8 text; v1 write is bounded to 64 KiB; v54 read decodes UTF-8; no begin/chunk/finalize upload session exists.
- Ka's review requires concrete grant binding, path scope, quotas, TTL, revocation, replay/idempotency, atomic state transitions, durable audit and failure cleanup. Q4 remains NOT APPROVED; implementation is not authorized.
- Xu prepared the proposed design revision `XU-W28-WP3-F01-Q4-DESIGN-20261122-001` in `06_EVIDENCE/XU_WP3_F01_Q4_GRANT_DESIGN_REVISION_20261122.md`. It specifies a Core-issued least-privilege grant, trusted principal/session binding, canonical Work mapping/version, operation and path scope, immutable quota ceilings, begin/chunk/finalize/abort state machine, atomic reservation/idempotency/revocation, no-overwrite promotion, independent readback and durable audit.
- The design explicitly remains PROPOSED / NOT APPROVED. It does not invent a Core endpoint, authorize implementation or replace Ka's independent review.

### DECIDE / NEXT
- Keep PR #69 DRAFT / DO NOT MERGE pending independent An QA and Ka approval. Do not claim Xu's self-check as independent review.
- Submit the Q4 design revision for future Ka review when delegation is available. Until then, no WP3-F01 code, registration, staging or filesystem side effect.
- Continue WP0 live provenance and WP4/WP5 source-to-runtime tracing. Current connector readback does not provide a deployed process ID/source SHA/build digest; issue #33 remains open for runtime provenance.
- Keep Work status ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

### STATUS
**PR #69 EXACT-HEAD CI RUN #44977448394 PASS / LIVE DEPLOYED E2E BLOCKED / WP2 INDEPENDENT QA AND SECURITY APPROVAL PENDING / WP3-F01 Q4 DESIGN REVISION PREPARED BUT NOT APPROVED / IMPLEMENTATION BLOCKED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 — JRN-W28-039 — Xu kiểm chứng WP1/WP4/WP5 và ổn định CI trigger

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Canonical branch before commit:** `work/28-mcp-tooling-platform`  
**Latest candidate PR head tested:** `b788355b045e2937f97cbb7b24d29d45961416a2`

### VERIFY — PR #69 exact-head CI
- GitHub Actions run `44977854122` completed SUCCESS on PR head `b788355b045e2937f97cbb7b24d29d45961416a2`.
- Jobs SUCCESS: Linux lifecycle, Windows lifecycle, full unit/regression, immutable exact-SHA source artifact, automatic E2E gate report job.
- The immutable source snapshot used by the workflow report is merge commit `1ef8fa8e4c5c456c69d01293a9db9bb423bbcbf0`.
- Artifacts: `work28-source-artifact-1ef8fa8e4c5c456c69d01293a9db9bb423bbcbf0` (ID `14737010217`); `work28-auto-e2e-report-44977854122` (ID `14736541469`).
- E2E report remains BLOCKED for deployed MCP/Core/Runtime identity, trusted Core WorkContext, approved Execution Host/isolation attestation and full request-to-protected-evidence readback. CI success is not live product acceptance.

### CI trigger correction
- During branch synchronization, an intermediate workflow edit produced invalid YAML at commit `d6b868f0356292e3e963c301c0f253ab68d5e624`; push run `44977828182` failed before creating jobs. This was caught by reading back the workflow, not treated as a product test result.
- Corrected path-filter syntax in commit `b788355b045e2937f97cbb7b24d29d45961416a2`; GitHub then created PR workflow run `44977854122`, which passed all configured CI jobs.
- Updated canonical workflow to trigger source CI on Work 28 executable code/test paths, root execution/Core/runtime code, requirements and the workflow itself. Journal, evidence and plan-only edits no longer trigger the full code CI. This preserves exact-source test evidence while avoiding repeated full runs for append-only journal updates.
- The same scoped filter is present on the candidate branch and was exercised by run `44977854122`.

### WP1 — source-side registry inventory
- `mcp8020_catalog_v54.py` contains 54 ToolSpec entries: 24 marked IMPLEMENTED and 30 marked NOT_IMPLEMENTED. The 24 marked implemented are room and Sandbox file/metadata operations; the 30 not implemented include seven execution/evidence operations and the computer/browser tool family.
- `mcp8020_unified_registry_v1.py` defines a separate 31-name prepared registry and explicitly says it does not prove live registration.
- `mcp_tool_registration_v1.py` defines a third v1 registration surface: 13 required tools plus up to 2 optional discovery tools, with injected providers.
- No current live deployed tools/list capture tied to a verified process/build identity proves which registry is authoritative or that schemas/handlers match. These are source-side contracts, not runtime parity evidence.
- **G1 remains NOT VERIFIED** until one canonical registry/version is declared and exact deployed tools/list parity is proven.

### WP4 — Runtime MCP / Execution Gateway
- `runtime_tools_v1.py` is an adapter-only layer; it calls an injected Core function and does not execute processes.
- `mcp8020_w13_core_client_v1.py` explicitly says STAGED / NOT WIRED; its run registry is in-memory and cancel is BLOCKED at the synchronous bridge boundary.
- `mcp8020_w13_execute_envelope_v1.py` validates inputs then explicitly refuses with `W13_SAFE_SERVER_SIDE_ENTRYPOINT_ADAPTER_NOT_IMPLEMENTED`; it does not manufacture a legacy envelope.
- `mcp8020_execution_gateway_v54.py` is protocol-complete but deliberately unwired; its default client returns BLOCKED.
- No clean deployed Runtime MCP identity, source/build digest, health/readiness or live contract evidence was found. **G4 remains NOT VERIFIED.**

### WP5 — Core authority
- `mcp8020_core_authority_authorizer_v1.py` explicitly states STAGED / NOT WIRED into MCP registration or the v54 catalog.
- `mcp8020_core_execution_session_v1.py` is also staged/not wired; local tests of its candidate do not prove deployed Core authorization.
- The v1 RuntimeTools adapter requires an injected authenticated Core transport, but no deployed trusted principal/WorkContext route evidence is attached to the current E2E workflow.
- Issue #26 remains OPEN and records the missing live authenticated MCP → Core → Execution Host → evidence chain. **G5 remains NOT VERIFIED.**

### DECIDE
- Keep G1, G4 and G5 NOT VERIFIED; do not promote status from source presence or local CI.
- Keep WP3-F01 implementation blocked until Ka independently approves the revised Q4 grant design. The design record is PROPOSED only.
- Keep PR #69 DRAFT and do not merge while An independent QA and Ka approval are unavailable.
- Work remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED.

### NEXT
1. Complete the exact-head PR #69 workflow after canonical workflow synchronization; retain the candidate branch as a reviewable integration slice.
2. Continue WP0 deployed Build MCP process/build identity and tools/list provenance; reconcile the service identity returned by the supporting connector with the deployed build evidence without assuming they are the same service.
3. Resolve the single authoritative registry/version and prove tools/list/schema/handler parity.
4. Keep Runtime MCP and Core integration blocked until an approved server-side route, trusted principal/WorkContext and safe W13 entrypoint adapter are evidenced.
5. Await independent review/QA before WP2 acceptance or WP3 implementation.

### STATUS
**PR #69 EXACT-HEAD CI RUN #44977854122 PASS / WORKFLOW PATH FILTER CORRECTED / WP1 REGISTRY PARITY NOT VERIFIED / WP4 RUNTIME NOT VERIFIED / WP5 CORE AUTHORITY NOT VERIFIED / WP3-F01 Q4 PROPOSED NOT APPROVED / LIVE E2E BLOCKED / PR DRAFT — DO NOT MERGE / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 — JRN-W28-040 — Xu xác nhận CI trên canonical và WP2 candidate cuối phiên

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Canonical branch before append:** `work/28-mcp-tooling-platform` at `3530ff847fa51d6b00f374c6a106fe07750e6a6e`  
**Integration branch:** `xu/work28-wp2-integration-20261122`  
**PR:** #69 (DRAFT) — current tested head `3497957827f332774fc34d7dec45ab7cb4e5ccd7`

### VERIFY — canonical branch CI
- Push workflow run `44978021033` completed SUCCESS on canonical commit `3530ff847fa51d6b00f374c6a106fe07750e6a6e`.
- All jobs SUCCESS: unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA source artifact and automatic E2E gate report job.
- Source artifact: `work28-source-artifact-3530ff847fa51d6b00f374c6a106fe07750e6a6e` (ID `14736208154`); E2E report artifact `work28-auto-e2e-report-44978021033` (ID `14736033759`).
- The report remains BLOCKED for deployed MCP/Core/Runtime E2E; no live product acceptance is inferred.

### VERIFY — PR #69 latest candidate CI
- PR workflow run `44978067896` completed SUCCESS on PR head `3497957827f332774fc34d7dec45ab7cb4e5ccd7`.
- All jobs SUCCESS: `execution-host-lifecycle-linux`, `execution-host-lifecycle-windows`, `unit-regression-tests`, `Build and retest exact-SHA Work 28 source artifact`, `automatic-e2e-gate-report`.
- Full Work 28 pytest evidence: 348 passed; 238 subtests passed. The Linux and Windows lifecycle jobs passed on the same PR head.
- Source artifact: `work28-source-artifact-960fc8b8c402fd5532ddf9ea6f3bfe2b4feedc70` (ID `14736695764`); E2E report artifact `work28-auto-e2e-report-44978067896` (ID `14736935801`).
- E2E report source snapshot is merge commit `960fc8b8c402fd5532ddf9ea6f3bfe2b4feedc70`; run head remains PR commit `349795...`.
- The automatic report again says deployed MCP/Core/Runtime E2E BLOCKED, despite CI preconditions PASS.

### PR / branch state
- PR #69 is DRAFT / OPEN / UNMERGED. GitHub compare: 13 commits ahead / 0 behind; mergeable=true; six product/workflow paths changed.
- PR #61 remains OPEN and divergent; it is retained as historical remediation source and is not merged or rewritten.
- CI path filters now scope Work 28 local CI to executable code/test paths plus root execution/Core/runtime, requirements and the workflow. Append-only journal/evidence/plan changes do not trigger the full code CI.
- The candidate workflow retains the WP2 service-registry regression suite and the corrected POSIX full-process-table probe.

### ACCEPTANCE STATUS
- WP2: candidate source has exact-head Linux/Windows lifecycle and full regression CI PASS. It is **not accepted** because An independent QA and Ka security approval are unavailable during Vinh's temporary absence; Xu self-review is not independent sign-off.
- WP0: Sandbox manifest and master plan matched GitHub on diagnostic readback, but Sandbox journal is stale and live Build MCP process/build provenance + deployed tools/list parity remain NOT VERIFIED.
- WP1: source catalogs/registries remain unreconciled to one proven live registry; G1 NOT VERIFIED.
- WP3-F01: binary upload absent in current v1/v54 adapters; Q4 design revision is PROPOSED / NOT APPROVED; implementation remains BLOCKED.
- WP4/WP5: W13 adapter, execution gateway and Core authorizer remain staged/unwired; trusted deployed Core WorkContext and clean Runtime MCP identity are not evidenced.
- WP6/WP7: automatic CI report job passes as a report generator, but deployed request-to-protected-evidence E2E is BLOCKED; Execution Gate CLOSED; NOT RELEASED.

### NEXT
1. Keep PR #69 DRAFT and do not merge until An QA and Ka review can be independently obtained.
2. Continue source/provenance work that does not require live deployment, Core mutation or production execution.
3. Preserve the revised WP3 Q4 grant design as PROPOSED until independent Ka approval.
4. When Vinh is available, request the independent An/Ka gates; no acknowledgement or assignment is fabricated during this temporary takeover.

### STATUS
**CANONICAL CI RUN #44978021033 PASS / PR #69 EXACT-HEAD CI RUN #44978067896 PASS / WP2 TECHNICAL CI VERIFIED / INDEPENDENT QA AND SECURITY APPROVAL PENDING / WP0–WP1–WP3–WP5–WP6–WP7 REMAIN NOT VERIFIED OR BLOCKED AS ABOVE / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 14:42–14:47 UTC+07 — JRN-W28-041 — Xu tiếp tục takeover: đối soát đường chạy pytest Sandbox và cổng E2E

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Source baseline read:** `3530ff847fa51d6b00f374c6a106fe07750e6a6e` (đã đối chiếu các tài liệu canonical; không sửa code trong checkpoint này).

### READ — tài liệu chuẩn đã mở lại trực tiếp
1. `01_PLAN/WORK28_MASTER_EXECUTION_PLAN_V2.0.md` — xác nhận Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED; Execution Gate CLOSED; Core :8000 là authority duy nhất; Build MCP :8030 là kênh build/verification; Execution Host :8031 là ranh giới thực thi duy nhất; historical listener :8020 bị quarantine / DO NOT USE.
2. `01_PLAN/WORK28_AUTO_E2E_RUNBOOK_V2.0.md` — pipeline chuẩn DISCOVER → AUTHORIZE → SNAPSHOT → HASH → DISPATCH → COLLECT → VERIFY → PERSIST → READBACK → REPORT; CI preconditions không được đánh đồng với deployed E2E.
3. `01_PLAN/PLAN_WORK28_CONTINUATION_V1.0.md` — WP0 yêu cầu raw tools/list có timestamp, names, schemas và deployed process/build provenance; WP2 giữ BlockedExecutionClient cho tới khi route Core, identity và isolation được chứng minh.
4. `05_TEST/WORK_28_TEST_PLAN.md` trên Sandbox Work 28 được đọc bằng diagnostic read probe. Nội dung xác nhận canonical command là `python -m unittest discover -s 05_TEST -t . -v`; tài liệu tự ghi rõ chưa có approved-runner execution. G3 approved-runner, G4 auth/path/isolation và G5 live E2E vẫn BLOCKED.

### TRACE — thao tác và bằng chứng trong checkpoint
- Method: mở lại trực tiếp GitHub canonical files qua GitHub connector; gọi MCP 8030 diagnostic `sandbox_read_probe(work_id="28", relative_path="MCP-8020-TOOLING-PLATFORM/05_TEST/WORK_28_TEST_PLAN.md")`.
- Probe response: `status=ok`, đúng `work_id=28`, đúng path; trả về nguyên nội dung test plan và `size_bytes=5009`.
- MCP tool surface được cung cấp trong phiên có Sandbox read/list/create/write/append/delete và các thao tác context/meeting; không thấy action Python/pytest execution hoặc command execution trong danh sách tool khả dụng. Không gửi lệnh thực thi thay thế, không chạy trên môi trường khác để giả danh Sandbox.
- Issue #26 được đọc lại: còn OPEN; yêu cầu authenticated MCP 8030 → Core 8000 → Execution Host 8031, pytest fixture thật trong Sandbox, negative tests, exact source hash và protected evidence readback. Đây là yêu cầu nghiệm thu chưa được chứng minh, không phải giấy phép bypass.
- PR #69 vẫn DRAFT / OPEN / UNMERGED; PR #61 vẫn OPEN và divergent. Không sửa/merge PR #61.

### ANALYZE / DECIDE
- **PASS:** đọc lại canonical plan/runbook và Sandbox test plan thành công; xác nhận đúng test command và tình trạng gate trong tài liệu.
- **BLOCKED:** actual pytest execution inside Sandbox — thiếu authorized Python/pytest execution action trong MCP tool surface hiện khả dụng. Không có run_id/exit code/test output thật nên tuyệt đối không ghi pytest PASS.
- **NOT VERIFIED:** live MCP process/build identity và raw deployed tools/list parity; probe file read không chứng minh service process identity hay registry parity.
- Giữ Execution Gate CLOSED; không wire tool execution, không thay đổi Core, không deploy/restart listener, không gọi historical :8020.
- Giữ WP2 PR #69 ở DRAFT cho tới khi independent An QA và Ka security review có evidence riêng. Không tự ký thay hai vai trò độc lập.

### NEXT
1. Tiếp tục rà source-side registry/provider và mapping catalog → registered handler → schema/test, ghi rõ design-only / registered / callable / blocked.
2. Thu thập được raw deployed `tools/list` và process/build provenance chỉ khi có kênh quan sát đúng service; không suy từ tool catalog của connector.
3. Khi authorized RUN_TESTS route được expose qua Core → canonical runtime → Execution Host, chạy đúng command trong Sandbox và lưu run_id, exit code, stdout/stderr, test counts, source SHA và cleanup evidence.
4. Chỉ mở các gate tương ứng khi có evidence độc lập; không hạ tiêu chuẩn nghiệm thu để tăng tiến độ.

### STATUS
**CANONICAL PLAN/RUNBOOK READBACK PASS / SANDBOX TEST-PLAN PROBE PASS / SANDBOX PYTEST EXECUTION BLOCKED — NOT RUN / DEPLOYED TOOLS-LIST + BUILD PROVENANCE NOT VERIFIED / LIVE E2E BLOCKED / PR #69 DRAFT / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 14:47–14:52 UTC+07 — JRN-W28-042 — WP1 source-contract reconciliation: 54 catalog vs 31 unified server registry vs 13 registration adapter

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Scope:** Source-only READ / TRACE / ANALYZE. No runtime listener started, no product code changed.

### READ — exact source files and Git blob SHA
| File | Blob SHA | What source declares |
|---|---|---|
| `04_CODE/mcp8020_catalog_v54.py` | `e51251f33ca8beb0d181cc8abdcb95875101faf1` | `CATALOG_VERSION=54.0.0-draft1`; 54 ToolSpec design entries |
| `04_CODE/mcp8020_unified_registry_v1.py` | `b3b975c7ccc16d76595bdb6fa695a088639a4e2c` | `CONTRACT_VERSION=1.0.0`; 31 expected names = 18 legacy + 3 GitHub + 10 extensions |
| `04_CODE/mcp_tool_registration_v1.py` | `b9f306c9e4765117af517be578139faabe8bab01` | 13 required v1 handlers; optional discovery adds 2 |
| `04_CODE/mcp8020_unified_server_v1.py` | `65ab9cd41da231c97e5094cb6fab0a6b9c3c84cb` | Local MCP Server factory imports the 31-name unified registry and maps names to injected providers |
| `05_TEST/test_mcp8020_unified_server_stdio_contract_v1.py` | `35dbef31e061d7ae15fb060c38888e3538118b58` | Real stdio subprocess test compares names and schemas against the 31-name registry |

### TRACE — concrete inconsistencies
1. The v54 catalog and v1 unified registry are distinct inventories with different names, groupings, schema shapes and contract versions. They are not one registry merely because both exist in the same Work.
2. The v1 server factory imports `TOOL_SPECS` from `mcp8020_unified_registry_v1.py`, not the v54 catalog.
3. The separate `mcp_tool_registration_v1.py` registers 13 required methods (+2 optional discovery) and does not itself import or validate the v54 54-tool catalog.
4. The stdio test uses an `InertProvider` whose dynamic handler returns `{"accepted": true}`, but the test only calls `session.list_tools()`; it compares the 31 names and schemas and does not invoke tool handlers. Its own docstring correctly scopes it to transport/schema contract only.
5. The server factory docstring says it does not open a listener. The v1 code therefore does not establish a deployed service or live :8030 registry. The current architecture also quarantines historical :8020; this source must not be used as authority to activate that listener.

### ANALYZE
- There are at least three source-side registry/registration surfaces: 54 design catalog entries, 31 unified server entries and 13 required v1 registration adapter methods (+2 optional discovery).
- The 31-tool stdio test is valid evidence for local MCP transport and schema publication against its own registry only; it is not proof of parity with the v54 catalog, real provider execution, Core authorization, or deployed runtime.
- A 54/31/13 count comparison alone cannot decide which surface is authoritative. Names, schemas, handler mapping, provider boundary, contract version and deployment identity must be reconciled together.
- Contract version evidence is currently split: catalog draft `54.0.0-draft1`, unified registry `1.0.0`; the registration module does not declare a single global contract version. No approval evidence authorizing silent version unification was found in this source pass.

### DECIDE
- **G1 remains NOT VERIFIED.** Do not select or rewrite a canonical registry in code without the approved architecture decision and independent Ka review.
- Preserve the v54 catalog as a design artifact; preserve v1 registry/server factory as a separate contract/test surface until formally reconciled.
- Do not call the 31-tool test a 54-tool parity test or a live tools/list capture.
- No activation/probe of quarantined historical :8020; no live traffic, deployment or execution.

### NEXT
1. Trace which server factory/registration module is actually used by the approved clean deployment source and exact process/build identity.
2. Build a name-by-name matrix for v54 ↔ v1 registry ↔ registration adapter ↔ actual provider methods ↔ tests; mark absent/duplicate/renamed/schema mismatch.
3. Prepare a decision brief for Ka only after source mapping is complete; do not claim Ka approval.
4. Keep G1 NOT VERIFIED until raw deployed tools/list + schemas and source/build identity are linked.

### STATUS
**SOURCE READBACK PASS / 54-vs-31-vs-13 REGISTRY SURFACES CONFIRMED / LOCAL 31-TOOL STDIO TEST SCOPE LIMITED TO LIST+SCHEMA / LIVE REGISTRY PARITY NOT VERIFIED / G1 NOT VERIFIED / NO CODE OR RUNTIME CHANGE.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-22 14:55–15:05 UTC+07 — JRN-W28-043 — WP1 trace provider composition: hai server contract chưa có bằng chứng nối với nhau

**Người thực hiện:** Xu — temporary Work 28 coordinator / technical execution owner  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Phạm vi:** READ / TRACE / ANALYZE source-only; không sửa code, không khởi động listener, không gọi runtime.

### READ — source và blob SHA
| File | Blob SHA | Kết quả đọc |
|---|---|---|
| `04_CODE/mcp_tool_registration_v1.py` | `b9f306c9e4765117af517be578139faabe8bab01` | Đăng ký 13 required handlers từ RuntimeToolsV1, SandboxToolsV1, GitHubToolsV1; DiscoveryToolsV1 bổ sung tối đa 2 capability tools |
| `04_CODE/mcp8020_unified_server_v1.py` | `65ab9cd41da231c97e5094cb6fab0a6b9c3c84cb` | Server factory độc lập đọc 31 ToolSpec từ unified registry và resolve handler qua sáu provider boundary |
| `04_CODE/mcp8020_unified_registry_v1.py` | `b3b975c7ccc16d76595bdb6fa695a088639a4e2c` | 31 tool names, mỗi ToolSpec có boundary + handler + input schema |
| `04_CODE/runtime_tools_v1.py` | `5bba7ffc83ad9f28a9a2e64566f713b56c09b0df` | RuntimeToolsV1 cung cấp execution_submit/status/output_read; Core call được inject |
| `04_CODE/sandbox_tools_v1.py` | `6682a4812b199dc1d1384d5eee28866c9b7ba459` | SandboxToolsV1 cung cấp search/stat/read_range/write qua injected provider |
| `04_CODE/github_tools_v1.py` | `c0a29e4a9f27144ed31e59bf4c535bad88506861` | GitHubToolsV1 cung cấp repository/read/search/create_branch/create_file/update_file |
| `04_CODE/discovery_tools_v1.py` | `fc18ac1a3ef9d1b91024597423b7307f631fbcba` | DiscoveryToolsV1 cung cấp capability_discover và capability_check |

### TRACE — phát hiện cụ thể
1. Registration adapter v1 đăng ký trực tiếp 13 tên: `execution_submit`, `execution_status`, `execution_output_read`, `sandbox_search`, `sandbox_stat`, `sandbox_read_range`, `sandbox_write`, `github_repository`, `github_read_file`, `github_search_files`, `github_create_branch`, `github_create_file`, `github_update_file`. Discovery có thể thêm `capability_discover` và `capability_check`.
2. Unified server factory không gọi `register_work28_tools()`; nó tạo server riêng, lấy 31 ToolSpec và resolve handler theo các provider boundary `core`, `sandbox`, `sandbox_extensions`, `proposals`, `github`, `runtime`. Thiếu bất kỳ handler nào thì fail-closed ngay khi tạo server.
3. Hai cơ chế có interface provider khác nhau: adapter v1 dùng các class RuntimeToolsV1/SandboxToolsV1/GitHubToolsV1/DiscoveryToolsV1; factory 31-tool yêu cầu sáu provider object khác và method names được khai báo trong registry. Chưa tìm thấy trong các file đã đọc bằng chứng call-site khởi tạo hai cơ chế, adapter bridge, hoặc startup wiring nối chúng.
4. Có khác biệt tên/schema có ý nghĩa, không chỉ khác số lượng: registration adapter gọi `sandbox_write` với signature provider của SandboxToolsV1; unified registry đồng thời có `sandbox_write` trong legacy set và `sandbox_write_verified` trong extension set; v54 catalog dùng các tên `room_*` và schema khác với legacy names như `get_room_context`/`list_meetings`. Không được suy ra chúng tương đương chỉ vì chức năng gần nhau.
5. Các provider v1 hiện là lớp adapter nhận dependency qua constructor; sự tồn tại của class/method không chứng minh provider triển khai thật đã được inject hoặc server đang chạy. Factory 31-tool cũng chỉ là factory; docstring xác nhận nó không mở listener.
6. PR #69 vừa được đọc lại: OPEN, DRAFT; GitHub hiện trả `mergeable=false`. Không merge. Trạng thái này không thay thế việc xác định nguyên nhân mergeable false; cần đọc metadata/checks/diff riêng trước khi kết luận conflict hay trạng thái khác.

### ANALYZE / DECIDE
- **PASS:** đã trace được hai composition pattern khác nhau và các provider class/method v1 trên source branch; blob SHA được ghi để tái lập.
- **BLOCKED:** chưa xác định entrypoint/server factory nào được host/deployment sử dụng; chưa có call-site wiring, deployed process/build identity hoặc raw live tools/list. Do đó chưa thể xác nhận 13+2 hay 31 là registry runtime thực tế.
- **NOT VERIFIED:** parity 54 ↔ 31 ↔ 13+2; handler/provider invocation thực tế; Core trusted context; deployed MCP identity.
- Không chọn registry chuẩn, không đổi schema/tên tool, không gộp adapter, không kích hoạt factory/listener trong checkpoint này.
- Giữ G1 NOT VERIFIED, Execution Gate CLOSED, PR #69 DRAFT/OPEN/UNMERGED, Work 28 NOT RELEASED.

### NEXT — tháo gỡ có thứ tự
1. Trace toàn repo các import/call-site của `register_work28_tools`, `create_work28_server`, `FastMCP`/MCP host startup; xác định entrypoint nào được workflow/deployment tham chiếu.
2. Đối chiếu provider boundary và handler method của 31 ToolSpec với provider class thực tế; không dùng tên gần giống làm bằng chứng.
3. Lập matrix theo từng tool: v54 name/schema/status ↔ v1 registry name/schema/boundary/handler ↔ adapter registration ↔ concrete provider method ↔ test assertion ↔ deployment call-site. Đánh dấu EXACT / RENAMED / SCHEMA_DRIFT / NO_HANDLER / DESIGN_ONLY / UNKNOWN.
4. Chỉ sau matrix mới lập decision brief cho Ka; mọi đề xuất thay đổi registry phải có lựa chọn tương thích ngược và kế hoạch migration, không tự ý áp dụng.
5. Đọc PR #69 metadata/checks/diff để xác định mergeable=false, nhưng giữ draft và không merge khi chưa có independent An QA + Ka security review.

### STATUS
**PROVIDER SOURCE TRACE PARTIAL PASS / TWO SERVER COMPOSITION PATTERNS IDENTIFIED / STARTUP CALL-SITE NOT FOUND IN FILES INSPECTED / REGISTRY PARITY NOT VERIFIED / G1 NOT VERIFIED / PR #69 DRAFT OPEN UNMERGED (mergeable=false) / EXECUTION GATE CLOSED / NOT RELEASED.**

**Signature:** [KÝ: XU | TEMPORARY WORK COORDINATOR]


## 2026-11-23 01:19 UTC+07:00 — JRN-W28-044 — Vinh delegates autonomous Auto E2E build through owner handoff

**Role:** Vi | CODER — implementation and integration owner  
**Authority:** Explicit user delegation in chat, 2026-11-23 01:19 UTC+07:00  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Reconciled canonical Work 28 branch HEAD: `dd60e22b5b660daa58d6a17061722e01f6c5c3d2`.
- Re-read the canonical Auto E2E runbook V2.0, Work journal through JRN-W28-043, WP3-F01 decision record and WP2 security findings.
- PR #61 is a historical candidate: OPEN, mergeable=false, 24 commits ahead / 24 behind the current canonical branch. Its latest head `46888f44b4913ed371c89cddd4ebce9a737a39e8` has no associated PR workflow run or commit status in the current query. It will not be merged or used as the integration base.
- PR #69 is the newer WP2 recovery candidate: DRAFT/OPEN, head `3fba64aa4e322a5eac5c7f57e69582ab40e70005`, based on `786aa5f3396b4a61e1d21845a9be5293805d710f`. GitHub reports mergeable=true/clean against its recorded base; the current canonical branch has advanced three journal-only commits since that base.
- Auto E2E run `44978228957` on PR #69 head completed SUCCESS: unit/regression, Linux lifecycle, Windows lifecycle, immutable source artifact and Auto E2E report jobs all succeeded. Source artifact and machine report artifacts were retained. The earlier code-bearing run `44978067896` is also recorded in PR #69 as SUCCESS.
- The Auto E2E workflow report contract explicitly keeps deployed MCP → Core → Runtime E2E BLOCKED, Execution Gate CLOSED and release NOT_RELEASED until live identity, authorization, runtime and protected-evidence readback are proven.
- JRN-W28-043 identifies unresolved WP1 G1: two distinct server composition patterns (13+2 adapter handlers vs 31-tool unified registry) have not been traced to an actual startup entrypoint/deployed process. Live registry parity is NOT VERIFIED.
- WP3-F01 Q4 Core capability-grant semantics remain NOT APPROVED in the canonical decision record. The existing decision explicitly prohibits implementation/side effects until the grant contract is approved. This is a mandatory authorization boundary, not an optional peer-review preference.

### DELEGATION / EXECUTION POLICY
- Vinh delegates Vi to continue autonomously through READ → TRACE → ANALYZE → DECIDE → BUILD/FIX → VERIFY → HANDOFF, without waiting for optional An/Ka review or routine chat approvals.
- Vi will perform and document its own code, security-boundary, regression and acceptance checks. No independent An/Ka approval will be claimed.
- Preserve canonical branch and Co's existing work. Use a fresh feature branch from the latest canonical HEAD for code integration; do not rewrite the user's dirty PC checkout.
- No changes to MAIN, no production deployment, no listener restart, no Core mutation, and no interaction with quarantined historical MCP :8020.
- Mandatory authorization decisions remain fail-closed: WP3 binary upload/capability grant cannot be activated or implemented beyond non-side-effecting contract/tests until Q4 is approved by its decision authority. No bypass based on this delegation.
- Acceptance must distinguish CI/source verification from live deployed E2E. Do not open Execution Gate or mark release PASS while live identity, trusted Core WorkContext, runtime attestation, OS isolation and protected evidence/readback remain unproven.

### INITIAL EXECUTION STATE
- WP2 recovery candidate: source/test changes present on PR #69; CI exact-PR-head run SUCCESS, but candidate must be rebased/reapplied onto the latest canonical tip and retested before integration.
- WP1 provider composition and registry parity: OPEN / NOT VERIFIED; next source-trace target.
- WP3-F01: contract partially decided; Q4 authorization grant BLOCKED; no upload implementation/activation.
- Live MCP 8030 → Core 8000 → Runtime MCP → Execution Host 8031: BLOCKED / NOT VERIFIED.
- PR #61: historical, do not merge.
- PR #69: candidate source only; do not merge until latest-canonical integration and exact-SHA retest.
- Work: ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate: CLOSED.

### NEXT
1. Create a fresh Vi integration branch from the canonical branch tip after this journal commit.
2. Port only the six WP2 source/test/workflow paths from the verified PR #69 candidate; preserve the current canonical journal and unrelated WP1 work.
3. Run exact-SHA Auto E2E on the new branch through a PR; fix all failures.
4. Continue WP1 source call-site/provider composition trace and create a registry matrix with exact blob evidence.
5. Reassess WP3 only within the approved Core authorization boundary; record the exact blocker and decision owner.
6. Produce a single owner handoff with commits, workflow runs, artifacts, tests, known gaps and rollback instructions.

**STATUS:** AUTONOMOUS EXECUTION AUTHORIZED / WP2 CANDIDATE CI PASS BUT NOT YET INTEGRATED ON CURRENT CANONICAL TIP / WP1 G1 NOT VERIFIED / WP3 Q4 BLOCKED / LIVE E2E BLOCKED / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 01:35 UTC+07:00 — JRN-W28-045 — WP2 recovery integrated on canonical branch after exact-SHA Auto E2E

**Role:** Vi | CODER — implementation and integration owner  
**Signature:** [KÝ: VI | CODER]

### BUILD / INTEGRATION
- Created clean feature branch `vi/work28-auto-e2e-integration-20261123` from canonical journal commit `ab40590cebd557a41bf739ae1bebb9b088d5186c`.
- Ported exactly six WP2 paths from the newer PR #69 candidate without copying its stale journal or overwriting the three newer canonical journal-only commits.
- Opened PR #70 against the latest canonical baseline. PR head tested: `42d9c43ec4dbd573b1dad5318cfa0bf10433eab0`.
- GitHub Actions Auto E2E run `45054861801` (run #387) completed **SUCCESS** on the exact PR head. All five jobs succeeded:
  1. `unit-regression-tests`
  2. `execution-host-lifecycle-linux`
  3. `execution-host-lifecycle-windows`
  4. `immutable-source-artifact`
  5. `automatic-e2e-gate-report`
- Artifacts retained:
  - Source artifact ID `14767445570`, archive digest `sha256:dc1743f85d42e9c026f02620412480a429d5babd4a54baebb5de3e8a9b025d90`.
  - Auto E2E report artifact ID `14766786821`, ZIP digest `sha256:518c03ccbe6f6f8d204950e5ae82e538b72f96497aa95c7de819d9381f1160d2`.
- Merged PR #70 after exact-head CI success using expected head SHA. Merge commit: `2d006dcb5aaac5624d45cf88b173bf59d0dce55a`.
- Verified canonical branch `work/28-mcp-tooling-platform` now points to the merge commit and all six code/test/workflow blobs exactly match the tested PR candidate:
  - workflow `8876f1a9096ec54e5a78a073820755087e67ecbf`
  - `execution_host/host.py` `0ee65126549c86caeb65fb0662b046d394fa8a03`
  - `execution_host/host_run.py` `63bb92fe9e8f179a2f6ae4783f05c65bc841fd0d`
  - `execution_host/process_job.py` `a8f56a2487dae72cc14a28926037943243907db3`
  - `tests/test_process_job.py` `3be6003844a0a1f32dfb3308b7e1ef60f0a14d5b`
  - `tests/test_wp2_service_mapping_and_race.py` `0e0d0f313df9d96bc0a87523b703130dc2f8bfe1`

### VERIFY / LIMITATIONS
- **PASS:** exact PR-head Auto E2E CI, Linux lifecycle, Windows lifecycle, immutable source artifact retest and machine report job.
- **PASS:** post-merge canonical branch identity and exact six-file blob parity with the tested PR head.
- No separate push-triggered workflow run or commit status was returned for merge commit `2d006dcb...`; the verified test run is explicitly tied to pre-merge source SHA `42d9c43...`, whose six changed blobs are unchanged in the merge commit.
- The machine report job's contract keeps deployed MCP → Core → Runtime E2E BLOCKED; this is not live product acceptance.
- No claim is made for live MCP 8030 process/build identity, raw tools/list parity, trusted Core WorkContext, Runtime/Execution Host deployment identity, OS isolation, protected evidence persistence or checksum readback.
- No production listener was restarted; no Core state was mutated; historical MCP :8020 remains DO NOT USE.

### STATUS / NEXT
- WP2 service lifecycle recovery: **INTEGRATED / EXACT-SHA CI PASS** on canonical branch.
- WP1 G1 registry/runtime provenance: **NOT VERIFIED**; JRN-W28-043 provider-composition discrepancy remains open.
- WP3-F01 Q4 upload capability grant: **NOT APPROVED** per Ka's review and Xu's 2026-11-22 revised proposal; no upload implementation or side effects are authorized until decision owner approves the exact contract.
- Live deployed product E2E: **BLOCKED**. Execution Gate: **CLOSED**. Release: **NOT_RELEASED**.
- Continue WP1 startup call-site/provider composition trace, registry matrix and evidence plan. Continue WP4/WP5/WP6 only after their exact current contracts and live dependencies are traced; do not bypass Core authorization.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 01:45 UTC+07:00 — JRN-W28-046 — WP0/WP1 live connector and source-to-entrypoint reconciliation

**Role:** Vi | CODER — implementation and integration owner  
**Signature:** [KÝ: VI | CODER]

### LIVE BUILD MCP READ-ONLY OBSERVATION
- ROOM-HOP Build MCP helper call `get_room_context` returned service `room-hop-build`, version `1.0`, status `ok`; boundary says Working Source read-only and Sandbox read/write.
- `get_room_structure` returned Sandbox root `.ai-workspace\sessions\AI-BUILD-GATEWAY-V1\workspace` and helper capabilities: sandbox_list/read/create/write/append/delete/create_work/list_works.
- `sandbox_list(work_id=28)` returned the Work 28 inventory, including canonical-looking Sandbox journal, source, test, evidence and dashboard paths.
- These helper responses are NOT a raw MCP protocol `tools/list` response and do not contain the full deployed JSON schemas or process/build identity. They cannot close WP0 G0.
- `sandbox_read` returned an empty object for the canonical Sandbox journal/manifest paths; `sandbox_read_probe` returned the actual journal content (102,326 characters) successfully. Treat this as a read-path discrepancy; use the diagnostic read only for readback until the regular read path is fixed.

### SOURCE-TO-ENTRYPOINT TRACE
- Canonical repository `room_hop_mcp/__main__.py` (blob `43adaa746f8e51a6ecce762a7b01694d0411d105`) is an stdio entrypoint. It wires `MeetingManager → MeetingService → room_hop_mcp.adapter.server.create_server`.
- `room_hop_mcp/adapter/server.py` (blob `f34b4eebc847dac31feb7c9161c2d8bded812991`) registers exactly four ROOM HOP meeting tools: `list_meetings`, `get_meeting`, `get_transcript`, `add_paste_to_meeting`. It does not wire the Work 28 unified 31-tool registry or v54 catalog.
- Work 28 `mcp8020_server_v54.py` (blob `80365761d75fe27a1e8c7677f79c14ae90819c97`) is a factory and explicitly does not own/open the listener.
- Work 28 `mcp8020_unified_server_v1.py` (blob `65ab9cd41da231c97e5094cb6fab0a6b9c3c84cb`) is another factory, requires six injected provider groups, and explicitly does not open the listener.
- `mcp_tool_registration_v1.py` (blob `b9f306c9e4765117af517be578139faabe8bab01`) documents that `register_work28_tools()` must be called by an existing FastMCP startup after provider injection. No such callsite was found in the inspected Work 28 adapter/entrypoint modules.
- The previously reported PC startup module path `room_hop_mcp.mcp_build_http_main` is absent from the canonical branch tree at the inspected revision (repository file lookup returned 404). Therefore historical PC listener PID/command evidence cannot be bound to this canonical branch/source SHA.
- Existing source inventory still contains distinct 18-tool legacy, 31-tool unified and 54-tool v54 catalogs. A helper capability list or a tool count is not live registry parity.

### WP1 DISPOSITION
- **G1 provider composition/startup callsite:** NOT VERIFIED.
- **G2 exact raw MCP 8030 tools/list and schema digest:** NOT VERIFIED.
- **G3 process/build/source identity bound to the same live listener:** NOT VERIFIED.
- **G4 approved non-destructive live tool-call/readback evidence:** NOT VERIFIED.
- No startup entrypoint or provider composition is invented; no listener is restarted and no runtime deployment is attempted. Historical MCP :8020 remains DO NOT USE.
- Next: resolve the authoritative Build MCP deployment repository/module and obtain raw protocol-level tools/list plus process/build identity from the same approved live instance. Until then WP1 remains BLOCKED.

## 2026-11-23 01:46 UTC+07:00 — JRN-W28-047 — WP5 Core grant authority fail-closed remediation

**Role:** Vi | CODER — implementation and integration owner  
**PR:** #71 — https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/71  
**Tested source SHA:** `a9eafadfc797fef75bb14e397046ab5bc2a8a3be`  
**Merge commit:** `dca6fd27ea119b64cee550395e0613289057b0f8`  
**Signature:** [KÝ: VI | CODER]

### FINDING / BUILD
- Source trace confirmed `execution_host/work28_core_grant_client.build_grant_source()` automatically selected `FileGrantSource` when `ROOM_HOP_CORE_GRANT_URL` was missing.
- `execution_host/server.py::main()` caught any Core grant-source exception and substituted `load_grant_registry()`, allowing startup with local grant state after Core failure.
- `Handler.snapshot_only`, `serve()` and main's environment parsing defaulted command mode open when `ROOM_HOP_SNAPSHOT_ONLY` was unset.
- Remediation:
  1. Core grant URL is mandatory; missing/blank URL raises `GrantError(core_grant_url_required)`.
  2. Execution Host startup no longer falls back to a local file registry on Core error; it aborts before serving.
  3. `FileGrantSource` remains available only as an explicitly selected offline/test adapter.
  4. Snapshot-only defaults TRUE at handler, serve and main layers. An explicit trusted deployment environment opt-out is required to enable legacy command mode.
  5. Added fail-closed regression coverage and updated legacy tests to opt into their intended test mode explicitly.

### VERIFY — EXACT-SHA AUTO E2E
- Initial red runs exposed existing tests that encoded the old file-fallback/default-command behavior; those tests were corrected to assert the new secure contract or explicitly opt into legacy command mode where that was the subject under test.
- Final GitHub Actions run #391 / ID `45055422844` on exact source SHA `a9eafadfc797fef75bb14e397046ab5bc2a8a3be`: **SUCCESS**.
- All five jobs completed success: unit/regression, Linux lifecycle, Windows lifecycle, immutable source artifact retest, automatic E2E gate report.
- Source artifact ID `14767765017`, digest `sha256:8f3aaee8df368e9534725b1368f651025f0768fe159e7c80ac71410517f1f8c5`.
- Auto E2E report artifact ID `14767595848`, digest `sha256:3c938575af14460de76a22f450b733397c49e7dddc1d353a9b1317dca10c3757`.
- PR #71 merged after exact-head CI success. Canonical branch now points to merge commit `dca6fd27ea119b64cee550395e0613289057b0f8`.

### LIMITATIONS / GATES
- This patch makes the Execution Host fail closed; it does not prove the deployed Core endpoint exists, is compatible with the client's list response contract, or is reachable from the runtime.
- No listener restart, production deployment, Core mutation or live grant issuance was performed.
- WP3-F01 Q4 remains NOT APPROVED under the exact Ka review and Xu revision record; upload capability implementation/registration/staging/promotion remains blocked pending the decision authority's approval of the versioned contract.
- WP1 provider composition/raw tools/list/live build identity remains NOT VERIFIED.
- Deployed MCP → Core → Runtime E2E remains BLOCKED. Execution Gate CLOSED. Release NOT_RELEASED.

**STATUS:** WP5 FAIL-CLOSED SOURCE REMEDIATION INTEGRATED / EXACT-SHA AUTO E2E PASS / LIVE CORE AND MCP PROVENANCE NOT VERIFIED / WP3 Q4 NOT APPROVED / NOT RELEASED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 01:52 UTC+07:00 — JRN-W28-048 — Canonical GitHub → Work 28 Sandbox exact artifact synchronization

**Role:** Vi | CODER — implementation and integration owner  
**Canonical branch HEAD at synchronization:** `dca6fd27ea119b64cee550395e0613289057b0f8`  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Reconciled canonical GitHub journal against the Work 28 Sandbox journal using `sandbox_read_probe`.
- Sandbox journal was stale at JRN-W28-030 (102,326 characters); canonical GitHub journal contained newer entries through JRN-W28-047.
- Regular `sandbox_read` continued to return an empty object for the journal/manifest, while `sandbox_read_probe` returned the actual file content. Used the diagnostic read path for verification; no inference was made from the empty regular-read result.

### BUILD — EXACT ARTIFACT SYNC
- Replaced the Sandbox canonical journal with the full canonical GitHub journal through JRN-W28-047.
- Synchronized the 12 source/test/workflow files changed by PR #70 and PR #71 from the canonical branch into the matching Work 28 Sandbox paths:
  - workflow: `.github/workflows/work28-mcp-tooling.yml`
  - source: `execution_host/host.py`, `execution_host/host_run.py`, `execution_host/process_job.py`, `execution_host/server.py`, `execution_host/work28_core_grant_client.py`
  - tests: `test_process_job.py`, `test_wp2_service_mapping_and_race.py`, `test_work28_core_grant_fail_closed.py`, `test_work28_evidence.py`, `test_w13_execute_handler_http_boundary.py`, `test_w13_execution_auth_config_bootstrap.py`
- GitHub source blobs were read from canonical branch and written to the corresponding Sandbox paths. No unrelated historical files, cache files or bytecode were promoted.

### VERIFY — READBACK
- Full journal: Sandbox `sandbox_read_probe` content exactly equals canonical GitHub journal content before this synchronization entry; lengths both 169,265 characters, including JRN-W28-044 through JRN-W28-047.
- 12/12 source/test/workflow files: each Sandbox `sandbox_read_probe` content compared byte-for-byte at text level against the corresponding canonical GitHub file; all 12 returned `exact_match=true`.
- This proves exact selected-artifact text parity for the 12 listed files and journal version through JRN-W28-047. It does not claim whole-workspace synchronization or local PC checkout synchronization.

### LIMITATIONS / NEXT
- Append this JRN-W28-048 entry to canonical GitHub, then repeat full-journal Sandbox write/readback so the Sandbox journal includes this synchronization record.
- Continue exact artifact synchronization only; GitHub remains canonical.
- WP1 raw tools/list and deployed process/build provenance remain NOT VERIFIED.
- WP3-F01 Q4 remains NOT APPROVED; no upload side effects.
- Live MCP → Core → Runtime E2E remains BLOCKED; Execution Gate CLOSED; release NOT_RELEASED.

**STATUS:** CANONICAL JOURNAL + 12 SELECTED SOURCE/TEST/WORKFLOW FILES SYNCED / EXACT TEXT READBACK PASS / WHOLE WORKSPACE SYNC NOT CLAIMED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 02:03 UTC+07:00 — JRN-W28-049 — WP1 31-tool schema and handler-binding hardening integrated

**Role:** Vi | CODER — implementation and integration owner  
**PR:** #72 — https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/72  
**Tested source SHA:** `e310882ceafd2705b79efb4718af7e8f3a4ea5fc`  
**Merge commit:** `ab51accd1fb186c68beec8fcf08009c25c3dfa67`  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Re-read the Sandbox WP1 vertical-slice status (2026-11-15), provider-composition gap audit (2026-11-03), Core authority dependency blocker and the 2026-10-26 live-entrypoint audit.
- Sandbox source had a newer 31-tool registry/server than GitHub, plus two missing modules: Draft 2020-12 schema validation and exact handler binding. The 31-tool registry is the chosen source-level contract; no runtime listener/provider claim is inferred.
- The current Sandbox entrypoint adapter is explicitly a contract scaffold and does not create a listener or execute work. The seven v54 execution/evidence tools return NOT_IMPLEMENTED (and arbitrary command is POLICY_REFUSED); it is not production registration.
- Existing provider gap remains: six approved provider groups are required (Core, Sandbox, Sandbox extensions, Proposal, GitHub, Runtime); no verified composition root or real approved Core/Sandbox/Proposal/Runtime providers were found. In-memory reference providers and echo test providers are not production providers.

### BUILD
- Ported the latest Sandbox WP1 static contract hardening into canonical GitHub:
  1. `mcp8020_unified_registry_v1.py`: 31 exact ordered names, unique-name/boundary checks, strict SHA-256 source hash pattern and schema validation at registry export.
  2. `mcp8020_schema_validation_v1.py`: Draft 2020-12 schema validation, full argument validation and provider signature compatibility checks.
  3. `mcp8020_tool_handler_binding.py`: exact handler-key set, no missing/extra handlers and signature validation before registration.
  4. `mcp8020_unified_server_v1.py`: validates full JSON Schema before provider invocation and preserves empty mappings as structured JSON objects.
  5. Added focused schema and handler-binding tests; declared `jsonschema>=4.20,<5` in requirements.
- No listener, provider, Core endpoint or execution behavior was invented. This is a transport-neutral factory/contract improvement.

### VERIFY — EXACT-SHA AUTO E2E
- PR #72 exact tested source SHA: `e310882ceafd2705b79efb4718af7e8f3a4ea5fc`.
- GitHub Actions run #393 / ID `45056547390`: **SUCCESS** on the exact PR head.
- All five jobs succeeded: unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA source artifact retest and automatic E2E gate report.
- Source artifact ID `14766644475`, digest `sha256:b63c4e6c6260ddbdaba6412f0067632d5a5a44c2f282ec52ea9cd99cbaef2cef`.
- Auto E2E report artifact ID `14767397963`, digest `sha256:c77f9bbf38a0c3a9097416ac3a6920f2714624ba85d561e171dd98f34f071956`.
- PR #72 merged after exact-head CI success. Canonical branch now points to merge commit `ab51accd1fb186c68beec8fcf08009c25c3dfa67`.

### LIMITATIONS / ACCEPTANCE
- **WP1 source contract/schema/binding:** IMPLEMENTED / EXACT-SHA CI PASS.
- **WP1 live composition root/provider binding:** NOT VERIFIED / BLOCKED.
- **WP0 raw MCP 8030 tools/list parity + process/build identity:** NOT VERIFIED.
- **Core authorization/WorkContext and Runtime provider:** BLOCKED by missing approved Core execution-grant capability; do not use caller-supplied identity or local/in-memory state as authority.
- **WP3-F01 Q4 upload grant:** NOT APPROVED; no upload implementation/side effects.
- **Live MCP → Core → Runtime → Execution Host E2E:** BLOCKED. Execution Gate CLOSED. Release NOT_RELEASED.
- No deployment, listener restart, Core mutation or activity against historical MCP :8020.

**STATUS:** WP1 STATIC CONTRACT HARDENING INTEGRATED / EXACT-SHA AUTO E2E PASS / LIVE PROVIDER COMPOSITION AND DEPLOYED PARITY NOT VERIFIED / NOT RELEASED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 02:12 UTC+07:00 — JRN-W28-050 — Post-merge exact-SHA CI reconciliation and WP1 Sandbox source sync

**Role:** Vi | CODER — implementation and integration owner  
**Signature:** [KÝ: VI | CODER]

### POST-MERGE CI RECONCILIATION
The push-triggered workflow runs were queried after the merge commits and are now available. This supersedes the earlier "no push-triggered run returned yet" observation in JRN-W28-045.
- PR #70 merge commit `2d006dcb5aaac5624d45cf88b173bf59d0dce55a`: push run #388 / ID `45055014499` — **SUCCESS**, all five jobs completed success.
- PR #71 merge commit `dca6fd27ea119b64cee550395e0613289057b0f8`: push run #392 / ID `45055750014` — **SUCCESS**, all five jobs completed success.
- PR #72 merge commit `ab51accd1fb186c68beec8fcf08009c25c3dfa67`: push run #394 / ID `45056717662` — **SUCCESS**, all five jobs completed success.
- Each push run includes unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA source artifact retest and automatic E2E gate report. These post-merge runs now prove the integrated canonical merge commits themselves passed the configured workflow.
- These results still do not prove live MCP/Core/Runtime deployment or release acceptance.

### WP1 SANDBOX SOURCE SYNCHRONIZATION
- Synced from canonical GitHub into Work 28 Sandbox:
  - `04_CODE/mcp8020_unified_registry_v1.py`
  - `04_CODE/mcp8020_unified_server_v1.py`
  - `04_CODE/mcp8020_schema_validation_v1.py`
  - `04_CODE/mcp8020_tool_handler_binding.py`
  - `05_TEST/test_mcp8020_tool_handler_binding.py`
  - `05_TEST/test_mcp8020_schema_validation_v1.py`
  - `requirements.txt`
- Read back each Sandbox file through `sandbox_read_probe` and compared with the canonical GitHub file text. Result: **7/7 exact_match=true**.
- The full canonical journal through JRN-W28-049 was also written to Sandbox and read back with exact text equality. This entry is followed by another journal sync/readback.

### CONSOLIDATED SELECTED-ARTIFACT PARITY
- PR #70/#71 selected source/test/workflow batch: 12/12 exact text readbacks (JRN-W28-048).
- PR #72 WP1 source/test/dependency batch: 7/7 exact text readbacks.
- Journal through JRN-W28-049: exact text readback.
- Total selected source/test/workflow artifacts verified across the two batches: **19/19**. This is not a claim that the entire Work Sandbox, local PC checkout, binary files, caches or runtime deployment are synchronized.

### CURRENT GATES
- WP2 lifecycle recovery: integrated; exact pre-merge and post-merge Auto E2E PASS.
- WP5 Core-grant fail-closed startup + snapshot-only default: integrated; exact pre-merge and post-merge Auto E2E PASS.
- WP1 31-tool registry schema and exact handler-binding contract: integrated; exact pre-merge and post-merge Auto E2E PASS.
- WP1 provider composition/startup entrypoint, live tools/list schema parity and deployed process/build identity: NOT VERIFIED / BLOCKED.
- WP3-F01 Q4 upload grant: NOT APPROVED; no upload side effects.
- Core execution-grant route, trusted WorkContext, Runtime identity, OS isolation and protected evidence/readback: NOT VERIFIED.
- Execution Gate CLOSED. Release NOT_RELEASED. No production deployment, listener restart or Core mutation.

**STATUS:** POST-MERGE CI PASS ON THREE CANONICAL MERGE COMMITS / 19 SELECTED SOURCE-TEST-WORKFLOW FILES EXACTLY SYNCED / LIVE E2E STILL BLOCKED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 02:20 UTC+07:00 — JRN-W28-051 — Stale PR cleanup and owner Auto E2E handoff

**Role:** Vi | CODER — implementation and integration owner  
**Handoff artifact:** `06_EVIDENCE/VI_OWNER_HANDOFF_AUTO_E2E_20261123.md`  
**Handoff commit:** `34f0e026443a2d70ff557d190188e01b51fe2174`  
**Signature:** [KÝ: VI | CODER]

### PR CLEANUP
- Rechecked PRs #61, #69, #70, #71 and #72.
- PR #61 and PR #69 were OPEN, stale and based on older divergent snapshots. Their WP2 code was superseded by the tested latest-baseline integration in PR #70.
- Added explicit supersession comments and closed PR #61 (comment ID `7083860364`) and PR #69 (comment ID `7083861213`).
- PRs #70, #71 and #72 remain MERGED. No source change was discarded from the canonical branch.

### POST-MERGE WORKFLOW EVIDENCE
- Re-read the repository Actions run list and verified the post-merge push runs for all three integration commits:
  - #388 / `45055014499` on `2d006dcb...`: all five jobs SUCCESS.
  - #392 / `45055750014` on `dca6fd27...`: all five jobs SUCCESS.
  - #394 / `45056717662` on `ab51accd...`: all five jobs SUCCESS.
- This reconciles the later-arriving push-run evidence with JRN-W28-045/047/049. It does not change the live E2E gate disposition.

### OWNER HANDOFF
- Created the formal owner handoff artifact at `06_EVIDENCE/VI_OWNER_HANDOFF_AUTO_E2E_20261123.md`.
- The document contains integrated PR/merge/test evidence, artifact IDs and SHA-256 digests, selected Sandbox parity, current acceptance matrix, live blockers, required owner dependencies and rollback sequence.
- The handoff deliberately distinguishes source/CI PASS from live deployed product acceptance. It does not claim release readiness.

### FINAL DISPOSITION AT THIS CHECKPOINT
- WP2 lifecycle: INTEGRATED / exact pre-merge and post-merge CI PASS.
- WP5 Core grant fail-closed + snapshot-only default: INTEGRATED / exact pre-merge and post-merge CI PASS.
- WP1 31-tool schema/handler-binding contract: INTEGRATED / exact pre-merge and post-merge CI PASS.
- WP0/WP1 live MCP 8030 process/build identity, raw tools/list parity and real provider composition: NOT VERIFIED / BLOCKED.
- WP3-F01 Q4 upload capability grant: NOT APPROVED; no upload side effects.
- Core execution-grant/WorkContext, Runtime identity, OS isolation and protected evidence/readback: NOT VERIFIED.
- Execution Gate CLOSED. Release NOT_RELEASED. No deployment/listener restart/Core mutation; historical MCP :8020 remains DO NOT USE.
- The only remaining route to full product acceptance is to satisfy the live deployment/Core authority prerequisites listed in the owner handoff. Vi can then resume Auto E2E without routine code-review waiting.

**STATUS:** CODE/CI INTEGRATION COMPLETE FOR THREE SLICES / STALE PRs CLOSED / OWNER HANDOFF WRITTEN / LIVE PRODUCT ACCEPTANCE BLOCKED BY EXTERNAL AUTHORITY AND DEPLOYMENT EVIDENCE.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 02:26 UTC+07:00 — JRN-W28-052 — Owner handoff publication correction / default-branch tree restoration

**Role:** Vi | CODER — implementation and integration owner  
**Signature:** [KÝ: VI | CODER]

### INCIDENT / CORRECTION
- During publication of `VI_OWNER_HANDOFF_AUTO_E2E_20261123.md`, the first GitHub create-file call omitted its branch argument. The connector therefore created a documentation-only commit on the default branch `main`: `34f0e026443a2d70ff557d190188e01b51fe2174`. The only added path was the Work 28 handoff Markdown file; no product source/test/workflow code was changed.
- Immediately deleted that exact file from `main` in commit `0902cd26518673aa078bb4c7c7899e1e4a95656a`. No force reset or history rewrite was used.
- Compared the Git tree SHA of the parent before the add (`554f02e2e9ac9aedc43d875d7a212b35c94525e7`) with the tree after deletion (`0902cd26518673aa078bb4c7c7899e1e4a95656a`): both are `c8f2bbb9e1b88a7fc0bb173aab4e6e745448506b`. This proves the default-branch file tree was restored exactly; main history now contains two documentation-only commits.
- Recreated the handoff on the correct canonical branch `work/28-mcp-tooling-platform` with an explicit branch argument: commit `4597f0589b7110b94492b027290047c7fecac16c`.
- Updated the Work 28 handoff document to disclose this correction explicitly. No product source changes remain on `main`; no deployment occurred.

### CURRENT HANDOFF LOCATION
- Canonical Work 28 path: `work/28/MCP-8020-TOOLING-PLATFORM/06_EVIDENCE/VI_OWNER_HANDOFF_AUTO_E2E_20261123.md`.
- The controlled document register includes `HND-W28-20261123-001`.
- This entry is recorded to preserve an accurate audit trail; it does not change the Work 28 code acceptance or CI outcomes.

**STATUS:** DEFAULT-BRANCH TREE RESTORED EXACTLY / WORK28 HANDOFF RECREATED ON CORRECT BRANCH / NO PRODUCT SOURCE CHANGE REMAINS ON MAIN / TRANSPARENT AUDIT ENTRY RECORDED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-053 — Core execution authority source/approval reconciliation

**Role:** Vi | CODER — implementation and integration owner  
**Source branch HEAD at audit:** `6dc211c3a6f6ced933c36ab2c2d2787bf4d24d1d`  
**Handoff update commit:** `defc9f3c2fa9120703abcc31979f239af837f051`  
**Signature:** [KÝ: VI | CODER]

### READ / TRACE
- Re-read Work 28 architecture decision V2 (AD-W28-20261103-001): Build/Verification MCP :8030 is separate; Core :8000 is sole identity/Work/policy authority; Runtime MCP is a separate clean deployment; Execution Host :8031 remains the only execution site; historical :8020 is DO NOT USE.
- Re-read Core authority V1.2 contract, Core source, W28 authorizer/session adapters, W13 client, live-authority CI tests and the November 15 Ka Q4 review.
- Found a material documentation/provenance contradiction:
  - The V1.2 contract document still labels itself DESIGN / PROPOSED / NOT APPROVED / NOT WIRED and says it awaits Vinh's final approval.
  - The implementation package `core/execution_authority` exists in canonical source and exposes a separate HTTP server (default port 8001), Work-scoped grant issue/status and run-recording routes, and an fsync-backed append-only JSONL store.
  - The package `__init__.py` and test docstrings call DR-1..DR-4 approved, which conflicts with the contract's explicit approval status. No approval record was found in the Work 28 decision/evidence paths inspected. Vi will not infer approval from implementation or tests.
- Source blobs read:
  - `core/execution_authority/authority.py`: `bfb052fed0fde69767dd219f17a0b14ae6383560`
  - `core/execution_authority/http_server.py`: `6363c277ce410d3f5465f449b730199e06e5024c`
  - `core/execution_authority/store.py`: `a628dc578c68c05bb875318d1b74528b26f0e4eb`
  - `tests/test_core_execution_authority_v1.py`: component/store/HTTP boundary tests using temporary storage and an ephemeral local port.
  - `test_core_execution_authority_boot_v1.py`: CI subprocess/socket boot test with temporary Work registry/credentials; its docstring explicitly says this is not trusted-Sandbox deployment evidence.
  - `test_w13_client_live_authority_e2e_v1.py`: staged client-to-test-authority CI harness; explicitly not wired to the MCP gateway or real W13 host. The harness creates a synthetic PASS record and is not production execution evidence.
- The Work 28 Core grant client already in Execution Host expects a different GET payload contract (a list of grants with Bearer token), while the new Core HTTP authority exposes a per-grant GET route and uses `X-Room-Hop-Service-Identity`. No compatible deployed adapter/configuration was verified.
- Connected ROOM-HOP Build MCP read-only context still reports service `room-hop-build` v1.0 and only Sandbox/build helper capabilities. It is not raw protocol `tools/list`, not Core authority, and not the Work 28 Runtime MCP deployment.

### ANALYSIS / DECISION
- Core authority code + CI tests are now classified as **SOURCE IMPLEMENTED / CI-TESTED**, not as live deployed Core authorization.
- Core V1.2 approval state remains **UNRESOLVED / NOT APPROVED per the contract document** until the product owner explicitly approves or supersedes that versioned contract. No service identity secret, Core Work registry, or W28-to-Sandbox mapping was invented or written.
- Keep the staged W13 client and execution tools NOT_IMPLEMENTED / BLOCKED. Do not wire the CI harness, synthesize a trusted WorkContext, or claim runtime execution.
- WP3-F01 Q4 remains NOT APPROVED under Ka's 2026-11-15 security review; Xu's 2026-11-22 revision is PROPOSED FOR REVIEW / NOT APPROVED. No upload side effects.
- No deployment, listener restart, Core mutation, secret provisioning or live execution request was performed.

### HANDOFF UPDATE
- Updated `06_EVIDENCE/VI_OWNER_HANDOFF_AUTO_E2E_20261123.md` in commit `defc9f3c2fa9120703abcc31979f239af837f051` to distinguish existing Core source/CI tests from deployed authority and to expose the approval-status contradiction.
- The remaining live gate now requires: explicit disposition of Core V1.2 contract; actual Core deployment identity/endpoint and enrolled service identity; trusted canonical W28/Sandbox mapping; compatible remote grant/WorkContext adapter; real W13 host provenance and execution evidence.
- No routine An/Ka code review is being awaited. These are owner-authority and live-deployment proof requirements, not code-review queue items.

**STATUS:** CORE AUTHORITY SOURCE EXISTS / CI COMPONENT AND BOOT TESTS EXIST / CONTRACT APPROVAL AND LIVE DEPLOYMENT NOT VERIFIED / EXECUTION GATE CLOSED / RELEASE NOT_RELEASED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-054 — Core authority contract/source consistency PR #73 integrated

**Role:** Vi | CODER — implementation and integration owner  
**PR:** #73 — https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/73  
**Tested source SHA:** `f341a3f8bb67141b352d0c6647a214851483365d`  
**Merge commit:** `7666c0c7de60583c77b466c1e08ea10a0a7d0cd7`  
**Auto E2E run:** #395 / `45060135687` — SUCCESS  
**Signature:** [KÝ: VI | CODER]

### BUILD / VERIFY
- Corrected the Core authority package docstring: source code is an implementation candidate, not self-approved.
- Corrected the Core authority component test docstring: local component/HTTP tests prove only candidate behavior, not owner approval or production deployment.
- Corrected the V1.2 architecture contract: the HTTP endpoint candidate exists in source, but no owner-approved/deployed endpoint has been verified. Updated Gate 2 and the explicit non-claims to reflect source reality without treating source presence as approval.
- No grant behavior, endpoint semantics, credentials, Work registry, identity enrollment, MCP wiring, Runtime, or deployment changed.
- PR #73 exact tested source SHA `f341a3f8bb67141b352d0c6647a214851483365d` passed all five Auto E2E jobs: unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA artifact retest and automatic gate report.
- Exact artifacts: source `14769366587` / `sha256:4fccc0f499608d977736903825ccd0ae651eee6463fd9dffbcd9731c316dbd0c`; report `14769321707` / `sha256:609a87773f9e95ab3af83e4e2e9acb35b6e479c3897056a6d03eaa5b9927a517`.
- PR #73 merged with expected head SHA; canonical branch advanced to `7666c0c7de60583c77b466c1e08ea10a0a7d0cd7`.

### POST-MERGE / HANDOFF
- PR #73 and its exact-head CI evidence were added to the owner handoff document.
- Post-merge push workflow for `7666c0c...` had not yet appeared at the time of this entry; it must be checked before recording post-merge PASS.
- Source/CI status is stronger and more accurate, but live Core authority deployment, trusted WorkContext, W28 identity enrollment, mapping and real MCP→W13 E2E remain unverified.
- Execution Gate CLOSED; release NOT_RELEASED.

**STATUS:** PR #73 MERGED / EXACT-HEAD AUTO E2E PASS / CORE CONTRACT PROVENANCE RECONCILED / LIVE DEPLOYMENT AND AUTHORITY STILL NOT VERIFIED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-055 — PR #73 post-merge Auto E2E and Sandbox parity

**Role:** Vi | CODER — implementation and integration owner  
**Canonical merge SHA:** `7666c0c7de60583c77b466c1e08ea10a0a7d0cd7`  
**Post-merge run:** #396 / `45060288335` — SUCCESS  
**Handoff update commit:** `62ed29f72c4676ccfa2f5a99521864d19a4ddd67`  
**Signature:** [KÝ: VI | CODER]

### POST-MERGE EXACT-SHA VERIFICATION
- Confirmed PR #73 merge commit is the exact canonical branch revision.
- Push-triggered run #396 / ID `45060288335` completed **SUCCESS** on merge SHA `7666c0c7de60583c77b466c1e08ea10a0a7d0cd7`.
- All five jobs succeeded: unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA source artifact retest and automatic E2E gate report.
- Exact artifacts:
  - Source archive ID `14769077832`, digest `sha256:086b2ca2ada57e0045b917861bed9d2b8b325f0a6944fefd46d0f095cca9b087`.
  - Auto E2E report ID `14769580524`, digest `sha256:cbf0c1f8543fe259606428e7218759a48d965c97d43b72b519e653f3fa7ea104`.
- Updated the owner handoff with the post-merge run and artifact identities.

### SANDBOX READBACK
- Synced canonical journal, owner handoff, Core V1.2 contract, Core authority package docstring snapshot and Core authority component-test source to Work 28 Sandbox.
- Read each back with `sandbox_read_probe` and compared exact text against GitHub. Result: **5/5 exact_match=true**.
- This is selected-document/source parity only; it does not prove deployment or live process identity.

### CURRENT GATE
- Core authority source/contract wording is now internally consistent: implementation candidate and CI-tested, while owner approval, deployed endpoint, identity enrollment, trusted W28 WorkContext and MCP/W13 wiring remain unverified.
- PR #73 source/docs consistency fix is integrated and exact post-merge Auto E2E PASS.
- Execution Gate remains CLOSED. Release remains NOT_RELEASED. No deployment, secret provisioning, listener restart or live execution was performed.

**STATUS:** PR #73 POST-MERGE AUTO E2E PASS / 5 SANDBOX ARTIFACTS EXACTLY SYNCED / LIVE AUTHORITY AND RUNTIME ACCEPTANCE STILL BLOCKED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-056 — Prepared read-only PC provenance collector for live acceptance

**Role:** Vi | CODER — implementation and integration owner  
**Collector:** `06_EVIDENCE/PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.ps1`  
**Runbook:** `06_EVIDENCE/PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.md`  
**Collector commit:** `5789bb6f545f45ae1392de2086a7520e5cd92833`  
**Runbook commit:** `bdca4bcafbb010a7c39a036178e2be83237a9e7c`  
**Handoff update:** `429a998ab91880d20dd2f5a910a32eec5ddda8c8`  
**Signature:** [KÝ: VI | CODER]

### PURPOSE
The remaining acceptance gap requires evidence from the actual ROOM-HOP PC. ChatGPT's connected Build MCP tools expose Sandbox operations and context but do not provide the raw remote MCP wire-level tools/list or the PC process/module identity. No available connector action can safely substitute for those facts.

### COLLECTOR SCOPE
- Read-only Git branch/HEAD/dirty status.
- Listener metadata only for ports 8000, 8001, 8030 and 8031; sanitized PID, executable, parent, creation time and parsed Python module name. Full command line and environment variables are never printed.
- SHA-256 for the local source files that define the Core, MCP and Execution Host boundaries.
- One MCP initialize handshake and one raw `tools/list` request to the historical candidate Build endpoint `https://admin-pc.tail7d6101.ts.net/build/mcp`, using the protocol version negotiation response.
- No `tools/call`, no write operations, no listener restart, no environment change, no secret reads, and no contact with historical MCP :8020. No alternate endpoint fallback; endpoint failure remains BLOCKED.
- Captured response digest is explicitly labelled UTF-8 body capture digest; it is not misrepresented as a packet-level wire hash or proof of loaded process memory.

### HANDOFF
- Added the PowerShell collector and companion runbook under Work 28 `06_EVIDENCE`.
- Updated owner handoff with the exact run command and limited return artifacts.
- The collector has **not been run on the PC**. No PC output, current listener, live endpoint or raw tools/list result is claimed.
- Owner needs only to run the read-only script once and return `summary.txt`, `mcp_tools_list_raw.txt` if created, and the evidence timestamp. If the endpoint fails, return BLOCKED; do not start/restart a service.
- Once returned, Vi can correlate PC process/module/source hashes with canonical GitHub, compare raw live tool names/schemas against the selected registry, and decide the next safe adapter/provider work.

**STATUS:** READ-ONLY LIVE EVIDENCE COLLECTOR PREPARED / NOT YET EXECUTED ON PC / LIVE G0 AND DEPLOYMENT ACCEPTANCE REMAIN BLOCKED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-057 — Collector encoding portability correction

**Role:** Vi | CODER — implementation and integration owner  
**File:** `06_EVIDENCE/PC_READONLY_LIVE_PROVENANCE_COLLECTOR_20261123.ps1`  
**Commit:** `c5c223250c6fe8a9597af5d1fb9d3a367757ed6d`  
**Signature:** [KÝ: VI | CODER]

- Replaced the UTF-8 no-BOM encoder construction with the explicit .NET constructor `[System.Text.UTF8Encoding]::new($false)` for PowerShell 5.1 compatibility.
- This is a script portability correction only; no PC script execution is claimed. No service/process or local repository was touched.
- Collector remains PREPARED / NOT RUN ON PC. Its endpoint and protocol result remain unverified until the owner runs the read-only collector.

**STATUS:** COLLECTOR PORTABILITY PATCHED / NOT EXECUTED / LIVE PROVENANCE STILL BLOCKED.

**Signature:** [KÝ: VI | CODER]


## 2026-11-23 — JRN-W28-058 — Ka independent continuation review: integrated WP2/WP5/WP1 slices and remaining live gates

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:03 UTC+07:00 (Asia/Ho_Chi_Minh)  
**Source branch:** `work/28-mcp-tooling-platform`  
**Authority:** Vinh — delegated continuation; no release or deployment authority inferred  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Re-read the canonical Work Manifest, Work Structure Standard, original Work 28 requirement, Master Execution Plan V2.0, Auto E2E Runbook V2.0, Architecture Decision V2 and existing canonical journal.
- Confirmed canonical governance: GitHub branch `work/28-mcp-tooling-platform`; Core :8000 remains sole authorization/application authority; Build/Verification MCP :8030 remains separate; historical MCP :8020 remains quarantined / DO NOT USE; Execution Host :8031 is the controlled execution boundary; Execution Gate CLOSED; release NOT_RELEASED.
- Re-read current canonical WP2 source surfaces `execution_host/process_job.py`, `execution_host/host.py`, `execution_host/host_run.py`, lifecycle tests and `.github/workflows/work28-mcp-tooling.yml`. Source contains the suspended Windows spawn sequence (Job Object before suspended process, assignment before resume), explicit fail-closed handling, serialized service registry transitions and retry-preserving cleanup behavior. The workflow includes unit/regression, Linux lifecycle, Windows lifecycle, immutable exact-SHA artifact retest and gate-report jobs.
- Re-read the Vi owner handoff and its exact-source/merge/CI references for PRs #70–#73. The handoff records:
  - PR #70 WP2: tested SHA `42d9c43ec4dbd573b1dad5318cfa0bf10433eab0`; merge `2d006dcb5aaac5624d45cf88b173bf59d0dce55a`; PR run #387 / `45054861801` and post-merge run #388 / `45055014499`, all five configured jobs SUCCESS.
  - PR #71 WP5: tested SHA `a9eafadfc797fef75bb14e397046ab5bc2a8a3be`; merge `dca6fd27ea119b64cee550395e0613289057b0f8`; PR run #391 / `45055422844` and post-merge run #392 / `45055750014`, all five configured jobs SUCCESS.
  - PR #72 WP1 static registry/schema/handler-binding: tested SHA `e310882ceafd2705b79efb4718af7e8f3a4ea5fc`; merge `ab51accd1fb186c68beec8fcf08009c25c3dfa67`; PR run #393 / `45056547390` and post-merge run #394 / `45056717662`, all five configured jobs SUCCESS.
  - PR #73 Core authority provenance wording: tested SHA `f341a3f8bb67141b352d0c6647a214851483365d`; merge `7666c0c7de60583c77b466c1e08ea10a0a7d0cd7`; PR run #395 / `45060135687` and post-merge run #396 / `45060288335`, all five configured jobs SUCCESS.
- Exact live source identity is still not established by these CI runs. CI proves the configured repository test/build lanes only.
- Inspected PR #74, “W28: Core Execution Authority & Agent-to-Computer Contract V1.3”. Its description declares architecture-contract-only scope; no implementation, endpoint, runtime, deployment or release. Independent review and QA are pending. It is not treated as an approved Work 28 implementation contract in this entry.

### REVIEW / FINDINGS
1. **WP2 — INTEGRATED / CI PASS (source + configured CI scope).** Current source and handoff evidence support the lifecycle remediation and Linux/Windows CI claims. OS isolation remains NOT_VERIFIED; CI does not attest the deployed Execution Host or production process identity.
2. **WP5 — INTEGRATED / CI PASS (fail-closed source behavior).** The handoff records mandatory Core grant URL, startup abort on missing/unreachable Core and no automatic local file-grant fallback; snapshot-only is the default. This is not proof that a compatible, owner-approved Core grant endpoint is deployed and reachable.
3. **WP1 — STATIC CONTRACT INTEGRATED / CI PASS.** The handoff records exact ordered 31-tool registry, Draft 2020-12 schema validation, complete argument validation before provider invocation and exact provider-handler key/signature checks. The production composition root and real provider groups remain NOT VERIFIED.
4. **Core authority — SOURCE IMPLEMENTED / CI-TESTED; APPROVAL AND LIVE DEPLOYMENT NOT VERIFIED.** PR #73 corrected misleading approval wording. The V1.2 contract still says NOT APPROVED / NOT DEPLOYED / NOT WIRED; do not wire the staged client or synthesize WorkContext until the authority decision and real deployment evidence exist.
5. **WP3-F01 — BLOCKED.** Q4 upload grant is not approved; no binary upload side effects may be enabled.
6. **WP0 / live Build MCP :8030 — BLOCKED.** Raw protocol tools/list, process/build identity and deployed registry/schema parity are not established.
7. **Runtime MCP / Execution Host :8031 — BLOCKED.** No complete live MCP → Core → Runtime → Host execution, protected evidence persistence and authorized checksum readback are verified.
8. **PC provenance collector — PREPARED / NOT RUN.** The read-only collector and runbook are present, but no PC output was supplied or observed in this review. Do not claim a listener, process or deployment PASS.
9. PR #61 and PR #69 are recorded in the owner handoff as superseded by PR #70; do not revive the historical branches as integration targets.

### DECISION
- Keep the canonical branch as the only source of truth. Treat WP2, WP5 and WP1 static contract as integrated source/CI slices, not as full product acceptance.
- Continue only source/CI work that does not invent Core authority, deploy services, change credentials, or interact with the quarantined historical :8020 listener.
- Do not merge PR #74 or treat its V1.3 architecture contract as approved solely because it exists. Require exact contract readback and the required authority/owner decision.
- Execution Gate remains CLOSED; Work 28 remains ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

### NEXT
- Vi: maintain the integrated source and CI evidence; prepare a clean, explicit dependency handoff for the remaining live provenance/authority inputs; do not create a local fallback or synthetic live PASS.
- An: independent native Linux/Windows reproduction remains distinct from Vi's CI evidence; no QA PASS is inferred here.
- Ka: continue static security review of exact canonical code and contract diffs; report only evidence-backed findings.
- Xu: coordinate the external Core/W14/W52/W70/W33/W102 authority decisions and the PR #74 contract review under delegated governance.
- Vinh: no routine technical action requested; product acceptance remains with Vinh.

**STATUS:** WP2 / WP5 / WP1 STATIC CONTRACT INTEGRATED WITH REPORTED EXACT-HEAD AND POST-MERGE CI PASS; LIVE AUTHORITY / DEPLOYMENT / PROVIDER COMPOSITION / WP3-F01 / RUNTIME E2E BLOCKED; EXECUTION GATE CLOSED; NOT RELEASED.


## 2026-11-23 — JRN-W28-059 — Ka WP5 trust-boundary review: Core grant transport and contract incompatibility

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:03 UTC+07:00  
**Source branch:** `work/28-mcp-tooling-platform`  
**Review type:** Read-only source/contract review; no live endpoint call  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE — exact source blobs
- `execution_host/work28_core_grant_client.py`: `e330d4f3681d3fb142e559f7ee35b21db128be7e`.
- `execution_host/work28_grant.py`: `05c082b00a5c38fbdf45950d42211e644f57ed45`.
- `execution_host/work28_dispatch.py`: `22d5dcd385e301a43fcd0e1c3e901ff2c90abac9`.
- `execution_host/work28_execute.py`: `ecb4fc05332c77983cd244c66d1e838def6c30d2`.
- `execution_host/server.py`: `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`.
- `core/execution_authority/http_server.py`: `6363c277ce410d3f5465f449b730199e06e5024c`.
- `core/execution_authority/authority.py`: `bfb052fed0fde69767dd219f17a0b14ae6383560`.
- `PROPOSED_CORE_EXECUTION_AUTHORITY_CONTRACT_V1.md`: `83fb425364a893e602a122c42bc74f80cbd05166`.

### FINDINGS
**W28-KA-WP5-01 — HIGH: remote Core grant URL permits plaintext HTTP while sending a Bearer token.**
- `HttpCoreGrantSource.__init__` accepts any non-empty URL without scheme/host/TLS validation.
- `fetch_grants()` attaches `Authorization: Bearer <token>` when configured and passes the URL to `urllib.request.urlopen`.
- A remote `http://` configuration can therefore transmit the Core grant credential without TLS. Redirect behavior is also not explicitly constrained.
- Required remediation: require HTTPS for all non-loopback Core endpoints; allow HTTP only for explicit loopback development; reject URL userinfo/query/fragment and malformed ports; prevent credential-bearing cross-origin redirects; add negative and positive regression tests.
- Severity: HIGH / security blocker before any remote grant client is enabled. No live call or credential was made/read.

**W28-KA-WP5-02 — P0: Work 28 grant client is not compatible with the current Core authority HTTP contract.**
- Work 28 client performs a GET against one configured URL and requires a top-level JSON list of grant records with `grant_id`, `work_id`, `entry_path`, `operation`, `expected_source_sha256` and optional `expires_at_unix`; it uses an optional Bearer token.
- Core source instead exposes POST `/works/{work_id}/execution-grants` using `X-Room-Hop-Service-Identity`, returning a nested `{"status":"ok","grant":...}` object; GET is per-grant status at `/works/{work_id}/execution-grants/{grant_id}`. No list endpoint matching the Work 28 client was found in the inspected Core HTTP surface.
- Core grant metadata includes service identity and a separate grant token/status model; the Work 28 client/ExecutionGrant does not map this contract or demonstrate online revocation/status validation.
- Therefore the current client cannot consume the inspected Core API as written. Do not configure a guessed endpoint or translate fields heuristically.
- Severity: P0 integration blocker. Requires an explicitly approved versioned Core↔W28 contract and an adapter implemented against the actual Core route/schema.

**W28-KA-WP5-03 — P0: caller-supplied WorkContext is not proof of Core authority.**
- Execution Host `POST /execute` accepts `work_context` from the request body; the handler applies a local `ROOM_HOP_AUTHORIZED_WORKS` allow-list and sets `authorized=True`.
- Snapshot dispatch then compares the local grant's Work ID with this body-supplied context. This is not a trusted WorkContext returned by authenticated Core middleware/provider and does not prove the request principal, Assignment, purpose, audience or revocation state.
- Local allow-list and shared execution-token checks are defense-in-depth/configuration, not substitutes for Core-owned authorization.
- Keep MCP execution tools closed and do not expose this server as a production route until Core-derived principal/WorkContext and the approved grant validation flow replace the caller-controlled context path.

**W28-KA-WP5-04 — P1: readiness/health must not be interpreted as deployment acceptance.**
- `GET /health` returns HTTP 200 and top-level `status=PASS` when the host object exists, while the nested readiness report can still show `core_grant_live=BLOCKED`, `os_isolation=NOT_VERIFIED`, `mcp_execution_tools=CLOSED` and `release=NOT_RELEASED`.
- Consumers must use the full readiness gates; a top-level health PASS only indicates the local handler object is initialized. Consider renaming the field to `health=OK` or ensuring dashboards never promote it to product readiness.

### REVIEW-ONLY PATCH CANDIDATE — NOT PROMOTED
- A non-canonical review branch was created: `ka/work28-core-grant-transport-tls-20261123`.
- It contains a proposed URL validation guard in `execution_host/work28_core_grant_client.py` and four policy tests appended to `tests/test_work28_grant.py`.
- Exact candidate blobs: client `93203c8b7937804efbfbefafd6cce823135610cb`; tests `38849aa4e3052165d2f71ab2ee5740d8c5ff76ca`.
- This is an untested review aid only: no CI run, no PR, no merge, no canonical branch mutation. It is not accepted implementation and must be independently inspected/ported by Vi as the designated implementation lead. Ka does not self-approve this candidate.

### DECISION / NEXT
- Do not wire the current Work 28 grant client to the current Core candidate. Do not enable remote plaintext HTTP, local fallback, caller-supplied authority or production execution.
- Vi: inspect the review candidate, implement the TLS/redirect guard on the designated implementation branch, add tests to the required CI lane, and separately propose a contract adapter only after the Core API contract is approved and proven.
- Xu: coordinate the versioned Core authority decision and resolve the V1.2/V1.3 contract approval boundary.
- An: independently reproduce the transport-policy and Core-denial tests after Vi's implementation; no QA PASS is inferred.
- Ka: review the resulting exact diff and threat boundary independently.
- Execution Gate CLOSED; Work 28 ACTIVE / INTEGRATION BLOCKED / NOT RELEASED.

**STATUS:** HIGH/P0 WP5 TRUST-BOUNDARY FINDINGS RECORDED; REVIEW-ONLY TLS PATCH CANDIDATE NOT TESTED OR PROMOTED; CORE CONTRACT MISMATCH AND TRUSTED WORKCONTEXT BLOCKED.


## 2026-11-23 — JRN-W28-060 — Independent review of Core Execution Authority & Agent-to-Computer Contract V1.3 (PR #74)

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:03 UTC+07:00  
**PR:** #74 — W28 Core Execution Authority & Agent-to-Computer Contract V1.3  
**Review ID:** 6015314554 — COMMENT (not APPROVE)  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Read the complete V1.3 contract at branch `xu/w28-core-authority-v1-3-20261123`, blob `85c88a5ac50a6d12e4edcd34879a9db79277466a`.
- Compared that branch against canonical `work/28-mcp-tooling-platform`: DIVERGED, 2 commits ahead / 2 behind; one modified contract file.
- Verified that the PR declares architecture baseline only: implementation not approved by the document alone, not deployed, not wired and not released.
- Confirmed the contract's intended ownership split: W70 Work/Gate lifecycle; Core authority and durable ledger; W52 Agent orchestration/ACK; W14 sole Execution Host product; W10 LOCKED / NO CHANGE; W092/W113 read-only projections.

### REVIEW
- Positive: the contract establishes a coherent single-authority boundary, authenticated recipient ACK, scoped grants, online validation before side effects, correlated events, fail-closed behavior and explicit G0–G7 acceptance gates.
- P1: no concrete versioned wire schemas, grant token fields, error taxonomy, ACK proof format or event sequencing contract is provided yet. W28's current grant client and inspected Core HTTP candidate are not wire-compatible.
- P1: W14 sole Host ownership is not mapped to the W28 canonical `execution_host/` source and :8031 server. The contract must identify whether this is W14 source, a W28 adapter, or a second Host implementation to be retired.
- P1: Core candidate provenance is ambiguous across current main, W1111 PR #48, and the distinct W28 canonical `core/execution_authority/` source. Each candidate must be identified by repository, branch, path and exact SHA; no candidate is selected by inference.
- P2: W70 policy version/snapshot consistency and fail-closed behavior for unavailable/stale policy need explicit invariants.
- P2: HostPort needs a minimum normative bidirectional message envelope, cursor/sequence, idempotency, cancellation acknowledgement and close/descendant-exit semantics.

### ACTION / DISPOSITION
- Submitted a formal GitHub COMMENT review on PR #74 (Review ID `6015314554`). No approval or merge authorization was given.
- Requested Xu/Vi to add the concrete contract addendum and source-mapping table, reconcile the PR branch onto the latest canonical Work 28 baseline, and request a fresh independent review.
- No code, endpoint, service, deployment, Core configuration, credential, runtime or release state was changed by this review.
- PR #74 remains a proposed architecture contract; no endpoint, grant adapter, runtime wiring, Host migration or gate transition is authorized by this comment.

**STATUS:** PR #74 REVIEW COMMENT SUBMITTED / ARCHITECTURE DIRECTION POSITIVE WITH P1/P2 CLARIFICATIONS REQUIRED / NOT APPROVED FOR IMPLEMENTATION OR MERGE / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 — JRN-W28-061 — Supplemental WP0 capture provenance and PR drift review

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:16 UTC+07:00  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Review scope:** GitHub-only readback; no listener probes, no PC commands, no deployment changes  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Re-read Work 28 Manifest, Auto E2E Runbook V2.0, Master Execution Plan V2.0, canonical journal, workflow `.github/workflows/work28-mcp-tooling.yml`, PR #33 evidence branch, and PR #74 V1.3 contract branch.
- Runbook V2.0 records exact-SHA CI source `e835a13ae0cddd84a077e17055cd9354a874f212`, 348 unit/regression tests, immutable artifact-level retest 348 tests, Linux lifecycle 13 suspended-spawn tests (4 native-Windows-only cases skipped), Windows lifecycle 17 suspended-spawn tests, and five successful configured jobs in run `41743292650`. The runbook explicitly scopes this to CI preconditions, not deployed MCP/Core/Runtime E2E.
- PR #33 branch `work/28/wp0-evidence-handoff-20261029` compares to canonical as DIVERGED: 6 commits ahead / 246 behind; it is not a current integration candidate.
- Exact PR #33 raw capture `WP0_MCP8030_tools_list_capture_20261029.txt`: blob `7c16429d1732ffa75cdb520c94113d198cbfc602`, 5,022 characters. Parsed JSON-RPC `tools` array contains 17 names: `sandbox_read`, `list_meetings`, `get_meeting`, `get_transcript`, `join_meeting`, `start_meeting`, `add_paste_to_meeting`, `sandbox_create_work`, `sandbox_list_works`, `sandbox_read_probe`, `sandbox_list`, `sandbox_create`, `sandbox_write`, `sandbox_append`, `sandbox_delete`, `get_room_structure`, `get_room_context`.
- Work 28's static registry/stdio contract is 31 tools. The 17-tool capture is therefore not parity evidence for the Work 28 31-tool registry; it may represent a distinct Build MCP composition. The artifact digest proves only the captured bytes, not current process identity, source provenance, handler execution or deployment.
- PR #33 has one prior COMMENT review (no approval); no inline review threads were returned.
- PR #74 branch `xu/w28-core-authority-v1-3-20261123` now compares to canonical as DIVERGED: 2 commits ahead / 3 behind, with one modified contract file. This supersedes the earlier 2-behind count in JRN-W28-060; reconciliation is still required before merge consideration.

### ACTION
- Submitted supplemental GitHub COMMENT review to PR #33, Review ID `6015330414`, recording the exact 17-vs-31 mismatch, stale branch divergence, and evidence limits. No approval or merge authorization was given.
- No source code, runtime process, credentials, endpoint, deployment, or execution gate was changed.
- Preserved the capture as historical integrity evidence only; do not merge PR #33 into the current canonical branch.
- Historical MCP :8020 remains quarantined / DO NOT USE.

### DECISION / NEXT
1. Keep WP0 live provenance and deployed registry parity BLOCKED until the authorized PC collector output is available from the actual MCP 8030 process, capturing process/build identity and raw protocol `tools/list` in the same session.
2. Do not infer that a 17-tool helper capture equals the Work 28 31-tool registry.
3. Xu/Vi must reconcile PR #74 to the latest canonical branch and resolve the concrete wire-schema, W14 Host source mapping, Core candidate provenance, W70 policy-version and HostPort semantics identified in JRN-W28-060.
4. Do not wire the current Work 28 grant client to an unapproved or incompatible Core endpoint. Do not enable WP3-F01 upload without the exact Q4 capability-grant decision.
5. Keep CI precondition PASS separate from deployed E2E. The live MCP 8030 → Core 8000 → approved Runtime → W14 Host chain, protected evidence persistence and authorized checksum readback remain unverified.

**STATUS:** PR #33 HISTORICAL CAPTURE INTEGRITY ONLY / 17-TOOL CAPTURE NOT 31-TOOL PARITY / PR #33 BRANCH 6 AHEAD 246 BEHIND / PR #74 BRANCH 2 AHEAD 3 BEHIND / WP0 LIVE PROVENANCE BLOCKED / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 — JRN-W28-062 — PR #74 branch freshness correction submitted

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:16 UTC+07:00  
**PR:** #74 — Core Execution Authority & Agent-to-Computer Contract V1.3  
**Review ID:** 6015332822 — COMMENT (not APPROVE)  
**Signature:** [KÝ: KA | CSA]

### ACTION
- Submitted a supplemental GitHub COMMENT correcting the branch-freshness count from the initial review. Latest compare: `xu/w28-core-authority-v1-3-20261123` is DIVERGED, 2 commits ahead / 3 commits behind canonical `work/28-mcp-tooling-platform`, with one modified contract file.
- Asked Xu/Vi to reconcile onto the latest canonical baseline, preserve intended V1.3 changes, re-read the exact resulting blob and request fresh review.
- Reaffirmed that P1/P2 contract findings remain open; no merge, implementation, deployment, endpoint wiring or gate transition is approved.

### STATUS
**PR #74 COMMENT REVIEW UPDATED / BRANCH RECONCILIATION REQUIRED / NOT APPROVED / EXECUTION GATE CLOSED / NOT RELEASED.**


## 2026-11-23 — JRN-W28-063 — Implementation-branch freshness, TLS candidate status and CI coverage audit

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 07:23:38 UTC+07:00  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Scope:** GitHub source/branch/workflow audit; no PC/runtime interaction  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Re-read canonical journal (prior blob `a290d5213b9a0b372522632178daee20f22c6bc2`), Work 28 workflow `.github/workflows/work28-mcp-tooling.yml` (blob `8876f1a9096ec54e5a78a073820755087e67ecbf`), grant client, grant model, Execution Host server and grant regression test.
- Exact canonical blobs:
  - `execution_host/work28_core_grant_client.py`: `e330d4f3681d3fb142e559f7ee35b21db128be7e`.
  - `execution_host/work28_grant.py`: `05c082b00a5c38fbdf45950d42211e644f57ed45`.
  - `execution_host/server.py`: `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`.
  - `tests/test_work28_grant.py`: `f30f2a148314b3c3526a62c4193c43219bd89571`.
- Canonical grant test imports grant binding/model and does not import `HttpCoreGrantSource`; no `tests/test_work28_core_grant_client.py` exists at the tested canonical path. Repository code search returned no matches for `core_grant_https_required`, `core_grant_url_invalid`, or `CoreGrantTransportPolicyTests`. Therefore the TLS candidate tests have not been promoted into canonical CI.
- The existing workflow explicitly runs `tests/test_work28_grant.py` in Linux and Windows lifecycle jobs, so a properly integrated client transport regression suite can be added to an existing required lane without inventing a new CI workflow.
- Current canonical grant client still accepts any non-empty URL, attaches an optional Bearer token, and issues GET via `urllib.request.urlopen`; it has no HTTPS-only remote policy, explicit redirect policy, or URL authority validation.
- The review-only TLS candidate branch `ka/work28-core-grant-transport-tls-20261123` compares to canonical as DIVERGED: 2 commits ahead / 4 behind, with only two modified files (`execution_host/work28_core_grant_client.py`, `tests/test_work28_grant.py`). It remains untested and unmerged. Do not treat its tests as canonical coverage.
- Vi implementation branches were checked against the canonical branch:
  - `vi/work28-auto-e2e-integration-20261123`: 0 ahead / 48 behind.
  - `vi/work28-core-authority-doc-consistency-20261123`: 0 ahead / 19 behind.
  - `vi/work28-wp1-schema-binding-hardening-20261123`: 0 ahead / 30 behind.
  - `vi/work28-wp5-core-grant-fail-closed-20261123`: 0 ahead / 40 behind.
  These refs contain no unique commits relative to the current canonical branch and are stale working refs, not pending code deliveries.
- Historical recovery branch `auto/work28-vi-wp2-recovery-20261118` compares DIVERGED 24 ahead / 79 behind, with lifecycle/workflow/source/journal changes. It is not a safe merge candidate; do not merge or cherry-pick wholesale.
- Current GitHub main HEAD observed in the cross-Work trace is `0902cd26518673aa078bb4c7c7899e1e4a95656a`. W17 Entry 053 and GAP Register record exact NOT_FOUND at main for `execution_host/work28_core_grant_client.py`, `execution_host/work28_dispatch.py`, `core/execution_authority/http_server.py`, and `core/execution_authority/authority.py`. Thus the Work 28 implementation is still branch-scoped and not integrated into main. This is not evidence of a deployed service.
- The latest canonical journal-only commit `829b21e5784a3fec8b07c6fd0f64d56b47dbdf1d` has no associated workflow run. The journal-only change is outside the workflow's code/test path filters; no CI result is claimed for it.

### FINDINGS / DISPOSITION
1. **W28-KA-WP5-05 — HIGH: canonical transport regression coverage absent.** The known remote-HTTP/Bearer-token exposure remains in canonical source and is not covered by canonical tests.
2. **W28-KA-GOV-06 — P1: stale Vi working refs.** Four named Vi refs are behind canonical and have no unique commits. Implementation ownership must continue from a fresh branch based on current canonical HEAD; do not assume old branch names represent active delivery.
3. **W28-KA-GOV-07 — P1: Work 28 remains branch-only.** Main does not contain the inspected W28 grant/Core authority source paths. Branch CI is not main integration, and neither proves runtime deployment.
4. The TLS review candidate is a reference for Vi to independently inspect, not an approved patch. Ka has not modified canonical source or promoted the candidate.

### REQUIRED NEXT ACTIONS
- Vi: create/refresh a clean implementation branch from current `work/28-mcp-tooling-platform`; port the reviewed URL policy only after independently inspecting the candidate; add tests for HTTPS remote acceptance, remote HTTP rejection before network I/O, loopback HTTP development allowance, invalid URL/userinfo/query/fragment/port rejection, and credential-safe redirect behavior; run exact-head Linux + Windows CI and provide raw evidence.
- Vi: reconcile the WP1/WP5/Auto E2E work against current canonical before any implementation claim; close or clearly supersede stale refs with explicit evidence, without force-push or broad cherry-pick.
- Xu/Core owner: approve a concrete Core↔W28 wire contract before any endpoint adapter or runtime wiring.
- An: independently reproduce the transport policy tests after a canonical implementation is delivered.
- Ka: re-review exact diff, redirect behavior, error handling, and the final exact-head CI evidence.
- PC-dependent provenance remains queued until Vinh reports PC availability. No PC command is being requested now.

**STATUS:** CANONICAL TLS EXPOSURE STILL OPEN / TRANSPORT TEST COVERAGE MISSING / TLS PATCH CANDIDATE UNTESTED / VI WORKING REFS STALE / W28 NOT IN MAIN / LIVE PC PROVENANCE PENDING / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 — JRN-W28-064 — TLS candidate redirect/credential boundary re-review

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00; GitHub-only review checkpoint)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Review branch:** `ka/work28-core-grant-transport-tls-20261123`  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Re-fetched review-branch client `execution_host/work28_core_grant_client.py`, blob `93203c8b7937804efbfbefafd6cce823135610cb`, and tests `tests/test_work28_grant.py`, blob `38849aa4e3052165d2f71ab2ee5740d8c5ff76ca`.
- Latest branch comparison supersedes JRN-W28-063: review branch is now DIVERGED, 2 commits ahead / 5 behind canonical, with the same two modified paths. It remains a review-only branch and must not be merged wholesale.
- Candidate validates scheme/host, rejects URL userinfo/query/fragment and malformed ports, requires HTTPS for non-loopback remote hosts, and permits HTTP for localhost/127.0.0.1/::1.
- Candidate still constructs a request containing optional `Authorization: Bearer <token>` and calls the default `urllib.request.urlopen()` redirect handler. No explicit redirect policy or redirect regression test is present in the fetched diff.
- The four new policy tests cover remote HTTP rejection, remote HTTPS acceptance, loopback HTTP allowance and malformed URL rejection. They do not exercise same-origin redirects, cross-origin redirects, scheme downgrade, redirect loops, or whether Authorization is retained/forwarded after a redirect.
- A redirect can change the request destination after the initial URL validation. Therefore validating only the configured URL does not establish the destination policy for every network hop. In particular, credential forwarding across an origin change or HTTPS→HTTP downgrade must be prevented by an explicit, tested policy.

### FINDING
**W28-KA-WP5-06 — HIGH: redirect destination and bearer-token forwarding are not constrained.**
- The current candidate does not prove that redirects remain HTTPS and within the approved origin.
- It does not prove that the Bearer token is stripped on cross-origin redirects or that the redirect is rejected before credentials can be sent to a different authority.
- The current four tests are insufficient to close the transport credential-exposure finding. This is a review finding, not a claim that a credential leak has been observed in a live request.

### REQUIRED REMEDIATION / RETEST
1. Prefer disabling automatic redirects for the Core grant client and fail closed on any 3xx unless the approved Core contract explicitly requires redirects.
2. If redirects are required, implement a bounded redirect handler that validates every Location target: HTTPS-only for remote destinations, no userinfo/query/fragment, bounded hop count, and strict same-origin policy; never forward Authorization across origin changes or to a downgraded scheme.
3. Add deterministic local tests with a fake/local HTTP handler proving: redirect is rejected by default; cross-origin redirect cannot receive the Bearer token; HTTPS→HTTP downgrade is rejected; same-origin redirect behavior matches the approved policy; redirect loops/hop limit fail closed. Tests must assert that no second-hop request receives credentials when rejected.
4. Integrate the code and tests on a fresh Vi implementation branch based on the latest canonical head. Run exact-head Linux and Windows CI; provide raw workflow/job evidence. An independently reproduces the security tests; Ka reviews the resulting exact diff and CI.
5. Do not change Core endpoint wiring until Xu/Core owner approves the versioned wire contract.

### DISPOSITION
- No source implementation was changed by this review. No test was executed by Ka; the candidate remains UNTESTED.
- No credential, endpoint, runtime, PC process, deployment or execution gate was touched.
- Do not promote the review branch to canonical and do not infer that the TLS issue is closed.

**STATUS:** TLS URL VALIDATION CANDIDATE PARTIAL / REDIRECT AND CREDENTIAL BOUNDARY OPEN / EXACT-HEAD CI NOT PROVEN / CANONICAL EXPOSURE NOT CLOSED / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 — JRN-W28-065 — Fresh PR inventory, V1.3 contract drift and canonical grant-boundary recheck

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE
- Re-read canonical `execution_host/work28_core_grant_client.py`, blob `e330d4f3681d3fb142e559f7ee35b21db128be7e`. It remains the pre-TLS implementation: any non-empty URL is accepted, optional Bearer token is attached, and `urllib.request.urlopen()` is used without explicit HTTPS-only remote policy or redirect restriction.
- Re-read canonical `execution_host/server.py`, blob `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`. `POST /execute` still accepts `work_context` from the caller body, validates Work only against local `ROOM_HOP_AUTHORIZED_WORKS`, then sets `authorized=True`. This is not authenticated Core-derived WorkContext or proof of principal/Assignment/Gate authority. The previously recorded W28-KA-WP5-03 trust-boundary finding remains open.
- Re-read `.github/workflows/work28-mcp-tooling.yml`, blob `8876f1a9096ec54e5a78a073820755087e67ecbf`. Both Linux and Windows lifecycle jobs execute `tests/test_work28_grant.py`; transport-policy tests added to this file will therefore enter both existing lanes when integrated into the canonical branch and when the workflow triggers.
- Refreshed PR #74 metadata and comparison. PR remains OPEN / DRAFT / UNMERGED, `mergeable=false`; head `a25c74c60a90f177825e5ec35c56f3a8ec7851f7`, canonical base `8b26c5ee8d823d1707af6b51bfe06e147065128a`; DIVERGED 2 ahead / 7 behind, one modified contract file. The earlier 2-ahead / 3-behind value in JRN-W28-062 is superseded.
- Re-read PR #74 reviews/comments: only Ka's two COMMENT reviews exist; no inline review threads and no author response resolving the five findings. The current contract diff remains document-only.
- Refreshed PR #33 comparison: DIVERGED 6 ahead / 250 behind canonical. Its six added files are historical capture/digest/provenance artifacts; no current runtime/build provenance or 31-tool parity is established. Do not merge this stale branch.
- Reconfirmed the review-only TLS branch is DIVERGED 2 ahead / 6 behind after the latest canonical journal commit; it is not a clean integration branch.

### ACTION
- Submitted PR #74 supplemental COMMENT review, ID `6015359749`, correcting branch drift and PR metadata. Requested rebase/reconciliation to latest canonical, resolution of the five architecture/security findings and fresh exact-head review. No approval was submitted.
- No source code, service, endpoint, credential, PC runtime, deployment, branch protection, merge or release state was changed.

### REQUIRED NEXT
1. Vi: implement the TLS/redirect protections on a clean branch from latest canonical, with deterministic credential-forwarding/downgrade/loop tests; run exact-head Linux and Windows CI.
2. Vi: replace caller-controlled WorkContext/authorization with the approved Core-derived principal/Work/Gate/grant binding only after the concrete Core contract is approved; no compatibility shortcut or local allow-list promotion.
3. Xu/Vi: reconcile PR #74 to canonical and address the five review findings before requesting a new review.
4. An: independently reproduce transport and authority-denial regressions after canonical implementation exists.
5. Ka: review exact source diff, CI evidence, Core adapter compatibility and fail-closed behavior.
6. PC-dependent MCP 8030 provenance and live Auto E2E remain queued until Vinh reports PC availability.

**STATUS:** CANONICAL TLS/REDIRECT EXPOSURE OPEN / CALLER-SUPPLIED WORKCONTEXT AUTHORITY GAP OPEN / PR #74 2 AHEAD 7 BEHIND AND DRAFT / PR #33 6 AHEAD 250 BEHIND / LIVE PROVENANCE PENDING / EXECUTION GATE CLOSED / NOT RELEASED.


## 2026-11-23 — JRN-W28-066 — Redirect boundary, caller-controlled authority and branch freshness re-audit

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Pre-entry canonical commit:** `b9010765abb0c224fe96331eb6f6ac725968df29`  
**Signature:** [KÝ: KA | CSA]

### READ / TRACE — exact source snapshots

1. TLS candidate `execution_host/work28_core_grant_client.py`, blob `93203c8b7937804efbfbefafd6cce823135610cb`, branch `ka/work28-core-grant-transport-tls-20261123`:
   - URL validation now rejects remote plaintext HTTP, userinfo, query, fragment, unsupported schemes and malformed ports; loopback HTTP is permitted.
   - `fetch_grants()` still calls the default `urllib.request.urlopen(req, timeout=...)` with an Authorization Bearer header. No explicit redirect handler or redirect destination validation exists in this candidate.
   - Therefore URL validation covers only the configured initial URL; it does not establish the policy for each redirect hop. Finding W28-KA-WP5-06 remains OPEN.

2. TLS candidate `tests/test_work28_grant.py`, blob `38849aa4e3052165d2f71ab2ee5740d8c5ff76ca`:
   - Four `CoreGrantTransportPolicyTests` validate initial URL scheme/host/userinfo/query/fragment/port.
   - No test starts a local redirecting server or fake opener; no test asserts that a second hop cannot receive Authorization; no HTTPS downgrade, cross-origin, same-origin, or redirect-loop behavior is tested.
   - These tests are source inspection only. Ka did not execute them; candidate remains UNTESTED.

3. Canonical `execution_host/work28_core_grant_client.py`, blob `e330d4f3681d3fb142e559f7ee35b21db128be7e`:
   - Still accepts any non-empty URL and uses default `urlopen`; no remote HTTPS enforcement or explicit redirect policy is present in canonical.
   - Candidate hardening has not been integrated.

4. Canonical `execution_host/server.py`, blob `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`:
   - `POST /execute` allows `work_context` in the caller body, requires that object, checks `work_id` only against local `ROOM_HOP_AUTHORIZED_WORKS`, then assigns `work_context['authorized'] = True` before dispatch.
   - This local allow-list plus caller-supplied context is not authenticated Core-derived principal/Work/WP/Gate/Assignment/Task/grant authority. W28-KA-WP5-03 remains OPEN; do not treat this as a verified Core grant boundary.

5. Canonical workflow `.github/workflows/work28-mcp-tooling.yml`, blob `8876f1a9096ec54e5a78a073820755087e67ecbf`:
   - Linux and Windows lifecycle jobs both execute `tests/test_work28_grant.py`; new transport regressions can be covered by both existing lanes after integration and an exact-head workflow run.
   - The workflow's own Auto E2E report explicitly retains deployed MCP→Core→Runtime E2E as BLOCKED, Execution Gate CLOSED and release NOT_RELEASED. CI success alone cannot close the live gate.

### BRANCH / PR FRESHNESS — live compare

- Canonical Work28 base at this audit: `b9010765abb0c224fe96331eb6f6ac725968df29`.
- PR #74 / `xu/w28-core-authority-v1-3-20261123`: DIVERGED **2 ahead / 8 behind**, merge base `29dfc5d6884835a8d3c46bf8509790ed2abe423b`, one contract file changed. PR remains OPEN / DRAFT / UNMERGED / `mergeable=false`. The prior 2/7 comparison in JRN-W28-065 is superseded. Five review findings remain unresolved; no author response or new contract revision was observed.
- PR #33 / `work/28/wp0-evidence-handoff-20261029`: DIVERGED **6 ahead / 251 behind**, six historical evidence files only. The prior 6/250 figure is superseded. No current MCP process/build provenance or 31-tool parity is established; do not merge.
- TLS candidate / `ka/work28-core-grant-transport-tls-20261123`: DIVERGED **2 ahead / 7 behind**, two modified source/test files. It is not a clean integration branch and must not be merged or cherry-picked wholesale.
- Vi WP5 branch / `vi/work28-wp5-core-grant-fail-closed-20261123`: DIVERGED/BEHIND **0 ahead / 43 behind**, no unique commits. It contains no new integration work.
- Recent repository commit inventory did not surface a new W28 source/contract implementation after the previously audited candidate set. This is not proof that no off-repository or local work exists; only GitHub-visible evidence was assessed.

### FINDINGS / DISPOSITION

- **W28-KA-WP5-06 — HIGH / OPEN:** initial TLS URL validation does not constrain redirect hops or credential forwarding; candidate tests omit redirect cases.
- **W28-KA-WP5-03 — HIGH / OPEN:** canonical Host still trusts caller-supplied `work_context` plus a local Work allow-list and sets `authorized=True`; Core-derived authority is not proven.
- **PR #74:** architecture direction may be retained as a proposal, but wire schemas, W14 source ownership, three-way Core provenance, W70 policy snapshot/fail-closed semantics and HostPort envelope still require resolution and exact-head review.
- **PR #33:** historical byte integrity only; no runtime provenance or registry parity.
- No tests were run by Ka; no source implementation was changed; no PC/runtime/endpoint/credential/deployment/branch protection/merge/release mutation occurred.

### REQUIRED NEXT

1. Vi: start from the latest canonical head; implement redirect rejection by default (or a bounded same-origin HTTPS-only policy if explicitly required), and add credential non-forwarding, downgrade, same-origin and loop/hop-limit regressions.
2. Vi/Xu: resolve the approved Core wire contract and replace caller-controlled WorkContext/local allow-list authorization with server-authenticated Core-derived authority; no guessed endpoint translation.
3. Xu/Vi: reconcile PR #74 to latest canonical and answer all five findings; request fresh exact-head review.
4. An: independently reproduce the transport and authority-denial regressions once an integrated source candidate exists.
5. Ka: inspect exact diff, exact-head Linux/Windows jobs, and Core adapter compatibility; do not infer PASS from candidate source alone.
6. PC-dependent MCP 8030 process/build provenance and full live Auto E2E remain queued until Vinh reports PC availability.

**STATUS:** TLS REDIRECT BOUNDARY OPEN / CORE AUTHORITY BOUNDARY OPEN / PR #74 2 AHEAD 8 BEHIND / PR #33 6 AHEAD 251 BEHIND / TLS CANDIDATE 2 AHEAD 7 BEHIND / LIVE PROVENANCE PENDING / EXECUTION GATE CLOSED / ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.


## 2026-11-23 — JRN-W28-067 — CI discovery coverage and local-grant test boundary correction

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Pre-entry canonical commit:** `13a83aa48146e0372b593d514d5bcfa264969dbf`  
**Signature:** [KÝ: KA | CSA]

### NEW EVIDENCE — CI workflow vs grant fail-closed tests

Inspected exact canonical files:

- `tests/test_work28_core_grant_fail_closed.py`, blob `6fecca58c97ffe0f042ead8e6eaedf30e5552d78`.
- `tests/test_work28_dispatch.py`, blob `b40cac9c315e4eaa52802542759c26cfc6a4721e`.
- `.github/workflows/work28-mcp-tooling.yml`, blob `8876f1a9096ec54e5a78a073820755087e67ecbf`.

**Correction to earlier audit wording:** a canonical test module importing `HttpCoreGrantSource` does exist: `tests/test_work28_core_grant_fail_closed.py`. It tests missing Core URL rejection, configured URL selecting the HTTP source, unreachable Core rejection, and server startup failure. It does not test TLS/redirect security or a deployed Core grant exchange. This corrects any earlier statement that implied no canonical test imports the client at all.

**New finding W28-KA-WP5-07 — HIGH / OPEN: fail-closed grant-client test module is not invoked by the checked-in Work28 workflow.**

- The workflow's unit-regression job runs unittest/pytest discovery only under `work/28/MCP-8020-TOOLING-PLATFORM/05_TEST`.
- Linux and Windows lifecycle jobs explicitly invoke `tests/test_work28_grant.py`, dispatch, contract, evidence and other named modules, but neither invokes `tests/test_work28_core_grant_fail_closed.py`.
- No workflow command in the inspected workflow references `test_work28_core_grant_fail_closed.py`.
- Therefore the existence of this test module is not evidence that it runs in the canonical Work28 CI lanes. It may be manually runnable, but exact-head CI coverage is not established.
- Required remediation: add the module to both Linux and Windows lifecycle jobs (or deliberately relocate it into the suite already discovered by the workflow), then verify exact-head workflow run and raw logs show the module executed and passed. Add a workflow-parity assertion so the regression cannot silently fall out of either lane.

### AUTHORITY TEST SEMANTICS — LIMIT

The canonical dispatch tests construct a local in-memory grant with `issue_grant_for_tests`, pass a caller-built `work_context`, and supply a local `grant_registry` to `dispatch_execute`. The HTTP integration tests similarly configure `Handler.grant_registry` in-process. These are useful unit/contract tests for local dispatch and grant behavior, but they do not prove an authenticated Core-issued grant, W70 authoritative policy decision, server-derived principal, or removal of caller-controlled WorkContext from the production HTTP boundary.

The canonical server blob `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83` remains the source of the open W28-KA-WP5-03 authority-boundary finding. Do not elevate local grant-registry tests into Core authority PASS.

### CI / SOURCE DISPOSITION

- Workflow file and tests were inspected from GitHub canonical branch; Ka did not execute tests.
- No workflow run was found associated with the journal-only commit JRN-W28-066; the workflow path filters exclude the journal path. No CI PASS is claimed for the journal update.
- No source or workflow file was modified in this entry. No branch, service, endpoint, credential, deployment, merge or release state changed.
- PR #74 remains OPEN / DRAFT / UNMERGED; five contract findings remain open. PR #33 remains historical evidence only. PC-dependent provenance and live Auto E2E remain pending.

### REQUIRED NEXT

1. Vi: wire `tests/test_work28_core_grant_fail_closed.py` into both Linux and Windows lifecycle jobs, and add a workflow-parity check proving required test modules execute in both lanes.
2. Vi: add redirect-policy tests and implement explicit redirect rejection / constrained same-origin HTTPS redirect behavior before sending credentials.
3. Vi/Xu: replace local registry and caller-supplied WorkContext authority with the approved authenticated Core grant and W70 policy snapshot contract.
4. An: independently verify the test module runs in both lanes and test negative authority/redirect cases after source integration.
5. Ka: review exact source/workflow diff and read raw exact-head logs; do not claim CI coverage from file existence.

**STATUS:** W28-KA-WP5-07 HIGH / OPEN — GRANT FAIL-CLOSED TEST MODULE NOT WIRED INTO CANONICAL WORKFLOW / W28-KA-WP5-03 HIGH / OPEN — CORE AUTHORITY NOT PROVEN / W28-KA-WP5-06 HIGH / OPEN — REDIRECT BOUNDARY NOT PROVEN / EXECUTION GATE CLOSED / ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.


## 2026-11-23 — JRN-W28-068 — Command-mode grant bypass and CI test-discovery boundary

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Pre-entry canonical commit:** `4e2475551cd7e980f7136e8f811189dee80c0ffb`  
**Signature:** [KÝ: KA | CSA]

### NEW FINDING — W28-KA-WP5-08 — HIGH / OPEN: privileged command mode bypasses Core grant validation

Exact canonical source inspected:

- `execution_host/server.py`, blob `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`.
- `execution_host/work28_dispatch.py`, blob `22d5dcd385e301a43fcd0e1c3e901ff2c90abac9`.
- `execution_host/work28_grant.py`, blob `05c082b00a5c38fbdf45950d42211e644f57ed45`.
- `tests/test_work28_dispatch.py`, blob `b40cac9c315e4eaa52802542759c26cfc6a4721e`.

Observed control flow:

1. HTTP `POST /execute` authenticates a shared `X-Room-Hop-Execution-Auth` token, accepts caller-provided `work_context`, checks its Work ID against local `ROOM_HOP_AUTHORIZED_WORKS`, and then sets `work_context['authorized'] = True`.
2. `dispatch_execute()` branches on mode. `work28_snapshot` requires `execution_grant_id`, resolves a server-side registry grant and binds Work/entry/operation/source hash. The `command` branch does not resolve or validate any grant.
3. Command mode is blocked by default because `snapshot_only=True`; however, `main()` explicitly permits trusted deployment environment configuration `ROOM_HOP_SNAPSHOT_ONLY=false` (also 0/no/off) to disable snapshot-only mode. Once disabled, a caller with the shared execution token and allow-listed WorkContext can enter command mode without a Core-issued execution grant.
4. This is a source-level authority bypass path under the privileged opt-out configuration. No evidence was obtained that the opt-out is enabled in any deployed runtime; do not claim a live exploit or current deployment exposure.

**Risk:** the product contract says Core is the sole authority and no MCP-to-arbitrary-shell path. A configuration toggle must not silently convert the Host into a grantless command executor. The secure default is useful defense-in-depth but does not satisfy the invariant if a production configuration can bypass Core grant authorization.

**Required remediation / decision:**
- Prefer removing production command mode entirely; retain it only behind a test-only adapter that cannot be enabled by runtime environment.
- If command mode is a legitimate product requirement, it must use the same authenticated Core-issued grant, principal, Work/WP/Gate/Assignment/Task, purpose, operation, source snapshot, expiry/revocation and audit binding before any process spawn.
- Reject any caller-supplied `authorized` flag and derive all authority fields server-side.
- Add negative HTTP tests with `ROOM_HOP_SNAPSHOT_ONLY=false`: missing grant, forged WorkContext, mismatched Work, expired/revoked grant and unauthorized operation must all fail before process spawn. Add a positive case only after the approved Core contract is implemented.
- Xu must decide the normative command-mode product policy; Ka does not unilaterally alter the architecture.

### CI TEST DISCOVERY — CONFIRMATION / BOUNDARY

Exact workflow `.github/workflows/work28-mcp-tooling.yml`, blob `8876f1a9096ec54e5a78a073820755087e67ecbf` confirms:
- Unit-regression job discovers only `work/28/MCP-8020-TOOLING-PLATFORM/05_TEST` using unittest and pytest.
- Linux and Windows lifecycle jobs invoke explicit `tests/test_work28_*.py` modules; neither invokes root-level `tests/test_work28_core_grant_fail_closed.py`, blob `6fecca58c97ffe0f042ead8e6eaedf30e5552d78`.
- The artifact retest also discovers only Work28 `05_TEST`.
- Thus W28-KA-WP5-07 remains HIGH / OPEN. The file exists and imports `HttpCoreGrantSource`, but the checked-in workflow does not execute it. Its tests also do not exercise TLS redirects or grantless command-mode denial.

### CORRECTION / CURRENT BRANCH FRESHNESS

All compares below use canonical base `4e2475551cd7e980f7136e8f811189dee80c0ffb` (the pre-entry head):
- PR #74: DIVERGED 2 ahead / 10 behind; one contract file. OPEN / DRAFT / UNMERGED; mergeability metadata is not an approval.
- PR #33: DIVERGED 6 ahead / 253 behind; historical evidence files only.
- TLS candidate: DIVERGED 2 ahead / 9 behind; two files. Do not merge/cherry-pick wholesale.
- Vi WP5 branch: 0 ahead / 45 behind; no unique commits.
- Journal Entry 067's prior compare counts are superseded by this exact-base refresh.

### VALIDATION / DISPOSITION

- This is a static GitHub source and workflow review only. Ka did not execute tests, run a server, send HTTP requests, or inspect a live PC/runtime.
- No source/workflow code changed. No branch rebase, merge, force-push, credential, service, endpoint, deployment, branch-protection or release mutation occurred.
- No CI run is claimed for this journal-only update.
- Existing findings remain: W28-KA-WP5-03 caller WorkContext / Core authority gap; W28-KA-WP5-06 TLS redirect boundary; W28-KA-WP5-07 grant fail-closed test omitted from CI; W28-KA-WP5-08 command-mode grant bypass under privileged opt-out.
- PC-dependent MCP 8030 provenance and full live Auto E2E remain pending.

### REQUIRED NEXT

1. Xu: issue an explicit normative decision on whether production command mode is forbidden or must be grant-bound; preserve W14 as sole Host owner and Core as sole authority.
2. Vi: implement fail-closed server-derived authority and remove caller-controlled WorkContext/authorized flag; eliminate the grantless production command-mode opt-out.
3. Vi: add W28 fail-closed, redirect and command-mode negative tests to both Linux and Windows lanes; add workflow parity assertions.
4. An: independently run and review negative authority/redirect/command-mode cases on the integrated exact head.
5. Ka: re-review exact source diff, exact-head CI raw logs, and Core adapter compatibility. Do not infer deployment or PASS from source/CI alone.

**STATUS:** W28-KA-WP5-08 HIGH / OPEN — GRANTLESS COMMAND MODE UNDER PRIVILEGED OPT-OUT / W28-KA-WP5-07 HIGH / OPEN — FAIL-CLOSED TEST MODULE OMITTED FROM WORKFLOW / W28-KA-WP5-03 HIGH / OPEN — CORE AUTHORITY NOT PROVEN / W28-KA-WP5-06 HIGH / OPEN — REDIRECT BOUNDARY NOT PROVEN / EXECUTION GATE CLOSED / ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.


## 2026-11-23 — JRN-W28-069 — Integrated WP5 exact-CI coverage recheck and command-mode policy confirmation

**Role:** Ka | Independent Architecture & Security Reviewer (CSA)  
**Title:** Chief Security Architect — Work 28 independent reviewer  
**Date-time:** 2026-11-23 (UTC+07:00)  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Pre-entry canonical HEAD:** `b1fa4050fbef75e75c93f0fb6f946047fcbbaa88`  
**Pre-entry journal blob:** `ed3d68a542980ffac1223a048d79cfcdb5c2dea5`  
**Signature:** [KÝ: KA | CSA]

### 1. Canonical integration state correction

A fresh exact branch-ref read confirms canonical HEAD `b1fa4050fbef75e75c93f0fb6f946047fcbbaa88`. The owner handoff artifact `06_EVIDENCE/VI_OWNER_HANDOFF_AUTO_E2E_20261123.md` (blob `26fe36c6594dee1a0fb60ac2bd98e48ed87c9497`) records PR #70 WP2, PR #71 WP5, PR #72 WP1 and PR #73 Core authority provenance consistency as merged, with exact PR-head and post-merge CI runs. PR #70–#73 are closed/merged. This supersedes any implication in earlier audit summaries that these three/four integration slices were still merely candidate branches.

This integration status is source/CI only. The handoff explicitly retains product acceptance NOT ACCEPTED, live MCP 8030 → Core 8000 → Runtime → Host 8031 BLOCKED, Execution Gate CLOSED, and NOT_RELEASED.

### 2. W28-KA-WP5-07 — HIGH / OPEN: root fail-closed tests still not executed by canonical workflow

Exact canonical evidence:
- Workflow `.github/workflows/work28-mcp-tooling.yml`, blob `8876f1a9096ec54e5a78a073820755087e67ecbf`.
- Root test module `tests/test_work28_core_grant_fail_closed.py`, blob `6fecca58c97ffe0f042ead8e6eaedf30e5552d78`.
- Workflow unit lane runs unittest/pytest discovery only under `work/28/MCP-8020-TOOLING-PLATFORM/05_TEST`.
- Linux and Windows lifecycle lanes explicitly invoke named `tests/test_work28_*.py` modules; neither invokes `test_work28_core_grant_fail_closed.py`.
- Run #392 / ID `45055750014` exact post-merge WP5 CI: all five jobs SUCCESS. Unit job `137310467705` log ends `348 passed, 238 subtests passed in 9.61s`; Linux lifecycle job `137310467722` completed the explicit named test list. Neither raw log contains the fail-closed module name.
- Run #396 / ID `45060288335` exact post-merge provenance/documentation CI: all five jobs SUCCESS. Unit job `137324446780` log ends `357 passed, 238 subtests passed in 9.94s`; Linux lifecycle job `137324446419` completed the explicit named test list. Neither raw log contains the fail-closed module name.
- Workflow run jobs confirm Windows and Linux lanes completed successfully; source workflow and raw logs confirm no explicit invocation of this root module.

**Disposition:** green configured CI does not close this coverage gap. Finding remains HIGH / OPEN until the module is wired into both OS lanes (or moved into a discovered suite), exact-head CI reruns, and raw logs prove its execution. A workflow parity test should guard against regression.

### 3. W28-KA-WP5-08 — HIGH / OPEN: trusted environment opt-out still permits grantless command mode

PR #71 is merged, but its patch explicitly:
- changes the default `Handler.snapshot_only` and `serve(... snapshot_only=...)` to TRUE;
- requires Core grant URL and removes automatic local file-grant fallback;
- parses `ROOM_HOP_SNAPSHOT_ONLY` so `0/false/no/off` explicitly sets `snapshot_only=False`;
- adds root test `test_explicit_false_requires_trusted_environment_opt_out`, which asserts that `ROOM_HOP_SNAPSHOT_ONLY=false` is passed to `serve(snapshot_only=False)`.

Canonical current source blobs remain:
- `execution_host/server.py`: `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`.
- `execution_host/work28_dispatch.py`: `22d5dcd385e301a43fcd0e1c3e901ff2c90abac9`.
- `execution_host/work28_core_grant_client.py`: `e330d4f3681d3fb142e559f7ee35b21db128be7e`.
- `tests/test_work28_core_grant_fail_closed.py`: `6fecca58c97ffe0f042ead8e6eaedf30e5552d78`.

The server's `POST /execute` still accepts caller-supplied `work_context`, checks only the Work ID against local `ROOM_HOP_AUTHORIZED_WORKS`, then sets `authorized=True`. When trusted deployment config opts out of snapshot-only mode, dispatch `command` mode proceeds without resolving a Core grant. The current source has no Core-issued command grant validation on this branch.

**Risk statement:** this is a grantless command-execution path if the privileged opt-out is configured; no evidence says that setting is enabled in any deployed environment. Do not describe this as a confirmed live exploit. The secure default is defense-in-depth, not proof that every permitted configuration obeys the Core-authority invariant.

**Required disposition:** remove production opt-out / command mode, or require the same authenticated Core grant and server-derived principal/Work/task/assignment/Gate/purpose/action/snapshot/expiry/revocation binding before command-mode process spawn. Add negative HTTP tests proving no spawn for missing/forged/mismatched/expired/revoked grant with the opt-out path exercised.

### 4. PR #74 contract branch freshness

Compare exact against canonical pre-entry HEAD:
- PR #74 remains OPEN / DRAFT / UNMERGED.
- Branch compare: DIVERGED, 2 ahead / 11 behind, one modified contract file.
- Five prior P1/P2 contract findings remain outstanding; no new author resolution was found in the latest fetched PR timeline.
- Do not merge or treat the architecture direction as an interoperable wire contract until Xu reconciles the branch and the versioned schemas, W14 source ownership, three-way Core provenance, W70 policy snapshot/fail-closed semantics and HostPort envelope are addressed.

### 5. Validation and limits

- Static source review, GitHub workflow/job metadata and raw CI job logs only.
- No tests were executed by Ka; no server or live endpoint was called; no PC collector was executed.
- No source, workflow, PR, branch, runtime, credential, endpoint, deployment, or release mutation occurred.
- CI PASS for configured lanes is retained as CI evidence only; it does not establish live Core authorization, deployed MCP provenance, real provider composition, protected evidence readback, or product acceptance.

### 6. Required next

1. Vi: remove grantless production command mode or bind it to the approved Core grant contract; reject caller WorkContext authority and derive identity/Work from trusted Core data.
2. Vi: add `test_work28_core_grant_fail_closed.py` (and command-mode/redirect negative tests) to both Linux and Windows lanes; add workflow-parity assertion.
3. An: independently verify exact-head logs and the negative no-process-spawn tests.
4. Xu: resolve the V1.3 contract branch findings and issue the normative command-mode decision.
5. Ka: review exact source/workflow SHA and logs after integration. PC live provenance remains pending until Vinh reports the PC is available and collector evidence is returned.

**STATUS:** WP2/WP5/WP1/PR73 SOURCE INTEGRATION AND CONFIGURED CI: RECORDED; W28-KA-WP5-03 HIGH / OPEN; W28-KA-WP5-06 HIGH / OPEN; W28-KA-WP5-07 HIGH / OPEN; W28-KA-WP5-08 HIGH / OPEN; PR #74 CONTRACT: OPEN / DRAFT / UNMERGED; LIVE MCP → CORE → RUNTIME E2E: BLOCKED; EXECUTION GATE CLOSED; ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.


## 2026-11-23 — JRN-W28-070 — Canonical branch freshness correction and PR #74 re-review reconciliation

**Name:** Ka  
**Title:** CSA / Independent Architecture & Security Reviewer  
**Date-Time:** 2026-11-23 07:46 +07:00  
**Canonical branch:** `work/28-mcp-tooling-platform`  
**Canonical HEAD before this entry:** `1545c4de4e558e467a76582e2d7196b853019cec`  
**PR #74 head:** `a25c74c60a90f177825e5ec35c56f3a8ec7851f7`

### 1. Current branch and PR freshness

- Direct Git ref read confirms the canonical Work28 branch head before this entry is `1545c4de4e558e467a76582e2d7196b853019cec`; journal content read at this exact commit includes JRN-W28-068 and JRN-W28-069.
- Exact compare canonical `1545c4de4e558e467a76582e2d7196b853019cec` → PR #74 head `a25c74c...`: **DIVERGED — 2 commits ahead / 12 behind**, merge base `29dfc5d6884835a8d3c46bf8509790ed2abe423b`, one modified contract file.
- PR #74 remains OPEN / DRAFT / UNMERGED. PR API's displayed base_sha remains the older merge-base SHA and must not be mistaken for current branch HEAD.
- Review 6015443161 had compared PR head against the older `29dfc5d...` base (2 ahead / 0 behind). That compare was valid for that SHA but stale for current canonical freshness.
- Submitted supplemental COMMENT-only correction review ID `6015449638`, recording the current 2-ahead / 12-behind result. No approval or merge recommendation was issued.

### 2. Exact-head contract findings retained

PR #74 contract blob `85c88a5ac50a6d12e4edcd34879a9db79277466a` remains architecture-only and does not define:
1. P1 — versioned wire schemas, grant claims/token representation, error taxonomy, ACK proof, event sequence/cursor and compatibility rules;
2. P1 — exact W14 source/release ownership mapping for W28 `execution_host/` and :8031;
3. P1 — three-way Core provenance, including distinct W28 `core/execution_authority/` candidate, current main and W1111 PR #48;
4. P2 — W70 policy version/snapshot binding and fail-closed stale/unavailable/mismatch behavior;
5. P2 — normative HostPort message envelope, correlation/sequence, idempotency, cancellation ACK, close and descendant-exit proof.

Review 6015443161 records the detailed findings; review 6015449638 corrects current branch freshness. Both are COMMENT-only.

### 3. Canonical source findings re-confirmed

- `execution_host/server.py` blob `cfdecca58e6146d067ce0e0c0a0feebac0ebdc83`: caller-provided `work_context`, local Work allowlist, and server assignment of `authorized=True` remain.
- `execution_host/work28_dispatch.py` blob `22d5dcd385e301a43fcd0e1c3e901ff2c90abac9`: `command` mode bypasses snapshot grant resolution when `snapshot_only=False`; this is a static source path, not proof of live deployment exposure.
- `ROOM_HOP_SNAPSHOT_ONLY=false` remains a trusted configuration opt-out; live PC value is UNKNOWN.
- `tests/test_work28_core_grant_fail_closed.py` blob `6fecca58c97ffe0f042ead8e6eaedf30e5552d78` is present but the current canonical workflow blob `8876f1a9096ec54e5a78a073820755087e67ecbf` does not invoke it in Linux or Windows lifecycle lanes.
- W28-KA-WP5-03, WP5-06, WP5-07 and WP5-08 remain HIGH / OPEN. No source or workflow change was made by Ka; no tests or live services were executed.

### 4. Validation boundary and next actions

- This pass is GitHub ref, file and PR review evidence only.
- No PC collector, live MCP 8030 tools/list, Core endpoint, Runtime or protected evidence readback was run.
- Vi must reconcile PR #74 only after Xu resolves the contract findings; Vi must remediate caller-controlled authority, grantless command mode, redirect handling and CI test discovery on a fresh canonical base.
- An must independently verify exact-head Linux/Windows raw logs and negative no-side-effect tests.
- Ka will re-review exact source SHA and raw CI evidence after integration.

**STATUS:** PR #74 OPEN / DRAFT / UNMERGED / 2 AHEAD / 12 BEHIND; WP5-03 / WP5-06 / WP5-07 / WP5-08 HIGH / OPEN; LIVE MCP → CORE → RUNTIME E2E BLOCKED; EXECUTION GATE CLOSED; ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.

**Signature:** [KÝ: KA | CSA / INDEPENDENT REVIEWER]


## 2026-11-23 — JRN-W28-071 — Owner-delegated Ka build: fail-closed command and Core transport hardening

**Name:** Ka  
**Title:** BUILD OWNER (owner-delegated) / CSA / Security Implementer  
**Date-Time:** 2026-11-23 09:40 +07:00  
**Repository:** `hqtt2026-thevinhvtqni/room-meeting-ai`  
**Base canonical SHA:** `14a535a6f7d10bb318734cc8df6c76090286ac08`  
**Build branch:** `ka/work28-security-hardening-20261123`

### 1. Explicit owner delegation and scope

Vinh explicitly delegated Ka to build Work 28 autonomously and stated Vi and An are not participating in this phase. This is a temporary owner override for the current build phase; it does not rewrite the historical four-role manifest or assign work to absent participants. Ka performs implementation and self-review; independent QA evidence remains a separate acceptance requirement and is not claimed by Ka.

### 2. Implemented source changes (candidate branch only)

1. `execution_host/work28_dispatch.py`: every `mode=command` request now fails closed with `command_mode_disabled_core_grant_contract_required`, regardless of the `snapshot_only` flag. This removes the grantless command dispatch path from the candidate.
2. `execution_host/server.py`: startup always passes `snapshot_only=True`; legacy `ROOM_HOP_SNAPSHOT_ONLY=false/0/no/off` can no longer opt command mode back in through `main()`.
3. `execution_host/work28_core_grant_client.py`: Core grant URL must be HTTPS, have a hostname, and contain no userinfo, query or fragment; malformed ports are rejected. A custom `HTTPRedirectHandler` refuses all redirects, so bearer authorization is not forwarded to a redirect destination.
4. `tests/test_work28_core_grant_fail_closed.py`: added HTTPS URL validation, rejection of HTTP/userinfo/query/fragment, no-follow redirect handler, unreachable Core and explicit-false startup regressions.
5. `tests/test_work28_dispatch.py`: added a direct dispatch regression proving command mode is rejected even when caller passes `snapshot_only=False`.
6. `.github/workflows/work28-mcp-tooling.yml`: added explicit execution of `test_work28_core_grant_fail_closed.py` in both Linux and Windows lifecycle lanes, with a distinct Windows output log.

### 3. Candidate commit chain

- `205dd2f49c02fd1e7f8fb4cd9685c9b8170ba5c7` — disable ungranted command dispatch.
- `8f36f96ae807973a7107d302fbde21604e5e192e` — remove startup snapshot-only opt-out.
- `16f342c79328835fea7dae491d013f76273a0c07` — require HTTPS and reject redirects.
- `0db032aa09f13c190d72be47f41222fd0b010f1a` — extend Core-grant fail-closed regressions.
- `f3a99f96dee10d82b5eb07165cd11e12fdbdf69c` — run fail-closed tests on Linux and Windows.
- `000dae4fb07f057db3fc42dc8757d248a1001ad2` — test command-mode denial with opt-out flag false.

### 4. Known unresolved authority boundary

This candidate does **not** claim to solve `W28-KA-WP5-03`: `POST /execute` still accepts caller-provided `work_context`, and snapshot dispatch still constructs `WorkContext` from that request after local allowlist checking. A safe replacement requires a normative, versioned Core wire contract and trusted server-side resolution of principal, Work, assignment, gate and grant. No endpoint, schema or claim is guessed here.

The existing static grant registry is fetched at startup; this candidate does not yet prove online revocation/expiry refresh or durable W70 policy snapshot binding. PR #74 contract findings remain a separate prerequisite. No live PC configuration or deployment has been inspected.

### 5. Validation status

- GitHub source writes/readbacks: candidate files were fetched after writes; their blob SHAs are retained in the branch.
- Ka did not execute local Python tests or the PC runner in this pass. GitHub Actions evidence is **PENDING** until a PR run exists and raw Linux/Windows logs show the new test module executing.
- No live MCP 8030, Core 8000, Runtime MCP, W14 Host, protected evidence readback or deployment was exercised.
- No canonical branch, historical PR, credential, endpoint or runtime was mutated. All source changes are isolated on the candidate branch.

### 6. Disposition

- W28-KA-WP5-08: candidate mitigation implemented; remains **PENDING CI/review**, not closed.
- W28-KA-WP5-06: candidate HTTPS + no-redirect hardening implemented; remains **PENDING CI/security tests**, not closed.
- W28-KA-WP5-07: workflow calls fail-closed module on Linux and Windows; remains **PENDING raw CI evidence**.
- W28-KA-WP5-03: **HIGH / OPEN**, caller-controlled WorkContext / Core authority unresolved.
- PR #74 five contract findings: **OPEN**.
- Live MCP → Core → Runtime E2E: **BLOCKED**.

**STATUS:** BUILD CANDIDATE — CI PENDING — INTEGRATION NOT APPROVED — EXECUTION GATE CLOSED — NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]


## 2026-11-23 — JRN-W28-072 — CI #425 failure triage and regression alignment

**Name:** Ka  
**Title:** Owner-delegated BUILD OWNER / CSA  
**Date-Time:** 2026-11-23 09:43 +07:00  
**Workflow run:** `45101824503` / run #425  
**Initial tested SHA:** `121efd7dbc2ff05173d9253fab4fe7941804b5b7`

### 1. Exact CI result

- Unit/regression job: **FAIL**.
- Linux lifecycle job: **FAIL**.
- Windows lifecycle job: **FAIL**.
- Automatic E2E gate report job: SUCCESS, but reports deployed E2E BLOCKED and is not a product PASS.
- Compile step: SUCCESS.
- Both Linux and Windows raw logs show `test_work28_core_grant_fail_closed.py` was actually executed; its 9 tests passed on both OS lanes.

### 2. Root causes from raw logs

1. Existing `tests/test_work28_evidence.py` still supplied `http://` Core URLs. The new HTTPS-only source correctly rejected those fixtures, producing two errors in the WP18 CoreGrantClientTests.
2. Existing Work28 unit test `05_TEST/test_w13_execute_handler_http_boundary.py::test_authenticated_and_authorized_call_reaches_host_with_server_side_authorization` asserted that a caller-supplied WorkContext + local allowlist + `snapshot_only=False` could reach the Host. The new command-mode block correctly returned HTTP 400 instead of the old expected 200. This test encoded the grantless behavior now intentionally removed.

### 3. Corrective changes committed on candidate branch

- Commit `bf0ab07f4c371660d470121ebe2482e664a43a65`: changed WP18 Core URL fixtures to HTTPS.
- Commit `daec39e85e580eb411eb66ded919fa731fde657c`: replaced the legacy HTTP happy-path expectation with an explicit denial + host-never-invoked assertion; updated test description to match the retired command contract.
- These changes are candidate fixes only. They have not yet been re-run by CI at the time of this entry.

### 4. Security disposition

The failures do not justify restoring command mode or allowing HTTP Core grant transport. The test expectations were updated to assert the new fail-closed behavior. WP5-08 and WP5-06 remain PENDING a fresh exact-head CI run.

**STATUS:** CI #425 FAIL; root causes identified; corrective commits pushed; rerun PENDING; WP5-03 HIGH / OPEN; PR #76 DRAFT / UNMERGED; Execution Gate CLOSED; NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]


## 2026-11-23 — JRN-W28-073 — Exact-head CI #427 follow-up: command-denial assertion correction

**Name:** Ka  
**Title:** Owner-delegated BUILD OWNER / CSA  
**Date-Time:** 2026-11-23 09:46 +07:00  
**Workflow run:** `45102006936` / run #427  
**Run source SHA:** `97e255f12fc75af5171b6e682ee9a40850a052db`

### 1. Exact CI result

- Unit/regression job: **SUCCESS** (including Work28 unit/pytest suites).
- Linux lifecycle: **FAIL**.
- Windows lifecycle: **FAIL**.
- Both OS raw logs confirm the newly wired `test_work28_core_grant_fail_closed.py` ran and all 9 tests passed.
- WP18 `test_work28_evidence.py`: all 7 tests passed on both OS.
- WP16 dispatch tests: all 9 tests passed on both OS.
- Remaining failure on both OS: WP19 `tests/test_work28_readback.py::SnapshotOnlyTests.test_command_refused` expected the old error text `snapshot_only`; implementation now returns the more specific unconditional denial `command_mode_disabled_core_grant_contract_required`.

### 2. Corrective change

- Commit `600f291309d202ab906f46eb4bd45625e318bed9`.
- Updated WP19 test to assert the new stable denial code and set `snapshot_only=False`, proving the legacy opt-out does not restore command mode.
- No source behavior was weakened. New exact-head CI rerun is pending.

### 3. Current disposition

- HTTPS + redirect rejection tests: PASS in run #427 on both OS.
- Core grant fail-closed tests: PASS in run #427 on both OS.
- Command mode opt-out denial tests: PASS in run #427; WP19 assertion corrected for rerun.
- Overall lifecycle: NOT PASS until exact-head rerun succeeds.

**STATUS:** RUN #427 UNIT/REGRESSION SUCCESS; LINUX/WINDOWS LIFECYCLE FAIL ON ONE STALE ASSERTION; FIX COMMITTED; RERUN PENDING; EXECUTION GATE CLOSED; NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]


## 2026-11-23 — JRN-W28-074 — Exact merge-candidate CI #429 PASS and immutable artifact

**Name:** Ka  
**Title:** Owner-delegated BUILD OWNER / CSA  
**Date-Time:** 2026-11-23 09:49 +07:00  
**PR:** #76 — OPEN / DRAFT / UNMERGED  
**PR head SHA:** `75b275055488482b6a9e6c83912212d9b5c05f8a`  
**CI run:** `45102189583` / run #429  
**GitHub pull_request merge candidate SHA:** `661e3b7d4706026fa8f3b1da7d7ca28bd613d801`

### 1. Exact workflow result

All five jobs completed SUCCESS:
- `unit-regression-tests`: SUCCESS, including full Work28 pytest suite.
- `execution-host-lifecycle-linux`: SUCCESS.
- `execution-host-lifecycle-windows`: SUCCESS.
- `Build and retest exact-SHA Work 28 source artifact`: SUCCESS.
- `automatic-e2e-gate-report`: SUCCESS.

GitHub generated merge candidate `661e3b7d...` with parents canonical base `14a535a6...` and PR head `75b27505...`. Exact compare canonical base → merge candidate: 13 ahead / 0 behind. This is the tested pull-request merge candidate, not a canonical branch merge.

### 2. Raw log coverage

Both Linux and Windows lifecycle raw logs contain all nine named tests from `test_work28_core_grant_fail_closed.py` and show the module summary as 9 tests / OK. The same lanes also show:
- `test_work28_dispatch.py`: 9 tests / OK;
- `test_work28_evidence.py`: 7 tests / OK;
- `test_work28_readback.py`: 5 tests / OK after the corrected command-denial assertion.

Unit/regression and full pytest jobs also completed SUCCESS. The CI #425 and #427 failures remain preserved in prior entries; the #429 rerun is the successful exact merge-candidate evidence.

### 3. Immutable source artifact

- Artifact: `work28-source-artifact-661e3b7d4706026fa8f3b1da7d7ca28bd613d801`
- Artifact ID: `14785762519`
- Size: 2,306,523 bytes
- SHA-256: `254d51c27df8d1f5c085ac7bb4ba68a1fa720f1008f8428661ee0d4f55c6fae8`
- Artifact job extracted and retested the archive successfully.
- Auto E2E report artifact ID: `14786156325`, SHA-256 `6f472312f527f0a525170104634727b689a4c91df5d4b11a0b7bc5a677959b94`.

### 4. Interpretation and limits

- **CI PASS is confirmed for the exact PR merge candidate.**
- It proves candidate code compiles, configured unit/regression and Linux/Windows lifecycle lanes pass, and the immutable archive was built and retested.
- It does not prove live Core grant issuance/online validation, caller WorkContext authority removal, W70 policy snapshot, live MCP 8030 provenance, Runtime MCP, W14 PC process identity, protected evidence persistence/readback or deployed E2E.
- WP5-08 command-mode mitigation and WP5-06 transport hardening have CI evidence, but remain candidate mitigations pending merge/review and runtime confirmation.
- WP5-07 CI omission is corrected on this candidate; raw logs now prove both OS lanes run the module.
- WP5-03 remains HIGH / OPEN; static grant-registry authorization and caller-supplied WorkContext remain unresolved.
- PR #76 stays DRAFT; no merge or release is performed.

**STATUS:** PR #76 CANDIDATE CI #429 PASS / IMMUTABLE ARTIFACT PASS; WP5-03 HIGH / OPEN; CORE WIRE CONTRACT / LIVE AUTHORITY NOT VERIFIED; EXECUTION GATE CLOSED; ACTIVE — INTEGRATION BLOCKED — NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]


## 2026-11-23 — JRN-W28-075 — Disable unvalidated HTTP snapshot execution and correct readiness semantics

**Name:** Ka  
**Title:** Owner-delegated BUILD OWNER / CSA  
**Date-Time:** 2026-11-23 09:54 +07:00  
**Branch:** ka/work28-security-hardening-20261123  
**Prior exact merge-candidate CI:** run #429 / 45102189583 / PASS  
**New candidate source head:** 7240a0d2d6fd115ddfb86ae7b7624837c76bd84d  
**New CI:** run #435 / 45102801064 / PENDING at entry time

### 1. Security boundary discovered

The previous candidate disabled mode=command, but HTTP work28_snapshot still accepted caller-supplied work_context and a startup-loaded static grant registry. That registry is not online Core validation: it cannot prove current expiry/revocation, trusted caller identity, W70 policy snapshot or that caller-supplied workspace/evidence paths came from Core. A local cached grant must not be treated as authority.

### 2. Containment implemented (candidate branch only)

- execution_host/server.py: HTTP snapshot execution returns 503 core_online_grant_validation_not_configured unless an online Core validator is actually wired. This candidate intentionally wires none, so all protected HTTP snapshot execution is blocked; caller WorkContext is not allowed to reach dispatch.
- main() no longer loads the static grant list as if it were an authority source. It starts in explicit BLOCKED execution mode and passes an empty registry.
- serve() pins snapshot-only true and leaves the Core online validator unset; legacy opt-out cannot enable execution.
- execution_host/work28_readiness.py: health readiness now reports caller WorkContext authority BLOCKED, online Core grant validation BLOCKED, and static grant cache IGNORED rather than PASS. The health response reflects INTEGRATION_BLOCKED, not a false PASS.
- tests/test_work28_dispatch.py: the HTTP snapshot test now proves HTTP 503 and no snapshot directory/side effect without online Core validation.
- tests/test_work28_core_grant_fail_closed.py: startup no longer treats static grants as authority; added readiness regression proving even 99 cached grants cannot satisfy online authority gate.

### 3. Candidate commits

- d6ddcdd47327cf5eb3df57531cb8e96b6f371696 — block HTTP snapshot without Core online validation.
- d648fa8bd5ec71134bd8895108df8222143cd1a5 — correct readiness gate semantics.
- 16d000c5a64ad7b363adc9bb2bfa23a2137d7659 — test startup does not trust static grant cache.
- 1d25173989e1ffbff808ee17f415299346b6d49d — test HTTP snapshot is blocked without online Core.
- bcc9d25636098f73a9f2f737c8236a67d2997303 — mark static grants non-authoritative in readiness.
- 7240a0d2d6fd115ddfb86ae7b7624837c76bd84d — test readiness cannot be satisfied by cached grants.

### 4. Core implementation boundary

- This is fail-closed containment, not completion of online Core authority.
- Work28's proposed Core V1.2 implementation exists under core/execution_authority/ but is not approved/deployed and its current separate HTTP handler does not yet expose the complete Work28 online validation contract.
- Current-main Core :8000 app composition inspected in this pass mounts Meeting routes only; no Work execution-grant router is mounted there.
- PR #48 is a separate open/draft W1111 candidate, not canonical main and not automatically reusable. PR #74 remains open/draft with five wire/ownership/policy/HostPort findings.
- No endpoint, body schema, credential, W70 policy version or Core principal is guessed or wired in this entry.
- To restore execution, next implementation slice must reconcile and version the Core wire contract, implement grant issuance/online validation/revocation/run-record with Work/operation/source/policy binding, derive WorkContext solely from the Core response, and test no-side-effect denial for every invalid grant branch.

### 5. Validation status

- Prior PR merge-candidate CI #429 passed all five jobs on SHA 661e3b7d4706026fa8f3b1da7d7ca28bd613d801; immutable archive and artifact checksums are recorded in JRN-W28-074.
- New changes above are not yet validated by CI. Run #435 is pending; no PASS is claimed for these additional changes.
- No local PC, live MCP 8030, Core 8000, Runtime MCP, W14 Host, deployment or protected evidence readback was executed.

**STATUS:** FAIL-CLOSED HTTP CONTAINMENT IMPLEMENTED / CI #435 PENDING; WP5-03 FUNCTIONAL CORE AUTHORITY REMAINS HIGH / OPEN; WP5-06 TRANSPORT MITIGATION CI #429 PASS; WP5-07 COVERAGE CI #429 PASS; WP5-08 COMMAND MODE MITIGATION CI #429 PASS; EXECUTION GATE CLOSED; NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]


## 2026-11-23 — JRN-W28-076 — CI #435 failure triage: readiness and legacy bootstrap tests

**Name:** Ka  
**Title:** Owner-delegated BUILD OWNER / CSA  
**Date-Time:** 2026-11-23 09:57 +07:00  
**Workflow run:** 45102801064 / run #435  
**Tested source head:** 7240a0d2d6fd115ddfb86ae7b7624837c76bd84d

### 1. Exact CI result

- Unit/regression: FAIL (one legacy bootstrap test error).
- Linux lifecycle: FAIL (two stale readiness expectations).
- Windows lifecycle: FAIL (same two stale readiness expectations).
- The new HTTP containment test passed on both OS: snapshot request received 503 and no snapshot directory was created.
- New Core readiness regression passed: 99 cached grants do not satisfy online Core authority.
- New fail-closed module passed: 10 tests / OK on both OS.
- WP16 dispatch, WP18 evidence and WP19 readback modules passed on both OS.

### 2. Root causes

1. Legacy Work13 bootstrap test still accessed removed server attribute build_grant_source and expected main() to load a static Core grant list. The candidate intentionally removed that authority shortcut.
2. Legacy readiness test still passed obsolete keyword core_grant_url_set and expected /health to return PASS. The candidate intentionally reports INTEGRATION_BLOCKED until online Core validation is wired.

### 3. Corrective test changes

- Commit e0363a4671940783fd02c90ee70bb4f8007023b3: update readiness tests to assert INTEGRATION_BLOCKED, caller WorkContext authority BLOCKED, online Core grant validation BLOCKED and static grant cache IGNORED.
- Commit 3a64249b00f3310e2ec461d984754eeff0aa5888: update legacy W13 bootstrap test to prove main() starts with empty static grant registry and remains BLOCKED even when ROOM_HOP_SNAPSHOT_ONLY=false.
- No source security behavior was relaxed. A new exact-head CI run is pending.

### 4. Disposition

- CI #435 is FAIL; no overall PASS claimed.
- HTTP snapshot containment is proven by the #435 raw logs, but full workflow remains failed on stale tests.
- WP5-03 remains HIGH / OPEN as functional Core authority is not implemented or wired. HTTP execution is intentionally blocked in the candidate until it is.
- WP5-06, WP5-07 and WP5-08 retain prior exact merge-candidate CI #429 PASS evidence; current follow-up candidate requires fresh exact-head CI.

**STATUS:** CI #435 FAIL / TWO LEGACY TEST EXPECTATIONS IDENTIFIED; TEST FIXES COMMITTED; RERUN PENDING; EXECUTION GATE CLOSED; NOT RELEASED.

**Signature:** [KÝ: KA | OWNER-DELEGATED BUILD OWNER / CSA]
