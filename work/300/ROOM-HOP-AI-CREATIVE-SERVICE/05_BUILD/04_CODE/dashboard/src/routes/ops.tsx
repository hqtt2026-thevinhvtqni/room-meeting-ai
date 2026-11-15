import { createFileRoute, Outlet } from "@tanstack/react-router";
import { LayoutDashboard, ListChecks, Activity, ShieldCheck, Plug, ScrollText } from "lucide-react";
import { AppShell } from "@/components/w300/shell";
import { RoleGate } from "@/components/w300/guard";
import { canAccessOps } from "@/lib/w300/rules";

export const Route = createFileRoute("/ops")({
  head: () => ({
    meta: [{ title: "Ops — W300 ROOM-HOP" }, { name: "robots", content: "noindex" }],
  }),
  component: OpsLayout,
});

const nav = [
  { to: "/ops", label: "Tổng quan", icon: <LayoutDashboard /> },
  { to: "/ops/work", label: "Tiến độ công việc", icon: <ListChecks /> },
  { to: "/ops/production", label: "Giám sát sản xuất", icon: <Activity /> },
  { to: "/ops/review", label: "Kiến trúc & review", icon: <ShieldCheck /> },
  { to: "/ops/integrations", label: "Tích hợp", icon: <Plug /> },
  { to: "/ops/journal", label: "Nhật ký / Audit", icon: <ScrollText /> },
];

function OpsLayout() {
  return (
    <RoleGate
      allow={canAccessOps}
      message="Khu vực Ops chỉ dành cho vai trò nội bộ ROOM-HOP. Tài khoản khách hàng không thể truy cập."
    >
      <AppShell nav={nav} sub="Internal Operations">
        <Outlet />
      </AppShell>
    </RoleGate>
  );
}
