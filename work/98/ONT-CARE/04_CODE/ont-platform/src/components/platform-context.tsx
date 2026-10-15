import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import {
  customers as initialCustomers,
  onts as initialOnts,
  initialTickets,
  type Customer,
  type Ont,
  type Ticket,
  type TicketStatus,
} from "@/lib/ont-data";

type Platform = {
  tickets: Ticket[];
  customers: Customer[];
  onts: Ont[];
  createTicket: (customerId: string, ontId: string, issue: string) => Ticket;
  updateTicket: (id: string, patch: Partial<Ticket>) => void;
  addCustomer: (data: { name: string; phone: string; address: string }) => Customer;
  addOnt: (data: { serial: string; model: string; customerId: string }) => Ont;
  message: string;
  notify: (value: string) => void;
};
const Context = createContext<Platform | null>(null);
const pad = (n: number, size = 3) => String(n).padStart(size, "0");
export function PlatformProvider({ children }: { children: ReactNode }) {
  const [tickets, setTickets] = useState<Ticket[]>(initialTickets);
  const [customers, setCustomers] = useState<Customer[]>(initialCustomers);
  const [onts, setOnts] = useState<Ont[]>(initialOnts);
  const [message, setMessage] = useState("");
  const createTicket = (customerId: string, ontId: string, issue: string) => {
    const ticket: Ticket = {
      id: `TK-${String(2431 + tickets.length - 30).padStart(4, "0")}`,
      customerId,
      ontId,
      issue,
      priority: "Trung bình",
      status: "OPEN" as TicketStatus,
      created: "Vừa xong",
      updated: "Vừa xong",
    };
    setTickets((prev) => [ticket, ...prev]);
    setMessage(`Đã tạo yêu cầu ${ticket.id}`);
    return ticket;
  };
  const updateTicket = (id: string, patch: Partial<Ticket>) =>
    setTickets((prev) =>
      prev.map((t) => (t.id === id ? { ...t, ...patch, updated: "Vừa xong" } : t)),
    );
  useEffect(() => {
    if (!message) return;
    const t = setTimeout(() => setMessage(""), 3000);
    return () => clearTimeout(t);
  }, [message]);
  const addCustomer = (data: { name: string; phone: string; address: string }) => {
    const id = `KH-${pad(customers.length + 1)}`;
    const customer: Customer = {
      id,
      name: data.name,
      phone: data.phone,
      address: data.address,
      ontId: "",
    };
    setCustomers((prev) => [...prev, customer]);
    setMessage(`Đã thêm khách hàng ${id} — ${data.name}`);
    return customer;
  };
  const addOnt = (data: { serial: string; model: string; customerId: string }) => {
    const id = `ONT-${pad(onts.length + 1)}`;
    const ont: Ont = {
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
      ping: 0,
    };
    setOnts((prev) => [...prev, ont]);
    if (data.customerId)
      setCustomers((prev) => prev.map((c) => (c.id === data.customerId ? { ...c, ontId: id } : c)));
    setMessage(`Đã thêm thiết bị ${id} (${data.serial})`);
    return ont;
  };
  return (
    <Context.Provider
      value={{
        tickets,
        customers,
        onts,
        createTicket,
        updateTicket,
        addCustomer,
        addOnt,
        message,
        notify: setMessage,
      }}
    >
      {children}
      {message && (
        <div
          role="status"
          className="fixed bottom-5 right-5 z-50 max-w-sm rounded-md border border-border bg-foreground px-4 py-3 text-sm text-background shadow-lg"
          onClick={() => setMessage("")}
        >
          {message}
        </div>
      )}
    </Context.Provider>
  );
}
export function usePlatform() {
  const value = useContext(Context);
  if (!value) throw new Error("Platform provider missing");
  return value;
}
