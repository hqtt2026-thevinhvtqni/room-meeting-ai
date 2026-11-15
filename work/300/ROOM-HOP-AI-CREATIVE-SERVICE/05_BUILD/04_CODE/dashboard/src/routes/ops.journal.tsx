import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, StatusBadge } from "@/components/w300/status";
import { demoJournal } from "@/lib/w300/demo-data";
export const Route = createFileRoute("/ops/journal")({
  head: () => ({ meta: [{ title: "Nhật ký — W300 Ops" }] }),
  component: Page,
});
function Page() {
  return (
    <>
      <PageHeader title="Nhật ký / Audit" sub="Dữ liệu minh họa" />
      <div className="surface overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left text-xs text-muted-foreground">
            <tr>
              {[
                "Thời gian",
                "Actor",
                "Scope",
                "Hành động",
                "Bằng chứng",
                "Kết quả",
                "Bước tiếp",
              ].map((h) => (
                <th key={h} className="px-4 py-3">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {demoJournal.map((j) => (
              <tr key={j.id} className="border-t border-border">
                <td className="px-4 py-3 font-mono text-xs">
                  {j.ts.replace("T", " ").slice(0, 16)}
                </td>
                <td className="px-4 py-3">{j.actor}</td>
                <td className="px-4 py-3">{j.scope}</td>
                <td className="px-4 py-3">{j.action}</td>
                <td className="px-4 py-3 text-muted-foreground">{j.evidence ?? "—"}</td>
                <td className="px-4 py-3">
                  <StatusBadge value={j.result} />
                </td>
                <td className="px-4 py-3 text-muted-foreground">{j.nextStep}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
