# Work 05 — G09 Acceptance Test

The default G09 path is Drive Changes polling, not Watch. The sequence is: obtain a real start page token; identify an approved safe document; make one controlled Docs change; poll `changes.list`; map provider ID to Core ID; fetch current Docs state; reconcile into Core :8000; read through MCP :8020; verify audit; replay the event; and store complete evidence. If Watch is selected, channel creation, notification, renewal, and stop evidence become additional gates.

G09 is not REAL GOOGLE PASS unless it runs against Google Docs/Drive with real resource IDs. Offline tests prove only the change/reconcile contract and duplicate-event semantics.
