from core.meeting_manager import MeetingManager, MeetingError

m = MeetingManager().get_meeting("MEETING-2026-009")

before = m.secretary.read()

print("STATUS_BEFORE:", m.data["status"])
print("TRANSCRIPT_LEN_BEFORE:", len(before))

try:
    m.add_paste("MUST NOT BE RECORDED")
    print("UNEXPECTED: PASTE ACCEPTED")
except MeetingError as exc:
    print("REJECTED:", type(exc).__name__)
    print("ERROR:", exc)

after = m.secretary.read()

print("STATUS_AFTER:", m.data["status"])
print("TRANSCRIPT_UNCHANGED:", after == before)
print("TRANSCRIPT_LEN_AFTER:", len(after))