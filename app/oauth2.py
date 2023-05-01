from jose import JWTError, jwt
from app.config import settings
import datetime

SECRET_KEY = settings.secret_key
ALORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expiry


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALORITHM)

    return encoded_jwt
