from core.meeting_manager import MeetingManager, MeetingError
import hashlib

m = MeetingManager().get_meeting("MEETING-2026-008")

before = m.secretary.read()
before_sha = hashlib.sha256(
    m.secretary._transcript_path.read_bytes()
).hexdigest()

print("STATUS_BEFORE:", m.data["status"])
print("TRANSCRIPT_LEN_BEFORE:", len(before))
print("BEFORE_SHA256:", before_sha)

try:
    m.add_paste("ATTEMPT AFTER CLOSED\nThis must never be recorded.")
    print("UNEXPECTED: PASTE ACCEPTED")
except MeetingError as e:
    print("REJECTED:", type(e).__name__)
    print("ERROR:", e)

after = m.secretary.read()
after_sha = hashlib.sha256(
    m.secretary._transcript_path.read_bytes()
).hexdigest()

print("STATUS_AFTER:", m.data["status"])
print("TRANSCRIPT_UNCHANGED:", after == before)
print("SHA_UNCHANGED:", after_sha == before_sha)
print("AFTER_SHA256:", after_sha)