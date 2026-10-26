
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

@dataclass
class MeetingContract:
    id: str
    title: str
    status: str
    participants: List['ParticipantContract'] = field(default_factory=list)
    current_turn: Optional['TurnContract'] = None
    agenda: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ParticipantContract:
    id: str
    name: str
    role: str
    connector_type: str
    connector: Any = None
    enabled: bool = True
    capabilities: Dict = field(default_factory=dict)

@dataclass
class TurnContract:
    id: str
    meeting_id: str
    participant_id: str
    input_message: 'MessageContract'
    status: str
    result: Optional['TurnResultContract'] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

@dataclass
class MessageContract:
    id: str
    meeting_id: str
    from_id: str
    from_name: str
    text: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    attachments: List[Dict] = field(default_factory=list)

class AgentConnectorContract:
    @property
    def id(self) -> str: raise NotImplementedError
    @property
    def name(self) -> str: raise NotImplementedError
    def send_turn(self, context): raise NotImplementedError

@dataclass
class RoomEventContract:
    id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    meeting_id: str = ""
    type: str = ""
    payload: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: Optional[str] = None

@dataclass
class TranscriptContract:
    meeting_id: str
    lines: List[MessageContract] = field(default_factory=list)
    events: List[RoomEventContract] = field(default_factory=list)
    evidence: List[Dict] = field(default_factory=list)

@dataclass
class MeetingContextContract:
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
class TurnResultContract:
    turn_id: str
    agent_id: str
    agent_name: str
    content: str
    status: str = "COMPLETED"
    structured: Optional[Dict] = None
    evidence: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    correlation_id: str = ""
    verified: bool = False
