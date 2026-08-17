from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models import Permission

class PermissionRepository:
    """
    Repository for the existing permissions table.
    """

    def __init__(self, db: Session):
        self.db = db

    # --------------------------------------------------------------
    # Get all permissions for a role
    # --------------------------------------------------------------

    def get_permissions_by_role(
        self,
        role: str,
    ) -> list[Permission]:

        statement = (
            select(Permission)
            .where(Permission.role == role)
            .order_by(Permission.permission_name)
        )

        return list(
            self.db.scalars(statement).all()
        )

    # --------------------------------------------------------------
    # Check whether role has permission
    # --------------------------------------------------------------

    def has_permission(
        self,
        role: str,
        permission_name: str,
    ) -> bool:

        statement = select(Permission).where(
            Permission.role == role,
            Permission.permission_name == permission_name,
        )

        permission = self.db.scalar(statement)

        return permission is not None

    # --------------------------------------------------------------
    # Get permission names
    # --------------------------------------------------------------

    def get_permission_names(
        self,
        role: str,
    ) -> list[str]:

        statement = select(
            Permission.permission_name
        ).where(
            Permission.role == role
        )

        return list(
            self.db.scalars(statement).all()
        )