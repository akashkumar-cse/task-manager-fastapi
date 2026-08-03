"""
Database connection setup.

Uses MySQL running via XAMPP (default: localhost, port 3306, user 'root', no password).
Create the database once in phpMyAdmin or the MySQL CLI:

    CREATE DATABASE task_tracker;

If your XAMPP MySQL uses a different user/password, edit DATABASE_URL below.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format: mysql+pymysql://<user>:<password>@<host>:<port>/<db_name>
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/task_tracker"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency: yields a DB session per request, closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
