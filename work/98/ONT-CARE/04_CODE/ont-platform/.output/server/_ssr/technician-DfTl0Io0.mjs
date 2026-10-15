import { n as __toESM } from "../_runtime.mjs";
import { n as require_react } from "../_libs/@radix-ui/react-compose-refs+[...].mjs";
import { n as require_jsx_runtime } from "../_libs/react+tanstack__react-query.mjs";
import { a as ontFor, d as technicians, f as usePlatform, l as statusLabels, n as customerFor } from "./deep-links-BPsBDoll.mjs";
import { b as useNavigate, y as Link } from "../_libs/@tanstack/react-router+[...].mjs";
import { t as Button } from "./button-DRsC1qZi.mjs";
import { A as CircleUserRound, B as ArrowRight, I as Check, L as Camera, M as CircleCheck, O as Clock3, R as Bell, T as HardDrive, U as Activity, V as ArrowLeft, _ as Phone, a as Users, f as Search, g as Plus, k as ClipboardList, n as X, o as UserRound, r as Wrench, w as House, x as MapPin } from "../_libs/lucide-react.mjs";
import { t as Route } from "./technician-4pASRdn4.mjs";
import { t as Input } from "./input-DicJzR9-.mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/technician-DfTl0Io0.js
var import_react = /* @__PURE__ */ __toESM(require_react());
var import_jsx_runtime = require_jsx_runtime();
var tabs = [
	{
		name: "Trang chủ",
		icon: House
	},
	{
		name: "Công việc",
		icon: ClipboardList
	},
	{
		name: "Khách hàng",
		icon: Users
	},
	{
		name: "Thiết bị",
		icon: HardDrive
	},
	{
		name: "Cá nhân",
		icon: CircleUserRound
	}
];
var technician = technicians[0] ?? {
	id: "KT-001",
	name: "Kỹ thuật viên",
	area: "Quận 1",
	status: "AVAILABLE",
	lastActive: "Vừa xong"
};
var checklist = [
	"Kiểm tra nguồn",
	"Kiểm tra WAN",
	"Kiểm tra PON",
	"Kiểm tra optical",
	"Kiểm tra Wi-Fi",
	"Kiểm tra LAN",
	"Chạy Speed Test",
	"Kiểm tra thiết bị khách"
];
function TechnicianApp() {
	const { tickets, customers, onts, updateTicket, addCustomer, addOnt, notify } = usePlatform();
	const [tab, setTab] = (0, import_react.useState)("Trang chủ");
	const [checks, setChecks] = (0, import_react.useState)([]);
	const [diagnosis, setDiagnosis] = (0, import_react.useState)("");
	const [action, setAction] = (0, import_react.useState)("");
	const [testResult, setTestResult] = (0, import_react.useState)("");
	const [confirmed, setConfirmed] = (0, import_react.useState)(false);
	const [query, setQuery] = (0, import_react.useState)("");
	const [addingCustomer, setAddingCustomer] = (0, import_react.useState)(false);
	const [newName, setNewName] = (0, import_react.useState)("");
	const [newPhone, setNewPhone] = (0, import_react.useState)("");
	const [newAddress, setNewAddress] = (0, import_react.useState)("");
	const [addingOnt, setAddingOnt] = (0, import_react.useState)(false);
	const [newSerial, setNewSerial] = (0, import_react.useState)("");
	const [newModel, setNewModel] = (0, import_react.useState)("ZXHN F670L");
	const [newOntCustomer, setNewOntCustomer] = (0, import_react.useState)("");
	const mine = tickets.filter((t) => t.technicianId === technician.id || t.status === "OPEN");
	const sp = Route.useSearch();
	const navigate = useNavigate({ from: "/technician" });
	const setJob = (t) => navigate({ search: t ? { ticket: t.id } : {} });
	const current = sp.ticket ? tickets.find((t) => t.id === sp.ticket) ?? null : null;
	const missingTicket = sp.ticket && !current ? sp.ticket : null;
	const cust = current ? customerFor(current.customerId) : void 0;
	const ont = current ? ontFor(current.ontId) : void 0;
	const select = (t) => setJob(t);
	(0, import_react.useEffect)(() => {
		const t = sp.ticket ? tickets.find((x) => x.id === sp.ticket) : void 0;
		setChecks([]);
		setDiagnosis(t?.diagnosis ?? "");
		setAction(t?.action ?? "");
		setTestResult(t?.testResult ?? "");
		setConfirmed(t?.confirmed ?? false);
	}, [sp.ticket]);
	const start = (t) => {
		updateTicket(t.id, {
			status: t.status === "OPEN" ? "ASSIGNED" : "IN_PROGRESS",
			technicianId: technician.id
		});
		notify(t.status === "OPEN" ? "Đã nhận công việc" : "Đã bắt đầu xử lý");
	};
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "mobile-app technician-app",
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
							to: "/customer",
							title: "App Khách",
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Users, { size: 18 })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
							variant: "ghost",
							size: "icon",
							"aria-label": "Thông báo",
							onClick: () => notify(`${mine.length} công việc cần theo dõi`),
							children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Bell, { size: 20 })
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mobile-avatar",
							children: "KT"
						})
					]
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
				className: "mobile-body",
				children: missingTicket ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
					className: "not-found-block",
					children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mini-section-title",
							children: "LIÊN KẾT KHÔNG HỢP LỆ"
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", { children: ["Không tìm thấy công việc ", missingTicket] }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Công việc này không tồn tại hoặc đã bị xoá." }),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							className: "w-full",
							onClick: () => {
								setJob(null);
								setTab("Công việc");
							},
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { size: 17 }), " Về danh sách công việc"]
						})
					]
				}) : current && cust && ont ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
						variant: "ghost",
						className: "mobile-back",
						onClick: () => setJob(null),
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowLeft, { size: 18 }), " Công việc"]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mobile-title-row",
						children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
							className: "mobile-kicker",
							children: [
								current.id,
								" · ",
								current.priority.toUpperCase()
							]
						}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: current.issue })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
							className: "mobile-status",
							children: statusLabels[current.status]
						})]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mobile-info-block",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "THÔNG TIN KHÁCH HÀNG"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: cust.name }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(MapPin, { size: 15 }), cust.address] }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("a", {
								href: `tel:${cust.phone}`,
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Phone, { size: 15 }), cust.phone]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
								to: "/",
								search: { ticket: current.id },
								className: "deep-inline",
								children: ["Xem ticket trên Dashboard ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 14 })]
							})
						]
					}),
					/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mobile-info-block",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
								className: "mini-section-title",
								children: "THIẾT BỊ ONT"
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "mobile-device-row",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: ont.model }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
									ont.serial,
									" · ",
									ont.id
								] })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
									className: `status status-${ont.status === "ONLINE" ? "good" : ont.status === "WARNING" ? "warn" : "bad"}`,
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "status-dot" }), statusLabels[ont.status]]
								})]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
								className: "mobile-device-metrics",
								children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["Optical ", /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("strong", { children: [ont.optical, " dBm"] })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: ["WAN ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: ont.wan })] })]
							}),
							/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Link, {
								to: "/",
								search: { ont: ont.id },
								className: "deep-inline",
								children: ["Mở chi tiết ONT ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 14 })]
							})
						]
					}),
					current.status === "OPEN" || current.status === "ASSIGNED" ? /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mobile-cta",
						children: /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							className: "w-full",
							onClick: () => start(current),
							children: [
								current.status === "OPEN" ? "Nhận việc" : "Bắt đầu xử lý",
								" ",
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 17 })
							]
						})
					}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mini-section-title checklist-heading",
							children: [
								"CHECKLIST KỸ THUẬT",
								" ",
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [
									checks.length,
									"/",
									checklist.length
								] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "checklist",
							children: checklist.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
									type: "checkbox",
									checked: checks.includes(c),
									onChange: () => setChecks((prev) => prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c])
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "check-mark",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Check, { size: 13 })
								}),
								c
							] }, c))
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-form",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
									className: "mini-section-title",
									children: "BÁO CÁO XỬ LÝ"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"1. Chẩn đoán nguyên nhân",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", {
										value: diagnosis,
										onChange: (e) => setDiagnosis(e.target.value),
										placeholder: "Mô tả vấn đề đã xác định..."
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"2. Biện pháp xử lý",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", {
										value: action,
										onChange: (e) => setAction(e.target.value),
										placeholder: "Các bước đã thực hiện..."
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"3. Kết quả kiểm tra",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", {
										value: testResult,
										onChange: (e) => setTestResult(e.target.value),
										placeholder: "Kết quả sau xử lý..."
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "field-tools",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
										variant: "outline",
										onClick: () => {
											setTestResult(`Download ${ont.speed} Mbps · Upload ${Math.round(ont.speed * .36)} Mbps · Ping ${ont.ping} ms`);
											notify("Đã chạy kiểm tra tốc độ");
										},
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Activity, { size: 16 }), " Chạy test"]
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
										className: "photo-tool",
										children: [
											/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Camera, { size: 16 }),
											" Chụp ảnh",
											/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
												type: "file",
												accept: "image/*",
												capture: "environment",
												onChange: (e) => notify(e.target.files?.[0]?.name ? `Đã chọn ảnh ${e.target.files[0].name}` : "")
											})
										]
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: ["Ghi chú thêm ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", { placeholder: "Ghi chú cho đội vận hành..." })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", {
									className: "confirm-check",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("input", {
										type: "checkbox",
										checked: confirmed,
										onChange: (e) => setConfirmed(e.target.checked)
									}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Khách hàng đã xác nhận kết quả xử lý" })]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									className: "w-full",
									disabled: !diagnosis.trim() || !action.trim() || !testResult.trim() || !confirmed,
									onClick: () => {
										updateTicket(current.id, {
											status: "CLOSED",
											diagnosis,
											action,
											testResult,
											confirmed
										});
										notify(`${current.id} đã hoàn thành và đóng`);
										setJob(null);
										setTab("Công việc");
									},
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(CircleCheck, { size: 17 }), " Xác nhận hoàn thành"]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", {
									className: "form-hint",
									children: "Cần chẩn đoán, xử lý, kiểm tra và xác nhận từ khách hàng trước khi hoàn thành."
								})
							]
						})
					] })
				] }) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
					tab === "Trang chủ" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-greeting",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "THỨ HAI, 28 THÁNG 9" }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("h1", { children: [
									"Chào buổi sáng,",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("br", {}),
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("em", { children: [technician.name.split(" ").slice(-1)[0], "."] })
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [
									"Hôm nay bạn có",
									" ",
									mine.filter((t) => !["CLOSED", "RESOLVED"].includes(t.status)).length,
									" công việc cần theo dõi."
								] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-stat-grid",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "primary-mobile-stat",
									children: [
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Công việc hôm nay" }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: mine.length }),
										/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Đang chờ và được giao" })
									]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Đang xử lý" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: mine.filter((t) => t.status === "IN_PROGRESS").length }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Công việc" })
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: "Hoàn thành" }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: tickets.filter((t) => t.status === "CLOSED").length }),
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "Tháng này" })
								] })
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-section-heading",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "CÔNG VIỆC" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Cần xử lý" })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
								variant: "ghost",
								onClick: () => setTab("Công việc"),
								children: ["Xem tất cả ", /* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 16 })]
							})]
						}),
						mine.slice(0, 3).map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(JobCard, {
							ticket: t,
							open: () => select(t)
						}, t.id))
					] }),
					tab === "Công việc" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
						className: "mobile-page-title",
						children: [
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "QUẢN LÝ CÔNG VIỆC" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Công việc của tôi" }),
							/* @__PURE__ */ (0, import_jsx_runtime.jsx)("p", { children: "Tiếp nhận và theo dõi sự cố hiện trường." })
						]
					}), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
						className: "mobile-list",
						children: mine.map((t) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)(JobCard, {
							ticket: t,
							open: () => select(t)
						}, t.id))
					})] }),
					tab === "Khách hàng" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "DANH BẠ" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Khách hàng" })]
						}),
						addingCustomer ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-form",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "mobile-section-heading",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "THÊM MỚI" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Khách hàng mới" })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
										variant: "ghost",
										size: "icon",
										"aria-label": "Đóng",
										onClick: () => setAddingCustomer(false),
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(X, { size: 18 })
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Họ tên",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Input, {
										value: newName,
										onChange: (e) => setNewName(e.target.value),
										placeholder: "Nguyễn Văn A"
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Số điện thoại",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Input, {
										value: newPhone,
										onChange: (e) => setNewPhone(e.target.value),
										placeholder: "09xxxxxxxx",
										inputMode: "tel"
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Địa chỉ lắp đặt",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("textarea", {
										value: newAddress,
										onChange: (e) => setNewAddress(e.target.value),
										placeholder: "Số nhà, đường, quận/huyện..."
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									className: "w-full",
									disabled: !newName.trim() || !newPhone.trim() || !newAddress.trim(),
									onClick: () => {
										addCustomer({
											name: newName.trim(),
											phone: newPhone.trim(),
											address: newAddress.trim()
										});
										setNewName("");
										setNewPhone("");
										setNewAddress("");
										setAddingCustomer(false);
									},
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Check, { size: 17 }), " Lưu khách hàng"]
								})
							]
						}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							variant: "outline",
							className: "w-full",
							onClick: () => setAddingCustomer(true),
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Plus, { size: 17 }), " Thêm khách hàng mới"]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-search",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Search, { size: 17 }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Input, {
								placeholder: "Tìm tên, mã khách hàng...",
								value: query,
								onChange: (e) => setQuery(e.target.value)
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-rows",
							children: customers.filter((c) => `${c.name} ${c.id}`.toLocaleLowerCase("vi").includes(query.toLocaleLowerCase("vi"))).slice(0, 30).map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "row-icon",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(UserRound, { size: 18 })
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: c.name }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
									c.id,
									" · ",
									c.phone
								] })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "row-end",
									children: c.ontId
								})
							] }, c.id))
						})
					] }),
					tab === "Thiết bị" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "MẠNG LƯỚI" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Thiết bị ONT" })]
						}),
						addingOnt ? /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-form",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
									className: "mobile-section-heading",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "THÊM MỚI" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: "Thiết bị ONT mới" })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Button, {
										variant: "ghost",
										size: "icon",
										"aria-label": "Đóng",
										onClick: () => setAddingOnt(false),
										children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(X, { size: 18 })
									})]
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Serial number",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Input, {
										value: newSerial,
										onChange: (e) => setNewSerial(e.target.value),
										placeholder: "ZTEG48290001"
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Model",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsx)("select", {
										value: newModel,
										onChange: (e) => setNewModel(e.target.value),
										children: [
											"ZXHN F670L",
											"HG8145V5",
											"ZXHN F6600P",
											"HG8245H"
										].map((m) => /* @__PURE__ */ (0, import_jsx_runtime.jsx)("option", {
											value: m,
											children: m
										}, m))
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("label", { children: [
									"Gán cho khách hàng",
									" ",
									/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("select", {
										value: newOntCustomer,
										onChange: (e) => setNewOntCustomer(e.target.value),
										children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("option", {
											value: "",
											children: "— Chưa gán —"
										}), customers.map((c) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("option", {
											value: c.id,
											children: [
												c.id,
												" · ",
												c.name
											]
										}, c.id))]
									})
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
									className: "w-full",
									disabled: !newSerial.trim(),
									onClick: () => {
										addOnt({
											serial: newSerial.trim(),
											model: newModel,
											customerId: newOntCustomer
										});
										setNewSerial("");
										setNewOntCustomer("");
										setAddingOnt(false);
									},
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Check, { size: 17 }), " Lưu thiết bị"]
								})
							]
						}) : /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
							variant: "outline",
							className: "w-full",
							onClick: () => setAddingOnt(true),
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Plus, { size: 17 }), " Thêm thiết bị mới"]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-search",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Search, { size: 17 }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)(Input, {
								placeholder: "Tìm ONT ID, serial...",
								value: query,
								onChange: (e) => setQuery(e.target.value)
							})]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsx)("div", {
							className: "mobile-rows",
							children: onts.filter((o) => `${o.id} ${o.serial}`.toLowerCase().includes(query.toLowerCase())).slice(0, 30).map((o) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "row-icon",
									children: /* @__PURE__ */ (0, import_jsx_runtime.jsx)(HardDrive, { size: 18 })
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: o.id }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [
									o.model,
									" · ",
									o.serial
								] })] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
									className: `status status-${o.status === "ONLINE" ? "good" : o.status === "WARNING" ? "warn" : "bad"}`,
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "status-dot" }), statusLabels[o.status]]
								})
							] }, o.id))
						})
					] }),
					tab === "Cá nhân" && /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(import_jsx_runtime.Fragment, { children: [
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-page-title",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: "TÀI KHOẢN" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("h1", { children: "Cá nhân" })]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "profile-block",
							children: [
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
									className: "profile-avatar",
									children: "KT"
								}),
								/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h2", { children: technician.name }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [
									technician.id,
									" · ",
									technician.area
								] }),
								/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", {
									className: "status status-good",
									children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { className: "status-dot" }), "Sẵn sàng"]
								})
							]
						}),
						/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
							className: "mobile-rows",
							children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Wrench, { size: 19 }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Công việc đang xử lý" }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("small", { children: [mine.filter((t) => t.status === "IN_PROGRESS").length, " ticket"] })] })] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Clock3, { size: 19 }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: "Hoạt động gần nhất" }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("small", { children: technician.lastActive })] })] })]
						})
					] })
				] })
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("nav", {
				className: "mobile-bottom-nav",
				children: tabs.map(({ name, icon: Icon }) => /* @__PURE__ */ (0, import_jsx_runtime.jsxs)(Button, {
					variant: "ghost",
					className: tab === name ? "active" : "",
					onClick: () => {
						setTab(name);
						if (sp.ticket) setJob(null);
						setQuery("");
					},
					children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Icon, { size: 21 }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: name })]
				}, name))
			})
		]
	});
}
function JobCard({ ticket: t, open }) {
	const c = customerFor(t.customerId);
	return /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
		className: "job-card",
		onClick: open,
		role: "button",
		tabIndex: 0,
		onKeyDown: (e) => e.key === "Enter" && open(),
		children: [
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "job-card-top",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", { children: t.id }), /* @__PURE__ */ (0, import_jsx_runtime.jsx)("span", {
					className: `job-priority ${t.priority === "Cao" ? "high" : ""}`,
					children: t.priority === "Cao" ? "Ưu tiên cao" : t.priority
				})]
			}),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("h3", { children: t.issue }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsx)("strong", { children: c?.name }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("p", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(MapPin, { size: 14 }), c?.address] }),
			/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("div", {
				className: "job-card-bottom",
				children: [/* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [/* @__PURE__ */ (0, import_jsx_runtime.jsx)(Clock3, { size: 14 }), " ETA 30 phút"] }), /* @__PURE__ */ (0, import_jsx_runtime.jsxs)("span", { children: [
					statusLabels[t.status],
					" ",
					/* @__PURE__ */ (0, import_jsx_runtime.jsx)(ArrowRight, { size: 15 })
				] })]
			})
		]
	});
}
//#endregion
export { TechnicianApp as component };
