"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { StudioNav } from "@/components/studio-nav";
import { ApiError, apiJson, getApiErrorMessage } from "@/lib/api";
import {
  MCP_TEMPLATE_BLUEPRINTS,
  MCP_TEMPLATE_COUNTS,
  type McpTemplateBlueprint,
  type TemplateTier,
} from "@/lib/mcp-template-catalog";
import { getStoredAccessToken } from "@/lib/auth-storage";

type ApiTemplate = {
  id: string;
  name: string;
  description: string | null;
  category: string | null;
  use_count: number;
  config: { runtime?: string; transport?: string };
};

type CreatedProject = {
  id: string;
  name: string;
};

type TierFilter = "all" | TemplateTier;

const TIER_ORDER: TemplateTier[] = ["basic", "intermediate", "advanced"];

const TIER_LABEL: Record<TemplateTier, string> = {
  basic: "Basic",
  intermediate: "Intermediate",
  advanced: "Advanced",
};

const TIER_DESCRIPTION: Record<TemplateTier, string> = {
  basic:
    "Single-process utilities, parsers, and teaching servers. Minimal dependencies, easy to ship in stdio mode, ideal for learning MCP tool contracts.",
  intermediate:
    "Production-style integrations with auth, quotas, pagination, and cloud SDKs. Always combine with hostname allowlists, secrets from env, and org review before widening scope.",
  advanced:
    "Multi-tenant routing, resilience, compliance, and orchestration patterns. Intended for platform engineers—pair every pattern with threat modeling and sandboxed side effects.",
};

function matchesQuery(t: McpTemplateBlueprint, q: string): boolean {
  if (!q.trim()) return true;
  const s = q.toLowerCase();
  const blob = [
    t.name,
    t.tagline,
    t.category,
    t.overview,
    t.design,
    t.extensionIdeas,
    t.risks,
    t.primaryRuntime,
    t.transport,
    ...t.suggestedTools,
  ]
    .join("\n")
    .toLowerCase();
  return blob.includes(s);
}

function exportBlueprintJson(t: McpTemplateBlueprint): void {
  const payload = {
    id: t.id,
    tier: t.tier,
    name: t.name,
    tagline: t.tagline,
    category: t.category,
    primaryRuntime: t.primaryRuntime,
    transport: t.transport,
    overview: t.overview,
    design: t.design,
    extensionIdeas: t.extensionIdeas,
    risks: t.risks,
    suggestedTools: [...t.suggestedTools],
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `mcp-blueprint-${t.id}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function TierSection({
  tier,
  items,
  hasToken,
  instantiatingBlueprintId,
  onUseBlueprint,
}: {
  tier: TemplateTier;
  items: readonly McpTemplateBlueprint[];
  hasToken: boolean;
  instantiatingBlueprintId: string | null;
  onUseBlueprint: (t: McpTemplateBlueprint) => void;
}) {
  return (
    <section className="space-y-4">
      <div className="border-b border-zinc-800 pb-3">
        <h2 className="text-lg font-semibold text-zinc-100">{TIER_LABEL[tier]}</h2>
        <p className="mt-1 text-sm text-zinc-400">{TIER_DESCRIPTION[tier]}</p>
        <p className="mt-2 text-xs text-zinc-500">
          {MCP_TEMPLATE_COUNTS[tier]} blueprints in this section
          {items.length !== MCP_TEMPLATE_COUNTS[tier] ? ` (${items.length} visible with current search)` : ""}
        </p>
      </div>
      {items.length === 0 ? (
        <p className="rounded-md border border-dashed border-zinc-800 bg-zinc-950/30 px-4 py-6 text-center text-sm text-zinc-500">
          No blueprints in this tier match your search.
        </p>
      ) : (
        <ul className="grid gap-3 md:grid-cols-2">
          {items.map((t) => (
            <li
              key={t.id}
              className="flex flex-col rounded-lg border border-zinc-800 bg-zinc-950/40 ring-1 ring-zinc-900/80"
            >
              <div className="flex flex-wrap gap-2 border-b border-zinc-800/80 p-3">
                <button
                  type="button"
                  disabled={!hasToken || instantiatingBlueprintId !== null}
                  onClick={() => onUseBlueprint(t)}
                  className="rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {instantiatingBlueprintId === t.id ? "Creating…" : "Use this template"}
                </button>
                <button
                  type="button"
                  onClick={() => exportBlueprintJson(t)}
                  className="rounded-md border border-zinc-600 bg-zinc-900 px-3 py-1.5 text-xs font-medium text-zinc-200 hover:border-zinc-500 hover:bg-zinc-800"
                >
                  Export JSON
                </button>
                {!hasToken && (
                  <span className="self-center text-[11px] text-zinc-500">Sign in to use a catalog blueprint</span>
                )}
              </div>
              <details className="group p-4">
                <summary className="cursor-pointer list-none [&::-webkit-details-marker]:hidden">
                  <div className="flex flex-col gap-2">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-[11px] uppercase tracking-wide text-amber-400/90">
                        {t.category.replace(/-/g, " ")}
                      </span>
                      <span className="rounded bg-zinc-800 px-1.5 py-0.5 text-[10px] uppercase tracking-wide text-zinc-300">
                        {t.primaryRuntime}
                      </span>
                      <span className="rounded bg-zinc-900 px-1.5 py-0.5 text-[10px] text-zinc-500">
                        {t.transport}
                      </span>
                    </div>
                    <p className="font-medium text-zinc-100">{t.name}</p>
                    <p className="text-sm text-zinc-400">{t.tagline}</p>
                    <p className="text-xs text-zinc-500 group-open:hidden">Open for full design, tools, and risks</p>
                    <p className="hidden text-xs text-emerald-400/90 group-open:block">Design narrative and mitigations</p>
                  </div>
                </summary>
                <div className="mt-4 space-y-4 border-t border-zinc-800/80 pt-4 text-sm">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Use case</p>
                    <p className="mt-1 leading-relaxed text-zinc-300">{t.overview}</p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Architecture and tool design</p>
                    <p className="mt-1 whitespace-pre-wrap leading-relaxed text-zinc-300">{t.design}</p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Suggested tools</p>
                    <ul className="mt-1 flex flex-wrap gap-1.5">
                      {t.suggestedTools.map((n) => (
                        <li
                          key={n}
                          className="rounded-md border border-zinc-700/80 bg-zinc-900/60 px-2 py-0.5 font-mono text-[11px] text-emerald-300/90"
                        >
                          {n}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-zinc-500">Extension ideas</p>
                    <p className="mt-1 leading-relaxed text-zinc-400">{t.extensionIdeas}</p>
                  </div>
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-amber-600/90">Risks</p>
                    <p className="mt-1 leading-relaxed text-amber-200/80">{t.risks}</p>
                  </div>
                </div>
              </details>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

const FILTER_TABS: { id: TierFilter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "basic", label: "Basic" },
  { id: "intermediate", label: "Intermediate" },
  { id: "advanced", label: "Advanced" },
];

export default function TemplatesPage() {
  const router = useRouter();
  const importInputRef = useRef<HTMLInputElement>(null);
  const [apiTemplates, setApiTemplates] = useState<ApiTemplate[]>([]);
  const [apiError, setApiError] = useState<string | null>(null);
  const [apiLoading, setApiLoading] = useState(false);
  const [instantiatingLibraryId, setInstantiatingLibraryId] = useState<string | null>(null);
  const [instantiatingBlueprintId, setInstantiatingBlueprintId] = useState<string | null>(null);
  const [instantiateError, setInstantiateError] = useState<string | null>(null);
  const [blueprintImportError, setBlueprintImportError] = useState<string | null>(null);
  const [blueprintImporting, setBlueprintImporting] = useState(false);
  const [hasToken, setHasToken] = useState(false);
  const [query, setQuery] = useState("");
  const [tierFilter, setTierFilter] = useState<TierFilter>("all");

  useEffect(() => {
    const token = getStoredAccessToken();
    setHasToken(!!token);
    if (!token) {
      setApiTemplates([]);
      setApiError(null);
      setApiLoading(false);
      return;
    }
    setApiLoading(true);
    (async () => {
      try {
        const data = await apiJson<ApiTemplate[]>("/api/v1/templates", { token });
        setApiTemplates(data);
        setApiError(null);
      } catch (err) {
        if (err instanceof ApiError) {
          const hint =
            err.status >= 500
              ? " If this persists, ensure the database is migrated (`alembic upgrade head` from `backend/`)."
              : "";
          const detail = getApiErrorMessage(err.body);
          setApiError(
            detail
              ? `Could not load library templates (${err.status}): ${detail}.${hint}`
              : `Could not load library templates (HTTP ${err.status}).${hint}`,
          );
        } else {
          setApiError("Could not load registered templates from the API.");
        }
      } finally {
        setApiLoading(false);
      }
    })();
  }, []);

  async function instantiateLibraryTemplate(t: ApiTemplate) {
    const token = getStoredAccessToken();
    if (!token) return;
    setInstantiateError(null);
    setInstantiatingLibraryId(t.id);
    try {
      const project = await apiJson<CreatedProject>("/api/v1/projects/from-template", {
        method: "POST",
        token,
        body: JSON.stringify({ template_id: t.id }),
      });
      router.push(`/projects/${project.id}/design`);
    } catch {
      setInstantiateError("Could not create a project from this template. Try again or pick another template.");
    } finally {
      setInstantiatingLibraryId(null);
    }
  }

  async function instantiateCatalogBlueprint(t: McpTemplateBlueprint) {
    const token = getStoredAccessToken();
    if (!token) return;
    setInstantiateError(null);
    setBlueprintImportError(null);
    setInstantiatingBlueprintId(t.id);
    try {
      const project = await apiJson<CreatedProject>("/api/v1/projects/from-catalog-blueprint", {
        method: "POST",
        token,
        body: JSON.stringify({ blueprint_id: t.id, name: t.name }),
      });
      router.push(`/projects/${project.id}/design`);
    } catch (err) {
      const msg =
        err instanceof ApiError ? getApiErrorMessage(err.body) : null;
      setInstantiateError(
        msg
          ? `Could not create from blueprint: ${msg}`
          : "Could not create a project from this blueprint. Try again.",
      );
    } finally {
      setInstantiatingBlueprintId(null);
    }
  }

  async function onImportBlueprintFile(file: File) {
    const token = getStoredAccessToken();
    if (!token) {
      setBlueprintImportError("Sign in to import a blueprint.");
      return;
    }
    setBlueprintImportError(null);
    setInstantiateError(null);
    setBlueprintImporting(true);
    try {
      const text = await file.text();
      const data = JSON.parse(text) as Record<string, unknown>;
      if (!data || typeof data !== "object") {
        throw new Error("File must contain a JSON object.");
      }
      const project = await apiJson<CreatedProject>("/api/v1/projects/from-blueprint-export", {
        method: "POST",
        token,
        body: JSON.stringify(data),
      });
      router.push(`/projects/${project.id}/design`);
    } catch (err) {
      const msg =
        err instanceof ApiError ? getApiErrorMessage(err.body) : err instanceof Error ? err.message : null;
      setBlueprintImportError(
        msg ?? "Invalid blueprint file or import failed. Use an export from this page or match the catalog JSON shape.",
      );
    } finally {
      setBlueprintImporting(false);
      if (importInputRef.current) importInputRef.current.value = "";
    }
  }

  const filtered = useMemo(() => {
    const q = query.trim();
    return MCP_TEMPLATE_BLUEPRINTS.filter((t) => matchesQuery(t, q));
  }, [query]);

  const tierFiltered = useMemo(() => {
    if (tierFilter === "all") return filtered;
    return filtered.filter((t) => t.tier === tierFilter);
  }, [filtered, tierFilter]);

  const byTier = useMemo(() => {
    const map: Record<TemplateTier, McpTemplateBlueprint[]> = {
      basic: [],
      intermediate: [],
      advanced: [],
    };
    for (const t of tierFiltered) {
      map[t.tier].push(t);
    }
    return map;
  }, [tierFiltered]);

  const visibleTiers: TemplateTier[] =
    tierFilter === "all" ? TIER_ORDER : tierFilter === "basic" ? ["basic"] : tierFilter === "intermediate" ? ["intermediate"] : ["advanced"];

  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-6 py-12">
      <header className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <div className="max-w-2xl space-y-3">
          <p className="text-xs uppercase tracking-wide text-zinc-500">Library</p>
          <h1 className="text-3xl font-semibold tracking-tight text-zinc-50">MCP template blueprints</h1>
          <p className="text-sm leading-relaxed text-zinc-400">
            Browse {MCP_TEMPLATE_BLUEPRINTS.length} curated patterns. Filter by tier, search, then{" "}
            <span className="text-zinc-200">Use this template</span> to open a real project in the designer (stub tools are
            created from the blueprint). <span className="text-zinc-200">Export JSON</span> saves the blueprint for sharing or
            re-import below. Database-backed library templates still support one-click create when the API is available.
          </p>
        </div>
        <StudioNav />
      </header>

      <section
        id="instantiate"
        className="scroll-mt-8 space-y-3 rounded-lg border border-emerald-900/50 bg-emerald-950/20 p-5"
      >
        <h2 className="text-sm font-semibold text-emerald-200/90">Start from a library template (API)</h2>
        <p className="text-sm leading-relaxed text-zinc-400">
          These rows come from <code className="text-emerald-200/80">GET /api/v1/templates</code> (seeded in the database).
          They include concrete tool definitions. Catalog cards above/below can also create projects via the new blueprint
          endpoint.
        </p>
        {!hasToken && (
          <p className="text-sm text-zinc-300">
            <Link href="/auth/login" className="font-medium text-emerald-400 underline-offset-4 hover:underline">
              Sign in
            </Link>{" "}
            to instantiate templates or import an export.
          </p>
        )}
        {hasToken && apiLoading && <p className="text-sm text-zinc-500">Loading library templates…</p>}
        {hasToken && !apiLoading && apiError && <p className="text-sm text-amber-400">{apiError}</p>}
        {hasToken && !apiLoading && !apiError && apiTemplates.length === 0 && (
          <p className="text-sm text-zinc-500">
            No library templates returned. If the database is empty, run backend migrations so seeded templates are
            available.
          </p>
        )}
        {instantiateError && <p className="text-sm text-amber-400">{instantiateError}</p>}
        {blueprintImportError && <p className="text-sm text-amber-400">{blueprintImportError}</p>}
        {hasToken && !apiLoading && apiTemplates.length > 0 && (
          <ul className="grid gap-3 sm:grid-cols-2">
            {apiTemplates.map((t) => (
              <li key={t.id} className="flex flex-col gap-3 rounded-md border border-zinc-800 bg-zinc-950/50 p-3 text-sm">
                <div>
                  <p className="font-medium text-zinc-100">{t.name}</p>
                  {t.description && <p className="mt-1 text-zinc-400">{t.description}</p>}
                  <div className="mt-2 flex flex-wrap gap-2 text-xs text-zinc-500">
                    {t.category && <span>{t.category}</span>}
                    {t.config.runtime && <span>{t.config.runtime}</span>}
                    {t.config.transport && <span>{t.config.transport}</span>}
                    <span>used {t.use_count}×</span>
                  </div>
                </div>
                <button
                  type="button"
                  disabled={instantiatingLibraryId !== null || instantiatingBlueprintId !== null || blueprintImporting}
                  onClick={() => instantiateLibraryTemplate(t)}
                  className="self-start rounded-md bg-emerald-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {instantiatingLibraryId === t.id ? "Creating…" : "Use this template"}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="flex flex-col gap-4 rounded-lg border border-zinc-800/80 bg-zinc-900/20 p-4">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">Tier filter</p>
          <div className="flex flex-wrap gap-2">
            {FILTER_TABS.map((tab) => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setTierFilter(tab.id)}
                className={
                  tierFilter === tab.id
                    ? "rounded-full bg-emerald-600 px-3 py-1 text-xs font-medium text-white"
                    : "rounded-full border border-zinc-700 bg-zinc-950 px-3 py-1 text-xs font-medium text-zinc-300 hover:border-zinc-500"
                }
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <label className="flex max-w-xl flex-1 flex-col gap-1 text-sm">
            <span className="text-zinc-500">Search the catalog</span>
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Try slack, postgres, audit, hashing…"
              className="rounded-md border border-zinc-700 bg-zinc-950 px-3 py-2 text-zinc-100 placeholder:text-zinc-600 outline-none ring-zinc-600 focus:ring-2"
            />
          </label>
          <p className="text-xs text-zinc-500">
            Showing {tierFiltered.length} of {MCP_TEMPLATE_BLUEPRINTS.length} blueprints
            {tierFilter !== "all" ? ` (${TIER_LABEL[tierFilter]} only)` : ""}
          </p>
        </div>
        {hasToken && (
          <div className="flex flex-wrap items-center gap-3 border-t border-zinc-800/80 pt-4">
            <input
              ref={importInputRef}
              type="file"
              accept="application/json,.json"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0];
                if (f) void onImportBlueprintFile(f);
              }}
            />
            <button
              type="button"
              disabled={blueprintImporting || instantiatingBlueprintId !== null}
              onClick={() => importInputRef.current?.click()}
              className="rounded-md border border-zinc-600 bg-zinc-950 px-3 py-1.5 text-xs font-medium text-zinc-200 hover:bg-zinc-900 disabled:opacity-50"
            >
              {blueprintImporting ? "Importing…" : "Import blueprint JSON"}
            </button>
            <span className="text-[11px] text-zinc-500">Use a file from Export JSON, or any object matching the catalog shape.</span>
          </div>
        )}
      </div>

      <div className="grid gap-2 rounded-lg border border-zinc-800/80 bg-zinc-900/20 p-4 text-xs text-zinc-400 sm:grid-cols-3">
        <p>
          <span className="font-semibold text-zinc-300">Basic:</span> {MCP_TEMPLATE_COUNTS.basic} patterns
        </p>
        <p>
          <span className="font-semibold text-zinc-300">Intermediate:</span> {MCP_TEMPLATE_COUNTS.intermediate} patterns
        </p>
        <p>
          <span className="font-semibold text-zinc-300">Advanced:</span> {MCP_TEMPLATE_COUNTS.advanced} patterns
        </p>
      </div>

      <div className="space-y-14">
        {visibleTiers.map((tier) => (
          <TierSection
            key={tier}
            tier={tier}
            items={byTier[tier]}
            hasToken={hasToken}
            instantiatingBlueprintId={instantiatingBlueprintId}
            onUseBlueprint={instantiateCatalogBlueprint}
          />
        ))}
      </div>

      <footer className="flex flex-wrap gap-4 border-t border-zinc-800 pt-6 text-sm text-zinc-400">
        <Link href="/projects" className="hover:text-white">
          ← Projects
        </Link>
        <Link href="/templates#instantiate" className="text-zinc-500 hover:text-zinc-200">
          Jump to API library templates
        </Link>
      </footer>
    </main>
  );
}
