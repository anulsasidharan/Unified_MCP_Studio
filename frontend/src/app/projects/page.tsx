"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Project = {
  id: string;
  name: string;
  description: string | null;
  runtime: string;
  transport: string;
  created_at: string;
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");
  const [runtime, setRuntime] = useState("python");

  useEffect(() => {
    load();
  }, []);

  function load() {
    const token = getStoredAccessToken();
    if (!token) { setError("Sign in first."); return; }
    (async () => {
      try {
        const data = await apiJson<Project[]>("/api/v1/projects", { token });
        setProjects(data);
      } catch {
        setError("Could not load projects.");
      }
    })();
  }

  async function onCreate(e: FormEvent) {
    e.preventDefault();
    const token = getStoredAccessToken();
    if (!token || !name.trim()) return;
    try {
      const p = await apiJson<Project>("/api/v1/projects", {
        method: "POST",
        token,
        body: JSON.stringify({ name: name.trim(), runtime, transport: "stdio" }),
      });
      setProjects((prev) => [p, ...prev]);
      setName("");
      setCreating(false);
    } catch {
      setError("Could not create project.");
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Workspace</p>
          <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
        </div>
        <StudioNav />
      </header>

      {error && <p className="text-sm text-amber-400">{error}</p>}

      {creating ? (
        <form onSubmit={onCreate} className="flex flex-wrap items-end gap-3 rounded-lg border border-zinc-800 p-4">
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-zinc-300">Name</span>
            <input
              autoFocus
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100 outline-none focus:ring-2 focus:ring-zinc-500"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-zinc-300">Runtime</span>
            <select
              value={runtime}
              onChange={(e) => setRuntime(e.target.value)}
              className="rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-zinc-100"
            >
              <option value="python">Python</option>
              <option value="typescript">TypeScript</option>
            </select>
          </label>
          <button type="submit" className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950">
            Create
          </button>
          <button type="button" onClick={() => setCreating(false)} className="text-sm text-zinc-500 hover:text-white">
            Cancel
          </button>
        </form>
      ) : (
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => setCreating(true)}
            className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950"
          >
            + New project
          </button>
          <Link
            href="/templates#instantiate"
            className="rounded-md border border-zinc-600 px-4 py-2 text-sm font-medium text-zinc-100 hover:border-zinc-400 hover:bg-zinc-900"
          >
            Start from template
          </Link>
        </div>
      )}

      {projects.length === 0 && !error && (
        <p className="text-sm text-zinc-500">
          No projects yet — create one above, or{" "}
          <Link href="/templates#instantiate" className="text-zinc-300 underline underline-offset-4 hover:text-white">
            start from a library template
          </Link>{" "}
          to open the designer with starter tools.
        </p>
      )}

      <ul className="flex flex-col gap-3">
        {projects.map((p) => (
          <li key={p.id}>
            <Link
              href={`/projects/${p.id}`}
              className="flex items-center justify-between rounded-lg border border-zinc-800 px-4 py-3 hover:border-zinc-600 hover:bg-zinc-900"
            >
              <div>
                <p className="font-medium text-zinc-100">{p.name}</p>
                <p className="text-xs text-zinc-500">{p.runtime} · {p.transport}</p>
              </div>
              <span className="text-sm text-zinc-500">→</span>
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
