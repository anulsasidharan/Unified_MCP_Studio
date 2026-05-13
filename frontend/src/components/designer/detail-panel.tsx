"use client";

import { useEffect, useState } from "react";
import { apiJson } from "@/lib/api";

export type ToolRow = {
  id: string; project_id: string; name: string; description: string | null;
  input_schema: Record<string, unknown>; handler_code: string; handler_language: string;
};
export type ResourceRow = {
  id: string; project_id: string; name: string; uri: string;
  description: string | null; mime_type: string | null; provider_code: string;
};
export type PromptRow = {
  id: string; project_id: string; name: string; description: string | null;
  arguments: unknown[]; messages: unknown[];
};

export type SelectedItem =
  | { type: "tool"; data: ToolRow }
  | { type: "resource"; data: ResourceRow }
  | { type: "prompt"; data: PromptRow };

type Props = {
  item: SelectedItem;
  token: string;
  onSaved: (item: SelectedItem) => void;
  onDeleted: (id: string, type: SelectedItem["type"]) => void;
  onClose: () => void;
};

function jsonStr(v: unknown): string {
  return JSON.stringify(v, null, 2);
}

export function DetailPanel({ item, token, onSaved, onDeleted, onClose }: Props) {
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  // Tool fields
  const [toolName, setToolName] = useState("");
  const [toolDesc, setToolDesc] = useState("");
  const [toolLang, setToolLang] = useState("python");
  const [toolSchema, setToolSchema] = useState("");
  const [toolCode, setToolCode] = useState("");

  // Resource fields
  const [resName, setResName] = useState("");
  const [resUri, setResUri] = useState("");
  const [resDesc, setResDesc] = useState("");
  const [resMime, setResMime] = useState("");
  const [resCode, setResCode] = useState("");

  // Prompt fields
  const [pName, setPName] = useState("");
  const [pDesc, setPDesc] = useState("");
  const [pArgs, setPArgs] = useState("");
  const [pMsgs, setPMsgs] = useState("");

  useEffect(() => {
    setErr(null);
    if (item.type === "tool") {
      const d = item.data;
      setToolName(d.name); setToolDesc(d.description ?? "");
      setToolLang(d.handler_language); setToolSchema(jsonStr(d.input_schema));
      setToolCode(d.handler_code);
    } else if (item.type === "resource") {
      const d = item.data;
      setResName(d.name); setResUri(d.uri); setResDesc(d.description ?? "");
      setResMime(d.mime_type ?? ""); setResCode(d.provider_code);
    } else {
      const d = item.data;
      setPName(d.name); setPDesc(d.description ?? "");
      setPArgs(jsonStr(d.arguments)); setPMsgs(jsonStr(d.messages));
    }
  }, [item.data.id, item.type]);

  async function save() {
    setErr(null); setSaving(true);
    try {
      if (item.type === "tool") {
        let schema: Record<string, unknown>;
        try { schema = JSON.parse(toolSchema) as Record<string, unknown>; }
        catch { setErr("Input schema is not valid JSON."); setSaving(false); return; }
        const updated = await apiJson<ToolRow>(`/api/v1/tools/${item.data.id}`, {
          method: "PUT", token,
          body: JSON.stringify({ name: toolName, description: toolDesc || null,
            handler_language: toolLang, input_schema: schema, handler_code: toolCode }),
        });
        onSaved({ type: "tool", data: updated });
      } else if (item.type === "resource") {
        const updated = await apiJson<ResourceRow>(`/api/v1/resources/${item.data.id}`, {
          method: "PUT", token,
          body: JSON.stringify({ name: resName, uri: resUri, description: resDesc || null,
            mime_type: resMime || null, provider_code: resCode }),
        });
        onSaved({ type: "resource", data: updated });
      } else {
        let args: unknown[], msgs: unknown[];
        try { args = JSON.parse(pArgs) as unknown[]; msgs = JSON.parse(pMsgs) as unknown[]; }
        catch { setErr("Arguments or messages is not valid JSON array."); setSaving(false); return; }
        const updated = await apiJson<PromptRow>(`/api/v1/prompts/${item.data.id}`, {
          method: "PUT", token,
          body: JSON.stringify({ name: pName, description: pDesc || null, arguments: args, messages: msgs }),
        });
        onSaved({ type: "prompt", data: updated });
      }
    } catch {
      setErr("Save failed. Check the backend.");
    } finally { setSaving(false); }
  }

  async function remove() {
    if (!confirm(`Delete this ${item.type}? This cannot be undone.`)) return;
    setDeleting(true);
    const endpoint =
      item.type === "tool" ? `/api/v1/tools/${item.data.id}`
      : item.type === "resource" ? `/api/v1/resources/${item.data.id}`
      : `/api/v1/prompts/${item.data.id}`;
    try {
      await apiJson(endpoint, { method: "DELETE", token });
      onDeleted(item.data.id, item.type);
    } catch {
      setErr("Delete failed.");
    } finally { setDeleting(false); }
  }

  const labelCls = "text-xs font-medium text-zinc-400 uppercase tracking-wide";
  const inputCls = "mt-1 w-full rounded-md border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-100 outline-none focus:ring-1 focus:ring-zinc-500";
  const codeCls = `${inputCls} font-mono text-xs leading-relaxed`;

  const typeColor = item.type === "tool" ? "#60a5fa" : item.type === "resource" ? "#4ade80" : "#c084fc";

  return (
    <aside
      style={{ width: 400, borderLeft: "1px solid #27272a", background: "#0f0f10" }}
      className="flex flex-col overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-zinc-800 px-4 py-3">
        <div className="flex items-center gap-2">
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: typeColor, display: "inline-block" }} />
          <span className="text-sm font-semibold capitalize text-zinc-100">{item.type}</span>
        </div>
        <button onClick={onClose} className="text-zinc-500 hover:text-white text-lg leading-none">✕</button>
      </div>

      {/* Fields */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {item.type === "tool" && (
          <>
            <div><label className={labelCls}>Name</label>
              <input className={inputCls} value={toolName} onChange={(e) => setToolName(e.target.value)} /></div>
            <div><label className={labelCls}>Description</label>
              <textarea className={codeCls} rows={2} value={toolDesc} onChange={(e) => setToolDesc(e.target.value)} /></div>
            <div><label className={labelCls}>Language</label>
              <select className={inputCls} value={toolLang} onChange={(e) => setToolLang(e.target.value)}>
                <option value="python">Python</option>
                <option value="typescript">TypeScript</option>
              </select>
            </div>
            <div><label className={labelCls}>Input Schema (JSON)</label>
              <textarea className={codeCls} rows={6} value={toolSchema} onChange={(e) => setToolSchema(e.target.value)} spellCheck={false} /></div>
            <div><label className={labelCls}>Handler Code</label>
              <textarea className={codeCls} rows={10} value={toolCode} onChange={(e) => setToolCode(e.target.value)} spellCheck={false} /></div>
          </>
        )}

        {item.type === "resource" && (
          <>
            <div><label className={labelCls}>Name</label>
              <input className={inputCls} value={resName} onChange={(e) => setResName(e.target.value)} /></div>
            <div><label className={labelCls}>URI</label>
              <input className={inputCls} value={resUri} onChange={(e) => setResUri(e.target.value)} /></div>
            <div><label className={labelCls}>Description</label>
              <textarea className={codeCls} rows={2} value={resDesc} onChange={(e) => setResDesc(e.target.value)} /></div>
            <div><label className={labelCls}>MIME Type</label>
              <input className={inputCls} value={resMime} onChange={(e) => setResMime(e.target.value)} placeholder="text/plain" /></div>
            <div><label className={labelCls}>Provider Code</label>
              <textarea className={codeCls} rows={10} value={resCode} onChange={(e) => setResCode(e.target.value)} spellCheck={false} /></div>
          </>
        )}

        {item.type === "prompt" && (
          <>
            <div><label className={labelCls}>Name</label>
              <input className={inputCls} value={pName} onChange={(e) => setPName(e.target.value)} /></div>
            <div><label className={labelCls}>Description</label>
              <textarea className={codeCls} rows={2} value={pDesc} onChange={(e) => setPDesc(e.target.value)} /></div>
            <div><label className={labelCls}>Arguments (JSON array)</label>
              <textarea className={codeCls} rows={6} value={pArgs} onChange={(e) => setPArgs(e.target.value)} spellCheck={false} /></div>
            <div><label className={labelCls}>Messages (JSON array)</label>
              <textarea className={codeCls} rows={8} value={pMsgs} onChange={(e) => setPMsgs(e.target.value)} spellCheck={false} /></div>
          </>
        )}

        {err && <p className="text-xs text-red-400">{err}</p>}
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between border-t border-zinc-800 px-4 py-3">
        <button
          onClick={remove}
          disabled={deleting}
          className="rounded-md border border-red-900 px-3 py-1.5 text-sm text-red-400 hover:bg-red-950 disabled:opacity-40"
        >
          {deleting ? "Deleting…" : "Delete"}
        </button>
        <button
          onClick={save}
          disabled={saving}
          className="rounded-md bg-zinc-100 px-4 py-1.5 text-sm font-medium text-zinc-950 disabled:opacity-40"
        >
          {saving ? "Saving…" : "Save"}
        </button>
      </div>
    </aside>
  );
}
