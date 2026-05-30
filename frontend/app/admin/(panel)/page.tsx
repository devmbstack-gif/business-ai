"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "@/lib/api-client";
import { DashboardStats } from "@/types/admin";
import { AdminHeader } from "@/components/admin/header";
import { StatCard } from "@/components/admin/stat-card";
import { DailyUsageChart } from "@/components/admin/daily-usage-chart";
import { ScoreDistributionChart } from "@/components/admin/score-distribution-chart";
import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/card";
import { PageLoader } from "@/components/ui/loading";

export default function AdminDashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiRequest<DashboardStats>("/admin/stats")
      .then(setStats)
      .catch((err) => setError(err.message));
  }, []);

  if (error) {
    return (
      <div>
        <AdminHeader title="Dashboard" />
        <div className="rounded-lg bg-brand-danger/10 px-4 py-3 text-sm text-brand-danger">
          {error}
        </div>
      </div>
    );
  }

  if (!stats) return <PageLoader />;

  const providers = Object.entries(stats.ai_provider_breakdown);

  return (
    <div>
      <AdminHeader
        title="Dashboard"
        subtitle="Overview of your Business AI platform"
      />

      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Users"
          value={stats.total_users}
          subtitle={`${stats.total_guest_sessions} guest sessions`}
          accent
          icon={<UsersIcon />}
        />
        <StatCard
          title="Total Analyses"
          value={stats.total_analyses}
          subtitle={`${stats.analyses_today} today`}
          icon={<ChartIcon />}
        />
        <StatCard
          title="Proposals Generated"
          value={stats.total_proposals_generated}
          icon={<DocIcon />}
        />
        <StatCard
          title="Avg Success Score"
          value={stats.average_success_score.toFixed(1)}
          subtitle="Across all analyses"
          accent
          icon={<ScoreIcon />}
        />
      </div>

      <div className="mb-8 grid grid-cols-1 gap-5 sm:grid-cols-3">
        <StatCard title="This Week" value={stats.analyses_this_week} subtitle="Analyses" />
        <StatCard title="This Month" value={stats.analyses_this_month} subtitle="Analyses" />
        <StatCard title="Guest Sessions" value={stats.total_guest_sessions} subtitle="Total guests" />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Daily Usage (Last 7 Days)</CardTitle>
          </CardHeader>
          <CardBody>
            <div className="mb-4 flex gap-4 text-xs text-brand-text-muted">
              <span className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-sm bg-brand-secondary" />
                Analyses
              </span>
              <span className="flex items-center gap-1.5">
                <span className="h-2.5 w-2.5 rounded-sm bg-brand-accent" />
                Proposals
              </span>
            </div>
            <DailyUsageChart data={stats.daily_usage} />
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Success Score Distribution</CardTitle>
          </CardHeader>
          <CardBody>
            <ScoreDistributionChart data={stats.score_distribution} />
          </CardBody>
        </Card>
      </div>

      {providers.length > 0 && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>AI Provider Usage</CardTitle>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {providers.map(([provider, count]) => (
                <div
                  key={provider}
                  className="rounded-lg border border-brand-border bg-brand-background px-4 py-3"
                >
                  <p className="text-sm capitalize text-brand-text-muted">{provider}</p>
                  <p className="mt-1 text-2xl font-bold text-brand-text">{count}</p>
                </div>
              ))}
            </div>
          </CardBody>
        </Card>
      )}
    </div>
  );
}

function UsersIcon() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
    </svg>
  );
}

function ChartIcon() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
    </svg>
  );
}

function DocIcon() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
    </svg>
  );
}

function ScoreIcon() {
  return (
    <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
    </svg>
  );
}
