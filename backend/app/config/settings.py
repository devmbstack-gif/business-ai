from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Business AI"
    app_version: str = "1.0.0"
    debug: bool = False
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/business_ai"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    upload_dir: str = "uploads"
    max_upload_size_mb: int = 10
    allowed_image_types: List[str] = ["image/jpeg", "image/png", "image/webp"]

    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    admin_email: str = "admin@businessai.com"
    admin_password: str = "admin123"


@lru_cache
def get_settings() -> Settings:
    return Settings()
