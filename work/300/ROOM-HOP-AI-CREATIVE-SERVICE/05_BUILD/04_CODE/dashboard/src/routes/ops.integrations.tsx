import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, StatusBadge } from "@/components/w300/status";
import { defaultIntegrations } from "@/lib/w300/demo-data";
export const Route = createFileRoute("/ops/integrations")({
  head: () => ({ meta: [{ title: "Tích hợp — W300 Ops" }] }),
  component: Page,
});
function Page() {
  return (
    <>
      <PageHeader title="Tích hợp" sub="Mặc định: chưa kết nối / chưa xác minh" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {defaultIntegrations.map((i) => (
          <div key={i.id} className="surface p-5">
            <div className="flex justify-between">
              <b>{i.name}</b>
              <StatusBadge value={i.state} />
            </div>
            <dl className="mt-3 space-y-1 text-xs text-muted-foreground">
              <div>
                Env: <code className="font-mono text-foreground">{i.envVar}</code>
              </div>
              <div>Kiểm tra lần cuối: {i.lastChecked ?? "Chưa kiểm tra"}</div>
              <div>Bằng chứng: {i.evidence ?? "—"}</div>
              <div>{i.note}</div>
            </dl>
          </div>
        ))}
      </div>
    </>
  );
}
