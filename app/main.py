from fastapi import FastAPI, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.database import SessionLocal, engine
from app.controller import UserController, AuthorController, BookController
import psycopg2
from app.config import settings
import app.auth as auth
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(UserController.router)
app.include_router(BookController.router)
app.include_router(AuthorController.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hey this is Backend"}
