import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

const tone: Record<string, string> = {
  ok: "bg-success/15 text-success border-success/30",
  warn: "bg-warning/15 text-warning border-warning/30",
  bad: "bg-destructive/15 text-destructive border-destructive/30",
  info: "bg-info/15 text-info border-info/30",
  pri: "bg-primary/15 text-primary border-primary/30",
  mute: "bg-muted text-muted-foreground border-border",
};
const map: Record<string, keyof typeof tone> = {
  DONE: "ok", COMPLETED: "ok", APPROVE: "ok", PASS: "ok", PASSED: "ok", CONNECTED: "ok",
  IN_PROGRESS: "info", RUNNING: "info", IN_REVIEW: "info",
  NEEDS_REVIEW: "warn", CONDITIONAL: "warn", UNVERIFIED: "warn", QUEUED: "pri", PENDING: "mute",
  BLOCKED: "bad", FAILED: "bad", REJECT: "bad", FAIL: "bad", ERROR: "bad",
  PLANNED: "mute", CANCELLED: "mute", NOT_REQUESTED: "mute", NOT_CONNECTED: "mute",
  P0: "bad", P1: "warn", P2: "info", P3: "mute",
};
const label: Record<string, string> = { NOT_CONNECTED: "Chưa kết nối", UNVERIFIED: "Chưa xác minh" };

export function StatusBadge({ value, className }: { value: string; className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-1.5 whitespace-nowrap rounded-full border px-2.5 py-0.5 font-mono text-[11px] font-medium", tone[map[value] ?? "mute"], className)}>
      <span className="size-1.5 rounded-full bg-current" />{label[value] ?? value.replace(/_/g, " ")}
    </span>
  );
}

export function DemoTag({ className }: { className?: string }) {
  return <span className={cn("rounded border border-warning/40 bg-warning/10 px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wider text-warning", className)}>Demo</span>;
}

export function DemoBanner() {
  return (
    <div role="status" className="demo-stripes border-b border-warning/30 bg-background px-4 py-1.5 text-center text-xs font-medium text-warning">
      DEMO — Backend/MCP chưa kết nối · Mọi dữ liệu là dữ liệu minh họa (Demo data). Không có job thật nào được chạy.
    </div>
  );
}

export function PageHeader({ title, sub, actions }: { title: string; sub?: string; actions?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div><h1 className="text-2xl font-semibold sm:text-3xl">{title}</h1>{sub && <p className="mt-1 text-sm text-muted-foreground">{sub}</p>}</div>
      {actions && <div className="flex gap-2">{actions}</div>}
    </div>
  );
}

export function Stat({ label, value, hint, demo = true }: { label: string; value: ReactNode; hint?: string; demo?: boolean }) {
  return (
    <div className="surface p-5">
      <div className="flex items-center justify-between text-xs text-muted-foreground">{label}{demo && <DemoTag />}</div>
      <div className="mt-2 font-display text-3xl font-semibold">{value}</div>
      {hint && <div className="mt-1 text-xs text-muted-foreground">{hint}</div>}
    </div>
  );
}

export function Empty({ icon, title, sub, action }: { icon: ReactNode; title: string; sub?: string; action?: ReactNode }) {
  return (
    <div className="surface flex flex-col items-center px-6 py-14 text-center">
      <div className="mb-3 grid size-12 place-items-center rounded-full bg-primary/15 text-primary">{icon}</div>
      <h3 className="font-semibold">{title}</h3>{sub && <p className="mt-1 max-w-sm text-sm text-muted-foreground">{sub}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

export function Section({ title, children, right }: { title: string; children: ReactNode; right?: ReactNode }) {
  return <section className="surface p-5"><div className="mb-4 flex items-center justify-between gap-2"><h2 className="text-base font-semibold">{title}</h2>{right}</div>{children}</section>;
}