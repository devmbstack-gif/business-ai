from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import (
    GuestSessionRequest,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.services.auth_service import AuthService
from app.utils.response_helpers import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.register(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
        )
        token = auth_service.create_access_token(user.id)
        return success_response(
            data={
                "access_token": token,
                "token_type": "bearer",
                "user_id": user.id,
                "is_guest": False,
                "is_admin": user.is_admin,
            },
            message="Registration successful",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login")
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    try:
        user = auth_service.login(payload.email, payload.password)
        token = auth_service.create_access_token(user.id)
        return success_response(
            data={
                "access_token": token,
                "token_type": "bearer",
                "user_id": user.id,
                "is_guest": False,
                "is_admin": user.is_admin,
            },
            message="Login successful",
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/guest")
def guest_session(payload: GuestSessionRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.create_guest_session(payload.guest_session_id)
    token = auth_service.create_access_token(user.id, is_guest=True)
    return success_response(
        data={
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "is_guest": True,
            "is_admin": False,
        },
        message="Guest session created",
    )


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return success_response(
        data={
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role.value,
            "plan": current_user.plan.value,
            "is_guest": current_user.is_guest,
            "is_admin": current_user.is_admin,
            "created_at": current_user.created_at.isoformat(),
        },
        message="User profile fetched",
    )
