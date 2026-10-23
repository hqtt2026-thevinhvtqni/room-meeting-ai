"""a2a_ct — Work 51 vertical slice: A2A Coder-Tester pipeline.

Components:
- contract:    WorkContract schema + validation (P1 contract gate)
- states:      task state machine (A2A task states)
- a2a:         minimal A2A-compatible JSON-RPC 2.0 binding (server + client)
- coder_agent: Coder Agent backend (deterministic generator, LLM-pluggable)
- tester_agent: Tester Agent backend (independent verification in sandbox)
- sandbox:     execution sandbox (subprocess, isolated mode, timeout)
- orchestrator: pipeline loop (Coder -> Tester -> feedback -> gate)

Design notes: see 02_ARCHITECTURE/ARCHITECTURE_WORK51.md and DECISION_REGISTER.md.
"""

__version__ = "0.1.0"
