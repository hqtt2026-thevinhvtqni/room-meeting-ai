import { Link } from "@tanstack/react-router";
import type { ReactNode } from "react";
import { ShieldAlert } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useW300 } from "@/lib/w300/store";
import type { Role } from "@/lib/w300/types";

export function RoleGate({ allow, children, message }: { allow: (r: Role) => boolean; children: ReactNode; message: string }) {
  const { role, hydrated } = useW300();
  if (!hydrated) return <div className="mx-auto max-w-3xl space-y-4 p-10"><Skeleton className="h-10 w-1/2" /><Skeleton className="h-40" /></div>;
  if (!allow(role)) return (
    <div className="grid min-h-screen place-items-center px-6">
      <div className="surface max-w-md p-8 text-center">
        <ShieldAlert className="mx-auto size-10 text-destructive" />
        <h1 className="mt-4 text-xl font-semibold">Không có quyền truy cập</h1>
        <p className="mt-2 text-sm text-muted-foreground">{message}</p>
        <div className="mt-6 flex justify-center gap-2"><Button asChild variant="hero"><Link to="/signin">Đăng nhập demo</Link></Button><Button asChild variant="outline"><Link to="/">Trang chủ</Link></Button></div>
      </div>
    </div>
  );
  return <>{children}</>;
}