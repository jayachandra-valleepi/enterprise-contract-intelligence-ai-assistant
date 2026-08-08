from sqlalchemy import text
from sqlalchemy.orm import Session


class RBACService:

    def __init__(self, db: Session):
        self.db = db

    # -----------------------------------------------------
    # GET USER PERMISSIONS
    # -----------------------------------------------------

    def get_user_permissions(self, email: str):

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

    # -----------------------------------------------------
    # CHECK COUNTRY ACCESS
    # -----------------------------------------------------

    def has_country_access(
        self,
        email: str,
        country: str
    ) -> bool:

        user = self.get_user_permissions(email)

        if not user:
            return False

        # Admin can access all countries
        if user["role"].lower() == "admin":
            return True

        # Normal user can access assigned country
        if user["country"].lower() == country.lower():
            return True

        return False

    # -----------------------------------------------------
    # CHECK ROLE
    # -----------------------------------------------------

    def has_role(
        self,
        email: str,
        required_role: str
    ) -> bool:

        user = self.get_user_permissions(email)

        if not user:
            return False

        return (
            user["role"].lower()
            == required_role.lower()
        )