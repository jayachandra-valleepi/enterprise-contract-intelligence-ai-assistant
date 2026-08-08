from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

from app.Config.settings import settings


connection_string = (
    f"mssql+pyodbc://@{settings.SQL_SERVER}/{settings.SQL_DATABASE}"
    f"?driver={quote_plus(settings.SQL_DRIVER)}"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# # Check database connection
# def check_database_connection():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))
#             print("✅ Database connected successfully")
#             return True

#     except Exception as e:
#         print("❌ Database connection failed")
#         print("Error:", e)
#         return False


# check_database_connection()