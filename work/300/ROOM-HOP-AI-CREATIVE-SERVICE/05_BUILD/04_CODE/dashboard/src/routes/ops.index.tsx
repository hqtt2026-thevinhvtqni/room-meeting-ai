import { createFileRoute, Link } from "@tanstack/react-router";
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from "recharts";
import { PageHeader, Section, Stat, StatusBadge, DemoTag } from "@/components/w300/status";
import { DEMO_PHASE, demoDecisions, demoGates, demoJournal, demoRisks, demoWorkPackages, defaultIntegrations } from "@/lib/w300/demo-data";
import { Progress } from "@/components/ui/progress";

export const Route = createFileRoute("/ops/")({
  head: () => ({ meta: [{ title: "Tổng quan Ops — W300" }, { name: "description", content: "Tổng quan tiến độ W300 nội bộ." }, { property: "og:title", content: "Ops overview — W300" }, { property: "og:description", content: "Internal overview" }] }),
  component: Overview,
});

function Overview() {
  const counts = (["PLANNED", "IN_PROGRESS", "BLOCKED", "DONE"] as const).map((s) => ({ s, n: demoWorkPackages.filter((w) => w.status === s).length }));
  const blockers = demoWorkPackages.filter((w) => w.status === "BLOCKED");
  return (
    <>
      <PageHeader title="Tổng quan W300" sub="ROOM-HOP AI Creative Service · Dữ liệu minh họa / Demo data" />
      <div className="mb-6 surface bg-hero p-6">
        <div className="flex items-center justify-between"><div className="text-xs text-muted-foreground">Giai đoạn hiện tại</div><DemoTag /></div>
        <div className="mt-1 flex flex-wrap items-center gap-3"><h2 className="text-xl font-semibold">{DEMO_PHASE.name}</h2><StatusBadge value={DEMO_PHASE.status} /></div>
        <Progress value={DEMO_PHASE.percent} className="mt-4 h-2" /><div className="mt-1 text-xs text-muted-foreground">{DEMO_PHASE.percent}% (ước tính thủ công)</div>
      </div>
      <div className="mb-6 grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Stat label="Work packages" value={demoWorkPackages.length} />
        <Stat label="Đang bị chặn" value={blockers.length} hint="Blockers" />
        <Stat label="Gate đã qua" value={`${demoGates.filter((g) => g.status === "PASSED").length}/9`} />
        <Stat label="Tích hợp đã kết nối" value={`0/${defaultIntegrations.length}`} hint="Chưa kết nối" demo={false} />
      </div>
      <div className="grid gap-6 lg:grid-cols-3">
        <Section title="Gates G0–G8" right={<DemoTag />}>
          <ol className="space-y-2">{demoGates.map((g) => <li key={g.id} className="flex items-center justify-between text-sm"><span><span className="font-mono text-muted-foreground">{g.id}</span> {g.name}</span><StatusBadge value={g.status} /></li>)}</ol>
        </Section>
        <Section title="Work packages theo trạng thái" right={<DemoTag />}>
          <div className="h-56"><ResponsiveContainer><BarChart data={counts}><XAxis dataKey="s" tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} /><YAxis allowDecimals={false} tick={{ fontSize: 10, fill: "var(--muted-foreground)" }} /><Tooltip contentStyle={{ background: "var(--popover)", border: "1px solid var(--border)" }} /><Bar dataKey="n" fill="var(--primary)" radius={[6, 6, 0, 0]} /></BarChart></ResponsiveContainer></div>
        </Section>
        <Section title="Blockers & rủi ro P0">
          <ul className="space-y-3 text-sm">
            {blockers.map((b) => <li key={b.id}><StatusBadge value="BLOCKED" /> <span className="ml-1">{b.id} · {b.title}</span></li>)}
            {demoRisks.filter((r) => r.severity === "P0").map((r) => <li key={r.id}><StatusBadge value="P0" /> <span className="ml-1">{r.title}</span></li>)}
          </ul>
        </Section>
        <Section title="Quyết định review gần đây"><ul className="space-y-2 text-sm">{demoDecisions.map((d) => <li key={d.id} className="flex justify-between gap-2"><span>{d.title}</span><span className="text-muted-foreground">{d.outcome}</span></li>)}</ul></Section>
        <Section title="Nhật ký gần đây" right={<Link to="/ops/journal" className="text-xs text-primary">Xem tất cả</Link>}><ul className="space-y-2 text-sm">{demoJournal.slice(0, 3).map((j) => <li key={j.id} className="flex justify-between gap-2"><span>{j.actor} · {j.action}</span><StatusBadge value={j.result} /></li>)}</ul></Section>
        <Section title="Sức khỏe tích hợp" right={<Link to="/ops/integrations" className="text-xs text-primary">Chi tiết</Link>}><ul className="space-y-2 text-sm">{defaultIntegrations.map((i) => <li key={i.id} className="flex justify-between"><span>{i.name}</span><StatusBadge value={i.state} /></li>)}</ul></Section>
      </div>
    </>
  );
}