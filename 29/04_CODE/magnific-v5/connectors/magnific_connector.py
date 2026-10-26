from .manual_clipboard import ManualClipboardConnector
from .base import MeetingContext, TurnResult
from datetime import datetime
import os, json

# === PHÂN LOẠI 24 TOOL THEO G4 ===
TOOL_CATEGORIES = {
    "core_image": {
        "label": "Hình ảnh gốc (10 tool từ Magnific)",
        "tools": ["image-generator", "image-editor", "upscaler", "cinematic-shot", "variations", "camera-change", "model-creator", "remove-bg", "beauty-retouch", "relight"],
        "execution": "generic_manual",
        "status": "REGISTERED + GENERIC_EXEC"
    },
    "website": {
        "label": "Website (4 tool bổ sung)",
        "tools": ["website-builder", "landing-builder", "ui-component", "seo-optimizer"],
        "execution": "specialized",
        "status": "REGISTERED + SPECIALIZED"
    },
    "image_edit": {
        "label": "Cắt ghép Ảnh (4 tool bổ sung)",
        "tools": ["image-crop", "image-merge", "image-collage", "image-resize"],
        "execution": "specialized",
        "status": "REGISTERED + SPECIALIZED"
    },
    "video_edit": {
        "label": "Cắt ghép Video (6 tool bổ sung)",
        "tools": ["video-cut", "video-merge", "video-trim", "video-effects", "video-subtitle", "video-compress"],
        "execution": "specialized",
        "status": "REGISTERED + SPECIALIZED"
    }
}

MAGNIFIC_TOOLS = {
    "image-generator": {"name": "Trình tạo ảnh", "category": "Hình ảnh", "desc": "Tạo hình ảnh từ gợi ý văn bản", "group": "core_image"},
    "image-editor": {"name": "Trình chỉnh sửa hình ảnh", "category": "Hình ảnh", "desc": "Chỉnh sửa và sửa đổi hình ảnh hiện có", "group": "core_image"},
    "upscaler": {"name": "Bộ nâng cấp hình ảnh", "category": "Hình ảnh", "desc": "Nâng cao độ phân giải và chi tiết", "group": "core_image"},
    "cinematic-shot": {"name": "Cảnh quay điện ảnh", "category": "Băng hình", "desc": "Tạo ra các cú bấm điện ảnh", "group": "core_image"},
    "variations": {"name": "Biến thể", "category": "Hình ảnh", "desc": "Tạo các biến thể của hình ảnh", "group": "core_image"},
    "camera-change": {"name": "Thay đổi máy ảnh", "category": "Hình ảnh", "desc": "Điều chỉnh góc máy ảnh và ống kính", "group": "core_image"},
    "model-creator": {"name": "Công cụ tạo mô hình", "category": "Thiết kế", "desc": "Đặt thiết kế lên mô hình sản phẩm - Dùng cho Perfume Video", "group": "core_image"},
    "remove-bg": {"name": "Xóa nền", "category": "Hình ảnh", "desc": "Tách riêng đối tượng khỏi bối cảnh", "group": "core_image"},
    "beauty-retouch": {"name": "Chốt làm đẹp da", "category": "Hình ảnh", "desc": "Chỉnh sửa và làm nổi bật chi tiết da", "group": "core_image"},
    "relight": {"name": "Thắp lại", "category": "Hình ảnh", "desc": "Thay đổi ánh sáng và không khí", "group": "core_image"},
    "website-builder": {"name": "Trình tạo Website", "category": "Website", "desc": "Tạo website đầy đủ từ prompt, hỗ trợ HTML/CSS/JS, responsive", "group": "website"},
    "landing-builder": {"name": "Tạo Landing Page", "category": "Website", "desc": "Tạo landing page bán hàng, giới thiệu sản phẩm nước hoa", "group": "website"},
    "ui-component": {"name": "Tạo Component UI", "category": "Website", "desc": "Tạo component React/Tailwind cho website", "group": "website"},
    "seo-optimizer": {"name": "Tối ưu SEO Website", "category": "Website", "desc": "Tối ưu SEO, meta tags, tốc độ website", "group": "website"},
    "image-crop": {"name": "Cắt ảnh", "category": "Cắt ghép Ảnh", "desc": "Cắt ảnh theo tỷ lệ, kích thước tùy chỉnh", "group": "image_edit"},
    "image-merge": {"name": "Ghép ảnh", "category": "Cắt ghép Ảnh", "desc": "Ghép nhiều ảnh thành 1, tạo collage, panorama", "group": "image_edit"},
    "image-collage": {"name": "Tạo Collage", "category": "Cắt ghép Ảnh", "desc": "Tạo ảnh ghép nghệ thuật cho quảng cáo nước hoa", "group": "image_edit"},
    "image-resize": {"name": "Đổi kích thước hàng loạt", "category": "Cắt ghép Ảnh", "desc": "Resize nhiều ảnh cùng lúc cho website", "group": "image_edit"},
    "video-cut": {"name": "Cắt Video", "category": "Cắt ghép Video", "desc": "Cắt video theo thời gian, loại bỏ đoạn thừa", "group": "video_edit"},
    "video-merge": {"name": "Ghép Video", "category": "Cắt ghép Video", "desc": "Ghép nhiều video thành 1 video hoàn chỉnh", "group": "video_edit"},
    "video-trim": {"name": "Xén & Xoay Video", "category": "Cắt ghép Video", "desc": "Xén khung hình, xoay video", "group": "video_edit"},
    "video-effects": {"name": "Hiệu ứng Video", "category": "Cắt ghép Video", "desc": "Thêm transition, filter, text cho video perfume", "group": "video_edit"},
    "video-subtitle": {"name": "Thêm phụ đề Video", "category": "Cắt ghép Video", "desc": "Tự động tạo và gắn phụ đề cho video", "group": "video_edit"},
    "video-compress": {"name": "Nén Video", "category": "Cắt ghép Video", "desc": "Nén video giữ chất lượng để up website", "group": "video_edit"},
}

# Specialized connectors - FIX G4
class WebsiteBuilderConnector(ManualClipboardConnector):
    def __init__(self, tool_id="website-builder", base_dir="."):
        super().__init__(agent_id=tool_id, agent_name=MAGNIFIC_TOOLS[tool_id]["name"], base_dir=base_dir)
    
    def _build_prompt(self, context, turn_id, correlation_id):
        base = super()._build_prompt(context, turn_id, correlation_id)
        return base + "\n## Template website nước hoa: Hero 3D + USP + Testimonials + CTA - Mobile first - Tích hợp video perfume"

class VideoCutMergeConnector(ManualClipboardConnector):
    def __init__(self, tool_id="video-cut", base_dir="."):
        super().__init__(agent_id=tool_id, agent_name=MAGNIFIC_TOOLS[tool_id]["name"], base_dir=base_dir)

class ImageCutMergeConnector(ManualClipboardConnector):
    def __init__(self, tool_id="image-crop", base_dir="."):
        super().__init__(agent_id=tool_id, agent_name=MAGNIFIC_TOOLS[tool_id]["name"], base_dir=base_dir)

# Factory - FIX G4: Phân loại rõ
def create_connector(tool_id: str, base_dir="."):
    if tool_id not in MAGNIFIC_TOOLS:
        raise ValueError(f"Tool {tool_id} không tồn tại")
    
    group = MAGNIFIC_TOOLS[tool_id]["group"]
    if group == "website":
        return WebsiteBuilderConnector(tool_id, base_dir)
    elif group in ["image_edit", "video_edit"]:
        if group == "video_edit":
            return VideoCutMergeConnector(tool_id, base_dir)
        else:
            return ImageCutMergeConnector(tool_id, base_dir)
    else:
        # core_image - generic
        return ManualClipboardConnector(tool_id, MAGNIFIC_TOOLS[tool_id]["name"], base_dir)

class MagnificWorkflowOrchestrator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.connectors = {}
    
    def register_tool(self, tool_id: str):
        self.connectors[tool_id] = create_connector(tool_id, self.base_dir)
    
    def run_perfume_workflow(self, meeting_id: str, design_file: str, agenda: str = "Tạo Perfume Video", auto_wait=False):
        workflow_steps = [
            ("model-creator", f"Đặt thiết kế {design_file} lên mô hình chai nước hoa", None),
            ("relight", "Thắp lại - Chỉnh ánh sáng studio", "model-creator"),
            ("cinematic-shot", "Cảnh quay điện ảnh - Tạo video xoay 360", "relight"),
            ("upscaler", "Bộ nâng cấp - Upscale lên 4K", "cinematic-shot"),
        ]
        
        results = []
        previous_output = None
        
        for tool_id, task, depends_on in workflow_steps:
            if tool_id not in self.connectors:
                self.register_tool(tool_id)
            
            if depends_on:
                dep_result = next((r for r in results if r["tool_id"] == depends_on), None)
                if not dep_result or dep_result["status"] != "COMPLETED":
                    results.append({
                        "tool_id": tool_id,
                        "status": "BLOCKED",
                        "reason": f"Dependency {depends_on} not COMPLETED",
                        "turn_id": None
                    })
                    print(f"[BLOCKED] {tool_id} - chờ {depends_on}")
                    break
                previous_output = dep_result.get("output")
            
            ctx = MeetingContext(
                meeting_id=meeting_id,
                room_id="perfume-room",
                speaker_id="vinh",
                speaker_name="Vinh",
                intent="assign_task",
                message=task,
                current_agenda=agenda,
                transcript=[{"speaker": "System", "content": f"Prev: {previous_output}"}] if previous_output else [],
                attachments=[{"type": "design", "file": design_file}],
                correlation_id=f"{meeting_id}_{tool_id}_{datetime.now().strftime('%H%M%S')}",
                previous_output=previous_output
            )
            
            result = self.connectors[tool_id].send_turn(ctx)
            results.append({
                "tool_id": tool_id,
                "status": result.status,
                "turn_id": result.turn_id,
                "outbox": result.evidence,
                "output": None,
                "correlation_id": result.correlation_id
            })
            print(f"✓ [{result.status}] {tool_id} -> {result.evidence}")
        
        self._write_evidence(meeting_id, results)
        return results
    
    def _write_evidence(self, meeting_id: str, results: list):
        evidence_path = f"{self.base_dir}/meetings/{meeting_id}/evidence.json"
        os.makedirs(f"{self.base_dir}/meetings/{meeting_id}", exist_ok=True)
        evidence = {
            "meeting_id": meeting_id,
            "workflow": "perfume-video",
            "created_at": datetime.now().isoformat(),
            "steps": results,
            "total_steps": len(results),
            "completed_steps": len([r for r in results if r["status"] == "COMPLETED"]),
            "requested_steps": len([r for r in results if r["status"] == "REQUESTED"]),
            "note": "Evidence từ events thực tế, chỉ REQUESTED chưa COMPLETED vì chưa có inbox verified đủ TURN_ID+CORRELATION_ID"
        }
        with open(evidence_path, "w", encoding="utf-8") as f:
            json.dump(evidence, f, ensure_ascii=False, indent=2)
