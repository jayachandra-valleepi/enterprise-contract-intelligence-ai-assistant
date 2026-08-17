from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import Feedback


class FeedbackRepository:
    """
    Repository for RAG answer feedback.
    """

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------------
    # Create feedback
    # --------------------------------------------------------------

    def create(
        self,
        message_id: int,
        user_id: int,
        rating: int,
        comment: Optional[str] = None,
    ) -> Feedback:

        if rating < 1 or rating > 5:
            raise ValueError(
                "Rating must be between 1 and 5."
            )

        feedback = Feedback(
            message_id=message_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
        )

        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)

        return feedback

    # --------------------------------------------------------------
    # Get feedback by message
    # --------------------------------------------------------------

    def get_by_message(
        self,
        message_id: int,
    ) -> list[Feedback]:

        statement = (
            select(Feedback)
            .where(
                Feedback.message_id == message_id
            )
            .order_by(
                Feedback.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Get feedback by user
    # --------------------------------------------------------------

    def get_by_user(
        self,
        user_id: int,
    ) -> list[Feedback]:

        statement = (
            select(Feedback)
            .where(
                Feedback.user_id == user_id
            )
            .order_by(
                Feedback.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )