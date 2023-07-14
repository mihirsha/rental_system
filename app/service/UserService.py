from time import sleep
from app.schema.UserSchema import Signup
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from app.models import User
from app.utils import hash, validMobileNumber
import json
from app.rabbitMq import publish_to_rabbitmq
import uuid


class UserService:

    def signup(user: Signup,  db:  Session):
        msg_to_be_returned = User()
        if (user.email == None or user.email.strip() == "" or user.phoneNumber == None or
            user.phoneNumber.strip() == "" or user.name == None or user.name.strip() == "" or
                user.password == None or user.password.strip() == ""):

            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Incomplete information")

        if not validMobileNumber(user.phoneNumber):
            raise HTTPException(
                status_code=406, detail=f"Invalid phone no.")

        user_fetched = db.query(User).filter(user.email == User.email).first()

        if user_fetched is not None:
            raise HTTPException(
                status_code=406, detail=f"Account {user.email} already present")
        else:
            hashed_password = hash(user.password)
            user.password = hashed_password
            new_user = User(**user.dict())

            new_user.id = str(uuid.uuid4())
            user_json_string = json.dumps(new_user.to_dict())
            status = publish_to_rabbitmq(user_json_string)

            if status == 200:
                return 200, new_user
            return 406, new_user

    def getUser(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if user == None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Account {email} does not exists")
        return user
