import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Building2, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DemoBanner } from "@/components/w300/status";
import { Logo } from "@/components/w300/shell";
import { useW300 } from "@/lib/w300/store";

export const Route = createFileRoute("/signin")({
  head: () => ({
    meta: [
      { title: "Đăng nhập demo — W300" },
      {
        name: "description",
        content: "Đăng nhập mô phỏng cho bản xem trước W300. Xác thực chưa kết nối.",
      },
      { property: "og:title", content: "Đăng nhập demo — W300" },
      { property: "og:description", content: "Xác thực mô phỏng, chưa kết nối." },
    ],
  }),
  component: SignIn,
});

function SignIn() {
  const { setRole } = useW300();
  const nav = useNavigate();
  return (
    <div className="min-h-screen bg-hero">
      <DemoBanner />
      <div className="mx-auto flex max-w-md flex-col gap-6 px-6 py-16">
        <Logo />
        <div className="surface p-6">
          <h1 className="text-2xl font-semibold">Đăng nhập</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Xác thực đang ở chế độ <b className="text-warning">demo / chưa kết nối</b>. Chọn vai trò
            để xem trước giao diện. Không có tài khoản thật nào được tạo.
          </p>
          <div className="mt-6 space-y-3">
            <Button
              variant="hero"
              className="h-auto w-full justify-start gap-3 py-3"
              onClick={() => {
                setRole("customer");
                nav({ to: "/app" });
              }}
            >
              <User />
              <span className="text-left">
                <span className="block">Khách hàng</span>
                <span className="block text-xs opacity-80">Customer portal · /app</span>
              </span>
            </Button>
            <Button
              variant="outline"
              className="h-auto w-full justify-start gap-3 py-3"
              onClick={() => {
                setRole("internal");
                nav({ to: "/ops" });
              }}
            >
              <Building2 />
              <span className="text-left">
                <span className="block">Nội bộ ROOM-HOP</span>
                <span className="block text-xs text-muted-foreground">
                  Internal operations · /ops
                </span>
              </span>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
