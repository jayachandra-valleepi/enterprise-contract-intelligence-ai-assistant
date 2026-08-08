from typing import Optional, List

from sqlalchemy.orm import Session

from app.database.models import UserChatHistory


class UserChatRepository:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------------
    # SAVE CHAT
    # -----------------------------------------------------

    def save_chat(
        self,
        user_email: str,
        user_name: Optional[str],
        country: Optional[str],
        role: Optional[str],
        session_id: Optional[str],
        user_question: str,
        bot_response: Optional[str],
        response_time: Optional[int] = None,
        is_success: bool = True
    ):

        chat = UserChatHistory(
            user_email=user_email,
            user_name=user_name,
            country=country,
            role=role,
            session_id=session_id,
            user_question=user_question,
            bot_response=bot_response,
            response_time=response_time,
            is_success=is_success
        )

        self.db.add(chat)
        self.db.commit()
        self.db.refresh(chat)

        return chat

    # -----------------------------------------------------
    # GET USER CHAT HISTORY
    # -----------------------------------------------------

    def get_user_chat_history(
        self,
        user_email: str,
        limit: int = 20
    ) -> List[UserChatHistory]:

        return (
            self.db.query(UserChatHistory)
            .filter(
                UserChatHistory.user_email == user_email
            )
            .order_by(
                UserChatHistory.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # -----------------------------------------------------
    # GET SESSION HISTORY
    # -----------------------------------------------------

    def get_session_history(
        self,
        user_email: str,
        session_id: str
    ) -> List[UserChatHistory]:

        return (
            self.db.query(UserChatHistory)
            .filter(
                UserChatHistory.user_email == user_email,
                UserChatHistory.session_id == session_id
            )
            .order_by(
                UserChatHistory.created_at.asc()
            )
            .all()
        )

    # -----------------------------------------------------
    # DELETE USER CHAT HISTORY
    # -----------------------------------------------------

    def delete_user_history(
        self,
        user_email: str
    ):

        self.db.query(UserChatHistory).filter(
            UserChatHistory.user_email == user_email
        ).delete(
            synchronize_session=False
        )

        self.db.commit()