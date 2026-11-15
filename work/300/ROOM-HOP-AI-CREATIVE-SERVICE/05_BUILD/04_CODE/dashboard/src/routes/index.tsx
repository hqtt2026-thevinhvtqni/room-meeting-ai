import { createFileRoute, Link } from "@tanstack/react-router";
import { ArrowRight, Image as ImageIcon, Film, Layers, Wand2, LayoutGrid } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DemoBanner, DemoTag } from "@/components/w300/status";
import { Logo } from "@/components/w300/shell";
import perfume from "@/assets/demo-perfume.svg";
import city from "@/assets/demo-city.svg";
import abstractImg from "@/assets/demo-abstract.svg";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "W300 — Dịch vụ sáng tạo ảnh & video AI | ROOM-HOP" },
      {
        name: "description",
        content:
          "Đặt yêu cầu tạo ảnh, ghép ảnh, video, image-to-video và storyboard. Bản demo — backend chưa kết nối.",
      },
      { property: "og:title", content: "W300 — ROOM-HOP AI Creative Service" },
      { property: "og:description", content: "Cổng đặt sản xuất ảnh & video AI (bản demo)." },
    ],
  }),
  component: Landing,
});

const services = [
  { icon: ImageIcon, vi: "Tạo ảnh", en: "Image generation" },
  { icon: Layers, vi: "Chỉnh sửa & ghép ảnh", en: "Edit & compositing" },
  { icon: Film, vi: "Tạo video", en: "Video generation" },
  { icon: Wand2, vi: "Ảnh thành video", en: "Image-to-video" },
  { icon: LayoutGrid, vi: "Storyboard", en: "Storyboard" },
];

function Landing() {
  return (
    <div className="min-h-screen bg-hero">
      <DemoBanner />
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <Logo />
        <nav className="flex items-center gap-2 text-sm">
          <Link to="/docs" className="px-3 py-2 text-muted-foreground hover:text-foreground">
            Tài liệu MCP
          </Link>
          <Button asChild size="sm" variant="hero">
            <Link to="/signin">Đăng nhập demo</Link>
          </Button>
        </nav>
      </header>
      <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 py-14 lg:grid-cols-2 lg:py-24">
        <div>
          <span className="rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs text-primary">
            MCP-based creative service · Planned
          </span>
          <h1 className="mt-5 text-4xl font-bold leading-tight sm:text-5xl">
            Sản xuất <span className="text-gradient">ảnh & video AI</span> cho thương hiệu của bạn
          </h1>
          <p className="mt-5 max-w-lg text-muted-foreground">
            Gửi yêu cầu, theo dõi tiến độ và nhận bàn giao tại một nơi. Đây là bản xem trước giao
            diện — chưa có job thật nào được thực thi.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button asChild variant="hero" size="lg">
              <Link to="/signin">
                Bắt đầu (demo) <ArrowRight />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to="/docs">Xem tài liệu</Link>
            </Button>
          </div>
        </div>
        <div className="relative grid grid-cols-2 gap-3">
          {[perfume, city, abstractImg].map((src, i) => (
            <div
              key={src}
              className={`relative overflow-hidden rounded-2xl border border-border ${i === 0 ? "col-span-2 aspect-[16/9]" : "aspect-square"}`}
            >
              <img
                src={src}
                alt="Ảnh minh họa demo"
                width={1024}
                height={768}
                className="size-full object-cover"
                loading={i ? "lazy" : undefined}
              />
              <DemoTag className="absolute left-2 top-2 bg-background/80" />
            </div>
          ))}
        </div>
      </section>
      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
          {services.map((s) => (
            <div key={s.en} className="surface p-5">
              <s.icon className="size-5 text-primary" />
              <div className="mt-3 font-semibold">{s.vi}</div>
              <div className="text-xs text-muted-foreground">{s.en} · planned</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
