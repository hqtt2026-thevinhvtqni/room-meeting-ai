import { c as parseDeepLink } from "./deep-links-BPsBDoll.mjs";
import { _ as createFileRoute, g as lazyRouteComponent } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/routes-7F_TZHJU.js
var $$splitComponentImporter = () => import("./routes-CymGhkhl.mjs");
var Route = createFileRoute("/")({
	head: () => ({ meta: [
		{ title: "Tổng quan vận hành | ONT Platform" },
		{
			name: "description",
			content: "Trung tâm quản lý, giám sát ONT và điều phối sự cố Internet."
		},
		{
			property: "og:title",
			content: "ONT Platform — Tổng quan vận hành"
		},
		{
			property: "og:description",
			content: "Giám sát ONT, khách hàng, sức khỏe mạng và sự cố trên một nền tảng."
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
