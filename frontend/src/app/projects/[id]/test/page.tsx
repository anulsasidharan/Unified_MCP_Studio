"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";

import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Tool = { id: string; name: string };

export default function TestingConsolePage() {
  const params = useParams<{ id: string }>();
  const projectId = params.id;
  const [tools, setTools] = useState<Tool[]>([]);
  const [toolName, setToolName] = useState("");
  const [argsJson, setArgsJson] = useState("{}");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [output, setOutput] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) {
      setError("Sign in to run tests.");
      return;
    }
    (async () => {
      try {
        const rows = await apiJson<Tool[]>(`/api/v1/projects/${projectId}/tools`, { token });
        setTools(rows);
        if (rows[0]) setToolName(rows[0].name);
      } catch {
        setError("Could not load tools.");
      }
    })();
  }, [projectId]);

  async function startSandbox(e: FormEvent) {
    e.preventDefault();
    setError(null);
    const token = getStoredAccessToken();
    if (!token) return;
    try {
      const res = await apiJson<{ session_id: string }>("/api/v1/testing/sandbox/start", {
        method: "POST",
        token,
        body: JSON.stringify({ project_id: projectId }),
      });
      setSessionId(res.session_id);
      setOutput(`Session ${res.session_id}`);
    } catch {
      setError("Could not start sandbox.");
    }
  }

  async function runTool(e: FormEvent) {
    e.preventDefault();
    if (!sessionId) {
      setError("Start the sandbox first.");
      return;
    }
    const token = getStoredAccessToken();
    if (!token) return;
    let parsed: Record<string, unknown> = {};
    try {
      parsed = JSON.parse(argsJson) as Record<string, unknown>;
    } catch {
      setError("Arguments must be valid JSON.");
      return;
    }
    setError(null);
    try {
      const res = await apiJson<{
        ok: boolean;
        stdout: string;
        stderr: string;
        detail: string | null;
      }>("/api/v1/testing/sandbox/execute", {
        method: "POST",
        token,
        body: JSON.stringify({
          session_id: sessionId,
          tool_name: toolName,
          arguments: parsed,
        }),
      });
      setOutput(JSON.stringify(res, null, 2));
    } catch {
      setError("Execution failed.");
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col gap-6 px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Testing</p>
          <h1 className="text-2xl font-semibold tracking-tight">Sandbox console</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Python runtime executes generated tools via `studio_execute.py` (Phase 5).
          </p>
        </div>
        <StudioNav />
      </header>

      <div className="flex flex-wrap gap-3 text-sm">
        <Link className="text-zinc-400 hover:text-white" href={`/projects/${projectId}/design`}>
          Designer
        </Link>
        <Link className="text-zinc-400 hover:text-white" href={`/projects/${projectId}`}>
          Overview
        </Link>
      </div>

      <form onSubmit={startSandbox} className="flex flex-wrap items-end gap-3">
        <button
          type="submit"
          className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950"
        >
          Start sandbox
        </button>
        {sessionId ? <span className="text-xs text-zinc-500">session: {sessionId}</span> : null}
      </form>

      <form onSubmit={runTool} className="flex flex-col gap-3 rounded-lg border border-zinc-800 p-4">
        <label className="text-sm text-zinc-300">
          Tool
          <select
            className="mt-1 w-full rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-zinc-100"
            value={toolName}
            onChange={(ev) => setToolName(ev.target.value)}
          >
            {tools.map((t) => (
              <option key={t.id} value={t.name}>
                {t.name}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm text-zinc-300">
          Arguments (JSON)
          <textarea
            className="mt-1 w-full rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 font-mono text-xs text-zinc-100"
            rows={5}
            value={argsJson}
            onChange={(ev) => setArgsJson(ev.target.value)}
          />
        </label>
        <button
          type="submit"
          className="rounded-md border border-zinc-700 px-4 py-2 text-sm text-zinc-100"
        >
          Execute tool
        </button>
      </form>

      {error ? <p className="text-sm text-amber-400">{error}</p> : null}

      <section>
        <p className="text-xs uppercase tracking-wide text-zinc-500">Output</p>
        <pre className="mt-2 overflow-x-auto rounded-md bg-zinc-950 p-4 text-xs text-zinc-200">
          {output || "—"}
        </pre>
      </section>
    </main>
  );
}
