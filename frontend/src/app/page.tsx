"use client";

import Link from "next/link";
import { AuthBar } from "@/components/auth-bar";

const sections = [
  {
    href: "/projects",
    label: "Projects",
    description: "Create and manage your MCP server projects.",
    color: "#60a5fa",
  },
  {
    href: "/templates",
    label: "Templates",
    description: "Browse starter templates for common integrations.",
    color: "#4ade80",
  },
  {
    href: "/auth/login",
    label: "Account",
    description: "Sign in, register, or manage your session.",
    color: "#c084fc",
  },
];

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col px-6 py-12">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Unified MCP Studio</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Visual builder for Model Context Protocol servers — design, test, and deploy without writing boilerplate.
          </p>
        </div>
        <AuthBar />
      </header>

      <nav className="mt-12 grid gap-4 sm:grid-cols-3">
        {sections.map((s) => (
          <Link
            key={s.href}
            href={s.href}
            className="group flex flex-col gap-2 rounded-xl border border-zinc-800 p-5 transition-colors hover:border-zinc-600 hover:bg-zinc-900"
          >
            <span
              className="text-xs font-bold uppercase tracking-widest"
              style={{ color: s.color }}
            >
              {s.label}
            </span>
            <span className="text-sm text-zinc-400 group-hover:text-zinc-200">
              {s.description}
            </span>
            <span className="mt-auto text-xs text-zinc-600 group-hover:text-zinc-400">
              Open →
            </span>
          </Link>
        ))}
      </nav>

      <section className="mt-12 rounded-xl border border-zinc-800 p-6">
        <p className="text-xs font-bold uppercase tracking-widest text-zinc-500">Quick start</p>
        <ol className="mt-4 flex flex-col gap-2 text-sm text-zinc-400">
          <li><span className="text-zinc-200">1.</span> Go to <Link href="/projects" className="text-zinc-200 underline underline-offset-4 hover:text-white">Projects</Link> and create a new project (Python or TypeScript).</li>
          <li><span className="text-zinc-200">2.</span> Open the project and click <span className="text-zinc-200">Visual designer</span>.</li>
          <li><span className="text-zinc-200">3.</span> Add Tools, Resources, and Prompts from the left sidebar.</li>
          <li><span className="text-zinc-200">4.</span> Click any node to edit its name, code, and schema in the detail panel.</li>
          <li><span className="text-zinc-200">5.</span> Use the <span className="text-zinc-200">Testing console</span> to run tools against a live sandbox.</li>
        </ol>
      </section>
    </main>
  );
}
