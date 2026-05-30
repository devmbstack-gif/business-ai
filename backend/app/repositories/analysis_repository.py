import json
from typing import Any, Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.analysis import JobAnalysis
from app.models.user import User


class AnalysisRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> JobAnalysis:
        analysis = JobAnalysis(**data)
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_by_id(self, analysis_id: int) -> Optional[JobAnalysis]:
        return self.db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id).first()

    def update(self, analysis: JobAnalysis, data: dict) -> JobAnalysis:
        for key, value in data.items():
            setattr(analysis, key, value)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def list_all(self, page: int = 1, page_size: int = 20) -> tuple[list[JobAnalysis], int]:
        query = self.db.query(JobAnalysis).order_by(desc(JobAnalysis.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def count_total(self) -> int:
        return self.db.query(func.count(JobAnalysis.id)).scalar() or 0

    def count_proposals_generated(self) -> int:
        return (
            self.db.query(func.count(JobAnalysis.id))
            .filter(JobAnalysis.proposal_generated.is_(True))
            .scalar()
            or 0
        )

    def count_today(self) -> int:
        return (
            self.db.query(func.count(JobAnalysis.id))
            .filter(func.date(JobAnalysis.created_at) == func.current_date())
            .scalar()
            or 0
        )

    def average_success_score(self) -> float:
        result = self.db.query(func.avg(JobAnalysis.success_score)).scalar()
        return round(float(result or 0), 2)

    def get_score_distribution(self) -> list[dict[str, Any]]:
        ranges = [
            ("90-100", 90, 100),
            ("70-89", 70, 89.99),
            ("50-69", 50, 69.99),
            ("30-49", 30, 49.99),
            ("0-29", 0, 29.99),
        ]
        total = self.count_total() or 1
        distribution = []
        for label, low, high in ranges:
            count = (
                self.db.query(func.count(JobAnalysis.id))
                .filter(JobAnalysis.success_score >= low, JobAnalysis.success_score <= high)
                .scalar()
                or 0
            )
            distribution.append(
                {
                    "range_label": label,
                    "count": count,
                    "percentage": round((count / total) * 100, 1),
                }
            )
        return distribution

    def get_ai_provider_breakdown(self) -> dict[str, int]:
        rows = (
            self.db.query(JobAnalysis.ai_provider_used, func.count(JobAnalysis.id))
            .group_by(JobAnalysis.ai_provider_used)
            .all()
        )
        return {provider or "unknown": count for provider, count in rows}

    def get_daily_usage(self, days: int = 7) -> list[dict[str, Any]]:
        results = []
        for day_offset in range(days - 1, -1, -1):
            date_expr = func.date(func.current_date()) - day_offset
            analyses_count = (
                self.db.query(func.count(JobAnalysis.id))
                .filter(func.date(JobAnalysis.created_at) == date_expr)
                .scalar()
                or 0
            )
            proposals_count = (
                self.db.query(func.count(JobAnalysis.id))
                .filter(
                    func.date(JobAnalysis.created_at) == date_expr,
                    JobAnalysis.proposal_generated.is_(True),
                )
                .scalar()
                or 0
            )
            results.append(
                {
                    "date": str(date_expr),
                    "analyses_count": analyses_count,
                    "proposals_count": proposals_count,
                }
            )
        return results

    def store_full_analysis(self, analysis: JobAnalysis, payload: dict) -> JobAnalysis:
        analysis.full_analysis_json = json.dumps(payload)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis
