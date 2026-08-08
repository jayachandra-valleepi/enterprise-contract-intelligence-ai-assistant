from sqlalchemy import text
from sqlalchemy.orm import Session


class AuthenticationService:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------------
    # CHECK USER ACCESS
    # -----------------------------------------------------

    def authenticate_user(self, email: str):

        query = text("""
            SELECT
                email,
                name,
                country,
                role,
                is_active
            FROM bot_access
            WHERE email = :email
        """)

        result = self.db.execute(
            query,
            {
                "email": email
            }
        ).fetchone()

        if not result:
            return None

        if not result.is_active:
            return None

        return {
            "email": result.email,
            "name": result.name,
            "country": result.country,
            "role": result.role,
            "is_active": result.is_active
        }