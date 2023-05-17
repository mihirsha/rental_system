from fastapi import FastAPI
from app.controller import UserController, AuthorController, BookController, GenreController, BookDetailController, CartController, PaymentController
import app.auth as auth
from app.jobs.newjobs import scheduler
from app.utils import send_email

from app.database.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

app = FastAPI()

# scheduler.start()

app.include_router(auth.router)
app.include_router(UserController.router)
app.include_router(BookController.router)
app.include_router(CartController.router)
app.include_router(BookDetailController.router)
app.include_router(PaymentController.router)
app.include_router(GenreController.router)
app.include_router(AuthorController.router)


@app.on_event('startup')
async def startup_event():
    scheduler.start()


@app.get('/')
async def root():
    return {"message": "Hey this is Backend-------- testing"}
