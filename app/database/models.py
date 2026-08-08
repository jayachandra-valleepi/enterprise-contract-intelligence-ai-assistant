from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime

from app.database.sql_server import Base


class UserChatHistory(Base):

    __tablename__ = "user_chat_history"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # -----------------------------------------------------
    # USER INFORMATION
    # -----------------------------------------------------

    user_email = Column(
        String(255),
        nullable=False,
        index=True
    )

    user_name = Column(
        String(255),
        nullable=True
    )

    country = Column(
        String(100),
        nullable=True
    )

    role = Column(
        String(100),
        nullable=True
    )

    # -----------------------------------------------------
    # CHAT INFORMATION
    # -----------------------------------------------------

    session_id = Column(
        String(100),
        nullable=True,
        index=True
    )

    user_question = Column(
        Text,
        nullable=False
    )

    bot_response = Column(
        Text,
        nullable=True
    )

    # -----------------------------------------------------
    # METADATA
    # -----------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    response_time = Column(
        Integer,
        nullable=True
    )

    is_success = Column(
        Boolean,
        default=True
    )