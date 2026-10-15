import { n as __toESM } from "../_runtime.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as require_jsx_runtime } from "../_libs/react+tanstack__react-query.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/deep-links-BPsBDoll.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var first = [
	"Nguyễn Minh",
	"Trần Thị",
	"Lê Văn",
	"Phạm Hoàng",
	"Đỗ Thu",
	"Võ Thanh",
	"Bùi Ngọc",
	"Hoàng Anh",
	"Mai Quốc",
	"Đặng Hải"
];
var last = [
	"An",
	"Bình",
	"Chi",
	"Dũng",
	"Hà",
	"Hùng",
	"Lan",
	"Minh",
	"Phong",
	"Trang"
];
var streets = [
	"Nguyễn Huệ",
	"Lê Lợi",
	"Trần Hưng Đạo",
	"Điện Biên Phủ",
	"Phan Xích Long",
	"Hoàng Văn Thụ"
];
var areas = [
	"Quận 1",
	"Quận 3",
	"Bình Thạnh",
	"Phú Nhuận",
	"Thủ Đức"
];
var pad$1 = (n, size = 3) => String(n).padStart(size, "0");
var customers = Array.from({ length: 100 }, (_, i) => ({
	id: `KH-${pad$1(i + 1)}`,
	name: `${first[i % 10] ?? "Nguyễn Minh"} ${last[Math.floor(i / 10)] ?? "An"}`,
	phone: `09${String(1e7 + i * 78391).slice(0, 8)}`,
	address: `${12 + i * 3} ${streets[i % streets.length] ?? "Nguyễn Huệ"}, ${areas[i % areas.length] ?? "Quận 1"}, TP. HCM`,
	ontId: `ONT-${pad$1(i + 1)}`
}));
var onts = Array.from({ length: 100 }, (_, i) => ({
	id: `ONT-${pad$1(i + 1)}`,
	serial: `ZTEG${String(48290001 + i * 17)}`,
	model: [
		"ZXHN F670L",
		"HG8145V5",
		"ZXHN F6600P",
		"HG8245H"
	][i % 4] ?? "ZXHN F670L",
	firmware: `V${i % 3 + 1}.2.${i % 7}`,
	customerId: `KH-${pad$1(i + 1)}`,
	status: i < 80 ? "ONLINE" : i < 92 ? "WARNING" : "OFFLINE",
	optical: Number((i < 80 ? -18.2 - i % 8 * .5 : i < 92 ? -26.1 - i % 4 * .6 : -30.2).toFixed(1)),
	uptime: i < 80 ? `${2 + i % 17} ngày ${i % 23} giờ` : i < 92 ? `${i % 8} giờ` : "—",
	lastSeen: i < 80 ? "Vừa xong" : i < 92 ? `${3 + i % 20} phút trước` : `${1 + i % 7} giờ trước`,
	wan: i >= 92 ? "Mất kết nối" : "Đã kết nối",
	wifi: i >= 92 ? "Không khả dụng" : "Hoạt động",
	speed: i < 80 ? 110 + i % 55 : i < 92 ? 24 + i % 18 : 0,
	ping: i < 80 ? 10 + i % 14 : i < 92 ? 68 + i % 34 : 0
}));
var technicians = Array.from({ length: 15 }, (_, i) => ({
	id: `KT-${pad$1(i + 1)}`,
	name: `${first[(i + 3) % 10] ?? "Nguyễn Minh"} ${last[(i + 2) % 10] ?? "An"}`,
	area: areas[i % 5] ?? "Quận 1",
	status: i < 6 ? "BUSY" : i < 13 ? "AVAILABLE" : "OFFLINE",
	lastActive: i < 13 ? "Vừa xong" : "2 giờ trước"
}));
var issues = [
	"Internet chậm",
	"Mất kết nối Internet",
	"Wi-Fi yếu",
	"Không kết nối được",
	"Thiết bị không vào mạng",
	"Tín hiệu quang yếu"
];
var initialTickets = Array.from({ length: 30 }, (_, i) => ({
	id: `TK-${pad$1(2401 + i, 4)}`,
	customerId: `KH-${pad$1((i * 7 + 80) % 100 + 1)}`,
	ontId: `ONT-${pad$1((i * 7 + 80) % 100 + 1)}`,
	issue: issues[i % issues.length] ?? "Internet chậm",
	priority: i % 6 === 0 ? "Cao" : i % 3 === 0 ? "Thấp" : "Trung bình",
	status: [
		"OPEN",
		"ASSIGNED",
		"IN_PROGRESS",
		"RESOLVED",
		"CLOSED"
	][i % 5] ?? "OPEN",
	technicianId: i % 5 !== 0 ? `KT-${pad$1(i % 15 + 1)}` : void 0,
	created: `28/09/2026 · ${pad$1(8 + i % 10, 2)}:${pad$1(i * 7 % 60, 2)}`,
	updated: `${i % 5 + 1} phút trước`
}));
var lanDevices = Array.from({ length: 200 }, (_, i) => ({
	id: `DEV-${pad$1(i + 1)}`,
	ontId: `ONT-${pad$1(Math.floor(i / 2) + 1)}`,
	name: [
		"iPhone",
		"Smart TV",
		"Laptop",
		"Camera IP",
		"Máy tính bảng"
	][i % 5] ?? "Thiết bị",
	ip: `192.168.1.${10 + i % 200}`,
	mac: `A4:6B:BC:${pad$1(i % 99, 2)}:${pad$1(i * 3 % 99, 2)}:${pad$1(i * 7 % 99, 2)}`,
	connection: i % 4 === 0 ? "LAN" : i % 3 === 0 ? "Wi-Fi 2.4GHz" : "Wi-Fi 5GHz",
	online: i % 9 !== 0,
	lastSeen: i % 9 !== 0 ? "Vừa xong" : "1 giờ trước"
}));
var statusLabels = {
	ONLINE: "Online",
	WARNING: "Cảnh báo",
	OFFLINE: "Offline",
	UNKNOWN: "Chưa rõ",
	OPEN: "Mới tạo",
	ASSIGNED: "Đã phân công",
	IN_PROGRESS: "Đang xử lý",
	WAITING_CUSTOMER: "Chờ khách xác nhận",
	RESOLVED: "Đã xử lý",
	CLOSED: "Đã đóng"
};
var customerFor = (id) => customers.find((c) => c.id === id);
var ontFor = (id) => onts.find((o) => o.id === id);
var techFor = (id) => technicians.find((t) => t.id === id);
var Context = (0, import_react.createContext)(null);
var pad = (n, size = 3) => String(n).padStart(size, "0");
function PlatformProvider({ children }) {
	const [tickets, setTickets] = (0, import_react.useState)(initialTickets);
	const [customers$1, setCustomers] = (0, import_react.useState)(customers);
	const [onts$1, setOnts] = (0, import_react.useState)(onts);
	const [message, setMessage] = (0, import_react.useState)("");
	const createTicket = (customerId, ontId, issue) => {
		const ticket = {
			id: `TK-${String(2431 + tickets.length - 30).padStart(4, "0")}`,
			customerId,
			ontId,
			issue,
			priority: "Trung bình",
			status: "OPEN",
			created: "Vừa xong",
			updated: "Vừa xong"
		};
		setTickets((prev) => [ticket, ...prev]);
		setMessage(`Đã tạo yêu cầu ${ticket.id}`);
		return ticket;
	};
	const updateTicket = (id, patch) => setTickets((prev) => prev.map((t) => t.id === id ? {
		...t,
		...patch,
		updated: "Vừa xong"
	} : t));
	(0, import_react.useEffect)(() => {
		if (!message) return;
		const t = setTimeout(() => setMessage(""), 3e3);
		return () => clearTimeout(t);
	}, [message]);
	const addCustomer = (data) => {
		const id = `KH-${pad(customers$1.length + 1)}`;
		const customer = {
			id,
			name: data.name,
			phone: data.phone,
			address: data.address,
			ontId: ""
		};
		setCustomers((prev) => [...prev, customer]);
		setMessage(`Đã thêm khách hàng ${id} — ${data.name}`);
		return customer;
	};
	const addOnt = (data) => {
		const id = `ONT-${pad(onts$1.length + 1)}`;
		const ont = {
			id,
			serial: data.serial,
			model: data.model,
			firmware: "V1.2.0",
			customerId: data.customerId,
			status: "UNKNOWN",
			optical: 0,
			uptime: "—",
			lastSeen: "Chưa kết nối",
			wan: "Chưa cấu hình",
			wifi: "Chưa cấu hình",
			speed: 0,
			ping: 0
		};
		setOnts((prev) => [...prev, ont]);
		if (data.customerId) setCustomers((prev) => prev.map((c) => c.id === data.customerId ? {
			...c,
			ontId: id
		} : c));
		setMessage(`Đã thêm thiết bị ${id} (${data.serial})`);
		return ont;
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Context.Provider, {
		value: {
			tickets,
			customers: customers$1,
			onts: onts$1,
			createTicket,
			updateTicket,
			addCustomer,
			addOnt,
			message,
			notify: setMessage
		},
		children: [children, message && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
			role: "status",
			className: "fixed bottom-5 right-5 z-50 max-w-sm rounded-md border border-border bg-foreground px-4 py-3 text-sm text-background shadow-lg",
			onClick: () => setMessage(""),
			children: message
		})]
	});
}
function usePlatform() {
	const value = (0, import_react.useContext)(Context);
	if (!value) throw new Error("Platform provider missing");
	return value;
}
var clean = (value) => typeof value === "string" && value.trim() ? value.trim().toUpperCase().slice(0, 32) : void 0;
function parseDeepLink(raw) {
	const out = {};
	const ont = clean(raw["ont"]);
	const ticket = clean(raw["ticket"]);
	if (ont) out.ont = ont;
	if (ticket) out.ticket = ticket;
	if (typeof raw["tab"] === "string" && raw["tab"].trim()) out.tab = raw["tab"].trim().slice(0, 32);
	return out;
}
var ontTabs = [
	"Overview",
	"Internet",
	"Wi-Fi",
	"LAN",
	"Optical / PON",
	"Devices",
	"Tests",
	"Events",
	"Remote Actions"
];
//#endregion
export { ontFor as a, parseDeepLink as c, technicians as d, usePlatform as f, lanDevices as i, statusLabels as l, customerFor as n, ontTabs as o, customers as r, onts as s, PlatformProvider as t, techFor as u };
