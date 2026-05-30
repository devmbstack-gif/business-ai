"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { apiRequest } from "@/lib/api-client";
import { saveToken } from "@/lib/auth";
import { LoginResponse } from "@/types/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardBody } from "@/components/ui/card";

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
    <div className="flex min-h-screen items-center justify-center bg-brand-background px-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <Image
            src="/logo.jpeg"
            alt="Business AI"
            width={200}
            height={80}
            className="mx-auto rounded-xl"
          />
          <h1 className="mt-6 text-2xl font-bold text-brand-text">Admin Login</h1>
          <p className="mt-2 text-sm text-brand-text-muted">
            Sign in to manage your Business AI platform
          </p>
        </div>

        <Card>
          <CardBody>
            <form onSubmit={handleSubmit} className="space-y-5">
              <Input
                label="Email"
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
                <div className="rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">
                  {error}
                </div>
              )}

              <Button type="submit" className="w-full" loading={loading}>
                Sign In
              </Button>
            </form>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
