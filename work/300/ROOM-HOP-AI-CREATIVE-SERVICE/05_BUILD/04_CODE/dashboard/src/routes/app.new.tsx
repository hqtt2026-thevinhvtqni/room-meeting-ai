import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { PageHeader } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { createDemoJob, validateRequest } from "@/lib/w300/rules";
import { JOB_TYPE_LABEL, type JobType } from "@/lib/w300/types";
export const Route = createFileRoute("/app/new")({ head: () => ({ meta: [{ title: "Tạo yêu cầu — W300" }] }), component: P });
function P() {
  const { addJob } = useW300(); const nav = useNavigate();
  const [type, setType] = useState<JobType>("IMAGE_GEN"); const [title, setTitle] = useState(""); const [prompt, setPrompt] = useState("");
  const [format, setFormat] = useState("1:1"); const [quantity, setQ] = useState(1); const [intendedUse, setUse] = useState("");
  const [file, setFile] = useState<File | null>(null); const [rights, setRights] = useState(false); const [err, setErr] = useState<string | null>(null);
  const isVideo = JOB_TYPE_LABEL[type].kind === "video";
  const submit = (e: React.FormEvent) => { e.preventDefault();
    const input = { type, title, prompt, format, quantity, intendedUse, rightsConfirmed: rights, hasReference: !!file };
    const v = validateRequest(input); setErr(v); if (v) return;
    const j = createDemoJob(input); addJob(j); toast.success(`Đã tạo job DEMO ${j.ref}`, { description: "Không có nhà cung cấp AI nào được gọi." }); nav({ to: "/app/jobs" }); };
  return (<><PageHeader title="Tạo yêu cầu mới" sub="Gửi yêu cầu sẽ chỉ tạo job DEMO — chưa gọi AI provider" />
    <form onSubmit={submit} className="surface max-w-3xl space-y-5 p-6">
      <div><Label>Loại dịch vụ</Label><div className="mt-2 grid gap-2 sm:grid-cols-3">{(Object.keys(JOB_TYPE_LABEL) as JobType[]).map((k) => <button type="button" key={k} onClick={() => setType(k)} className={`rounded-lg border p-3 text-left text-sm ${type === k ? "border-primary bg-primary/10" : "border-border"}`}><div className="font-medium">{JOB_TYPE_LABEL[k].vi}</div><div className="text-xs text-muted-foreground">{JOB_TYPE_LABEL[k].en}</div></button>)}</div></div>
      <div><Label htmlFor="t">Tên yêu cầu</Label><Input id="t" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="VD: Key visual Tết" /></div>
      <div><Label htmlFor="p">Mô tả (prompt) *</Label><Textarea id="p" rows={4} value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Mô tả chi tiết bối cảnh, phong cách, ánh sáng..." /></div>
      <div className="grid gap-4 sm:grid-cols-3">
        <div><Label htmlFor="f">Tỉ lệ khung</Label><select id="f" value={format} onChange={(e) => setFormat(e.target.value)} className="mt-1 h-9 w-full rounded-md border border-input bg-background px-2 text-sm">{["1:1", "4:5", "16:9", "9:16", "4:3"].map((o) => <option key={o}>{o}</option>)}</select></div>
        <div><Label htmlFor="q">{isVideo ? "Thời lượng (giây)" : "Số lượng"}</Label><Input id="q" type="number" min={1} max={isVideo ? 60 : 8} value={quantity} onChange={(e) => setQ(Number(e.target.value))} /></div>
        <div><Label htmlFor="u">Mục đích sử dụng</Label><Input id="u" value={intendedUse} onChange={(e) => setUse(e.target.value)} placeholder="Social, web..." /></div>
      </div>
      <div><Label htmlFor="r">Ảnh tham chiếu (tùy chọn)</Label><Input id="r" type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} /><p className="mt-1 text-xs text-muted-foreground">Tệp chỉ được giữ trên trình duyệt ở bản demo, không tải lên máy chủ.</p></div>
      <label className="flex items-start gap-2 text-sm"><Checkbox checked={rights} onCheckedChange={(v) => setRights(v === true)} className="mt-0.5" />Tôi xác nhận có quyền sử dụng mọi tài liệu tải lên và đồng ý điều khoản dịch vụ.</label>
      {err && <p role="alert" className="text-sm text-destructive">{err}</p>}
      <Button type="submit" variant="hero">Gửi yêu cầu (demo)</Button>
    </form></>);
}