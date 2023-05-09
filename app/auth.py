from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schema.UserSchema import *
import app.models as models
from app.utils import verify
from app.oauth2 import create_access_token
from app.schema.UserSchema import UserOutLogin


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=UserOutLogin)
def login(user_credentials: Userlogin, db:  Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return UserOutLogin(
        token=access_token,
        name=user.name,
        phoneNumber=user.phoneNumber,
        email=user.email
    )
