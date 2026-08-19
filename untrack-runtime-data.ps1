# ROOM HOP - Bước 1: Untrack 59 file runtime/data khỏi Git index
# (file thật KHÔNG bị xóa, chỉ ngưng theo dõi bởi Git)
# Đã dry-run PASS trên bản sao repo trước khi anh chạy trên máy thật.
# Chạy tại: D:\ROOM-HOP-CLEAN\room-meeting-ai

git rm --cached test_long_transcript.txt transcript_test_output.txt pytest_output.txt

git rm --cached secretary_size_tests/transcript_5MB.txt
git rm --cached secretary_size_tests/transcript_10MB.txt
git rm --cached secretary_size_tests/transcript_50MB.txt

git rm --cached meetings/MEETING-2026-008/transcript.txt
git rm --cached meetings/MEETING-2026-008/test_case_b_transcript.txt
git rm --cached meetings/MEETING-2026-008/test_case_c_transcript.txt

git rm --cached -r tmp/
git rm --cached -r trash/

# desktop.ini (bản đã sửa lỗi cú pháp -z không tương thích PowerShell)
git rm --cached (git ls-files | Where-Object { $_ -match '(^|/)desktop\.ini$' })

# Checkpoint - dán kết quả để đối chiếu 59 dòng D
git status --short
