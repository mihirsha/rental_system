from typing import Optional
from pydantic import BaseModel


class Genres(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookOutForAuthor(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genres: list[Genres]

    class Config:
        orm_mode = True


class AuthorForGet(BaseModel):
    id: int
    name: str
    books: list[BookOutForAuthor]

    class Config:
        orm_mode = True
