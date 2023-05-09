import pytest
from app.service.UserService import Signup
from fastapi.testclient import TestClient
from app.main import app
from alembic.script import ScriptDirectory
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.database.database import get_db
from alembic import command
from alembic.config import Config
from app.database.database import Base
import psycopg2


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def test_get_db():
        db = TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = test_get_db
    yield TestClient(app)
