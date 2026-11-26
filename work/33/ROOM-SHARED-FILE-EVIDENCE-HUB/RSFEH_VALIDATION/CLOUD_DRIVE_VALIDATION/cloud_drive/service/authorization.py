"""Authorization boundary for Cloud Drive services.

No Core API integration is implemented here. Production must inject a verified
Core-backed authorizer; the default is fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Principal:
    subject_id: str


class AuthorizationDenied(PermissionError):
    pass


class Authorizer(Protocol):
    def authorize(self, *, principal: Principal, scope_id: str, action: str) -> None: ...


class UnconfiguredAuthorizer:
    """Safe default: deny all operations until a real identity adapter is wired."""

    def authorize(self, *, principal: Principal, scope_id: str, action: str) -> None:
        raise AuthorizationDenied("Core-backed authorization adapter is not configured")
