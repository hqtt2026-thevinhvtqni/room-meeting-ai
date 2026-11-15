import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, Section, StatusBadge } from "@/components/w300/status";
export const Route = createFileRoute("/app/account")({ head: () => ({ meta: [{ title: "Tài khoản & sử dụng — W300" }] }), component: P });
function P() {
  return (<><PageHeader title="Tài khoản & sử dụng" />
    <div className="grid gap-6 lg:grid-cols-2">
      <Section title="Gói dịch vụ" right={<StatusBadge value="NOT_CONNECTED" />}><p className="text-sm text-muted-foreground">Gói và hạn mức chưa được kích hoạt (not yet enabled). Không có thanh toán nào được xử lý.</p></Section>
      <Section title="Mức sử dụng"><p className="text-sm text-muted-foreground">Chưa có dữ liệu sử dụng thật. Số liệu sẽ hiển thị khi hệ thống tính phí được xác minh.</p></Section>
    </div></>);
}