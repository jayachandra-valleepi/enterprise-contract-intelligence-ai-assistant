from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from backend.app.config.settings import settings

def create_access_token(
        user_id:int,
        email:str,
        role:str,
) -> str:

    """
    Create a JWT access token for an authenticated user.
    """

    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "iat": now,
        "exp": expires_at,
        "type": "access",
    }


    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    return token



def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Raises:
        ValueError: If the token is invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        if payload.get("type") != "access":
            raise ValueError("Invalid token type.")

        if payload.get("sub") is None:
            raise ValueError("Token does not contain user ID.")

        return payload

    except JWTError as exc:
        raise ValueError(
            "Invalid or expired access token."
        ) from exc