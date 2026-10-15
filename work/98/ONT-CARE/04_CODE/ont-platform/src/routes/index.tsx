import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { parseDeepLink, ontTabs } from "@/lib/deep-links";
import { useMemo, useState } from "react";
import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  Bell,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  CircleHelp,
  ClipboardList,
  Download,
  Gauge,
  HardDrive,
  LayoutDashboard,
  MapPin,
  Network,
  Radio,
  RefreshCw,
  Search,
  ShieldCheck,
  Signal,
  SlidersHorizontal,
  Users,
  Wifi,
  Wrench,
  X,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { usePlatform } from "@/components/platform-context";
import {
  customers,
  onts,
  technicians,
  lanDevices,
  customerFor,
  ontFor,
  techFor,
  statusLabels,
  type OntStatus,
  type TicketStatus,
  type Ticket,
} from "@/lib/ont-data";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Tổng quan vận hành | ONT Platform" },
      {
        name: "description",
        content: "Trung tâm quản lý, giám sát ONT và điều phối sự cố Internet.",
      },
      { property: "og:title", content: "ONT Platform — Tổng quan vận hành" },
      {
        property: "og:description",
        content: "Giám sát ONT, khách hàng, sức khỏe mạng và sự cố trên một nền tảng.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  validateSearch: parseDeepLink,
  component: Dashboard,
});

type Section =
  | "Tổng quan"
  | "Khách hàng"
  | "ONT"
  | "Health Monitor"
  | "Speed Test"
  | "LAN Guard"
  | "Ticket / Sự cố"
  | "Kỹ thuật viên"
  | "Báo cáo";
const areas = ["Quận 1", "Quận 3", "Bình Thạnh", "Phú Nhuận", "Thủ Đức"];
const menu: { label: Section; icon: typeof Activity }[] = [
  { label: "Tổng quan", icon: LayoutDashboard },
  { label: "Khách hàng", icon: Users },
  { label: "ONT", icon: HardDrive },
  { label: "Health Monitor", icon: Activity },
  { label: "Speed Test", icon: Gauge },
  { label: "LAN Guard", icon: ShieldCheck },
  { label: "Ticket / Sự cố", icon: ClipboardList },
  { label: "Kỹ thuật viên", icon: Wrench },
  { label: "Báo cáo", icon: SlidersHorizontal },
];
const tone = (s: string) =>
  s === "ONLINE" || s === "RESOLVED" || s === "CLOSED" || s === "AVAILABLE"
    ? "good"
    : s === "WARNING" || s === "ASSIGNED" || s === "WAITING_CUSTOMER" || s === "BUSY"
      ? "warn"
      : s === "OFFLINE" || s === "OPEN"
        ? "bad"
        : "info";
function Status({ value, label }: { value: string; label?: string }) {
  return (
    <span className={`status status-${tone(value)}`}>
      <span className="status-dot" />
      {label ?? statusLabels[value as OntStatus | TicketStatus] ?? value}
    </span>
  );
}
function SectionHead({
  eyebrow,
  title,
  action,
}: {
  eyebrow: string;
  title: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="section-head">
      <div>
        <div className="eyebrow">{eyebrow}</div>
        <h2>{title}</h2>
      </div>
      {action}
    </div>
  );
}
function Empty({ text = "Không tìm thấy kết quả phù hợp." }: { text?: string }) {
  return <div className="empty">{text}</div>;
}
const speedBars = [
  38, 47, 42, 59, 55, 65, 60, 72, 58, 74, 69, 83, 73, 79, 70, 89, 78, 86, 73, 93, 80, 89, 76, 88,
];
function Dashboard() {
  const { tickets, updateTicket, notify } = usePlatform();
  const [section, setSection] = useState<Section>("Tổng quan");
  const sp = Route.useSearch();
  const navigate = useNavigate({ from: "/" });
  const selectedId = sp.ont ?? null;
  const detailTab = sp.tab && ontTabs.includes(sp.tab) ? sp.tab : "Overview";
  const setDetailTab = (tab: string) => navigate({ search: { ont: sp.ont, tab } });
  const setSelectedId = (_: null) => navigate({ search: {} });
  const deepTicket = sp.ticket ? tickets.find((t) => t.id === sp.ticket) : undefined;
  const missing =
    sp.ont && !ontFor(sp.ont)
      ? `ONT ${sp.ont}`
      : sp.ticket && !deepTicket
        ? `Ticket ${sp.ticket}`
        : null;
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("Tất cả");
  const [page, setPage] = useState(1);
  const [confirm, setConfirm] = useState<string | null>(null);
  const [notifications, setNotifications] = useState(false);
  const [sidebar, setSidebar] = useState(false);
  const selected = selectedId ? ontFor(selectedId) : undefined;
  const customer = selected ? customerFor(selected.customerId) : undefined;
  const q = search.toLocaleLowerCase("vi");
  const visibleOnts = useMemo(
    () =>
      onts.filter(
        (o) =>
          (filter === "Tất cả" || o.status === filter) &&
          (o.id.toLowerCase().includes(q) ||
            o.serial.toLowerCase().includes(q) ||
            customerFor(o.customerId)?.name.toLocaleLowerCase("vi").includes(q)),
      ),
    [q, filter],
  );
  const go = (value: Section) => {
    setSection(value);
    navigate({ search: {} });
    setSearch("");
    setFilter("Tất cả");
    setPage(1);
    setSidebar(false);
  };
  const openOnt = (id: string) => navigate({ search: { ont: id } });
  const tableOnts = visibleOnts.slice((page - 1) * 10, page * 10);
  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebar ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">
            <Network size={20} strokeWidth={2.3} />
          </div>
          <div>
            <strong>
              ONT<span>Platform</span>
            </strong>
            <small>NETWORK OPERATIONS</small>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="ml-auto lg:hidden"
            onClick={() => setSidebar(false)}
            aria-label="Đóng menu"
          >
            <X />
          </Button>
        </div>
        <div className="workspace">
          <span className="workspace-avatar">VX</span>
          <div className="min-w-0">
            <strong>Vận hành mạng</strong>
            <small>Không gian làm việc</small>
          </div>
          <ChevronDown size={14} />
        </div>
        <div className="nav-caption">ĐIỀU HƯỚNG</div>
        <nav className="side-nav">
          {menu.map(({ label, icon: Icon }) => (
            <Button
              key={label}
              variant="ghost"
              className={`nav-item ${section === label && !selectedId && !sp.ticket ? "nav-active" : ""}`}
              onClick={() => go(label)}
            >
              <Icon size={18} />
              <span>{label}</span>
              {label === "Ticket / Sự cố" && (
                <em>{tickets.filter((t) => t.status === "OPEN").length}</em>
              )}
            </Button>
          ))}
        </nav>
        <div className="side-bottom">
          <div className="app-switch">
            <div className="nav-caption">GIAO DIỆN KHÁC</div>
            <Link to="/technician">
              <Wrench size={16} /> App Thợ <ArrowUpRight size={13} />
            </Link>
            <Link to="/customer">
              <Users size={16} /> App Khách <ArrowUpRight size={13} />
            </Link>
          </div>
          <div className="side-help">
            <CircleHelp size={17} />
            <div>
              <strong>Trung tâm hỗ trợ</strong>
              <small>Hướng dẫn sử dụng</small>
            </div>
            <ArrowUpRight size={14} />
          </div>
          <div className="sidebar-footer">
            ONT PLATFORM <span>v1.0 · Prototype</span>
          </div>
        </div>
      </aside>
      {sidebar && <div className="mobile-overlay" onClick={() => setSidebar(false)} />}
      <div className="main-area">
        <header className="topbar">
          <div className="topbar-left">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebar(true)}
              aria-label="Mở menu"
            >
              <LayoutDashboard />
            </Button>
            <span className="breadcrumb">Hệ thống</span>
            <ChevronRight size={14} />
            <strong>
              {missing
                ? "Không tìm thấy"
                : deepTicket
                  ? "Chi tiết ticket"
                  : selected
                    ? "Chi tiết ONT"
                    : section}
            </strong>
          </div>
          <div className="topbar-right">
            <span className="system-live">
              <span /> DEMO · DỮ LIỆU MẪU (MOCK)
            </span>
            <div className="topbar-divider" />
            <div className="notification-wrap">
              <Button
                variant="ghost"
                size="icon"
                aria-label="Thông báo"
                title="Thông báo"
                onClick={() => setNotifications(!notifications)}
              >
                <Bell size={19} />
              </Button>
              <i className="notification-pip" />
              {notifications && (
                <div className="notification-pop">
                  <strong>Thông báo</strong>
                  <p>{tickets.filter((t) => t.status === "OPEN").length} sự cố mới cần xử lý</p>
                  <p>12 ONT đang ở trạng thái cảnh báo</p>
                </div>
              )}
            </div>
            <div className="user-profile">
              <span className="user-avatar">AD</span>
              <div>
                <strong>Admin Operator</strong>
                <small>Quản trị viên</small>
              </div>
              <ChevronDown size={14} />
            </div>
          </div>
        </header>
        <main className="content">
          {missing ? (
            <div className="panel detail-panel">
              <SectionHead eyebrow="LIÊN KẾT KHÔNG HỢP LỆ" title={`Không tìm thấy ${missing}`} />
              <p className="note-line">
                Mã này không tồn tại hoặc đã bị xoá. Kiểm tra lại đường dẫn hoặc quay về danh sách.
              </p>
              <div className="detail-actions mt-4">
                <Button onClick={() => go(sp.ticket ? "Ticket / Sự cố" : "ONT")}>
                  <ChevronLeft size={17} /> Về danh sách {sp.ticket ? "ticket" : "ONT"}
                </Button>
              </div>
            </div>
          ) : deepTicket ? (
            <TicketDetail ticket={deepTicket} back={() => go("Ticket / Sự cố")} />
          ) : selected && customer ? (
            <>
              <Button variant="ghost" className="back-link" onClick={() => setSelectedId(null)}>
                <ChevronLeft size={17} /> Quay lại {section}
              </Button>
              <div className="detail-heading">
                <div>
                  <div className="eyebrow">THIẾT BỊ / {selected.id}</div>
                  <h1>{customer.name}</h1>
                  <p>
                    {selected.id} <span>·</span> {selected.serial} <span>·</span> {selected.model}
                  </p>
                </div>
                <div className="detail-actions">
                  <Status value={selected.status} />
                  <Button
                    variant="outline"
                    onClick={() => notify(`Đã làm mới trạng thái ${selected.id}`)}
                  >
                    <RefreshCw /> Làm mới
                  </Button>
                </div>
              </div>
              <div className="detail-meta">
                <span>
                  <MapPin size={15} />
                  {customer.address}
                </span>
                <span>
                  <Radio size={15} /> Lần cuối: {selected.lastSeen}
                </span>
                <span>
                  <Wifi size={15} /> Firmware {selected.firmware}
                </span>
              </div>
              <div className="tab-list">
                {[
                  "Overview",
                  "Internet",
                  "Wi-Fi",
                  "LAN",
                  "Optical / PON",
                  "Devices",
                  "Tests",
                  "Events",
                  "Remote Actions",
                ].map((t) => (
                  <Button
                    key={t}
                    variant="ghost"
                    className={`tab-button ${detailTab === t ? "tab-current" : ""}`}
                    onClick={() => setDetailTab(t)}
                  >
                    {t}
                  </Button>
                ))}
              </div>
              {detailTab === "Overview" && (
                <div className="detail-grid">
                  <div className="panel span-2">
                    <div className="panel-heading">
                      <h3>Tình trạng kết nối</h3>
                      <Status value={selected.status} />
                    </div>
                    <div className="health-grid">
                      {[
                        ["Internet", selected.wan, "WAN"],
                        ["Wi-Fi", selected.wifi, "2.4 / 5 GHz"],
                        ["Tín hiệu quang", `${selected.optical} dBm`, "PON"],
                        ["Thời gian hoạt động", selected.uptime, "Uptime"],
                      ].map(([a, b, c]) => (
                        <div className="health-cell" key={a}>
                          <small>{a}</small>
                          <strong>{b}</strong>
                          <span>{c}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="panel">
                    <div className="panel-heading">
                      <h3>Thông tin khách hàng</h3>
                    </div>
                    <div className="kv">
                      <span>Họ tên</span>
                      <strong>{customer.name}</strong>
                      <span>Mã khách hàng</span>
                      <strong>{customer.id}</strong>
                      <span>Điện thoại</span>
                      <strong>{customer.phone}</strong>
                      <span>Địa chỉ</span>
                      <strong>{customer.address}</strong>
                    </div>
                  </div>
                  <div className="panel span-2">
                    <div className="panel-heading">
                      <h3>Chỉ số kết nối</h3>
                      <span className="muted-label">Cập nhật: Vừa xong</span>
                    </div>
                    <div className="metric-row">
                      <div>
                        <small>Download</small>
                        <strong>
                          {selected.speed} <sub>Mbps</sub>
                        </strong>
                      </div>
                      <div>
                        <small>Upload</small>
                        <strong>
                          {Math.round(selected.speed * 0.36)} <sub>Mbps</sub>
                        </strong>
                      </div>
                      <div>
                        <small>Độ trễ</small>
                        <strong>
                          {selected.ping || "—"} <sub>ms</sub>
                        </strong>
                      </div>
                      <div>
                        <small>Packet loss</small>
                        <strong>
                          {selected.status === "ONLINE" ? "0.1" : "2.4"} <sub>%</sub>
                        </strong>
                      </div>
                    </div>
                  </div>
                  <div className="panel">
                    <div className="panel-heading">
                      <h3>Hoạt động gần đây</h3>
                    </div>
                    <Timeline />
                  </div>
                </div>
              )}
              {detailTab === "Internet" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="KẾT NỐI WAN" title="Thông tin Internet" />
                  <div className="kv wide-kv">
                    {[
                      [
                        "WAN IP",
                        selected.status === "OFFLINE"
                          ? "—"
                          : `113.161.24.${Number(selected.id.slice(-3)) + 12}`,
                      ],
                      ["Trạng thái kết nối", selected.wan],
                      ["VLAN", "35"],
                      ["NAT", "Đang bật"],
                      ["RX / TX", "1.2 GB / 428 MB"],
                      ["Uptime", selected.uptime],
                      ["Latency", `${selected.ping} ms`],
                    ].map(([k, v]) => (
                      <>
                        <span key={k}>{k}</span>
                        <strong key={`${k}-v`}>{v}</strong>
                      </>
                    ))}
                  </div>
                </div>
              )}
              {detailTab === "Wi-Fi" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="MẠNG KHÔNG DÂY" title="Cấu hình Wi-Fi" />
                  <div className="data-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Băng tần</th>
                          <th>SSID</th>
                          <th>Kênh</th>
                          <th>Tín hiệu</th>
                          <th>Thiết bị kết nối</th>
                          <th>Trạng thái</th>
                        </tr>
                      </thead>
                      <tbody>
                        {["2.4GHz", "5GHz"].map((band, i) => (
                          <tr key={band}>
                            <td>{band}</td>
                            <td>
                              ONT_Home_{selected.id.slice(-3)}
                              {i ? "_5G" : ""}
                            </td>
                            <td>{i ? "36" : "6"}</td>
                            <td>{i ? "-52" : "-61"} dBm</td>
                            <td>
                              {
                                lanDevices.filter(
                                  (d) =>
                                    d.ontId === selected.id &&
                                    d.online &&
                                    d.connection.includes("Wi-Fi"),
                                ).length
                              }
                            </td>
                            <td>
                              <Status value={selected.status} />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              {detailTab === "LAN" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="CỔNG KẾT NỐI" title="Mạng LAN" />
                  <div className="data-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Cổng</th>
                          <th>Liên kết</th>
                          <th>Tốc độ</th>
                          <th>Thiết bị</th>
                          <th>Lưu lượng</th>
                        </tr>
                      </thead>
                      <tbody>
                        {[1, 2, 3, 4].map((i) => (
                          <tr key={i}>
                            <td className="strong-cell">LAN{i}</td>
                            <td>
                              <Status
                                value={
                                  i < 3 && selected.status !== "OFFLINE" ? "ONLINE" : "OFFLINE"
                                }
                                label={i < 3 && selected.status !== "OFFLINE" ? "Kết nối" : "Ngắt"}
                              />
                            </td>
                            <td>{i < 3 ? "1000 Mbps" : "—"}</td>
                            <td>{i === 1 ? "Smart TV" : i === 2 ? "Máy tính" : "—"}</td>
                            <td>{i < 3 ? `${24 + i * 11} MB` : "—"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              {detailTab === "Optical / PON" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="TÍN HIỆU QUANG" title="Optical / PON" />
                  <div className="metric-row optical-metrics">
                    <div>
                      <small>RX power</small>
                      <strong>
                        {selected.optical} <sub>dBm</sub>
                      </strong>
                    </div>
                    <div>
                      <small>TX power</small>
                      <strong>
                        2.3 <sub>dBm</sub>
                      </strong>
                    </div>
                    <div>
                      <small>OLT</small>
                      <strong className="text-base!">OLT-HCM-01</strong>
                    </div>
                    <div>
                      <small>PON status</small>
                      <Status value={selected.status} />
                    </div>
                  </div>
                  <p className="note-line">
                    Cảnh báo tín hiệu quang:{" "}
                    {selected.status === "WARNING"
                      ? "Tín hiệu yếu, cần kiểm tra đường truyền."
                      : selected.status === "OFFLINE"
                        ? "Mất tín hiệu."
                        : "Không có cảnh báo."}
                  </p>
                </div>
              )}
              {detailTab === "Devices" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="LAN GUARD" title="Thiết bị đang kết nối" />
                  <DeviceTable devices={lanDevices.filter((d) => d.ontId === selected.id)} />
                </div>
              )}
              {detailTab === "Tests" && (
                <div className="panel detail-panel">
                  <SectionHead
                    eyebrow="CHẨN ĐOÁN"
                    title="Kiểm tra kết nối"
                    action={
                      <Button
                        onClick={() =>
                          notify(
                            `Đã chạy kiểm tra ${selected.id}: ${selected.speed} Mbps, ping ${selected.ping} ms`,
                          )
                        }
                      >
                        <Zap /> Chạy kiểm tra
                      </Button>
                    }
                  />
                  <div className="metric-row optical-metrics">
                    <div>
                      <small>Download</small>
                      <strong>
                        {selected.speed} <sub>Mbps</sub>
                      </strong>
                    </div>
                    <div>
                      <small>Upload</small>
                      <strong>
                        {Math.round(selected.speed * 0.36)} <sub>Mbps</sub>
                      </strong>
                    </div>
                    <div>
                      <small>Ping</small>
                      <strong>
                        {selected.ping} <sub>ms</sub>
                      </strong>
                    </div>
                    <div>
                      <small>Packet loss</small>
                      <strong>
                        0.1 <sub>%</sub>
                      </strong>
                    </div>
                  </div>
                  <div className="test-types">
                    Speedtest <span>·</span> iPerf <span>·</span> Ping <span>·</span> Packet loss
                  </div>
                </div>
              )}
              {detailTab === "Events" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="NHẬT KÝ HỆ THỐNG" title="Lịch sử sự kiện" />
                  <Timeline />
                </div>
              )}
              {detailTab === "Remote Actions" && (
                <div className="panel detail-panel">
                  <SectionHead eyebrow="THAO TÁC TỪ XA" title="Điều khiển ONT" />
                  <div className="action-list">
                    {[
                      ["Làm mới trạng thái", "Đồng bộ tình trạng thiết bị mới nhất", false],
                      ["Chạy Speed Test", "Kiểm tra tốc độ kết nối hiện tại", false],
                      ["Chạy chẩn đoán", "Kiểm tra các chỉ số WAN, Wi-Fi và PON", false],
                      ["Cấu hình Wi-Fi", "Thay đổi cài đặt mạng không dây", true],
                      ["Khởi động lại ONT", "Thiết bị sẽ tạm thời mất kết nối", true],
                    ].map(([name, desc, danger]) => (
                      <div key={String(name)}>
                        <div>
                          <strong>{name}</strong>
                          <small>{desc}</small>
                        </div>
                        <Button
                          variant="outline"
                          onClick={() =>
                            danger ? setConfirm(String(name)) : notify(`Đã thực hiện: ${name}`)
                          }
                        >
                          {name}
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <>
              <div className="page-heading">
                <div>
                  <div className="eyebrow">
                    ONT PLATFORM <span className="eyebrow-divider">/</span> VẬN HÀNH MẠNG
                  </div>
                  <h1>{section}</h1>
                  <p>
                    {section === "Tổng quan"
                      ? "Theo dõi hiệu suất mạng và tình trạng thiết bị theo thời gian thực."
                      : subtitles[section]}
                  </p>
                </div>
                <div className="page-heading-actions">
                  <span className="updated">
                    <span /> Cập nhật vừa xong
                  </span>
                  <Button variant="outline" onClick={() => notify("Dữ liệu đã được làm mới")}>
                    <RefreshCw /> Làm mới
                  </Button>
                </div>
              </div>
              {section === "Tổng quan" && (
                <>
                  <div className="stats-grid">
                    <Stat
                      icon={HardDrive}
                      label="Tổng số ONT"
                      value="100"
                      note="Thiết bị được quản lý"
                      kind="neutral"
                    />
                    <Stat
                      icon={Signal}
                      label="Đang online"
                      value="80"
                      suffix="/ 100"
                      note="80% tổng thiết bị"
                      kind="good"
                    />
                    <Stat
                      icon={Activity}
                      label="Cảnh báo"
                      value="12"
                      note="Cần theo dõi"
                      kind="warn"
                    />
                    <Stat
                      icon={Radio}
                      label="Ngoại tuyến"
                      value="08"
                      note="Cần can thiệp"
                      kind="bad"
                    />
                  </div>
                  <div className="overview-grid">
                    <div className="panel trend-panel">
                      <div className="panel-heading">
                        <div>
                          <h3>Tình trạng hệ thống</h3>
                          <p>Hiệu suất kết nối trong 24 giờ qua</p>
                        </div>
                        <span className="period">
                          24 giờ qua <ChevronDown size={14} />
                        </span>
                      </div>
                      <div className="trend-chart">
                        <div className="chart-guide">
                          <span>100%</span>
                          <span>75%</span>
                          <span>50%</span>
                          <span>25%</span>
                          <span>0%</span>
                        </div>
                        <div className="chart-inner">
                          <div className="chart-lines">
                            <i />
                            <i />
                            <i />
                            <i />
                            <i />
                          </div>
                          <div className="bars">
                            {speedBars.map((v, i) => (
                              <span key={i} style={{ height: `${v}%` }} title={`${v}%`} />
                            ))}
                          </div>
                          <div className="chart-times">
                            <span>00:00</span>
                            <span>04:00</span>
                            <span>08:00</span>
                            <span>12:00</span>
                            <span>16:00</span>
                            <span>20:00</span>
                            <span>23:59</span>
                          </div>
                        </div>
                      </div>
                      <div className="chart-legend">
                        <span>
                          <i className="legend-good" /> ONT Online
                        </span>
                        <span>
                          <i className="legend-warn" /> Cảnh báo
                        </span>
                        <span>
                          <i className="legend-bad" /> Ngoại tuyến
                        </span>
                      </div>
                    </div>
                    <div className="panel alert-panel">
                      <div className="panel-heading">
                        <div>
                          <h3>Cần chú ý</h3>
                          <p>Các vấn đề cần xử lý</p>
                        </div>
                        <span className="alert-count">
                          {tickets.filter((t) => t.status === "OPEN").length + 8}
                        </span>
                      </div>
                      <div className="alert-list">
                        <div>
                          <span className="alert-icon bad-bg">
                            <Radio size={18} />
                          </span>
                          <div>
                            <strong>8 ONT mất kết nối</strong>
                            <small>Cần kiểm tra kết nối & nguồn điện</small>
                          </div>
                          <ArrowRight size={16} />
                        </div>
                        <div>
                          <span className="alert-icon warn-bg">
                            <Activity size={18} />
                          </span>
                          <div>
                            <strong>12 tín hiệu quang yếu</strong>
                            <small>Chỉ số PON ngoài ngưỡng an toàn</small>
                          </div>
                          <ArrowRight size={16} />
                        </div>
                        <div>
                          <span className="alert-icon info-bg">
                            <ClipboardList size={18} />
                          </span>
                          <div>
                            <strong>
                              {tickets.filter((t) => t.status === "OPEN").length} sự cố chưa phân
                              công
                            </strong>
                            <small>Đang chờ kỹ thuật viên tiếp nhận</small>
                          </div>
                          <ArrowRight size={16} />
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        className="panel-bottom-link"
                        onClick={() => go("Ticket / Sự cố")}
                      >
                        Xem tất cả sự cố <ArrowRight size={16} />
                      </Button>
                    </div>
                  </div>
                  <div className="panel table-panel">
                    <div className="panel-heading">
                      <div>
                        <h3>Thiết bị cần theo dõi</h3>
                        <p>ONT có cảnh báo hoặc mất kết nối gần đây</p>
                      </div>
                      <Button variant="ghost" onClick={() => go("ONT")}>
                        Xem tất cả <ArrowRight />
                      </Button>
                    </div>
                    <OntTable items={onts.slice(80, 86)} onOpen={openOnt} compact />
                  </div>
                  <div className="lower-grid">
                    <div className="panel">
                      <div className="panel-heading">
                        <div>
                          <h3>Sự cố gần đây</h3>
                          <p>Cập nhật từ toàn hệ thống</p>
                        </div>
                        <Button variant="ghost" onClick={() => go("Ticket / Sự cố")}>
                          Xem tất cả <ArrowRight />
                        </Button>
                      </div>
                      <div className="ticket-mini-list">
                        {tickets.slice(0, 4).map((t) => (
                          <div key={t.id}>
                            <span className="ticket-mini-icon">
                              <ClipboardList size={16} />
                            </span>
                            <div>
                              <strong>{t.issue}</strong>
                              <small>
                                {customerFor(t.customerId)?.name} · {t.id}
                              </small>
                            </div>
                            <Status value={t.status} />
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="panel">
                      <div className="panel-heading">
                        <div>
                          <h3>Hiệu suất vận hành</h3>
                          <p>Tổng hợp hôm nay</p>
                        </div>
                        <ArrowUpRight size={17} className="text-muted-foreground" />
                      </div>
                      <div className="performance-list">
                        <div>
                          <span>Tỷ lệ online</span>
                          <strong>80%</strong>
                          <div className="progress-track">
                            <i style={{ width: "80%" }} />
                          </div>
                        </div>
                        <div>
                          <span>Ticket đã xử lý</span>
                          <strong>
                            {
                              tickets.filter((t) => ["RESOLVED", "CLOSED"].includes(t.status))
                                .length
                            }{" "}
                            / {tickets.length}
                          </strong>
                          <div className="progress-track">
                            <i style={{ width: "40%" }} />
                          </div>
                        </div>
                        <div>
                          <span>Thời gian xử lý TB</span>
                          <strong>2.4 giờ</strong>
                          <div className="progress-track">
                            <i style={{ width: "62%" }} />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}
              {(section === "ONT" || section === "Khách hàng") && (
                <div className="panel table-panel">
                  <div className="panel-heading">
                    <div>
                      <h3>{section === "ONT" ? "Danh sách thiết bị" : "Danh sách khách hàng"}</h3>
                      <p>{visibleOnts.length} kết quả trong hệ thống</p>
                    </div>
                  </div>
                  <div className="table-toolbar">
                    <div className="search-box">
                      <Search size={17} />
                      <Input
                        placeholder={
                          section === "ONT"
                            ? "Tìm theo ONT ID, serial, khách hàng..."
                            : "Tìm khách hàng, mã, thiết bị..."
                        }
                        value={search}
                        onChange={(e) => {
                          setSearch(e.target.value);
                          setPage(1);
                        }}
                      />
                    </div>
                    <select
                      aria-label="Lọc trạng thái"
                      value={filter}
                      onChange={(e) => {
                        setFilter(e.target.value);
                        setPage(1);
                      }}
                    >
                      <option value="Tất cả">Tất cả trạng thái</option>
                      <option value="ONLINE">Online</option>
                      <option value="WARNING">Cảnh báo</option>
                      <option value="OFFLINE">Offline</option>
                    </select>
                  </div>
                  {section === "ONT" ? (
                    <OntTable items={tableOnts} onOpen={openOnt} />
                  ) : (
                    <div className="data-table">
                      <table>
                        <thead>
                          <tr>
                            <th>Mã KH</th>
                            <th>Khách hàng</th>
                            <th>Số điện thoại</th>
                            <th>Địa chỉ</th>
                            <th>ONT</th>
                            <th>Internet</th>
                            <th>Thiết bị</th>
                            <th>Last Seen</th>
                          </tr>
                        </thead>
                        <tbody>
                          {tableOnts.map((o) => {
                            const c = customerFor(o.customerId);
                            return (
                              <tr key={o.id} onClick={() => openOnt(o.id)} className="click-row">
                                <td className="mono">{c?.id}</td>
                                <td className="strong-cell">{c?.name}</td>
                                <td>{c?.phone}</td>
                                <td className="address-cell">{c?.address}</td>
                                <td className="mono">{o.id}</td>
                                <td>
                                  <Status value={o.status} />
                                </td>
                                <td>{o.wan}</td>
                                <td>{o.lastSeen}</td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  )}
                  {!visibleOnts.length && <Empty />}
                  <Pagination page={page} total={visibleOnts.length} setPage={setPage} />
                </div>
              )}
              {section === "Ticket / Sự cố" && (
                <div className="panel table-panel">
                  <div className="panel-heading">
                    <div>
                      <h3>Danh sách sự cố</h3>
                      <p>{tickets.length} ticket đang được theo dõi</p>
                    </div>
                  </div>
                  <div className="table-toolbar">
                    <div className="search-box">
                      <Search size={17} />
                      <Input
                        placeholder="Tìm ticket, khách hàng, vấn đề..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                      />
                    </div>
                    <select
                      aria-label="Lọc trạng thái"
                      value={filter}
                      onChange={(e) => setFilter(e.target.value)}
                    >
                      <option value="Tất cả">Tất cả trạng thái</option>
                      {(
                        [
                          "OPEN",
                          "ASSIGNED",
                          "IN_PROGRESS",
                          "WAITING_CUSTOMER",
                          "RESOLVED",
                          "CLOSED",
                        ] as TicketStatus[]
                      ).map((s) => (
                        <option value={s} key={s}>
                          {statusLabels[s]}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="data-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Ticket ID</th>
                          <th>Khách hàng</th>
                          <th>ONT</th>
                          <th>Sự cố</th>
                          <th>Ưu tiên</th>
                          <th>Trạng thái</th>
                          <th>Kỹ thuật viên</th>
                          <th>Tạo lúc</th>
                          <th>Thao tác</th>
                        </tr>
                      </thead>
                      <tbody>
                        {tickets
                          .filter(
                            (t) =>
                              (filter === "Tất cả" || t.status === filter) &&
                              `${t.id} ${t.issue} ${customerFor(t.customerId)?.name}`
                                .toLocaleLowerCase("vi")
                                .includes(q),
                          )
                          .map((t) => (
                            <tr key={t.id}>
                              <td className="mono strong-cell">
                                <Link to="/" search={{ ticket: t.id }} className="table-link">
                                  {t.id}
                                </Link>
                              </td>
                              <td>{customerFor(t.customerId)?.name}</td>
                              <td>
                                <Button
                                  variant="link"
                                  className="table-link"
                                  onClick={() => openOnt(t.ontId)}
                                >
                                  {t.ontId}
                                </Button>
                              </td>
                              <td>{t.issue}</td>
                              <td>
                                <span
                                  className={`priority ${t.priority === "Cao" ? "priority-high" : ""}`}
                                >
                                  {t.priority}
                                </span>
                              </td>
                              <td>
                                <Status value={t.status} />
                              </td>
                              <td>{techFor(t.technicianId)?.name ?? "Chưa phân công"}</td>
                              <td>{t.created}</td>
                              <td>
                                {t.status === "OPEN" ? (
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => {
                                      updateTicket(t.id, {
                                        status: "ASSIGNED",
                                        technicianId: technicians[0]?.id ?? "KT-001",
                                      });
                                      notify(
                                        `Đã phân công ${t.id} cho ${technicians[0]?.name ?? "Kỹ thuật viên"}`,
                                      );
                                    }}
                                  >
                                    Phân công
                                  </Button>
                                ) : (
                                  <span className="muted-label">{t.updated}</span>
                                )}
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              {section === "Health Monitor" && (
                <>
                  <div className="stats-grid">
                    <Stat
                      icon={Activity}
                      label="Internet"
                      value="80%"
                      note="Kết nối ổn định"
                      kind="good"
                    />
                    <Stat
                      icon={Wifi}
                      label="Wi-Fi"
                      value="94%"
                      note="Hoạt động bình thường"
                      kind="good"
                    />
                    <Stat
                      icon={Signal}
                      label="Optical / PON"
                      value="12"
                      note="Tín hiệu cần chú ý"
                      kind="warn"
                    />
                    <Stat
                      icon={Gauge}
                      label="Độ trễ trung bình"
                      value="16"
                      suffix="ms"
                      note="Trong ngưỡng an toàn"
                      kind="neutral"
                    />
                  </div>
                  <div className="panel detail-panel">
                    <SectionHead eyebrow="GIÁM SÁT SỨC KHỎE" title="Chỉ số thiết bị" />
                    <div className="monitor-grid">
                      {[
                        ["WAN", "80 / 100", "Kết nối"],
                        ["LAN", "96 / 100", "Cổng hoạt động"],
                        ["Wi-Fi", "94 / 100", "Băng tần"],
                        ["CPU", "28%", "Sử dụng trung bình"],
                        ["Memory", "42%", "Sử dụng trung bình"],
                        ["Temperature", "41°C", "Nhiệt độ trung bình"],
                        ["Packet loss", "0.1%", "Trung bình"],
                        ["Latency", "16 ms", "Trung bình"],
                        ["iPerf", "732 Mbps", "Thông lượng"],
                        ["TR-069", "98 / 100", "Thiết bị kết nối"],
                      ].map(([k, v, n]) => (
                        <div key={k}>
                          <small>{k}</small>
                          <strong>{v}</strong>
                          <span>{n}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="panel detail-panel">
                    <SectionHead eyebrow="LỊCH SỬ" title="Dòng thời gian" />
                    <Timeline />
                  </div>
                </>
              )}
              {section === "Speed Test" && (
                <>
                  <div className="stats-grid">
                    <Stat
                      icon={Download}
                      label="Download TB"
                      value="125"
                      suffix="Mbps"
                      note="Tăng 8% tuần này"
                      kind="good"
                    />
                    <Stat
                      icon={ArrowUpRight}
                      label="Upload TB"
                      value="45"
                      suffix="Mbps"
                      note="Ổn định"
                      kind="neutral"
                    />
                    <Stat
                      icon={Gauge}
                      label="Ping TB"
                      value="12"
                      suffix="ms"
                      note="Độ trễ thấp"
                      kind="neutral"
                    />
                    <Stat
                      icon={Activity}
                      label="Packet loss"
                      value="0.1"
                      suffix="%"
                      note="Trong ngưỡng an toàn"
                      kind="good"
                    />
                  </div>
                  <div className="panel trend-panel">
                    <div className="panel-heading">
                      <div>
                        <h3>Lịch sử kiểm tra tốc độ</h3>
                        <p>Download / Upload theo thời gian</p>
                      </div>
                      <span className="period">
                        7 ngày qua <ChevronDown size={14} />
                      </span>
                    </div>
                    <div className="speed-chart">
                      {[62, 76, 68, 82, 73, 91, 85, 69, 80, 87, 76, 92, 81, 88].map((v, i) => (
                        <div key={i}>
                          <span style={{ height: `${v}%` }} />
                          <i style={{ height: `${v * 0.37}%` }} />
                        </div>
                      ))}
                    </div>
                    <div className="chart-legend">
                      <span>
                        <i className="legend-good" /> Download
                      </span>
                      <span>
                        <i className="legend-info" /> Upload
                      </span>
                    </div>
                  </div>
                  <div className="panel table-panel">
                    <div className="panel-heading">
                      <h3>Các lần kiểm tra gần đây</h3>
                    </div>
                    <div className="data-table">
                      <table>
                        <thead>
                          <tr>
                            <th>ONT</th>
                            <th>Khách hàng</th>
                            <th>Download</th>
                            <th>Upload</th>
                            <th>Ping</th>
                            <th>Jitter</th>
                            <th>Packet loss</th>
                            <th>Thời điểm</th>
                          </tr>
                        </thead>
                        <tbody>
                          {onts.slice(0, 10).map((o, i) => (
                            <tr key={o.id} className="click-row" onClick={() => openOnt(o.id)}>
                              <td className="mono">{o.id}</td>
                              <td>{customerFor(o.customerId)?.name}</td>
                              <td>{o.speed} Mbps</td>
                              <td>{Math.round(o.speed * 0.36)} Mbps</td>
                              <td>{o.ping} ms</td>
                              <td>{3 + (i % 4)} ms</td>
                              <td>0.{i % 4}%</td>
                              <td>{i + 1} phút trước</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </>
              )}
              {section === "LAN Guard" && (
                <div className="panel table-panel">
                  <div className="panel-heading">
                    <div>
                      <h3>Thiết bị trong mạng LAN</h3>
                      <p>{lanDevices.length} thiết bị từ 100 mạng khách hàng</p>
                    </div>
                  </div>
                  <div className="table-toolbar">
                    <div className="search-box">
                      <Search size={17} />
                      <Input
                        placeholder="Tìm thiết bị, IP, MAC, ONT..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                      />
                    </div>
                  </div>
                  <DeviceTable
                    devices={lanDevices
                      .filter((d) =>
                        `${d.name} ${d.ip} ${d.mac} ${d.ontId}`.toLowerCase().includes(q),
                      )
                      .slice(0, 30)}
                  />
                </div>
              )}
              {section === "Kỹ thuật viên" && (
                <div className="panel table-panel">
                  <div className="panel-heading">
                    <div>
                      <h3>Đội ngũ kỹ thuật</h3>
                      <p>{technicians.length} kỹ thuật viên trong hệ thống</p>
                    </div>
                  </div>
                  <div className="data-table">
                    <table>
                      <thead>
                        <tr>
                          <th>Mã thợ</th>
                          <th>Kỹ thuật viên</th>
                          <th>Khu vực</th>
                          <th>Trạng thái</th>
                          <th>Công việc đang xử lý</th>
                          <th>Số ticket</th>
                          <th>Last Active</th>
                        </tr>
                      </thead>
                      <tbody>
                        {technicians.map((t) => (
                          <tr key={t.id}>
                            <td className="mono">{t.id}</td>
                            <td className="strong-cell">{t.name}</td>
                            <td>{t.area}</td>
                            <td>
                              <Status
                                value={t.status}
                                label={
                                  t.status === "AVAILABLE"
                                    ? "Sẵn sàng"
                                    : t.status === "BUSY"
                                      ? "Đang bận"
                                      : "Offline"
                                }
                              />
                            </td>
                            <td>
                              {tickets.find(
                                (tk) => tk.technicianId === t.id && tk.status === "IN_PROGRESS",
                              )?.issue ?? "—"}
                            </td>
                            <td>{tickets.filter((tk) => tk.technicianId === t.id).length}</td>
                            <td>{t.lastActive}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
              {section === "Báo cáo" && (
                <>
                  <div className="stats-grid">
                    <Stat
                      icon={HardDrive}
                      label="Tổng ONT"
                      value="100"
                      note="Thiết bị quản lý"
                      kind="neutral"
                    />
                    <Stat
                      icon={Signal}
                      label="Online rate"
                      value="80%"
                      note="80 thiết bị"
                      kind="good"
                    />
                    <Stat
                      icon={Radio}
                      label="Offline rate"
                      value="8%"
                      note="8 thiết bị"
                      kind="bad"
                    />
                    <Stat
                      icon={ClipboardList}
                      label="Sự cố"
                      value={String(tickets.length)}
                      note="Tổng ticket"
                      kind="warn"
                    />
                  </div>
                  <div className="lower-grid">
                    <div className="panel detail-panel">
                      <SectionHead eyebrow="HIỆU SUẤT" title="Chỉ số vận hành" />
                      <div className="report-list">
                        {[
                          ["MTTR", "2.4 giờ"],
                          ["Speed test TB", "125 Mbps"],
                          ["Vấn đề Wi-Fi", "8"],
                          ["Vấn đề LAN", "4"],
                        ].map(([k, v]) => (
                          <div key={k}>
                            <span>{k}</span>
                            <strong>{v}</strong>
                          </div>
                        ))}
                      </div>
                    </div>
                    <div className="panel detail-panel">
                      <SectionHead eyebrow="THEO KHU VỰC" title="Ticket theo khu vực" />
                      <div className="report-list">
                        {areas.map((a, i) => (
                          <div key={a}>
                            <span>{a}</span>
                            <strong>
                              {tickets.filter((t) => customerFor(t.customerId)?.address.includes(a))
                                .length + i}
                            </strong>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </main>
      </div>
      {confirm && (
        <div className="modal-backdrop" onClick={() => setConfirm(null)}>
          <div
            className="confirm-modal"
            role="dialog"
            aria-modal="true"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="modal-icon">
              <Wrench size={22} />
            </div>
            <h3>Xác nhận {confirm.toLowerCase()}?</h3>
            <p>
              Thao tác này có thể tạm thời ảnh hưởng đến kết nối Internet của khách hàng. Bạn có
              chắc muốn tiếp tục?
            </p>
            <div>
              <Button variant="outline" onClick={() => setConfirm(null)}>
                Hủy
              </Button>
              <Button
                onClick={() => {
                  notify(`Đã gửi lệnh ${confirm} cho ${selected?.id}`);
                  setConfirm(null);
                }}
              >
                Xác nhận
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
const subtitles: Record<Section, string> = {
  "Tổng quan": "",
  "Khách hàng": "Quản lý thông tin khách hàng và kết nối Internet.",
  ONT: "Theo dõi toàn bộ thiết bị ONT trong hệ thống.",
  "Health Monitor": "Quan sát sức khỏe mạng và chỉ số thiết bị.",
  "Speed Test": "Theo dõi tốc độ và chất lượng đường truyền.",
  "LAN Guard": "Giám sát thiết bị kết nối trong mạng khách hàng.",
  "Ticket / Sự cố": "Tiếp nhận và xử lý các yêu cầu hỗ trợ.",
  "Kỹ thuật viên": "Quản lý đội ngũ kỹ thuật hiện trường.",
  "Báo cáo": "Tổng hợp hiệu suất và tình trạng vận hành.",
};
function TicketDetail({ ticket: t, back }: { ticket: Ticket; back: () => void }) {
  const c = customerFor(t.customerId);
  const tech = t.technicianId ? techFor(t.technicianId) : undefined;
  return (
    <>
      <Button variant="ghost" className="back-link" onClick={back}>
        <ChevronLeft size={17} /> Quay lại Ticket / Sự cố
      </Button>
      <div className="detail-heading">
        <div>
          <div className="eyebrow">TICKET / {t.id}</div>
          <h1>{t.issue}</h1>
          <p>
            {c?.name} <span>·</span> {t.ontId} <span>·</span> Ưu tiên {t.priority}
          </p>
        </div>
        <div className="detail-actions">
          <Status value={t.status} />
        </div>
      </div>
      <div className="detail-grid">
        <div className="panel span-2">
          <SectionHead eyebrow="THÔNG TIN XỬ LÝ" title="Báo cáo kỹ thuật" />
          <div className="kv wide-kv">
            {[
              ["Khách hàng", c?.name ?? "—"],
              ["Địa chỉ", c?.address ?? "—"],
              ["Kỹ thuật viên", tech?.name ?? "Chưa phân công"],
              ["Tạo lúc", t.created],
              ["Cập nhật", t.updated],
              ["Chẩn đoán", t.diagnosis ?? "—"],
              ["Biện pháp", t.action ?? "—"],
              ["Kết quả kiểm tra", t.testResult ?? "—"],
              ["Khách xác nhận", t.confirmed ? "Đã xác nhận" : "Chưa"],
            ].map(([k, v]) => (
              <>
                <span key={k}>{k}</span>
                <strong key={`${k}-v`}>{v}</strong>
              </>
            ))}
          </div>
        </div>
        <div className="panel">
          <SectionHead eyebrow="MỞ NHANH" title="Liên kết" />
          <div className="app-switch deep-links">
            <Link to="/" search={{ ont: t.ontId }}>
              <HardDrive size={16} /> Chi tiết {t.ontId} <ArrowUpRight size={13} />
            </Link>
            <Link to="/technician" search={{ ticket: t.id }}>
              <Wrench size={16} /> Mở trong App Thợ <ArrowUpRight size={13} />
            </Link>
            {t.customerId === customers[0]?.id && (
              <Link to="/customer" search={{ ticket: t.id }}>
                <Users size={16} /> Mở trong App Khách <ArrowUpRight size={13} />
              </Link>
            )}
          </div>
        </div>
      </div>
    </>
  );
}
function Stat({
  icon: Icon,
  label,
  value,
  suffix,
  note,
  kind,
}: {
  icon: typeof Activity;
  label: string;
  value: string;
  suffix?: string;
  note: string;
  kind: string;
}) {
  return (
    <div className="stat">
      <div className="stat-top">
        <span>{label}</span>
        <span className={`stat-icon stat-${kind}`}>
          <Icon size={18} />
        </span>
      </div>
      <div className="stat-value">
        {value} {suffix && <small>{suffix}</small>}
      </div>
      <div className="stat-note">
        {kind === "good" ? (
          <ArrowUpRight size={14} />
        ) : kind === "bad" ? (
          <ArrowDownRight size={14} />
        ) : (
          <span className="note-dot" />
        )}
        {note}
      </div>
    </div>
  );
}
function OntTable({
  items,
  onOpen,
  compact = false,
}: {
  items: typeof onts;
  onOpen: (id: string) => void;
  compact?: boolean;
}) {
  return (
    <div className="data-table">
      <table>
        <thead>
          <tr>
            <th>ONT ID</th>
            <th>Khách hàng</th>
            <th>Model / Serial</th>
            {!compact && (
              <>
                <th>Firmware</th>
                <th>WAN</th>
                <th>LAN</th>
                <th>Wi-Fi</th>
              </>
            )}
            <th>Optical</th>
            <th>Uptime</th>
            <th>Last Seen</th>
            <th>Trạng thái</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {items.map((o) => (
            <tr key={o.id} onClick={() => onOpen(o.id)} className="click-row">
              <td className="mono strong-cell">{o.id}</td>
              <td>{customerFor(o.customerId)?.name}</td>
              <td>
                <span className="table-stack">
                  <strong>{o.model}</strong>
                  <small>{o.serial}</small>
                </span>
              </td>
              {!compact && (
                <>
                  <td>{o.firmware}</td>
                  <td>{o.wan}</td>
                  <td>{o.status === "OFFLINE" ? "—" : "2/4"}</td>
                  <td>{o.wifi}</td>
                </>
              )}
              <td className={o.optical < -26 ? "text-warning" : ""}>{o.optical} dBm</td>
              <td>{o.uptime}</td>
              <td>{o.lastSeen}</td>
              <td>
                <Status value={o.status} />
              </td>
              <td>
                <ChevronRight size={16} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
function DeviceTable({ devices }: { devices: typeof lanDevices }) {
  return (
    <div className="data-table">
      <table>
        <thead>
          <tr>
            <th>Thiết bị</th>
            <th>ONT</th>
            <th>IP</th>
            <th>MAC</th>
            <th>Kết nối</th>
            <th>Trạng thái</th>
            <th>Last Seen</th>
          </tr>
        </thead>
        <tbody>
          {devices.map((d) => (
            <tr key={d.id}>
              <td className="strong-cell">{d.name}</td>
              <td className="mono">{d.ontId}</td>
              <td className="mono">{d.ip}</td>
              <td className="mono">{d.mac}</td>
              <td>{d.connection}</td>
              <td>
                <Status value={d.online ? "ONLINE" : "OFFLINE"} />
              </td>
              <td>{d.lastSeen}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
function Pagination({
  page,
  total,
  setPage,
}: {
  page: number;
  total: number;
  setPage: (n: number) => void;
}) {
  const max = Math.max(1, Math.ceil(total / 10));
  return (
    <div className="pagination">
      <span>
        Hiển thị {total ? (page - 1) * 10 + 1 : 0}–{Math.min(page * 10, total)} / {total}
      </span>
      <div>
        <Button
          variant="outline"
          size="icon"
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
          aria-label="Trang trước"
        >
          <ChevronLeft />
        </Button>
        <span>
          {page} / {max}
        </span>
        <Button
          variant="outline"
          size="icon"
          disabled={page >= max}
          onClick={() => setPage(page + 1)}
          aria-label="Trang sau"
        >
          <ChevronRight />
        </Button>
      </div>
    </div>
  );
}
function Timeline() {
  return (
    <div className="timeline">
      {[
        ["09:12", "ONT Online", "Kết nối đã được khôi phục"],
        ["09:10", "WAN reconnect", "Thiết bị kết nối lại với mạng"],
        ["08:41", "Speed test", "Đã hoàn thành bài kiểm tra tốc độ"],
        ["08:35", "Thiết bị Wi-Fi kết nối", "Một thiết bị mới tham gia mạng"],
        ["08:32", "ONT Online", "Thiết bị đang hoạt động"],
      ].map(([time, title, desc]) => (
        <div key={time}>
          <span className="timeline-node" />
          <time>{time}</time>
          <div>
            <strong>{title}</strong>
            <small>{desc}</small>
          </div>
        </div>
      ))}
    </div>
  );
}
