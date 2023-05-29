from typing import Optional
from pydantic import BaseModel
from fastapi import File
from typing import Annotated


class updateBookUser(BaseModel):
    user_id: int
    book_id: int


class Genres(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Author(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookDetailInput(BaseModel):
    book_id: int
    rental_price: int
    rental_period: int
    availability: bool

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[Author]
    genres: list[Genres]

    class Config:
        orm_mode = True


class UserBook(BaseModel):
    name: str
    email: str
    phoneNumber: str

    class Config:
        orm_mode = True


class BookResponse(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[Author]
    genres: list[Genres]
    bookDetail: list[BookDetailInput]
    userRented: Optional[UserBook] = None

    class Config:
        orm_mode = True


class BookResponse_file(BaseModel):
    book: BookResponse

    class Config:
        orm_mode = True


class Book(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[int]
    genres: list[int]
