import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { demoJobs } from "./demo-data";
import type { Job, Role } from "./types";

/** Partial patch that also allows explicitly clearing optional fields (exactOptionalPropertyTypes). */
export type JobPatch = { [K in keyof Job]?: Job[K] | undefined };

interface Ctx {
  role: Role;
  setRole: (r: Role) => void;
  jobs: Job[];
  addJob: (j: Job) => void;
  updateJob: (id: string, p: JobPatch) => void;
  resetDemoJobs: () => void;
  hydrated: boolean;
}
const C = createContext<Ctx | null>(null);
const KEY = "w300-demo-role";
const JOBS_KEY = "w300-demo-jobs";

export function W300Provider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<Role>("guest");
  const [hydrated, setHydrated] = useState(false);
  const [jobs, setJobs] = useState<Job[]>(demoJobs);
  useEffect(() => {
    try {
      const r = localStorage.getItem(KEY) as Role | null;
      if (r === "customer" || r === "internal") setRoleState(r);
      const raw = localStorage.getItem(JOBS_KEY);
      if (raw) {
        const saved = JSON.parse(raw) as Job[];
        if (Array.isArray(saved))
          setJobs([...saved, ...demoJobs.filter((d) => !saved.some((s) => s.id === d.id))]);
      }
    } catch {
      /* corrupted storage: fall back to demo data */
    }
    setHydrated(true);
  }, []);
  useEffect(() => {
    if (!hydrated) return;
    try {
      localStorage.setItem(JOBS_KEY, JSON.stringify(jobs.filter((j) => j.id.startsWith("demo-"))));
    } catch {
      /* quota exceeded: ignore */
    }
  }, [jobs, hydrated]);
  const setRole = (r: Role) => {
    setRoleState(r);
    if (r === "guest") localStorage.removeItem(KEY);
    else localStorage.setItem(KEY, r);
  };
  return (
    <C.Provider
      value={{
        role,
        setRole,
        jobs,
        hydrated,
        addJob: (j) => setJobs((s) => [j, ...s]),
        // Apply patch key-by-key: spreading JobPatch into Job would type every optional
        // prop as "T | undefined", which violates exactOptionalPropertyTypes on Job.
        updateJob: (id, p) =>
          setJobs((s) =>
            s.map((j) => {
              if (j.id !== id) return j;
              const next: Job = { ...j, updatedAt: new Date().toISOString() };
              for (const key of Object.keys(p) as Array<keyof Job>) {
                const v = p[key];
                if (v === undefined) delete (next as unknown as Record<string, unknown>)[key];
                else (next as unknown as Record<string, unknown>)[key] = v;
              }
              return next;
            }),
          ),
        resetDemoJobs: () => setJobs(demoJobs),
      }}
    >
      {children}
    </C.Provider>
  );
}
export function useW300() {
  const c = useContext(C);
  if (!c) throw new Error("W300Provider missing");
  return c;
}
