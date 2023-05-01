from fastapi import FastAPI, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.database import SessionLocal, engine
import app.models as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hey this is Backend"}
