"""Fail-closed policy adapter; never treats caller-provided booleans as authority."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Protocol
class PolicyOutcome(str, Enum):
    ALLOW="ALLOW"; DENY="DENY"; REQUIRE_APPROVAL="REQUIRE_APPROVAL"; INDETERMINATE="INDETERMINATE"
@dataclass(frozen=True)
class PolicyRequest:
    principal_ref: str; work_id: str; wp_id: str; action_type: str; policy_ref: str; assignment_ref: str; correlation_id: str

    def __post_init__(self):
        for field in ("principal_ref", "work_id", "wp_id", "action_type", "policy_ref", "assignment_ref", "correlation_id"):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be a non-empty string")

@dataclass(frozen=True)
class PolicyResult:
    outcome: PolicyOutcome; decision_ref: str; policy_revision: str; reason: str
class PolicyProvider(Protocol):
    def evaluate_current(self, request: PolicyRequest) -> PolicyResult: ...
class ApprovalVerifier(Protocol):
    def verify_current(self, approval_ref: str, request: PolicyRequest) -> bool: ...
class PolicyAdapter:
    def __init__(self, provider: PolicyProvider | None, approval_verifier: ApprovalVerifier | None=None):
        self._provider, self._approval = provider, approval_verifier
    def authorize(self, request: PolicyRequest, approval_ref: str | None=None) -> PolicyResult:
        if not isinstance(request, PolicyRequest):
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "invalid policy request")
        if self._provider is None:
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "authoritative provider unavailable")
        try:
            result = self._provider.evaluate_current(request)
        except Exception:
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "provider failure")
        if not isinstance(result, PolicyResult):
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "invalid provider response")
        if not isinstance(result.outcome, PolicyOutcome):
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "invalid provider outcome")
        if not isinstance(result.reason, str) or not result.reason.strip():
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "provider response missing reason")
        if result.outcome == PolicyOutcome.INDETERMINATE:
            return result
        if not all(isinstance(value, str) and value.strip() for value in (result.decision_ref, result.policy_revision)):
            return PolicyResult(PolicyOutcome.INDETERMINATE, "", "", "provider decision lacks authoritative reference/revision")
        if result.outcome != PolicyOutcome.REQUIRE_APPROVAL:
            return result
        if not isinstance(approval_ref, str) or not approval_ref.strip() or self._approval is None:
            return PolicyResult(PolicyOutcome.DENY, result.decision_ref, result.policy_revision, "required approval missing")
        try:
            valid = self._approval.verify_current(approval_ref, request)
        except Exception:
            valid = False
        if valid is not True:
            return PolicyResult(PolicyOutcome.DENY, result.decision_ref, result.policy_revision, "approval invalid, expired or out of scope")
        return PolicyResult(PolicyOutcome.ALLOW, result.decision_ref, result.policy_revision, "required approval verified")
