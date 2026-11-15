import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { Inbox, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { PageHeader, StatusBadge, DemoTag, Empty } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { demoProjects } from "@/lib/w300/demo-data";
import { JOB_TYPE_LABEL, type JobStatus } from "@/lib/w300/types";
export const Route = createFileRoute("/app/jobs")({
  head: () => ({ meta: [{ title: "Dự án & job — W300" }] }),
  component: P,
});
const FILTERS: Array<JobStatus | "ALL"> = [
  "ALL",
  "QUEUED",
  "RUNNING",
  "NEEDS_REVIEW",
  "COMPLETED",
  "FAILED",
  "CANCELLED",
];
function P() {
  const { jobs, updateJob } = useW300();
  const [filter, setFilter] = useState<JobStatus | "ALL">("ALL");
  const projectName = (id: string) => demoProjects.find((p) => p.id === id)?.name ?? id;
  const list = filter === "ALL" ? jobs : jobs.filter((j) => j.status === filter);
  return (
    <>
      <PageHeader
        title="Dự án & job"
        sub="Thời gian hoàn thành chỉ là ước tính cho tới khi được xác nhận"
      />
      <div className="mb-4 flex flex-wrap gap-2" role="tablist" aria-label="Lọc theo trạng thái">
        {FILTERS.map((f) => (
          <button
            key={f}
            role="tab"
            aria-selected={filter === f}
            onClick={() => setFilter(f)}
            className={`rounded-full border px-3 py-1 text-xs font-medium transition-colors ${filter === f ? "border-primary bg-primary/10 text-primary" : "border-border text-muted-foreground hover:text-foreground"}`}
          >
            {f === "ALL" ? "Tất cả" : f.replace(/_/g, " ")}
          </button>
        ))}
      </div>
      {list.length === 0 ? (
        <Empty
          icon={<Inbox />}
          title="Không có job nào ở trạng thái này"
          sub="Chọn bộ lọc khác hoặc tạo yêu cầu mới (demo)."
        />
      ) : (
        <div className="space-y-3">
          {list.map((j) => (
            <div key={j.id} className="surface p-5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <div className="font-semibold">
                    {j.title} {j.isDemo && <DemoTag />}
                  </div>
                  <div className="font-mono text-xs text-muted-foreground">
                    {j.ref} · {JOB_TYPE_LABEL[j.type].vi} · {projectName(j.projectId)} ·{" "}
                    {new Date(j.createdAt).toLocaleString("vi-VN")}
                  </div>
                </div>
                <StatusBadge value={j.status} />
              </div>
              <Progress value={j.progress} className="mt-3 h-1.5" />
              <div className="mt-2 text-xs text-muted-foreground">
                ETA: {j.etaConfirmed ? "Đã xác nhận" : "Chưa xác nhận (ước tính)"}
                {j.retries > 0 ? ` · Lần thử lại: ${j.retries}` : ""}
              </div>
              {j.error && <p className="mt-2 text-sm text-destructive">{j.error}</p>}
              <div className="mt-3 flex flex-wrap gap-2">
                {j.status === "FAILED" && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => {
                      const { error: _ignored, ...rest } = j;
                      updateJob(j.id, {
                        ...rest,
                        status: "QUEUED",
                        retries: j.retries + 1,
                        progress: 0,
                      });
                      toast("Đã xếp lại hàng đợi (demo)");
                    }}
                  >
                    Thử lại
                  </Button>
                )}
                {(j.status === "QUEUED" || j.status === "RUNNING") && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => {
                      updateJob(j.id, { status: "CANCELLED", progress: 0 });
                      toast("Đã hủy job (demo)");
                    }}
                  >
                    <XCircle />
                    Hủy
                  </Button>
                )}
                {j.status === "FAILED" && (
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={() => toast("Yêu cầu hỗ trợ đã ghi nhận (demo)")}
                  >
                    Yêu cầu hỗ trợ
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
