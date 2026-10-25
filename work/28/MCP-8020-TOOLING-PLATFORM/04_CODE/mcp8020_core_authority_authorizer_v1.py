"""Core-authority authorizer bridge for the authorized execution adapter.

Contract V1.2 cross-check (Core vs W12/W13, 2026-10-25) found a real drift:
the Work 28 execution contract accepts free-form work ids (e.g. "work28"),
while the Core execution authority registry pins the canonical form
W<number> (W[0-9]+) and answers anything else with unknown_work. The
adapter's CoreAuthorizer protocol also had no Core-backed implementation.

This module closes exactly that gap, fail-closed, WITHOUT wiring anything
into MCP registration or the v54 catalog:

* require_core_canonical_work_id refuses any work id that the Core
  authority registry could never accept, BEFORE the request reaches Core.
* CoreAuthorityAuthorizer implements the adapter's CoreAuthorizer protocol
  on top of the Core ExecutionAuthority (DR-1 enrolled identities,
  per-Work allowed_identities). It never sees or stores credential
  values: the caller context supplies the credential, the authority keeps
  only SHA-256 digests, and denials return False without detail leaks.

STAGED and NOT WIRED: flipping the v54 execution tools to IMPLEMENTED
still requires deployment and E2E evidence per the Work 28 gate rules.
"""
from __future__ import annotations

import re
from typing import Any, Callable

_CORE_CANONICAL_WORK_ID_RE = re.compile(r"W[0-9]+")


class CoreWorkIdError(ValueError):
    """Raised when a work id is not in the Core-canonical W<number> form."""


def require_core_canonical_work_id(work_id: Any) -> str:
    """Return the work id unchanged only if it is Core-canonical W<number>."""
    if not isinstance(work_id, str) or not _CORE_CANONICAL_WORK_ID_RE.fullmatch(work_id):
        raise CoreWorkIdError(
            "work id must match the Core canonical form W<number>; "
            "free-form work ids are refused before reaching Core"
        )
    return work_id


class CoreAuthorityAuthorizer:
    """CoreAuthorizer protocol backed by the Core ExecutionAuthority.

    authorize(trusted_caller, work_id) returns True only when the caller's
    credential authenticates as an enrolled service identity AND that
    identity is in the work's allowed_identities. Every other outcome is a
    fail-closed denial: False for authentication/authorization failures,
    CoreWorkIdError for non-canonical work ids.
    """

    def __init__(self, *, authority: Any,
                 work_id_validator: Callable[[Any], str] = require_core_canonical_work_id) -> None:
        if not callable(getattr(authority, "authenticate", None)):
            raise TypeError("authority must provide authenticate(credential)")
        if not callable(work_id_validator):
            raise TypeError("work_id_validator must be callable(work_id)")
        self._authority = authority
        self._work_id_validator = work_id_validator

    def authorize(self, trusted_caller: Any, work_id: Any) -> bool:
        self._work_id_validator(work_id)
        if not isinstance(trusted_caller, dict):
            return False
        credential = trusted_caller.get("credential")
        try:
            identity = self._authority.authenticate(credential)
        except PermissionError:
            return False
        work = getattr(self._authority, "_works", {}).get(work_id)
        if not isinstance(work, dict):
            return False
        allowed = work.get("allowed_identities")
        if not isinstance(allowed, list):
            return False
        return identity in allowed


__all__ = ["CoreWorkIdError", "require_core_canonical_work_id", "CoreAuthorityAuthorizer"]
