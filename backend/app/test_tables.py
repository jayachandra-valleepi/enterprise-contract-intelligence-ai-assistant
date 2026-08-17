from backend.app.database.connection import create_tables

if __name__ == "__main__":
    create_tables()
    print("Application tables created successfully!")