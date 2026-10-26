#!/usr/bin/env bash
# Work 29 — single validation entrypoint (offline-first)
# NEVER invents RELEASE_PASS / COMPLETED without gates.
set -uo pipefail
STAMP="$(date -u +%Y%m%dT%H%M%SZ 2>/dev/null || date +%Y%m%d_%H%M%S)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
EVID="${ROOT}/06_EVIDENCE"
mkdir -p "$EVID"
LOG="${EVID}/VALIDATION_ENTRYPOINT_${STAMP}.log"
REPORT="${EVID}/VALIDATION_ENTRYPOINT_REPORT_${STAMP}.md"
HANDOFF="${EVID}/QA_HANDOFF_${STAMP}.md"

log(){ echo "$*" | tee -a "$LOG"; }
sha(){ sha256sum "$1" 2>/dev/null | awk '{print $1}' || echo NOHASH; }

log "=== WORK29 VALIDATION $STAMP ROOT=$ROOT ==="
log "PYTHON=$(python3 -V 2>&1)"
FAILED=0

run_step() {
  local name="$1"; shift
  log "--- $name ---"
  set +e
  "$@" >>"$LOG" 2>&1
  local rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then log "STEP $name PASS exit=0"
  else log "STEP $name FAIL exit=$rc"; FAILED=$((FAILED+1)); fi
  return 0
}

run_step unit_tests python3 -m pytest -q tests
run_step no_release_token bash -c '! grep -R "RELEASE_PASS" src tests 2>/dev/null | grep -v Binary'

# integration probes — independent
probe() {
  local name="$1" url="$2"
  set +e
  code=$(curl -sS -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 6 "$url" 2>/dev/null)
  rc=$?
  set -e
  if [[ $rc -ne 0 || "$code" == "000" || "$code" == "404" ]]; then
    log "STEP $name BLOCKED http=$code"
  else
    log "STEP $name PARTIAL http=$code"
  fi
}
probe core_8000 http://127.0.0.1:8000/health
probe mcp_build https://admin-pc.tail7d6101.ts.net/build/mcp

if [[ $FAILED -eq 0 ]]; then
  OFFLINE=OFFLINE_VALIDATION_PASS
  EXIT=0
else
  OFFLINE=OFFLINE_VALIDATION_FAIL
  EXIT=1
fi
INTEG=INTEGRATION_BLOCKED
RELEASE=NO_RELEASE

LOG_SHA=$(sha "$LOG")
{
  echo "# Work 29 Validation Report"
  echo "**Stamp:** $STAMP"
  echo "**Offline:** $OFFLINE"
  echo "**Integration:** $INTEG"
  echo "**RELEASE:** $RELEASE"
  echo "**Exit:** $EXIT"
  echo "**Log SHA-256:** \`$LOG_SHA\`"
  echo ""
  echo "Command: \`bash scripts/run_work29_validation_entrypoint.sh\`"
} > "$REPORT"

{
  echo "# QA Handoff Work 29"
  echo "To: Qw (QA) · Cla (security if providers added)"
  echo "Command: bash scripts/run_work29_validation_entrypoint.sh"
  echo "Go-reported offline=$OFFLINE exit=$EXIT — re-run independently."
  echo "Do not issue RELEASE from offline-only evidence."
} > "$HANDOFF"

log "SUMMARY offline=$OFFLINE integration=$INTEG release=$RELEASE exit=$EXIT log_sha=$LOG_SHA"
exit $EXIT
