import { createFileRoute } from "@tanstack/react-router";
import { PageHeader, Section, StatusBadge, DemoTag } from "@/components/w300/status";
import { useW300 } from "@/lib/w300/store";
import { JOB_TYPE_LABEL, type JobType } from "@/lib/w300/types";
export const Route = createFileRoute("/app/account")({ head: () => ({ meta: [{ title: "Tài khoản & sử dụng — W300" }] }), component: P });
function P() {
  const { jobs, role } = useW300();
  const byType = (Object.keys(JOB_TYPE_LABEL) as JobType[]).map((t) => ({ t, n: jobs.filter((j) => j.type === t).length })).filter((x) => x.n > 0);
  return (<>
    <PageHeader title="Tài khoản & sử dụng" />
    <div className="grid gap-6 lg:grid-cols-2">
      <Section title="Gói dịch vụ" right={<StatusBadge value="NOT_CONNECTED" />}>
        <p className="text-sm text-muted-foreground">Gói và hạn mức chưa được kích hoạt (not yet enabled). Không có thanh toán nào được xử lý.</p>
      </Section>
      <Section title="Phiên bản demo" right={<DemoTag />}>
        <p className="text-sm text-muted-foreground">Vai trò hiện tại: <span className="font-mono text-foreground">{role}</span>. Dữ liệu job được lưu cục bộ trên trình duyệt này và không được gửi tới máy chủ nào.</p>
      </Section>
      <Section title="Mức sử dụng" right={<DemoTag />}>
        {byType.length === 0 ? <p className="text-sm text-muted-foreground">Chưa có dữ liệu sử dụng thật. Số liệu sẽ hiển thị khi hệ thống tính phí được xác minh.</p> : (
          <ul className="space-y-2 text-sm">{byType.map((x) => <li key={x.t} className="flex justify-between"><span>{JOB_TYPE_LABEL[x.t].vi}</span><span className="font-mono text-muted-foreground">{x.n} job (demo)</span></li>)}</ul>
        )}
      </Section>
      <Section title="Bảo mật & quyền riêng tư">
        <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
          <li>Chưa có xác thực thật; đăng nhập chỉ mang tính minh họa.</li>
          <li>Tệp tham chiếu chỉ được giữ trên trình duyệt, không tải lên máy chủ.</li>
          <li>Không có nhà cung cấp AI, lưu trữ hay thanh toán nào được kết nối.</li>
        </ul>
      </Section>
    </div>
  </>);
}
