from typing import Optional
from pydantic import BaseModel


class Author(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookOutForGenre(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    authors: list[Author]

    class Config:
        orm_mode = True


class GenresResponse(BaseModel):
    id: int
    name: str
    books: list[BookOutForGenre]

    class Config:
        orm_mode: True
