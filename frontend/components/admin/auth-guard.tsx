"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken } from "@/lib/auth";
import { apiRequest } from "@/lib/api-client";
import { UserProfile } from "@/types/auth";
import { PageLoader } from "@/components/ui/loading";

export function AdminAuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function checkAuth() {
      const token = getToken();

      if (!token) {
        router.replace("/admin/login");
        return;
      }

      try {
        const user = await apiRequest<UserProfile>("/auth/me");
        if (!user.is_admin) {
          router.replace("/admin/login");
          return;
        }
        setReady(true);
      } catch {
        router.replace("/admin/login");
      }
    }

    checkAuth();
  }, [router]);

  if (!ready) {
    return <PageLoader />;
  }

  return <>{children}</>;
}
