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


class UserOut(BaseModel):
    token: str = None
    name: str
    email: str
    phoneNumber: str

    class Config:
        orm_mode = True
