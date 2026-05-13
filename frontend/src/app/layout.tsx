import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Unified MCP Studio",
  description: "Visual builder for Model Context Protocol servers",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
