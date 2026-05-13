"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Template = {
  id: string;
  name: string;
  description: string | null;
  category: string | null;
  use_count: number;
  config: { runtime?: string; transport?: string };
};

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) { setError("Sign in to browse templates."); return; }
    (async () => {
      try {
        const data = await apiJson<Template[]>("/api/v1/templates", { token });
        setTemplates(data);
      } catch {
        setError("Could not load templates.");
      }
    })();
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Library</p>
          <h1 className="text-2xl font-semibold tracking-tight">Templates</h1>
        </div>
        <StudioNav />
      </header>
      {error && <p className="text-sm text-amber-400">{error}</p>}
      {templates.length === 0 && !error && (
        <p className="text-sm text-zinc-500">No templates yet.</p>
      )}
      <ul className="grid gap-4 sm:grid-cols-2">
        {templates.map((t) => (
          <li key={t.id} className="rounded-lg border border-zinc-800 p-4">
            <p className="font-medium text-zinc-100">{t.name}</p>
            {t.description && <p className="mt-1 text-sm text-zinc-400">{t.description}</p>}
            <div className="mt-2 flex gap-2 text-xs text-zinc-500">
              {t.category && <span>{t.category}</span>}
              {t.config.runtime && <span>{t.config.runtime}</span>}
            </div>
            <p className="mt-1 text-xs text-zinc-600">Used {t.use_count} times</p>
          </li>
        ))}
      </ul>
      <Link href="/projects" className="self-start text-sm text-zinc-400 hover:text-white">
        ← Projects
      </Link>
    </main>
  );
}
