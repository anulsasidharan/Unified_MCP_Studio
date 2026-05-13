"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

import { apiJson } from "@/lib/api";
import { getStoredAccessToken, setStoredAccessToken } from "@/lib/auth-storage";

type MeResponse = { email: string; name: string | null; tier: string };

export function AuthBar() {
  const [me, setMe] = useState<MeResponse | null | "loading">("loading");

  useEffect(() => {
    const token = getStoredAccessToken();
    if (!token) {
      setMe(null);
      return;
    }
    let cancelled = false;
    (async () => {
      try {
        const user = await apiJson<MeResponse>("/api/v1/auth/me", { token });
        if (!cancelled) setMe(user);
      } catch {
        if (!cancelled) {
          setStoredAccessToken(null);
          setMe(null);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (me === "loading") {
    return <p className="text-sm text-zinc-500">Checking session…</p>;
  }

  if (me) {
    return (
      <div className="flex flex-wrap items-center gap-3 text-sm text-zinc-300">
        <span>
          Signed in as <span className="text-zinc-100">{me.email}</span>
        </span>
        <button
          type="button"
          className="rounded-md border border-zinc-700 px-3 py-1 text-zinc-200 hover:bg-zinc-900"
          onClick={() => {
            setStoredAccessToken(null);
            setMe(null);
          }}
        >
          Sign out
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-3 text-sm">
      <Link
        href="/auth/login"
        className="rounded-md border border-zinc-700 px-3 py-1 text-zinc-200 hover:bg-zinc-900"
      >
        Sign in
      </Link>
      <Link
        href="/auth/register"
        className="rounded-md bg-zinc-100 px-3 py-1 font-medium text-zinc-950 hover:bg-white"
      >
        Register
      </Link>
    </div>
  );
}
