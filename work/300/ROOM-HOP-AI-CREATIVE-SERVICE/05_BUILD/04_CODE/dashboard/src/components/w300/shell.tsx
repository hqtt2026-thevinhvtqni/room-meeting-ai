import { Link, useLocation } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import { Menu, X, Sparkles, LogOut } from "lucide-react";
import { cn } from "@/lib/utils";
import { useW300 } from "@/lib/w300/store";
import { DemoBanner } from "./status";

export interface NavItem {
  to: string;
  label: string;
  icon: ReactNode;
}

export function Logo({ sub }: { sub?: string }) {
  return (
    <Link to="/" className="flex items-center gap-2.5">
      <span className="grid size-8 place-items-center rounded-lg bg-gradient-primary shadow-glow">
        <Sparkles className="size-4 text-primary-foreground" />
      </span>
      <span className="leading-tight">
        <span className="block font-display text-sm font-bold">W300</span>
        <span className="block text-[11px] text-muted-foreground">
          {sub ?? "ROOM-HOP AI Creative"}
        </span>
      </span>
    </Link>
  );
}

export function AppShell({
  nav,
  sub,
  children,
}: {
  nav: NavItem[];
  sub: string;
  children: ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();
  const { role, setRole } = useW300();
  const links = (
    <nav className="flex flex-col gap-1">
      {nav.map((n) => {
        const active =
          n.to === pathname || (n.to.split("/").length > 2 && pathname.startsWith(n.to));
        return (
          <Link
            key={n.to}
            to={n.to}
            onClick={() => setOpen(false)}
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
              active
                ? "bg-sidebar-accent text-sidebar-accent-foreground"
                : "text-sidebar-foreground/70 hover:bg-sidebar-accent/60 hover:text-sidebar-foreground",
            )}
          >
            <span className={cn("[&_svg]:size-4", active && "text-primary")}>{n.icon}</span>
            {n.label}
          </Link>
        );
      })}
    </nav>
  );
  const footer = (
    <div className="mt-auto space-y-2 border-t border-sidebar-border pt-4 text-xs text-muted-foreground">
      <div>
        Vai trò (demo): <span className="font-mono text-foreground">{role}</span>
      </div>
      <Link
        to="/"
        onClick={() => setRole("guest")}
        className="flex items-center gap-2 hover:text-foreground"
      >
        <LogOut className="size-3.5" />
        Đăng xuất demo
      </Link>
    </div>
  );
  return (
    <div className="flex min-h-screen flex-col">
      <DemoBanner />
      <div className="flex flex-1">
        <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col gap-6 border-r border-sidebar-border bg-sidebar p-4 lg:flex">
          <Logo sub={sub} />
          {links}
          {footer}
        </aside>
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex items-center justify-between border-b border-border px-4 py-3 lg:hidden">
            <Logo sub={sub} />
            <button
              aria-label="Mở menu"
              onClick={() => setOpen(true)}
              className="rounded-md p-2 hover:bg-accent"
            >
              <Menu className="size-5" />
            </button>
          </header>
          {open && (
            <div className="fixed inset-0 z-50 flex lg:hidden">
              <div className="flex w-72 flex-col gap-6 bg-sidebar p-4">
                <div className="flex items-center justify-between">
                  <Logo sub={sub} />
                  <button aria-label="Đóng menu" onClick={() => setOpen(false)}>
                    <X className="size-5" />
                  </button>
                </div>
                {links}
                {footer}
              </div>
              <button
                aria-label="Đóng"
                className="flex-1 bg-background/70"
                onClick={() => setOpen(false)}
              />
            </div>
          )}
          <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 sm:px-8 sm:py-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
