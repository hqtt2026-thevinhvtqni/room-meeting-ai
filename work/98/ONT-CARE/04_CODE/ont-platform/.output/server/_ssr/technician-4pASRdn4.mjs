import { c as parseDeepLink } from "./deep-links-BPsBDoll.mjs";
import { _ as createFileRoute, g as lazyRouteComponent } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/technician-4pASRdn4.js
var $$splitComponentImporter = () => import("./technician-DfTl0Io0.mjs");
var Route = createFileRoute("/technician")({
	head: () => ({ meta: [
		{ title: "App Thợ | ONT Platform" },
		{
			name: "description",
			content: "Công việc hiện trường, chẩn đoán ONT và xác nhận hoàn thành cho kỹ thuật viên."
		},
		{
			property: "og:title",
			content: "App Thợ — ONT Platform"
		},
		{
			property: "og:description",
			content: "Tiếp nhận và xử lý sự cố mạng ngay tại hiện trường."
		},
		{
			property: "og:type",
			content: "website"
		},
		{
			name: "twitter:card",
			content: "summary_large_image"
		}
	] }),
	validateSearch: parseDeepLink,
	component: lazyRouteComponent($$splitComponentImporter, "component")
});
//#endregion
export { Route as t };
