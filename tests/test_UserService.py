import pytest
from app.service.UserService import Signup
from fastapi.testclient import TestClient
from app.main import app
from alembic.script import ScriptDirectory
from app.schema.UserSchema import UserOut
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


def test_get_db():

    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = test_get_db

# alembic_cfg = Config('alembic.ini')
# alembic_cfg.set_main_option("script_location", "alembic")
# alembic_cfg.set_main_option(
#     "sqlalchemy.url", f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test')
# alembic_cfg.set_section_option(
#     "mysection", f"{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}", f"{settings.database_name}_test")

app.dependency_overrides[get_db] = test_get_db


@pytest.fixture
def client():

    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_root(client):
    res = client.get("/")
    val = res.json().get("message")
    assert res.status_code == 200
    assert val == "Hey this is Backend"


def test_create_user(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": '9791121311',
        "name": "User"
    })

    # script = ScriptDirectory.from_config(alembic_cfg)

    # print(script.get_current_head())
    # print(res.json())

    new_user = UserOut(**res.json())
    assert new_user.email == "user@example.com"
    assert res.status_code == 201


def test_create_duplicate_user(client):
    client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": '9791121311',
        "name": "User"
    })

    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": '9791121311',
        "name": "User"
    })

    assert res.status_code == 406


def test_create_user_invalid_phone_number(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": '979111311',
        "name": "User"
    })

    assert res.status_code == 406


def test_create_user_empty_fields(client):
    res = client.post("/users/signup", json={
        "email": "",
        "password": "123",
        "phoneNumber": '9791121311',
        "name": "User"
    })

    assert res.status_code == 406


def test_get_user(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": '9791121311',
        "name": "User"
    })

    resGet = client.get("/users?email=user@example.com")
    user = UserOut(**resGet.json())
    assert user.email == "user@example.com"
    assert user.name == "User"
    assert resGet.status_code == 200


def test_get_user_does_not_exist(client):

    resGet = client.get("/users?email=user@example.com")
    assert resGet.status_code == 406
