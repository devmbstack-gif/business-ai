from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.config.settings import get_settings
from app.core.database import SessionLocal, init_db
from app.core.exception_handlers import register_exception_handlers
from app.repositories.plan_repository import PlanRepository
from app.services.auth_service import AuthService
from app.utils.response_helpers import success_response

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        PlanRepository(db).seed_default_plans()
        AuthService(db).ensure_default_admin()
    finally:
        db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Proposal Writer and Job Success Analyzer API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
def health_check():
    return success_response(
        data={
            "app": settings.app_name,
            "version": settings.app_version,
            "database": "postgresql",
        },
        message="Service is healthy",
    )
