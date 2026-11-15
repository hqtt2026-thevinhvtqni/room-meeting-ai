import { createFileRoute, Link } from "@tanstack/react-router";
import { Download, ImageOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHeader, DemoTag } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { demoAssets } from "@/lib/w300/demo-data";
import { canDownload } from "@/lib/w300/rules";
export const Route = createFileRoute("/app/gallery")({ head: () => ({ meta: [{ title: "Kết quả — W300" }] }), component: P });
function P() {
  const { jobs } = useW300();
  const doneJobs = jobs.filter((j) => j.status === "COMPLETED" && !demoAssets.some((a) => a.jobId === j.id));
  return (<>
    <PageHeader title="Kết quả" sub="Ảnh minh họa demo — không phải asset thật" />
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {demoAssets.map((a) => <div key={a.id} className="surface overflow-hidden">
        <div className="relative aspect-[4/3]">{a.thumbnail && <img src={a.thumbnail} alt={a.label} loading="lazy" width={1024} height={768} className="size-full object-cover" />}<DemoTag className="absolute left-2 top-2 bg-background/80" /></div>
        <div className="flex items-center justify-between p-4 text-sm"><span>{a.label}</span>{canDownload(a) ? <Button asChild size="sm"><a href={a.url} download><Download />Tải</a></Button> : <span className="text-xs text-muted-foreground">Chưa có file thật</span>}</div>
      </div>)}
      {doneJobs.map((j) => <div key={j.id} className="surface overflow-hidden">
        <div className="relative grid aspect-[4/3] place-items-center bg-muted/40 text-muted-foreground"><ImageOff className="size-8" /><DemoTag className="absolute left-2 top-2" /></div>
        <div className="flex items-center justify-between p-4 text-sm"><span className="min-w-0 truncate">{j.title}</span><span className="whitespace-nowrap text-xs text-muted-foreground">Chưa có asset · không gọi provider</span></div>
      </div>)}
    </div>
    {demoAssets.length === 0 && doneJobs.length === 0 && <p className="text-sm text-muted-foreground">Chưa có kết quả nào. <Link to="/app/new" className="text-primary">Tạo yêu cầu đầu tiên</Link>.</p>}
  </>);
}
