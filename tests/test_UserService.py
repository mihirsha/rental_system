
from app.schema.UserSchema import UserOut, UserOutLogin
from tests.database import client, session


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


def test_login(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": 9791121311,
        "name": "User"
    })

    resGet = client.post(
        '/login', json={
            "email": "user@example.com",
            "password": "123"
        })
    assert UserOutLogin(**resGet.json()).name == "User"
    assert UserOutLogin(**resGet.json()).email == "user@example.com"
    assert resGet.status_code == 200


def test_login_incorrect_credentials(client):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": 9791121311,
        "name": "User"
    })

    resGet = client.post(
        '/login', json={
            "email": "user@example.com",
            "password": "1223"
        })
    assert res.status_code == 201
    assert resGet.status_code == 404
