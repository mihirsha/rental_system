from fastapi import status, Depends, APIRouter
from app.schema.UserSchema import Signup
from sqlalchemy.orm import Session
from app.service.UserService import *
from app.database.database import get_db
from app.schema.UserSchema import UserOut
from app.oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def signup(user: Signup, db:  Session = Depends(get_db)):
    return UserService.signup(user, db)


@router.get("", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_current_user(db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = UserService.getUser(email, db)
    return user
