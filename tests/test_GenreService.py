
from app.schema.GenreSchema import GenresResponse
import pytest


@pytest.mark.parametrize("name, status_code", [
    ("Action", 201),
    ("Romantic", 201),
    ("Thriller", 201),
])
def test_create_a_genre(client, name, status_code):
    res = client.post(f"/genre/add?genre={name}")
    assert res.status_code == status_code


@pytest.mark.parametrize("name, status_code", [
    ("Romantic", 406),
    ("Thriller", 406),
])
def test_create_a_genre_which_already_exists(client, name, status_code):
    res = client.post(f"/genre/add?genre={name}")
    res = client.post(f"/genre/add?genre={name}")
    assert res.status_code == status_code


@pytest.mark.parametrize("name, status_code", [
    ("Romantic", 200),
    ("Thriller", 200),
])
def test_delete_genre(client, name, status_code):
    res = client.post(f"/genre/add?genre={name}")
    res = client.delete(f"/genre/delete?genre={name}")
    assert res.status_code == status_code


def test_to_fetch_books_of_one_genre(client, create_books):
    res = client.get("/genre/get?genre=Action")
    genre = GenresResponse(**res.json())
    assert len(genre.books) == 0
    assert res.status_code == 200
