"use client";

import { useEffect, useState } from "react";

import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Template = {
  id: string;
  name: string;
  description: string | null;
  category: string | null;
};

export default function TemplatesGalleryPage() {
  const [items, setItems] = useState<Template[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const rows = await apiJson<Template[]>("/api/v1/templates?page=1&page_size=50");
        setItems(rows);
      } catch {
        setError("Could not load templates.");
      }
    })();
  }, []);

  async function instantiate(templateId: string) {
    const token = getStoredAccessToken();
    if (!token) {
      setError("Sign in to create a project from a template.");
      return;
    }
    setBusy(templateId);
    setError(null);
    try {
      const project = await apiJson<{ id: string }>("/api/v1/projects/from-template", {
        method: "POST",
        token,
        body: JSON.stringify({ template_id: templateId }),
      });
      window.location.href = `/projects/${project.id}`;
    } catch {
      setError("Instantiation failed.");
    } finally {
      setBusy(null);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Template gallery</h1>
          <p className="mt-1 text-sm text-zinc-400">
            Phase 6 — instantiate a starter project (requires authentication).
          </p>
        </div>
        <StudioNav />
      </header>

      {error ? <p className="text-sm text-amber-400">{error}</p> : null}

      <ul className="divide-y divide-zinc-800 rounded-lg border border-zinc-800">
        {items.map((t) => (
          <li key={t.id} className="flex flex-col gap-2 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-medium text-zinc-100">{t.name}</p>
              <p className="text-sm text-zinc-500">{t.description}</p>
              <p className="text-xs text-zinc-600">{t.category}</p>
            </div>
            <button
              type="button"
              disabled={busy === t.id}
              onClick={() => instantiate(t.id)}
              className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 disabled:opacity-50"
            >
              {busy === t.id ? "Creating…" : "Use template"}
            </button>
          </li>
        ))}
        {!items.length && !error ? (
          <li className="px-4 py-6 text-sm text-zinc-500">No templates yet.</li>
        ) : null}
      </ul>

      <p className="text-xs text-zinc-600">
        Want more control? Use the REST API per <code className="rounded bg-zinc-900 px-1">docs/API_SPEC.md</code>.
      </p>
    </main>
  );
}
