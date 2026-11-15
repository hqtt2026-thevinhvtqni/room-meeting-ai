import { createFileRoute, Outlet } from "@tanstack/react-router";
import { Home, PlusCircle, FolderKanban, Images, User, BookOpen } from "lucide-react";
import { AppShell } from "@/components/w300/shell";
import { RoleGate } from "@/components/w300/guard";
import { canAccessPortal } from "@/lib/w300/rules";
export const Route = createFileRoute("/app")({
  head: () => ({ meta: [{ title: "Cổng khách hàng — W300" }] }),
  component: L,
});
const nav = [
  { to: "/app", label: "Trang chính", icon: <Home /> },
  { to: "/app/new", label: "Tạo yêu cầu", icon: <PlusCircle /> },
  { to: "/app/jobs", label: "Dự án & job", icon: <FolderKanban /> },
  { to: "/app/gallery", label: "Kết quả", icon: <Images /> },
  { to: "/app/account", label: "Tài khoản", icon: <User /> },
  { to: "/docs", label: "Tài liệu MCP", icon: <BookOpen /> },
];
function L() {
  return (
    <RoleGate allow={canAccessPortal} message="Vui lòng đăng nhập (demo) để dùng cổng khách hàng.">
      <AppShell nav={nav} sub="Customer portal">
        <Outlet />
      </AppShell>
    </RoleGate>
  );
}
