"use client";

import { useRouter } from "next/navigation";
import { clearToken } from "@/lib/auth";
import { Button } from "@/components/ui/button";

type AdminHeaderProps = {
  title: string;
  subtitle?: string;
};

export function AdminHeader({ title, subtitle }: AdminHeaderProps) {
  const router = useRouter();

  function handleLogout() {
    clearToken();
    router.push("/admin/login");
  }

  return (
    <header className="mb-8 flex items-center justify-between">
      <div>
        <h1 className="text-2xl font-bold text-brand-text">{title}</h1>
        {subtitle && <p className="mt-1 text-sm text-brand-text-muted">{subtitle}</p>}
      </div>
      <Button variant="outline" size="sm" onClick={handleLogout}>
        Logout
      </Button>
    </header>
  );
}
