"""Execution state machine; state is committed only after durable transition append."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol
class ExecutionState(str,Enum):
    RECEIVED="RECEIVED"; VALIDATED="VALIDATED"; EVALUATED="EVALUATED"; SUPPRESSED="SUPPRESSED"
    AUTHORIZED="AUTHORIZED"; QUEUED="QUEUED"; DISPATCHED="DISPATCHED"; RECEIVED_BY_TARGET="RECEIVED_BY_TARGET"
    ACKNOWLEDGED="ACKNOWLEDGED"; SUCCEEDED="SUCCEEDED"; FAILED="FAILED"; EXPIRED="EXPIRED"; UNKNOWN="UNKNOWN"
_ALLOWED={
 ExecutionState.RECEIVED:{ExecutionState.VALIDATED,ExecutionState.FAILED},
 ExecutionState.VALIDATED:{ExecutionState.EVALUATED,ExecutionState.FAILED},
 ExecutionState.EVALUATED:{ExecutionState.SUPPRESSED,ExecutionState.AUTHORIZED,ExecutionState.FAILED},
 ExecutionState.AUTHORIZED:{ExecutionState.QUEUED,ExecutionState.FAILED},
 ExecutionState.QUEUED:{ExecutionState.DISPATCHED,ExecutionState.EXPIRED,ExecutionState.FAILED},
 ExecutionState.DISPATCHED:{ExecutionState.RECEIVED_BY_TARGET,ExecutionState.UNKNOWN,ExecutionState.FAILED,ExecutionState.EXPIRED},
 ExecutionState.RECEIVED_BY_TARGET:{ExecutionState.ACKNOWLEDGED,ExecutionState.UNKNOWN,ExecutionState.FAILED,ExecutionState.EXPIRED},
 ExecutionState.ACKNOWLEDGED:{ExecutionState.SUCCEEDED,ExecutionState.FAILED}}
class StateTransitionError(RuntimeError): pass
@dataclass(frozen=True)
class Transition:
    execution_id:str; from_state:ExecutionState; to_state:ExecutionState; at:datetime; reason:str; correlation_id:str
class TransitionSink(Protocol):
    def append_transition(self, transition:Transition)->None: ...
class ExecutionStateMachine:
    def __init__(self,sink:TransitionSink|None): self._sink=sink; self._states={}
    def start(self,execution_id:str,correlation_id:str)->ExecutionState:
        if not execution_id or execution_id in self._states: raise StateTransitionError("execution_id empty or duplicate")
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
