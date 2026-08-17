# backend/app/security/jwt.py

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from backend.app.config.settings import settings


# ============================================================
# JWT CONFIGURATION
# ============================================================

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm


# ============================================================
# CREATE ACCESS TOKEN
# ============================================================

def create_access_token(
    data: dict[str, Any],
) -> str:
    """
    Create a JWT access token.

    The input data is copied before adding JWT-specific fields.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# CREATE REFRESH TOKEN
# ============================================================

def create_refresh_token(
    data: dict[str, Any],
) -> str:
    """
    Create a JWT refresh token.

    Refresh tokens have a longer expiration period.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )

    payload.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ============================================================
# DECODE TOKEN
# ============================================================

def decode_token(
    token: str,
) -> dict[str, Any] | None:
    """
    Decode and validate a JWT.

    Returns:
        Token payload if valid.
        None if invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        return None