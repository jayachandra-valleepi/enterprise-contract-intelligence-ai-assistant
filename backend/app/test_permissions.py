from backend.app.database.connection import SessionLocal
from backend.app.database.repositories.permission_repository import (
    PermissionRepository,
)


def test_permissions():

    db = SessionLocal()

    try:
        repository = PermissionRepository(db)

        permissions = repository.get_permission_names(
            "Admin"
        )

        print("Admin permissions:")

        for permission in permissions:
            print("-", permission)

        allowed = repository.has_permission(
            role="Admin",
            permission_name="ASK_QUESTION",
        )

        print()
        print(
            "Admin can ask question:",
            allowed,
        )

    except Exception as e:
        print("Permission query failed!")
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    test_permissions()