from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import psycopg2


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


try:
    conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name,
                            user=settings.database_username, password=settings.database_password, port=settings.database_port)
    print("database connected")
except Exception as error:
    print("database connection failed")


def get_db():
    print("hey")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
