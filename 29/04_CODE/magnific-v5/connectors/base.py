
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

@dataclass
class MeetingContext:
    meeting_id: str
    room_id: str
    speaker_id: str
    speaker_name: str
    intent: str
    message: str
    transcript: List[Dict] = field(default_factory=list)
    current_agenda: str = ""
    evidence: List[Dict] = field(default_factory=list)
    attachments: List[Dict] = field(default_factory=list)
    correlation_id: str = field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:8]}")
    previous_output: Optional[Dict] = None

@dataclass
class TurnResult:
    turn_id: str
    agent_id: str
    agent_name: str
    content: str
    status: str = "COMPLETED"  # FIX G1: Thêm status - REQUESTED | PROCESSING | COMPLETED | FAILED | BLOCKED
    structured: Optional[Dict] = None
    evidence: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: str = ""
    verified: bool = False

class AgentConnector(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def send_turn(self, context: MeetingContext) -> TurnResult:
        pass
