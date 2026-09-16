"""ROOM HOP Meeting Session lifecycle v0.2.1."""
from __future__ import annotations

import json
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

from core.agent_registry import AgentRegistry
from core.context_loader import package_context
from core.meeting_log import MeetingLog
from core.governance import GOV, MissionContext
from core.identity_resolution import resolve_identity
from core.message_identity import (
    MessageIdentityError,
    SOURCE_AI_CHAT_PASTE,
    build_header,
)
from core.principal_registry import PrincipalRegistry
from core.secretary import Secretary

ROOM_HOP_ROOT = Path(__file__).resolve().parent.parent
MEETINGS_DIR = ROOM_HOP_ROOT / "meetings"

# ID allocation v0.1 — race-tolerant, collision-detected (KHÔNG atomic:
# không có lock/transaction thật). Nếu 2 process tạo cùng lúc và đụng
# đúng 1 sequence, create_meeting() sẽ raise MeetingError ở bước
# meeting_dir.mkdir() thay vì silent overwrite. Chấp nhận được ở v0.1.
MEETING_ID_RE = re.compile(r"^MEETING-(\d{4})-(\d{3})$")


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
        """
        Signature GIỮ NGUYÊN (speaker, content) — Message v1.0 Contract:
        không phá add_message() legacy API. `speaker` chính là identity_id
        (đã resolve thành công lúc JOIN_ACCEPTED); ở đây resolve LẠI qua
        Identity/Principal/Agent Registry để dựng Header v1.0 — không có
        kênh nào cho caller tự khai name/role.
        """
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

        # MESSAGE v1.0: speaker đã JOIN_ACCEPTED (resolve thành công lúc
        # JOIN), nhưng KHÔNG cache lại kết quả đó — resolve lại tại đây,
        # trực tiếp từ Registry, đúng tinh thần "role không do caller tự
        # khai báo". Trường hợp hiếm registry đổi giữa JOIN và message
        # (vd. principal/agent file bị xoá) KHÔNG được phép chặn quyền
        # nhắn tin đã được lifecycle cấp — hạ cấp về header=None/source=None
        # (không giả danh) thay vì reject, để không phá legacy contract
        # "participant đã JOIN_ACCEPTED thì add_message() luôn thành công".
        header = None
        source = None
        try:
            header, source_type = build_header(
                speaker,
                self.principal_registry,
                self.agent_registry,
            )
            source = {"type": source_type}
        except MessageIdentityError:
            header = None
            source = None

        return self.log.log_message(
            speaker,
            content,
            header=header,
            source=source,
        )

    def add_paste(
        self,
        raw_text: str,
        identity_id: str | None = None,
    ) -> dict:
        """SECRETARY V1: ghi nguyên văn block text vào transcript.

        MESSAGE v1.0 (bổ sung, KHÔNG đổi hành vi cũ):
        - `identity_id` là OPTIONAL (Architecture Gate DECISION đã khóa).
          Không được chuyển thành required — sẽ phá backward compat của
          Gate 2 / các caller cũ đang gọi add_paste(raw_text) không kèm
          identity.
        - Có `identity_id` -> resolve qua Identity/Principal/Agent
          Registry -> Header v1.0 đầy đủ. Nếu identity_id KHÔNG resolve
          được, REJECT (raise MeetingError) — không fallback, không giả
          danh.
        - Không có `identity_id` -> legacy compatibility path: Message
          vẫn được tạo (source=ai_chat_paste, vì đây là sự kiện paste,
          không phải tuyên bố về danh tính), nhưng `header=None` và
          `speaker=None` — phản ánh ĐÚNG trạng thái chưa định danh,
          TUYỆT ĐỐI không tự gán một identity mặc định (vd. vinh/claude)
          để lấp vào Header.
        - Return value GIỮ NGUYÊN 100%: vẫn là `self.secretary.append()`
          (vd. {"status": "READY"}) — Message creation là side-effect
          ghi log, không được làm caller cũ (test_secretary*,
          test_integration_add_paste) nhận về shape khác đi.
        """
        data = self.data

        if data.get("status") != "active":
            raise MeetingError(
                f"Meeting '{data.get('id')}' đang ở trạng thái "
                f"'{data.get('status')}', không thể PASTE."
            )

        header = None
        if identity_id is not None:
            try:
                header, _source_type = build_header(
                    identity_id,
                    self.principal_registry,
                    self.agent_registry,
                )
            except MessageIdentityError as e:
                raise MeetingError(str(e)) from None

        # RAW, byte-identical — KHÔNG đổi so với hành vi trước Message v1.0.
        result = self.secretary.append(raw_text)

        # MESSAGE v1.0: "một lần paste = một logical Message" — đúng một
        # entry Message được tạo ở đây, dù có/không có identity_id.
        self.log.log_paste_message(
            raw_text,
            identity_id=identity_id,
            header=header,
            source={"type": SOURCE_AI_CHAT_PASTE},
        )

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
                # --- Legacy fields (KHÔNG đổi) ---
                "index": index,
                "type": message.get("type", "message"),
                "speaker": message["speaker"],
                "timestamp": message["timestamp"],
                "content": message["content"],
                "file": message.get("file"),
                # --- MESSAGE v1.0 fields (bổ sung, tolerant với message
                # cũ chưa có các field này -> None qua .get(), KHÔNG
                # rewrite lịch sử) ---
                "id": message.get("id"),
                "header": message.get("header"),
                "source": message.get("source"),
                "created_at": message.get("created_at", message.get("timestamp")),
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

        # MESSAGE v1.0 GUARD: Secretary (AI Chat Paste RAW) và final.md
        # (dựng từ add_message()) PHẢI tách biệt hoàn toàn — đã là hành
        # vi khoá cứng từ trước Message v1.0
        # (tests/test_secretary_acceptance_abc.py::TestCaseC). Từ khi
        # add_paste() cũng ghi một Message vào cùng log.jsonl (Contract
        # target architecture — Message Store/Log), phải lọc bỏ đúng các
        # Message nguồn ai_chat_paste trước khi render final.md, để RAW
        # paste KHÔNG rò vào final.md. Không đổi logic close()/lifecycle
        # nào khác.
        messages_for_final = [
            message
            for message in messages
            if (message.get("source") or {}).get("type")
            != SOURCE_AI_CHAT_PASTE
        ]

        final_content = self._render_final_md(
            data,
            messages_for_final,
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

    def _allocate_meeting_id(self) -> str:
        """
        Sinh meeting_id dạng MEETING-{YYYY}-{seq:03d} cho năm UTC hiện tại.

        race-tolerant / collision-detected — KHÔNG atomic. Dùng
        max(existing_seq) + 1, không dùng len(existing), để không bị
        lệch nếu có thư mục meeting bị xóa thủ công giữa chừng.
        """
        year = datetime.now(timezone.utc).year
        max_seq = 0

        if self.meetings_dir.exists():
            for meeting_dir in self.meetings_dir.iterdir():
                if not meeting_dir.is_dir():
                    continue

                match = MEETING_ID_RE.match(meeting_dir.name)

                if match and int(match.group(1)) == year:
                    seq = int(match.group(2))
                    if seq > max_seq:
                        max_seq = seq

        return f"MEETING-{year}-{max_seq + 1:03d}"

    def create_meeting(
        self,
        meeting_id: str | None,
        topic: str,
        participants: list[str],
        context_files: list[str],
        created_by: str = "vinh",
    ) -> Meeting:
        # meeting_id=None -> Core allocate (v0.1 decision: ID là
        # authority của Core, Bridge không tự sinh sequence).
        # meeting_id tường minh -> giữ nguyên behavior cũ (backward compat).
        if meeting_id is None:
            meeting_id = self._allocate_meeting_id()

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