from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import User

class UserRepository:
    """
    Repository for the existing users table.
    """

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------------
    # Get user by ID
    # --------------------------------------------------------------

    def get_by_id(
        self,
        user_id: int,
    ) -> Optional[User]:

        statement = select(User).where(
            User.user_id == user_id
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get user by email
    # --------------------------------------------------------------

    def get_by_email(
        self,
        email: str,
    ) -> Optional[User]:

        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get active user
    # --------------------------------------------------------------

    def get_active_user(
        self,
        user_id: int,
    ) -> Optional[User]:

        statement = select(User).where(
            User.user_id == user_id,
            User.is_active.is_(True),
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get users by role
    # --------------------------------------------------------------

    def get_by_role(
        self,
        role: str,
    ) -> list[User]:

        statement = (
            select(User)
            .where(User.role == role)
            .order_by(User.full_name)
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Update last login
    # --------------------------------------------------------------

    def update_last_login(
        self,
        user_id: int,
    ) -> Optional[User]:

        user = self.get_by_id(user_id)

        if user is None:
            return None

        from datetime import datetime, timezone

        user.last_login = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(user)

        return user