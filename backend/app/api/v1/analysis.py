import json
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user_optional
from app.core.exceptions import AIServiceError
from app.models.user import User
from app.schemas.job import ClientInfoInput, ProposalGenerateRequest
from app.services.analysis_service import AnalysisService
from app.utils.file_handler import save_upload_file
from app.utils.response_helpers import success_response

router = APIRouter(prefix="/analysis", tags=["Job Analysis"])


@router.post("/submit")
async def submit_job_analysis(
    job_description: str = Form(...),
    client_info: str = Form(...),
    generate_proposal: bool = Form(default=True),
    screenshot: Optional[UploadFile] = File(None),
    freelancer_name: Optional[str] = Form(default=None),
    freelancer_skills: Optional[str] = Form(default=None),
    freelancer_experience: Optional[str] = Form(default=None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    try:
        client_data = ClientInfoInput(**json.loads(client_info))
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid client_info JSON: {exc}",
        ) from exc

    screenshot_path = None
    if screenshot and screenshot.filename:
        try:
            screenshot_path = await save_upload_file(screenshot)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    service = AnalysisService(db)
    try:
        result = service.process_job_analysis(
            job_description=job_description,
            client_info=client_data,
            screenshot_path=screenshot_path,
            user=current_user,
            generate_proposal=generate_proposal,
            freelancer_name=freelancer_name,
            freelancer_skills=freelancer_skills,
            freelancer_experience=freelancer_experience,
        )
        message = "Job analysis completed successfully"
        if generate_proposal and not result.proposal_text:
            message = "Job analysis completed, but proposal could not be generated"
        return success_response(
            data=result.model_dump(),
            message=message,
        )
    except AIServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    service = AnalysisService(db)
    result = service.get_analysis_by_id(analysis_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return success_response(
        data=result.model_dump(),
        message="Analysis fetched successfully",
    )


@router.post("/proposal/generate")
def generate_proposal(
    payload: ProposalGenerateRequest,
    db: Session = Depends(get_db),
):
    service = AnalysisService(db)
    try:
        analysis, proposal_text, provider = service.generate_proposal_for_analysis(
            analysis_id=payload.analysis_id,
            freelancer_name=payload.freelancer_name,
            freelancer_skills=payload.freelancer_skills,
            freelancer_experience=payload.freelancer_experience,
        )
        return success_response(
            data={
                "analysis_id": analysis.id,
                "proposal_text": proposal_text,
                "ai_provider_used": provider,
            },
            message="Proposal generated successfully",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except AIServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
