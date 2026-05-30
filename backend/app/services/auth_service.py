import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config.settings import get_settings
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository

settings = get_settings()


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    def create_access_token(self, user_id: int, is_guest: bool = False) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        payload = {"sub": str(user_id), "exp": expire, "is_guest": is_guest}
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

    def get_user_from_token(self, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            user_id = int(payload.get("sub", 0))
            if not user_id:
                return None
            user = self.user_repo.get_by_id(user_id)
            if user and user.is_active:
                return user
            return None
        except (JWTError, ValueError):
            return None

    def register(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        existing = self.user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        return self.user_repo.create(
            {
                "email": email,
                "hashed_password": self.hash_password(password),
                "full_name": full_name,
                "role": UserRole.USER,
                "is_guest": False,
            }
        )

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not user.hashed_password:
            raise ValueError("Invalid email or password")
        if not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")
        if not user.is_active:
            raise ValueError("Account is deactivated")
        return user

    def create_guest_session(self, guest_session_id: Optional[str] = None) -> User:
        session_id = guest_session_id or uuid.uuid4().hex
        existing = self.user_repo.get_by_guest_session(session_id)
        if existing:
            return existing
        return self.user_repo.create(
            {
                "guest_session_id": session_id,
                "role": UserRole.GUEST,
                "is_guest": True,
            }
        )

    def ensure_default_admin(self) -> None:
        self.user_repo.ensure_admin_exists(
            settings.admin_email,
            self.hash_password(settings.admin_password),
        )
