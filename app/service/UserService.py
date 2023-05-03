from app.schemas import Signup
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database.database import get_db
from app.models import User
from app.utils import hash, validMobileNumber
from app.schemas import UserOut


class UserService:

    def signup(user: Signup,  db:  Session):
        if (user.email == None or user.email.strip() == "" or user.phoneNumber == None or
            user.phoneNumber.strip() == "" or user.name == None or user.name.strip() == "" or
                user.password == None or user.password.strip() == ""):

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Incomplete information")

        if not validMobileNumber(user.phoneNumber):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Invalid phone no.")

        user_fetched = db.query(User).filter(user.email == User.email).first()

        if user_fetched is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account {user.email} already present")
        else:
            hashed_password = hash(user.password)
            user.password = hashed_password
            new_user = User(**user.dict())

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    def get_User(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        return user
