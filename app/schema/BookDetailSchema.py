from typing import Optional
from pydantic import BaseModel


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
    userRented: Optional[UserBook] = None

    class Config:
        orm_mode = True


class Book(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[int]
    genres: list[int]

    class Config:
        orm_mode = True


class BookDetails(BaseModel):
    rental_price: int
    rental_period: int
    availability: Optional[bool] = False

    class Config:
        orm_mode = True


class BookDetailInput(BaseModel):
    book_id: int
    rental_price: int
    rental_period: int
    availability: bool


class BookResponse(BaseModel):
    title: str
    description: Optional[str] = None
    userRented: Optional[UserBook] = None
    bookDetail: list[BookDetails] = None

    class Config:
        orm_mode = True
