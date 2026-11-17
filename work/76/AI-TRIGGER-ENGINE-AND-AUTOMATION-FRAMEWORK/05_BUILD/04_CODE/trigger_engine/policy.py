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
        if self._provider is None: return PolicyResult(PolicyOutcome.INDETERMINATE,"","","authoritative provider unavailable")
        try: result=self._provider.evaluate_current(request)
        except Exception: return PolicyResult(PolicyOutcome.INDETERMINATE,"","","provider failure")
        if not isinstance(result,PolicyResult): return PolicyResult(PolicyOutcome.INDETERMINATE,"","","invalid provider response")
        if result.outcome != PolicyOutcome.REQUIRE_APPROVAL: return result
        if not approval_ref or self._approval is None:
            return PolicyResult(PolicyOutcome.DENY,result.decision_ref,result.policy_revision,"required approval missing")
        try: valid=self._approval.verify_current(approval_ref,request)
        except Exception: valid=False
        if valid is not True: return PolicyResult(PolicyOutcome.DENY,result.decision_ref,result.policy_revision,"approval invalid, expired or out of scope")
        return PolicyResult(PolicyOutcome.ALLOW,result.decision_ref,result.policy_revision,"required approval verified")
