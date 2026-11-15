import { createFileRoute } from "@tanstack/react-router";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { PageHeader, StatusBadge, DemoTag } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { JOB_TYPE_LABEL } from "@/lib/w300/types";
export const Route = createFileRoute("/app/jobs")({ head: () => ({ meta: [{ title: "Dự án & job — W300" }] }), component: P });
function P() {
  const { jobs, updateJob } = useW300();
  return (<><PageHeader title="Dự án & job" sub="Thời gian hoàn thành chỉ là ước tính cho tới khi được xác nhận" />
    <div className="space-y-3">{jobs.map((j) => <div key={j.id} className="surface p-5"><div className="flex flex-wrap items-center justify-between gap-2"><div><div className="font-semibold">{j.title} {j.isDemo && <DemoTag />}</div><div className="font-mono text-xs text-muted-foreground">{j.ref} · {JOB_TYPE_LABEL[j.type].vi} · {new Date(j.createdAt).toLocaleString("vi-VN")}</div></div><StatusBadge value={j.status} /></div>
      <Progress value={j.progress} className="mt-3 h-1.5" /><div className="mt-2 text-xs text-muted-foreground">ETA: {j.etaConfirmed ? "Đã xác nhận" : "Chưa xác nhận (ước tính)"}</div>
      {j.error && <p className="mt-2 text-sm text-destructive">{j.error}</p>}
      {j.status === "FAILED" && <div className="mt-3 flex gap-2"><Button size="sm" variant="outline" onClick={() => { updateJob(j.id, { status: "QUEUED", retries: j.retries + 1, error: undefined, progress: 0 }); toast("Đã xếp lại hàng đợi (demo)"); }}>Thử lại</Button><Button size="sm" variant="ghost" onClick={() => toast("Yêu cầu hỗ trợ đã ghi nhận (demo)")}>Yêu cầu hỗ trợ</Button></div>}
    </div>)}</div></>);
}