MCP PUBLIC CONTRACT V1
1. list_meetings

Mục đích: lấy danh sách meeting mà MeetingService cho phép public.

Input
{}
{
  "meetings": [
    {
      "id": "string",
      "title": "string",
      "status": "string"
    }
  ]
}

Không cho MCP truy cập storage trực tiếp.

2. get_meeting

Input:

{
  "meeting_id": "string"
}

Output:

{
  "meeting": {}
}

meeting là DTO detached do MeetingService cung cấp.

Không trả object Meeting nội bộ.

3. get_transcript

Input:

{
  "meeting_id": "string"
}

Output:

{
  "transcript": {}
}

Transcript đi qua:

MCP
 ↓
MeetingService
 ↓
Transcript

Không:

MCP → filesystem
MCP → Secretary internals
🔒 Error Contract

MCP Adapter không nuốt lỗi và cũng không tự tạo business semantics mới.

Phân tầng:

Invalid input
      ↓
MCP inputSchema validation


Meeting không tồn tại
      ↓
ROOM HOP service/domain error
      ↓
MCP error result


Unexpected internal exception
      ↓
MCP error result

Không expose:

❌ stack trace
❌ filesystem path
❌ internal object representation
❌ provider credential
🔒 Dependency Boundary

Đây là điểm quan trọng nhất:

MCP Adapter
    │
    └── depends on
          MeetingService

Không:

MCP Adapter
 ├── ❌ MeetingManager
 ├── ❌ Meeting
 ├── ❌ Transcript storage
 ├── ❌ Secretary
 └── ❌ AI Provider

Dependency direction:

MCP Boundary
     ↓
Application Service
     ↓
Core

Core không biết MCP tồn tại.

🔒 SDK Boundary

mcp==1.28.1 chỉ là implementation dependency:

ROOM HOP contract
      ↓
adapter implementation
      ↓
mcp SDK

Nếu sau này đổi SDK:

mcp 1.28.1
      ↓
SDK-X

thì Public Contract V1 của ROOM HOP không đổi.

🟢 CONTRACT GATE

Ka đề xuất khóa:

MCP PUBLIC BOUNDARY V1 = CONTRACT APPROVED

Phạm vi V1 chỉ:

list_meetings
get_meeting
get_transcript

Không thêm:

❌ create_meeting
❌ update_meeting
❌ delete_meeting
❌ decision
❌ action_items
❌ audio
❌ summarization
❌ AI provider integration