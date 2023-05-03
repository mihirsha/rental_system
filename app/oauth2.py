from jose import JWTError, jwt
from app.config import settings
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.schema.UserSchema import TokenData
from app.database.database import get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')


SECRET_KEY = settings.secret_key
ALORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expiry


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALORITHM)

    return encoded_jwt


def verify_access_token(token: str, credenctial_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALORITHM)
        id: str = payload.get("users_id")
        if id is None:
            raise credenctial_exception
        else:
            tokenData = TokenData(id=id)

    except JWTError:
        raise credenctial_exception


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credenctial_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credenctial_exception)

    user = db.query(User).filter(User.id == token.id).first()

    return user
