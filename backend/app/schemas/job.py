from typing import Optional

from pydantic import BaseModel, Field


class ClientInfoInput(BaseModel):
    payment_verified: Optional[bool] = None
    client_spending: Optional[float] = Field(default=None, ge=0)
    client_hire_rate: Optional[float] = Field(default=None, ge=0, le=100)
    total_jobs_posted: Optional[int] = Field(default=None, ge=0)
    average_hourly_rate: Optional[float] = Field(default=None, ge=0)
    total_hires: Optional[int] = Field(default=None, ge=0)
    client_location: Optional[str] = Field(default=None, max_length=255)
    proposal_count: Optional[int] = Field(default=None, ge=0)
    connect_cost: Optional[int] = Field(default=None, ge=0)


class JobAnalysisRequest(BaseModel):
    job_description: str = Field(min_length=10)
    client_info: ClientInfoInput
    generate_proposal: bool = True


class ConnectStrategyResponse(BaseModel):
    minimum_connects: int
    recommended_connects: int
    maximum_connects: int
    warning: Optional[str] = None


class CompetitionAnalysisResponse(BaseModel):
    proposal_count: Optional[int] = None
    competition_level: str
    visibility_chance: str
    recommended_submission_timing: str


class ClientAnalysisResponse(BaseModel):
    trust_level: str
    payment_verified: Optional[bool] = None
    total_spending: Optional[float] = None
    hiring_history: str
    active_jobs_info: str
    review_history: str
    summary: str


class BidRecommendationResponse(BaseModel):
    decision: str
    reasoning: str


class SuccessScoreResponse(BaseModel):
    score: float
    color: str
    label: str


class JobAnalysisResponse(BaseModel):
    id: int
    success_score: SuccessScoreResponse
    bid_recommendation: BidRecommendationResponse
    connect_strategy: ConnectStrategyResponse
    competition_analysis: CompetitionAnalysisResponse
    client_analysis: ClientAnalysisResponse
    extracted_job_info: Optional[str] = None
    proposal_text: Optional[str] = None
    ai_provider_used: str
    processing_time_ms: int

    model_config = {"from_attributes": True}


class ProposalGenerateRequest(BaseModel):
    analysis_id: int
    freelancer_name: Optional[str] = None
    freelancer_skills: Optional[str] = None
    freelancer_experience: Optional[str] = None


class ProposalResponse(BaseModel):
    analysis_id: int
    proposal_text: str
    ai_provider_used: str
