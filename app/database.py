from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
)  # (ya sqlalchemy.ext.declarative import declarative_base)
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_recycle=1800)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="photomath4321",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Databse connection was successful!")
except Exception as error:
    print("Connecting to database failed")
    print("Error: ", error)
    time.sleep(3)
