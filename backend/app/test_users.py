from backend.app.database.connection import SessionLocal
from backend.app.database.repositories.user_repository import UserRepository


def test_users():

    db = SessionLocal()

    try:
        repository = UserRepository(db)

        user = repository.get_by_email(
            "jay.kumar@company.com"
        )

        if user:
            print("User found!")
            print("ID:", user.user_id)
            print("Name:", user.full_name)
            print("Email:", user.email)
            print("Role:", user.role)
            print("Department:", user.department)
            print("Active:", user.is_active)

        else:
            print("User not found!")

    except Exception as e:
        print("User query failed!")
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    test_users()