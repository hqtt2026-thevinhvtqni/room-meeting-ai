import { createFileRoute, Link } from "@tanstack/react-router";
import { PlusCircle, FolderKanban, ArrowRight, Inbox } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PageHeader, Stat, StatusBadge, Empty, DemoTag } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { demoProjects } from "@/lib/w300/demo-data";
import { JOB_TYPE_LABEL } from "@/lib/w300/types";
export const Route = createFileRoute("/app/")({
  head: () => ({ meta: [{ title: "Trang chính — W300" }] }),
  component: P,
});
function P() {
  const { jobs } = useW300();
  const projectName = (id: string) => demoProjects.find((p) => p.id === id)?.name ?? id;
  const active = jobs.filter(
    (j) => j.status === "QUEUED" || j.status === "RUNNING" || j.status === "NEEDS_REVIEW",
  );
  const done = jobs.filter((j) => j.status === "COMPLETED");
  return (
    <>
      <PageHeader
        title="Xin chào 👋"
        sub="Theo dõi yêu cầu sản xuất ảnh & video của bạn"
        actions={
          <Button asChild variant="hero">
            <Link to="/app/new">
              <PlusCircle />
              Tạo yêu cầu
            </Link>
          </Button>
        }
      />
      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Stat label="Tổng job" value={jobs.length} />
        <Stat label="Đang hoạt động" value={active.length} hint="Queued / running / cần duyệt" />
        <Stat label="Hoàn thành" value={done.length} />
        <Stat label="Hạn mức" value="—" hint="Chưa kích hoạt" demo={false} />
      </div>
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <section className="surface p-5" aria-label="Đang diễn ra">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-base font-semibold">Đang diễn ra</h2>
            <DemoTag />
          </div>
          {active.length === 0 ? (
            <Empty
              icon={<Inbox />}
              title="Không có job nào đang chạy"
              sub="Tạo yêu cầu mới để bắt đầu (demo)."
              action={
                <Button asChild size="sm" variant="outline">
                  <Link to="/app/new">
                    <PlusCircle />
                    Tạo yêu cầu
                  </Link>
                </Button>
              }
            />
          ) : (
            <ul className="divide-y divide-border">
              {active.map((j) => (
                <li key={j.id} className="flex items-center justify-between gap-3 py-3 text-sm">
                  <div className="min-w-0">
                    <div className="truncate font-medium">{j.title}</div>
                    <div className="truncate font-mono text-xs text-muted-foreground">
                      {j.ref} · {JOB_TYPE_LABEL[j.type].vi} · {projectName(j.projectId)}
                    </div>
                  </div>
                  <StatusBadge value={j.status} />
                </li>
              ))}
            </ul>
          )}
        </section>
        <section className="surface p-5" aria-label="Dự án">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-base font-semibold">Dự án</h2>
            <DemoTag />
          </div>
          <ul className="divide-y divide-border">
            {demoProjects.map((p) => {
              const n = jobs.filter((j) => j.projectId === p.id).length;
              return (
                <li key={p.id} className="flex items-center justify-between gap-3 py-3 text-sm">
                  <div>
                    <div className="font-medium">{p.name}</div>
                    <div className="text-xs text-muted-foreground">{n} job</div>
                  </div>
                  <Link to="/app/jobs" className="text-primary">
                    <ArrowRight className="size-4" />
                    <span className="sr-only">Mở dự án &amp; job</span>
                  </Link>
                </li>
              );
            })}
          </ul>
          <Button asChild variant="ghost" size="sm" className="mt-3">
            <Link to="/app/jobs">
              <FolderKanban />
              Xem tất cả job
            </Link>
          </Button>
        </section>
      </div>
    </>
  );
}
