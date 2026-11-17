"""Execution lifecycle with explicit dispatch/action boundaries and durable transition port."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol

class ExecutionState(str,Enum):
    RECEIVED="RECEIVED"
    SOURCE_AUTHENTICATED="SOURCE_AUTHENTICATED"
    VALIDATED="VALIDATED"
    NORMALIZED="NORMALIZED"
    DEDUPLICATED="DEDUPLICATED"
    TRIGGER_LOADED="TRIGGER_LOADED"
    CONDITION_EVALUATED="CONDITION_EVALUATED"
    POLICY_EVALUATED="POLICY_EVALUATED"
    APPROVAL_PENDING="APPROVAL_PENDING"
    AUTHORIZED="AUTHORIZED"
    SUPPRESSED="SUPPRESSED"
    QUEUED="QUEUED"
    DISPATCHED="DISPATCHED"
    RECEIVED_BY_TARGET="RECEIVED_BY_TARGET"
    ACKNOWLEDGED="ACKNOWLEDGED"
    ACTION_AUTHORIZED="ACTION_AUTHORIZED"
    ACTION_EXECUTING="ACTION_EXECUTING"
    OUTCOME_RECORDED="OUTCOME_RECORDED"
    SUCCEEDED="SUCCEEDED"
    FAILED="FAILED"
    EXPIRED="EXPIRED"
    UNKNOWN="UNKNOWN"

_ALLOWED={
 ExecutionState.RECEIVED:{ExecutionState.SOURCE_AUTHENTICATED,ExecutionState.FAILED},
 ExecutionState.SOURCE_AUTHENTICATED:{ExecutionState.VALIDATED,ExecutionState.FAILED},
 ExecutionState.VALIDATED:{ExecutionState.NORMALIZED,ExecutionState.FAILED},
 ExecutionState.NORMALIZED:{ExecutionState.DEDUPLICATED,ExecutionState.FAILED},
 ExecutionState.DEDUPLICATED:{ExecutionState.TRIGGER_LOADED,ExecutionState.SUPPRESSED,ExecutionState.FAILED},
 ExecutionState.TRIGGER_LOADED:{ExecutionState.CONDITION_EVALUATED,ExecutionState.FAILED},
 ExecutionState.CONDITION_EVALUATED:{ExecutionState.POLICY_EVALUATED,ExecutionState.SUPPRESSED,ExecutionState.FAILED},
 ExecutionState.POLICY_EVALUATED:{ExecutionState.APPROVAL_PENDING,ExecutionState.AUTHORIZED,ExecutionState.SUPPRESSED,ExecutionState.FAILED},
 ExecutionState.APPROVAL_PENDING:{ExecutionState.AUTHORIZED,ExecutionState.SUPPRESSED,ExecutionState.EXPIRED,ExecutionState.FAILED},
 ExecutionState.AUTHORIZED:{ExecutionState.QUEUED,ExecutionState.FAILED},
 ExecutionState.QUEUED:{ExecutionState.DISPATCHED,ExecutionState.EXPIRED,ExecutionState.FAILED},
 ExecutionState.DISPATCHED:{ExecutionState.RECEIVED_BY_TARGET,ExecutionState.UNKNOWN,ExecutionState.EXPIRED,ExecutionState.FAILED},
 ExecutionState.RECEIVED_BY_TARGET:{ExecutionState.ACKNOWLEDGED,ExecutionState.UNKNOWN,ExecutionState.EXPIRED,ExecutionState.FAILED},
 ExecutionState.ACKNOWLEDGED:{ExecutionState.ACTION_AUTHORIZED,ExecutionState.FAILED},
 ExecutionState.ACTION_AUTHORIZED:{ExecutionState.ACTION_EXECUTING,ExecutionState.FAILED},
 ExecutionState.ACTION_EXECUTING:{ExecutionState.OUTCOME_RECORDED,ExecutionState.FAILED,ExecutionState.UNKNOWN},
 ExecutionState.OUTCOME_RECORDED:{ExecutionState.SUCCEEDED,ExecutionState.FAILED}
}
class StateTransitionError(RuntimeError): pass
@dataclass(frozen=True)
class Transition:
    execution_id:str
    from_state:ExecutionState|None
    to_state:ExecutionState
    at:datetime
    reason:str
    correlation_id:str
class TransitionSink(Protocol):
    def append_transition(self,transition:Transition)->None: ...
class ExecutionStateMachine:
    def __init__(self,sink:TransitionSink|None): self._sink=sink; self._states={}
    def start(self,execution_id:str,correlation_id:str)->ExecutionState:
        if self._sink is None: raise StateTransitionError("durable transition/audit sink unavailable")
        if not execution_id or execution_id in self._states: raise StateTransitionError("execution_id empty or duplicate")
        self._sink.append_transition(Transition(execution_id,None,ExecutionState.RECEIVED,datetime.now(timezone.utc),"execution created",correlation_id))
        self._states[execution_id]=ExecutionState.RECEIVED
        return ExecutionState.RECEIVED
    def transition(self,execution_id:str,target:ExecutionState,reason:str,correlation_id:str)->ExecutionState:
        if self._sink is None: raise StateTransitionError("durable transition/audit sink unavailable")
        current=self._states.get(execution_id)
        if current is None or target not in _ALLOWED.get(current,set()): raise StateTransitionError(f"illegal transition: {current} -> {target}")
        self._sink.append_transition(Transition(execution_id,current,target,datetime.now(timezone.utc),reason,correlation_id))
        self._states[execution_id]=target
        return target
    def state(self,execution_id:str)->ExecutionState|None: return self._states.get(execution_id)
