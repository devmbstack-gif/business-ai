export type DailyUsageItem = {
  date: string;
  analyses_count: number;
  proposals_count: number;
};

export type ScoreDistributionItem = {
  range_label: string;
  count: number;
  percentage: number;
};

export type DashboardStats = {
  total_users: number;
  total_analyses: number;
  total_proposals_generated: number;
  total_guest_sessions: number;
  analyses_today: number;
  analyses_this_week: number;
  analyses_this_month: number;
  average_success_score: number;
  daily_usage: DailyUsageItem[];
  score_distribution: ScoreDistributionItem[];
  ai_provider_breakdown: Record<string, number>;
};

export type UserListItem = {
  id: number;
  email: string | null;
  full_name: string | null;
  role: string;
  plan: string;
  is_guest: boolean;
  is_active: boolean;
  analyses_count: number;
  created_at: string;
};

export type UserListResponse = {
  users: UserListItem[];
  total: number;
  page: number;
  page_size: number;
};

export type AnalysisHistoryItem = {
  id: number;
  user_id: number | null;
  user_email: string | null;
  success_score: number | null;
  bid_decision: string | null;
  competition_level: string | null;
  client_trust_level: string | null;
  proposal_generated: boolean;
  ai_provider_used: string | null;
  created_at: string;
};

export type AnalysisHistoryResponse = {
  analyses: AnalysisHistoryItem[];
  total: number;
  page: number;
  page_size: number;
};

export type Plan = {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  price_monthly: number;
  analyses_limit: number;
  proposals_limit: number;
  is_active: boolean;
};

export type PlanUpdatePayload = {
  name?: string;
  description?: string;
  price_monthly?: number;
  analyses_limit?: number;
  proposals_limit?: number;
  is_active?: boolean;
};
