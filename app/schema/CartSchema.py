from typing import Optional
from pydantic import BaseModel


class CartInputs(BaseModel):
    user_id: int
    book_id: list[int]
    rental_period: list[int]
