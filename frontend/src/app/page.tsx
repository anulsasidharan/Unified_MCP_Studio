import { AuthBar } from "@/components/auth-bar";
import { StudioNav } from "@/components/studio-nav";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center px-6 py-16">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Unified MCP Studio</h1>
          <p className="mt-4 text-zinc-400">
            Phases 2–8 deliver projects, designer, codegen, sandbox, templates, deployments, and infra
            scaffolding per{" "}
            <code className="rounded bg-zinc-900 px-1.5 py-0.5 text-sm text-zinc-200">TASKS.md</code>
            .
          </p>
          <div className="mt-6">
            <StudioNav />
          </div>
        </div>
        <AuthBar />
      </div>
    </main>
  );
}
