from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import ChatMessage, Conversation

class ChatRepository:
    """
    Repository for chat conversations and messages.
    """

    def __init__(self, db: Session):
        self.db = db

    # ==============================================================
    # CONVERSATIONS
    # ==============================================================

    def create_conversation(
        self,
        user_id: int,
        title: Optional[str] = None,
        document_id: Optional[int] = None,
    ) -> Conversation:

        conversation = Conversation(
            user_id=user_id,
            title=title,
            document_id=document_id,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    # --------------------------------------------------------------
    # Get conversation
    # --------------------------------------------------------------

    def get_conversation(
        self,
        conversation_id: int,
        user_id: int,
    ) -> Optional[Conversation]:

        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == user_id,
        )

        return self.db.scalar(statement)

    # --------------------------------------------------------------
    # Get user's conversations
    # --------------------------------------------------------------

    def get_user_conversations(
        self,
        user_id: int,
    ) -> list[Conversation]:

        statement = (
            select(Conversation)
            .where(
                Conversation.user_id == user_id
            )
            .order_by(
                Conversation.updated_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Close conversation
    # --------------------------------------------------------------

    def close_conversation(
        self,
        conversation_id: int,
        user_id: int,
    ) -> Optional[Conversation]:

        conversation = self.get_conversation(
            conversation_id,
            user_id,
        )

        if conversation is None:
            return None

        conversation.is_active = False

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    # ==============================================================
    # MESSAGES
    # ==============================================================

    def add_message(
        self,
        conversation_id: int,
        user_id: int,
        role: str,
        content: str,
    ) -> ChatMessage:

        message = ChatMessage(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    # --------------------------------------------------------------
    # Get messages
    # --------------------------------------------------------------

    def get_messages(
        self,
        conversation_id: int,
        user_id: int,
    ) -> list[ChatMessage]:

        statement = (
            select(ChatMessage)
            .where(
                ChatMessage.conversation_id
                == conversation_id,
                ChatMessage.user_id == user_id,
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Add user question
    # --------------------------------------------------------------

    def add_user_question(
        self,
        conversation_id: int,
        user_id: int,
        question: str,
    ) -> ChatMessage:

        return self.add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=question,
        )

    # --------------------------------------------------------------
    # Add assistant answer
    # --------------------------------------------------------------

    def add_assistant_answer(
        self,
        conversation_id: int,
        user_id: int,
        answer: str,
    ) -> ChatMessage:

        return self.add_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=answer,
        )