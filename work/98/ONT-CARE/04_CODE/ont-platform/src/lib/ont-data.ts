export type OntStatus = 'ONLINE' | 'WARNING' | 'OFFLINE' | 'UNKNOWN';
export type TicketStatus = 'OPEN' | 'ASSIGNED' | 'IN_PROGRESS' | 'WAITING_CUSTOMER' | 'RESOLVED' | 'CLOSED';
export type Customer = { id: string; name: string; phone: string; address: string; ontId: string };
export type Ont = { id: string; serial: string; model: string; firmware: string; customerId: string; status: OntStatus; optical: number; uptime: string; lastSeen: string; wan: string; wifi: string; speed: number; ping: number };
export type Technician = { id: string; name: string; area: string; status: 'AVAILABLE' | 'BUSY' | 'OFFLINE'; lastActive: string };
export type Ticket = { id: string; customerId: string; ontId: string; issue: string; priority: 'Cao' | 'Trung bình' | 'Thấp'; status: TicketStatus; technicianId?: string | undefined; created: string; updated: string; diagnosis?: string; action?: string; testResult?: string; confirmed?: boolean };
export type LanDevice = { id: string; ontId: string; name: string; ip: string; mac: string; connection: string; online: boolean; lastSeen: string };

const first = ['Nguyễn Minh', 'Trần Thị', 'Lê Văn', 'Phạm Hoàng', 'Đỗ Thu', 'Võ Thanh', 'Bùi Ngọc', 'Hoàng Anh', 'Mai Quốc', 'Đặng Hải'];
const last = ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Hùng', 'Lan', 'Minh', 'Phong', 'Trang'];
const streets = ['Nguyễn Huệ', 'Lê Lợi', 'Trần Hưng Đạo', 'Điện Biên Phủ', 'Phan Xích Long', 'Hoàng Văn Thụ'];
const areas = ['Quận 1', 'Quận 3', 'Bình Thạnh', 'Phú Nhuận', 'Thủ Đức'];
const pad = (n: number, size = 3) => String(n).padStart(size, '0');
export const customers: Customer[] = Array.from({ length: 100 }, (_, i) => ({
  id: `KH-${pad(i + 1)}`, name: `${(first[i % 10] ?? 'Nguyễn Minh')} ${(last[Math.floor(i / 10)] ?? 'An')}`, phone: `09${String(10000000 + i * 78391).slice(0, 8)}`,
  address: `${12 + i * 3} ${(streets[i % streets.length] ?? 'Nguyễn Huệ')}, ${(areas[i % areas.length] ?? 'Quận 1')}, TP. HCM`, ontId: `ONT-${pad(i + 1)}`,
}));
export const onts: Ont[] = Array.from({ length: 100 }, (_, i) => ({
  id: `ONT-${pad(i + 1)}`, serial: `ZTEG${String(48290001 + i * 17)}`, model: (['ZXHN F670L', 'HG8145V5', 'ZXHN F6600P', 'HG8245H'][i % 4] ?? 'ZXHN F670L'), firmware: `V${(i % 3) + 1}.2.${i % 7}`,
  customerId: `KH-${pad(i + 1)}`, status: i < 80 ? 'ONLINE' : i < 92 ? 'WARNING' : 'OFFLINE',
  optical: Number((i < 80 ? -18.2 - (i % 8) * .5 : i < 92 ? -26.1 - (i % 4) * .6 : -30.2).toFixed(1)),
  uptime: i < 80 ? `${2 + i % 17} ngày ${i % 23} giờ` : i < 92 ? `${i % 8} giờ` : '—',
  lastSeen: i < 80 ? 'Vừa xong' : i < 92 ? `${3 + i % 20} phút trước` : `${1 + i % 7} giờ trước`,
  wan: i >= 92 ? 'Mất kết nối' : 'Đã kết nối', wifi: i >= 92 ? 'Không khả dụng' : 'Hoạt động', speed: i < 80 ? 110 + i % 55 : i < 92 ? 24 + i % 18 : 0, ping: i < 80 ? 10 + i % 14 : i < 92 ? 68 + i % 34 : 0,
}));
export const technicians: Technician[] = Array.from({ length: 15 }, (_, i) => ({ id: `KT-${pad(i + 1)}`, name: `${(first[(i + 3) % 10] ?? 'Nguyễn Minh')} ${(last[(i + 2) % 10] ?? 'An')}`, area: (areas[i % 5] ?? 'Quận 1'), status: i < 6 ? 'BUSY' : i < 13 ? 'AVAILABLE' : 'OFFLINE', lastActive: i < 13 ? 'Vừa xong' : '2 giờ trước' }));
const issues = ['Internet chậm', 'Mất kết nối Internet', 'Wi-Fi yếu', 'Không kết nối được', 'Thiết bị không vào mạng', 'Tín hiệu quang yếu'];
export const initialTickets: Ticket[] = Array.from({ length: 30 }, (_, i) => ({
  id: `TK-${pad(2401 + i, 4)}`, customerId: `KH-${pad((i * 7 + 80) % 100 + 1)}`, ontId: `ONT-${pad((i * 7 + 80) % 100 + 1)}`,
  issue: (issues[i % issues.length] ?? 'Internet chậm'), priority: i % 6 === 0 ? 'Cao' : i % 3 === 0 ? 'Thấp' : 'Trung bình',
  status: (['OPEN', 'ASSIGNED', 'IN_PROGRESS', 'RESOLVED', 'CLOSED'] as TicketStatus[])[i % 5] ?? 'OPEN',
  technicianId: i % 5 !== 0 ? `KT-${pad(i % 15 + 1)}` : undefined, created: `28/09/2026 · ${pad(8 + i % 10, 2)}:${pad(i * 7 % 60, 2)}`,
  updated: `${i % 5 + 1} phút trước`,
}));
export const lanDevices: LanDevice[] = Array.from({ length: 200 }, (_, i) => ({
  id: `DEV-${pad(i + 1)}`, ontId: `ONT-${pad(Math.floor(i / 2) + 1)}`, name: ['iPhone', 'Smart TV', 'Laptop', 'Camera IP', 'Máy tính bảng'][i % 5] ?? 'Thiết bị',
  ip: `192.168.1.${10 + i % 200}`, mac: `A4:6B:BC:${pad(i % 99, 2)}:${pad((i * 3) % 99, 2)}:${pad((i * 7) % 99, 2)}`,
  connection: i % 4 === 0 ? 'LAN' : i % 3 === 0 ? 'Wi-Fi 2.4GHz' : 'Wi-Fi 5GHz', online: i % 9 !== 0, lastSeen: i % 9 !== 0 ? 'Vừa xong' : '1 giờ trước',
}));
export const statusLabels: Record<OntStatus | TicketStatus, string> = { ONLINE: 'Online', WARNING: 'Cảnh báo', OFFLINE: 'Offline', UNKNOWN: 'Chưa rõ', OPEN: 'Mới tạo', ASSIGNED: 'Đã phân công', IN_PROGRESS: 'Đang xử lý', WAITING_CUSTOMER: 'Chờ khách xác nhận', RESOLVED: 'Đã xử lý', CLOSED: 'Đã đóng' };
export const customerFor = (id: string) => customers.find(c => c.id === id);
export const ontFor = (id: string) => onts.find(o => o.id === id);
export const techFor = (id?: string) => technicians.find(t => t.id === id);
