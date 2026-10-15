import { n as __toESM } from "../_runtime.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as require_jsx_runtime } from "../_libs/react+tanstack__react-query.mjs";
import { f as usePlatform, i as lanDevices, l as statusLabels, r as customers, s as onts, u as techFor } from "./deep-links-BPsBDoll.mjs";
import { b as useNavigate, y as Link } from "../_libs/@tanstack/react-router+[...].mjs";
import { t as Route } from "./customer-DsU2WWe1.mjs";
import { t as Button } from "./button-DRsC1qZi.mjs";
import { A as CircleUserRound, B as ArrowRight, C as Laptop, E as Gauge, M as CircleCheck, N as ChevronRight, R as Bell, T as HardDrive, U as Activity, V as ArrowLeft, _ as Phone, b as MessageCircle, d as Send, f as Search, i as Wifi, j as CircleQuestionMark, p as Router, s as Smartphone, t as Zap, w as House, y as Monitor } from "../_libs/lucide-react.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/customer-DokNFCei.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var nav = [
	{
		name: "Trang chủ",
		icon: House
	},
	{
		name: "Internet",
		icon: Wifi
	},
	{
		name: "Thiết bị",
		icon: HardDrive
	},
	{
		name: "Hỗ trợ",
		icon: CircleQuestionMark
	},
	{
		name: "Cá nhân",
		icon: CircleUserRound
	}
];
var issues = [
	"Internet chậm",
	"Mất Internet",
	"Wi-Fi yếu",
	"Không kết nối được",
	"Thiết bị không vào mạng",
	"Khác"
];
var you = customers[0] ?? {
	id: "KH-001",
	name: "Nguyễn Minh An",
	phone: "",
	address: "",
	ontId: "ONT-001"
};
var device = onts[0] ?? {
	id: "ONT-001",
	serial: "",
	model: "",
	firmware: "",
	customerId: you.id,
	status: "UNKNOWN",
	optical: 0,
	uptime: "",
	lastSeen: "",
	wan: "",
	wifi: "",
	speed: 0,
	ping: 0
};
function CustomerApp() {
	const { tickets, createTicket, notify } = usePlatform();
	const [tab, setTab] = (0, import_react.useState)("Trang chủ");
	const [issue, setIssue] = (0, import_react.useState)("");
	const [diagnosed, setDiagnosed] = (0, import_react.useState)(false);
	const [test, setTest] = (0, import_react.useState)(false);
	const [chat, setChat] = (0, import_react.useState)(false);
	const [chatText, setChatText] = (0, import_react.useState)("");
	const [chatMessages, setChatMessages] = (0, import_react.useState)([]);
	const myTickets = tickets.filter((t) => t.customerId === you.id);
	const sp = Route.useSearch();
	const navigate = useNavigate({ from: "/customer" });
	const openTicket = sp.ticket ? myTickets.find((t) => t.id === sp.ticket) : void 0;
	const closeTicket = () => {
		navigate({ search: {} });
		setTab("Hỗ trợ");
	};
	const devices = lanDevices.filter((d) => d.ontId === device.id);
	const chooseIssue = (value) => {
		setIssue(value);
		setDiagnosed(false);
		setTab("Hỗ trợ");
	};
	const submit = () => {
		createTicket(you.id, device.id, issue);
		setIssue("");
		setDiagnosed(false);
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "mobile-app customer-app",
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "mobile-top",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mobile-logo",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Activity, { size: 19 }) }),
						"ONT",
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Platform" })
					]
				}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "mobile-top-actions",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
							to: "/",
							title: "Bảng điều hành",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HardDrive, { size: 18 })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
							to: "/technician",
							title: "App Thợ",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Router, { size: 18 })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
							variant: "ghost",
							size: "icon",
							"aria-label": "Thông báo",
							onClick: () => notify(myTickets.length ? `${myTickets.length} yêu cầu hỗ trợ của bạn` : "Chưa có thông báo mới"),
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Bell, { size: 20 })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mobile-avatar customer-avatar",
							children: you.name.slice(-2)
						})
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mobile-body",
				children: sp.ticket ? openTicket ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
						variant: "ghost",
						className: "mobile-back",
						onClick: closeTicket,
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { size: 17 }), " Hỗ trợ"]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mobile-page-title",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["YÊU CẦU ", openTicket.id] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: openTicket.issue }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [
								"Tạo lúc ",
								openTicket.created,
								" · Cập nhật ",
								openTicket.updated
							] })
						]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(TicketRow, { ticket: openTicket }),
					openTicket.diagnosis && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "suggestion",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "KẾT QUẢ XỬ LÝ"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: openTicket.diagnosis }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: openTicket.action }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: openTicket.testResult })
						]
					})
				] }) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "not-found-block",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mini-section-title",
							children: "LIÊN KẾT KHÔNG HỢP LỆ"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", { children: ["Không tìm thấy yêu cầu ", sp.ticket] }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Yêu cầu này không tồn tại hoặc không thuộc tài khoản của bạn." }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							className: "w-full",
							onClick: closeTicket,
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { size: 17 }), " Về trang Hỗ trợ"]
						})
					]
				}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
					tab === "Trang chủ" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-greeting customer-greeting",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "CHÀO MỪNG TRỞ LẠI" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Internet của bạn." }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [
									"Xin chào ",
									you.name,
									", mọi thứ đều ổn định."
								] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "connection-block",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "connection-top",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
										className: "connection-icon",
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Wifi, { size: 27 })
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
										className: "connection-live",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("i", {}), " Đang hoạt động"]
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "connection-center",
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "TRẠNG THÁI KẾT NỐI" }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Đã kết nối" }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Internet đang hoạt động tốt" })
									]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "connection-stats",
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "DOWNLOAD" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: ["125 ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Mbps" })] })] }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "UPLOAD" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: ["45 ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Mbps" })] })] }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "PING" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: ["12 ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "ms" })] })] })
									]
								})
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-section-heading",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "KIỂM TRA NHANH" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Bạn muốn làm gì?" })] })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "quick-actions",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									variant: "outline",
									onClick: () => {
										setTab("Internet");
										setTest(true);
										notify("Đã kiểm tra Internet: kết nối ổn định");
									},
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Gauge, { size: 20 }) }),
										"Kiểm tra Internet ",
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronRight, { size: 16 })
									]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									variant: "outline",
									onClick: () => {
										setTab("Internet");
										notify("Wi-Fi 2.4GHz và 5GHz đang hoạt động");
									},
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Wifi, { size: 20 }) }),
										"Kiểm tra Wi-Fi ",
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronRight, { size: 16 })
									]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									variant: "outline",
									onClick: () => setTab("Hỗ trợ"),
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleQuestionMark, { size: 20 }) }),
										"Báo sự cố ",
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronRight, { size: 16 })
									]
								})
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-section-heading",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "MẠNG NHÀ BẠN" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Thiết bị đang kết nối" })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								variant: "ghost",
								onClick: () => setTab("Thiết bị"),
								children: ["Xem tất cả ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 16 })]
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(DeviceRows, { devices })
					] }),
					tab === "Internet" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "ĐƯỜNG TRUYỀN" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Internet" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Theo dõi chất lượng kết nối của bạn." })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "internet-status",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Wifi, { size: 22 }) }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Đường truyền ổn định" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "ONT và Wi-Fi đang hoạt động" })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleCheck, { size: 19 })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "internet-metrics",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Download" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: [
									device.speed,
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Mbps" })
								] })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Upload" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: [
									Math.round(device.speed * .36),
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Mbps" })
								] })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Ping" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: [
									device.ping,
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "ms" })
								] })] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-info-block",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "THÔNG TIN KẾT NỐI"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "simple-kv",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Internet" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Đang hoạt động" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "ONT" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: statusLabels[device.status] }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Wi-Fi" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Đang hoạt động" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Thời gian hoạt động" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: device.uptime })
								]
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							className: "w-full customer-main-button",
							onClick: () => {
								setTest(true);
								notify("Kiểm tra hoàn tất: kết nối ổn định");
							},
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Zap, { size: 17 }), " Kiểm tra Internet"]
						}),
						test && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "test-result",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleCheck, { size: 20 }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Kết nối của bạn đang tốt" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [
								"Download ",
								device.speed,
								" Mbps · Upload ",
								Math.round(device.speed * .36),
								" Mbps · Ping ",
								device.ping,
								" ms"
							] })] })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-section-heading",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "LỊCH SỬ" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Lần kiểm tra gần đây" })] })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-rows",
							children: [
								0,
								1,
								2
							].map((i) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "row-icon",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Gauge, { size: 18 })
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: [125 - i * 7, " Mbps download"] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
									i === 0 ? "Hôm nay" : `${i + 1} ngày trước`,
									" · Ping ",
									12 + i * 2,
									" ms"
								] })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleCheck, {
									size: 17,
									className: "text-success"
								})
							] }, i))
						})
					] }),
					tab === "Thiết bị" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "MẠNG NHÀ BẠN" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Thiết bị" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [devices.filter((d) => d.online).length, " thiết bị đang kết nối."] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(DeviceRows, { devices }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-info-block",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "THÔNG TIN BỘ PHÁT"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "simple-kv",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Model" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: device.model }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Serial" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: device.serial }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Wi-Fi" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "2.4GHz / 5GHz" })
								]
							})]
						})
					] }),
					tab === "Hỗ trợ" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "LUÔN SẴN SÀNG HỖ TRỢ" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Hỗ trợ" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Chọn vấn đề bạn đang gặp phải." })
							]
						}),
						issue ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								variant: "ghost",
								className: "mobile-back",
								onClick: () => {
									setIssue("");
									setDiagnosed(false);
								},
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { size: 17 }), " Chọn vấn đề khác"]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "issue-heading",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "row-icon",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleQuestionMark, { size: 20 })
								}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "VẤN ĐỀ BẠN GẶP" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: issue })] })]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "diagnosis-steps",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
										className: "step-active",
										children: [
											/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "1" }),
											/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Tự động kiểm tra" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Kiểm tra ONT, kết nối và Wi-Fi" })] }),
											/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleCheck, { size: 17 })
										]
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
										className: diagnosed ? "step-active" : "",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "2" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Đề xuất xử lý" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Các bước đơn giản bạn có thể thử" })] })]
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
										className: diagnosed ? "step-active" : "",
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "3" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Gửi yêu cầu hỗ trợ" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Nếu vấn đề vẫn chưa được giải quyết" })] })]
									})
								]
							}),
							!diagnosed ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								className: "w-full customer-main-button",
								onClick: () => setDiagnosed(true),
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Search, { size: 17 }), " Bắt đầu kiểm tra"]
							}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "suggestion",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
										className: "mini-section-title",
										children: "KẾT QUẢ KIỂM TRA"
									}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Thiết bị đang kết nối bình thường" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Hãy thử khởi động lại bộ phát Wi-Fi và kiểm tra vị trí đặt thiết bị. Nếu vẫn gặp sự cố, gửi yêu cầu để đội kỹ thuật hỗ trợ." })
								]
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								className: "w-full customer-main-button",
								onClick: submit,
								children: ["Vẫn gặp sự cố — Gửi yêu cầu ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 17 })]
							})] })
						] }) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "issue-list",
							children: issues.map((s) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								variant: "outline",
								onClick: () => chooseIssue(s),
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleQuestionMark, { size: 18 }) }),
									s,
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronRight, { size: 17 })
								]
							}, s))
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-section-heading",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "YÊU CẦU CỦA BẠN" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Lịch sử hỗ trợ" })] })
						}),
						myTickets.length ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "support-history",
							children: myTickets.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Link, {
								to: "/customer",
								search: { ticket: t.id },
								className: "block",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(TicketRow, { ticket: t })
							}, t.id))
						}) : /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "support-empty",
							children: "Chưa có yêu cầu hỗ trợ nào."
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							variant: "outline",
							className: "chat-entry",
							onClick: () => setChat(true),
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(MessageCircle, { size: 19 }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Trò chuyện hỗ trợ" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "AI hỗ trợ · Chăm sóc khách hàng · Kỹ thuật viên" })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ChevronRight, { size: 17 })
							]
						})
					] }),
					tab === "Cá nhân" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "TÀI KHOẢN CỦA BẠN" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Cá nhân" })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "profile-block",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "profile-avatar",
									children: you.name.slice(-2)
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: you.name }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: you.id })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-info-block",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "THÔNG TIN THUÊ BAO"
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "simple-kv",
								children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Số điện thoại" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: you.phone }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Địa chỉ" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: you.address }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "ONT" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: device.id })
								]
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							variant: "outline",
							className: "w-full mt-4",
							onClick: () => setTab("Hỗ trợ"),
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Phone, { size: 17 }), " Liên hệ hỗ trợ"]
						})
					] })
				] })
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("nav", {
				className: "mobile-bottom-nav",
				children: nav.map(({ name, icon: Icon }) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
					variant: "ghost",
					className: tab === name ? "active" : "",
					onClick: () => {
						setTab(name);
						setIssue("");
						setDiagnosed(false);
						if (sp.ticket) navigate({ search: {} });
					},
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Icon, { size: 21 }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: name })]
				}, name))
			}),
			chat && /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "chat-overlay",
				children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "chat-window",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "chat-header",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
								variant: "ghost",
								size: "icon",
								onClick: () => setChat(false),
								"aria-label": "Đóng trò chuyện",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, {})
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Hỗ trợ trực tuyến" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Giao diện trò chuyện thử nghiệm" })] })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "chat-body",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Xin chào! Chúng tôi có thể giúp gì cho bạn?" }), chatMessages.map((m, i) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
								className: "own-message",
								children: m
							}, i))]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "chat-input",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
								placeholder: "Nhập tin nhắn...",
								value: chatText,
								onChange: (e) => setChatText(e.target.value),
								onKeyDown: (e) => {
									if (e.key === "Enter" && chatText.trim()) {
										setChatMessages([...chatMessages, chatText]);
										setChatText("");
									}
								}
							}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
								size: "icon",
								onClick: () => {
									if (chatText.trim()) {
										setChatMessages([...chatMessages, chatText]);
										setChatText("");
									}
								},
								"aria-label": "Gửi tin nhắn",
								children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Send, { size: 17 })
							})]
						})
					]
				})
			})
		]
	});
}
function DeviceRows({ devices }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
		className: "mobile-rows device-rows",
		children: devices.map((d, i) => {
			return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
				/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: "row-icon",
					children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(i === 0 ? Smartphone : i === 1 ? Monitor : Laptop, { size: 19 })
				}),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: d.name }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
					d.connection,
					" · ",
					d.ip
				] })] }),
				/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
					className: `device-state ${d.online ? "online" : ""}`,
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("i", {}), d.online ? "Online" : "Offline"]
				})
			] }, d.id);
		})
	});
}
function TicketRow({ ticket: t }) {
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "ticket-row",
		children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: t.issue }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
				t.id,
				" · ",
				t.created
			] }),
			t.technicianId && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
				"Kỹ thuật viên: ",
				techFor(t.technicianId)?.name,
				" · ETA 30 phút"
			] })
		] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
			className: `status status-${["CLOSED", "RESOLVED"].includes(t.status) ? "good" : t.status === "OPEN" ? "bad" : "warn"}`,
			children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "status-dot" }), statusLabels[t.status]]
		})]
	});
}
//#endregion
export { CustomerApp as component };
