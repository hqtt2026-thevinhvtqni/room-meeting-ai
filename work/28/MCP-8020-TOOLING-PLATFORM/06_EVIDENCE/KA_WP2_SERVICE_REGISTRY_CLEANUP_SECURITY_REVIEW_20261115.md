# WORK 28 — INDEPENDENT WP2 SECURITY REVIEW: SERVICE REGISTRY AND CLEANUP

- **Evidence ID:** KA-W28-WP2-REV-20261115-001
- **Priority / Read order:** P0 / 02
- **Type:** Independent architecture, process-boundary and failure-evidence review
- **Reviewer:** Ka
- **Title:** Chief Security Architect (CSA) — Independent Reviewer
- **Date-time:** 2026-11-15 13:07 UTC+07:00
- **Work:** W28 — MCP Tooling Platform
- **Repository:** hqtt2026-thevinhvtqni/room-meeting-ai
- **Reviewed tree commit:** `8c9ff9d3a8f25faad03f0254954930de2031bedf`
- **Disposition:** **WP2 PARTIAL — HIGH FINDINGS OPEN / NOT ACCEPTED**
- **Execution Gate:** CLOSED
- **OS isolation:** NOT_VERIFIED

## 1. Executive summary

The suspended-spawn implementation in `execution_host/process_job.py` has a sound fail-closed design on static inspection: Windows Job Object creation/configuration precedes `Popen(CREATE_SUSPENDED)`; assignment precedes ResumeThread; failures abort without intentionally resuming the user process. The service path delegates to the same spawn helper, and `start_service()` now maps `JobObjectUnavailable` to a structured BLOCKED response.

However, the host-level service registry and cleanup callers do not preserve the guarantees provided by `ManagedProcess`. Three service lifecycle paths can lose the only cleanup handle, and the execute-command error path can emit a false `process_reaped=true` cleanup attestation after a failed suspended spawn. These are HIGH / RELEASE BLOCKERS.

**Ka does not accept WP2 close-out on this revision.** The code must be corrected and the missing service-registry tests independently verified before WP2 can close. This review does not challenge the positive suspended-spawn design; it identifies defects in its callers and evidence mapping.

## 2. Exact source revisions inspected

The files were fetched at reviewed tree commit `8c9ff9d3a8f25faad03f0254954930de2031bedf`:

| File | Blob SHA | Scope |
|---|---|---|
| `execution_host/host.py` | `ce6eff2ebf7ebfeb5d61463df859e8b4727f1a37` | start/stop/status service registry |
| `execution_host/host_run.py` | `73ef846748441489cc565da4b837449bb5317e42` | execute-command spawn/error/cleanup result |
| `execution_host/process_job.py` | `85f4866df7710aa2ad0fe1601ae319c470f1718a` | suspended spawn and process-tree cleanup |
| `execution_host/host_cleanup_bridge.py` | `5fd3455e90ec0249051bfb6ac86924b7aec63a02` | cleanup attestation bridge |
| `tests/test_wp2_service_mapping_and_race.py` | `a75958a070d7a49d70e2cde915f53d50ea545af5` | service mapping and spawn/cleanup tests |
| `tests/test_process_job_suspended_spawn.py` | `831691a44a56d8634a4b13243d664b21b47f64ae` | suspended-spawn and native Windows marker tests |
| `tests/test_process_job.py` | `f7fef2ffbf3c22c215ca602766a1d001309df386` | process-tree cleanup tests |
| `tests/test_process_job_gate.py` | `ebe12d02d00d2b7bfa17dae49400bbba8acd6855` | execution gate tests |
| `tests/test_execution_host.py` | `dcd65a5459f7c3338e929e4934984d7e43b6bfea` | host/service lifecycle tests |

The reviewed commit `8c9ff9d3...` is documented as restoring journal lines; the Work journal states that its tree includes the earlier service mapping change and race tests. The commit diff itself is documentation-only; the table above pins the actual source/test blobs read from that tree.

## 3. Positive findings — suspended spawn

Static review confirms:
1. Windows creates and configures the Job Object with KILL_ON_JOB_CLOSE before process creation.
2. Windows creates the process with CREATE_SUSPENDED.
3. Job assignment occurs before ResumeThread; if assignment or resume fails, the candidate aborts the suspended process and raises `JobObjectUnavailable`.
4. `spawn_managed()` and `spawn_managed_service()` share `_spawn()`; the service path uses DEVNULL streams and does not bypass the suspended-spawn ordering.
5. Unknown Job membership remains `None`; a failed drain query is not treated as zero members.
6. The validation module contains native-Windows-only marker tests for command spawn, service spawn, assignment failure and resume failure, in addition to mocked failure-injection tests.

These are positive source/design findings only. Ka did not run the suite or operate a Windows runner in this review. The canonical journal reports GitHub Actions run #327 as successful on the reviewed code-bearing tree, but this session's GitHub workflow/status queries returned empty arrays for commit `8c9ff9d3...`; therefore the run result is recorded as **reported in the journal, not independently revalidated here**.

## 4. HIGH findings

### WP2-SVC-01 — stop_service loses the cleanup handle before cleanup succeeds

**Source:** `ExecutionHost.stop_service()` in `execution_host/host.py`.

The method executes `self.processes.pop(name, None)` before calling `managed.cleanup()`. If cleanup returns `process_reaped=False` (for example, a Job query/drain timeout, a surviving child, or a failed kill), the method returns FAILED but the ManagedProcess is no longer in the registry. A subsequent stop call finds no entry and returns STOPPED, even though the previous cleanup was not proven complete. The only handle capable of retrying Job/process-group cleanup has been discarded.

**Required:** retain the ManagedProcess until cleanup is positively verified; on failure keep an explicit STOPPING/BLOCKED registry state and allow safe retry. Never convert a failed cleanup into a later STOPPED result merely because the registry entry was removed.

### WP2-SVC-02 — start_service overwrites an exited leader without draining surviving children

**Source:** `ExecutionHost.start_service()` in `execution_host/host.py`.

The existing-service check only treats `existing.poll() is None` as running. If the leader has exited while one or more Job Object/process-group members remain, the condition is false and the method spawns a new service, then overwrites `self.processes[name]` without calling `existing.cleanup()`. The `ManagedProcess.cleanup()` implementation explicitly supports the leader-exited/child-alive case, but this caller skips it. The old Job handle/process-group reference can be lost while descendants remain.

**Required:** before replacing any existing registry entry, call cleanup and verify the process tree/Job is drained. If cleanup is uncertain or fails, return BLOCKED and preserve the old handle; do not start a replacement service.

### WP2-SVC-03 — concurrent same-name service starts race the process registry

**Source:** `ExecutionHost.start_service()`, `service_status()`, `stop_service()`; `self.processes` is a plain dict with no per-name or registry lock.

Two concurrent calls for the same service name can both observe no active entry, both spawn a process, then both assign the same dictionary key. The last assignment wins; the other ManagedProcess becomes untracked. A later stop cleans only the stored process. The current concurrency test exercises direct `spawn_managed()` + cleanup in separate threads; it does not exercise concurrent `ExecutionHost.start_service()` on a shared registry.

**Required:** serialize check → stale-entry cleanup → spawn → register for each service name, and coordinate stop/status transitions. Add a same-name concurrent start test that proves one authoritative service entry and no untracked process tree.

### WP2-EVID-04 — execute-command reports a false cleanup attestation after spawn failure

**Source:** `run_execute_command()` in `execution_host/host_run.py` and `attested_cleanup(None)` in `host_cleanup_bridge.py`.

If `spawn_managed()` raises `JobObjectUnavailable`, the exception carries `process_reaped` from `_abort_suspended()`. The local `managed` variable remains None; the generic OSError handler records BLOCKED but does not preserve the exception's `process_reaped` value. The final result then calls `attested_cleanup(managed)`; for None, that helper returns `process_reaped=True` with note `no_process`.

If the suspended process abort was not confirmed reaped, the result can therefore say BLOCKED while simultaneously reporting cleanup as reaped=true. This is false/incomplete evidence and can hide an orphaned suspended process.

**Required:** preserve the original spawn exception and its `process_reaped` / failure notes in the result. `attested_cleanup(None)` is valid only when the caller can prove no process was created. A failed/uncertain abort must remain cleanup BLOCKED/false, never PASS.

## 5. Additional gaps

1. `test_wp2_service_mapping_and_race.py` contains five tests: containment failure mapping, blocked-start retry, repeated direct spawn/cleanup, exited-process direct cleanup, and concurrent direct spawn/cleanup. It does not test the shared host registry, same-name start races, leader-exit/child-alive replacement, or stop cleanup retry.
2. `tests/test_execution_host.py::test_service_lifecycle` is a simple start/stop case; it does not inject cleanup failure or leave a child after leader exit.
3. `start_service()` catches `JobObjectUnavailable` but not other `OSError` raised by the spawn path. The HTTP handler has a broad outer exception mapping, but direct callers can still receive an unstructured exception. Add a deliberate mapping test and preserve the distinction between spawn failure and containment failure.
4. `service_status()` checks only leader `poll()`; it does not prove service readiness or health. A PASS here must be interpreted as process alive, not application ready.
5. `ISOLATION_STATUS` remains NOT_VERIFIED. Job Object/process-group containment is not OS sandbox isolation.

## 6. Required patch and regression matrix

Vi should address these in one coherent WP2 service-lifecycle patch:
- retain registry handles on cleanup failure and support retry;
- drain stale leader-exited process trees before replacement;
- add per-service synchronization for start/stop and registry mutation;
- preserve abort `process_reaped` and notes from spawn exceptions in execute evidence;
- normalize remaining spawn OSError paths without claiming containment success.

Required tests on exact candidate SHA:
1. same-name concurrent start: no duplicate/untracked process;
2. leader exits while child remains; restart must drain or BLOCK, never overwrite the old handle;
3. stop cleanup failure retains handle; a second stop retries and reports the true final state;
4. Job assignment/resume failure with abort reaped=true and abort reaped=false both produce accurate cleanup evidence;
5. service spawn native Windows marker remains absent until Job assignment and resume;
6. assignment/resume failure marker remains absent and process is confirmed reaped or explicitly BLOCKED;
7. POSIX parent-exit/child-alive process-group cleanup and concurrent service start/stop;
8. full Linux and native Windows Work 28 CI on the exact integration SHA; independent An reproduction.

## 7. CI and verification disposition

- Canonical journal JRN-W28-017 reports run #327 SUCCESS on commit `8c9ff9d`, including Windows and Linux lifecycle jobs.
- Independent connector lookup for workflow runs and combined commit status on full SHA `8c9ff9d3a8f25faad03f0254954930de2031bedf` returned no records in this review. This is not a CI failure; it means Ka could not independently retrieve the run details in this session.
- No tests were executed by Ka in this review.
- Native Windows test functions exist in source; native execution is not independently reproduced here.

## 8. Decision and next handoff

**Ka disposition:** WP2 suspended-spawn source design = STATIC REVIEW POSITIVE. WP2 service lifecycle and cleanup evidence = HIGH / OPEN. **WP2 NOT ACCEPTED / NOT CLOSED** until WP2-SVC-01 through WP2-EVID-04 are fixed and independently tested.

- **Xu:** retain WP2 as open/release-blocking; coordinate Vi's patch and An's independent retest.
- **Vi:** implement the service-registry/cleanup corrections and provide exact commit SHA, changed-file blob SHAs and CI run evidence.
- **An:** independently reproduce on native Windows and Linux after the patch; specifically test same-name concurrency, leader-exit/child-alive and cleanup retry.
- **Ka:** review the exact patched blobs and verify that no false cleanup PASS or untracked service path remains.

No production listener was probed, restarted or modified. No execution gate was opened. No OS-isolation claim is made.

**Current Work:** ACTIVE / INTEGRATION BLOCKED / NOT RELEASED. Execution Gate CLOSED.

**[KÝ: KA | CSA / INDEPENDENT REVIEWER]**
