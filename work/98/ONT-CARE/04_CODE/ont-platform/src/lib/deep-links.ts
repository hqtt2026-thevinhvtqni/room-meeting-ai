// Shared search-param parsing for deep links (?ont=ONT-001, ?ticket=TK-2401, ?tab=LAN).
export type DeepLinkSearch = {
  ont?: string | undefined;
  ticket?: string | undefined;
  tab?: string | undefined;
};

const clean = (value: unknown) =>
  typeof value === "string" && value.trim() ? value.trim().toUpperCase().slice(0, 32) : undefined;

export function parseDeepLink(raw: Record<string, unknown>): DeepLinkSearch {
  const out: DeepLinkSearch = {};
  const ont = clean(raw["ont"]);
  const ticket = clean(raw["ticket"]);
  if (ont) out.ont = ont;
  if (ticket) out.ticket = ticket;
  if (typeof raw["tab"] === "string" && raw["tab"].trim()) out.tab = raw["tab"].trim().slice(0, 32);
  return out;
}

export const ontTabs = [
  "Overview",
  "Internet",
  "Wi-Fi",
  "LAN",
  "Optical / PON",
  "Devices",
  "Tests",
  "Events",
  "Remote Actions",
];
