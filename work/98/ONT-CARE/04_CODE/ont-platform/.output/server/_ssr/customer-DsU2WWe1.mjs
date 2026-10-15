import { c as parseDeepLink } from "./deep-links-BPsBDoll.mjs";
import { _ as createFileRoute, g as lazyRouteComponent } from "../_libs/@tanstack/react-router+[...].mjs";
//#region node_modules/.nitro/vite/services/ssr/assets/customer-DsU2WWe1.js
var $$splitComponentImporter = () => import("./customer-DokNFCei.mjs");
var Route = createFileRoute("/customer")({
	head: () => ({ meta: [
		{ title: "App Khách | ONT Platform" },
		{
			name: "description",
			content: "Kiểm tra Internet, Wi-Fi, thiết bị và gửi yêu cầu hỗ trợ."
		},
		{
			property: "og:title",
			content: "App Khách — ONT Platform"
		},
		{
			property: "og:description",
			content: "Theo dõi kết nối và nhận hỗ trợ Internet dễ dàng."
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
