# WORK 28 — VI → KA INDEPENDENT SECURITY REVIEW HANDOFF
**Handoff ID:** W28-HO-KA-WP2-RECOVERY-20261118-PR61
**Execution time:** 2026-11-18 05:11:16 UTC+07:00
**From:** Vi | CODER
**To:** Ka | Independent Architecture/Security Reviewer
**Work:** 28 — MCP Tooling Platform / WP2
**PR:** https://github.com/hqtt2026-thevinhvtqni/room-meeting-ai/pull/61
**Branch:** `auto/work28-vi-wp2-recovery-20261118`
**Base SHA:** `8301a7f8fb6a91689482710a9006e2cdbab709c4`
**Current reviewed head at handoff:** `8ad00128de931adf2a3beacc647056dfb4a4663c`

## Review target
- `execution_host/host.py`
- `execution_host/host_run.py`
- `tests/test_wp2_service_mapping_and_race.py`

## Findings addressed
This slice responds to Ka's 2026-11-15 HIGH findings WP2-SVC-01, WP2-SVC-02, WP2-SVC-03 and WP2-EVID-04:
- Retain service registry ownership through cleanup completion; failed cleanup is retryable.
- Drain stale leader descendants before service replacement.
- Serialize registry transitions to prevent duplicate same-name starts and untracked processes.
- Preserve actual suspended-spawn abort/reap evidence instead of emitting a false no-process attestation.

## Required security review
1. Check lock scope, reentrancy, deadlock risk and whether holding the registry lock during spawn/cleanup is acceptable for this host.
2. Confirm a failed cleanup retains the exact ManagedProcess handle and prevents replacement/restart from claiming healthy.
3. Confirm `service_status` is BLOCKED for a dead leader with live or unknown members.
4. Inspect exception paths and ensure a cleanup exception never drops the registry entry or fabricates reaped=true.
5. Verify `attested_cleanup(None)` remains valid only for a proven no-process path; inspect all callers.
6. Review the new evidence structure for truthful fields, especially PID/membership fields intentionally left unknown.
7. Identify any process registry readers/writers outside these three methods that must share the lock.
8. Review compatibility with service shutdown, concurrent start/stop and old unmanaged Popen entries.

## Acceptance boundary
Source review is independent from QA. Do not approve based on PR summary alone. Record exact PR head SHA, reviewed diff, severity-ranked findings, remediation and retest criteria. WP2 remains unaccepted until the findings are closed and An's exact-SHA tests are independently verified.

## Verification status
- Exact source readback and compare were completed by Vi.
- GitHub workflow/status queries returned empty run/status arrays for the observed head; CI is NOT VERIFIED by this handoff.
- No PC or local test was run by Vi in this session.
- No Core/Runtime/Execution Host deployment or live E2E was performed.

**STATUS:** HANDOFF STAGED / KA ACKNOWLEDGEMENT AND INDEPENDENT REVIEW NOT YET OBSERVED.
**Signature:** [KÝ: VI | CODER]
