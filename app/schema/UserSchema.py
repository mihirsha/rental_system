from typing import Optional
from pydantic import BaseModel


class Signup(BaseModel):
    email: str
    password: str
    phoneNumber: str
    name: str


class Userlogin(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None


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


class BookOut(BaseModel):
    title: str
    description: Optional[str] = None
    authors: list[Author]
    genres: list[Genres]

    class Config:
        orm_mode = True


class CartList(BaseModel):
    rental_period: int
    books: BookOut

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    token: Optional[str] = None
    name: str
    email: str
    phoneNumber: str
    books: list[BookOut]
    cart: list[CartList]

    class Config:
        orm_mode = True


class UserOutLogin(BaseModel):
    token: Optional[str] = None
    name: str
    email: str
    phoneNumber: str

    class Config:
        orm_mode = True
