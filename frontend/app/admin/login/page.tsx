"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { apiRequest } from "@/lib/api-client";
import { saveToken } from "@/lib/auth";
import { LoginResponse } from "@/types/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await apiRequest<LoginResponse>("/auth/login", {
        method: "POST",
        body: { email, password },
        auth: false,
      });

      if (!data.is_admin) {
        setError("You do not have admin access");
        setLoading(false);
        return;
      }

      saveToken(data.access_token);
      router.push("/admin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
      setLoading(false);
    }
  }

  return (
    <div className="login-page-bg flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-[440px]">
        <div className="login-card overflow-hidden rounded-2xl bg-brand-surface">
          <div className="login-card-accent h-1.5 w-full" />

          <div className="px-8 pb-8 pt-7">
            <div className="mb-6 flex flex-col items-center text-center">
              <Image
                src="/logo.jpeg"
                alt="Business AI"
                width={200}
                height={80}
                className="rounded-xl"
              />
              <h1 className="mt-5 text-2xl font-bold tracking-tight text-brand-text">
                Admin Login
              </h1>
              <p className="mt-1.5 text-sm text-brand-text-muted">
                Sign in to manage your Business AI platform
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <Input
                label="Email address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@businessai.com"
                required
              />
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />

              {error && (
                <div className="flex items-center gap-2 rounded-xl border border-brand-danger/20 bg-brand-danger/5 px-4 py-3 text-sm text-brand-danger">
                  <svg className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                  </svg>
                  {error}
                </div>
              )}

              <Button
                type="submit"
                size="lg"
                className="mt-2 w-full shadow-md shadow-brand-primary/30"
                loading={loading}
              >
                Sign In
              </Button>
            </form>
          </div>
        </div>

        <p className="mt-6 text-center text-sm text-brand-text-muted">
          <Link href="/" className="font-medium transition-colors hover:text-brand-primary">
            ← Back to home
          </Link>
        </p>

        <p className="mt-3 text-center text-xs text-brand-text-muted/70">
          Smart Proposals. Better Wins.
        </p>
      </div>
    </div>
  );
}
