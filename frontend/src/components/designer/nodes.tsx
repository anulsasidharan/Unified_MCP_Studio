import { memo } from "react";
import { Handle, Position, type NodeProps } from "reactflow";

export type NodeItemData = { label: string; itemId: string };

const handleStyle = { width: 8, height: 8 };

export const ToolNode = memo(function ToolNode({ data, selected }: NodeProps<NodeItemData>) {
  return (
    <div
      style={{
        minWidth: 170,
        padding: "10px 14px",
        borderRadius: 10,
        border: `2px solid ${selected ? "#60a5fa" : "#2563eb"}`,
        background: "#0c1a2e",
        color: "#bfdbfe",
        boxShadow: selected ? "0 0 0 2px #3b82f6" : "0 2px 8px rgba(0,0,0,0.4)",
        cursor: "pointer",
      }}
    >
      <Handle type="target" position={Position.Top} style={handleStyle} />
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: 1, color: "#60a5fa", marginBottom: 4, textTransform: "uppercase" }}>
        Tool
      </div>
      <div style={{ fontSize: 13, fontWeight: 600 }}>{data.label}</div>
      <Handle type="source" position={Position.Bottom} style={handleStyle} />
    </div>
  );
});

export const ResourceNode = memo(function ResourceNode({ data, selected }: NodeProps<NodeItemData>) {
  return (
    <div
      style={{
        minWidth: 170,
        padding: "10px 14px",
        borderRadius: 10,
        border: `2px solid ${selected ? "#4ade80" : "#16a34a"}`,
        background: "#0a1f10",
        color: "#bbf7d0",
        boxShadow: selected ? "0 0 0 2px #22c55e" : "0 2px 8px rgba(0,0,0,0.4)",
        cursor: "pointer",
      }}
    >
      <Handle type="target" position={Position.Top} style={handleStyle} />
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: 1, color: "#4ade80", marginBottom: 4, textTransform: "uppercase" }}>
        Resource
      </div>
      <div style={{ fontSize: 13, fontWeight: 600 }}>{data.label}</div>
      <Handle type="source" position={Position.Bottom} style={handleStyle} />
    </div>
  );
});

export const PromptNode = memo(function PromptNode({ data, selected }: NodeProps<NodeItemData>) {
  return (
    <div
      style={{
        minWidth: 170,
        padding: "10px 14px",
        borderRadius: 10,
        border: `2px solid ${selected ? "#c084fc" : "#7c3aed"}`,
        background: "#150d2e",
        color: "#e9d5ff",
        boxShadow: selected ? "0 0 0 2px #a855f7" : "0 2px 8px rgba(0,0,0,0.4)",
        cursor: "pointer",
      }}
    >
      <Handle type="target" position={Position.Top} style={handleStyle} />
      <div style={{ fontSize: 9, fontWeight: 700, letterSpacing: 1, color: "#c084fc", marginBottom: 4, textTransform: "uppercase" }}>
        Prompt
      </div>
      <div style={{ fontSize: 13, fontWeight: 600 }}>{data.label}</div>
      <Handle type="source" position={Position.Bottom} style={handleStyle} />
    </div>
  );
});
