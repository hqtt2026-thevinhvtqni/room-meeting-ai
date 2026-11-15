import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, Section, StatusBadge } from "@/components/w300/status";
import { demoDecisions, demoReviews, demoRisks } from "@/lib/w300/demo-data";
export const Route = createFileRoute("/ops/review")({
  head: () => ({ meta: [{ title: "Kiến trúc & review — W300 Ops" }] }),
  component: Page,
});
function Page() {
  return (
    <>
      <PageHeader title="Kiến trúc & review" sub="Ma trận reviewer · Dữ liệu minh họa" />
      <div className="grid gap-6 lg:grid-cols-2">
        <Section title="Reviewer matrix">
          <ul className="space-y-3">
            {demoReviews.map((r) => (
              <li key={r.reviewer} className="flex items-center justify-between gap-2 text-sm">
                <span>
                  <b>{r.reviewer}</b> · {r.scope}
                  {r.note && <span className="block text-xs text-muted-foreground">{r.note}</span>}
                </span>
                <StatusBadge value={r.status} />
              </li>
            ))}
          </ul>
        </Section>
        <Section title="Rủi ro chưa xử lý">
          <ul className="space-y-3 text-sm">
            {demoRisks.map((r) => (
              <li key={r.id}>
                <StatusBadge value={r.severity} /> {r.title}
                <div className="text-xs text-muted-foreground">
                  {r.owner} · {r.mitigation}
                </div>
              </li>
            ))}
          </ul>
        </Section>
        <Section title="Decision log">
          <ul className="space-y-2 text-sm">
            {demoDecisions.map((d) => (
              <li key={d.id} className="flex justify-between gap-2">
                <span className="font-mono text-muted-foreground">{d.id}</span>
                <span className="flex-1">{d.title}</span>
                <span>
                  {d.outcome} · {d.by}
                </span>
              </li>
            ))}
          </ul>
        </Section>
      </div>
    </>
  );
}
