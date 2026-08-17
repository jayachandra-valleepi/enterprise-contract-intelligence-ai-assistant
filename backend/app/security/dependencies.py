from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.database.connection import get_db
from backend.app.database.models import User
from backend.app.database.repositories.user_repository import UserRepository
from backend.app.security.jwt import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    Authenticate the current user.

    Steps:

    1. Extract JWT from Authorization header.
    2. Decode JWT.
    3. Get user_id from token.
    4. Query existing users table.
    5. Verify user is active.
    """

    try:
        payload = decode_access_token(token)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    try:
        user_id = int(user_id)

    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        ) from exc

    user_repository = UserRepository(db)

    user = user_repository.get_active_user(
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist or is inactive.",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    return user