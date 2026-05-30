import time
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.analysis import (
    BidDecision,
    ClientTrustLevel,
    CompetitionLevel,
    JobAnalysis,
    ScoreColor,
)
from app.models.user import User
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.job import (
    BidRecommendationResponse,
    ClientAnalysisResponse,
    CompetitionAnalysisResponse,
    ConnectStrategyResponse,
    JobAnalysisResponse,
    SuccessScoreResponse,
)
from app.services.ai.ai_orchestrator import AIOrchestrator
from app.utils.score_helpers import get_score_color, get_score_label


class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.analysis_repo = AnalysisRepository(db)
        self.ai = AIOrchestrator()

    def _client_info_to_dict(self, client_info: Any) -> dict[str, Any]:
        if hasattr(client_info, "model_dump"):
            return client_info.model_dump(exclude_none=True)
        return client_info

    def _map_bid_decision(self, value: str) -> BidDecision:
        mapping = {
            "recommended_to_bid": BidDecision.RECOMMENDED,
            "bid_with_caution": BidDecision.CAUTION,
            "skip_this_job": BidDecision.SKIP,
        }
        return mapping.get(value, BidDecision.CAUTION)

    def _map_trust_level(self, value: str) -> ClientTrustLevel:
        mapping = {
            "trusted": ClientTrustLevel.TRUSTED,
            "moderate_risk": ClientTrustLevel.MODERATE_RISK,
            "high_risk": ClientTrustLevel.HIGH_RISK,
        }
        return mapping.get(value, ClientTrustLevel.MODERATE_RISK)

    def _map_competition_level(self, value: str) -> CompetitionLevel:
        mapping = {
            "low": CompetitionLevel.LOW,
            "medium": CompetitionLevel.MEDIUM,
            "high": CompetitionLevel.HIGH,
            "very_high": CompetitionLevel.VERY_HIGH,
        }
        return mapping.get(value, CompetitionLevel.MEDIUM)

    def _build_response(self, analysis: JobAnalysis) -> JobAnalysisResponse:
        score = analysis.success_score or 0
        color = analysis.score_color or get_score_color(score)

        connect = ConnectStrategyResponse(
            minimum_connects=analysis.min_connects or 0,
            recommended_connects=analysis.recommended_connects or 0,
            maximum_connects=analysis.max_connects or 0,
            warning=analysis.connect_warning,
        )

        competition = CompetitionAnalysisResponse(
            proposal_count=analysis.proposal_count,
            competition_level=analysis.competition_level.value if analysis.competition_level else "medium",
            visibility_chance=analysis.visibility_chance or "Unknown",
            recommended_submission_timing=analysis.submission_timing or "Submit within 24 hours",
        )

        client = ClientAnalysisResponse(
            trust_level=analysis.client_trust_level.value if analysis.client_trust_level else "moderate_risk",
            payment_verified=analysis.payment_verified,
            total_spending=analysis.client_spending,
            hiring_history=f"Hire rate: {analysis.client_hire_rate or 'N/A'}%, Total hires: {analysis.total_hires or 'N/A'}",
            active_jobs_info=f"Total jobs posted: {analysis.total_jobs_posted or 'N/A'}",
            review_history=analysis.client_analysis_summary or "No detailed review data available",
            summary=analysis.client_analysis_summary or "Client assessment pending",
        )

        bid = BidRecommendationResponse(
            decision=analysis.bid_decision.value if analysis.bid_decision else "bid_with_caution",
            reasoning=analysis.bid_reasoning or "Analysis completed",
        )

        return JobAnalysisResponse(
            id=analysis.id,
            success_score=SuccessScoreResponse(
                score=score,
                color=color.value,
                label=get_score_label(score),
            ),
            bid_recommendation=bid,
            connect_strategy=connect,
            competition_analysis=competition,
            client_analysis=client,
            extracted_job_info=analysis.extracted_job_info,
            proposal_text=analysis.proposal_text,
            ai_provider_used=analysis.ai_provider_used or "unknown",
            processing_time_ms=analysis.processing_time_ms or 0,
        )

    def process_job_analysis(
        self,
        job_description: str,
        client_info: Any,
        screenshot_path: Optional[str] = None,
        user: Optional[User] = None,
        generate_proposal: bool = True,
    ) -> JobAnalysisResponse:
        start = time.time()
        client_dict = self._client_info_to_dict(client_info)

        ai_result = self.ai.analyze_job(
            job_description=job_description,
            client_info=client_dict,
            screenshot_path=screenshot_path,
        )

        connect = ai_result.get("connect_strategy", {})
        competition = ai_result.get("competition_analysis", {})
        client_analysis = ai_result.get("client_analysis", {})

        success_score = float(ai_result.get("success_score", 50))
        score_color = get_score_color(success_score)

        analysis_data = {
            "user_id": user.id if user else None,
            "job_description": job_description,
            "screenshot_path": screenshot_path,
            "payment_verified": client_dict.get("payment_verified"),
            "client_spending": client_dict.get("client_spending"),
            "client_hire_rate": client_dict.get("client_hire_rate"),
            "total_jobs_posted": client_dict.get("total_jobs_posted"),
            "average_hourly_rate": client_dict.get("average_hourly_rate"),
            "total_hires": client_dict.get("total_hires"),
            "client_location": client_dict.get("client_location"),
            "proposal_count": client_dict.get("proposal_count") or competition.get("proposal_count"),
            "connect_cost": client_dict.get("connect_cost"),
            "success_score": success_score,
            "score_color": score_color,
            "bid_decision": self._map_bid_decision(ai_result.get("bid_decision", "bid_with_caution")),
            "bid_reasoning": ai_result.get("bid_reasoning"),
            "min_connects": connect.get("minimum_connects"),
            "recommended_connects": connect.get("recommended_connects"),
            "max_connects": connect.get("maximum_connects"),
            "connect_warning": connect.get("warning"),
            "competition_level": self._map_competition_level(
                competition.get("competition_level", "medium")
            ),
            "visibility_chance": competition.get("visibility_chance"),
            "submission_timing": competition.get("recommended_submission_timing"),
            "client_trust_level": self._map_trust_level(
                client_analysis.get("trust_level", "moderate_risk")
            ),
            "client_analysis_summary": client_analysis.get("summary"),
            "extracted_job_info": ai_result.get("extracted_job_info"),
            "ai_provider_used": ai_result.get("ai_provider_used"),
            "proposal_text": ai_result.get("proposal_text") if generate_proposal else None,
            "proposal_generated": bool(ai_result.get("proposal_text")) and generate_proposal,
            "processing_time_ms": int((time.time() - start) * 1000),
        }

        analysis = self.analysis_repo.create(analysis_data)
        self.analysis_repo.store_full_analysis(analysis, ai_result)

        return self._build_response(analysis)

    def generate_proposal_for_analysis(
        self,
        analysis_id: int,
        freelancer_name: Optional[str] = None,
        freelancer_skills: Optional[str] = None,
        freelancer_experience: Optional[str] = None,
    ) -> tuple[JobAnalysis, str, str]:
        analysis = self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise ValueError("Analysis not found")

        client_info = {
            "payment_verified": analysis.payment_verified,
            "client_spending": analysis.client_spending,
            "client_hire_rate": analysis.client_hire_rate,
            "total_jobs_posted": analysis.total_jobs_posted,
            "average_hourly_rate": analysis.average_hourly_rate,
            "total_hires": analysis.total_hires,
            "client_location": analysis.client_location,
            "proposal_count": analysis.proposal_count,
            "connect_cost": analysis.connect_cost,
        }

        freelancer_profile = {}
        if freelancer_name:
            freelancer_profile["name"] = freelancer_name
        if freelancer_skills:
            freelancer_profile["skills"] = freelancer_skills
        if freelancer_experience:
            freelancer_profile["experience"] = freelancer_experience

        analysis_context = {
            "success_score": analysis.success_score,
            "bid_decision": analysis.bid_decision.value if analysis.bid_decision else None,
            "extracted_job_info": analysis.extracted_job_info,
        }

        result = self.ai.generate_proposal(
            job_description=analysis.job_description,
            client_info=client_info,
            analysis_context=analysis_context,
            freelancer_profile=freelancer_profile or None,
        )

        proposal_text = result.get("proposal_text", "")
        provider = result.get("ai_provider_used", "unknown")

        self.analysis_repo.update(
            analysis,
            {
                "proposal_text": proposal_text,
                "proposal_generated": True,
                "ai_provider_used": provider,
            },
        )

        return analysis, proposal_text, provider

    def get_analysis_by_id(self, analysis_id: int) -> Optional[JobAnalysisResponse]:
        analysis = self.analysis_repo.get_by_id(analysis_id)
        if not analysis:
            return None
        return self._build_response(analysis)
