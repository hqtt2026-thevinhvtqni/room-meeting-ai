import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { parseDeepLink } from "@/lib/deep-links";
import { useState } from "react";
import {
  Activity,
  ArrowLeft,
  ArrowRight,
  Bell,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  CircleUserRound,
  Gauge,
  HardDrive,
  Home,
  Laptop,
  MessageCircle,
  Monitor,
  Phone,
  Router,
  Search,
  Send,
  Smartphone,
  Wifi,
  Zap,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { usePlatform } from "@/components/platform-context";
import { customers, onts, lanDevices, statusLabels, techFor, type Ticket } from "@/lib/ont-data";
export const Route = createFileRoute("/customer")({
  head: () => ({
    meta: [
      { title: "App Khách | ONT Platform" },
      { name: "description", content: "Kiểm tra Internet, Wi-Fi, thiết bị và gửi yêu cầu hỗ trợ." },
      { property: "og:title", content: "App Khách — ONT Platform" },
      { property: "og:description", content: "Theo dõi kết nối và nhận hỗ trợ Internet dễ dàng." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  validateSearch: parseDeepLink,
  component: CustomerApp,
});
const nav = [
  { name: "Trang chủ", icon: Home },
  { name: "Internet", icon: Wifi },
  { name: "Thiết bị", icon: HardDrive },
  { name: "Hỗ trợ", icon: CircleHelp },
  { name: "Cá nhân", icon: CircleUserRound },
];
const issues = [
  "Internet chậm",
  "Mất Internet",
  "Wi-Fi yếu",
  "Không kết nối được",
  "Thiết bị không vào mạng",
  "Khác",
];
const you = customers[0] ?? {
  id: "KH-001",
  name: "Nguyễn Minh An",
  phone: "",
  address: "",
  ontId: "ONT-001",
};
const device = onts[0] ?? {
  id: "ONT-001",
  serial: "",
  model: "",
  firmware: "",
  customerId: you.id,
  status: "UNKNOWN" as const,
  optical: 0,
  uptime: "",
  lastSeen: "",
  wan: "",
  wifi: "",
  speed: 0,
  ping: 0,
};
function CustomerApp() {
  const { tickets, createTicket, notify } = usePlatform();
  const [tab, setTab] = useState("Trang chủ");
  const [issue, setIssue] = useState("");
  const [diagnosed, setDiagnosed] = useState(false);
  const [test, setTest] = useState(false);
  const [chat, setChat] = useState(false);
  const [chatText, setChatText] = useState("");
  const [chatMessages, setChatMessages] = useState<string[]>([]);
  const myTickets = tickets.filter((t) => t.customerId === you.id);
  const sp = Route.useSearch();
  const navigate = useNavigate({ from: "/customer" });
  const openTicket = sp.ticket ? myTickets.find((t) => t.id === sp.ticket) : undefined;
  const closeTicket = () => {
    navigate({ search: {} });
    setTab("Hỗ trợ");
  };
  const devices = lanDevices.filter((d) => d.ontId === device.id);
  const chooseIssue = (value: string) => {
    setIssue(value);
    setDiagnosed(false);
    setTab("Hỗ trợ");
  };
  const submit = () => {
    createTicket(you.id, device.id, issue);
    setIssue("");
    setDiagnosed(false);
  };
  return (
    <div className="mobile-app customer-app">
      <div className="mobile-top">
        <div className="mobile-logo">
          <span>
            <Activity size={19} />
          </span>
          ONT<span>Platform</span>
        </div>
        <div className="mobile-top-actions">
          <Link to="/" title="Bảng điều hành">
            <HardDrive size={18} />
          </Link>
          <Link to="/technician" title="App Thợ">
            <Router size={18} />
          </Link>
          <Button
            variant="ghost"
            size="icon"
            aria-label="Thông báo"
            onClick={() =>
              notify(
                myTickets.length
                  ? `${myTickets.length} yêu cầu hỗ trợ của bạn`
                  : "Chưa có thông báo mới",
              )
            }
          >
            <Bell size={20} />
          </Button>
          <span className="mobile-avatar customer-avatar">{you.name.slice(-2)}</span>
        </div>
      </div>
      <div className="mobile-body">
        {sp.ticket ? (
          openTicket ? (
            <>
              <Button variant="ghost" className="mobile-back" onClick={closeTicket}>
                <ArrowLeft size={17} /> Hỗ trợ
              </Button>
              <div className="mobile-page-title">
                <span>YÊU CẦU {openTicket.id}</span>
                <h1>{openTicket.issue}</h1>
                <p>
                  Tạo lúc {openTicket.created} · Cập nhật {openTicket.updated}
                </p>
              </div>
              <TicketRow ticket={openTicket} />
              {openTicket.diagnosis && (
                <div className="suggestion">
                  <div className="mini-section-title">KẾT QUẢ XỬ LÝ</div>
                  <strong>{openTicket.diagnosis}</strong>
                  <p>{openTicket.action}</p>
                  <p>{openTicket.testResult}</p>
                </div>
              )}
            </>
          ) : (
            <div className="not-found-block">
              <span className="mini-section-title">LIÊN KẾT KHÔNG HỢP LỆ</span>
              <h1>Không tìm thấy yêu cầu {sp.ticket}</h1>
              <p>Yêu cầu này không tồn tại hoặc không thuộc tài khoản của bạn.</p>
              <Button className="w-full" onClick={closeTicket}>
                <ArrowLeft size={17} /> Về trang Hỗ trợ
              </Button>
            </div>
          )
        ) : (
          <>
            {tab === "Trang chủ" && (
              <>
                <div className="mobile-greeting customer-greeting">
                  <span>CHÀO MỪNG TRỞ LẠI</span>
                  <h1>Internet của bạn.</h1>
                  <p>Xin chào {you.name}, mọi thứ đều ổn định.</p>
                </div>
                <div className="connection-block">
                  <div className="connection-top">
                    <div className="connection-icon">
                      <Wifi size={27} />
                    </div>
                    <span className="connection-live">
                      <i /> Đang hoạt động
                    </span>
                  </div>
                  <div className="connection-center">
                    <small>TRẠNG THÁI KẾT NỐI</small>
                    <h2>Đã kết nối</h2>
                    <p>Internet đang hoạt động tốt</p>
                  </div>
                  <div className="connection-stats">
                    <div>
                      <span>DOWNLOAD</span>
                      <strong>
                        125 <small>Mbps</small>
                      </strong>
                    </div>
                    <div>
                      <span>UPLOAD</span>
                      <strong>
                        45 <small>Mbps</small>
                      </strong>
                    </div>
                    <div>
                      <span>PING</span>
                      <strong>
                        12 <small>ms</small>
                      </strong>
                    </div>
                  </div>
                </div>
                <div className="mobile-section-heading">
                  <div>
                    <span>KIỂM TRA NHANH</span>
                    <h2>Bạn muốn làm gì?</h2>
                  </div>
                </div>
                <div className="quick-actions">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setTab("Internet");
                      setTest(true);
                      notify("Đã kiểm tra Internet: kết nối ổn định");
                    }}
                  >
                    <span>
                      <Gauge size={20} />
                    </span>
                    Kiểm tra Internet <ChevronRight size={16} />
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setTab("Internet");
                      notify("Wi-Fi 2.4GHz và 5GHz đang hoạt động");
                    }}
                  >
                    <span>
                      <Wifi size={20} />
                    </span>
                    Kiểm tra Wi-Fi <ChevronRight size={16} />
                  </Button>
                  <Button variant="outline" onClick={() => setTab("Hỗ trợ")}>
                    <span>
                      <CircleHelp size={20} />
                    </span>
                    Báo sự cố <ChevronRight size={16} />
                  </Button>
                </div>
                <div className="mobile-section-heading">
                  <div>
                    <span>MẠNG NHÀ BẠN</span>
                    <h2>Thiết bị đang kết nối</h2>
                  </div>
                  <Button variant="ghost" onClick={() => setTab("Thiết bị")}>
                    Xem tất cả <ArrowRight size={16} />
                  </Button>
                </div>
                <DeviceRows devices={devices} />
              </>
            )}
            {tab === "Internet" && (
              <>
                <div className="mobile-page-title">
                  <span>ĐƯỜNG TRUYỀN</span>
                  <h1>Internet</h1>
                  <p>Theo dõi chất lượng kết nối của bạn.</p>
                </div>
                <div className="internet-status">
                  <span>
                    <Wifi size={22} />
                  </span>
                  <div>
                    <strong>Đường truyền ổn định</strong>
                    <small>ONT và Wi-Fi đang hoạt động</small>
                  </div>
                  <CheckCircle2 size={19} />
                </div>
                <div className="internet-metrics">
                  <div>
                    <span>Download</span>
                    <strong>
                      {device.speed} <small>Mbps</small>
                    </strong>
                  </div>
                  <div>
                    <span>Upload</span>
                    <strong>
                      {Math.round(device.speed * 0.36)} <small>Mbps</small>
                    </strong>
                  </div>
                  <div>
                    <span>Ping</span>
                    <strong>
                      {device.ping} <small>ms</small>
                    </strong>
                  </div>
                </div>
                <div className="mobile-info-block">
                  <div className="mini-section-title">THÔNG TIN KẾT NỐI</div>
                  <div className="simple-kv">
                    <span>Internet</span>
                    <strong>Đang hoạt động</strong>
                    <span>ONT</span>
                    <strong>{statusLabels[device.status]}</strong>
                    <span>Wi-Fi</span>
                    <strong>Đang hoạt động</strong>
                    <span>Thời gian hoạt động</span>
                    <strong>{device.uptime}</strong>
                  </div>
                </div>
                <Button
                  className="w-full customer-main-button"
                  onClick={() => {
                    setTest(true);
                    notify("Kiểm tra hoàn tất: kết nối ổn định");
                  }}
                >
                  <Zap size={17} /> Kiểm tra Internet
                </Button>
                {test && (
                  <div className="test-result">
                    <CheckCircle2 size={20} />
                    <div>
                      <strong>Kết nối của bạn đang tốt</strong>
                      <p>
                        Download {device.speed} Mbps · Upload {Math.round(device.speed * 0.36)} Mbps
                        · Ping {device.ping} ms
                      </p>
                    </div>
                  </div>
                )}
                <div className="mobile-section-heading">
                  <div>
                    <span>LỊCH SỬ</span>
                    <h2>Lần kiểm tra gần đây</h2>
                  </div>
                </div>
                <div className="mobile-rows">
                  {[0, 1, 2].map((i) => (
                    <div key={i}>
                      <span className="row-icon">
                        <Gauge size={18} />
                      </span>
                      <div>
                        <strong>{125 - i * 7} Mbps download</strong>
                        <small>
                          {i === 0 ? "Hôm nay" : `${i + 1} ngày trước`} · Ping {12 + i * 2} ms
                        </small>
                      </div>
                      <CheckCircle2 size={17} className="text-success" />
                    </div>
                  ))}
                </div>
              </>
            )}
            {tab === "Thiết bị" && (
              <>
                <div className="mobile-page-title">
                  <span>MẠNG NHÀ BẠN</span>
                  <h1>Thiết bị</h1>
                  <p>{devices.filter((d) => d.online).length} thiết bị đang kết nối.</p>
                </div>
                <DeviceRows devices={devices} />
                <div className="mobile-info-block">
                  <div className="mini-section-title">THÔNG TIN BỘ PHÁT</div>
                  <div className="simple-kv">
                    <span>Model</span>
                    <strong>{device.model}</strong>
                    <span>Serial</span>
                    <strong>{device.serial}</strong>
                    <span>Wi-Fi</span>
                    <strong>2.4GHz / 5GHz</strong>
                  </div>
                </div>
              </>
            )}
            {tab === "Hỗ trợ" && (
              <>
                <div className="mobile-page-title">
                  <span>LUÔN SẴN SÀNG HỖ TRỢ</span>
                  <h1>Hỗ trợ</h1>
                  <p>Chọn vấn đề bạn đang gặp phải.</p>
                </div>
                {issue ? (
                  <>
                    <Button
                      variant="ghost"
                      className="mobile-back"
                      onClick={() => {
                        setIssue("");
                        setDiagnosed(false);
                      }}
                    >
                      <ArrowLeft size={17} /> Chọn vấn đề khác
                    </Button>
                    <div className="issue-heading">
                      <span className="row-icon">
                        <CircleHelp size={20} />
                      </span>
                      <div>
                        <small>VẤN ĐỀ BẠN GẶP</small>
                        <h2>{issue}</h2>
                      </div>
                    </div>
                    <div className="diagnosis-steps">
                      <div className="step-active">
                        <span>1</span>
                        <div>
                          <strong>Tự động kiểm tra</strong>
                          <small>Kiểm tra ONT, kết nối và Wi-Fi</small>
                        </div>
                        <CheckCircle2 size={17} />
                      </div>
                      <div className={diagnosed ? "step-active" : ""}>
                        <span>2</span>
                        <div>
                          <strong>Đề xuất xử lý</strong>
                          <small>Các bước đơn giản bạn có thể thử</small>
                        </div>
                      </div>
                      <div className={diagnosed ? "step-active" : ""}>
                        <span>3</span>
                        <div>
                          <strong>Gửi yêu cầu hỗ trợ</strong>
                          <small>Nếu vấn đề vẫn chưa được giải quyết</small>
                        </div>
                      </div>
                    </div>
                    {!diagnosed ? (
                      <Button
                        className="w-full customer-main-button"
                        onClick={() => setDiagnosed(true)}
                      >
                        <Search size={17} /> Bắt đầu kiểm tra
                      </Button>
                    ) : (
                      <>
                        <div className="suggestion">
                          <div className="mini-section-title">KẾT QUẢ KIỂM TRA</div>
                          <strong>Thiết bị đang kết nối bình thường</strong>
                          <p>
                            Hãy thử khởi động lại bộ phát Wi-Fi và kiểm tra vị trí đặt thiết bị. Nếu
                            vẫn gặp sự cố, gửi yêu cầu để đội kỹ thuật hỗ trợ.
                          </p>
                        </div>
                        <Button className="w-full customer-main-button" onClick={submit}>
                          Vẫn gặp sự cố — Gửi yêu cầu <ArrowRight size={17} />
                        </Button>
                      </>
                    )}
                  </>
                ) : (
                  <div className="issue-list">
                    {issues.map((s) => (
                      <Button key={s} variant="outline" onClick={() => chooseIssue(s)}>
                        <span>
                          <CircleHelp size={18} />
                        </span>
                        {s}
                        <ChevronRight size={17} />
                      </Button>
                    ))}
                  </div>
                )}
                <div className="mobile-section-heading">
                  <div>
                    <span>YÊU CẦU CỦA BẠN</span>
                    <h2>Lịch sử hỗ trợ</h2>
                  </div>
                </div>
                {myTickets.length ? (
                  <div className="support-history">
                    {myTickets.map((t) => (
                      <Link key={t.id} to="/customer" search={{ ticket: t.id }} className="block">
                        <TicketRow ticket={t} />
                      </Link>
                    ))}
                  </div>
                ) : (
                  <div className="support-empty">Chưa có yêu cầu hỗ trợ nào.</div>
                )}
                <Button variant="outline" className="chat-entry" onClick={() => setChat(true)}>
                  <MessageCircle size={19} />
                  <span>
                    <strong>Trò chuyện hỗ trợ</strong>
                    <small>AI hỗ trợ · Chăm sóc khách hàng · Kỹ thuật viên</small>
                  </span>
                  <ChevronRight size={17} />
                </Button>
              </>
            )}
            {tab === "Cá nhân" && (
              <>
                <div className="mobile-page-title">
                  <span>TÀI KHOẢN CỦA BẠN</span>
                  <h1>Cá nhân</h1>
                </div>
                <div className="profile-block">
                  <span className="profile-avatar">{you.name.slice(-2)}</span>
                  <h2>{you.name}</h2>
                  <p>{you.id}</p>
                </div>
                <div className="mobile-info-block">
                  <div className="mini-section-title">THÔNG TIN THUÊ BAO</div>
                  <div className="simple-kv">
                    <span>Số điện thoại</span>
                    <strong>{you.phone}</strong>
                    <span>Địa chỉ</span>
                    <strong>{you.address}</strong>
                    <span>ONT</span>
                    <strong>{device.id}</strong>
                  </div>
                </div>
                <Button variant="outline" className="w-full mt-4" onClick={() => setTab("Hỗ trợ")}>
                  <Phone size={17} /> Liên hệ hỗ trợ
                </Button>
              </>
            )}
          </>
        )}
      </div>
      <nav className="mobile-bottom-nav">
        {nav.map(({ name, icon: Icon }) => (
          <Button
            key={name}
            variant="ghost"
            className={tab === name ? "active" : ""}
            onClick={() => {
              setTab(name);
              setIssue("");
              setDiagnosed(false);
              if (sp.ticket) navigate({ search: {} });
            }}
          >
            <Icon size={21} />
            <span>{name}</span>
          </Button>
        ))}
      </nav>
      {chat && (
        <div className="chat-overlay">
          <div className="chat-window">
            <div className="chat-header">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setChat(false)}
                aria-label="Đóng trò chuyện"
              >
                <ArrowLeft />
              </Button>
              <div>
                <strong>Hỗ trợ trực tuyến</strong>
                <small>Giao diện trò chuyện thử nghiệm</small>
              </div>
            </div>
            <div className="chat-body">
              <p>Xin chào! Chúng tôi có thể giúp gì cho bạn?</p>
              {chatMessages.map((m, i) => (
                <p className="own-message" key={i}>
                  {m}
                </p>
              ))}
            </div>
            <div className="chat-input">
              <input
                placeholder="Nhập tin nhắn..."
                value={chatText}
                onChange={(e) => setChatText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" && chatText.trim()) {
                    setChatMessages([...chatMessages, chatText]);
                    setChatText("");
                  }
                }}
              />
              <Button
                size="icon"
                onClick={() => {
                  if (chatText.trim()) {
                    setChatMessages([...chatMessages, chatText]);
                    setChatText("");
                  }
                }}
                aria-label="Gửi tin nhắn"
              >
                <Send size={17} />
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
function DeviceRows({ devices }: { devices: typeof lanDevices }) {
  return (
    <div className="mobile-rows device-rows">
      {devices.map((d, i) => {
        const Icon = i === 0 ? Smartphone : i === 1 ? Monitor : Laptop;
        return (
          <div key={d.id}>
            <span className="row-icon">
              <Icon size={19} />
            </span>
            <div>
              <strong>{d.name}</strong>
              <small>
                {d.connection} · {d.ip}
              </small>
            </div>
            <span className={`device-state ${d.online ? "online" : ""}`}>
              <i />
              {d.online ? "Online" : "Offline"}
            </span>
          </div>
        );
      })}
    </div>
  );
}
function TicketRow({ ticket: t }: { ticket: Ticket }) {
  return (
    <div className="ticket-row">
      <div>
        <strong>{t.issue}</strong>
        <small>
          {t.id} · {t.created}
        </small>
        {t.technicianId && (
          <small>Kỹ thuật viên: {techFor(t.technicianId)?.name} · ETA 30 phút</small>
        )}
      </div>
      <span
        className={`status status-${["CLOSED", "RESOLVED"].includes(t.status) ? "good" : t.status === "OPEN" ? "bad" : "warn"}`}
      >
        <span className="status-dot" />
        {statusLabels[t.status]}
      </span>
    </div>
  );
}
