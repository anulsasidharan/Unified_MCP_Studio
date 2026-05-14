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

const RUNTIME_COMMANDS: Record<string, { install: string; run: string }> = {
  python: { install: "pip install mcp", run: "python main.py" },
  typescript: { install: "npm install && npm run build", run: "node dist/index.js" },
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

  const cmds = project ? (RUNTIME_COMMANDS[project.runtime] ?? RUNTIME_COMMANDS.python) : null;

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Project</p>
          <h1 className="text-2xl font-semibold tracking-tight">{project?.name ?? "…"}</h1>
          {project?.description && (
            <p className="mt-1 text-sm text-zinc-400">{project.description}</p>
          )}
          {project && (
            <p className="mt-1 text-xs text-zinc-500">{project.runtime} · {project.transport}</p>
          )}
        </div>
        <StudioNav />
      </header>

      {error && <p className="text-sm text-amber-400">{error}</p>}

      {project && (
        <>
          {/* Action buttons */}
          <div className="flex flex-wrap gap-3 text-sm">
            <Link
              href={`/projects/${project.id}/design`}
              className="rounded-md bg-zinc-100 px-4 py-2 font-medium text-zinc-950"
            >
              Visual Designer
            </Link>
            <Link
              href={`/projects/${project.id}/design?generate=1`}
              className="rounded-md bg-blue-600 px-4 py-2 font-medium text-white"
            >
              ⚡ Generate &amp; Download
            </Link>
            <Link
              href={`/projects/${project.id}/test`}
              className="rounded-md border border-zinc-700 px-4 py-2 text-zinc-200"
            >
              Testing Console
            </Link>
            <Link href="/projects" className="rounded-md border border-zinc-800 px-4 py-2 text-zinc-400">
              All Projects
            </Link>
          </div>

          {/* How it works */}
          <section className="rounded-xl border border-zinc-800 p-6">
            <p className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-4">
              How to use your MCP server
            </p>
            <ol className="flex flex-col gap-3 text-sm">
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-300">1</span>
                <span className="text-zinc-300">
                  Open <Link href={`/projects/${project.id}/design`} className="text-zinc-100 underline underline-offset-4 hover:text-white">Visual Designer</Link> — add <span className="text-blue-400">Tools</span>, <span className="text-green-400">Resources</span>, and <span className="text-purple-400">Prompts</span> using the left sidebar. Click any node to edit its name, description, and handler code.
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-300">2</span>
                <span className="text-zinc-300">
                  Click <span className="rounded bg-blue-900 px-1.5 py-0.5 text-blue-300 font-mono text-xs">⚡ Generate Code</span> in the designer header. A code preview will open showing every generated file.
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-300">3</span>
                <span className="text-zinc-300">
                  Click <span className="rounded bg-zinc-800 px-1.5 py-0.5 text-zinc-300 font-mono text-xs">↓ Download ZIP</span> to export your server. Unzip it anywhere on your machine.
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-300">4</span>
                <span className="text-zinc-300">
                  Run the server locally:
                  <code className="ml-2 rounded bg-zinc-900 px-2 py-0.5 font-mono text-xs text-zinc-200">
                    {cmds?.install}
                  </code>
                  <span className="mx-1 text-zinc-600">then</span>
                  <code className="rounded bg-zinc-900 px-2 py-0.5 font-mono text-xs text-zinc-200">
                    {cmds?.run}
                  </code>
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-xs font-bold text-zinc-300">5</span>
                <span className="text-zinc-300">
                  Add to Claude Desktop via the config in the generated <code className="rounded bg-zinc-900 px-1.5 py-0.5 font-mono text-xs text-zinc-200">README.md</code>. Your tools will appear in Claude immediately.
                </span>
              </li>
            </ol>

            <div className="mt-5 rounded-lg border border-zinc-800 bg-zinc-950 p-4">
              <p className="mb-2 text-xs font-medium text-zinc-500">Claude Desktop config snippet</p>
              <pre className="text-xs text-zinc-300 leading-relaxed font-mono whitespace-pre-wrap">{`{
  "mcpServers": {
    "${project.name.toLowerCase().replace(/\s+/g, "-")}": {
      "command": "${project.runtime === "typescript" ? "node" : "python"}",
      "args": ["/path/to/your/server/${project.runtime === "typescript" ? "dist/index.js" : "main.py"}"]
    }
  }
}`}</pre>
            </div>

            <p className="mt-4 text-xs text-zinc-600">
              Changes are saved to the database every time you click <strong>Save</strong> in the detail panel — no manual save needed.
            </p>
          </section>
        </>
      )}
    </main>
  );
}
