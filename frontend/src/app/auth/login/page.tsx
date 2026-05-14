"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { apiJson, ApiError, getApiErrorMessage } from "@/lib/api";
import { setStoredAccessToken } from "@/lib/auth-storage";

type TokenResponse = { access_token: string; token_type: string };

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const data = await apiJson<TokenResponse>("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });
      setStoredAccessToken(data.access_token);
      router.push("/");
      router.refresh();
    } catch (err) {
      if (err instanceof ApiError) {
        const apiMessage = getApiErrorMessage(err.body);
        if (apiMessage) {
          setError(apiMessage);
        } else if (err.status === 401) {
          setError("Incorrect email or password.");
        } else if (err.status === 503 || err.status === 502 || err.status === 504) {
          setError(
            "The API or database is not reachable. Start PostgreSQL, set backend DATABASE_URL to match " +
              "your DB user and password (see docker-compose POSTGRES_*), run alembic upgrade head, then restart the API.",
          );
        } else if (err.status >= 500) {
          setError(
            "Server error while signing in. Typical causes: PostgreSQL not running, wrong DATABASE_URL in backend/.env, " +
              "or migrations not applied. Confirm uvicorn is running and check the API terminal log.",
          );
        } else {
          setError(`Sign-in failed (${err.status}). Try again.`);
        }
      } else {
        setError("Login failed. Check your network connection.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-6 py-16">
      <h1 className="text-2xl font-semibold tracking-tight">Sign in</h1>
      <p className="mt-2 text-sm text-zinc-400">
        Use your Unified MCP Studio account. New here?{" "}
        <Link href="/auth/register" className="text-zinc-100 underline underline-offset-4">
          Create an account
        </Link>
        .
      </p>
      <form onSubmit={onSubmit} className="mt-8 flex flex-col gap-4">
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-zinc-300">Email</span>
          <input
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(ev) => setEmail(ev.target.value)}
            className="rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-zinc-100 outline-none ring-zinc-600 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-zinc-300">Password</span>
          <input
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(ev) => setPassword(ev.target.value)}
            className="rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-zinc-100 outline-none ring-zinc-600 focus:ring-2"
          />
        </label>
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 disabled:opacity-50"
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </main>
  );
}
