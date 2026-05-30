"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { UserListItem, UserListResponse } from "@/types/admin";
import { AdminHeader } from "@/components/admin/header";
import { Pagination } from "@/components/admin/pagination";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Select } from "@/components/ui/select";
import { PageLoader } from "@/components/ui/loading";

export default function AdminUsersPage() {
  const [data, setData] = useState<UserListResponse | null>(null);
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  function loadUsers(currentPage: number) {
    apiRequest<UserListResponse>(`/admin/users?page=${currentPage}&page_size=15`)
      .then(setData)
      .catch((err) => setError(err.message));
  }

  useEffect(() => {
    loadUsers(page);
  }, [page]);

  async function handlePlanChange(userId: number, plan: string) {
    setUpdatingId(userId);
    try {
      await apiRequest<UserListItem>(`/admin/users/${userId}/plan`, {
        method: "PATCH",
        body: { plan },
      });
      loadUsers(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update plan");
    } finally {
      setUpdatingId(null);
    }
  }

  if (error && !data) {
    return (
      <div>
        <AdminHeader title="Users" />
        <div className="rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">{error}</div>
      </div>
    );
  }

  if (!data) return <PageLoader />;

  return (
    <div>
      <AdminHeader title="Users" subtitle={`${data.total} total users`} />

      {error && (
        <div className="mb-4 rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">
          {error}
        </div>
      )}

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-brand-border bg-brand-background">
                <th className="px-6 py-3 font-medium text-brand-text-muted">User</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Role</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Plan</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Analyses</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Status</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Joined</th>
              </tr>
            </thead>
            <tbody>
              {data.users.map((user) => (
                <tr key={user.id} className="border-b border-brand-border last:border-0">
                  <td className="px-6 py-4">
                    <p className="font-medium text-brand-text">
                      {user.full_name || "Guest User"}
                    </p>
                    <p className="text-xs text-brand-text-muted">
                      {user.email || `Guest #${user.id}`}
                    </p>
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={user.is_guest ? "muted" : "info"}>
                      {user.is_guest ? "Guest" : user.role}
                    </Badge>
                  </td>
                  <td className="px-6 py-4">
                    <Select
                      options={[
                        { value: "free", label: "Free" },
                        { value: "pro", label: "Pro" },
                        { value: "enterprise", label: "Enterprise" },
                      ]}
                      value={user.plan}
                      disabled={updatingId === user.id}
                      onChange={(e) => handlePlanChange(user.id, e.target.value)}
                      className="w-36"
                    />
                  </td>
                  <td className="px-6 py-4 text-brand-text">{user.analyses_count}</td>
                  <td className="px-6 py-4">
                    <Badge variant={user.is_active ? "success" : "danger"}>
                      {user.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 text-brand-text-muted">
                    {new Date(user.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Pagination
          page={data.page}
          pageSize={data.page_size}
          total={data.total}
          onPageChange={setPage}
        />
      </Card>
    </div>
  );
}
