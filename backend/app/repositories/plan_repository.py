from typing import Optional

from sqlalchemy.orm import Session

from app.models.plan import Plan


class PlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, plan_id: int) -> Optional[Plan]:
        return self.db.query(Plan).filter(Plan.id == plan_id).first()

    def get_by_slug(self, slug: str) -> Optional[Plan]:
        return self.db.query(Plan).filter(Plan.slug == slug).first()

    def list_all(self) -> list[Plan]:
        return self.db.query(Plan).order_by(Plan.price_monthly).all()

    def update(self, plan: Plan, data: dict) -> Plan:
        for key, value in data.items():
            if value is not None:
                setattr(plan, key, value)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def seed_default_plans(self) -> None:
        defaults = [
            {
                "name": "Free",
                "slug": "free",
                "description": "Basic access with limited analyses",
                "price_monthly": 0,
                "analyses_limit": 5,
                "proposals_limit": 5,
            },
            {
                "name": "Pro",
                "slug": "pro",
                "description": "For active freelancers",
                "price_monthly": 19.99,
                "analyses_limit": 100,
                "proposals_limit": 100,
            },
            {
                "name": "Enterprise",
                "slug": "enterprise",
                "description": "Unlimited access for teams",
                "price_monthly": 49.99,
                "analyses_limit": 9999,
                "proposals_limit": 9999,
            },
        ]
        for plan_data in defaults:
            existing = self.get_by_slug(plan_data["slug"])
            if not existing:
                self.db.add(Plan(**plan_data))
        self.db.commit()
