"""End-to-end checks for ONT/ticket deep links across the three apps.
Run: python3 e2e/deep_links_e2e.py  (dev server on BASE, default http://localhost:8080)
"""
import asyncio, os, sys
from playwright.async_api import async_playwright

BASE = os.environ.get("BASE", "http://localhost:8080")
NF = "LIÊN KẾT KHÔNG HỢP LỆ"

# (name, path, must_contain, must_not_contain)
CASES = [
    ("dashboard: valid ONT", "/?ont=ONT-001", ["Chi tiết ONT", "ONT-001"], [NF]),
    ("dashboard: ONT tab LAN", "/?ont=ONT-005&tab=LAN", ["ONT-005"], [NF]),
    ("dashboard: bad tab falls back", "/?ont=ONT-005&tab=Hack", ["ONT-005"], [NF]),
    ("dashboard: lowercase ONT id", "/?ont=ont-010", ["ONT-010"], [NF]),
    ("dashboard: invalid ONT", "/?ont=ONT-999", [NF, "ONT ONT-999"], []),
    ("dashboard: valid ticket", "/?ticket=TK-2401", ["Chi tiết ticket", "TK-2401"], [NF]),
    ("dashboard: invalid ticket", "/?ticket=TK-0000", [NF, "Ticket TK-0000"], []),
    ("dashboard: garbage ticket", "/?ticket=%3Cscript%3E", [NF], []),
    ("technician: valid ticket", "/technician?ticket=TK-2402", ["TK-2402"], [NF]),
    ("technician: invalid ticket", "/technician?ticket=TK-9999", [NF, "TK-9999"], []),
    # Access control: TK-2401 belongs to another customer, demo customer is KH-001
    ("customer: other customer's ticket blocked", "/customer?ticket=TK-2401", [NF, "không thuộc tài khoản"], ["Kỹ thuật viên:"]),
    ("customer: invalid ticket", "/customer?ticket=TK-9999", [NF], []),
    ("404: unknown route", "/khong-ton-tai", [], []),
]

async def main():
    failures = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for device, vp in [("desktop", {"width": 1280, "height": 1800}), ("mobile", {"width": 390, "height": 844})]:
            ctx = await browser.new_context(viewport=vp)
            page = await ctx.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            for name, path, yes, no in CASES:
                resp = await page.goto(BASE + path, wait_until="networkidle")
                text = await page.inner_text("body")
                problems = [f"missing '{s}'" for s in yes if s not in text]
                problems += [f"unexpected '{s}'" for s in no if s in text]
                if name.startswith("404") and resp and resp.status != 404:
                    problems.append(f"status {resp.status}")
                elif not name.startswith("404") and resp and resp.status >= 400:
                    problems.append(f"status {resp.status}")
                tag = f"[{device}] {name}"
                print(("FAIL " if problems else "ok   ") + tag, "; ".join(problems))
                if problems: failures.append(tag)

            # Cross-app flow: technician job -> dashboard ticket -> ONT detail
            await page.goto(BASE + "/technician?ticket=TK-2402", wait_until="networkidle")
            await page.get_by_text("Xem ticket trên Dashboard").click()
            await page.wait_for_url("**/?ticket=TK-2402")
            await page.goto(BASE + "/technician?ticket=TK-2402", wait_until="networkidle")
            await page.get_by_text("Mở chi tiết ONT").click()
            await page.wait_for_url("**/?ont=ONT-*")
            ok = NF not in await page.inner_text("body")
            print(("ok   " if ok else "FAIL ") + f"[{device}] cross-app technician -> dashboard")
            if not ok: failures.append(f"[{device}] cross-app")

            # Recovery button from not-found state returns to list
            await page.goto(BASE + "/technician?ticket=TK-9999", wait_until="networkidle")
            await page.get_by_role("button", name="Về danh sách công việc").click()
            ok = "ticket=" not in page.url
            print(("ok   " if ok else "FAIL ") + f"[{device}] technician not-found recovery")
            if not ok: failures.append(f"[{device}] recovery")

            if errors:
                failures.append(f"[{device}] page errors: {errors[:3]}")
                print("FAIL page errors", errors[:3])
            await ctx.close()
        await browser.close()
    print(f"\n{len(failures)} failure(s)")
    sys.exit(1 if failures else 0)

asyncio.run(main())
