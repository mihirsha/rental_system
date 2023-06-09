from typing import Optional
from pydantic import BaseModel


class CartDelete(BaseModel):
    book_id: list[int]


class CartInputs(BaseModel):
    book_id: list[int]
    rental_period: list[int]


class Author(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Genres(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookDetailSchema(BaseModel):
    availability: Optional[bool] = False

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[Author]
    genres: list[Genres]
    bookDetail: list[BookDetailSchema]

    class Config:
        orm_mode = True


class CartList(BaseModel):
    rental_period: int
    books: BookOut

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    name: str
    email: str
    phoneNumber: str
    cart: list[CartList]

    class Config:
        orm_mode = True
