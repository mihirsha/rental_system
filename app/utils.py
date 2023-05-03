from passlib.context import CryptContext
from app.constants import regexMobile
from re import fullmatch

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def validMobileNumber(number: str):
    if fullmatch(regexMobile, number) is None:
        return False
    else:
        return True
