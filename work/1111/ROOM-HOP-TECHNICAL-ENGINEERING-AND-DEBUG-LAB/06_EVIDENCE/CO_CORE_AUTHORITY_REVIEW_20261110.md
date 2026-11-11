# W1111 — CO CORE AUTHORITY REVIEW / THREE-AGENT ASSIGNMENT

**TÊN:** Co  
**CHỨC DANH:** Technical Execution Assistant / Coder W1111 — Core Authorization  
**NGÀY:** 2026-11-10  
**GIỜ - PHÚT:** 13:36 UTC+7  
**Task:** Co ownership in THREE_AGENT_END_TO_END_REASSIGNMENT_20261110.md  
**Disposition:** PARTIAL — CORE SOURCE TRACE COMPLETE; PROTECTED SOURCE CHANGE BLOCKED; LIVE E2E NOT VERIFIED

## 1. Scope and methods

- Read Sandbox canonical files: WORK_MANIFEST.md, AI_WORKING_RULES.md, AUTONOMOUS_E2E_EXECUTION_MODE.md, NHAT_KY_THI_CONG.md, TECHNICAL_BASELINE_AND_OPEN_BLOCKERS.md, CLA_TASK_ASSIGNMENT_TO_CO_20261109.md, APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md, DOC-010_REVISION-LEDGER_SOURCE-OF-TRUTH.md, THREE_AGENT_END_TO_END_REASSIGNMENT_20261110.md, C07 evidence.
- Used ROOM-HOP MCP 8030 sandbox_list / sandbox_read_probe for Work 1111. Note: sandbox_read returned empty objects in this session; sandbox_read_probe returned status=ok and full file_content. No content was inferred from empty read responses.
- Used GitHub connector read-only: PR #48 metadata, changed-file list, branch-vs-main compare, exact branch file fetches, workflow-run lookup and combined status.
- No source, Git, PC, runtime, credential, PR metadata, merge or deployment mutation.

## 2. Current GitHub snapshot — exact observed state

Repository: hqtt2026-thevinhvtqni/room-meeting-ai  
PR: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/48  
PR #48: OPEN, DRAFT, merged=false, mergeable=false.  
Head branch: work/w1111-core-execution-authority-v1-2  
Exact head SHA observed from PR metadata: 647d4aa2b159a9e4dacd86d8b71fe68e820deab5  
PR reports 115 commits; 61 changed files.  
Branch compare against main: status=diverged, ahead_by=115, behind_by=113. This is a material integration/reconciliation risk; do not infer that the branch is safely current with main.

Exact-HEAD CI recheck:
- fetch_commit_workflow_runs(647d4aa2b159a9e4dacd86d8b71fe68e820deab5) returned workflow_runs=[].
- get_commit_combined_status(647d4aa2b159a9e4dacd86d8b71fe68e820deab5) returned statuses=[].
- PR body contains older CI claims (including runs 42454767666 and 42732254869 on other SHAs). Those claims do not establish CI for current HEAD 647d4aa.
- Current disposition: EXACT_HEAD_CI = NOT FOUND / NOT VERIFIED. Do not claim current HEAD CI PASS.

## 3. Core source trace — exact branch blob revisions

Fetched from ref=work/w1111-core-execution-authority-v1-2:
- core/execution_authority.py — blob 163b126178b67c6e0a3f68ba33eaf7b9e6d91503
- room_hop_mcp/adapter/execution_authority_http.py — blob 8cb21fadf6bf2318f4884d368b77f2abf796b807
- room_hop_mcp/adapter/http_server.py — blob 48e05c0f5d8121e35ba9bea01ebd8f338529073c
- room_hop_mcp/core_http_main.py — blob d990dd2e152e487c678f67e27add4c0ac94fef53
- tests/test_execution_authority.py — blob 4ea5158c07df1e66183a6fbe7a6f79042332605d
- tests/test_core_http_main.py — blob 4ffa0f9a977f53387b3350644da02a68ac89890d

## 4. Findings — Core ownership

### C-CORE-01 — Run record accepts a source hash different from the grant policy hash (HIGH)

In core/execution_authority.py, issue_grant returns policy['source_sha256'] but the GRANT_ISSUED event does not persist the source hash or an immutable policy snapshot. validate_grant_token returns source_sha256 by looking up the current mutable in-memory Work policy. record_run validates only that the submitted source_sha256 is syntactically 64-hex; it does not compare it to the source hash bound to the grant.

Direct corroborating test: tests/test_execution_authority.py::test_run_record_links_grant_source_exit_and_evidence configures the Work policy with source_sha256='a'*64, then records source_sha256='b'*64 and expects success. Therefore the current test suite explicitly accepts a mismatched source revision as a successful durable run record.

Impact: the Core durable record can attest a source hash different from the hash authorized for that grant. This violates the required grant/source binding and makes the journal insufficient as proof that the recorded run used the authorized Work snapshot.

Required remediation (not applied): persist the immutable source snapshot/policy revision in GRANT_ISSUED; on validate and record, require the submitted run hash to equal the grant-bound hash; add negative mismatch tests at authority and HTTP boundary; preserve fail-closed behavior if the policy revision is missing or changed.

### C-CORE-02 — No task/assignment/owner-ACK state is bound into authority (HIGH / contract gap)

The current Core grant model binds service identity, Work ID, purpose, expiry and timeout. It does not carry a Task/Assignment ID, task owner, ACK/claim state, assignment state or assignment revocation/version. This does not satisfy the three-agent assignment's requested verification that authenticated principal, exact Work + Task/Assignment, owner/ACK/state/revocation and action/resource are bound together.

Required remediation: define and approve the authoritative assignment contract before implementation; test missing, mismatched, unclaimed, revoked and stale assignment state. Do not invent an assignment registry or accept caller-supplied ACK booleans.

### C-CORE-03 — Grant revocation and run-record append are not one atomic state transition (RISK)

record_run validates the token, reads grant events, then separately appends RUN_RECORDED. Revocation uses a separate read/status check and append. There is no transaction/lock spanning final grant-state validation and run append. A concurrent revoke may race with run recording. This needs a concurrency test and a serialized atomic store operation or equivalent state transition.

### C-CORE-04 — Runtime configuration and Core startup remain unproven

ExecutionAuthority.from_env requires all of:
ROOM_HOP_EXECUTION_IDENTITIES_JSON,
ROOM_HOP_EXECUTION_WORKS_JSON,
ROOM_HOP_EXECUTION_STORE_PATH.
Missing configuration fails closed with execution_authority_not_configured. The deployment document states room_hop_mcp.core_http_main is not yet wired into the existing start-dev.ps1 / live Core PID. No runtime configuration values were read, no secret was accessed, and no endpoint was called. Therefore Core service identity enrollment, Work 1111 policy, persistent store path, active Core mount and durable journal are NOT VERIFIED.

### C-CORE-05 — Grant policy has Work-level scope only

The current policy uses work_id, allowed_identities, allowed_purposes, workspace paths and source_sha256. There is no task-level action/resource allow-list, assignment state or expiry/replay binding to a task. The HTTP routes enforce service credential on grant issuance/status and bearer token on validate/run/revoke, but that does not by itself establish per-task authorization.

## 5. Authority gate — no protected changes made

APPROVAL_RECORD_CORE_EXEC_AUTHORITY_V1_2_DRAFT.md states DR-1 through DR-4 are PENDING explicit confirmation by Anh Vinh and explicitly says not to infer approval from historical instruction, draft, branch, CI or this record. The three-agent prompt also retains DOC-117 and forbids protected source mutation, CI dispatch, PC/runner operation, restart, merge/deploy, secret access or destructive action until exact task-scoped authorization is verified.

Accordingly, this review is read-only. No code/test change was made, no CI was dispatched, no Git branch was changed, no secret/config values were read, and no live request was sent. This is not a refusal to continue; it is the precise authorization boundary.

## 6. Required next actions / dependencies

1. Human owner: explicit decision on DR-1..DR-4 and ordered gates in the approval record; this is a reserved authority decision, not something Co may self-approve.
2. Core: once authorized, fix immutable grant-to-source binding and add negative mismatch tests; address assignment/task binding and atomic revoke/record semantics in the approved contract.
3. Xuco: independently prove real Gateway/MCP caller identity and protected Sandbox mutation enforcement; do not assume file-only MCP 8030 is a process runner.
4. Vi: independently prove W13/W12 grant validation, process boundary, nested failure propagation, FINAL_RESULT and Core callback failure behavior.
5. Integration: reconcile PR #48's 115-ahead/113-behind divergence against main before relying on branch/PR integration. Obtain exact-HEAD CI run/status for 647d4aa; older run IDs are not substitutes.
6. PC: only after approval, provide one consolidated read-only/runtime handoff for actual Core launcher/PID/module path/config presence and Host identity. No secret values in chat.

## 7. Status

- Core source/call-site trace: PARTIAL COMPLETE (read-only).
- C-CORE-01 source/hash binding: DEFECT FOUND.
- C-CORE-02 task/assignment authorization: CONTRACT GAP FOUND.
- C-CORE-03 revoke/run atomicity: RISK FOUND, concurrency proof absent.
- Core live configuration/startup/durable journal: NOT VERIFIED.
- Current PR #48 exact-HEAD CI: NOT FOUND / NOT VERIFIED.
- Protected source remediation: BLOCKED pending explicit authority confirmation.
- Overall Work 1111 Core → Gateway/Execution Host → Sandbox → durable result/GitHub: BLOCKED / NOT VERIFIED.

**Handoff:** READY FOR CLA REVIEW of this read-only Core trace; not DONE, not PASS, not production accepted.
