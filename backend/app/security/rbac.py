from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.database.models import User
from backend.app.database.repositories.permission_repository  import(
    PermissionRepository
)

from backend.app.security.dependencies import get_current_user
from backend.app.security.permissions import Permission


def require_permission(
    required_permission: Permission,
) -> Callable:

    def permission_checker(
        current_user: Annotated[
            User,
            Depends(get_current_user),
        ],
        db: Annotated[
            Session,
            Depends(get_db),
        ],
    ) -> User:
        """
        Verify that the current user's role has
        the required permission.
        """

        permission_repository = PermissionRepository(db)

        has_permission = (
            permission_repository.has_permission(
                role=current_user.role,
                permission_name=required_permission.value,
            )
        )

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permission denied. "
                    f"Required permission: "
                    f"{required_permission.value}"
                ),
            )

        return current_user

    return permission_checker