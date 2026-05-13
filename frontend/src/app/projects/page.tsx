"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Project = {
  id: string;
  name: string;
  runtime: string;
  transport: string;
  updated_at: string;
};

export default function ProjectsPage() {
  const [items, setItems] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) {
      setError("Sign in to view projects.");
      return;
    }
    (async () => {
      try {
        const data = await apiJson<{ items: Project[] }>("/api/v1/projects?page=1&page_size=50", {
          token,
        });
        setItems(data.items);
      } catch {
        setError("Could not load projects.");
      }
    })();
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
          <p className="mt-1 text-sm text-zinc-400">
            Phase 2 studio list — open a project for the designer and testing console.
          </p>
        </div>
        <StudioNav />
      </header>

      {error ? <p className="text-sm text-amber-400">{error}</p> : null}

      <ul className="divide-y divide-zinc-800 rounded-lg border border-zinc-800">
        {items.map((p) => (
          <li key={p.id} className="flex flex-col gap-1 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <Link href={`/projects/${p.id}`} className="font-medium text-zinc-100 hover:underline">
                {p.name}
              </Link>
              <p className="text-xs text-zinc-500">
                {p.runtime} · {p.transport}
              </p>
            </div>
            <Link
              className="text-sm text-zinc-400 hover:text-zinc-200"
              href={`/projects/${p.id}/design`}
            >
              Open designer →
            </Link>
          </li>
        ))}
        {!items.length && !error ? (
          <li className="px-4 py-6 text-sm text-zinc-500">No projects yet. Create one via the API or templates gallery.</li>
        ) : null}
      </ul>
    </main>
  );
}
