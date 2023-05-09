from typing import Optional
from pydantic import BaseModel


class CartInputs(BaseModel):
    user_id: int
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


class BookDetails(BaseModel):
    availability: Optional[bool] = False

    class Config:
        orm_mode = True


class BookOut(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[Author]
    genres: list[Genres]
    bookDetail: list[BookDetails]

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
