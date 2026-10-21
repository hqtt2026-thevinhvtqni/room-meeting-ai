# WORK 10 — DASHBOARD

The Dashboard is a control/presentation layer only.

It must show:
- Agent status
- current task
- live action stream
- observation/screenshot
- PASS / FAIL / BLOCKED
- evidence
- start/stop controls

It must never fabricate agent state or success.

Implementation will call the Agent API rather than embedding browser-control logic in the UI.
