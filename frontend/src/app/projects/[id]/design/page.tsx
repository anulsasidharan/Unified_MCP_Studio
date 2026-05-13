"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import ReactFlow, {
  Background,
  Controls,
  Edge,
  MiniMap,
  Node,
  addEdge,
  useEdgesState,
  useNodesState,
  type Connection,
} from "reactflow";
import "reactflow/dist/style.css";

import { StudioNav } from "@/components/studio-nav";
import { apiJson } from "@/lib/api";
import { getStoredAccessToken } from "@/lib/auth-storage";

type Tool = {
  id: string;
  name: string;
  description: string | null;
};

export default function DesignerPage() {
  const params = useParams<{ id: string }>();
  const projectId = params.id;
  const [tools, setTools] = useState<Tool[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) {
      setError("Sign in to use the designer.");
      return;
    }
    (async () => {
      try {
        const rows = await apiJson<Tool[]>(`/api/v1/projects/${projectId}/tools`, { token });
        setTools(rows);
      } catch {
        setError("Could not load tools.");
      }
    })();
  }, [projectId]);

  const initialNodes: Node[] = useMemo(() => {
    return tools.map((t, idx) => ({
      id: t.id,
      position: { x: 40 + (idx % 3) * 220, y: 40 + Math.floor(idx / 3) * 140 },
      data: { label: `Tool · ${t.name}` },
      style: { borderRadius: 8, padding: 10, background: "#18181b", color: "#fafafa", width: 200 },
    }));
  }, [tools]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge[]>([]);

  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  const onConnect = useCallback(
    (connection: Connection) =>
      setEdges((eds) => addEdge({ ...connection, animated: true }, eds)),
    [setEdges],
  );

  return (
    <main className="flex h-screen flex-col">
      <header className="flex items-center justify-between border-b border-zinc-900 px-4 py-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-zinc-500">Designer</p>
          <p className="text-sm text-zinc-300">
            React Flow canvas — tools as nodes (Phase 3 MVP). Edit definitions via API or future forms.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <StudioNav />
          <Link href={`/projects/${projectId}`} className="text-sm text-zinc-400 hover:text-white">
            ← Back
          </Link>
        </div>
      </header>
      {error ? (
        <div className="px-4 py-2 text-sm text-amber-400">{error}</div>
      ) : (
        <div className="relative flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >
            <MiniMap />
            <Controls />
            <Background gap={16} color="#27272a" />
          </ReactFlow>
        </div>
      )}
    </main>
  );
}
