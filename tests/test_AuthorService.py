
# from app.schema.GenreSchema import GenresResponse
# from app.schema.AuthorSchema import AuthorForGet
# from tests.database import client, session
# import pytest


# @pytest.mark.parametrize("name, status_code", [
#     ("author1", 201),
#     ("author2", 201),
#     ("author3", 201),
# ])
# def test_create_an_author(client, name, status_code):
#     res = client.post(f"/author/add?author={name}")
#     assert res.status_code == status_code


# @pytest.mark.parametrize("name, status_code", [
#     ("author1", 406),
#     ("author2", 406),
# ])
# def test_create_an_author_which_already_exists(client, name, status_code):
#     res = client.post(f"/author/add?author={name}")
#     res = client.post(f"/author/add?author={name}")
#     assert res.status_code == status_code


# @pytest.mark.parametrize("name, status_code", [
#     ("Romantic", 200),
#     ("Thriller", 200),
# ])
# def test_delete_author(client, name, status_code):
#     res = client.post(f"/author/add?author={name}")
#     res = client.delete(f"/author/delete?author={name}")
#     assert res.status_code == status_code


# def test_to_fetch_books_of_one_author(client, create_books):
#     res = client.get("/author/get?author=author1")
#     genre = AuthorForGet(**res.json())
#     assert len(genre.books) == 2
#     assert res.status_code == 200
