# WORK 10 — CROSS-PLATFORM VERIFICATION EVIDENCE — RUN 52

- Document ID: W10-CROSS-PLATFORM-CI-EVIDENCE-20261122-RUN52
- Work: 10 — COMPUTER-AGENT
- Workflow: Work 10 Cross-Platform Verification
- Run ID: 44959557526
- Run number: 52
- Tested commit: `843a532d2c08bc4bbd404fcd165ff5d619c130f6`
- Branch: `work/10-computer-agent-mirror`
- Run URL: https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/actions/runs/44959557526
- Result: SUCCESS — both matrix jobs completed successfully.

## 1. Ubuntu 24.04 job

- Job ID: `137015152884`
- Syntax check: SUCCESS
- Real Chromium E2E: SUCCESS
- Regression suites:
  - offline_contract_p0_p5: 60 PASS / 0 FAIL
  - safety_policy_negative: 41 PASS / 0 FAIL / 2 expected SKIP
  - http_api: 52 PASS / 0 FAIL
  - process_containment: 2 PASS / 0 FAIL
  - host_operations: 12 PASS / 0 FAIL
  - acceptance_validator: 16 PASS / 0 FAIL
- Total: **183 PASS / 0 FAIL / 2 SKIP**
- Chromium E2E screenshot retained; process supervisor evidence reported `LIMITED_NOT_CGROUP_V2`, process-group empty verified.

Artifact:
- ID: `14728674665`
- Name: `work10-evidence-Linux`
- Size: 40,050 bytes
- ZIP SHA-256: `2d6338874ff0977c9e47a51e5a21bfbc87b45a159e90a288558b11a070b79b75`

## 2. Windows Server 2022 job

- Job ID: `137015153031`
- Syntax check: SUCCESS
- Real Chromium E2E: SUCCESS
- Regression suites:
  - offline_contract_p0_p5: 60 PASS / 0 FAIL
  - safety_policy_negative: 45 PASS / 0 FAIL
  - http_api: 52 PASS / 0 FAIL
  - process_containment: 2 PASS / 0 FAIL
  - host_operations: 14 PASS / 0 FAIL
  - acceptance_validator: 16 PASS / 0 FAIL
- Total: **189 PASS / 0 FAIL / 0 SKIP**
- Windows process evidence reports profile `windows-job-object-kill-on-close-v1`, active processes after cleanup = 0, containment empty verified.
- Real Chromium E2E ran through the HTTP API and ProcessSupervisor; screenshot retained.

Artifact:
- ID: `14729430156`
- Name: `work10-evidence-Windows`
- Size: 33,928 bytes
- ZIP SHA-256: `7cd16b4fdda217a9d4b1bdcba37b4d30a822891b1ebbd7859ea393d0921099a2`

## 3. Failed predecessor run #51

Run #51 (ID `44959501929`, commit `af889b8c178a40ab1e42433bf7bb06ce8e2287b7`) failed on both matrix jobs because the `http_api` and `acceptance_validator` suite subprocesses exited non-zero before emitting individual PASS/FAIL checks. Chromium E2E, syntax, offline contract, safety and containment steps had passed. Run #52 is the next commit and passed all suites. The exact subprocess stderr for #51 was not present in the job summary log; do not invent a specific root cause.

## 4. Scope and limitations

- This is hosted CI evidence for the exact tested commit above, not evidence from the Owner's physical Windows 10 PC.
- Windows Server 2022 validates the Windows Job Object implementation on a hosted runner; local Windows 10 startup, ACL, Chrome profile, PowerShell configuration and repository-root behavior remain unverified.
- Linux process-group profile is explicitly limited; cgroup-v2 production containment remains NOT IMPLEMENTED.
- Run #52 tested the GitHub branch snapshot before the additional policy-catalog/version hardening in Sandbox's `acceptance_validator.py`. That hardening has since been mirrored to GitHub as commit `29daa718509b1c3906527a8cd9358104061e3b85`; its cross-platform CI is Run #53 and was IN_PROGRESS when this report was authored. Do not attribute Run #52 to the newer commit.
- Production HMAC key and pinned hashes are not provisioned on the Owner PC. CI's test key is unit-test-only and is not production trust configuration.
- No ROOM-HOP Dashboard / PC Bridge integrated E2E is established by this run.

## 5. Disposition

- Hosted cross-platform browser/API/process/host-operation regression: **PASS — RUN 52**.
- V8 semantic validator unit suite: **16 PASS on each OS in Run 52**.
- Linux hardened cgroup-v2 profile: **OPEN / NOT IMPLEMENTED**.
- Physical Windows 10 PC: **NOT RUN**.
- Production HMAC key provisioning: **NOT DONE**.
- ROOM-HOP integration: **OPEN**.
- Full Sandbox↔GitHub parity: **RECHECK IN PROGRESS**.
- Work 10: **ACTIVE — NOT RELEASED**. No main merge or production release.

**KÝ: Co | AI-07 / End-to-End Architecture & Implementation Lead**
