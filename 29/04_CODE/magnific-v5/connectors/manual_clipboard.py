import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict
from .base import AgentConnector, MeetingContext, TurnResult

class ManualClipboardConnector(AgentConnector):
    """
    v5 FIX G1-G3:
    - G1: TurnResult có status
    - G2: Chạy được gói nguyên bản, không monkey-patch
    - G3: Verification chặt chẽ - yêu cầu cả TURN_ID và CORRELATION_ID, không chấp nhận chỉ có VERIFIED
    """
    def __init__(self, agent_id: str, agent_name: str, base_dir: str = "."):
        self._id = agent_id
        self._name = agent_name
        self.base_dir = base_dir
        os.makedirs(f"{base_dir}/outbox", exist_ok=True)
        os.makedirs(f"{base_dir}/inbox", exist_ok=True)
        os.makedirs(f"{base_dir}/inbox/processed", exist_ok=True)
        os.makedirs(f"{base_dir}/meetings", exist_ok=True)
        self._pending_turns: Dict[str, Dict] = {}
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    def send_turn(self, context: MeetingContext) -> TurnResult:
        turn_id = f"turn_{context.meeting_id}_{self._id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(2).hex()}"
        correlation_id = context.correlation_id or turn_id
        
        self._pending_turns[turn_id] = {
            "context": context,
            "correlation_id": correlation_id,
            "meeting_id": context.meeting_id,
            "created_at": datetime.now().isoformat(),
            "status": "REQUESTED"
        }
        
        outbox_path = f"{self.base_dir}/outbox/{self._id}_{turn_id}.md"
        prompt_content = self._build_prompt(context, turn_id, correlation_id)
        
        with open(outbox_path, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        
        self._write_event(context.meeting_id, "TURN_REQUESTED", {
            "turn_id": turn_id,
            "agent_id": self._id,
            "correlation_id": correlation_id,
            "outbox_path": outbox_path,
            "status": "REQUESTED"
        }, correlation_id)
        
        return TurnResult(
            turn_id=turn_id,
            agent_id=self._id,
            agent_name=self._name,
            content=f"[REQUESTED] Prompt at {outbox_path}",
            status="REQUESTED",
            evidence=outbox_path,
            correlation_id=correlation_id,
            verified=False
        )
    
    def read_inbox_result(self, turn_id: str) -> Optional[TurnResult]:
        """
        FIX G3: Verification chặt chẽ
        - Yêu cầu BẮT BUỘC có cả TURN_ID và CORRELATION_ID trong file
        - Không chấp nhận chỉ có chuỗi VERIFIED
        - Kiểm tra chống đọc lại, sai lượt, phản hồi cũ
        """
        if turn_id not in self._pending_turns:
            return TurnResult(
                turn_id=turn_id,
                agent_id=self._id,
                agent_name=self._name,
                content="",
                status="FAILED",
                evidence=f"turn_id {turn_id} not in pending or already processed",
                verified=False
            )
        
        pending = self._pending_turns[turn_id]
        correlation_id = pending["correlation_id"]
        meeting_id = pending["meeting_id"]
        
        inbox_path = f"{self.base_dir}/inbox/{self._id}_{turn_id}.md"
        fallback_path = f"{self.base_dir}/inbox/{self._id}.md"
        
        target_path = None
        if os.path.exists(inbox_path):
            target_path = inbox_path
        elif os.path.exists(fallback_path):
            target_path = fallback_path
        else:
            return None
        
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # === FIX G3: Verification chặt chẽ, không dùng OR với VERIFIED ===
        has_turn_id = turn_id in content
        has_corr_id = correlation_id in content
        has_min_length = len(content.strip()) >= 20
        
        # Yêu cầu BẮT BUỘC: phải có cả TURN_ID và CORRELATION_ID
        verified = has_turn_id and has_corr_id and has_min_length
        
        # Trường hợp chỉ có VERIFIED mà không có ID -> FAILED
        if "VERIFIED" in content and not (has_turn_id and has_corr_id):
            verified = False
            status = "FAILED"
            reason = "Chỉ có VERIFIED nhưng thiếu TURN_ID/CORRELATION_ID - không đủ bằng chứng"
        elif not has_turn_id:
            status = "FAILED"
            reason = f"Thiếu TURN_ID {turn_id}"
        elif not has_corr_id:
            status = "FAILED"
            reason = f"Thiếu CORRELATION_ID {correlation_id}"
        elif not has_min_length:
            status = "FAILED"
            reason = "Nội dung quá ngắn (<20 ký tự)"
        else:
            status = "COMPLETED"
            reason = "Verified đủ TURN_ID + CORRELATION_ID"
        
        # Move sang processed
        processed_dir = f"{self.base_dir}/inbox/processed"
        os.makedirs(processed_dir, exist_ok=True)
        processed_path = f"{processed_dir}/{self._id}_{turn_id}_{datetime.now().strftime('%H%M%S')}.md"
        try:
            with open(processed_path, "w", encoding="utf-8") as out:
                out.write(f"# AUDIT: {reason}\n# verified={verified}\n\n{content}")
            if os.path.exists(target_path):
                os.remove(target_path)
        except Exception:
            pass
        
        self._write_event(meeting_id, "TURN_COMPLETED" if verified else "TURN_FAILED", {
            "turn_id": turn_id,
            "agent_id": self._id,
            "correlation_id": correlation_id,
            "inbox_path": target_path,
            "processed_path": processed_path,
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
            "verified": verified,
            "status": status,
            "reason": reason
        }, correlation_id)
        
        if verified:
            del self._pending_turns[turn_id]
        
        return TurnResult(
            turn_id=turn_id,
            agent_id=self._id,
            agent_name=self._name,
            content=content if verified else "",
            status=status,
            evidence=processed_path,
            correlation_id=correlation_id,
            verified=verified
        )
    
    def _build_prompt(self, context: MeetingContext, turn_id: str, correlation_id: str) -> str:
        transcript_text = "\n".join([f"{t.get('speaker')}: {t.get('content')}" for t in context.transcript[-10:]])
        prev = getattr(context, 'previous_output', None)
        prev_text = f"\nĐầu ra bước trước (đã verified):\n{json.dumps(prev, ensure_ascii=False, indent=2)}" if prev else "\nKhông có đầu ra bước trước"
        
        return f"""# ROOM HOP - REQUEST_TURN: {self._name}
TURN_ID: {turn_id}
CORRELATION_ID: {correlation_id}
Meeting: {context.meeting_id}
Intent: {context.intent}
From: {context.speaker_name}
Time: {datetime.now().isoformat()}

## Agenda:
{context.current_agenda}

## Transcript gần nhất:
{transcript_text}
{prev_text}

## Message:
{context.speaker_name}: {context.message}

## YÊU CẦU BẮT BUỘC ĐỂ ĐƯỢC VERIFIED (FIX G3):
Khi dán kết quả vào inbox/{self._id}_{turn_id}.md, PHẢI bao gồm 2 dòng:
TURN_ID: {turn_id}
CORRELATION_ID: {correlation_id}

Chỉ ghi VERIFIED mà không có 2 dòng trên cũng sẽ FAILED.

Generated: {datetime.now().isoformat()}
"""
    
    def _write_event(self, meeting_id: str, event_type: str, payload: dict, correlation_id: str):
        events_dir = f"{self.base_dir}/meetings/{meeting_id}"
        os.makedirs(events_dir, exist_ok=True)
        event_file = f"{events_dir}/events.jsonl"
        
        event = {
            "id": f"evt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.urandom(2).hex()}",
            "meeting_id": meeting_id,
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.now().isoformat(),
            "correlation_id": correlation_id
        }
        
        with open(event_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
