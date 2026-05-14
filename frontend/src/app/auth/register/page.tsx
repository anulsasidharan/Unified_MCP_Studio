"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { apiJson, ApiError, getApiErrorMessage } from "@/lib/api";
import { setStoredAccessToken } from "@/lib/auth-storage";

type TokenResponse = { access_token: string; token_type: string };

export default function RegisterPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setLoading(true);
    try {
      const data = await apiJson<TokenResponse>("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email,
          password,
          ...(name.trim() ? { name: name.trim() } : {}),
        }),
      });
      setStoredAccessToken(data.access_token);
      router.push("/");
      router.refresh();
    } catch (err) {
      if (err instanceof ApiError) {
        const apiMessage = getApiErrorMessage(err.body);
        if (err.status === 409) {
          setError("An account with this email already exists.");
        } else if (apiMessage) {
          setError(apiMessage);
        } else {
          setError("Registration failed. Try a different email or stronger password.");
        }
      } else {
        setError("Registration failed. Try a different email or stronger password.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-6 py-16">
      <h1 className="text-2xl font-semibold tracking-tight">Create account</h1>
      <p className="mt-2 text-sm text-zinc-400">
        Already registered?{" "}
        <Link href="/auth/login" className="text-zinc-100 underline underline-offset-4">
          Sign in
        </Link>
        .
      </p>
      <form onSubmit={onSubmit} className="mt-8 flex flex-col gap-4">
        <label className="flex flex-col gap-1 text-sm">
          <span className="text-zinc-300">Name (optional)</span>
          <input
            type="text"
            autoComplete="name"
            value={name}
            onChange={(ev) => setName(ev.target.value)}
            className="rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-zinc-100 outline-none ring-zinc-600 focus:ring-2"
          />
        </label>
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
            autoComplete="new-password"
            required
            minLength={8}
            value={password}
            onChange={(ev) => setPassword(ev.target.value)}
            className="rounded-md border border-zinc-800 bg-zinc-950 px-3 py-2 text-zinc-100 outline-none ring-zinc-600 focus:ring-2"
          />
          <span className="text-xs text-zinc-500">At least 8 characters (max 72).</span>
        </label>
        {error ? <p className="text-sm text-red-400">{error}</p> : null}
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-950 disabled:opacity-50"
        >
          {loading ? "Creating account…" : "Create account"}
        </button>
      </form>
    </main>
  );
}
