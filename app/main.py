from fastapi import FastAPI
from app.controller import UserController, AuthorController, BookController, GenreController, BookDetailController
import app.auth as auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(UserController.router)
app.include_router(BookController.router)
app.include_router(BookDetailController.router)
app.include_router(GenreController.router)
app.include_router(AuthorController.router)


@app.get("/")
async def root():
    return {"message": "Hey this is Backend"}
