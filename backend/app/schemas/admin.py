from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DailyUsageItem(BaseModel):
    date: str
    analyses_count: int
    proposals_count: int


class ScoreDistributionItem(BaseModel):
    range_label: str
    count: int
    percentage: float


class DashboardStatsResponse(BaseModel):
    total_users: int
    total_analyses: int
    total_proposals_generated: int
    total_guest_sessions: int
    analyses_today: int
    analyses_this_week: int
    analyses_this_month: int
    average_success_score: float
    daily_usage: List[DailyUsageItem]
    score_distribution: List[ScoreDistributionItem]
    ai_provider_breakdown: dict


class UserListItem(BaseModel):
    id: int
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    plan: str
    is_guest: bool
    is_active: bool
    analyses_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class UserListResponse(BaseModel):
    users: List[UserListItem]
    total: int
    page: int
    page_size: int


class AnalysisHistoryItem(BaseModel):
    id: int
    user_id: Optional[int] = None
    user_email: Optional[str] = None
    success_score: Optional[float] = None
    bid_decision: Optional[str] = None
    competition_level: Optional[str] = None
    client_trust_level: Optional[str] = None
    proposal_generated: bool
    ai_provider_used: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisHistoryResponse(BaseModel):
    analyses: List[AnalysisHistoryItem]
    total: int
    page: int
    page_size: int


class PlanResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    price_monthly: float
    analyses_limit: int
    proposals_limit: int
    is_active: bool

    model_config = {"from_attributes": True}


class PlanUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price_monthly: Optional[float] = Field(default=None, ge=0)
    analyses_limit: Optional[int] = Field(default=None, ge=0)
    proposals_limit: Optional[int] = Field(default=None, ge=0)
    is_active: Optional[bool] = None


class UserPlanUpdateRequest(BaseModel):
    plan: str = Field(description="Plan slug: free, pro, enterprise")
