from typing import Optional
from pydantic import BaseModel


class PaymentInput(BaseModel):
    book_id: list[int]
