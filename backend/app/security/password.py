from pwdlib import PasswordHash


# Argon2-based password hashing.
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.

    The returned value should be stored in the database
    instead of the original password.
    """

    return password_hash.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against a stored hash.
    """

    return password_hash.verify(
        plain_password,
        hashed_password,
    )