"""ARCHIVED / NON-RUNTIME — DO NOT IMPORT.

This former Work 14 LocalGitProvider directly owned subprocess Git calls. It is retained only as historical provenance for Phase 2 and is not a Work 14 runtime implementation.

Canonical ownership:
  Work 13 Execution Host GitAdapter and authorization boundary.

Current Work 14 path:
  browser_ui_app -> execution_host_bridge -> W13 POST /execute -> authorized Git command.

Any new Git capability must be implemented/injected through Work 13; do not revive this file.
"""
