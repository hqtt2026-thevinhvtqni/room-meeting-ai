import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, StatusBadge, DemoTag } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { JOB_TYPE_LABEL } from "@/lib/w300/types";
export const Route = createFileRoute("/ops/production")({
  head: () => ({ meta: [{ title: "Giám sát sản xuất — W300 Ops" }] }),
  component: Page,
});
function Page() {
  const { jobs } = useW300();
  return (
    <>
      <PageHeader
        title="Giám sát sản xuất"
        sub="Hàng đợi job · Chi phí chỉ hiển thị khi có nguồn"
      />
      <div className="surface overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="text-left text-xs text-muted-foreground">
            <tr>
              {["Mã job", "Loại", "Trạng thái", "Provider", "Thời lượng", "Retry", "Chi phí"].map(
                (h) => (
                  <th key={h} className="px-4 py-3">
                    {h}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody>
            {jobs.map((j) => (
              <tr key={j.id} className="border-t border-border">
                <td className="px-4 py-3 font-mono">
                  {j.ref} {j.isDemo && <DemoTag />}
                </td>
                <td className="px-4 py-3">{JOB_TYPE_LABEL[j.type].en}</td>
                <td className="px-4 py-3">
                  <StatusBadge value={j.status} />
                </td>
                <td className="px-4 py-3">
                  <StatusBadge value={j.providerStatus} />
                </td>
                <td className="px-4 py-3">{j.durationSec ? `${j.durationSec}s` : "—"}</td>
                <td className="px-4 py-3">{j.retries}</td>
                <td className="px-4 py-3 text-muted-foreground">
                  {j.costSource ? (j.costActual ?? j.costEstimate) : "Chưa có nguồn"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
