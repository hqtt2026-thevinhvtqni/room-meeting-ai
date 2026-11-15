import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { PageHeader, StatusBadge } from "@/components/w300/status";
import { demoWorkPackages } from "@/lib/w300/demo-data";
export const Route = createFileRoute("/ops/work")({ head: () => ({ meta: [{ title: "Tiến độ công việc — W300 Ops" }] }), component: Page });
function Page() {
  const [f, setF] = useState("ALL");
  const rows = demoWorkPackages.filter((w) => f === "ALL" || w.status === f);
  return (<><PageHeader title="Tiến độ công việc" sub="Work packages · Dữ liệu minh họa" />
    <div className="mb-4 flex flex-wrap gap-2">{["ALL", "PLANNED", "IN_PROGRESS", "BLOCKED", "DONE"].map((s) => <button key={s} onClick={() => setF(s)} className={`rounded-full border px-3 py-1 text-xs ${f === s ? "border-primary bg-primary/15 text-primary" : "border-border text-muted-foreground"}`}>{s}</button>)}</div>
    <div className="surface overflow-x-auto"><table className="w-full text-sm"><thead className="text-left text-xs text-muted-foreground"><tr>{["ID", "Hạng mục", "Owner", "Trạng thái", "Ưu tiên", "Hạn", "Bằng chứng", "Bước tiếp"].map((h) => <th key={h} className="px-4 py-3">{h}</th>)}</tr></thead>
    <tbody>{rows.map((w) => <tr key={w.id} className="border-t border-border"><td className="px-4 py-3 font-mono">{w.id}</td><td className="px-4 py-3">{w.title}</td><td className="px-4 py-3">{w.owner}</td><td className="px-4 py-3"><StatusBadge value={w.status} /></td><td className="px-4 py-3"><StatusBadge value={w.priority} /></td><td className="px-4 py-3">{w.due}</td><td className="px-4 py-3 text-muted-foreground">{w.evidence ?? "—"}</td><td className="px-4 py-3 text-muted-foreground">{w.nextStep}</td></tr>)}</tbody></table></div></>);
}