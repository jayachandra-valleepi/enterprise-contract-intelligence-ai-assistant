from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import AuditLog


class AuditRepository:
    """
    Repository for application audit logs.
    """

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------------
    # Create audit log
    # --------------------------------------------------------------

    def create(
        self,
        user_id: int,
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        status: str = "SUCCESS",
    ) -> AuditLog:

        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            status=status,
        )

        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)

        return audit_log

    # --------------------------------------------------------------
    # Get logs for one user
    # --------------------------------------------------------------

    def get_by_user(
        self,
        user_id: int,
    ) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.user_id == user_id
            )
            .order_by(
                AuditLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Get logs by action
    # --------------------------------------------------------------

    def get_by_action(
        self,
        action: str,
    ) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .where(
                AuditLog.action == action
            )
            .order_by(
                AuditLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Get all logs
    # --------------------------------------------------------------

    def get_all(self) -> list[AuditLog]:

        statement = (
            select(AuditLog)
            .order_by(
                AuditLog.created_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )