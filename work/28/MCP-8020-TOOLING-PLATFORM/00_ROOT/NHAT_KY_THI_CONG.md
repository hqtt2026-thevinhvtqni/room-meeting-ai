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
