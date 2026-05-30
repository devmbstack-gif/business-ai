"use client";

import { AdminAuthGuard } from "@/components/admin/auth-guard";
import { AdminSidebar } from "@/components/admin/sidebar";

export default function AdminPanelLayout({ children }: { children: React.ReactNode }) {
  return (
    <AdminAuthGuard>
      <div className="min-h-screen bg-brand-background">
        <AdminSidebar />
        <main className="ml-64 min-h-screen p-8">{children}</main>
      </div>
    </AdminAuthGuard>
  );
}
