"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { AnalysisHistoryResponse } from "@/types/admin";
import { AdminHeader } from "@/components/admin/header";
import { Pagination } from "@/components/admin/pagination";
import { ScoreBadge } from "@/components/admin/score-badge";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { PageLoader } from "@/components/ui/loading";

function getBidVariant(decision: string | null) {
  if (!decision) return "muted" as const;
  const lower = decision.toLowerCase();
  if (lower.includes("recommended") && !lower.includes("caution")) return "success" as const;
  if (lower.includes("caution")) return "warning" as const;
  if (lower.includes("skip")) return "danger" as const;
  return "default" as const;
}

export default function AdminAnalysesPage() {
  const [data, setData] = useState<AnalysisHistoryResponse | null>(null);
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");

  useEffect(() => {
    apiRequest<AnalysisHistoryResponse>(`/admin/analyses?page=${page}&page_size=15`)
      .then(setData)
      .catch((err) => setError(err.message));
  }, [page]);

  if (error) {
    return (
      <div>
        <AdminHeader title="Analysis History" />
        <div className="rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">{error}</div>
      </div>
    );
  }

  if (!data) return <PageLoader />;

  return (
    <div>
      <AdminHeader title="Analysis History" subtitle={`${data.total} total analyses`} />

      <Card className="overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-brand-border bg-brand-background">
                <th className="px-6 py-3 font-medium text-brand-text-muted">ID</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">User</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Score</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Bid Decision</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Competition</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Client Trust</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Proposal</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">AI Provider</th>
                <th className="px-6 py-3 font-medium text-brand-text-muted">Date</th>
              </tr>
            </thead>
            <tbody>
              {data.analyses.map((item) => (
                <tr key={item.id} className="border-b border-brand-border last:border-0">
                  <td className="px-6 py-4 font-medium text-brand-text">#{item.id}</td>
                  <td className="px-6 py-4 text-brand-text-muted">
                    {item.user_email || "Guest"}
                  </td>
                  <td className="px-6 py-4">
                    <ScoreBadge score={item.success_score} />
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={getBidVariant(item.bid_decision)}>
                      {item.bid_decision?.replace(/_/g, " ") || "N/A"}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 capitalize text-brand-text-muted">
                    {item.competition_level?.replace(/_/g, " ") || "N/A"}
                  </td>
                  <td className="px-6 py-4 capitalize text-brand-text-muted">
                    {item.client_trust_level?.replace(/_/g, " ") || "N/A"}
                  </td>
                  <td className="px-6 py-4">
                    <Badge variant={item.proposal_generated ? "success" : "muted"}>
                      {item.proposal_generated ? "Yes" : "No"}
                    </Badge>
                  </td>
                  <td className="px-6 py-4 capitalize text-brand-text-muted">
                    {item.ai_provider_used || "N/A"}
                  </td>
                  <td className="px-6 py-4 text-brand-text-muted">
                    {new Date(item.created_at).toLocaleDateString()}
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
