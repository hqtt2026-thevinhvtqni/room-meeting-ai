import { createFileRoute, Link } from "@tanstack/react-router";
import { DemoBanner, StatusBadge } from "@/components/w300/status";
import { Logo } from "@/components/w300/shell";

export const Route = createFileRoute("/docs")({
  head: () => ({
    meta: [
      { title: "Tài liệu MCP — W300" },
      {
        name: "description",
        content:
          "Cách W300 dự kiến kết nối qua MCP: công cụ dự kiến, mô hình xác thực và giới hạn dịch vụ.",
      },
      { property: "og:title", content: "Tài liệu MCP — W300" },
      { property: "og:description", content: "Công cụ MCP dự kiến của W300 (chưa xác minh)." },
    ],
  }),
  component: Docs,
});

const tools = [
  ["image.generate", "Tạo ảnh từ prompt, tỉ lệ khung, số lượng"],
  ["image.edit", "Chỉnh sửa / ghép ảnh với ảnh tham chiếu"],
  ["video.generate", "Tạo video ngắn từ mô tả"],
  ["video.from_image", "Chuyển ảnh tĩnh thành video"],
  ["storyboard.create", "Tạo storyboard nhiều khung"],
  ["job.status", "Tra cứu trạng thái job theo mã"],
  ["asset.deliver", "Lấy liên kết bàn giao có thời hạn"],
];

function Docs() {
  return (
    <div className="min-h-screen">
      <DemoBanner />
      <header className="mx-auto flex max-w-4xl items-center justify-between px-6 py-5">
        <Logo />
        <Link to="/signin" className="text-sm text-primary">
          Đăng nhập demo
        </Link>
      </header>
      <article className="mx-auto max-w-4xl space-y-8 px-6 pb-24">
        <div>
          <h1 className="text-3xl font-bold sm:text-4xl">Kết nối W300 qua MCP</h1>
          <p className="mt-3 text-muted-foreground">
            W300 được thiết kế như một dịch vụ MCP (Model Context Protocol) công khai. Client MCP
            (trợ lý AI, công cụ sáng tạo) gọi các tool bên dưới.{" "}
            <b className="text-warning">
              Tất cả tool đang ở trạng thái dự kiến (planned) — backend chưa được xác minh.
            </b>
          </p>
        </div>
        <section className="surface p-6">
          <h2 className="text-lg font-semibold">Luồng khái niệm</h2>
          <ol className="mt-3 list-decimal space-y-1.5 pl-5 text-sm text-muted-foreground">
            <li>Client xác thực với MCP Gateway của W300.</li>
            <li>
              Gọi tool (ví dụ <code className="font-mono text-foreground">image.generate</code>) →
              nhận mã job.
            </li>
            <li>
              Theo dõi bằng <code className="font-mono text-foreground">job.status</code>.
            </li>
            <li>Nhận asset qua liên kết có thời hạn.</li>
          </ol>
        </section>
        <section className="surface overflow-hidden">
          <h2 className="p-6 pb-3 text-lg font-semibold">Tool dự kiến</h2>
          <ul>
            {tools.map(([n, d]) => (
              <li
                key={n}
                className="flex flex-col gap-1 border-t border-border px-6 py-3 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <code className="font-mono text-sm text-primary">{n}</code>
                  <div className="text-sm text-muted-foreground">{d}</div>
                </div>
                <StatusBadge value="PLANNED" />
              </li>
            ))}
          </ul>
        </section>
        <section className="grid gap-4 sm:grid-cols-2">
          <div className="surface p-6">
            <h2 className="font-semibold">Mô hình xác thực (dự kiến)</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              Token theo tài khoản khách hàng, phạm vi theo project. Token không bao giờ được nhúng
              vào trình duyệt; khóa nhà cung cấp AI chỉ nằm phía máy chủ ROOM-HOP.
            </p>
          </div>
          <div className="surface p-6">
            <h2 className="font-semibold">Giới hạn hiện tại</h2>
            <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted-foreground">
              <li>Chưa có endpoint công khai.</li>
              <li>Chưa xử lý thanh toán.</li>
              <li>Chi phí/thời gian chỉ là ước tính khi có nguồn.</li>
              <li>Nội dung tải lên cần có quyền sử dụng.</li>
            </ul>
          </div>
        </section>
      </article>
    </div>
  );
}
