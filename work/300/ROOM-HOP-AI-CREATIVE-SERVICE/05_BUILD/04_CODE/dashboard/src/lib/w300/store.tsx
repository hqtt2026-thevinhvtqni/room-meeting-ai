import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { demoJobs } from "./demo-data";
import type { Job, Role } from "./types";

interface Ctx { role: Role; setRole: (r: Role) => void; jobs: Job[]; addJob: (j: Job) => void; updateJob: (id: string, p: Partial<Job>) => void; hydrated: boolean }
const C = createContext<Ctx | null>(null);
const KEY = "w300-demo-role";

export function W300Provider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<Role>("guest");
  const [hydrated, setHydrated] = useState(false);
  const [jobs, setJobs] = useState<Job[]>(demoJobs);
  useEffect(() => {
    const r = localStorage.getItem(KEY) as Role | null;
    if (r === "customer" || r === "internal") setRoleState(r);
    setHydrated(true);
  }, []);
  const setRole = (r: Role) => { setRoleState(r); if (r === "guest") localStorage.removeItem(KEY); else localStorage.setItem(KEY, r); };
  return (
    <C.Provider value={{ role, setRole, jobs, hydrated,
      addJob: (j) => setJobs((s) => [j, ...s]),
      updateJob: (id, p) => setJobs((s) => s.map((j) => (j.id === id ? { ...j, ...p, updatedAt: new Date().toISOString() } : j))) }}>
      {children}
    </C.Provider>
  );
}
export function useW300() { const c = useContext(C); if (!c) throw new Error("W300Provider missing"); return c; }