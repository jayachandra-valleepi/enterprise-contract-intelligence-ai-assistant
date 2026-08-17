
from passlib.context import CryptContext


# ============================================================
# PASSWORD HASHING CONFIGURATION
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(password: str) -> str:
    """
    Convert a plain-text password into a secure password hash.

    The plain-text password should never be stored in the database.
    """

    return pwd_context.hash(password)


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a stored hash.
    """

    return pwd_context.verify(
        plain_password,
        hashed_password,
    )