# backend/app/security/rbac.py

from fastapi import HTTPException, status

from backend.app.database.models import User
from backend.app.security.permissions import has_permission


# ============================================================
# REQUIRE ROLE
# ============================================================

def require_role(
    user: User,
    allowed_roles: set[str],
) -> User:
    """
    Allow access only when the user's role is in allowed_roles.
    """

    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    return user


# ============================================================
# REQUIRE PERMISSION
# ============================================================

def require_permission(
    user: User,
    permission: str,
) -> User:
    """
    Allow access only when the user's role
    contains the requested permission.
    """

    if not has_permission(
        user.role,
        permission,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    return user