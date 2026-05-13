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
  const params = useParams<{ id: string }>();
  const id = params.id;
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) {
      setError("Sign in first.");
      return;
    }
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
          <p className="mt-2 text-sm text-zinc-400">{project?.description ?? "No description"}</p>
          <p className="mt-2 text-xs text-zinc-500">
            {project ? `${project.runtime} · ${project.transport}` : ""}
          </p>
        </div>
        <StudioNav />
      </header>

      {error ? <p className="text-sm text-amber-400">{error}</p> : null}

      {project ? (
        <div className="flex flex-wrap gap-3 text-sm">
          <Link
            className="rounded-md bg-zinc-100 px-4 py-2 font-medium text-zinc-950"
            href={`/projects/${project.id}/design`}
          >
            Visual designer
          </Link>
          <Link
            className="rounded-md border border-zinc-700 px-4 py-2 text-zinc-200"
            href={`/projects/${project.id}/test`}
          >
            Testing console
          </Link>
          <Link className="rounded-md border border-zinc-800 px-4 py-2 text-zinc-400" href="/projects">
            All projects
          </Link>
        </div>
      ) : null}
    </main>
  );
}
