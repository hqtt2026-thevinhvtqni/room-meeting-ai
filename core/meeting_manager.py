"""ROOM HOP Meeting Session lifecycle v0.2.1."""
from __future__ import annotations

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path

from core.agent_registry import AgentRegistry
from core.context_loader import package_context
from core.meeting_log import MeetingLog
from core.governance import GOV, MissionContext
from core.identity_resolution import resolve_identity
from core.principal_registry import PrincipalRegistry
from core.secretary import Secretary

ROOM_HOP_ROOT = Path(__file__).resolve().parent.parent
MEETINGS_DIR = ROOM_HOP_ROOT / "meetings"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class MeetingError(Exception):
    pass


class Meeting:
    def __init__(
        self,
        meeting_dir: Path,
        principal_registry: PrincipalRegistry | None = None,
        agent_registry: AgentRegistry | None = None,
    ):
        self.meeting_dir = Path(meeting_dir)
        self.meeting_yaml_path = self.meeting_dir / "meeting.yaml"
        self.final_path = self.meeting_dir / "final.md"
        self.log = MeetingLog(self.meeting_dir)

        # SECRETARY V1: raw transcript record keeper.
        self.secretary = Secretary(self.meeting_dir / "transcript.txt")

        self.principal_registry = principal_registry or PrincipalRegistry()
        self.agent_registry = agent_registry or AgentRegistry()

    @property
    def data(self) -> dict:
        with open(self.meeting_yaml_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _save(self, data: dict) -> None:
        with open(self.meeting_yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False,
            )

    def _transition(
        self,
        expected: str,
        target: str,
        event: str,
        detail: str = "",
    ) -> dict:
        data = self.data

        if data.get("status") != expected:
            raise MeetingError(
                f"Meeting '{data.get('id')}' đang ở "
                f"'{data.get('status')}', cần '{expected}'."
            )

        data["status"] = target
        self._save(data)
        self.log.log_event(event, detail=detail)

        return data

    def open_session(self) -> None:
        self._transition(
            "draft",
            "open",
            "session_opened",
        )

    def join_request(self, identity_id: str) -> dict:
        data = self.data

        if data.get("status") != "open":
            raise MeetingError(
                f"Meeting '{data.get('id')}' không mở JOIN "
                f"ở trạng thái '{data.get('status')}'."
            )

        resolution = resolve_identity(
            identity_id,
            self.principal_registry,
            self.agent_registry,
        )

        if not resolution.is_resolved:
            self.log.log_event(
                "join_rejected",
                detail=f"identity={identity_id}; reason=unresolved",
            )
            raise MeetingError(
                f"Identity '{identity_id}' không resolve được."
            )

        invited = set(data.get("invited_participants", []))
        creator = data.get("created_by")

        if (
            identity_id != creator
            and identity_id not in invited
            and identity_id not in set(data.get("participants", []))
        ):
            self.log.log_event(
                "join_rejected",
                detail=f"identity={identity_id}; reason=meeting_policy",
            )
            raise MeetingError(
                f"Identity '{identity_id}' không được Meeting Policy "
                "cho phép tham gia."
            )

        if identity_id not in data.setdefault("participants", []):
            data["participants"].append(identity_id)

        data.setdefault("join_records", []).append(
            {
                "event": "JOIN_ACCEPTED",
                "identity": {
                    "id": identity_id,
                    "type": resolution.identity_type,
                    "auth_verified": True,
                },
                "authorization": {
                    "policy_source": (
                        "meeting.invited_participants/created_by"
                    ),
                    "policy_check": "PASS",
                    "registry_check": resolution.registry_check,
                },
                "decided_by": "MeetingManager",
                "timestamp": _now_iso(),
            }
        )

        self._save(data)

        self.log.log_event(
            "JOIN_ACCEPTED",
            detail=json.dumps(
                {
                    "meeting_id": data["id"],
                    "identity": identity_id,
                    "identity_type": resolution.identity_type,
                    "registry_check": resolution.registry_check,
                    "decided_by": "MeetingManager",
                },
                ensure_ascii=False,
            ),
        )

        return data["join_records"][-1]

    def start(self, starter: str = "vinh") -> None:
        data = self.data

        if data.get("status") != "open":
            raise MeetingError(
                f"Meeting '{data.get('id')}' không thể START "
                f"từ '{data.get('status')}'."
            )

        if len(set(data.get("participants", []))) < 2:
            raise MeetingError(
                "START yêu cầu ít nhất 2 participants đã JOIN_ACCEPTED."
            )

        if starter not in data.get("participants", []):
            raise MeetingError(
                f"'{starter}' chưa JOIN_ACCEPTED."
            )

        self._transition(
            "open",
            "active",
            "meeting_started",
            detail=f"starter={starter}",
        )

    def add_message(self, speaker: str, content: str) -> Path:
        data = self.data

        if data.get("status") != "active":
            raise MeetingError(
                f"Meeting '{data.get('id')}' đang ở trạng thái "
                f"'{data.get('status')}', không thể thêm message."
            )

        if speaker not in data.get("participants", []):
            raise MeetingError(
                f"'{speaker}' chưa JOIN_ACCEPTED trong meeting này: "
                f"{data.get('participants', [])}"
            )

        return self.log.log_message(speaker, content)

    def add_paste(self, raw_text: str) -> dict:
        """SECRETARY V1: ghi nguyên văn block text vào transcript."""
        data = self.data

        if data.get("status") != "active":
            raise MeetingError(
                f"Meeting '{data.get('id')}' đang ở trạng thái "
                f"'{data.get('status')}', không thể PASTE."
            )

        result = self.secretary.append(raw_text)

        self.log.log_event(
            "paste_received",
            detail=f"length={len(raw_text)}",
        )

        return result

    def get_transcript(self) -> list[dict]:
        """
        Return normalized read-only transcript entries.

        The MeetingLog remains the evidence storage layer.
        This method exposes a stable Core read contract.
        """
        messages = self.log.read_all_messages()

        return [
            {
                "index": index,
                "type": message.get("type", "message"),
                "speaker": message["speaker"],
                "timestamp": message["timestamp"],
                "content": message["content"],
                "file": message.get("file"),
            }
            for index, message in enumerate(messages, start=1)
        ]

    def request_close(self, requester: str = "vinh") -> None:
        data = self.data

        if data.get("status") != "active":
            raise MeetingError(
                f"REQUEST_CLOSE chỉ hợp lệ khi ACTIVE, "
                f"hiện tại '{data.get('status')}'."
            )

        self.log.log_event(
            "request_close",
            detail=f"requester={requester}",
        )

        data["status"] = "closing"
        self._save(data)

    def close(
        self,
        decisions: list[str],
        action_items: list[str],
        summary: str,
        closer: str = "xu",
    ) -> Path:
        data = self.data

        if data.get("status") not in {"closing", "active"}:
            raise MeetingError(
                f"Meeting đã ở trạng thái '{data.get('status')}', "
                "không thể close."
            )

        if data.get("status") == "active":
            self.request_close(closer)
            data = self.data

        rel_yaml_path = f"meetings/{data['id']}/meeting.yaml"

        mission = MissionContext(
            name=f"meeting_close_{data['id']}",
            allow_delete=False,
            allow_edit_protected=True,
        )

        ok, reason = GOV.check(
            closer,
            "EDIT",
            rel_yaml_path,
            mission,
        )

        if not ok:
            raise MeetingError(
                f"Agent '{closer}' không được phép đóng meeting: {reason}"
            )

        GOV.audit(
            closer,
            "CLOSE_MEETING",
            rel_yaml_path,
            "OK",
            mission,
        )

        data["status"] = "closed"
        data["decisions"] = decisions
        data["action_items"] = action_items

        self._save(data)

        self.log.log_event(
            "END_OF_TRANSCRIPT",
            detail=f"closed_by={closer}",
        )

        messages = self.log.read_all_messages()

        final_content = self._render_final_md(
            data,
            messages,
            decisions,
            action_items,
            summary,
        )

        with open(self.final_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        return self.final_path

    def save_artifact(
        self,
        artifact_name: str = "final.md",
    ) -> Path:
        data = self.data

        if data.get("status") != "closed":
            raise MeetingError(
                "SAVE_ARTIFACT chỉ hợp lệ khi CLOSED."
            )

        source = self.meeting_dir / artifact_name

        if not source.exists():
            raise MeetingError(
                f"Artifact không tồn tại: {source}"
            )

        artifacts = self.meeting_dir / "artifacts"
        artifacts.mkdir(exist_ok=True)

        target = artifacts / source.name
        target.write_bytes(source.read_bytes())

        data["status"] = "completed"
        data["completed_at"] = _now_iso()

        self._save(data)

        self.log.log_event(
            "SAVE_ARTIFACT",
            detail=str(target.relative_to(self.meeting_dir)),
        )

        return target

    @staticmethod
    def _render_final_md(
        data,
        messages,
        decisions,
        action_items,
        summary,
    ) -> str:
        lines = [
            f"# {data['id']} — {data['topic']}",
            "",
            f"- Trạng thái: {data['status']}",
            f"- Người tạo: {data['created_by']}",
            (
                "- Participants: "
                f"{', '.join(data.get('participants', []))}"
            ),
            "",
            "## Diễn biến",
            "",
        ]

        for message in messages:
            lines.extend(
                [
                    (
                        f"**{message['speaker']}** "
                        f"({message['timestamp']}):"
                    ),
                    message["content"],
                    "",
                ]
            )

        lines.extend(
            [
                "## Tổng hợp",
                summary or "(chưa có)",
                "",
                "## Quyết định",
            ]
        )

        lines.extend(
            [f"- {decision}" for decision in decisions]
            or ["(không có)"]
        )

        lines.extend(
            [
                "",
                "## Action Items",
            ]
        )

        lines.extend(
            [f"- {item}" for item in action_items]
            or ["(không có)"]
        )

        lines.append("")

        return "\n".join(lines)


class MeetingManager:
    def __init__(
        self,
        registry: AgentRegistry | None = None,
        meetings_dir: Path = MEETINGS_DIR,
        principal_registry: PrincipalRegistry | None = None,
    ):
        self.registry = registry or AgentRegistry()
        self.principal_registry = (
            principal_registry or PrincipalRegistry()
        )
        self.meetings_dir = Path(meetings_dir)
        self.meetings_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_meeting(
        self,
        meeting_id: str,
        topic: str,
        participants: list[str],
        context_files: list[str],
        created_by: str = "vinh",
    ) -> Meeting:
        # participants are INVITATIONS, not automatically accepted.
        for identity_id in [created_by, *participants]:
            resolution = resolve_identity(
                identity_id,
                self.principal_registry,
                self.registry,
            )

            if not resolution.is_resolved:
                raise MeetingError(
                    f"Identity không tồn tại: {identity_id}"
                )

        meeting_dir = self.meetings_dir / meeting_id

        if meeting_dir.exists():
            raise MeetingError(
                f"Meeting '{meeting_id}' đã tồn tại."
            )

        meeting_dir.mkdir(parents=True)

        data = {
            "id": meeting_id,
            "topic": topic,
            "invited_participants": list(
                dict.fromkeys(participants)
            ),
            "participants": [],
            "context_files": context_files,
            "status": "draft",
            "created_by": created_by,
            "created_at": _now_iso(),
            "join_records": [],
            "decisions": [],
            "action_items": [],
            "governance": None,
            "permissions": None,
            "message_bus_mode": None,
        }

        with open(
            meeting_dir / "meeting.yaml",
            "w",
            encoding="utf-8",
        ) as f:
            yaml.safe_dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False,
            )

        meeting = Meeting(
            meeting_dir,
            self.principal_registry,
            self.registry,
        )

        meeting.log.log_event(
            "meeting_created",
            detail=f"topic={topic}",
        )

        copied = package_context(
            context_files,
            meeting_dir / "context",
        )

        meeting.log.log_context_loaded(
            [path.name for path in copied]
        )

        return meeting

    def get_meeting(self, meeting_id: str) -> Meeting:
        meeting_dir = self.meetings_dir / meeting_id

        if not meeting_dir.exists():
            raise MeetingError(
                f"Không tìm thấy meeting '{meeting_id}'."
            )

        return Meeting(
            meeting_dir,
            self.principal_registry,
            self.registry,
        )

    def list_meetings(
        self,
        limit: int | None = None,
        status: str | None = None,
    ) -> list[dict]:
        """
        Return detached meeting metadata snapshots.

        Only directories containing meeting.yaml are considered.
        No lifecycle state is modified.
        """
        if limit is not None and limit < 0:
            raise ValueError("limit phải >= 0 hoặc None.")

        meetings = []

        if not self.meetings_dir.exists():
            return meetings

        for meeting_dir in sorted(self.meetings_dir.iterdir()):
            if not meeting_dir.is_dir():
                continue

            meeting_yaml = meeting_dir / "meeting.yaml"

            if not meeting_yaml.is_file():
                continue

            meeting = Meeting(
                meeting_dir,
                self.principal_registry,
                self.registry,
            )

            data = meeting.data

            if status is not None and data.get("status") != status:
                continue

            meetings.append(dict(data))

        if limit is not None:
            return meetings[:limit]

        return meetings