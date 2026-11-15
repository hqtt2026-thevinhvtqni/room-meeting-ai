import { createFileRoute } from "@tanstack/react-router";
import { Download } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHeader, DemoTag } from "@/components/w300/status";
import { demoAssets } from "@/lib/w300/demo-data";
import { canDownload } from "@/lib/w300/rules";
export const Route = createFileRoute("/app/gallery")({ head: () => ({ meta: [{ title: "Kết quả — W300" }] }), component: P });
function P() {
  return (<><PageHeader title="Kết quả" sub="Ảnh minh họa demo — không phải asset thật" />
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{demoAssets.map((a) => <div key={a.id} className="surface overflow-hidden"><div className="relative aspect-[4/3]">{a.thumbnail && <img src={a.thumbnail} alt={a.label} loading="lazy" width={1024} height={768} className="size-full object-cover" />}<DemoTag className="absolute left-2 top-2 bg-background/80" /></div>
      <div className="flex items-center justify-between p-4 text-sm"><span>{a.label}</span>{canDownload(a) ? <Button asChild size="sm"><a href={a.url} download><Download />Tải</a></Button> : <span className="text-xs text-muted-foreground">Chưa có file thật</span>}</div></div>)}</div></>);
}