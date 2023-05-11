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
from app.schema.UserSchema import UserOut
from app.oauth2 import create_access_token
from app.database.database import Base
from app.models import Authors, Genre
import psycopg2


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port_testing}/{settings.database_name}_test'

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


@pytest.fixture
def test_user(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": "9791121311",
        "name": "user",
    })
    user = UserOut(**res.json())
    assert res.status_code == 201
    return {"email": "user@example.com", "password": "123", "id": user.id}


@pytest.fixture
def token(test_user):
    access_token = create_access_token({"user_id": test_user["id"]})
    return access_token


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers,
                      "Authentication": f"{token}"}
    return client


@pytest.fixture
def create_authors(session):
    add_authors = ["author1", "author2", "author3"]

    def create_author_model(author):
        return Authors(name=author)

    db_arr = list(map(create_author_model, add_authors))

    session.add_all(db_arr)
    session.commit()


@pytest.fixture
def create_genres(session):
    add_genre = ["Action", "Thriller", "Romance"]

    def create_genre_model(genre):
        return Genre(name=genre)

    db_arr = list(map(create_genre_model, add_genre))

    session.add_all(db_arr)
    session.commit()


@pytest.fixture
def create_books(client, session, create_genres, create_authors):
    res = client.post("/book/addBook", json={
        "title": "My Book",
        "description": "desc",
        "authors": [1],
        "genres": [1, 2]
    })

    res = client.post("/book/addBook", json={
        "title": "My Book 2",
        "description": "desc",
        "authors": [1],
        "genres": [1, 3]
    })

    assert res.status_code == 201
