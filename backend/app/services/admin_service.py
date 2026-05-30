from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.analysis import JobAnalysis
from app.repositories.analysis_repository import AnalysisRepository
from app.repositories.plan_repository import PlanRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    AnalysisHistoryItem,
    AnalysisHistoryResponse,
    DailyUsageItem,
    DashboardStatsResponse,
    PlanResponse,
    ScoreDistributionItem,
    UserListItem,
    UserListResponse,
)
from app.models.user import PlanType


class AdminService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.analysis_repo = AnalysisRepository(db)
        self.plan_repo = PlanRepository(db)

    def get_dashboard_stats(self) -> DashboardStatsResponse:
        daily = self.analysis_repo.get_daily_usage(days=7)
        distribution = self.analysis_repo.get_score_distribution()

        week_count = (
            self.db.query(func.count(JobAnalysis.id))
            .filter(JobAnalysis.created_at >= func.current_date() - 7)
            .scalar()
            or 0
        )

        month_count = (
            self.db.query(func.count(JobAnalysis.id))
            .filter(JobAnalysis.created_at >= func.current_date() - 30)
            .scalar()
            or 0
        )

        return DashboardStatsResponse(
            total_users=self.user_repo.count_total(),
            total_analyses=self.analysis_repo.count_total(),
            total_proposals_generated=self.analysis_repo.count_proposals_generated(),
            total_guest_sessions=self.user_repo.count_guests(),
            analyses_today=self.analysis_repo.count_today(),
            analyses_this_week=week_count,
            analyses_this_month=month_count,
            average_success_score=self.analysis_repo.average_success_score(),
            daily_usage=[DailyUsageItem(**item) for item in daily],
            score_distribution=[ScoreDistributionItem(**item) for item in distribution],
            ai_provider_breakdown=self.analysis_repo.get_ai_provider_breakdown(),
        )

    def list_users(self, page: int = 1, page_size: int = 20) -> UserListResponse:
        users, total = self.user_repo.list_all(page, page_size)
        items = []
        for user in users:
            items.append(
                UserListItem(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    role=user.role.value,
                    plan=user.plan.value,
                    is_guest=user.is_guest,
                    is_active=user.is_active,
                    analyses_count=self.user_repo.count_analyses_for_user(user.id),
                    created_at=user.created_at,
                )
            )
        return UserListResponse(users=items, total=total, page=page, page_size=page_size)

    def list_analyses(self, page: int = 1, page_size: int = 20) -> AnalysisHistoryResponse:
        analyses, total = self.analysis_repo.list_all(page, page_size)
        items = []
        for analysis in analyses:
            user_email = None
            if analysis.user_id:
                user = self.user_repo.get_by_id(analysis.user_id)
                user_email = user.email if user else None

            items.append(
                AnalysisHistoryItem(
                    id=analysis.id,
                    user_id=analysis.user_id,
                    user_email=user_email,
                    success_score=analysis.success_score,
                    bid_decision=analysis.bid_decision.value if analysis.bid_decision else None,
                    competition_level=analysis.competition_level.value if analysis.competition_level else None,
                    client_trust_level=analysis.client_trust_level.value if analysis.client_trust_level else None,
                    proposal_generated=analysis.proposal_generated,
                    ai_provider_used=analysis.ai_provider_used,
                    created_at=analysis.created_at,
                )
            )
        return AnalysisHistoryResponse(analyses=items, total=total, page=page, page_size=page_size)

    def list_plans(self) -> list[PlanResponse]:
        plans = self.plan_repo.list_all()
        return [PlanResponse.model_validate(plan) for plan in plans]

    def update_plan(self, plan_id: int, data: dict) -> PlanResponse:
        plan = self.plan_repo.get_by_id(plan_id)
        if not plan:
            raise ValueError("Plan not found")
        updated = self.plan_repo.update(plan, data)
        return PlanResponse.model_validate(updated)

    def update_user_plan(self, user_id: int, plan_slug: str) -> UserListItem:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        plan_map = {
            "free": PlanType.FREE,
            "pro": PlanType.PRO,
            "enterprise": PlanType.ENTERPRISE,
        }
        plan_type = plan_map.get(plan_slug.lower())
        if not plan_type:
            raise ValueError("Invalid plan slug")

        updated = self.user_repo.update_plan(user, plan_type)
        return UserListItem(
            id=updated.id,
            email=updated.email,
            full_name=updated.full_name,
            role=updated.role.value,
            plan=updated.plan.value,
            is_guest=updated.is_guest,
            is_active=updated.is_active,
            analyses_count=self.user_repo.count_analyses_for_user(updated.id),
            created_at=updated.created_at,
        )
