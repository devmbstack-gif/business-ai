from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.user import User
from app.schemas.admin import PlanUpdateRequest, UserPlanUpdateRequest
from app.services.admin_service import AdminService
from app.utils.response_helpers import success_response

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    result = service.get_dashboard_stats()
    return success_response(
        data=result.model_dump(),
        message="Dashboard stats fetched successfully",
    )


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    result = service.list_users(page=page, page_size=page_size)
    return success_response(
        data=result.model_dump(),
        message="Users fetched successfully",
    )


@router.get("/analyses")
def list_analyses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    result = service.list_analyses(page=page, page_size=page_size)
    return success_response(
        data=result.model_dump(),
        message="Analysis history fetched successfully",
    )


@router.get("/plans")
def list_plans(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    plans = service.list_plans()
    return success_response(
        data=[plan.model_dump() for plan in plans],
        message="Plans fetched successfully",
    )


@router.patch("/plans/{plan_id}")
def update_plan(
    plan_id: int,
    payload: PlanUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    try:
        result = service.update_plan(plan_id, payload.model_dump(exclude_none=True))
        return success_response(
            data=result.model_dump(),
            message="Plan updated successfully",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/users/{user_id}/plan")
def update_user_plan(
    user_id: int,
    payload: UserPlanUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
):
    service = AdminService(db)
    try:
        result = service.update_user_plan(user_id, payload.plan)
        return success_response(
            data=result.model_dump(),
            message="User plan updated successfully",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
