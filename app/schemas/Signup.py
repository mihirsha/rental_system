from pydantic import BaseModel


class Signup(BaseModel):
    email: str
    password: str
    phoneNumber: int
    name: str
