"use client";

import Link from "next/link";

export function StudioNav() {
  return (
    <nav className="flex flex-wrap gap-3 text-sm text-zinc-300">
      <Link className="hover:text-white" href="/">
        Home
      </Link>
      <Link className="hover:text-white" href="/projects">
        Projects
      </Link>
      <Link className="hover:text-white" href="/templates">
        Templates
      </Link>
      <Link className="hover:text-white" href="/auth/login">
        Account
      </Link>
    </nav>
  );
}
