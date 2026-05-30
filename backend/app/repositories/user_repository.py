from typing import Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.user import PlanType, User, UserRole


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_guest_session(self, guest_session_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.guest_session_id == guest_session_id).first()

    def create(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_all(self, page: int = 1, page_size: int = 20) -> tuple[list[User], int]:
        query = self.db.query(User).order_by(desc(User.created_at))
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        return items, total

    def count_total(self) -> int:
        return self.db.query(func.count(User.id)).scalar() or 0

    def count_guests(self) -> int:
        return self.db.query(func.count(User.id)).filter(User.is_guest.is_(True)).scalar() or 0

    def count_analyses_for_user(self, user_id: int) -> int:
        from app.models.analysis import JobAnalysis

        return (
            self.db.query(func.count(JobAnalysis.id))
            .filter(JobAnalysis.user_id == user_id)
            .scalar()
            or 0
        )

    def update_plan(self, user: User, plan: PlanType) -> User:
        user.plan = plan
        self.db.commit()
        self.db.refresh(user)
        return user

    def ensure_admin_exists(self, email: str, hashed_password: str) -> User:
        admin = self.get_by_email(email)
        if admin:
            return admin
        return self.create(
            {
                "email": email,
                "hashed_password": hashed_password,
                "full_name": "Admin",
                "role": UserRole.ADMIN,
                "is_admin": True,
                "is_guest": False,
            }
        )
