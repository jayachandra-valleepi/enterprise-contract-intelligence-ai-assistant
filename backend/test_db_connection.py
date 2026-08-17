from sqlalchemy import text

from backend.app.database.connection import SessionLocal


def test_database_connection():
    db = SessionLocal()

    try:
        result = db.execute(
            text("SELECT 1")
        )

        print("PostgreSQL connection successful!")
        print("Result:", result.scalar())

    except Exception as e:
        print("Database connection failed!")
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    test_database_connection()