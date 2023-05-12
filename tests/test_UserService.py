
from app.schema.UserSchema import UserOut, UserOutLogin
from fastapi import Depends, status, HTTPException
from app.oauth2 import verify_access_token
import pytest


# def test_root(client):
#     res = client.get("/")
#     val = res.json().get("message")
#     assert res.status_code == 200
#     assert val == "Hey this is Backend"


@pytest.mark.parametrize("email, password, phoneNumber, name, status_code", [
    ("user@example.com", "123", "9791121311", "user", 406),
    ("mihirshah0114@gmail.com", "123234", "9792354657", "user2", 406)
])
def test_create_duplicate_user(client, email, password, phoneNumber, name, status_code):
    client.post("/users/signup", json={
        "email": email,
        "password": password,
        "phoneNumber": phoneNumber,
        "name": name,
    })
    res = client.post("/users/signup", json={
        "email": email,
        "password": password,
        "phoneNumber": phoneNumber,
        "name": name,
    })
    assert res.status_code == status_code


@pytest.mark.parametrize("email, password, phoneNumber, name, status_code", [
    ("user@example.com", "123", "9791121311", "user", 201),
    ("mihirshah0114@gmail.com", "123234", "9792354657", "user2", 201),
    ("mihirshah@gmail.com", "password123", "9364725821", "user", 201),
    ("newuser@example.com", "newpassword", "9791121311", "user2", 201),
    (None, "123", "9791121311", "user", 422),
    ("", "123", "9791121311", "user", 406)
])
def test_create_user(client, email, password, phoneNumber, name, status_code):
    res = client.post("/users/signup", json={
        "email": email,
        "password": password,
        "phoneNumber": phoneNumber,
        "name": name,
    })
    assert res.status_code == status_code


@pytest.mark.parametrize("email, password, phoneNumber, name, status_code", [
    ("user@example.com", "123", "9791121311", "user", 201),
    (None, "123", "9791121311", "user", 422),
    ("", "123", "9791121311", "user", 406),
    ("user@example.com", "123", "9791", "user", 406),
    ("user@example.com", "", "9791", "", 406),
    ("user@example.com", None, "9791", "", 422),
    ("user@example.com", "123", "9791", None, 422),
])
def test_create_user_empty_fields(client, email, password, phoneNumber, name, status_code):
    res = client.post("/users/signup", json={
        "email": email,
        "password": password,
        "phoneNumber": phoneNumber,
        "name": name
    })

    assert res.status_code == status_code


def test_get_user(authorized_client):

    resGet = authorized_client.get("/users")

    user = UserOut(**resGet.json())
    assert user.email == "user@example.com"
    assert user.name == "user"
    assert resGet.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("user@example.com", "123", 404)
])
def test_get_user_does_not_exist(client, email, password, status_code):
    resGet = client.post("/login", json={
        "email": email,
        "password": password
    })
    assert resGet.status_code == status_code


def test_login(client, test_user):
    resGet = client.post(
        '/login', json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
    credenctial_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    user = UserOutLogin(**resGet.json())
    assert resGet.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("user@example.comm", "123", 404),
    (None, "123", 422),
    ("mihirshah0114@gmail.com", None, 422),
    ("user@example.com", "wrongpwd", 403),
    ("user@example.com", "dskbsjdb", 403),
])
def test_login_incorrect_credentials(client, email, password, status_code):
    res = client.post("/users/signup", json={
        "email": "user@example.com",
        "password": "123",
        "phoneNumber": 9791121311,
        "name": "User"
    })

    resGet = client.post(
        '/login', json={
            "email": email,
            "password": password
        })
    assert res.status_code == 201
    assert resGet.status_code == status_code
