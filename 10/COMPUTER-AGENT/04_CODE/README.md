# 04_CODE — COMPUTER AGENT V1

This is a new implementation built from the Work 10 specification.

Do not treat 01_ORIGINAL/index.html as the implementation source.

Initial module boundary:
- agent_api.py — HTTP API contract
- agent_runtime.py — action execution + verification loop
- browser_adapter.py — browser control boundary
- models.py — typed request/result contracts

Implementation must remain observable and testable.
