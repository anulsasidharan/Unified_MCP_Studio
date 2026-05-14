"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { useParams, useSearchParams } from "next/navigation";
import ReactFlow, {
  Background, Controls, MiniMap,
  addEdge, useEdgesState, useNodesState,
  type Connection, type Edge, type Node, type NodeMouseHandler,
} from "reactflow";
import "reactflow/dist/style.css";

import { StudioNav } from "@/components/studio-nav";
import { ToolNode, ResourceNode, PromptNode, type NodeItemData } from "@/components/designer/nodes";
import { DetailPanel, type SelectedItem, type ToolRow, type ResourceRow, type PromptRow } from "@/components/designer/detail-panel";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

const nodeTypes = { toolNode: ToolNode, resourceNode: ResourceNode, promptNode: PromptNode };

type GeneratedFile = { path: string; content: string };
type CodePreview = { runtime: string; project_name: string; files: GeneratedFile[] };

function makeNodes(
  tools: ToolRow[],
  resources: ResourceRow[],
  prompts: PromptRow[],
): Node<NodeItemData>[] {
  const result: Node<NodeItemData>[] = [];
  tools.forEach((t, i) => result.push({
    id: "tool-" + t.id, type: "toolNode",
    position: { x: 60, y: 60 + i * 160 },
    data: { label: t.name, itemId: t.id },
  }));
  resources.forEach((r, i) => result.push({
    id: "resource-" + r.id, type: "resourceNode",
    position: { x: 310, y: 60 + i * 160 },
    data: { label: r.name, itemId: r.id },
  }));
  prompts.forEach((p, i) => result.push({
    id: "prompt-" + p.id, type: "promptNode",
    position: { x: 560, y: 60 + i * 160 },
    data: { label: p.name, itemId: p.id },
  }));
  return result;
}

export default function DesignerPage() {
  const params = useParams<{ id: string }>();
  const searchParams = useSearchParams();
  const projectId = params.id;
  const [token, setToken] = useState<string | null>(null);
  const [tools, setTools] = useState<ToolRow[]>([]);
  const [resources, setResources] = useState<ResourceRow[]>([]);
  const [prompts, setPrompts] = useState<PromptRow[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [selected, setSelected] = useState<SelectedItem | null>(null);
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [codePreview, setCodePreview] = useState<CodePreview | null>(null);
  const [previewFile, setPreviewFile] = useState<string | null>(null);
  const downloadRef = useRef<HTMLAnchorElement>(null);

  const initialNodes = useMemo(() => makeNodes(tools, resources, prompts), [tools, resources, prompts]);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdgesState, onEdgesChange] = useEdgesState<Edge[]>([]);

  useEffect(() => { setNodes(makeNodes(tools, resources, prompts)); }, [tools, resources, prompts]);

  useEffect(() => {
    const t = getStoredAccessToken();
    if (!t) { setLoadError("Sign in to use the designer."); return; }
    setToken(t);
    Promise.all([
      apiJson<ToolRow[]>("/api/v1/projects/" + projectId + "/tools", { token: t }),
      apiJson<ResourceRow[]>("/api/v1/projects/" + projectId + "/resources", { token: t }),
      apiJson<PromptRow[]>("/api/v1/projects/" + projectId + "/prompts", { token: t }),
    ]).then(([ts, rs, ps]) => {
      setTools(ts); setResources(rs); setPrompts(ps);
      if (searchParams.get("generate") === "1") {
        doGenerate(t);
      }
    }).catch(() => setLoadError("Could not load project items."));
  }, [projectId]);

  const onConnect = useCallback(
    (c: Connection) => setEdgesState((eds) => addEdge({ ...c, animated: true }, eds)),
    [setEdgesState],
  );

  const onNodeClick: NodeMouseHandler = useCallback((_evt, node) => {
    const id = (node.data as NodeItemData).itemId;
    if (node.type === "toolNode") {
      const d = tools.find((t) => t.id === id);
      if (d) setSelected({ type: "tool", data: d });
    } else if (node.type === "resourceNode") {
      const d = resources.find((r) => r.id === id);
      if (d) setSelected({ type: "resource", data: d });
    } else if (node.type === "promptNode") {
      const d = prompts.find((p) => p.id === id);
      if (d) setSelected({ type: "prompt", data: d });
    }
  }, [tools, resources, prompts]);

  async function doGenerate(tok?: string) {
    const t = tok ?? token;
    if (!t) return;
    setGenerating(true);
    try {
      const res = await apiJson<CodePreview>("/api/v1/projects/" + projectId + "/generate", {
        method: "POST", token: t,
      });
      setCodePreview(res);
      setPreviewFile(res.files[0]?.path ?? null);
    } catch {
      alert("Could not generate code. Make sure the project has at least one tool.");
    } finally {
      setGenerating(false);
    }
  }

  async function downloadZip() {
    if (!token) return;
    try {
      const res = await fetch("/api/v1/projects/" + projectId + "/download", {
        headers: { Authorization: "Bearer " + token },
      });
      if (!res.ok) { alert("Download failed."); return; }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = downloadRef.current!;
      const cd = res.headers.get("Content-Disposition") ?? "";
      const match = cd.match(/filename="([^"]+)"/);
      a.href = url;
      a.download = match ? match[1] : "mcp-server.zip";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Download failed.");
    }
  }

  async function addTool() {
    if (!token) return;
    try {
      const t = await apiJson<ToolRow>("/api/v1/projects/" + projectId + "/tools", {
        method: "POST", token,
        body: JSON.stringify({
          name: "new_tool", description: "", handler_language: "python",
          input_schema: { type: "object", properties: {}, additionalProperties: false },
          handler_code: "return f\"Hello from new_tool! args={arguments}\"",
        }),
      });
      setTools((prev) => [...prev, t]);
      setSelected({ type: "tool", data: t });
    } catch { alert("Could not create tool."); }
  }

  async function addResource() {
    if (!token) return;
    try {
      const r = await apiJson<ResourceRow>("/api/v1/projects/" + projectId + "/resources", {
        method: "POST", token,
        body: JSON.stringify({
          name: "new_resource", uri: "resource://", description: "",
          mime_type: "text/plain", provider_code: "",
        }),
      });
      setResources((prev) => [...prev, r]);
      setSelected({ type: "resource", data: r });
    } catch { alert("Could not create resource."); }
  }

  async function addPrompt() {
    if (!token) return;
    try {
      const p = await apiJson<PromptRow>("/api/v1/projects/" + projectId + "/prompts", {
        method: "POST", token,
        body: JSON.stringify({ name: "new_prompt", description: "", arguments: [], messages: [] }),
      });
      setPrompts((prev) => [...prev, p]);
      setSelected({ type: "prompt", data: p });
    } catch { alert("Could not create prompt."); }
  }

  function onSaved(updated: SelectedItem) {
    setSavedAt(new Date().toLocaleTimeString());
    if (updated.type === "tool") {
      setTools((prev) => prev.map((t) => (t.id === updated.data.id ? updated.data : t)));
      setNodes((nds) => nds.map((n) =>
        n.id === "tool-" + updated.data.id ? { ...n, data: { ...n.data, label: updated.data.name } } : n
      ));
    } else if (updated.type === "resource") {
      setResources((prev) => prev.map((r) => (r.id === updated.data.id ? updated.data : r)));
      setNodes((nds) => nds.map((n) =>
        n.id === "resource-" + updated.data.id ? { ...n, data: { ...n.data, label: updated.data.name } } : n
      ));
    } else {
      setPrompts((prev) => prev.map((p) => (p.id === updated.data.id ? updated.data : p)));
      setNodes((nds) => nds.map((n) =>
        n.id === "prompt-" + updated.data.id ? { ...n, data: { ...n.data, label: updated.data.name } } : n
      ));
    }
    setSelected(updated);
  }

  function onDeleted(id: string, type: SelectedItem["type"]) {
    const nodeId = type + "-" + id;
    if (type === "tool") { setTools((prev) => prev.filter((t) => t.id !== id)); }
    else if (type === "resource") { setResources((prev) => prev.filter((r) => r.id !== id)); }
    else { setPrompts((prev) => prev.filter((p) => p.id !== id)); }
    setNodes((nds) => nds.filter((n) => n.id !== nodeId));
    setSelected(null);
  }

  const selectedFileContent = codePreview?.files.find((f) => f.path === previewFile)?.content ?? "";

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", background: "#09090b", color: "#fafafa" }}>
      {/* Header */}
      <header style={{ borderBottom: "1px solid #27272a", padding: "10px 16px", display: "flex", alignItems: "center", justifyContent: "space-between", flexShrink: 0, gap: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, minWidth: 0 }}>
          <Link href={"/projects/" + projectId} style={{ color: "#71717a", fontSize: 13, whiteSpace: "nowrap" }}>← Project</Link>
          <span style={{ color: "#3f3f46" }}>|</span>
          <span style={{ fontSize: 13, fontWeight: 600, whiteSpace: "nowrap" }}>Visual Designer</span>
          <span style={{ display: "flex", gap: 10, marginLeft: 4, fontSize: 11, color: "#52525b", flexWrap: "wrap" }}>
            <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#2563eb", marginRight: 4 }} />Tools ({tools.length})</span>
            <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#16a34a", marginRight: 4 }} />Resources ({resources.length})</span>
            <span><span style={{ display: "inline-block", width: 8, height: 8, borderRadius: "50%", background: "#7c3aed", marginRight: 4 }} />Prompts ({prompts.length})</span>
          </span>
          {savedAt && (
            <span style={{ fontSize: 11, color: "#16a34a", marginLeft: 4 }}>✓ Saved {savedAt}</span>
          )}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
          <button
            onClick={() => doGenerate()}
            disabled={generating}
            style={{ background: "#2563eb", color: "#fff", border: "none", borderRadius: 6, padding: "7px 14px", fontSize: 12, fontWeight: 600, cursor: generating ? "wait" : "pointer", opacity: generating ? 0.7 : 1 }}
          >
            {generating ? "Generating…" : "⚡ Generate Code"}
          </button>
          <button
            onClick={downloadZip}
            title="Download ZIP of generated code"
            style={{ background: "transparent", color: "#a1a1aa", border: "1px solid #3f3f46", borderRadius: 6, padding: "7px 12px", fontSize: 12, cursor: "pointer" }}
          >
            ↓ Download ZIP
          </button>
          <StudioNav />
        </div>
      </header>

      {/* Hidden download anchor */}
      <a ref={downloadRef} style={{ display: "none" }} />

      {loadError && (
        <div style={{ padding: "8px 16px", background: "#451a03", color: "#fbbf24", fontSize: 13 }}>{loadError}</div>
      )}

      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        {/* Left sidebar — add nodes */}
        <aside style={{ width: 176, borderRight: "1px solid #27272a", padding: 12, display: "flex", flexDirection: "column", gap: 8, flexShrink: 0, background: "#0a0a0b" }}>
          <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: 1, color: "#52525b", textTransform: "uppercase", marginBottom: 4 }}>Add Node</p>
          <button onClick={addTool} style={{ textAlign: "left", border: "1px solid #1d4ed8", borderRadius: 6, background: "#0c1a2e", color: "#93c5fd", padding: "8px 10px", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
            + Tool
          </button>
          <button onClick={addResource} style={{ textAlign: "left", border: "1px solid #15803d", borderRadius: 6, background: "#0a1f10", color: "#86efac", padding: "8px 10px", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
            + Resource
          </button>
          <button onClick={addPrompt} style={{ textAlign: "left", border: "1px solid #6d28d9", borderRadius: 6, background: "#150d2e", color: "#d8b4fe", padding: "8px 10px", fontSize: 12, fontWeight: 600, cursor: "pointer" }}>
            + Prompt
          </button>
          <div style={{ marginTop: 12, borderTop: "1px solid #27272a", paddingTop: 12 }}>
            <p style={{ fontSize: 11, color: "#3f3f46", lineHeight: 1.6 }}>Click a node to edit it. When ready, click <strong style={{ color: "#52525b" }}>⚡ Generate Code</strong> to preview and download your MCP server.</p>
          </div>
        </aside>

        {/* React Flow canvas */}
        <div style={{ flex: 1, position: "relative" }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            fitViewOptions={{ padding: 0.3 }}
            style={{ background: "#09090b" }}
          >
            <MiniMap
              style={{ background: "#18181b" }}
              maskColor="rgba(0,0,0,0.6)"
              nodeColor={(n) => n.type === "toolNode" ? "#2563eb" : n.type === "resourceNode" ? "#16a34a" : "#7c3aed"}
            />
            <Controls style={{ background: "#18181b", borderColor: "#27272a" }} />
            <Background gap={20} color="#1c1c1e" />
          </ReactFlow>
        </div>

        {/* Detail panel */}
        {selected && token && (
          <DetailPanel
            item={selected}
            token={token}
            onSaved={onSaved}
            onDeleted={onDeleted}
            onClose={() => setSelected(null)}
          />
        )}
      </div>

      {/* Code preview overlay */}
      {codePreview && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", zIndex: 50, display: "flex", flexDirection: "column" }}>
          {/* Overlay header */}
          <div style={{ borderBottom: "1px solid #27272a", padding: "12px 20px", display: "flex", alignItems: "center", justifyContent: "space-between", background: "#0a0a0b", flexShrink: 0 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontWeight: 700, fontSize: 15 }}>{codePreview.project_name}</span>
              <span style={{ fontSize: 11, background: "#1c1c1e", border: "1px solid #3f3f46", borderRadius: 4, padding: "2px 8px", color: "#a1a1aa" }}>{codePreview.runtime}</span>
              <span style={{ fontSize: 12, color: "#52525b" }}>{codePreview.files.length} files generated</span>
            </div>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <button
                onClick={downloadZip}
                style={{ background: "#2563eb", color: "#fff", border: "none", borderRadius: 6, padding: "7px 14px", fontSize: 12, fontWeight: 600, cursor: "pointer" }}
              >
                ↓ Download ZIP
              </button>
              <button
                onClick={() => setCodePreview(null)}
                style={{ background: "transparent", color: "#a1a1aa", border: "1px solid #3f3f46", borderRadius: 6, padding: "7px 12px", fontSize: 12, cursor: "pointer" }}
              >
                ✕ Close
              </button>
            </div>
          </div>

          {/* File browser + code view */}
          <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
            {/* File tree */}
            <nav style={{ width: 240, borderRight: "1px solid #27272a", overflowY: "auto", background: "#0a0a0b", flexShrink: 0, padding: "8px 0" }}>
              <p style={{ fontSize: 10, fontWeight: 700, letterSpacing: 1, color: "#52525b", textTransform: "uppercase", padding: "4px 16px 8px" }}>Files</p>
              {codePreview.files.map((f) => (
                <button
                  key={f.path}
                  onClick={() => setPreviewFile(f.path)}
                  style={{
                    display: "block", width: "100%", textAlign: "left",
                    padding: "6px 16px", fontSize: 12, fontFamily: "monospace",
                    background: previewFile === f.path ? "#1c1c1e" : "transparent",
                    color: previewFile === f.path ? "#fafafa" : "#71717a",
                    border: "none", cursor: "pointer",
                    borderLeft: previewFile === f.path ? "2px solid #2563eb" : "2px solid transparent",
                  }}
                >
                  {f.path}
                </button>
              ))}
            </nav>

            {/* Code view */}
            <div style={{ flex: 1, overflowY: "auto", background: "#09090b", padding: "16px 20px" }}>
              {previewFile && (
                <>
                  <p style={{ fontSize: 12, color: "#52525b", marginBottom: 12, fontFamily: "monospace" }}>{previewFile}</p>
                  <pre style={{
                    margin: 0, padding: "16px", background: "#111113", borderRadius: 8,
                    border: "1px solid #27272a", fontSize: 12, lineHeight: 1.7,
                    color: "#e4e4e7", fontFamily: "'Fira Code', 'Cascadia Code', 'Courier New', monospace",
                    whiteSpace: "pre-wrap", wordBreak: "break-word",
                  }}>
                    <code>{selectedFileContent}</code>
                  </pre>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
