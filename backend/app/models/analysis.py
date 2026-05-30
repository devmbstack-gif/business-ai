import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class BidDecision(str, enum.Enum):
    RECOMMENDED = "recommended_to_bid"
    CAUTION = "bid_with_caution"
    SKIP = "skip_this_job"


class ClientTrustLevel(str, enum.Enum):
    TRUSTED = "trusted"
    MODERATE_RISK = "moderate_risk"
    HIGH_RISK = "high_risk"


class CompetitionLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ScoreColor(str, enum.Enum):
    GREEN = "green"
    LIGHT_GREEN = "light_green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    screenshot_path: Mapped[str | None] = mapped_column(String(500), nullable=True)

    payment_verified: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    client_spending: Mapped[float | None] = mapped_column(Float, nullable=True)
    client_hire_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_jobs_posted: Mapped[int | None] = mapped_column(Integer, nullable=True)
    average_hourly_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    total_hires: Mapped[int | None] = mapped_column(Integer, nullable=True)
    client_location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    proposal_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    connect_cost: Mapped[int | None] = mapped_column(Integer, nullable=True)

    success_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    score_color: Mapped[ScoreColor | None] = mapped_column(Enum(ScoreColor), nullable=True)
    bid_decision: Mapped[BidDecision | None] = mapped_column(Enum(BidDecision), nullable=True)
    bid_reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    min_connects: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recommended_connects: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_connects: Mapped[int | None] = mapped_column(Integer, nullable=True)
    connect_warning: Mapped[str | None] = mapped_column(String(500), nullable=True)

    competition_level: Mapped[CompetitionLevel | None] = mapped_column(Enum(CompetitionLevel), nullable=True)
    visibility_chance: Mapped[str | None] = mapped_column(String(100), nullable=True)
    submission_timing: Mapped[str | None] = mapped_column(String(255), nullable=True)

    client_trust_level: Mapped[ClientTrustLevel | None] = mapped_column(Enum(ClientTrustLevel), nullable=True)
    client_analysis_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    extracted_job_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_analysis_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_provider_used: Mapped[str | None] = mapped_column(String(50), nullable=True)

    proposal_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    proposal_generated: Mapped[bool] = mapped_column(Boolean, default=False)

    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="analyses")
