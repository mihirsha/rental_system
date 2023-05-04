from typing import Optional
from pydantic import BaseModel


class ReviewUserFetch(BaseModel):
    review: str
    book_id: int


class ReviewGet(BaseModel):
    user_id: int
    review: str
    book_id: list

    class Config:
        orm_mode = True
