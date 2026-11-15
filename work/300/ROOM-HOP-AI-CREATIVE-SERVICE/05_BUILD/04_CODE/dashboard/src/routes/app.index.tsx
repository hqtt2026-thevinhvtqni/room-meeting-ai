import { createFileRoute, Link } from "@tanstack/react-router";
import { PlusCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHeader, Stat, StatusBadge } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
export const Route = createFileRoute("/app/")({ head: () => ({ meta: [{ title: "Trang chính — W300" }] }), component: P });
function P() {
  const { jobs } = useW300();
  return (<><PageHeader title="Xin chào 👋" sub="Theo dõi yêu cầu sản xuất ảnh & video của bạn" actions={<Button asChild variant="hero"><Link to="/app/new"><PlusCircle />Tạo yêu cầu</Link></Button>} />
    <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4"><Stat label="Tổng job" value={jobs.length} /><Stat label="Đang chạy" value={jobs.filter((j) => j.status === "RUNNING").length} /><Stat label="Cần duyệt" value={jobs.filter((j) => j.status === "NEEDS_REVIEW").length} /><Stat label="Hạn mức" value="—" hint="Chưa kích hoạt" demo={false} /></div>
    <div className="surface divide-y divide-border">{jobs.slice(0, 5).map((j) => <div key={j.id} className="flex items-center justify-between gap-3 px-5 py-3 text-sm"><div><div className="font-medium">{j.title}</div><div className="font-mono text-xs text-muted-foreground">{j.ref}</div></div><StatusBadge value={j.status} /></div>)}</div></>);
}