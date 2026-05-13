"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Project = {
  id: string;
  name: string;
  description: string | null;
  runtime: string;
  transport: string;
};

export default function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) { setError("Sign in first."); return; }
    (async () => {
      try {
        const p = await apiJson<Project>(`/api/v1/projects/${id}`, { token });
        setProject(p);
      } catch {
        setError("Project not found or inaccessible.");
      }
    })();
  }, [id]);

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Project</p>
          <h1 className="text-2xl font-semibold tracking-tight">{project?.name ?? "…"}</h1>
          <p className="mt-1 text-sm text-zinc-400">{project?.description ?? "No description"}</p>
          {project && (
            <p className="mt-1 text-xs text-zinc-500">{project.runtime} · {project.transport}</p>
          )}
        </div>
        <StudioNav />
      </header>

      {error && <p className="text-sm text-amber-400">{error}</p>}

      {project && (
        <div className="flex flex-wrap gap-3 text-sm">
          <Link
            href={`/projects/${project.id}/design`}
            className="rounded-md bg-zinc-100 px-4 py-2 font-medium text-zinc-950"
          >
            Visual designer
          </Link>
          <Link
            href={`/projects/${project.id}/test`}
            className="rounded-md border border-zinc-700 px-4 py-2 text-zinc-200"
          >
            Testing console
          </Link>
          <Link href="/projects" className="rounded-md border border-zinc-800 px-4 py-2 text-zinc-400">
            All projects
          </Link>
        </div>
      )}
    </main>
  );
}
