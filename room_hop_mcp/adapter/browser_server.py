from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bridge.room_hop_bridge import RoomHOPBridge


class AddPasteRequest(BaseModel):
    text: str


def create_browser_app(
    bridge: RoomHOPBridge | None = None,
) -> FastAPI:
    app = FastAPI(title="ROOM HOP Browser Runtime")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    runtime_bridge = bridge or RoomHOPBridge()

    @app.get("/meetings")
    def list_meetings() -> dict:
        result = runtime_bridge.list_meetings()

        if not result.ok:
            raise RuntimeError(result.error or "ROOM HOP bridge error")

        return {"meetings": result.data}

    @app.get("/meetings/{meeting_id}")
    def get_meeting(meeting_id: str) -> dict:
        result = runtime_bridge.get_meeting(meeting_id)

        if not result.ok:
            raise RuntimeError(result.error or "ROOM HOP bridge error")

        return {"meeting": result.data}

    @app.get("/meetings/{meeting_id}/transcript")
    def get_transcript(meeting_id: str) -> dict:
        result = runtime_bridge.get_transcript(meeting_id)

        if not result.ok:
            raise RuntimeError(result.error or "ROOM HOP bridge error")

        return {"transcript": result.data}

    @app.post("/meetings/{meeting_id}/paste")
    def add_paste(
        meeting_id: str,
        body: AddPasteRequest,
    ) -> dict:
        result = runtime_bridge.add_paste_to_meeting(
            meeting_id,
            body.text,
        )

        if not result.ok:
            raise RuntimeError(result.error or "ROOM HOP bridge error")

        return {"paste": result.data}

    return app